import socket
import threading
import subprocess
import sys
import os
import time
import base64
import json

def recv_exact(sock, n):
    """Receive exactly n bytes or return fewer if the connection closed."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            return data
        data += chunk
    return data

def receive_messages(sock, name):
    """Continuously receive and display messages from the server"""
    while True:
        try:
            # All messages now use length-prefixed protocol
            length_data = recv_exact(sock, 10)
            if len(length_data) != 10:
                # Connection closed or partial read
                break
                
            try:
                header_text = length_data.decode('utf-8')
            except Exception:
                break
                
            if not header_text.isdigit():
                # Invalid header, connection might be corrupted
                break
                
            message_length = int(header_text)
            
            # Receive the full message
            msg_data = recv_exact(sock, message_length)
            if len(msg_data) != message_length:
                # Incomplete message received
                break
                
            try:
                msg = msg_data.decode('utf-8')
                
                # Try to parse as JSON first (for file transfers)
                try:
                    data = json.loads(msg)
                    if data.get('type') == 'file':
                        handle_file_receive(data)
                        continue
                except json.JSONDecodeError:
                    pass
                
                # Regular text message
                clean_msg = msg.replace('\\', '').strip()
                print(f"{clean_msg}")
                
            except Exception as e:
                print(f"\n[ERROR] Failed to decode message: {e}")
                
        except Exception as e:
            print(f"\n[ERROR] Connection lost: {e}")
            sock.close()
            break

def handle_file_receive(data):
    """Handle receiving a file"""
    try:
        filename = data['filename']
        file_data = base64.b64decode(data['content'])
        sender = data['sender']
        
        # Get user's Downloads folder
        import os
        home_dir = os.path.expanduser("~")
        downloads_dir = os.path.join(home_dir, "Downloads")
        
        # Create downloads directory if it doesn't exist (shouldn't be needed on most systems)
        os.makedirs(downloads_dir, exist_ok=True)
        
        # Handle duplicate filenames by adding (1), (2), etc.
        base_name, ext = os.path.splitext(filename)
        file_path = os.path.join(downloads_dir, filename)
        counter = 1
        
        while os.path.exists(file_path):
            new_filename = f"{base_name} ({counter}){ext}"
            file_path = os.path.join(downloads_dir, new_filename)
            counter += 1
        
        # Save the file
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        print(f"\n[FILE] {sender} sent you a file: {os.path.basename(file_path)}")
        print(f"[FILE] Saved to: {file_path}")
        print()  # Add blank line after file receive notification
        
    except Exception as e:
        print(f"\n[ERROR] Failed to receive file: {e}")

def send_messages(sock, name):
    """Handle user input and send messages/files to server"""
    print("\nCommands:")
    print("  /file <path>  - Send a file")
    print("  /quit         - Exit chat")
    print("  Just type     - Send text message")
    
    try:
        while True:
            user_input = input("").strip()
            if user_input:
                if user_input.lower() == '/quit':
                    break
                elif user_input.startswith('/file '):
                    # Send file
                    file_path = user_input[6:].strip()
                    send_file(sock, name, file_path)
                else:
                    clean_input = user_input.replace('\\', '').replace('\n', '').replace('\r', '')
                    full_msg = f"{name}: {clean_input}"
                    message_bytes = full_msg.encode('utf-8')
                    message_length = len(message_bytes)
                    length_header = f"{message_length:010d}".encode('utf-8')
                    sock.sendall(length_header)
                    sock.sendall(message_bytes)
    except KeyboardInterrupt:
        print("\n[INFO] Disconnecting...")
    except Exception as e:
        print(f"\n[ERROR] Failed to send message: {e}")

def send_file(sock, name, file_path):
    """Send a file to the server"""
    try:
        if not os.path.exists(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return
        
        # Check file size (limit to 1MB for now to avoid large message issues)
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"[ERROR] File is empty: {file_path}")
            return
        if file_size > 1 * 1024 * 1024 * 1024:  # 1GB limit
            print("[ERROR] File too large. Maximum size is 1GB.")
            return
        
        print(f"[INFO] Reading file: {file_path} ({file_size} bytes)")
        
        # Read and encode file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        if len(file_data) != file_size:
            print(f"[ERROR] Failed to read complete file. Expected {file_size}, got {len(file_data)}")
            return
        
        encoded_data = base64.b64encode(file_data).decode('utf-8')
        filename = os.path.basename(file_path)
        
        # Create file message
        file_message = {
            'type': 'file',
            'filename': filename,
            'content': encoded_data,
            'sender': name,
            'size': file_size
        }
        
        # Convert to JSON and send with length prefix
        json_data = json.dumps(file_message)
        message_length = len(json_data.encode('utf-8'))
        
        # Send message length first, then the message
        length_header = f"{message_length:010d}".encode('utf-8')  # 10-digit length
        sock.sendall(length_header)
        sock.sendall(json_data.encode('utf-8'))
        
        print(f"[FILE] Sent: {filename} ({file_size} bytes)")
        print()  # Add blank line after file send confirmation
        
    except Exception as e:
        print(f"[ERROR] Failed to send file: {e}")
        import traceback
        traceback.print_exc()

def connect_to_server():
    """Get server connection details from user"""
    print("=== Velora Chat with File Sharing ===")
    print("Chat and share files securely")
    print()
    
    # Get user details
    name = input("Enter your name: ").strip()
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
        start_server()
        host = "127.0.0.1"
        port = 5003
    elif choice == "2":
        room_choice = input("Do you want to create a room or join a room? (create/join): ").strip().lower()
        
        if room_choice == "create":
            start_server()
            try:
                result = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True)
                user_ip = result.stdout.strip()
                print(f"\n[INFO] Server started on your IP: {user_ip}")
                print(f"[INFO] Others should connect to: {user_ip}:5003")
                host = "127.0.0.1"
                port = 5003
            except Exception:
                print("[ERROR] Could not determine your IP address")
                print("[INFO] Server started locally. Use ifconfig to find your IP to share.")
                host = "127.0.0.1"
                port = 5003
                
        elif room_choice == "join":
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
            start_server()
            print("[INFO] Starting ngrok tunnel...")
            try:
                ngrok_process = subprocess.Popen(
                    ["ngrok", "tcp", "5003"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                time.sleep(3)
                
                result = subprocess.run(["curl", "-s", "http://127.0.0.1:4040/api/tunnels"], capture_output=True, text=True)
                import json
                tunnels = json.loads(result.stdout)
                public_url = tunnels['tunnels'][0]['public_url']
                ngrok_host_port = public_url.replace("tcp://", "")

                print(f"[INFO] Share this with others to join: {ngrok_host_port}")
                
                host, port_str = ngrok_host_port.split(":")
                port = int(port_str)
                
            except Exception as e:
                print(f"[ERROR] Failed to start ngrok: {e}")
                print("[INFO] Make sure ngrok is installed and try again")
                return None, None, None
                
        elif ngrok_choice == "join":
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
    name, host, port = connect_to_server()
    if not all([name, host, port]):
        return
    
    try:
        print(f"\n[INFO] Connecting to server...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        sock.settimeout(None)
        print("[INFO] Connected to server!")
        print(f"[INFO] You are now chatting as: {name}")
        print(f"[INFO] Files will be saved to: {os.path.join(os.path.expanduser('~'), 'Downloads')}")
        print("=" * 50)
        
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")
        return
    
    try:
        receive_thread = threading.Thread(
            target=receive_messages, 
            args=(sock, name), 
            daemon=True
        )
        receive_thread.start()
        
        send_messages(sock, name)
        
    except KeyboardInterrupt:
        print("\n[INFO] Chat interrupted by user")
    finally:
        print("[INFO] Closing connection...")
        sock.close()
        print("[INFO] Goodbye!")

def start_server():
    """Start the server as a subprocess"""
    print("[INFO] Starting the server...")
    subprocess.Popen(
        ["python3", os.path.join(os.path.dirname(__file__), "server_with_files.py")],
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

def quick_share():
    """Quick file sharing mode - share a file and exit"""
    if len(sys.argv) < 3:
        print("Usage: python client_with_files.py share <file_path> [server_address]")
        print("Examples:")
        print("  python client_with_files.py share /path/to/file.pdf                    # Local server")
        print("  python client_with_files.py share /path/to/file.pdf 192.168.1.100     # IP address (port 5003)")
        print("  python client_with_files.py share /path/to/file.pdf 192.168.1.100:8080 # IP with custom port")
        print("  python client_with_files.py share /path/to/file.pdf 0.tcp.ngrok.io:12345 # ngrok URL")
        return
    
    file_path = sys.argv[2]
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return
    
    # Get file info
    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    
    if file_size == 0:
        print(f"[ERROR] File is empty: {file_path}")
        return
    
    if file_size > 1 * 1024 * 1024 * 1024:  # 1GB limit
        print(f"[ERROR] File too large ({file_size} bytes). Maximum size is 1GB.")
        return
    
    print(f"=== Velora Quick Share ===")
    print(f"File: {filename} ({file_size} bytes)")
    print()
    
    # Get connection details
    if len(sys.argv) >= 4:
        # Server address provided (IP, IP:port, or ngrok URL)
        server_address = sys.argv[3]
        try:
            if ":" in server_address:
                # Has port specified
                host, port_str = server_address.split(":", 1)
                port = int(port_str)
            else:
                # Just IP address, use default port
                host = server_address
                port = 5003
            
            print(f"[INFO] Will connect to remote server: {host}:{port}")
            
        except ValueError:
            print("[ERROR] Invalid port number in server address")
            return
    else:
        # Use local server
        start_server()
        host = "127.0.0.1"
        port = 5003
        print("[INFO] Started local server. Others can connect to your IP on port 5003")
    
    # Get sender name
    sender_name = input("Enter your name: ").strip() or "Anonymous"
    sender_name = sender_name.replace('\\', '').replace('\n', '').replace('\r', '')
    
    try:
        print(f"[INFO] Connecting to {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        sock.settimeout(None)
        print("[INFO] Connected!")
        
        # Send the file immediately
        print(f"[INFO] Sending {filename}...")
        send_file(sock, sender_name, file_path)
        
        print("[INFO] File sent successfully!")
        print("[INFO] Keeping connection open for 30 seconds...")
        
        # Keep connection alive briefly to allow download
        time.sleep(30)
        
    except Exception as e:
        print(f"[ERROR] Failed to share file: {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        print("[INFO] Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            show_help()
        elif sys.argv[1] == 'share':
            quick_share()
        else:
            print("Unknown command. Use 'share' to quick-share a file or '-h' for help.")
    else:
        main()