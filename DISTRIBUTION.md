# 📦 Velora Distribution & Installation Guide

## 🚀 How Others Can Install Velora

### Option 1: Install from PyPI (Simplest - Coming Soon!)

```bash
# Simple installation (after PyPI publication)
pip install velora-chat
```

### Option 2: Install from GitHub (Current Method)

```bash
# Install directly from GitHub
pip install git+https://github.com/pavansai-tanguturi/Velora.git

# Or clone and install
git clone https://github.com/pavansai-tanguturi/Velora.git
cd Velora
pip install .
```

### Option 3: Install from Pre-built Package

```bash
# If you have the distribution files (velora_chat-1.0.0-py3-none-any.whl or velora_chat-1.0.0.tar.gz)
pip install velora_chat-1.0.0-py3-none-any.whl

# Or from the tarball
pip install velora_chat-1.0.0.tar.gz
```

### Option 4: Install from Downloaded Source

```bash
# Download the repository as ZIP from GitHub
# Extract the ZIP file
cd Velora-main  # or wherever you extracted it
pip install .
```

### Option 5: Development Install

```bash
# For developers who want to modify the code
git clone https://github.com/pavansai-tanguturi/Velora.git
cd Velora
pip install -e .  # Editable install
```

## ✅ Verification After Install

```bash
# Check if installation worked
velora version

# Show all commands
velora --help

# Test with a simple chat
velora chat
```

## 🌐 Usage Examples for New Users

### 1. Quick File Sharing

```bash
# Share a file locally (starts server automatically)
velora share document.pdf

# Others connect to receive the file
velora chat --host YOUR_IP_ADDRESS
```

### 2. Start a Chat Room

```bash
# Create a room
velora server

# Others join
velora chat --host YOUR_IP_ADDRESS
```

### 3. Global Sharing with ngrok

```bash
# Create global tunnel (requires ngrok installed)
velora chat  # Choose option 3 -> create

# Others join using the ngrok URL
velora chat  # Choose option 3 -> join
```

## 📋 System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: None (uses only Python standard library)
- **Optional**: ngrok (for global access)

## 🛠️ Troubleshooting

### Command not found

```bash
# If 'velora' command is not found, try:
python -m velora.cli --help

# Or use pip show to find installation path
pip show velora
```

### Permission Issues

```bash
# Use --user flag for user-only install
pip install --user git+https://github.com/pavansai-tanguturi/Velora.git
```

### Virtual Environment (Recommended)

```bash
# Create isolated environment
python -m venv velora-env
source velora-env/bin/activate  # On Windows: velora-env\Scripts\activate
pip install git+https://github.com/pavansai-tanguturi/Velora.git
```

## 🔧 For Developers

### Building Distribution Packages

```bash
# Install build tools
pip install build twine

# Build packages
python -m build

# This creates:
# dist/velora-1.0.0.tar.gz     (source distribution)
# dist/velora-1.0.0-py3-none-any.whl  (wheel)
```

### Publishing to PyPI

```bash
# Install upload tools
pip install twine

# Test upload to TestPyPI first (recommended)
twine upload --repository testpypi dist/*

# Upload to real PyPI (makes it available via 'pip install velora')
twine upload dist/*
```

**📋 Steps to Enable Simple Installation:**

1. **Create PyPI Account**: Sign up at https://pypi.org/
2. **Create API Token**: Go to Account Settings → API tokens
3. **Configure Credentials**:
   ```bash
   # Create ~/.pypirc file with your credentials
   [pypi]
   username = __token__
   password = pypi-YOUR_API_TOKEN_HERE
   ```
4. **Upload Package**:
   ```bash
   twine upload dist/*
   ```
5. **Users Can Then Install**:
   ```bash
   pip install velora  # That's it! 🎉
   ```

## 📤 Sharing Your Installation

### Share via GitHub

1. Push your code to GitHub
2. Others install with: `pip install git+https://github.com/YOUR_USERNAME/Velora.git`

3. **Share via Files**
4. Create distribution: `python -m build`
5. Share the `dist/velora_chat-1.0.0-py3-none-any.whl` file
6. Others install with: `pip install velora_chat-1.0.0-py3-none-any.whl`

### Share via ZIP

1. Create a ZIP of your project (excluding .git, **pycache**, etc.)
2. Others extract and run: `pip install .`

## 🎯 Quick Start for New Users

```bash
# 1. Install (after PyPI publication)
pip install velora-chat

# 1. Install (current method)
pip install git+https://github.com/pavansai-tanguturi/Velora.git

# 2. Try it out
velora chat

# 3. Share a file
velora share /path/to/file.pdf

# 4. Start a server for others
velora server
```

---

**That's it! Velora is now ready for distribution and easy installation by anyone!** 🎉
