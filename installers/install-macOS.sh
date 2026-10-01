#!/bin/bash

set -e

APP_NAME="ryujin-nmap"
INSTALL_DIR="/usr/local/lib/$APP_NAME"
BIN_PATH="/usr/local/bin/$APP_NAME"

SCRIPT_PATH="$(cd "$(dirname "$0")/.." && pwd)/ryujin_nmap.py"

echo
echo "=============================================="
echo "              R Y U J I N"
echo "          NMAP AUTOMATION TOOL"
echo "              macOS Installer"
echo "=============================================="
echo


# ============================================================
# Check macOS
# ============================================================

if [ "$(uname -s)" != "Darwin" ]; then
    echo "[!] This installer is for macOS."
    exit 1
fi


# ============================================================
# Check Python
# ============================================================

echo "[*] Checking Python 3..."

if command -v python3 >/dev/null 2>&1; then

    echo "[+] Python 3 found:"
    python3 --version

else

    echo "[!] Python 3 is not installed."

    if command -v brew >/dev/null 2>&1; then

        echo "[*] Installing Python with Homebrew..."
        brew install python

    else

        echo
        echo "[!] Homebrew is not installed."
        echo "[!] Please install Python 3 or Homebrew first."
        exit 1

    fi

fi


# ============================================================
# Check Homebrew
# ============================================================

if ! command -v brew >/dev/null 2>&1; then

    echo
    echo "[!] Homebrew is required to automatically install Nmap."
    echo
    echo "Install Homebrew, then run this installer again."
    exit 1

fi


# ============================================================
# Check / Install Nmap
# ============================================================

echo
echo "[*] Checking Nmap..."

if command -v nmap >/dev/null 2>&1; then

    echo "[+] Nmap found:"
    nmap --version | head -n 1

else

    echo "[!] Nmap is not installed."
    echo "[*] Installing Nmap with Homebrew..."

    brew install nmap

fi


# ============================================================
# Check application
# ============================================================

if [ ! -f "$SCRIPT_PATH" ]; then

    echo
    echo "[!] ryujin_nmap.py was not found:"
    echo "$SCRIPT_PATH"
    exit 1

fi


# ============================================================
# Install
# ============================================================

echo
echo "[*] Installing Ryujin Nmap..."

sudo mkdir -p "$INSTALL_DIR"

sudo cp "$SCRIPT_PATH" \
    "$INSTALL_DIR/ryujin_nmap.py"

sudo chmod +x \
    "$INSTALL_DIR/ryujin_nmap.py"


# ============================================================
# Create launcher
# ============================================================

echo "[*] Creating command: $APP_NAME"

sudo tee "$BIN_PATH" > /dev/null <<EOF
#!/bin/bash
exec python3 "$INSTALL_DIR/ryujin_nmap.py" "\$@"
EOF

sudo chmod +x "$BIN_PATH"


# ============================================================
# Complete
# ============================================================

echo
echo "=============================================="
echo "        RYUJIN NMAP INSTALLATION COMPLETE"
echo "=============================================="
echo
echo "Run from anywhere:"
echo
echo "    ryujin-nmap"
echo
