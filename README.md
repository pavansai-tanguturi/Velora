# Velora - Terminal Chat Application

A real-time terminal-based chat application that enables long-distance communication using ngrok tunneling.

## Features

- **Real-time messaging** - Instant communication between multiple users
- **Create or Join Rooms** - Host your own chat room or join existing ones
- **Global Access** - Connect with friends anywhere using ngrok tunneling
- **Simple Terminal Interface** - Clean, easy-to-use command-line chat
- **Auto Server Management** - Automatic server startup when creating rooms
- **Cross-platform** - Works on Windows, macOS, and Linux

## Prerequisites

- Python 3.6 or higher
- ngrok (for creating public tunnels)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pavansai-tanguturi/Velora.git
   cd Velora
   ```

2. **Install ngrok:**
   - Download from [ngrok.com](https://ngrok.com/download)
   - Or install via Homebrew (macOS):
     ```bash
     brew install ngrok
     ```

3. **No Python dependencies needed** - All required modules are built-in to Python

## Usage

### Starting the Chat Application

Run the client:
```bash
python client.py
```

### Create a Room

1. Enter your name when prompted
2. Choose `create` when asked to create or join a room
3. The application will:
   - Start a local server
   - Launch ngrok to create a public tunnel
   - Display a shareable URL (e.g., `0.tcp.in.ngrok.io:12345`)
4. Share this URL with friends so they can join your room

### Join a Room

1. Enter your name when prompted
2. Choose `join` when asked to create or join a room
3. Enter the port number from the ngrok URL your friend shared
4. Start chatting!

## Example Chat Session

```
Enter your name: Alice
Do you want to create a room or join a room? (create/join): create
[INFO] Starting the server...
[INFO] Starting ngrok...
[INFO] Ngrok started.
[INFO] Share this URL with others to join: 0.tcp.in.ngrok.io:12345
Connected to chat!

Alice: Hello everyone!
Bob: Hi Alice, how are you?
Alice: I'm doing great! This chat app works perfectly.
```

## How It Works

1. **Server (`server.py`)**: 
   - Handles multiple client connections
   - Relays messages between connected clients
   - Runs on localhost port 5003

2. **Client (`client.py`)**: 
   - Connects to the server (local or remote via ngrok)
   - Sends and receives messages in real-time
   - Manages ngrok tunneling for room creators

3. **ngrok Integration**:
   - Creates secure tunnels to expose local server
   - Enables global access without port forwarding
   - Automatically manages tunnel lifecycle

## Technical Details

- **Language**: Python 3
- **Networking**: TCP sockets
- **Threading**: Multi-threaded server and client
- **Tunneling**: ngrok for public access
- **Port**: Default server port 5003

## File Structure

```
Velora/
├── client.py          # Main client application
├── server.py          # Chat server
├── requirements.txt   # Dependencies (none needed)
└── README.md         # This file
```

## Troubleshooting

### Common Issues

1. **"Address already in use" error**:
   - Kill existing server process: `lsof -i :5003` then `kill -9 <PID>`
   - The server code includes socket reuse to prevent this

2. **ngrok not found**:
   - Ensure ngrok is installed and in your PATH
   - Check installation: `ngrok version`

3. **Connection refused**:
   - Verify the ngrok URL and port are correct
   - Make sure the room creator's application is still running

### Tips

- Room creators must keep their application running for others to stay connected
- Each new room gets a unique ngrok URL
- Messages are only visible to users in the same room

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Pavan Sai Tanguturi**
- GitHub: [@pavansai-tanguturi](https://github.com/pavansai-tanguturi)

## Acknowledgments

- Built with Python's built-in networking libraries
- ngrok for secure tunneling capabilities
- Inspired by the need for simple, accessible real-time communication