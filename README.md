# Velora 🚀

A lightweight Python library for peer-to-peer file sharing and real-time chat using TCP sockets. No external dependencies required!

## Features ✨

- 💬 **Real-time text chat** - Instant messaging over TCP
- 📁 **File sharing** - Share any file type up to 1GB
- 🌐 **Multiple connection modes** - Local, IP-based, and global (ngrok)
- 🔧 **Zero dependencies** - Pure Python using only standard library
- ⚡ **Quick share mode** - One-command file sharing
- 📦 **Easy installation** - Install via pip

## Installation 📦

```bash
pip install velora-chat
```

Or install from source:

```bash
git clone https://github.com/pavansai-tanguturi/Velora.git
cd Velora
pip install -e .
```

## Quick Start 🚀

### 1. Start a chat server

```bash
velora server
```

### 2. Join the chat

```bash
velora chat
```

### 3. Quick share a file

```bash
velora share /path/to/file.pdf
velora share /path/to/file.pdf 192.168.1.100        # To specific IP
velora share /path/to/file.pdf 0.tcp.ngrok.io:12345 # To ngrok tunnel
```

## Command Line Usage 💻

### Chat Commands

```bash
# Start interactive chat client
velora chat

# Connect directly to a server
velora chat --host 192.168.1.100 --port 5003 --name "Your Name"

# Start a server
velora server --host 0.0.0.0 --port 5003
```

### File Sharing Commands

```bash
# Share file locally (starts server automatically)
velora share document.pdf

# Share to remote server
velora share document.pdf 192.168.1.100:5003

# Share via ngrok
velora share document.pdf 0.tcp.ngrok.io:12345
```

### Alternative Commands

```bash
# Also available as separate commands
velora-chat      # Same as 'velora chat'
velora-share     # Same as 'velora share'
velora-server    # Same as 'velora server'
```

## Library Usage 📚

### Using Velora in your Python code

```python
import velora

# Start a server programmatically
server = velora.VeloraServer(host="0.0.0.0", port=5003)
server.start()

# Connect and send messages programmatically
client = velora.VeloraClient()
client.connect("127.0.0.1", 5003)
client.send_message("Hello from Python!")

# Quick file sharing
velora.quick_share("/path/to/file.pdf", "192.168.1.100:5003", "YourName")
```

## Connection Modes 🌐

### 1. Local Mode

Perfect for same-network sharing:

```bash
velora chat  # Choose option 1
```

### 2. IP-based Mode

Connect across networks using IP addresses:

```bash
velora chat --host 192.168.1.100
velora share file.pdf 192.168.1.100
```

### 3. Global Mode (ngrok)

Share globally using ngrok tunneling:

```bash
# Person A: Start server with ngrok
velora chat  # Choose option 3 -> create

# Person B: Connect to ngrok URL
velora chat  # Choose option 3 -> join
velora share file.pdf 0.tcp.ngrok.io:12345
```

## Chat Commands 💬

Once in a chat session:

- `hello` - Send a text message
- `/file /path/to/file.pdf` - Share a file
- `/quit` - Exit the chat

## File Sharing 📁

- **Supported formats**: Any file type
- **Size limit**: Up to 1GB per file
- **Auto-download**: Files saved to `~/Downloads`
- **Duplicate handling**: Automatic renaming (file.pdf, file (1).pdf, etc.)

## Network Requirements 🔧

### Local Network

- Port 5003 open (or custom port)
- All devices on same network

### Remote Network

- Server host needs public IP or port forwarding
- Firewall rules allowing TCP traffic on chosen port

### Global Access

- Install [ngrok](https://ngrok.com/) for easy tunneling
- Or use VPS/cloud server with public IP

## Examples 📋

### Example 1: Local File Sharing

```bash
# Terminal 1: Start server
velora server

# Terminal 2: Share a file
velora share vacation_photos.zip
```

### Example 2: Remote File Sharing

```bash
# Computer A (192.168.1.5): Start server
velora server

# Computer B: Share file to A
velora share presentation.pptx 192.168.1.5
```

### Example 3: Global Chat with ngrok

```bash
# Person A: Create global tunnel
velora chat  # Choose option 3 -> create -> get ngrok URL

# Person B: Join via ngrok URL
velora chat  # Choose option 3 -> join -> enter ngrok URL
```

## Development 🛠️

### Setup development environment

```bash
git clone https://github.com/pavansai-tanguturi/Velora.git
cd Velora
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/
```

### Code formatting

```bash
black velora/
flake8 velora/
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Notice ⚠️

This is designed for trusted networks and personal use. For production environments, consider adding:

- Authentication mechanisms
- End-to-end encryption
- Input validation and sanitization
- Rate limiting and abuse protection

## Support 💡

- 📖 [Documentation](https://github.com/pavansai-tanguturi/Velora#readme)
- 🐛 [Issue Tracker](https://github.com/pavansai-tanguturi/Velora/issues)
- 💬 [Discussions](https://github.com/pavansai-tanguturi/Velora/discussions)

---

Made with ❤️ by Pavan Sai Tanguturi
