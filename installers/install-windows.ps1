$ErrorActionPreference = "Stop"

$AppName = "ryujin-nmap"

$InstallDir = "$env:LOCALAPPDATA\Ryujin\$AppName"

$ScriptPath = Join-Path `
    (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)) `
    "ryujin_nmap.py"


Write-Host ""
Write-Host "=============================================="
Write-Host "              R Y U J I N"
Write-Host "          NMAP AUTOMATION TOOL"
Write-Host "              Windows Installer"
Write-Host "=============================================="
Write-Host ""


# ============================================================
# Check Windows
# ============================================================

if ($env:OS -ne "Windows_NT") {

    Write-Host "[!] This installer is for Windows."

    exit 1
}


# ============================================================
# Check Python
# ============================================================

Write-Host "[*] Checking Python..."

$PythonCommand = Get-Command python -ErrorAction SilentlyContinue

if (-not $PythonCommand) {

    Write-Host "[!] Python is not installed."

    $Winget = Get-Command winget -ErrorAction SilentlyContinue

    if (-not $Winget) {

        Write-Host "[!] winget is not available."
        Write-Host "[!] Please install Python 3 manually."

        exit 1
    }

    Write-Host "[*] Installing Python with winget..."

    winget install `
        --id Python.Python.3 `
        --exact `
        --accept-source-agreements `
        --accept-package-agreements

}
else {

    Write-Host "[+] Python found."

}


# ============================================================
# Check Nmap
# ============================================================

Write-Host ""
Write-Host "[*] Checking Nmap..."

$NmapCommand = Get-Command nmap -ErrorAction SilentlyContinue

if (-not $NmapCommand) {

    Write-Host "[!] Nmap is not installed."

    $Winget = Get-Command winget -ErrorAction SilentlyContinue

    if (-not $Winget) {

        Write-Host "[!] winget is not available."
        Write-Host "[!] Please install Nmap manually."

        exit 1
    }

    Write-Host "[*] Installing Nmap with winget..."

    winget install `
        --id Insecure.Nmap `
        --exact `
        --accept-source-agreements `
        --accept-package-agreements

}
else {

    Write-Host "[+] Nmap found."

}


# ============================================================
# Check application
# ============================================================

if (-not (Test-Path $ScriptPath)) {

    Write-Host ""
    Write-Host "[!] ryujin_nmap.py was not found:"
    Write-Host $ScriptPath

    exit 1
}


# ============================================================
# Create installation directory
# ============================================================

Write-Host ""
Write-Host "[*] Creating installation directory..."

New-Item `
    -ItemType Directory `
    -Force `
    -Path $InstallDir | Out-Null


# ============================================================
# Copy Python application
# ============================================================

Write-Host "[*] Installing Ryujin Nmap..."

Copy-Item `
    $ScriptPath `
    "$InstallDir\ryujin_nmap.py" `
    -Force


# ============================================================
# Create Windows launcher
# ============================================================

Write-Host "[*] Creating command: $AppName"

$Launcher = @"
@echo off
python "$InstallDir\ryujin_nmap.py" %*
"@

Set-Content `
    -Path "$InstallDir\$AppName.cmd" `
    -Value $Launcher `
    -Encoding ASCII


# ============================================================
# Add to user PATH
# ============================================================

Write-Host "[*] Adding Ryujin to PATH..."

$CurrentPath = [Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

if ([string]::IsNullOrEmpty($CurrentPath)) {

    $CurrentPath = ""

}

if ($CurrentPath -notlike "*$InstallDir*") {

    $NewPath = "$CurrentPath;$InstallDir"

    [Environment]::SetEnvironmentVariable(
        "Path",
        $NewPath,
        "User"
    )

}


# ============================================================
# Complete
# ============================================================

Write-Host ""
Write-Host "=============================================="
Write-Host "        RYUJIN NMAP INSTALLATION COMPLETE"
Write-Host "=============================================="
Write-Host ""

Write-Host "Close this terminal and open a new terminal."

Write-Host ""
Write-Host "Then run:"
Write-Host ""
Write-Host "    ryujin-nmap"
Write-Host ""
