import socket
import threading
import subprocess
import sys
import os
import time

def receive_messages(sock, name):
    """Continuously receive and display messages from the server"""
    buffer = ""
    while True:
        try:
            data = sock.recv(8192).decode('utf-8')  # Larger buffer for files
            if data:
                buffer += data
                
                # Check if we have complete messages
                while buffer:
                    if buffer.startswith("FILE:"):
                        # Look for newline delimiter
                        newline_pos = buffer.find('\n')
                        if newline_pos > 0:
                            # We have a complete file message
                            file_data = buffer[5:newline_pos]  # Remove "FILE:" prefix
                            receive_file(file_data)
                            buffer = buffer[newline_pos + 1:]
                        else:
                            # Incomplete message, wait for more data
                            break
                    else:
                        # Handle regular message
                        newline_pos = buffer.find('\n')
                        if newline_pos == -1:
                            newline_pos = len(buffer)
                        
                        msg = buffer[:newline_pos]
                        if msg.strip():
                            clean_msg = msg.replace('\\', '').strip()
                            print(f"{clean_msg}")
                        buffer = buffer[newline_pos+1:]
                        break
                
                # Handle any remaining regular messages
                if buffer and not buffer.startswith("FILE:"):
                    lines = buffer.split('\n')
                    for line in lines[:-1]:  # Process all complete lines
                        if line.strip():
                            clean_msg = line.replace('\\', '').strip()
                            print(f"{clean_msg}")
                    buffer = lines[-1]  # Keep the last incomplete line
                    
            else:
                break
        except Exception as e:
            print(f"\n[ERROR] Connection lost: {e}")
            sock.close()
            break

def send_file(sock, name, file_path):
    """Send a file through the chat"""
    try:
        import base64
        
        # Get file info
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Check if file exists and has content
        if file_size == 0:
            print(f"[ERROR] File is empty: {file_path}")
            return
        
        # Check file size limit (5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if file_size > max_size:
            print(f"[ERROR] File too large ({file_size} bytes). Maximum size is 5MB")
            return
        
        print(f"[INFO] Sending file '{file_name}' ({file_size:,} bytes)...")
        
        # Read and encode file
        with open(file_path, 'rb') as f:
            file_data = f.read()
            encoded_data = base64.b64encode(file_data).decode('utf-8')
        
        # Create file message
        file_msg = {
            "type": "file",
            "sender": name,
            "filename": file_name,
            "size": file_size,
            "data": encoded_data
        }

        import json
        file_json = json.dumps(file_msg)
        message = f"FILE:{file_json}\n".encode('utf-8')  # Add newline delimiter
        
        # Send in smaller chunks with error handling
        chunk_size = 1024  # Smaller chunks for reliability
        total_sent = 0
        
        while total_sent < len(message):
            try:
                chunk = message[total_sent:total_sent + chunk_size]
                sent = sock.send(chunk)
                if sent == 0:
                    raise Exception("Socket connection broken")
                total_sent += sent
                
                # Small delay to prevent overwhelming
                if total_sent % (chunk_size * 10) == 0:
                    time.sleep(0.01)
                    
            except (socket.error, BrokenPipeError) as e:
                raise Exception(f"Connection lost while sending file: {e}")
            except Exception as e:
                raise Exception(f"Unexpected error: {e}")
        
        print(f"[INFO] File '{file_name}' sent successfully!")
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except PermissionError:
        print(f"[ERROR] Permission denied accessing file: {file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to send file: {e}")

def receive_file(file_data):
    """Receive and save a file"""
    try:
        import base64
        import json
        
        # Parse file data
        file_info = json.loads(file_data)
        filename = file_info['filename']
        sender = file_info['sender']
        file_size = file_info['size']
        encoded_data = file_info['data']
        
        # Decode file data
        file_data = base64.b64decode(encoded_data.encode('utf-8'))
        
        # Create downloads directory if not exists
        downloads_dir = "downloads"
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        # Save file with sender prefix
        safe_filename = f"{sender}_{filename}"
        file_path = os.path.join(downloads_dir, safe_filename)
        
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        print(f"\n📁 File received: '{filename}' from {sender}")
        print(f"   Saved as: {file_path} ({file_size:,} bytes)")
        print("You: ", end="")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to receive file: {e}")

def send_messages(sock, name):
    """Handle user input and send messages to server"""
    try:
        print("\n💡 Commands:")
        print("   - Type messages normally to chat")
        print("   - /file <path> to send a file")
        print("   - /quit to exit")
        print()
        
        while True:
            user_input = input("").strip()
            if user_input:
                if user_input.lower() == '/quit':
                    break
                elif user_input.startswith('/file '):
                    # Send file
                    file_path = user_input[6:].strip()  # Remove '/file '
                    # Remove quotes if present
                    file_path = file_path.strip('\'"')
                    if os.path.exists(file_path):
                        send_file(sock, name, file_path)
                    else:
                        print(f"[ERROR] File not found: {file_path}")
                else:
                    # Send regular message
                    clean_input = user_input.replace('\\', '').replace('\n', '').replace('\r', '')
                    full_msg = f"{name}: {clean_input}\n"  # Add newline for consistency
                    sock.send(full_msg.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n[INFO] Disconnecting...")
    except Exception as e:
        print(f"\n[ERROR] Failed to send message: {e}")

def connect_to_server():
    """Get server connection details from user"""
    print("=== Velora Socket Chat ===")
    print("Connect to a chat server using IP address and port")
    print()
    
    # Get user details
    name = input("Enter your name: ").strip()
    # Remove any escape characters and clean the name
    name = name.replace('\\', '').replace('\n', '').replace('\r', '')
    if not name:
        print("[ERROR] Name cannot be empty")
        return None, None, None
    
    print("\nConnection Options:")
    print("1. Connect to local server (127.0.0.1:5003)")
    print("2. Connect to remote server (create/join room)")
    print("3. Connect using ngrok tunnel (global access)")
    
    choice = input("\nChoose option (1/2/3): ").strip()
    
    if choice == "1":
        host = "127.0.0.1"
        port = 5003
    elif choice == "2":
        room_choice = input("Do you want to create a room or join a room? (create/join): ").strip().lower()
        
        if room_choice == "create":
            # Start server and show user's IP
            start_server()
            
            # Get user's IP address
            try:
                result = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True)
                user_ip = result.stdout.strip()
                print(f"\n[INFO] Server started on your IP: {user_ip}")
                print(f"[INFO] Others should connect to: {user_ip}:5003")
                host = "127.0.0.1"  # Connect locally as the host
                port = 5003
            except Exception:
                print("[ERROR] Could not determine your IP address")
                print("[INFO] Server started locally. Use ifconfig to find your IP to share.")
                host = "127.0.0.1"
                port = 5003
                
        elif room_choice == "join":
            # Join existing room
            host = input("Enter room creator's IP address: ").strip()
            try:
                port = int(input("Enter server port (usually 5003): ").strip())
            except ValueError:
                print("[ERROR] Invalid port number")
                return None, None, None
        else:
            print("[ERROR] Invalid choice. Please enter 'create' or 'join'")
            return None, None, None
    elif choice == "3":
        ngrok_choice = input("Do you want to create ngrok tunnel or join existing ngrok? (create/join): ").strip().lower()
        
        if ngrok_choice == "create":
            # Start server first
            start_server()
            
            # Start ngrok TCP tunnel
            print("[INFO] Starting ngrok tunnel...")
            try:
                ngrok_process = subprocess.Popen(
                    ["ngrok", "tcp", "5003"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                time.sleep(3)  # Wait for ngrok to start
                
                # Get ngrok URL
                result = subprocess.run(["curl", "-s", "http://127.0.0.1:4040/api/tunnels"], capture_output=True, text=True)
                import json
                tunnels = json.loads(result.stdout)
                public_url = tunnels['tunnels'][0]['public_url']
                ngrok_host_port = public_url.replace("tcp://", "")

                print(f"[INFO] Share this with others to join: {ngrok_host_port}")
                
                # Connect through ngrok tunnel (same as others)
                host, port_str = ngrok_host_port.split(":")
                port = int(port_str)
                
            except Exception as e:
                print(f"[ERROR] Failed to start ngrok: {e}")
                print("[INFO] Make sure ngrok is installed and try again")
                return None, None, None
                
        elif ngrok_choice == "join":
            # Join existing ngrok tunnel
            ngrok_url = input("Enter ngrok TCP URL (e.g., 0.tcp.ngrok.io:12345): ").strip()
            try:
                if ":" in ngrok_url:
                    host, port_str = ngrok_url.split(":")
                    port = int(port_str)
                else:
                    print("[ERROR] Invalid ngrok URL format. Should be host:port")
                    return None, None, None
            except ValueError:
                print("[ERROR] Invalid port number in ngrok URL")
                return None, None, None
        else:
            print("[ERROR] Invalid choice. Please enter 'create' or 'join'")
            return None, None, None
    else:
        print("[ERROR] Invalid choice")
        return None, None, None
    
    return name, host, port

def main():
    """Main client application"""
    # Get connection details
    name, host, port = connect_to_server()
    if not all([name, host, port]):
        return
    
    # Create socket and connect
    try:
        # print(f"\n[INFO] Connecting to {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout for connection
        sock.connect((host, port))
        sock.settimeout(None)  # Remove timeout after connection
        print("\n[INFO] Connected to server!")
        print(f"[INFO] You are now chatting as: {name}")
        print("[INFO] Files will be saved to 'downloads' folder")
        print("=" * 50)
        
    except socket.timeout:
        print(f"[ERROR] Connection timeout. Server at {host}:{port} is not responding.")
        return
    except ConnectionRefusedError:
        print(f"[ERROR] Connection refused. No server running at {host}:{port}")
        return
    except socket.gaierror:
        print(f"[ERROR] Invalid hostname or IP address: {host}")
        return
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")
        return
    
    try:
        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(
            target=receive_messages, 
            args=(sock, name), 
            daemon=True
        )
        receive_thread.start()
        
        # Handle sending messages in main thread
        send_messages(sock, name)
        
    except KeyboardInterrupt:
        print("\n[INFO] Chat interrupted by user")
    finally:
        print("[INFO] Closing connection...")
        sock.close()
        print("[INFO] Goodbye!")

def start_server():
    # Start the server as a subprocess
    print("[INFO] Starting the server...")
    subprocess.Popen(
        ["python3", os.path.join(os.path.dirname(__file__), "server.py")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)

def show_help():
    """Display help information"""
    help_text = """
=== Velora Socket Chat - Help ===

This is a simple socket-based chat client that connects directly to chat servers.

USAGE:
    python client_socket_only.py

CONNECTION OPTIONS:
    1. Local Server: Connect to 127.0.0.1:5003 (for testing)
    2. Remote Server: Connect using IP address and port
    3. Domain Server: Connect using domain name and port

CHAT COMMANDS:
    /quit - Exit the chat

EXAMPLES:
    Local:     127.0.0.1:5003
    Remote:    192.168.1.100:5003
    Domain:    mychatserver.com:5003

REQUIREMENTS:
    - Python 3.6+
    - Network access to the server
    - Server must be running and accessible

GLOBAL CONNECTIVITY:
    For global access, the server must be:
    - Running on a public IP address, OR
    - Behind port forwarding (router configuration), OR  
    - Using a VPS/cloud server, OR
    - Using reverse proxy services

TROUBLESHOOTING:
    - Connection refused: Server is not running
    - Timeout: Server is unreachable (firewall/network issue)
    - Invalid hostname: Check domain name spelling
    """
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
    else:
        main()
        '/Users/pavansaitanguturi/Desktop/Screenshot 2025-07-20 at 12.33.05 PM.png'