# Velora Installation & Usage Guide

## 🚀 Velora is now a Python Library!

Velora has been converted into a proper Python package with easy installation and command-line tools.

## Installation Options

### Option 1: Install from Source (Current)
```bash
# Clone the repository
git clone https://github.com/pavansai-tanguturi/Velora.git
cd Velora

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Option 2: Future PyPI Installation
```bash
# Once published to PyPI (not yet available)
pip install velora
```

## Command Line Usage

After installation, you get these commands:

### Start a Chat Server
```bash
velora server
# Or with custom settings
velora server --host 0.0.0.0 --port 8080
```

### Join a Chat
```bash
velora chat
# Or connect directly
velora chat --host 192.168.1.100 --port 5003 --name "Your Name"
```

### Quick File Sharing
```bash
# Share locally (starts server automatically)
velora share document.pdf

# Share to specific server
velora share document.pdf 192.168.1.100
velora share document.pdf 192.168.1.100:8080
velora share document.pdf 0.tcp.ngrok.io:12345
```

### Other Commands
```bash
velora version          # Show version
velora --help          # Show help
velora chat --help     # Chat-specific help
velora share --help    # Share-specific help
```

### Alternative Commands
```bash
# Also available as separate commands
velora-chat      # Same as 'velora chat'
velora-share     # Same as 'velora share' 
velora-server    # Same as 'velora server'
```

## Library Usage in Python

```python
import velora

# Start a server programmatically
server = velora.VeloraServer(host="0.0.0.0", port=5003)
server.start()

# Connect and send messages
client = velora.VeloraClient()
client.connect("127.0.0.1", 5003)
client.send_message("Hello from Python!")
client.send_file("/path/to/file.pdf")

# Quick file sharing
velora.quick_share("/path/to/file.pdf", "192.168.1.100:5003", "YourName")
```

## Usage Examples

### Example 1: Local Chat Room
```bash
# Terminal 1: Start server
velora server

# Terminal 2: Join as first user
velora chat --host 127.0.0.1 --name "Alice"

# Terminal 3: Join as second user  
velora chat --host 127.0.0.1 --name "Bob"
```

### Example 2: Quick File Sharing
```bash
# Share a file locally
velora share vacation_photos.zip

# In another terminal, receive it
velora chat --host 127.0.0.1 --name "Receiver"
```

### Example 3: Remote Sharing
```bash
# Computer A (192.168.1.5): Start server
velora server

# Computer B: Share file to A
velora share presentation.pptx 192.168.1.5 --name "Sender"

# Computer C: Join chat on A
velora chat --host 192.168.1.5 --name "Viewer"
```

## Virtual Environment (Current Setup)

If using the current development setup:

```bash
# Activate the virtual environment
source chatenv/bin/activate

# Now velora commands work globally
velora --help
velora chat
velora share file.txt

# Deactivate when done
deactivate
```

## Key Features

✨ **Zero Dependencies** - Pure Python standard library
🚀 **Easy Installation** - Single pip command
💬 **Real-time Chat** - Instant messaging over TCP
📁 **File Sharing** - Share any file up to 1GB
🌐 **Multiple Modes** - Local, IP-based, global (ngrok)
⚡ **Quick Share** - One-command file sharing
🔧 **Programmatic API** - Use in your Python projects

## Publishing to PyPI (Future)

To publish this package to PyPI:

```bash
# Build the package
python setup.py sdist bdist_wheel

# Upload to PyPI (requires account and twine)
pip install twine
twine upload dist/*
```

Then anyone can install with:
```bash
pip install velora
```

## Development

```bash
# Setup development environment
git clone https://github.com/pavansai-tanguturi/Velora.git
cd Velora
pip install -e ".[dev]"

# Run tests
python test_velora.py

# Format code
black velora/
```

---

🎉 **Velora is now a proper Python package with easy installation and professional command-line tools!**