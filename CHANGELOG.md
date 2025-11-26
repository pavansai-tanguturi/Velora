# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-26

### Added

- **File Transfer Progress Bar** - Real-time progress visualization for files > 1MB
- **Transfer Speed & ETA** - Shows transfer speed (MB/s, KB/s) and estimated time remaining
- **System Notifications** - Plays sound notification when file is received (cross-platform)
- **Drag-and-Drop Support** - Paste file paths directly to send files with confirmation
- **`/help` Command** - Comprehensive help menu showing all available commands and tips
- **`/users` Command** - Lists all currently connected users in the chat
- **Automatic Reconnection** - Attempts to reconnect automatically on connection loss (3 attempts)
- **User Tracking** - Server now tracks connected usernames and displays join/leave messages
- **Unicode UI Elements** - Modern progress bars and status symbols (✓, █, ░)

### Changed

- Removed local server connection option from menu (option 1)
- Connection options now streamlined to: remote server and ngrok tunnel
- Improved file path handling with better quote and backslash stripping
- Enhanced error messages with more helpful troubleshooting information
- Better console output formatting with timing information

### Fixed

- **Cross-platform IP Detection** - Now supports both macOS (`ipconfig`) and Linux/Ubuntu (`hostname -I`)
- File transfer now shows completion time
- Improved error handling for network interruptions
- Better handling of special characters in filenames

### Technical Improvements

- Added command protocol for server-client communication
- Implemented user list request/response mechanism
- Enhanced message parsing to handle multiple JSON message types
- Added progress tracking with chunk-based file reading
- Improved socket timeout handling for reconnection

## [1.0.1] - 2025-11-13

### Changed

- Code cleanup and repository organization
- Removed development artifacts and temporary files
- Streamlined documentation structure

## [1.0.0] - 2025-11-13

### Added

- Initial release of Velora
- Real-time text chat over TCP sockets
- File sharing up to 1GB per file
- Multiple connection modes (local, IP-based, global via ngrok)
- Zero external dependencies - pure Python standard library
- Command line interface with subcommands
- Quick share mode for one-command file sharing
- Automatic file download to Downloads folder
- Duplicate filename handling
- Length-prefixed message protocol for reliability
- Support for both text and binary file transfers
- Interactive and programmatic API modes

### Features

- `velora chat` - Start interactive chat client
- `velora share` - Quick file sharing
- `velora server` - Start chat server
- `velora-chat`, `velora-share`, `velora-server` - Alternative commands
- Library usage with `velora.VeloraClient`, `velora.VeloraServer`, `velora.quick_share`

### Technical Details

- Base64 encoding for file transfers
- JSON message protocol for file metadata
- Robust TCP socket handling with proper error recovery
- Multi-threaded server supporting multiple clients
- Graceful connection handling and cleanup
