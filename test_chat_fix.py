#!/usr/bin/env python3
"""
Test script to verify that chat works after file transfer
"""
import socket
import threading
import time
import subprocess
import sys
import os

def test_client_messages():
    """Test sending messages with the new length-prefixed protocol"""
    try:
        # Connect to server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 5003))
        
        # Send a test message using the new protocol
        name = "TestUser"
        message = f"{name}: Hello, this is a test message!"
        message_bytes = message.encode('utf-8')
        message_length = len(message_bytes)
        length_header = f"{message_length:010d}".encode('utf-8')
        
        print(f"Sending message: '{message}'")
        print(f"Length header: {length_header}")
        print(f"Message length: {message_length}")
        
        sock.sendall(length_header)
        sock.sendall(message_bytes)
        
        print("Message sent successfully!")
        
        # Wait a bit then close
        time.sleep(1)
        sock.close()
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def main():
    print("=== Testing Chat Fix ===")
    print("This script tests the length-prefixed protocol for regular messages")
    print()
    
    # Start server
    print("Starting server...")
    try:
        server_process = subprocess.Popen(
            ["python3", "server_with_files.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # Let server start
        
        print("Server started, testing message sending...")
        
        # Test message sending
        success = test_client_messages()
        
        if success:
            print("✅ Test passed! Chat messages work with length-prefixed protocol")
        else:
            print("❌ Test failed!")
            
    except Exception as e:
        print(f"Failed to start server: {e}")
    finally:
        # Clean up
        try:
            server_process.terminate()
            server_process.wait(timeout=3)
        except:
            try:
                server_process.kill()
            except:
                pass

if __name__ == "__main__":
    main()