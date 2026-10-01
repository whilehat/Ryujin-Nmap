#!/usr/bin/env python3

import os
import platform
import shutil
import subprocess
import sys
import re


# ============================================================
# NMAP AUTOMATION TOOL
# ============================================================

VERSION = "1.0"

BANNER = r"""
███╗   ██╗███╗   ███╗ █████╗ ██████╗
████╗  ██║████╗ ████║██╔══██╗██╔══██╗
██╔██╗ ██║██╔████╔██║███████║██████╔╝
██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝
██║ ╚████║██║ ╚═╝ ██║██║  ██║██║
╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

        NMAP AUTOMATION TOOL
        Cross Platform Edition
"""


# ============================================================
# COLORS
# ============================================================

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"


def color(text, c):
    return f"{c}{text}{Colors.RESET}"


# ============================================================
# OS DETECTION
# ============================================================

def detect_os():

    system = platform.system().lower()

    if system == "windows":
        return "windows"

    if system == "darwin":
        return "mac"

    if system == "linux":
        return "linux"

    return "unknown"


def ask_os():

    print(color("\nSelect operating system:", Colors.CYAN))

    print("""
[1] Windows
[2] macOS
[3] Linux
[4] Auto Detect
""")

    while True:

        choice = input("Select: ").strip()

        if choice == "1":
            return "windows"

        elif choice == "2":
            return "mac"

        elif choice == "3":
            return "linux"

        elif choice == "4":
            detected = detect_os()

            print(
                color(
                    f"Detected OS: {detected}",
                    Colors.GREEN
                )
            )

            return detected

        else:
            print(color("Invalid choice.", Colors.RED))


# ============================================================
# NMAP CHECK
# ============================================================

def nmap_installed():

    return shutil.which("nmap") is not None


def nmap_version():

    try:

        result = subprocess.run(
            ["nmap", "--version"],
            capture_output=True,
            text=True
        )

        return result.stdout.splitlines()[0]

    except Exception:
        return "Unknown"


# ============================================================
# COMMAND RUNNER
# ============================================================

def run_command(command, shell=False):

    try:

        print(
            color(
                "\nExecuting installation command:",
                Colors.YELLOW
            )
        )

        print(" ".join(command) if isinstance(command, list) else command)

        result = subprocess.run(
            command,
            shell=shell
        )

        return result.returncode == 0

    except Exception as e:

        print(
            color(
                f"Error: {e}",
                Colors.RED
            )
        )

        return False


# ============================================================
# WINDOWS INSTALL
# ============================================================

def install_windows():

    print(color("\nWindows Nmap installation", Colors.CYAN))

    # First try winget
    if shutil.which("winget"):

        print("Using winget...")

        command = [
            "winget",
            "install",
            "-e",
            "--id",
            "Insecure.Nmap"
        ]

        return run_command(command)

    # Try Chocolatey
    if shutil.which("choco"):

        print("Using Chocolatey...")

        command = [
            "choco",
            "install",
            "nmap",
            "-y"
        ]

        return run_command(command)

    print(color("""
Nmap is not installed.

Install one of the following package managers:

1. winget
2. Chocolatey

Or install Nmap manually from the official Nmap website.
""", Colors.YELLOW))

    return False


# ============================================================
# MACOS INSTALL
# ============================================================

def install_mac():

    print(color("\nmacOS Nmap installation", Colors.CYAN))

    if not shutil.which("brew"):

        print(color(
            "Homebrew is not installed.",
            Colors.YELLOW
        ))

        print(
            "Install Homebrew first, then run this tool again."
        )

        return False

    command = [
        "brew",
        "install",
        "nmap"
    ]

    return run_command(command)


# ============================================================
# LINUX INSTALL
# ============================================================

def install_linux():

    print(color("\nLinux Nmap installation", Colors.CYAN))

    # Debian / Ubuntu / Kali
    if shutil.which("apt"):

        command = [
            "sudo",
            "apt",
            "update"
        ]

        if not run_command(command):
            return False

        command = [
            "sudo",
            "apt",
            "install",
            "-y",
            "nmap"
        ]

        return run_command(command)

    # Fedora / RHEL
    if shutil.which("dnf"):

        command = [
            "sudo",
            "dnf",
            "install",
            "-y",
            "nmap"
        ]

        return run_command(command)

    # Arch / Manjaro
    if shutil.which("pacman"):

        command = [
            "sudo",
            "pacman",
            "-Sy",
            "--noconfirm",
            "nmap"
        ]

        return run_command(command)

    # openSUSE
    if shutil.which("zypper"):

        command = [
            "sudo",
            "zypper",
            "install",
            "-y",
            "nmap"
        ]

        return run_command(command)

    print(color(
        "Could not identify a supported Linux package manager.",
        Colors.RED
    ))

    return False


# ============================================================
# INSTALL NMAP
# ============================================================

def install_nmap(os_type):

    if os_type == "windows":
        return install_windows()

    if os_type == "mac":
        return install_mac()

    if os_type == "linux":
        return install_linux()

    print(color(
        "Unsupported operating system.",
        Colors.RED
    ))

    return False


# ============================================================
# TARGET VALIDATION
# ============================================================

def valid_target(target):

    if not target:
        return False

    # Prevent command injection when target is passed as an
    # individual subprocess argument.
    pattern = r"^[a-zA-Z0-9._:/\-\[\]]+$"

    return re.match(pattern, target) is not None


def ask_target():

    print(color("\nTarget", Colors.CYAN))

    print("""
Examples:

192.168.1.10
192.168.1.0/24
192.168.1.1-50
example.com
""")

    while True:

        target = input("Target: ").strip()

        if valid_target(target):
            return target

        print(
            color(
                "Invalid target format.",
                Colors.RED
            )
        )


# ============================================================
# PORT OPTIONS
# ============================================================

def port_options(command):

    print(color("\nPort Selection", Colors.CYAN))

    print("""
[1] Default ports
[2] Specific ports
[3] Port range
[4] All TCP ports
[5] Top N ports
[6] Custom port specification
""")

    choice = input("Select: ").strip()

    if choice == "1":
        return command

    elif choice == "2":

        ports = input(
            "Ports (example: 22,80,443): "
        ).strip()

        if ports:
            command.extend(["-p", ports])

    elif choice == "3":

        ports = input(
            "Range (example: 1-1000): "
        ).strip()

        if ports:
            command.extend(["-p", ports])

    elif choice == "4":

        command.append("-p-")

    elif choice == "5":

        number = input(
            "Number of top ports: "
        ).strip()

        if number.isdigit():
            command.extend([
                "--top-ports",
                number
            ])

    elif choice == "6":

        ports = input(
            "Custom port specification: "
        ).strip()

        if ports:
            command.extend(["-p", ports])

    return command


# ============================================================
# SCAN TYPE
# ============================================================

def scan_type(command, os_type):

    print(color("\nScan Type", Colors.CYAN))

    print("""
[1] Basic Scan
[2] SYN Scan
[3] TCP Connect Scan
[4] UDP Scan
[5] SYN + UDP
[6] ACK Scan
[7] FIN Scan
[8] NULL Scan
[9] Xmas Scan
[10] Window Scan
[11] Maimon Scan
[12] SCTP INIT Scan
[13] SCTP COOKIE-ECHO Scan
[14] IP Protocol Scan
""")

    choice = input("Select: ").strip()

    if choice == "1":
        pass

    elif choice == "2":
        command.append("-sS")

    elif choice == "3":
        command.append("-sT")

    elif choice == "4":
        command.append("-sU")

    elif choice == "5":
        command.extend(["-sS", "-sU"])

    elif choice == "6":
        command.append("-sA")

    elif choice == "7":
        command.append("-sF")

    elif choice == "8":
        command.append("-sN")

    elif choice == "9":
        command.append("-sX")

    elif choice == "10":
        command.append("-sW")

    elif choice == "11":
        command.append("-sM")

    elif choice == "12":
        command.append("-sY")

    elif choice == "13":
        command.append("-sZ")

    elif choice == "14":
        command.append("-sO")

    return command


# ============================================================
# HOST DISCOVERY
# ============================================================

def discovery_options(command):

    print(color("\nHost Discovery", Colors.CYAN))

    print("""
[1] Normal discovery
[2] Ping scan only
[3] Treat hosts as online
[4] ARP discovery
[5] ICMP Echo
[6] TCP SYN discovery
[7] TCP ACK discovery
[8] UDP discovery
[9] Disable DNS resolution
""")

    choice = input("Select: ").strip()

    options = {
        "2": "-sn",
        "3": "-Pn",
        "4": "-PR",
        "5": "-PE",
        "6": "-PS",
        "7": "-PA",
        "8": "-PU",
        "9": "-n"
    }

    if choice in options:

        command.append(options[choice])

        if choice in ["6", "7", "8"]:

            ports = input(
                "Ports for discovery: "
            ).strip()

            if ports:
                command[-1] += ports

    return command


# ============================================================
# SERVICE DETECTION
# ============================================================

def service_options(command):

    print(color("\nService Detection", Colors.CYAN))

    print("""
[1] No version detection
[2] Version detection
[3] Light version detection
[4] Maximum version intensity
""")

    choice = input("Select: ").strip()

    if choice == "2":
        command.append("-sV")

    elif choice == "3":
        command.extend([
            "-sV",
            "--version-light"
        ])

    elif choice == "4":
        command.extend([
            "-sV",
            "--version-intensity",
            "9"
        ])

    return command


# ============================================================
# OS DETECTION
# ============================================================

def os_options(command):

    print(color("\nOS Detection", Colors.CYAN))

    print("""
[1] Disabled
[2] OS Detection
[3] OS Detection + Guess
""")

    choice = input("Select: ").strip()

    if choice == "2":
        command.append("-O")

    elif choice == "3":
        command.extend([
            "-O",
            "--osscan-guess"
        ])

    return command


# ============================================================
# NSE
# ============================================================

def nse_options(command):

    print(color("\nNSE Scripts", Colors.CYAN))

    print("""
[1] No NSE
[2] Default scripts
[3] Safe scripts
[4] Discovery scripts
[5] Version scripts
[6] HTTP scripts
[7] SMB scripts
[8] DNS scripts
[9] SSL/TLS scripts
[10] Vulnerability scripts
[11] Specific script
[12] Custom NSE expression
""")

    choice = input("Select: ").strip()

    scripts = {
        "2": "default",
        "3": "safe",
        "4": "discovery",
        "5": "version",
        "6": "http-*",
        "7": "smb-*",
        "8": "dns-*",
        "9": "ssl-*",
        "10": "vuln"
    }

    if choice in scripts:

        command.extend([
            "--script",
            scripts[choice]
        ])

    elif choice == "11":

        script = input(
            "NSE script name: "
        ).strip()

        if script:
            command.extend([
                "--script",
                script
            ])

    elif choice == "12":

        expression = input(
            "NSE expression: "
        ).strip()

        if expression:
            command.extend([
                "--script",
                expression
            ])

    return command


# ============================================================
# TIMING
# ============================================================

def timing_options(command):

    print(color("\nTiming", Colors.CYAN))

    print("""
[1] T0 - Paranoid
[2] T1 - Sneaky
[3] T2 - Polite
[4] T3 - Normal
[5] T4 - Aggressive
[6] T5 - Insane
""")

    choice = input("Select: ").strip()

    if choice in ["1", "2", "3", "4", "5", "6"]:

        command.append(
            "-T" + str(int(choice) - 1)
        )

    return command


# ============================================================
# ADVANCED OPTIONS
# ============================================================

def advanced_options(command):

    print(color("\nAdvanced Options", Colors.CYAN))

    print("""
[1] None
[2] IPv4
[3] IPv6
[4] Disable DNS
[5] Traceroute
[6] Specify interface
[7] Specify DNS server
[8] Source port
[9] Custom arguments
""")

    choice = input("Select: ").strip()

    if choice == "2":
        command.append("-4")

    elif choice == "3":
        command.append("-6")

    elif choice == "4":
        command.append("-n")

    elif choice == "5":
        command.append("--traceroute")

    elif choice == "6":

        interface = input(
            "Interface (example: eth0/wlan0): "
        ).strip()

        if interface:
            command.extend([
                "-e",
                interface
            ])

    elif choice == "7":

        dns = input(
            "DNS server: "
        ).strip()

        if dns:
            command.extend([
                "--dns-servers",
                dns
            ])

    elif choice == "8":

        port = input(
            "Source port: "
        ).strip()

        if port.isdigit():
            command.extend([
                "--source-port",
                port
            ])

    elif choice == "9":

        custom = input(
            "Custom Nmap arguments: "
        ).strip()

        if custom:
            # Deliberately limited: do not execute through a shell.
            # Split simple arguments safely.
            import shlex

            command.extend(
                shlex.split(custom, posix=(os.name != "nt"))
            )

    return command


# ============================================================
# OUTPUT
# ============================================================

def output_options(command):

    print(color("\nOutput", Colors.CYAN))

    print("""
[1] Display only
[2] Normal output
[3] XML output
[4] Grepable output
[5] All major formats
""")

    choice = input("Select: ").strip()

    if choice == "2":

        filename = input(
            "Output filename: "
        ).strip()

        if filename:
            command.extend([
                "-oN",
                filename
            ])

    elif choice == "3":

        filename = input(
            "XML filename: "
        ).strip()

        if filename:
            command.extend([
                "-oX",
                filename
            ])

    elif choice == "4":

        filename = input(
            "Grepable filename: "
        ).strip()

        if filename:
            command.extend([
                "-oG",
                filename
            ])

    elif choice == "5":

        filename = input(
            "Base filename: "
        ).strip()

        if filename:
            command.extend([
                "-oA",
                filename
            ])

    return command


# ============================================================
# BUILD SCAN
# ============================================================

def build_scan(target, os_type):

    command = ["nmap"]

    # Target
    command.append(target)

    print(color(
        "\nConfigure scan options",
        Colors.MAGENTA
    ))

    command = scan_type(command, os_type)

    command = port_options(command)

    command = service_options(command)

    command = os_options(command)

    command = nse_options(command)

    command = timing_options(command)

    command = discovery_options(command)

    command = advanced_options(command)

    command = output_options(command)

    return command


# ============================================================
# EXECUTE SCAN
# ============================================================

def execute_scan(command, os_type):

    print("\n")
    print(color(
        "==========================================",
        Colors.GREEN
    ))

    print(color(
        "FINAL NMAP COMMAND",
        Colors.GREEN
    ))

    print(color(
        " ".join(command),
        Colors.WHITE
    ))

    print(color(
        "==========================================",
        Colors.GREEN
    ))

    confirm = input(
        "\nExecute this command? [y/N]: "
    ).strip().lower()

    if confirm != "y":

        print(color(
            "Scan cancelled.",
            Colors.YELLOW
        ))

        return

    # Privileged scan warning
    privileged_options = [
        "-sS",
        "-sU",
        "-O",
        "-sF",
        "-sN",
        "-sX",
        "-sW",
        "-sM",
        "-sY",
        "-sZ"
    ]

    if any(option in command for option in privileged_options):

        if os_type == "linux":

            print(color(
                "\nThis scan may require root privileges.",
                Colors.YELLOW
            ))

            if os.geteuid() != 0:

                command.insert(0, "sudo")

        elif os_type == "mac":

            print(color(
                "\nThis scan may require administrator privileges.",
                Colors.YELLOW
            ))

            # sudo will request password interactively
            command.insert(0, "sudo")

        elif os_type == "windows":

            print(color(
                "\nSome Nmap scans require Administrator privileges.",
                Colors.YELLOW
            ))

    print(color(
        "\nStarting Nmap...\n",
        Colors.CYAN
    ))

    try:

        result = subprocess.run(
            command,
            text=True
        )

        if result.returncode == 0:

            print(color(
                "\nScan completed.",
                Colors.GREEN
            ))

        else:

            print(color(
                f"\nNmap exited with code {result.returncode}.",
                Colors.RED
            ))

    except KeyboardInterrupt:

        print(color(
            "\nScan interrupted.",
            Colors.YELLOW
        ))

    except FileNotFoundError:

        print(color(
            "\nNmap executable was not found.",
            Colors.RED
        ))

    except Exception as e:

        print(color(
            f"\nError: {e}",
            Colors.RED
        ))


# ============================================================
# MAIN
# ============================================================

def main():

    print(color(BANNER, Colors.CYAN))

    print(color(
        f"Version {VERSION}",
        Colors.YELLOW
    ))

    print(color(
        "\nAuthorized security testing only.",
        Colors.RED
    ))

    # --------------------------------------------------------
    # OS
    # --------------------------------------------------------

    os_type = ask_os()

    # --------------------------------------------------------
    # NMAP CHECK
    # --------------------------------------------------------

    print(
        color(
            "\nChecking Nmap...",
            Colors.CYAN
        )
    )

    if nmap_installed():

        print(
            color(
                f"Nmap detected: {nmap_version()}",
                Colors.GREEN
            )
        )

    else:

        print(
            color(
                "Nmap is not installed.",
                Colors.YELLOW
            )
        )

        install = input(
            "Install Nmap automatically? [Y/n]: "
        ).strip().lower()

        if install in ["", "y", "yes"]:

            success = install_nmap(os_type)

            if not success:

                print(color(
                    "\nNmap installation failed.",
                    Colors.RED
                ))

                sys.exit(1)

            # Refresh PATH lookup
            if not nmap_installed():

                print(color(
                    """
Nmap was installed, but this terminal does not
see the new PATH yet.

Restart your terminal and run the tool again.
""",
                    Colors.YELLOW
                ))

                sys.exit(1)

        else:

            print(
                color(
                    "Nmap is required to continue.",
                    Colors.RED
                )
            )

            sys.exit(1)

    # --------------------------------------------------------
    # TARGET
    # --------------------------------------------------------

    target = ask_target()

    # --------------------------------------------------------
    # BUILD COMMAND
    # --------------------------------------------------------

    command = build_scan(
        target,
        os_type
    )

    # --------------------------------------------------------
    # EXECUTE
    # --------------------------------------------------------

    execute_scan(
        command,
        os_type
    )


if __name__ == "__main__":
    main()
