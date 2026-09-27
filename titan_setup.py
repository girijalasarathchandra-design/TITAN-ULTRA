"""
TITAN ULTRA — Universal Installer & Launcher
=============================================
Paste this ONE command in terminal to install and open TITAN ULTRA on any device:

  python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/titan-ultra/main/titan_setup.py').read().decode())"

After first run, just type:  titan
"""

import subprocess, sys, os, json, platform, urllib.request, shutil
from pathlib import Path

# ══════════════════════════════════════════════════════════════════
#  CONFIG — Fill in YOUR GitHub username below
# ══════════════════════════════════════════════════════════════════
GITHUB_USERNAME = "girijalasarathchandra-design"
GITHUB_REPO     = "titan-ultra"
GITHUB_BRANCH   = "main"

GITHUB_RAW      = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/{GITHUB_BRANCH}"
TITAN_PY_URL    = f"{GITHUB_RAW}/TITAN_ULTRA.py"
VERSION_URL     = f"{GITHUB_RAW}/version.txt"
SETUP_URL       = f"{GITHUB_RAW}/titan_setup.py"

API_KEY         = "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"

# ══════════════════════════════════════════════════════════════════
#  PATHS
# ══════════════════════════════════════════════════════════════════
TITAN_DIR    = Path.home() / ".titan_ultra"
TITAN_PY     = TITAN_DIR / "TITAN_ULTRA.py"
TITAN_KEY    = TITAN_DIR / ".titan_key"
TITAN_MEM    = TITAN_DIR / "titan_memory.json"
TITAN_CHATS  = TITAN_DIR / "titan_chats.json"
LOCAL_VER    = TITAN_DIR / "version.txt"
SETUP_FILE   = TITAN_DIR / "titan_setup.py"


# ══════════════════════════════════════════════════════════════════
#  PRINT HELPERS
# ══════════════════════════════════════════════════════════════════
def ok(msg):  print(f"  ✅ {msg}")
def info(msg): print(f"  ℹ️  {msg}")
def err(msg): print(f"  ❌ {msg}")
def step(msg): print(f"\n  {msg}")


# ══════════════════════════════════════════════════════════════════
#  STEP 1 — Install Python packages
# ══════════════════════════════════════════════════════════════════
def install_packages():
    step("📦 Checking required packages...")
    packages = ["streamlit", "groq", "requests"]
    for pkg in packages:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "-q"],
            capture_output=True
        )
        if r.returncode == 0:
            ok(pkg)
        else:
            err(f"{pkg} failed — {r.stderr.decode()[:60]}")


# ══════════════════════════════════════════════════════════════════
#  STEP 2 — Download / auto-update TITAN ULTRA
# ══════════════════════════════════════════════════════════════════
def get_remote_version():
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=6) as r:
            return r.read().decode().strip()
    except Exception:
        return None

def get_local_version():
    try:
        return LOCAL_VER.read_text(encoding="utf-8").strip()
    except Exception:
        return None

def download_titan():
    step("⬇️  Checking for updates...")
    remote = get_remote_version()
    local  = get_local_version()

    if remote and local and remote == local and TITAN_PY.exists():
        ok(f"Already up to date  (version {local})")
        return

    if remote:
        info(f"New version available: {remote}")

    try:
        urllib.request.urlretrieve(TITAN_PY_URL, TITAN_PY)
        if remote:
            LOCAL_VER.write_text(remote, encoding="utf-8")
        ok("TITAN ULTRA updated!")
    except Exception as e:
        if TITAN_PY.exists():
            info("Could not reach GitHub — using saved version.")
        else:
            err(f"Download failed: {e}")
            sys.exit(1)

    # Also save the latest setup script to local folder
    try:
        urllib.request.urlretrieve(SETUP_URL, SETUP_FILE)
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════
#  STEP 3 — Ask for name (first time only)
# ══════════════════════════════════════════════════════════════════
def setup_name():
    step("👤 Profile setup...")

    if TITAN_MEM.exists():
        try:
            memory = json.loads(TITAN_MEM.read_text(encoding="utf-8"))
        except Exception:
            memory = {}
    else:
        memory = {}

    if "name" not in memory:
        print()
        print("  ╔══════════════════════════════════╗")
        print("  ║   🔱  Welcome to TITAN ULTRA!    ║")
        print("  ║                                  ║")
        print("  ║  What is your name?              ║")
        print("  ╚══════════════════════════════════╝")
        name = input("  >> ").strip()
        if not name:
            name = "User"
        memory["name"] = name
        TITAN_MEM.write_text(json.dumps(memory, indent=2, ensure_ascii=False), encoding="utf-8")
        ok(f"Name saved permanently: {name}")
    else:
        ok(f"Welcome back, {memory['name']}!")


# ══════════════════════════════════════════════════════════════════
#  STEP 4 — Save API key (first time only)
# ══════════════════════════════════════════════════════════════════
def setup_key():
    if not TITAN_KEY.exists():
        TITAN_KEY.write_text(API_KEY, encoding="utf-8")


# ══════════════════════════════════════════════════════════════════
#  STEP 5 — Create "titan" launcher command
# ══════════════════════════════════════════════════════════════════
def create_launcher():
    step("📌 Creating 'titan' launcher...")

    if platform.system() == "Windows":
        # titan.bat — double-click or type 'titan' if folder is in PATH
        bat_path = TITAN_DIR / "titan.bat"
        bat_path.write_text(
            f'@echo off\n'
            f'title TITAN ULTRA\n'
            f'color 0B\n'
            f'echo.\n'
            f'echo  [TITAN] Starting...\n'
            f'python "{SETUP_FILE}"\n',
            encoding="utf-8"
        )

        # Also copy to a simple location on Desktop
        desktop = Path.home() / "Desktop" / "titan.bat"
        try:
            shutil.copy(bat_path, desktop)
            ok(f"titan.bat saved to Desktop — double-click anytime to open!")
        except Exception:
            ok(f"Launcher saved: {bat_path}")

        # Add to PATH automatically (user-level, no admin needed)
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE
            )
            try:
                current_path, _ = winreg.QueryValueEx(key, "PATH")
            except FileNotFoundError:
                current_path = ""
            titan_dir_str = str(TITAN_DIR)
            if titan_dir_str not in current_path:
                new_path = current_path + ";" + titan_dir_str if current_path else titan_dir_str
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                info("Added to PATH — open a new terminal and type: titan")
            else:
                info("Already in PATH — type: titan")
            winreg.CloseKey(key)
        except Exception:
            info(f"To type 'titan' anywhere, add this to your PATH:\n     {TITAN_DIR}")

    else:
        # Mac / Linux
        sh_path = TITAN_DIR / "titan.sh"
        sh_path.write_text(
            f'#!/bin/bash\n'
            f'python3 "{SETUP_FILE}"\n',
            encoding="utf-8"
        )
        os.chmod(sh_path, 0o755)

        # Add alias to shell profile
        shell_rc = Path.home() / ".bashrc"
        if (Path.home() / ".zshrc").exists():
            shell_rc = Path.home() / ".zshrc"
        alias_line = f'\nalias titan="python3 \\"{SETUP_FILE}\\""\n'
        try:
            existing = shell_rc.read_text()
            if "alias titan=" not in existing:
                with open(shell_rc, "a") as f:
                    f.write(alias_line)
                info("Alias added — open new terminal and type: titan")
            else:
                info("Alias already set — type: titan")
        except Exception:
            info(f"To use 'titan' command, add this to ~/.bashrc:\n     alias titan='python3 \"{SETUP_FILE}\"'")


# ══════════════════════════════════════════════════════════════════
#  STEP 6 — Launch TITAN ULTRA
# ══════════════════════════════════════════════════════════════════
def launch():
    import threading, webbrowser, time

    step("🚀 Launching TITAN ULTRA...")
    print("  (browser will open automatically — do NOT close this window)\n")

    os.chdir(TITAN_DIR)

    # Kill any existing process on port 8501
    if platform.system() == "Windows":
        subprocess.run(
            'for /f "tokens=5" %a in (\'netstat -aon 2>nul ^| findstr ":8501 "\') do taskkill /f /pid %a >nul 2>nul',
            shell=True, capture_output=True
        )
        time.sleep(1)  # wait for port to free up
    else:
        subprocess.run("fuser -k 8501/tcp 2>/dev/null", shell=True, capture_output=True)
        time.sleep(1)

    # Open browser after 3 seconds (streamlit needs time to start)
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
    threading.Thread(target=open_browser, daemon=True).start()

    subprocess.run([
        sys.executable, "-m", "streamlit", "run", str(TITAN_PY),
        "--server.port", "8501",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ])


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════
print()
print("  ╔══════════════════════════════════════════════╗")
print("  ║       🔱  T I T A N   U L T R A  🔱         ║")
print("  ╚══════════════════════════════════════════════╝")

TITAN_DIR.mkdir(parents=True, exist_ok=True)

install_packages()
download_titan()
setup_name()
setup_key()
create_launcher()
launch()
