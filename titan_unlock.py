"""
TITAN ULTRA — Owner Authentication Tool

  First-time setup (only once ever):
      python titan_unlock.py --init

  Unlock on a new computer:
      python titan_unlock.py
"""

import sys, hashlib, getpass
from pathlib import Path

_AUTH_FILE = Path.home() / ".titan_ultra" / ".owner_auth"

def _banner():
    print("=" * 44)
    print("   TITAN ULTRA — Owner Authentication")
    print("=" * 44)

def init_mode():
    _banner()
    print("\n[SETUP MODE] Choose your secret owner code.")
    print("Pick something only you know.\n")
    code = getpass.getpass("Choose owner code: ").strip()
    confirm = getpass.getpass("Confirm owner code: ").strip()
    if code != confirm:
        print("\n❌ Codes do not match. Try again.")
        sys.exit(1)
    h = hashlib.sha256(code.encode()).hexdigest()
    print("\n" + "=" * 44)
    print("  Copy the line below into TITAN_ULTRA.py")
    print("  replacing PASTE_OWNER_HASH_HERE:")
    print("=" * 44)
    print(f'\n  _OWNER_HASH = "{h}"\n')
    print("Then push TITAN_ULTRA.py to GitHub.")
    print("=" * 44)
    _AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    _AUTH_FILE.write_text(h)
    print("\n✅ This computer is already unlocked as owner.")

def unlock_mode():
    _banner()
    print("\nType your secret owner code to get unlimited access.\n")
    code = getpass.getpass("Owner code: ").strip()
    h = hashlib.sha256(code.encode()).hexdigest()
    _AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    _AUTH_FILE.write_text(h)
    print("\n✅ Done! Run TITAN_ULTRA.py — you have full owner access.")

def revoke_mode():
    if _AUTH_FILE.exists():
        _AUTH_FILE.unlink()
        print("✅ Owner access removed from this computer.")
    else:
        print("No owner auth found on this computer.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--init":
            init_mode()
        elif sys.argv[1] == "--revoke":
            revoke_mode()
        else:
            print(f"Unknown: {sys.argv[1]}")
    else:
        unlock_mode()
