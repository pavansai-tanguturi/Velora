import socket
import threading
import json
import base64

# Server config
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5003       # Local port (ngrok will tunnel this)

# Keep track of connected clients
clients = []
lock = threading.Lock()


def recv_exact(conn, n):
    """Receive exactly n bytes or return fewer if the connection closed."""
    data = b''
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            # connection closed or no more data
            return data
        data += chunk
    return data

def handle_client(conn, addr):
    """Handle individual client connections"""
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        try:
            # Try to receive length header first (10 bytes)
            try:
                # Read an exact 10-byte header. If connection closed, recv_exact returns fewer bytes.
                length_data = recv_exact(conn, 10)
                # If we got 10 bytes and they are digits, treat as length-prefixed message
                if len(length_data) == 10:
                    try:
                        header_text = length_data.decode('utf-8')
                    except Exception:
                        header_text = ''

                    if header_text.isdigit():
                        # This is a length-prefixed message (file)
                        message_length = int(header_text)

                        # Receive the full message
                        msg_data = recv_exact(conn, message_length)

                        if len(msg_data) == message_length:
                            try:
                                msg = msg_data.decode('utf-8')
                                # Try to parse as JSON (file message)
                                try:
                                    data = json.loads(msg)
                                    if data.get('type') == 'file':
                                        print(f"[FILE TRANSFER] {data['sender']} sending {data['filename']} ({data['size']} bytes)")
                                        broadcast_file(data, conn)
                                        continue
                                except json.JSONDecodeError:
                                    # Regular text message (length-prefixed)
                                    broadcast_message(msg, conn)
                                    continue
                            except Exception as e:
                                print(f"[ERROR] Failed to parse length-prefixed message: {e}")

                # If we didn't get a valid 10-byte header, treat as old-style message (for backward compatibility)
                try:
                    msg = length_data.decode('utf-8')
                except Exception:
                    msg = ''

                # Read any additional available data (blocking read up to a reasonable buffer)
                try:
                    additional = conn.recv(4096).decode('utf-8')
                    msg += additional
                except Exception:
                    # no additional data or recv failed; msg may be what we have
                    pass
            except Exception as e:
                # Fallback to regular message receiving
                try:
                    msg = conn.recv(4096).decode('utf-8')
                except Exception:
                    msg = ''
            
            if not msg:
                break
            
            # Handle old-style messages (backward compatibility)
            try:
                data = json.loads(msg)
                if data.get('type') == 'file':
                    print(f"[FILE TRANSFER] {data['sender']} sending {data['filename']} ({data['size']} bytes)")
                    broadcast_file(data, conn)
                else:
                    broadcast_message(msg, conn)
            except json.JSONDecodeError:
                # Regular text message (old-style, no length prefix)
                broadcast_message(msg, conn)
                
        except Exception as e:
            print(f"[ERROR] Error handling client {addr}: {e}")
            break
    
    # Clean up connection
    with lock:
        if conn in clients:
            clients.remove(conn)
    conn.close()
    print(f"[DISCONNECTED] {addr} left.")

def broadcast_message(message, sender_conn):
    """Broadcast text message to all clients except sender"""
    with lock:
        disconnected_clients = []
        for client in clients:
            if client != sender_conn:
                try:
                    # Send as length-prefixed message for protocol consistency
                    msg_bytes = message.encode('utf-8')
                    msg_len = len(msg_bytes)
                    header = f"{msg_len:010d}".encode('utf-8')
                    client.sendall(header)
                    client.sendall(msg_bytes)
                except:
                    disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            clients.remove(client)
            client.close()

def broadcast_file(file_data, sender_conn):
    """Broadcast file to all clients except sender"""
    with lock:
        disconnected_clients = []
        file_message = json.dumps(file_data)
        message_length = len(file_message.encode('utf-8'))
        length_header = f"{message_length:010d}".encode('utf-8')
        
        for client in clients:
            if client != sender_conn:
                try:
                    client.sendall(length_header)
                    client.sendall(file_message.encode('utf-8'))
                except:
                    disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            clients.remove(client)
            client.close()

def start():
    """Start the server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER STARTED] File sharing server listening on port {PORT}...")
    print("[INFO] Supports text messages and file transfers")

    while True:
        conn, addr = server.accept()
        with lock:
            clients.append(conn)
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down...")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")