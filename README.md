# Velora

**Simple file sharing and chat over TCP sockets**

A lightweight Python library for peer-to-peer file sharing and real-time chat. Zero external dependencies - pure Python using only the standard library.

## Features

- 💬 Real-time text chat over TCP
- 📁 File sharing with progress bars and speed indicators
- 🔔 System notifications when files are received
- 🎯 Drag-and-drop file support
- 🔄 Automatic reconnection on connection loss
- 👥 User list and management commands
- 🌐 Multiple connection modes (IP-based, global with ngrok)
- 🔧 Zero dependencies - pure Python
- ⚡ One-command file sharing
- 📦 Easy CLI and programmatic usage

## Installation

```bash
pip install velora-chat
```

## Quick Start

### Start chatting (simplest way)
```bash
velora
```

### Or use specific commands
```bash
# Start a chat server
velora server

# Join a chat
velora chat

# Share a file
velora share /path/to/file.pdf
```

## Command Line Interface

### Chat
```bash
# Interactive chat client
velora chat

# Connect to specific server
velora chat --host 192.168.1.100 --port 5003 --name "Your Name"
```

### Server
```bash
velora server --host 0.0.0.0 --port 5003
```

### File Sharing
```bash
# Local sharing
velora share document.pdf

# Remote sharing
velora share document.pdf 192.168.1.100:5003

# Share via ngrok
velora share document.pdf 0.tcp.ngrok.io:12345
```

## Python API

```python
import velora

# Start a server
server = velora.VeloraServer(host="0.0.0.0", port=5003)
server.start()

# Connect and send messages
client = velora.VeloraClient()
client.connect("127.0.0.1", 5003)
client.send_message("Hello!")

# Quick file sharing
velora.quick_share("/path/to/file.pdf", "192.168.1.100:5003", "YourName")
```

## Connection Modes

**IP-based**: Connect across networks using IP addresses
```bash
velora  # Choose option 1 - create or join room
```

**Global (ngrok)**: Share globally using ngrok tunneling
```bash
velora  # Choose option 2 - create or join ngrok tunnel
```

**Direct Connection**: Connect to a specific server
```bash
velora chat --host 192.168.1.100
```

## In-Chat Commands

- Type any text to send a message
- Drag and drop files to share them instantly
- `/file /path/to/file.pdf` - Share a file
- `/users` - List all connected users
- `/help` - Show all available commands
- `/quit` - Exit the chat

## New in v1.1.0

- ⚡ **Progress Bars**: Real-time progress with transfer speed and ETA for large files
- 🔔 **Notifications**: Audio alerts when files are received (cross-platform)
- 🎯 **Drag & Drop**: Simply paste file paths to send files
- 👥 **User Management**: `/users` command to see who's connected
- 📖 **Help System**: `/help` command for quick reference
- 🔄 **Auto-Reconnect**: Automatically reconnects on connection loss (up to 3 attempts)
- 🖥️ **Better CLI**: Just run `velora` to start chatting instantly

## Requirements

- Python 3.7+
- No external dependencies
- Port 5003 (default) or custom port

## File Sharing Details

- **Formats**: Any file type
- **Size limit**: Up to 1GB
- **Download location**: `~/Downloads`
- **Duplicate handling**: Automatic renaming

## Documentation

For complete documentation, examples, and contribution guidelines, visit:

**[GitHub Repository](https://github.com/pavansai-tanguturi/Velora)**

## Links

- 📖 [Full Documentation](https://github.com/pavansai-tanguturi/Velora#readme)
- 🐛 [Issue Tracker](https://github.com/pavansai-tanguturi/Velora/issues)
- 💬 [Discussions](https://github.com/pavansai-tanguturi/Velora/discussions)

## License

MIT License - see [LICENSE](https://github.com/pavansai-tanguturi/Velora/blob/master/LICENSE) for details.

## Security Notice

Designed for trusted networks and personal use. For production environments, consider adding authentication, encryption, input validation, and rate limiting.

---

Made with ❤️ by [Pavan Sai Tanguturi](https://github.com/pavansai-tanguturi)