import socket
import threading

# Server config
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5003       # Local port (ngrok will tunnel this)

# Keep track of connected clients
clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    buffer = ""
    while True:
        try:
            # Receive data with larger buffer for files
            data = conn.recv(8192).decode('utf-8')
            if not data:
                break
            
            buffer += data
            
            # Process complete messages
            while buffer:
                if buffer.startswith("FILE:"):
                    # Handle file message - look for newline delimiter
                    newline_pos = buffer.find('\n')
                    if newline_pos > 0:
                        # Complete file message
                        complete_msg = buffer[:newline_pos]
                        print(f"[FILE TRANSFER] {addr} sent a file")
                        broadcast(complete_msg, conn)
                        buffer = buffer[newline_pos + 1:]
                    else:
                        # Incomplete, wait for more data
                        break
                else:
                    # Handle regular message
                    newline_pos = buffer.find('\n')
                    if newline_pos == -1:
                        # No complete message yet
                        break
                    
                    msg = buffer[:newline_pos]
                    if msg.strip():
                        broadcast(msg, conn)
                    buffer = buffer[newline_pos+1:]
                    
        except Exception as e:
            print(f"[ERROR] Client {addr}: {e}")
            break
            
    conn.close()
    if conn in clients:
        clients.remove(conn)
    print(f"[DISCONNECTED] {addr} left.")

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                # Ensure message ends with newline for proper formatting
                if not message.endswith('\n'):
                    message += '\n'
                client.send(message.encode('utf-8'))
            except:
                pass

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER STARTED] Listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start()