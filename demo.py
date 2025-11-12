#!/usr/bin/env python3
"""
Velora Demo Script - Shows all the ways to use Velora
"""

import time
import os

def show_usage_examples():
    """Display comprehensive usage examples"""
    
    print("🚀 Velora Python Library - Usage Examples")
    print("=" * 50)
    
    print("\n📦 1. INSTALLATION")
    print("   pip install -e .                    # Development install")
    print("   # pip install velora               # PyPI install (future)")
    
    print("\n💬 2. CHAT COMMANDS")
    print("   velora chat                        # Interactive mode")
    print("   velora chat --host 192.168.1.100  # Direct connect")
    print("   velora chat --name 'Your Name'    # Set display name")
    
    print("\n📁 3. FILE SHARING COMMANDS") 
    print("   velora share file.pdf              # Local sharing")
    print("   velora share file.pdf 192.168.1.5 # Remote IP")
    print("   velora share file.pdf 192.168.1.5:8080  # Custom port")
    print("   velora share file.pdf 0.tcp.ngrok.io:12345  # ngrok")
    
    print("\n🖥️  4. SERVER COMMANDS")
    print("   velora server                      # Default (0.0.0.0:5003)")
    print("   velora server --port 8080          # Custom port")
    print("   velora server --host 192.168.1.100 --port 9000")
    
    print("\n🔧 5. PYTHON LIBRARY USAGE")
    print("""
    import velora
    
    # Start server
    server = velora.VeloraServer(port=5003)
    server.start()
    
    # Connect client  
    client = velora.VeloraClient()
    client.connect('127.0.0.1', 5003)
    client.send_message('Hello!')
    client.send_file('/path/to/file.pdf')
    
    # Quick sharing
    velora.quick_share('file.pdf', '192.168.1.100', 'MyName')
    """)
    
    print("\n🌐 6. CONNECTION MODES")
    print("   Local:    Same network, automatic server start")
    print("   Remote:   Connect via IP address across networks") 
    print("   Global:   Use ngrok for worldwide access")
    
    print("\n📋 7. TYPICAL WORKFLOWS")
    
    print("\n   🏠 Local File Sharing:")
    print("      Terminal 1: velora share document.pdf")
    print("      Terminal 2: velora chat  # Choose local, receive file")
    
    print("\n   🌍 Remote File Sharing:")
    print("      Computer A: velora server")
    print("      Computer B: velora share file.pdf <A's IP>")
    print("      Computer C: velora chat --host <A's IP>")
    
    print("\n   🚀 Global Sharing (ngrok):")
    print("      Person A: velora chat  # Choose ngrok -> create")
    print("      Person B: velora share file.pdf <ngrok URL>")
    print("      Person C: velora chat  # Choose ngrok -> join")
    
    print("\n🛠️  8. DEVELOPMENT")
    print("   source chatenv/bin/activate        # Activate venv")
    print("   python test_velora.py              # Run tests")
    print("   velora version                     # Check version")
    
    print("\n✨ 9. KEY FEATURES")
    print("   ✅ Zero external dependencies")
    print("   ✅ File sharing up to 1GB")
    print("   ✅ Real-time chat over TCP")
    print("   ✅ Multiple connection modes")
    print("   ✅ Cross-platform (Windows/Mac/Linux)")
    print("   ✅ Command line + Python API")
    
    print(f"\n🎉 Velora is ready to use!")
    print("   Try: velora --help")
    print("   Or:  velora chat")

if __name__ == "__main__":
    show_usage_examples()