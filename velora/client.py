#!/usr/bin/env python3
"""
Velora Client - Chat client with file sharing capabilities
"""

import socket
import threading
import subprocess
import sys
import os
import time
import base64
import json
from datetime import datetime


def recv_exact(sock, n):
    """Receive exactly n bytes or return fewer if the connection closed."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            return data
        data += chunk
    return data


def show_progress_bar(current, total, start_time, width=40):
    """Display a progress bar with speed and ETA"""
    percent = min(100, (current / total) * 100)
    filled = int(width * current // total)
    bar = '█' * filled + '░' * (width - filled)
    
    elapsed = time.time() - start_time
    speed = current / elapsed if elapsed > 0 else 0
    
    # Format speed
    if speed > 1024 * 1024:
        speed_str = f"{speed / (1024 * 1024):.2f} MB/s"
    elif speed > 1024:
        speed_str = f"{speed / 1024:.2f} KB/s"
    else:
        speed_str = f"{speed:.2f} B/s"
    
    # Calculate ETA
    remaining = total - current
    eta = remaining / speed if speed > 0 else 0
    
    if eta > 3600:
        eta_str = f"{eta / 3600:.1f}h"
    elif eta > 60:
        eta_str = f"{eta / 60:.1f}m"
    else:
        eta_str = f"{eta:.0f}s"
    
    print(f"\r{bar} {percent:.1f}% | {speed_str} | ETA: {eta_str}", end='', flush=True)


def play_notification():
    """Play system notification sound"""
    try:
        if sys.platform == 'darwin':  # macOS
            os.system('afplay /System/Library/Sounds/Glass.aiff &')
        elif sys.platform == 'linux':
            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null &')
        elif sys.platform == 'win32':  # Windows
            import winsound
            winsound.MessageBeep()
    except:
        pass  # Silently fail if notification cannot be played


class VeloraClient:
    """Velora chat client with file sharing"""
    
    def __init__(self):
        self.sock = None
        self.name = None
        self.running = False
        
    def connect(self, host, port):
        """Connect to Velora server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((host, port))
            self.sock.settimeout(None)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            return False
    
    def connect_and_chat(self, host, port, name=None):
        """Connect to server and start chat session"""
        if not self.connect(host, port):
            return
            
        if not name:
            name = input("Enter your name: ").strip()
            
        self.name = name.replace('\\', '').replace('\n', '').replace('\r', '')
        
        print(f"[INFO] Connected as: {self.name}")
        print(f"[INFO] Files will be saved to: {os.path.join(os.path.expanduser('~'), 'Downloads')}")
        print("=" * 50)
        
        self.start_chat()
    
    def start_chat(self):
        """Start the chat session"""
        self.running = True
        
        # Start receive thread
        receive_thread = threading.Thread(
            target=self._receive_messages,
            daemon=True
        )
        receive_thread.start()
        
        # Handle user input
        self._send_messages()
    
    def _receive_messages(self):
        """Continuously receive and display messages from the server"""
        while self.running:
            try:
                # All messages now use length-prefixed protocol
                length_data = recv_exact(self.sock, 10)
                if len(length_data) != 10:
                    break
                    
                try:
                    header_text = length_data.decode('utf-8')
                except Exception:
                    break
                    
                if not header_text.isdigit():
                    break
                    
                message_length = int(header_text)
                
                # Receive the full message
                msg_data = recv_exact(self.sock, message_length)
                if len(msg_data) != message_length:
                    break
                    
                try:
                    msg = msg_data.decode('utf-8')
                    
                    # Try to parse as JSON first (for file transfers and commands)
                    try:
                        data = json.loads(msg)
                        if data.get('type') == 'file':
                            self._handle_file_receive(data)
                            continue
                        elif data.get('type') == 'users_list':
                            self._display_users_list(data.get('users', []))
                            continue
                    except json.JSONDecodeError:
                        pass
                    
                    # Regular text message
                    clean_msg = msg.replace('\\', '').strip()
                    print(f"{clean_msg}")
                    
                except Exception as e:
                    print(f"\n[ERROR] Failed to decode message: {e}")
                    
            except Exception as e:
                if self.running:
                    print(f"\n[WARNING] Connection lost: {e}")
                    if self._attempt_reconnection():
                        continue
                break
                
        self.running = False
    
    def _display_users_list(self, users):
        """Display list of connected users"""
        print("\n" + "="*50)
        print(f"Connected Users ({len(users)}):")
        print("="*50)
        for i, user in enumerate(users, 1):
            print(f"  {i}. {user}")
        print("="*50 + "\n")
    
    def _attempt_reconnection(self):
        """Attempt to reconnect to the server"""
        print("[INFO] Attempting to reconnect...")
        max_attempts = 3
        
        for attempt in range(1, max_attempts + 1):
            print(f"[INFO] Reconnection attempt {attempt}/{max_attempts}...")
            time.sleep(2)  # Wait before reconnecting
            
            try:
                # Store connection details
                host = self.sock.getpeername()[0] if self.sock else None
                port = self.sock.getpeername()[1] if self.sock else None
                
                if not host or not port:
                    print("[ERROR] Cannot reconnect: connection details lost")
                    return False
                
                # Close old socket
                try:
                    self.sock.close()
                except:
                    pass
                
                # Create new connection
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(5)
                self.sock.connect((host, port))
                self.sock.settimeout(None)
                
                print(f"[INFO] ✓ Reconnected successfully!")
                return True
                
            except Exception as e:
                if attempt == max_attempts:
                    print(f"[ERROR] Failed to reconnect after {max_attempts} attempts")
                    return False
        
        return False
        
    def _handle_file_receive(self, data):
        """Handle receiving a file"""
        try:
            filename = data['filename']
            file_size = data.get('size', 0)
            sender = data['sender']
            
            print(f"\n[FILE] Receiving {filename} from {sender} ({file_size} bytes)...")
            
            # Decode with progress for large files
            start_time = time.time()
            encoded_content = data['content']
            
            if file_size > 1024 * 1024:  # Show progress for files > 1MB
                print("[FILE] Decoding...")
            
            file_data = base64.b64decode(encoded_content)
            
            # Get user's Downloads folder
            home_dir = os.path.expanduser("~")
            downloads_dir = os.path.join(home_dir, "Downloads")
            
            os.makedirs(downloads_dir, exist_ok=True)
            
            # Handle duplicate filenames
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
            
            elapsed = time.time() - start_time
            print(f"\n[FILE] ✓ Received: {os.path.basename(file_path)}")
            print(f"[FILE] Saved to: {file_path}")
            print(f"[FILE] Transfer completed in {elapsed:.2f}s")
            print()
            
            # Play notification sound
            play_notification()
            
        except Exception as e:
            print(f"\n[ERROR] Failed to receive file: {e}")
    
    def _send_messages(self):
        """Handle user input and send messages/files to server"""
        print("\nCommands:")
        print("  /file <path>  - Send a file")
        print("  /help         - Show all commands")
        print("  /users        - List connected users")
        print("  /quit         - Exit chat")
        print("  Just type     - Send text message")
        print("\nTip: You can drag and drop files!")
        
        try:
            while self.running:
                user_input = input("").strip()
                if user_input:
                    if user_input.lower() == '/quit':
                        break
                    elif user_input.lower() == '/help':
                        self._show_help()
                    elif user_input.lower() == '/users':
                        self._request_users_list()
                    elif user_input.startswith('/file '):
                        file_path = user_input[6:].strip()
                        self.send_file(file_path)
                    elif os.path.isfile(user_input):
                        # Drag-and-drop support - if input is a file path, send it
                        confirm = input(f"Send file '{os.path.basename(user_input)}'? (y/n): ").lower()
                        if confirm == 'y':
                            self.send_file(user_input)
                    else:
                        self.send_message(user_input)
        except KeyboardInterrupt:
            print("\n[INFO] Disconnecting...")
        except Exception as e:
            print(f"\n[ERROR] Failed to send message: {e}")
        finally:
            self.disconnect()
    
    def _show_help(self):
        """Display help information"""
        print("\n" + "="*50)
        print("Velora Chat Commands")
        print("="*50)
        print("/file <path>     - Send a file to all users")
        print("/users           - Show list of connected users")
        print("/help            - Show this help message")
        print("/quit            - Exit the chat")
        print("\nFile Sharing:")
        print("  - Drag and drop files directly into the chat")
        print("  - Max file size: 1GB")
        print("  - All file types supported")
        print("  - Files saved to: ~/Downloads")
        print("\nTips:")
        print("  - File paths with spaces are supported")
        print("  - Quotes around paths are automatically removed")
        print("="*50 + "\n")
    
    def _request_users_list(self):
        """Request list of connected users from server"""
        try:
            # Send special command to request user list
            command_msg = json.dumps({'type': 'command', 'command': 'list_users', 'sender': self.name})
            message_length = len(command_msg.encode('utf-8'))
            length_header = f"{message_length:010d}".encode('utf-8')
            self.sock.sendall(length_header)
            self.sock.sendall(command_msg.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Failed to request users list: {e}")
    
    def send_message(self, message):
        """Send a text message"""
        if not self.sock or not self.running:
            return False
            
        try:
            clean_input = message.replace('\\', '').replace('\n', '').replace('\r', '')
            full_msg = f"{self.name}: {clean_input}"
            message_bytes = full_msg.encode('utf-8')
            message_length = len(message_bytes)
            length_header = f"{message_length:010d}".encode('utf-8')
            self.sock.sendall(length_header)
            self.sock.sendall(message_bytes)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
            return False
    
    def send_file(self, file_path):
        """Send a file to the server"""
        if not self.sock or not self.running:
            return False
            
        try:
            # Strip quotes and whitespace from file path
            file_path = file_path.strip()
            if file_path.startswith('"') and file_path.endswith('"'):
                file_path = file_path[1:-1]
            elif file_path.startswith("'") and file_path.endswith("'"):
                file_path = file_path[1:-1]
            
            # Remove backslashes often added by drag-and-drop on some systems
            file_path = file_path.replace('\\', '')
            
            if not os.path.exists(file_path):
                print(f"[ERROR] File not found: {file_path}")
                return False
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                print(f"[ERROR] File is empty: {file_path}")
                return False
                
            if file_size > 1 * 1024 * 1024 * 1024:  # 1GB limit
                print("[ERROR] File too large. Maximum size is 1GB.")
                return False
            
            filename = os.path.basename(file_path)
            print(f"[FILE] Preparing to send: {filename} ({file_size} bytes)")
            
            # Read file with progress
            start_time = time.time()
            chunk_size = 65536  # 64KB chunks
            file_data = b''
            bytes_read = 0
            
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    file_data += chunk
                    bytes_read += len(chunk)
                    
                    if file_size > 1024 * 1024:  # Show progress for files > 1MB
                        show_progress_bar(bytes_read, file_size, start_time)
            
            if file_size > 1024 * 1024:
                print()  # New line after progress bar
            
            print("[FILE] Encoding...")
            encoded_data = base64.b64encode(file_data).decode('utf-8')
            
            # Create file message
            file_message = {
                'type': 'file',
                'filename': filename,
                'content': encoded_data,
                'sender': self.name,
                'size': file_size
            }
            
            # Convert to JSON and send with length prefix
            print("[FILE] Sending...")
            json_data = json.dumps(file_message)
            message_length = len(json_data.encode('utf-8'))
            
            length_header = f"{message_length:010d}".encode('utf-8')
            self.sock.sendall(length_header)
            self.sock.sendall(json_data.encode('utf-8'))
            
            elapsed = time.time() - start_time
            print(f"[FILE] ✓ Sent: {filename} ({file_size} bytes) in {elapsed:.2f}s")
            print()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to send file: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None
        print("[INFO] Disconnected.")
    
    def start_interactive(self):
        """Start interactive connection mode"""
        print("=== Velora Chat with File Sharing ===")
        print("Chat and share files securely")
        print()
        
        # Get user details
        name = input("Enter your name: ").strip()
        name = name.replace('\\', '').replace('\n', '').replace('\r', '')
        if not name:
            print("[ERROR] Name cannot be empty")
            return
        
        print("\nConnection Options:")
        print("1. Connect to remote server (create/join room)")
        print("2. Connect using ngrok tunnel (global access)")
        
        choice = input("\nChoose option (1/2): ").strip()
        
        if choice == "1":
            room_choice = input("Do you want to create a room or join a room? (create/join): ").strip().lower()
            
            if room_choice == "create":
                self._start_server()
                try:
                    # Try macOS command first
                    result = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True)
                    user_ip = result.stdout.strip()
                    
                    # If macOS command fails, try Linux command
                    if not user_ip or result.returncode != 0:
                        result = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
                        user_ip = result.stdout.strip().split()[0] if result.stdout.strip() else ""
                    
                    if user_ip:
                        print(f"\n[INFO] Server started on your IP: {user_ip}")
                        print(f"[INFO] Others should connect to: {user_ip}:5003")
                    else:
                        print("[INFO] Server started on local network")
                        print("[INFO] Use 'ip addr' or 'ifconfig' to find your IP address")
                except Exception:
                    print("[INFO] Server started on local network")
                    print("[INFO] Use 'ip addr' or 'ifconfig' to find your IP address")
                host = "127.0.0.1"
                port = 5003
                
            elif room_choice == "join":
                host = input("Enter room creator's IP address: ").strip()
                try:
                    port = int(input("Enter server port (usually 5003): ").strip())
                except ValueError:
                    print("[ERROR] Invalid port number")
                    return
            else:
                print("[ERROR] Invalid choice. Please enter 'create' or 'join'")
                return
        elif choice == "2":
            ngrok_choice = input("Do you want to create ngrok tunnel or join existing ngrok? (create/join): ").strip().lower()
            
            if ngrok_choice == "create":
                # Check if ngrok is installed (try common locations)
                ngrok_cmd = None
                for path in ["/opt/homebrew/bin/ngrok", "/usr/local/bin/ngrok", "ngrok"]:
                    try:
                        subprocess.run([path, "--version"], capture_output=True, check=True)
                        ngrok_cmd = path
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                
                if not ngrok_cmd:
                    print("[ERROR] ngrok is not installed or not in PATH")
                    print("[INFO] Install ngrok from https://ngrok.com/ and try again")
                    return
                
                self._start_server()
                print("[INFO] Starting ngrok tunnel...")
                try:
                    ngrok_process = subprocess.Popen(
                        [ngrok_cmd, "tcp", "5003"],
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
                    return
                    
            elif ngrok_choice == "join":
                ngrok_url = input("Enter ngrok TCP URL (e.g., 0.tcp.ngrok.io:12345): ").strip()
                try:
                    if ":" in ngrok_url:
                        host, port_str = ngrok_url.split(":")
                        port = int(port_str)
                    else:
                        print("[ERROR] Invalid ngrok URL format. Should be host:port")
                        return
                except ValueError:
                    print("[ERROR] Invalid port number in ngrok URL")
                    return
            else:
                print("[ERROR] Invalid choice. Please enter 'create' or 'join'")
                return
        else:
            print("[ERROR] Invalid choice")
            return
        
        # Connect and start chat
        self.connect_and_chat(host, port, name)
    
    def _start_server(self):
        """Start the server as a subprocess"""
        print("[INFO] Starting the server...")
        subprocess.Popen(
            ["python3", "-c", "from velora.server import start; start()"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(2)


# For backward compatibility with standalone script
def main():
    client = VeloraClient()
    client.start_interactive()


if __name__ == "__main__":
    main()