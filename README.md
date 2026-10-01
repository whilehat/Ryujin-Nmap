# Ryujin Nmap

<p align="center">

**Cross-Platform Nmap Automation Tool**

Built by **Ryujin**

</p>

---

## Overview

Ryujin Nmap is a Python-based command-line automation tool designed to simplify Nmap network scanning.

Instead of manually remembering Nmap commands and options, Ryujin Nmap provides an interactive interface that allows users to configure scans and automatically generates the appropriate Nmap command.

The tool supports Linux, Windows, and macOS, providing a consistent scanning experience across different operating systems.

---

## Features

* Cross-platform support

  * Windows
  * Linux
  * macOS
* Automatic operating system detection
* Automatic Nmap detection
* Automatic Nmap installation (where supported)
* Interactive target selection
* Host discovery
* TCP scanning
* UDP scanning
* Port selection
* Service and version detection
* Operating system detection
* NSE script support
* Timing configuration
* IPv4 and IPv6 support
* Traceroute support
* Output file support
* Custom Nmap arguments
* Command preview before execution
* Interactive command confirmation

---

## Requirements

### Python

Python 3 is required.

Download Python:

https://www.python.org/downloads/

### Nmap

Nmap is required to perform network scans.

Download Nmap:

https://nmap.org/download.html

Ryujin Nmap can detect whether Nmap is installed and attempt to install it automatically using the platform's package manager.

---

# Installation

## Linux

### 1. Clone the repository

```bash
git clone https://github.com/whilehat/Ryujin-Nmap.git
```

### 2. Navigate to the project directory

```bash
cd Ryujin-Nmap
```

### 3. Run the installer

```bash
bash installers/install-linux.sh
```

The installer will:

* Detect the Linux distribution.
* Check for Python 3.
* Install Python if required.
* Check and install Nmap if required.
* Configure the Ryujin Nmap command.
* Set the required execution permissions.

### 4. Run Ryujin Nmap

After installation, execute:

```bash
ryujin-nmap
```

---

## macOS

### 1. Clone the repository

```bash
git clone https://github.com/whilehat/Ryujin-Nmap.git
```

### 2. Navigate to the project directory

```bash
cd Ryujin-Nmap
```

### 3. Run the installer

```bash
bash installers/install-macos.sh
```

The installer will:

* Check for Homebrew.
* Install Homebrew if required.
* Check for Python 3.
* Install Python if required.
* Check and install Nmap if required.
* Configure the Ryujin Nmap command.

### 4. Run Ryujin Nmap

After installation, execute:

```bash
ryujin-nmap
```

---

## Windows

### 1. Install Git

Download Git for Windows:

https://git-scm.com/downloads/win

### 2. Clone the repository

Open PowerShell:

```powershell
git clone https://github.com/whilehat/Ryujin-Nmap.git
```

### 3. Navigate to the project directory

```powershell
cd Ryujin-Nmap
```

### 4. Run the installer

```powershell
powershell -ExecutionPolicy Bypass -File .\installers\install-windows.ps1
```

The installer will:

* Check for Python 3.
* Install Python if required.
* Check and install Nmap if required.
* Configure the Ryujin Nmap command.
* Add the installation directory to the user PATH.

### 5. Run Ryujin Nmap

Close and reopen PowerShell, then execute:

```powershell
ryujin-nmap
```

---

# Usage

After installation, launch Ryujin Nmap from any terminal:

```bash
ryujin-nmap
```

The application will display an interactive menu to configure the scan.

### Example Nmap command

```bash
nmap -sV -p 22,80,443 192.168.1.10
```

This command:

* `-sV` — Detects service versions.
* `-p 22,80,443` — Scans the selected ports.
* `192.168.1.10` — Specifies the target IP address.

Ryujin Nmap allows users to configure these options through its interactive interface instead of manually constructing commands.

---

# Project Structure

```text
Ryujin-Nmap/
│
├── ryujin_nmap.py
│
├── installers/
│   ├── install-linux.sh
│   ├── install-macos.sh
│   └── install-windows.ps1
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# Supported Platforms

| Operating System | Installer           | Status    |
| ---------------- | ------------------- | --------- |
| Linux            | install-linux.sh    | Supported |
| macOS            | install-macos.sh    | Supported |
| Windows          | install-windows.ps1 | Supported |

---

# Security and Authorization

Ryujin Nmap is intended for authorized network discovery, security auditing, and educational purposes.

**Important:**

* Only scan networks and systems that you own or have explicit permission to test.
* Obtain authorization before performing vulnerability scans.
* Some NSE scripts and scanning techniques may generate significant network traffic or affect target services.
* Users are responsible for complying with applicable laws and regulations.

---

# License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

Nmap is a separate third-party application and is distributed under its own licensing terms.

Nmap official website:

https://nmap.org/

---

# Author

**Shivasankaran M**

GitHub: https://github.com/whilehat

---

<p align="center">

**Ryujin Nmap — Simplifying Network Scanning Through Automation.**

</p>
