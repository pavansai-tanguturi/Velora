import socket
import threading
import subprocess
import sys
import os
import time

def receive_messages(sock, name):
    """Continuously receive and display messages from the server"""
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg:
                # Clean the received message from any escape characters
                clean_msg = msg.replace('\\', '').strip()
                print(f"{clean_msg}")
            else:
                break
        except Exception as e:
            print(f"\n[ERROR] Connection lost: {e}")
            sock.close()
            break

def send_messages(sock, name):
    """Handle user input and send messages to server"""
    try:
        while True:
            user_input = input("").strip()
            if user_input:
                if user_input.lower() == '/quit':
                    break
                # Clean user input from escape characters
                clean_input = user_input.replace('\\', '').replace('\n', '').replace('\r', '')
                full_msg = f"{name}: {clean_input}"
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
        print("[INFO] Type '/quit' to exit the chat")
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