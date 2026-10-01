#!/usr/bin/env bash

set -e

APP_NAME="ryujin-nmap"
SCRIPT_NAME="ryujin_nmap.py"

INSTALL_DIR="/usr/local/lib/$APP_NAME"
BIN_PATH="/usr/local/bin/$APP_NAME"

echo
echo "=============================================="
echo "              R Y U J I N"
echo "          NMAP AUTOMATION TOOL"
echo "              Linux Installer"
echo "=============================================="
echo


# ============================================================
# Check that the Python application exists
# ============================================================

SCRIPT_PATH="$(dirname "$(realpath "$0")")/../$SCRIPT_NAME"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "[!] Could not find:"
    echo "    $SCRIPT_PATH"
    exit 1
fi


# ============================================================
# Detect Linux
# ============================================================

if [ "$(uname -s)" != "Linux" ]; then
    echo "[!] This installer is for Linux."
    exit 1
fi


# ============================================================
# Check / Install Python
# ============================================================

echo "[*] Checking Python 3..."

if command -v python3 >/dev/null 2>&1; then

    echo "[+] Python 3 found:"
    python3 --version

else

    echo "[!] Python 3 is not installed."
    echo "[*] Attempting installation..."

    if command -v apt-get >/dev/null 2>&1; then

        sudo apt-get update
        sudo apt-get install -y python3

    elif command -v dnf >/dev/null 2>&1; then

        sudo dnf install -y python3

    elif command -v yum >/dev/null 2>&1; then

        sudo yum install -y python3

    elif command -v pacman >/dev/null 2>&1; then

        sudo pacman -Sy --noconfirm python

    elif command -v zypper >/dev/null 2>&1; then

        sudo zypper install -y python3

    elif command -v apk >/dev/null 2>&1; then

        sudo apk add python3

    else

        echo
        echo "[!] Unsupported package manager."
        echo "[!] Please install Python 3 manually."
        exit 1

    fi

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
    echo "[*] Installing Nmap..."

    if command -v apt-get >/dev/null 2>&1; then

        sudo apt-get update
        sudo apt-get install -y nmap

    elif command -v dnf >/dev/null 2>&1; then

        sudo dnf install -y nmap

    elif command -v yum >/dev/null 2>&1; then

        sudo yum install -y nmap

    elif command -v pacman >/dev/null 2>&1; then

        sudo pacman -Sy --noconfirm nmap

    elif command -v zypper >/dev/null 2>&1; then

        sudo zypper install -y nmap

    elif command -v apk >/dev/null 2>&1; then

        sudo apk add nmap

    else

        echo
        echo "[!] Unsupported package manager."
        echo "[!] Please install Nmap manually."
        exit 1

    fi

fi


# ============================================================
# Create installation directory
# ============================================================

echo
echo "[*] Creating Ryujin installation directory..."

sudo mkdir -p "$INSTALL_DIR"


# ============================================================
# Copy Python application
# ============================================================

echo "[*] Installing Ryujin Nmap..."

sudo cp "$SCRIPT_PATH" "$INSTALL_DIR/ryujin_nmap.py"


# ============================================================
# Make executable
# ============================================================

sudo chmod +x "$INSTALL_DIR/ryujin_nmap.py"


# ============================================================
# Create launcher
# ============================================================

echo "[*] Creating command: $APP_NAME"

sudo tee "$BIN_PATH" > /dev/null <<EOF
#!/usr/bin/env bash
exec python3 "$INSTALL_DIR/ryujin_nmap.py" "\$@"
EOF

sudo chmod +x "$BIN_PATH"


# ============================================================
# Verify
# ============================================================

echo
echo "[*] Verifying installation..."

if command -v "$APP_NAME" >/dev/null 2>&1; then

    echo
    echo "=============================================="
    echo "        RYUJIN NMAP INSTALLATION COMPLETE"
    echo "=============================================="
    echo
    echo "Run the tool from anywhere:"
    echo
    echo "    ryujin-nmap"
    echo

else

    echo
    echo "[!] Installation completed, but command was"
    echo "    not found in PATH."
    echo
    echo "Try opening a new terminal."
    exit 1

fi
