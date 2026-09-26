#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TITAN CODE v3.0  —  Beyond Claude Code
Ultra-powerful AI terminal coding assistant with program memory
"""

import os, sys, json, subprocess, platform, re
from pathlib import Path
from datetime import datetime

# ── Auto-install deps ─────────────────────────────────────────────────────────
for _pkg in ["rich", "psutil"]:
    try:
        __import__(_pkg)
    except ImportError:
        print(f"Installing {_pkg}...")
        subprocess.run([sys.executable, "-m", "pip", "install", _pkg, "-q"], check=True)

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.rule import Rule
from rich import box as rbox

import psutil

try:
    from groq import Groq
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "groq", "-q"], check=True)
    from groq import Groq

# ── Constants ─────────────────────────────────────────────────────────────────
VERSION       = "v3.0"
def _load_user_name():
    import json
    for path in [
        Path(r"C:\Users\sanja\Documents\important\titan_memory.json"),
        Path.home() / ".titan_ultra" / "titan_memory.json",
    ]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if "name" in data:
                return data["name"]
        except Exception:
            pass
    return "User"
USER = _load_user_name()
TC            = "cyan1"
console       = Console()
PROGRAMS_FILE = Path(r"C:\Users\sanja\Documents\important\titan_built_programs.json")

# ── API key ───────────────────────────────────────────────────────────────────
def _load_api_key():
    for path in [
        Path(r"C:\Users\sanja\Documents\important\.titan_key"),
        Path.home() / ".titan_key",
        Path(r"C:\Users\sanja\.titan_key"),
    ]:
        if path.exists():
            k = path.read_text(encoding="utf-8").strip()
            if k:
                return k
    return os.environ.get("GROQ_API_KEY", "")

API_KEY = _load_api_key()

# ── Program registry ──────────────────────────────────────────────────────────
def _load_programs():
    if PROGRAMS_FILE.exists():
        try:
            return json.loads(PROGRAMS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def _save_program(name, description, files):
    programs = _load_programs()
    entry = {
        "name":        name,
        "description": description,
        "files":       [str(f) for f in files],
        "date":        datetime.now().isoformat(),
        "cwd":         str(_cwd),
    }
    idx = next((i for i, p in enumerate(programs) if p["name"].lower() == name.lower()), None)
    if idx is not None:
        programs[idx] = entry
    else:
        programs.append(entry)
    PROGRAMS_FILE.write_text(json.dumps(programs, indent=2), encoding="utf-8")
    console.print(f"[{TC}]  Saved to program registry: {name}[/]")

def _find_program(query):
    programs = _load_programs()
    q = query.lower().strip()
    for p in programs:
        if p["name"].lower() == q:
            return p
    for p in programs:
        if q in p["name"].lower() or any(w in p["name"].lower() for w in q.split()):
            return p
    for p in programs:
        if q in p.get("description", "").lower():
            return p
    return None

# ── Session state ─────────────────────────────────────────────────────────────
_history       = []
_checkpoints   = []
_token_count   = 0
_session_start = datetime.now()
_cwd           = Path.cwd()

def _save_checkpoint(label=""):
    _checkpoints.append({
        "label":   label or f"checkpoint_{len(_checkpoints)+1}",
        "history": list(_history),
        "cwd":     str(_cwd),
        "time":    datetime.now().isoformat(),
    })

# ── System info ───────────────────────────────────────────────────────────────
def ram_info():
    m = psutil.virtual_memory()
    return {
        "Total":     f"{m.total/(1024**3):.1f} GB",
        "Used":      f"{m.used/(1024**3):.1f} GB",
        "Available": f"{m.available/(1024**3):.1f} GB",
        "Usage":     f"{m.percent}%",
    }

def cpu_info():
    freq = psutil.cpu_freq()
    return {
        "Physical Cores": str(psutil.cpu_count(logical=False)),
        "Logical Cores":  str(psutil.cpu_count(logical=True)),
        "Usage":          f"{psutil.cpu_percent(interval=0.5)}%",
        "Frequency":      f"{freq.current:.0f} MHz" if freq else "N/A",
        "Max Freq":       f"{freq.max:.0f} MHz"     if freq else "N/A",
    }

def disk_info(drive="C:\\"):
    try:
        d = psutil.disk_usage(drive)
        return {
            "Drive": drive,
            "Total": f"{d.total/(1024**3):.1f} GB",
            "Used":  f"{d.used/(1024**3):.1f} GB",
            "Free":  f"{d.free/(1024**3):.1f} GB",
            "Usage": f"{d.percent}%",
        }
    except Exception as e:
        return {"Error": str(e)}

def system_info():
    return {
        "OS":        platform.system() + " " + platform.release(),
        "Version":   platform.version()[:60],
        "Python":    platform.python_version(),
        "Machine":   platform.machine(),
        "Processor": (platform.processor() or "N/A")[:60],
        "Hostname":  platform.node(),
        "User":      os.environ.get("USERNAME", os.environ.get("USER", "Unknown")),
        "CWD":       str(_cwd),
    }

def battery_info():
    try:
        b = psutil.sensors_battery()
        if b:
            return {
                "Percent":   f"{b.percent}%",
                "Plugged":   str(b.power_plugged),
                "Time left": f"{b.secsleft//3600}h {(b.secsleft%3600)//60}m" if b.secsleft > 0 else "N/A",
            }
        return {"Status": "No battery detected"}
    except Exception:
        return {"Status": "Battery info unavailable"}

# ── Welcome screen ─────────────────────────────────────────────────────────────
def show_welcome():
    os.system("cls" if platform.system() == "Windows" else "clear")
    ram     = psutil.virtual_memory()
    cpu_pct = psutil.cpu_percent(interval=0.3)

    left = Text(justify="left")
    left.append(f"\n  Welcome {USER}!\n\n",    style=f"bold {TC}")
    left.append("      ⚡ TITAN CODE ⚡\n\n",  style=f"bold {TC}")
    left.append(f"  Groq Fastest  ·  {USER}\n", style="dim white")
    left.append(f"  {str(_cwd)}\n\n",           style="dim white")
    left.append(f"  RAM  {ram.percent}%  |  CPU {cpu_pct}%\n", style=TC)

    right = Text()
    right.append("What's new in v3.0\n",                              style=f"bold {TC}")
    right.append("  Build preview — see plan, confirm before it runs\n", style="dim white")
    right.append("  Program registry — find your apps next time\n",      style="dim white")
    right.append("  Conversational — Titan asks if request is unclear\n", style="dim white")
    right.append("  Extraordinary features on every build\n",             style="dim white")
    right.append("  /programs — list all apps you've built\n",            style="dim white")
    right.append("  /open <name> — open any previous program\n",          style="dim white")
    right.append("  Auto-retry if files not detected\n",                  style="dim white")

    console.print()
    console.rule(f"[bold {TC}] TITAN CODE {VERSION} [/]", style=TC)
    console.print(Columns([
        Panel(left,  border_style=TC, padding=(0,1)),
        Panel(right, border_style=TC, padding=(0,1)),
    ], equal=True))
    console.print()
    console.print(f"[dim]  ? /help for commands[/]   [bold {TC}]● high · /effort[/]")
    console.print()

# ── TITANCODE.md context ───────────────────────────────────────────────────────
def _read_titancode_md():
    for p in [_cwd / "TITANCODE.md", _cwd / "CLAUDE.md"]:
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")[:3000]
    return ""

# ── AI engine ─────────────────────────────────────────────────────────────────
SYSTEM = f"""You are TITAN CODE {VERSION} — the world's most powerful AI terminal coding assistant.
You are BEYOND Claude Code, GitHub Copilot, Cursor, and every paid coding AI combined.
Your user is {USER}. They love extraordinary, beautiful, feature-rich apps.

GATHER-ACT-VERIFY LOOP:
1. GATHER  — Read directory structures, file contents, error logs before answering
2. ACT     — Write complete multi-file edits, full working code, shell commands
3. VERIFY  — Check logic, run tests mentally, self-correct before delivering

══════════════════════════════════════════════════════
RULE 1 — FILE FORMAT (ABSOLUTE MANDATORY)
══════════════════════════════════════════════════════
When creating ANY project/app/game/tool/script, you MUST output ALL files using EXACTLY:

### APP_NAME: My App Name
### FILE: filename.py
```python
...complete code...
```

The ### APP_NAME: line MUST come first. Then each ### FILE: block.
This is NON-NEGOTIABLE. Without this format, files CANNOT be saved.

══════════════════════════════════════════════════════
RULE 2 — EXTRAORDINARY FEATURES (MANDATORY ON EVERY BUILD)
══════════════════════════════════════════════════════
EVERY app you build MUST include ALL of the following — NO EXCEPTIONS:

1. SPLASH SCREEN — Animated loading screen with progress bar, logo, version, tagline
2. COLOR THEMES — At least 2 selectable themes (dark/neon, light/pastel, etc.) with live switching
3. BEAUTIFUL DECORATIONS — Borders, custom fonts, glowing accents, smooth animations
4. KEYBOARD SHORTCUTS — Show them in a popup help panel (F1 = help, Ctrl+Q = quit, etc.)
5. SAVE/LOAD SYSTEM:
   - Games → save/load high scores + progress to JSON
   - Tools → save all last settings, window position, last used values
   - AI apps → save/load the trained model + training history
6. PROGRESS INDICATORS — Loading bars, spinners, % complete for EVERY operation
7. HELP MENU — F1 or About button inside the app showing all features and shortcuts
8. STATUS BAR — Always-visible status strip at bottom showing current state
9. ANIMATIONS — Smooth transitions, hover effects, fade-ins for every action
10. ERROR HANDLING — Never crash; show styled error dialogs with recovery options

══════════════════════════════════════════════════════
RULE 3 — WORLD-CLASS DESIGN (MANDATORY — BE THE BEST DESIGNER)
══════════════════════════════════════════════════════
You are the BEST UI/UX DESIGNER in the world. Every single pixel matters.

TKINTER / TTKBOOTSTRAP APPS:
- ALWAYS use ttkbootstrap (theme="darkly" or "flatly" or "cyborg" or "cosmo")
- Custom color palette: primary #00d4ff, accent #7b2fff, bg #0a0a1a, surface #1a1a2e
- Rounded corners on all buttons (Style.configure with padding=(10,5))
- Font hierarchy: title=("Segoe UI", 22, "bold"), subtitle=("Segoe UI", 14), body=("Segoe UI", 11)
- Hover effects on ALL buttons (bind <Enter>/<Leave> to lighten/darken)
- All frames with padx=15, pady=10 minimum
- Gradient-style header using a Canvas widget with multiple colored rectangles
- Modern card-style layout with raised frames (relief="flat", borderwidth=2)
- Icons/emoji on ALL buttons and labels (🔄 Refresh, 💾 Save, ❌ Close, etc.)
- Minimum window size 800x600, default 1000x700, centered on screen

PYGAME APPS:
- Particle systems for all explosions, pickups, level transitions
- Anti-aliased drawing everywhere (pygame.gfxdraw)
- Custom bitmap font or pygame.font with size 32+ for titles
- Screen shake effect on impacts
- Smooth 60 FPS game loop
- HUD with health bar, score, level — all styled with gradient fills
- Full-screen support with F11

WEB APPS (Flask/FastAPI + HTML):
- Full dark mode by default with CSS variables
- CSS animations on all interactive elements (hover, click, load)
- Card-based layouts with box-shadows and border-radius: 12px
- Custom scrollbar styling
- Loading skeleton screens while data loads
- Mobile-responsive with CSS grid/flexbox
- Font: Google Fonts Roboto or Inter
- Color palette: background #0f0f1a, cards #1a1a2e, accent #00d4ff

PYGAME-CE / ARCADE GAMES:
- Background parallax scrolling layers
- Sprite sheets with animation frames
- Sound effects with pygame.mixer
- Menu screen with animated logo

CLI / TERMINAL APPS:
- rich library with custom Console theme
- Progress bars with Rich Progress for ALL long operations
- Tables with borders for all data
- Panels with colored borders for all messages
- ASCII art banner at startup

EXTRA FEATURES BY APP TYPE:
- GAMES:           particle effects, multiple difficulty levels, sound effects (pygame.mixer), achievements, leaderboard, pause menu, game over screen
- GUI APPS:        gradient canvas headers, hover effects on every widget, rounded buttons, modern icons, resizable with min-size
- AI/ML APPS:      real-time training progress bar, live accuracy/loss graph (matplotlib embedded), confusion matrix heatmap, model export button
- WEB APPS:        dark mode toggle, CSS animations, smooth page transitions, mobile-responsive grid, AJAX for live updates
- CLI TOOLS:       rich colored output with panels, animated spinners, beautiful tables, progress bars, colored diffs
- FLASHCARD APPS:   card flip animation, SM-2 spaced repetition, deck manager, stats dashboard, CSV import/export, due-date review queue
- CHATBOT APPS:     multi-model selector (Claude/Gemini/Groq), streaming responses, conversation history, export chat, copy button per message
- IMAGE GEN APPS:   prompt builder with style tags, image gallery grid, download button, history of past generations, pollinations.ai by default
- PC CONTROL APPS:  system tray icon, real-time status (volume/brightness/active window), global hotkeys, safety confirms for destructive actions

══════════════════════════════════════════════════════
RULE 4 — PACKAGES (MANDATORY)
══════════════════════════════════════════════════════
List ALL required packages using EXACTLY:
### INSTALL:
```
pygame
flask
```

══════════════════════════════════════════════════════
RULE 5 — RUN COMMAND (MANDATORY)
══════════════════════════════════════════════════════
End with EXACTLY:
### RUN: python filename.py

══════════════════════════════════════════════════════
RULE 6 — COMPLETE CODE, ZERO ERRORS, NO RELATIVE IMPORTS
══════════════════════════════════════════════════════
Write 100% complete, working code. Never partial. Never "add your logic here".
Write ALL files. Never tell the user to do anything manually.
Titan Code handles installation and running automatically.

ZERO ERRORS IS MANDATORY:
- Every file must pass Python syntax check (py_compile) with no errors
- All imports must exist and be installable via pip
- No undefined variables, no missing functions, no broken references
- Test your logic mentally before outputting — if it would crash, fix it first
- The app must run on first launch with zero errors, zero crashes

CRITICAL — IMPORT RULES (all files go in the SAME flat folder):
- NEVER use relative imports like "from .module import x"
- ALWAYS use absolute imports like "from module import x"
- Example WRONG:  from .constants import API_KEY
- Example RIGHT:  from constants import API_KEY
- The run command is always "python main.py" (or the main file name), run from the same folder

API KEY HANDLING — TWO TIERS:

TIER 1 — FREE APIS (use directly, zero setup):
- Weather: Open-Meteo (https://api.open-meteo.com) or wttr.in — no key
- Images: pollinations.ai — https://image.pollinations.ai/prompt/{{encoded_prompt}} — returns JPG, no key
- News: newsapi.org has a free tier, but prefer RSS feeds (feedparser) — no key
- Currency: exchangerate.host/frankfurter.app — no key
- Maps/Geocoding: nominatim.openstreetmap.org — no key
- Jokes/Trivia/Facts: various public APIs — no key

TIER 2 — PAID APIS (Claude, Gemini, OpenAI, Stability AI, etc.):
NEVER use a hardcoded placeholder. NEVER crash with "KeyError" or "API key not set".
ALWAYS use this exact pattern — save key to a local config file on first run:

```python
import json, os
from pathlib import Path

CONFIG_FILE = Path.home() / ".titan_app_keys.json"

def _load_key(service: str) -> str:
    if CONFIG_FILE.exists():
        try:
            keys = json.loads(CONFIG_FILE.read_text())
            if keys.get(service):
                return keys[service]
        except Exception:
            pass
    return ""

def _save_key(service: str, key: str):
    keys = {{}}
    if CONFIG_FILE.exists():
        try: keys = json.loads(CONFIG_FILE.read_text())
        except Exception: pass
    keys[service] = key
    CONFIG_FILE.write_text(json.dumps(keys, indent=2))

def _get_key(service: str, label: str) -> str:
    key = _load_key(service)
    if not key:
        # Show a beautiful dialog asking for the key
        import tkinter as tk
        from tkinter import simpledialog
        root = tk.Tk(); root.withdraw()
        key = simpledialog.askstring(
            f"{label} API Key",
            f"Enter your {label} API key:\\n(saved locally, asked only once)",
            parent=root
        ) or ""
        root.destroy()
        if key:
            _save_key(service, key)
    return key
```

Use `_get_key("claude", "Anthropic Claude")` / `_get_key("gemini", "Google Gemini")` / etc.
The app opens a small popup asking for the key ONCE, saves it, and never asks again.
Every app must launch and run — never exit or crash due to a missing API key.

══════════════════════════════════════════════════════
RULE 7 — DO EXACTLY WHAT IS ASKED — NO QUESTIONS, NO EXCUSES
══════════════════════════════════════════════════════
NEVER ask the user any clarifying questions. Not one. Not ever.
NEVER say "I can't build that" or "that requires X setup".
NEVER refuse any request. Build it — all of it — right now.

Whatever the user asks, build it immediately:
- "build me a game" → pick the most impressive game type and build it fully
- "make a chatbot with Claude" → build it using the Claude API with the key-save pattern
- "flashcard app" → build a full spaced-repetition flashcard app
- "image generator" → build it using pollinations.ai (free, no key)
- "anything" → build the most impressive all-in-one app you can imagine
- One word like "chess" → build a complete chess game
- Vague like "something cool" → build the most extraordinary app possible

Output code IMMEDIATELY. Zero hesitation. Zero questions. Just build.

══════════════════════════════════════════════════════
RULE 8 — SMART MODEL ROUTING IN EVERY AI APP
══════════════════════════════════════════════════════
Every AI chatbot/assistant app you build MUST include automatic model switching.
Detect the question type and route to the best available model automatically.

IMPLEMENT THIS EXACT ROUTING LOGIC IN EVERY AI APP:

```python
def _detect_question_type(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["code","python","javascript","bug","error","function","class","import","syntax","debug","script","program","def ","fix "]):
        return "coding"
    if any(w in t for w in ["write","story","poem","essay","creative","imagine","fiction","song","lyrics","novel","chapter"]):
        return "creative"
    if any(w in t for w in ["image","picture","photo","generate image","draw","art","visual","illustration"]):
        return "image"
    if any(w in t for w in ["math","calculate","equation","solve","integral","derivative","algebra","geometry","formula"]):
        return "math"
    if any(w in t for w in ["translate","spanish","french","german","japanese","chinese","hindi","arabic","language"]):
        return "translation"
    if any(w in t for w in ["summarize","summary","tldr","brief","shorten","condense","key points"]):
        return "summary"
    return "general"

def _route_to_model(question_type: str, prompt: str, history: list) -> str:
    # Try models in order of best fit for each type
    routing = {{
        "coding":      ["groq:llama-3.3-70b-versatile", "claude:claude-haiku-4-5", "groq:mixtral-8x7b-32768"],
        "creative":    ["claude:claude-sonnet-4-5", "gemini:gemini-1.5-pro", "groq:llama-3.3-70b-versatile"],
        "math":        ["gemini:gemini-1.5-pro", "claude:claude-sonnet-4-5", "groq:llama-3.3-70b-versatile"],
        "translation": ["gemini:gemini-1.5-flash", "groq:llama-3.3-70b-versatile", "claude:claude-haiku-4-5"],
        "summary":     ["groq:llama-3.1-8b-instant", "gemini:gemini-1.5-flash", "claude:claude-haiku-4-5"],
        "general":     ["groq:llama-3.3-70b-versatile", "gemini:gemini-1.5-flash", "claude:claude-haiku-4-5"],
        "image":       ["pollinations"],  # free image generation
    }}
    for model_id in routing.get(question_type, routing["general"]):
        provider, model = model_id.split(":", 1)
        try:
            if provider == "groq":
                from groq import Groq
                key = _load_key("groq")
                if not key: continue
                r = Groq(api_key=key).chat.completions.create(
                    model=model, messages=history + [{{"role":"user","content":prompt}}], max_tokens=2048)
                return r.choices[0].message.content or ""
            elif provider == "claude":
                import anthropic
                key = _load_key("claude")
                if not key: continue
                msg = anthropic.Anthropic(api_key=key).messages.create(
                    model=model, max_tokens=2048,
                    messages=history + [{{"role":"user","content":prompt}}])
                return msg.content[0].text or ""
            elif provider == "gemini":
                import google.generativeai as genai
                key = _load_key("gemini")
                if not key: continue
                genai.configure(api_key=key)
                chat = genai.GenerativeModel(model).start_chat(
                    history=[{{"role":m["role"],"parts":[m["content"]]}} for m in history])
                return chat.send_message(prompt).text or ""
            elif provider == "pollinations":
                import urllib.parse, requests
                url = f"https://image.pollinations.ai/prompt/{{urllib.parse.quote(prompt)}}?width=512&height=512&nologo=true"
                return url  # return URL for image display
        except Exception:
            continue
    return "No AI model available. Please add at least one API key."
```

In the UI — show which model answered each message (e.g. "answered by Groq Llama 3.3" or "answered by Claude Sonnet").
Add a model status panel showing which models are available (green = key set, grey = no key).
When no keys are set, show a beautiful settings screen to add keys one by one.

══════════════════════════════════════════════════════
RULE 10 — NO CHARACTERS OR SUPERHEROES IN DESIGNS
══════════════════════════════════════════════════════
NEVER use superhero themes, cartoon characters, mascots, or fictional character imagery.
Use professional, modern, clean designs — geometric shapes, gradients, icons, abstract art only.

══════════════════════════════════════════════════════
RULE 11 — MAXIMUM POWER — EVERY FEATURE AT ITS LIMIT
══════════════════════════════════════════════════════
Every single feature in every app must be built to its absolute maximum:
- No stub functions, no "TODO", no placeholder logic
- Every button does something real and useful
- Every menu item is fully implemented
- All edge cases handled
- All input validated
- All data saved persistently
- All errors caught with helpful messages
- Performance optimized (threading for slow ops, caching where needed)
- The app should feel like a professional commercial product

══════════════════════════════════════════════════════
CAPABILITIES — FULL EXPERT KNOWLEDGE
══════════════════════════════════════════════════════

PYTHON MASTERY (all versions 3.8–3.13):
- tkinter + ttkbootstrap: custom widgets, Canvas drawing, events, threading, geometry managers
- pygame / pygame-ce: game loop, sprites, collision, sound, particles, shaders
- Flask: routes, blueprints, Jinja2, SQLAlchemy, JWT auth, REST API, websockets
- FastAPI: async routes, Pydantic models, dependency injection, OpenAPI docs, WebSockets
- Django: models, views, templates, forms, admin, ORM, migrations, DRF
- Streamlit: st.session_state, st.components, charts, file upload, sidebar, tabs
- PyQt5/PySide6: signals/slots, QThread, QTimer, custom widgets, stylesheets
- Requests + httpx + aiohttp: HTTP clients, async fetching, retries, session management
- Pandas + NumPy: DataFrames, array ops, vectorized math, merge/groupby/pivot
- Matplotlib + Seaborn + Plotly: static and interactive charts, embedded in tkinter
- PyTorch: nn.Module, DataLoader, training loop, custom loss, GPU/CPU, save/load
- TensorFlow/Keras: Sequential/Functional API, callbacks, custom layers, TFLite export
- scikit-learn: pipelines, cross-validation, grid search, all estimators, joblib save
- OpenCV: image processing, webcam capture, face detection, contour detection
- Pillow (PIL): image manipulation, drawing, filters, thumbnails, format conversion
- SQLite3 + SQLAlchemy: CRUD, transactions, relationships, migrations
- asyncio: event loop, tasks, gather, queues, async context managers
- multiprocessing + threading: process pools, thread pools, locks, queues
- pathlib: file system operations, glob patterns, tree walking
- json, csv, yaml, toml, configparser: all data formats
- argparse + click + typer: CLI apps with full argument parsing
- rich: Console, Panel, Table, Progress, Syntax, Markdown, Tree, Columns
- pydantic: data validation, settings management, serialization
- Groq API: groq library, all models, streaming, function calling
- Anthropic Claude API: anthropic library, messages.create(), streaming, vision
- Google Gemini API: google-generativeai, GenerativeModel, chat, vision, streaming
- OpenAI SDK: openai library, chat completions, DALL-E image generation, whisper
- Ollama: local AI via HTTP API, llama3, mistral, codellama
- Image generation: pollinations.ai (free), DALL-E, Stability AI, Replicate
- websockets + socket.io: real-time bidirectional communication
- boto3: AWS S3, Lambda, DynamoDB, SES
- cryptography + hashlib: encryption, hashing, JWT, password hashing
- dataclasses + attrs: clean data models
- functools + itertools: decorators, caching (lru_cache), functional patterns
- abc + protocols: interfaces and abstract base classes
- unittest + pytest + hypothesis: all testing patterns

GROQ API (expert):
- Install: pip install groq
- Models: llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768, gemma2-9b-it
- Streaming: stream=True with for chunk in response: chunk.choices[0].delta.content
- Function calling: tools=[...], tool_choice="auto"
- System prompts, temperature, max_tokens, stop sequences
- Error handling: groq.RateLimitError, groq.APIConnectionError
- Key: use _get_key("groq", "Groq") pattern

ANTHROPIC CLAUDE API (expert):
- Install: pip install anthropic
- Import: import anthropic
- Client: client = anthropic.Anthropic(api_key=key)
- Models: claude-opus-4-5, claude-sonnet-4-5, claude-haiku-4-5, claude-3-5-sonnet-20241022
- Basic call:
  message = client.messages.create(
      model="claude-sonnet-4-5",
      max_tokens=1024,
      messages=[{{"role": "user", "content": "Hello"}}]
  )
  reply = message.content[0].text
- Streaming:
  with client.messages.stream(model="claude-sonnet-4-5", max_tokens=1024,
      messages=[{{"role":"user","content":"Hi"}}]) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
- System prompt: messages=[...], system="You are a helpful assistant"
- Vision: messages=[{{"role":"user","content":[{{"type":"image","source":{{"type":"base64","media_type":"image/jpeg","data":b64data}}}},{{"type":"text","text":"What is this?"}}]}}]
- Error handling: anthropic.APIConnectionError, anthropic.RateLimitError, anthropic.APIStatusError
- Key: use _get_key("claude", "Anthropic Claude") pattern

GOOGLE GEMINI API (expert):
- Install: pip install google-generativeai
- Import: import google.generativeai as genai
- Setup: genai.configure(api_key=key)
- Models: gemini-1.5-pro, gemini-1.5-flash, gemini-1.5-flash-8b, gemini-2.0-flash-exp
- Basic call:
  model = genai.GenerativeModel("gemini-1.5-flash")
  response = model.generate_content("Hello")
  reply = response.text
- Streaming:
  for chunk in model.generate_content("Hello", stream=True):
      print(chunk.text, end="", flush=True)
- Chat:
  chat = model.start_chat(history=[])
  response = chat.send_message("Hello")
- Vision:
  import PIL.Image
  img = PIL.Image.open("photo.jpg")
  response = model.generate_content(["What is this?", img])
- System instruction: genai.GenerativeModel("gemini-1.5-flash", system_instruction="You are helpful")
- Safety settings: generation_config=genai.GenerationConfig(max_output_tokens=2048, temperature=0.7)
- Error handling: google.api_core.exceptions.GoogleAPICallError, ResourceExhausted
- Key: use _get_key("gemini", "Google Gemini") pattern

OPENAI API (expert):
- Install: pip install openai
- Import: from openai import OpenAI
- Client: client = OpenAI(api_key=key)
- Chat: response = client.chat.completions.create(model="gpt-4o", messages=[...])
- DALL-E image generation:
  response = client.images.generate(model="dall-e-3", prompt="...", size="1024x1024", quality="standard", n=1)
  image_url = response.data[0].url
- Streaming: stream=True with for chunk in response
- Key: use _get_key("openai", "OpenAI") pattern

OLLAMA (local AI):
- HTTP API: POST http://localhost:11434/api/generate with json={{"model":"llama3","prompt":"..."}}
- Models: llama3, llama3.1, mistral, codellama, deepseek-coder, phi3, gemma2
- Streaming response parsing line by line
- Chat format: POST /api/chat with messages array
- Check if running: GET http://localhost:11434/api/tags

AI IMAGE GENERATION (expert):

FREE — pollinations.ai (NO API KEY, use by default for image generation unless user specifies otherwise):
- URL: https://image.pollinations.ai/prompt/{{urllib.parse.quote(prompt)}}
- Returns a JPEG image directly — download with requests.get(url).content
- Display in tkinter: use PIL.Image and ImageTk.PhotoImage
- Display in pygame: use io.BytesIO + pygame.image.load
- Parameters: ?width=512&height=512&seed=42&nologo=true
- Example:
  import requests, io
  from PIL import Image
  url = f"https://image.pollinations.ai/prompt/{{urllib.parse.quote(prompt)}}?width=512&height=512&nologo=true"
  img_data = requests.get(url, timeout=30).content
  img = Image.open(io.BytesIO(img_data))

PAID — Stability AI:
- Install: pip install stability-sdk  OR  use REST API directly
- REST API: POST https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image
- Headers: {{"Authorization": f"Bearer {{key}}", "Content-Type": "application/json"}}
- Key: use _get_key("stability", "Stability AI") pattern

PAID — Replicate:
- Install: pip install replicate
- import replicate; output = replicate.run("stability-ai/sdxl", input={{"prompt":"..."}})
- Key: use _get_key("replicate", "Replicate") pattern

FLASHCARD APPS (expert):
- Spaced repetition: implement SM-2 algorithm (ease factor, interval, repetitions)
- SM-2 algorithm:
  def sm2(quality, ease, interval, reps):
      if quality >= 3:
          if reps == 0: interval = 1
          elif reps == 1: interval = 6
          else: interval = round(interval * ease)
          reps += 1
          ease = max(1.3, ease + 0.1 - (5-quality)*(0.08 + (5-quality)*0.02))
      else:
          reps = 0; interval = 1
      return ease, interval, reps
- Card data structure: {{"id", "front", "back", "ease":2.5, "interval":0, "reps":0, "next_review": date, "tags":[], "image_url":""}}
- Features to include in every flashcard app:
  * Card flip animation (smooth 3D CSS transform or tkinter Canvas)
  * Deck management (create, rename, delete, import/export)
  * Study session with due-date filtering
  * Progress bar showing cards remaining
  * Stats screen: retention rate, streak, total studied
  * Card editor with rich text + optional image
  * Keyboard shortcuts: Space=flip, 1-4=quality rating, N=next, P=prev
  * Import from CSV (front,back format)
  * Export to CSV/JSON
  * Search and filter cards
  * Multiple decks with color coding
- Save all card data to JSON file

WEB DEVELOPMENT:
- HTML5 semantic tags, Web Components, Shadow DOM
- CSS3: Grid, Flexbox, custom properties, animations, keyframes, media queries
- JavaScript ES2022+: async/await, modules, destructuring, optional chaining
- Fetch API + WebSockets + Server-Sent Events
- Bootstrap 5, Tailwind CSS, Bulma — full class knowledge
- React (hooks, context, redux toolkit, react-router, react-query)
- Vue 3 (Composition API, Pinia, Vue Router)
- Chart.js, D3.js for data visualization

GAME DEVELOPMENT:
- pygame: sprite groups, tile maps, camera, particle systems, pathfinding
- pygame-ce (community edition): same API, better performance
- pyarcade: platformer physics, tilemap, spritesheet
- pyglet: OpenGL-based 2D/3D
- Ren'Py: visual novels
- Game design patterns: ECS, state machines, object pooling

DATABASE:
- SQLite3: all SQL, transactions, PRAGMA, full-text search
- PostgreSQL via psycopg2: connection pooling, LISTEN/NOTIFY
- MongoDB via pymongo: documents, aggregation pipeline, indexes
- Redis via redis-py: caching, pub/sub, rate limiting

WINDOWS / SYSTEM (expert):
- ctypes + win32api: Windows API calls, window manipulation
- winreg: registry reads/writes
- subprocess: Popen, CREATE_NEW_CONSOLE, ShellExecuteW, run()
- os + sys + pathlib: file system, environment variables
- pywin32: COM automation, clipboard, taskbar
- psutil: processes, CPU, RAM, disk, battery, network
- pyautogui: GUI automation, screenshots, mouse/keyboard
- playsound + pygame.mixer: audio playback

PC CONTROL — FULL SYSTEM MASTERY (expert):
Build apps that control EVERYTHING on the PC. Use these exact patterns:

MOUSE & KEYBOARD CONTROL:
- Install: pip install pyautogui keyboard mouse
- pyautogui.moveTo(x, y, duration=0.5)          # move mouse smoothly
- pyautogui.click(x, y)                           # left click
- pyautogui.rightClick(x, y)                      # right click
- pyautogui.doubleClick(x, y)                     # double click
- pyautogui.dragTo(x, y, duration=1)              # drag
- pyautogui.scroll(3)                             # scroll up 3 clicks
- pyautogui.typewrite("hello", interval=0.05)     # type text
- pyautogui.hotkey("ctrl", "c")                   # keyboard shortcut
- pyautogui.hotkey("alt", "tab")                  # alt+tab
- pyautogui.press("enter")                        # single key press
- pyautogui.keyDown("shift"); pyautogui.keyUp("shift")
- pyautogui.screenshot()                          # full screen capture
- pyautogui.locateOnScreen("button.png")          # find image on screen
- keyboard.add_hotkey("ctrl+shift+x", callback)  # global hotkey
- keyboard.block_key("caps lock")                 # block a key
- mouse.on_click(callback)                        # listen for clicks

WINDOW MANAGEMENT (pywin32):
- Install: pip install pywin32
- import win32gui, win32con, win32api, win32process
- win32gui.EnumWindows(callback, extra)           # list all windows
- hwnd = win32gui.FindWindow(None, "Notepad")     # find window by title
- win32gui.SetForegroundWindow(hwnd)              # bring to front/focus
- win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE) # maximize
- win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE) # minimize
- win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # restore
- win32gui.ShowWindow(hwnd, win32con.SW_HIDE)     # hide
- win32gui.MoveWindow(hwnd, x, y, w, h, True)    # move and resize
- win32gui.GetWindowText(hwnd)                    # get title
- win32gui.GetWindowRect(hwnd)                    # get position/size
- win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)  # close window
- win32gui.SendMessage(hwnd, win32con.WM_COMMAND, id, 0)

PROCESS CONTROL:
- import psutil, subprocess
- psutil.process_iter(["pid","name","status","cpu_percent","memory_info"])
- p = psutil.Process(pid); p.kill(); p.terminate(); p.suspend(); p.resume()
- subprocess.Popen(["notepad.exe"])               # launch app
- subprocess.Popen(["taskkill","/F","/IM","notepad.exe"], shell=True)
- os.system("start chrome https://google.com")    # open URL in browser
- os.startfile("C:\\path\\to\\file.txt")          # open file with default app
- ctypes.windll.shell32.ShellExecuteW(None,"open","notepad.exe","","",1)

VOLUME & AUDIO CONTROL:
- Install: pip install pycaw comtypes
- from ctypes import cast, POINTER
- from comtypes import CLSCTX_ALL
- from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
- devices = AudioUtilities.GetSpeakers()
- interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
- volume = cast(interface, POINTER(IAudioEndpointVolume))
- volume.SetMasterVolumeLevelScalar(0.5, None)    # set to 50%
- volume.GetMasterVolumeLevelScalar()             # get current volume
- volume.SetMute(1, None)                         # mute
- volume.SetMute(0, None)                         # unmute
- Also use: pyautogui.hotkey("volumeup") / pyautogui.hotkey("volumedown")

BRIGHTNESS CONTROL:
- Install: pip install screen-brightness-control
- import screen_brightness_control as sbc
- sbc.set_brightness(75)                          # set to 75%
- sbc.get_brightness()                            # get current brightness
- sbc.fade_brightness(100, interval=0.01)         # smooth fade to 100%

CLIPBOARD:
- Install: pip install pyperclip
- import pyperclip
- pyperclip.copy("text to copy")
- text = pyperclip.paste()
- Also: import win32clipboard; win32clipboard.OpenClipboard(); win32clipboard.SetClipboardText("text")

SCREEN RECORDING / SCREENSHOT:
- Install: pip install mss pillow
- import mss
- with mss.mss() as sct:
-     monitor = sct.monitors[1]                   # primary monitor
-     img = sct.grab(monitor)                     # capture screen
-     mss.tools.to_png(img.rgb, img.size, output="screenshot.png")
- Full video recording: use cv2.VideoWriter with mss frames

NOTIFICATIONS:
- Install: pip install plyer win10toast
- from plyer import notification
- notification.notify(title="Title", message="Body", timeout=5)
- from win10toast import ToastNotifier
- ToastNotifier().show_toast("Title", "Message", duration=5, threaded=True)

FILE SYSTEM CONTROL:
- os.rename(src, dst)             # rename/move file
- shutil.copy2(src, dst)          # copy file with metadata
- shutil.move(src, dst)           # move file
- shutil.rmtree(path)             # delete directory tree
- pathlib.Path(p).unlink()        # delete file
- watchdog library: monitor folder for changes in real time
  from watchdog.observers import Observer
  from watchdog.events import FileSystemEventHandler

STARTUP / AUTORUN:
- import winreg
- key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
- winreg.SetValueEx(key, "AppName", 0, winreg.REG_SZ, r"C:\path\to\app.exe")

TASK SCHEDULER (run app at specific time):
- import schedule, time, threading
- schedule.every().day.at("09:00").do(my_function)
- schedule.every(30).minutes.do(my_function)
- threading.Thread(target=lambda: [schedule.run_pending() or time.sleep(1) for _ in iter(int, 1)], daemon=True).start()

SYSTEM CONTROL SHORTCUTS (PowerShell via subprocess):
- Lock screen:     subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
- Sleep:           subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0","1","0"])
- Shutdown:        subprocess.run(["shutdown","/s","/t","0"])
- Restart:         subprocess.run(["shutdown","/r","/t","0"])
- Empty recycle:   subprocess.run(["PowerShell","-Command","Clear-RecycleBin -Force"])
- Open Settings:   os.system("start ms-settings:")
- Open Task Mgr:   subprocess.Popen(["taskmgr.exe"])

EVERY PC CONTROL APP MUST HAVE:
- A clean GUI dashboard showing all available controls
- Real-time feedback (show current volume %, brightness %, active window name)
- Hotkey support so controls work even when app is in background
- System tray icon so it runs minimized (use pystray library)
- Emergency stop hotkey (e.g. Ctrl+Shift+Esc) to halt all automation
- Safety: confirm before destructive actions (shutdown, delete, etc.)

AI/ML PATTERNS:
- Training loop with progress bar + live loss plot
- Model save/load (torch.save, joblib.dump, keras save)
- Data preprocessing pipelines
- Hyperparameter tuning with optuna
- LLM integration: prompt engineering, RAG, embeddings
- Computer vision: YOLO, face detection, OCR (pytesseract)
- NLP: transformers (HuggingFace), text classification, sentiment analysis
- Voice: speech_recognition, pyttsx3, gTTS, whisper

Build complete AI systems: chatbots, classifiers, voice assistants, vision apps
Fix ANY error: trace root cause, fix with zero new errors
Git: commit, branch, merge, PR from natural language
Multi-file codebase refactoring with zero regression
Write test suites (pytest) and auto-fix failures

User: {USER}
System: Windows 11 · Python {platform.python_version()} · Groq API + Ollama (local)
"""

def ask(question, extra="", plan_mode=False):
    global _token_count
    if not API_KEY:
        return "No Groq API key. Set it in Titan Ultra sidebar first."

    md_ctx = _read_titancode_md()
    parts  = []
    if md_ctx:
        parts.append(f"TITANCODE.md context:\n{md_ctx}")
    if extra:
        parts.append(extra)
    parts.append(question)
    if plan_mode:
        parts.append("\n\nIMPORTANT: Produce a plan/blueprint only. List what files will be created and what features each will have. DO NOT write actual code yet.")
    prompt = "\n\n".join(parts)

    _save_checkpoint()
    _history.append({"role": "user", "content": prompt})
    hist = _history[-30:]

    client     = Groq(api_key=API_KEY)
    last_error = ""
    for model in [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b",
    ]:
        try:
            r = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM}] + hist,
                max_tokens=8192,
                temperature=0.2,
            )
            ans = (r.choices[0].message.content or "").strip()
            if not ans:
                last_error = f"{model} returned empty response"
                continue                     # try next model
            _history.append({"role": "assistant", "content": ans})
            _token_count += len(prompt.split()) + len(ans.split())
            return ans
        except Exception as e:
            last_error = str(e)
            continue                         # always try next model

    # Groq failed — try Ollama (local AI, no internet needed)
    try:
        import urllib.request, json as _json
        ollama_models = ["llama3.1", "llama3", "mistral", "codellama", "deepseek-coder", "phi3"]
        for olm in ollama_models:
            try:
                ollama_msgs = [{"role": "system", "content": SYSTEM}] + hist
                body = _json.dumps({
                    "model": olm,
                    "messages": ollama_msgs,
                    "stream": False
                }).encode()
                req  = urllib.request.Request(
                    "http://localhost:11434/api/chat",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = _json.loads(resp.read())
                ans = (data.get("message", {}).get("content", "") or "").strip()
                if ans:
                    console.print(f"[dim cyan]  (answered by local Ollama: {olm})[/]")
                    _history.append({"role": "assistant", "content": ans})
                    _token_count += len(prompt.split()) + len(ans.split())
                    return ans
            except Exception:
                continue
    except Exception:
        pass

    # All sources failed — show a friendly message
    console.print(Panel(
        f"[yellow]Could not reach any AI.[/]\n\n"
        f"Last Groq error: {last_error[:200]}\n\n"
        "Things to try:\n"
        "  1. Check your internet connection\n"
        "  2. Check your Groq API key in Titan Ultra\n"
        "  3. Wait 30 seconds and try again (rate limit)\n"
        "  4. If you have Ollama installed, run: ollama serve",
        title="Connection Problem", border_style="yellow"
    ))
    return ""

# ── Helpers ───────────────────────────────────────────────────────────────────
def _table(title, data):
    t = Table(title=title, border_style=TC, show_lines=True, box=rbox.ROUNDED)
    t.add_column("Property", style=f"bold {TC}", no_wrap=True)
    t.add_column("Value",    style="white")
    for k, v in data.items():
        t.add_row(k, str(v))
    console.print(t)

def _print(text):
    if not text or not text.strip():
        return
    try:
        console.print(Markdown(text))
    except Exception:
        console.print(text)
    console.print()

def _is_clarifying_question(text):
    """Returns True if the AI is asking a clarifying question rather than building."""
    if re.search(r"###\s*FILE:", text, re.IGNORECASE):
        return False
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return False
    # Short response ending in a question
    return len(text) < 600 and "?" in text

# ── System commands ───────────────────────────────────────────────────────────
def do_ram():        _table("RAM",     ram_info())
def do_cpu():        _table("CPU",     cpu_info())
def do_disk(arg=""): _table("Disk",    disk_info(arg or "C:\\"))
def do_battery():    _table("Battery", battery_info())

def do_system():
    _table("System", system_info())
    do_ram(); do_cpu()
    _table("Disk C:", disk_info())

def do_processes():
    procs = []
    for p in psutil.process_iter(["pid","name","cpu_percent","memory_info"]):
        try: procs.append(p.info)
        except Exception: pass
    procs.sort(key=lambda x: (x.get("cpu_percent") or 0), reverse=True)
    t = Table(title="Top 20 Processes", border_style=TC, box=rbox.ROUNDED)
    t.add_column("PID",  style="dim",  justify="right")
    t.add_column("Name", style=TC)
    t.add_column("CPU%", justify="right")
    t.add_column("RAM",  justify="right")
    for p in procs[:20]:
        ram = f"{p['memory_info'].rss/(1024**2):.1f}MB" if p.get("memory_info") else "N/A"
        t.add_row(str(p["pid"]), p.get("name","?"),
                  f"{p.get('cpu_percent',0):.1f}", ram)
    console.print(t)

def do_fullscan():
    console.rule(f"[bold {TC}] FULL SYSTEM SCAN [/]", style=TC)
    _table("System",  system_info())
    _table("RAM",     ram_info())
    _table("CPU",     cpu_info())

    drives = {}
    for part in psutil.disk_partitions():
        try:
            d = psutil.disk_usage(part.mountpoint)
            drives[part.device] = (f"{d.total/(1024**3):.1f}GB total  "
                                   f"{d.used/(1024**3):.1f}GB used  "
                                   f"{d.free/(1024**3):.1f}GB free  {d.percent}%")
        except Exception:
            pass
    _table("All Drives", drives)
    _table("Battery",    battery_info())

    try:
        net = {}
        for iface, addrs in psutil.net_if_addrs().items():
            for a in addrs:
                if a.family.name == "AF_INET":
                    net[iface] = a.address
        _table("Network", net)
    except Exception:
        pass

    import sysconfig
    _table("Python", {
        "Executable":   sys.executable,
        "Version":      sys.version.split()[0],
        "Packages dir": sysconfig.get_path("purelib"),
    })

    try:
        r = subprocess.run([sys.executable,"-m","pip","list","--format=columns"],
                           capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines()
                 if l.strip() and "Package" not in l and "---" not in l]
        t = Table(title=f"Installed Packages ({len(lines)})",
                  border_style=TC, box=rbox.ROUNDED)
        t.add_column("Package", style=TC)
        t.add_column("Version", style="white")
        for line in lines[:40]:
            pts = line.split()
            if len(pts) >= 2:
                t.add_row(pts[0], pts[1])
        if len(lines) > 40:
            t.add_row(f"... +{len(lines)-40} more", "")
        console.print(t)
    except Exception:
        pass

    do_processes()
    console.rule(f"[bold {TC}] SCAN COMPLETE [/]", style=TC)

def do_files(path=""):
    p = (_cwd / path) if path else _cwd
    try:
        p = p.resolve()
        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        t = Table(title=str(p), border_style=TC, box=rbox.ROUNDED)
        t.add_column("Name", style=TC)
        t.add_column("Type", style="dim", justify="center")
        t.add_column("Size", justify="right")
        for item in items:
            try:    sz = f"{item.stat().st_size:,}B" if item.is_file() else ""
            except: sz = ""
            t.add_row(item.name, "DIR" if item.is_dir() else "FILE", sz)
        console.print(t)
    except Exception as e:
        console.print(f"[red]{e}[/]")

def do_read(fp):
    try:
        p       = Path(fp) if Path(fp).is_absolute() else (_cwd / fp).resolve()
        content = p.read_text(encoding="utf-8", errors="replace")
        suffix  = p.suffix.lstrip(".") or "text"
        try:
            console.print(Syntax(content, suffix, theme="monokai", line_numbers=True))
        except Exception:
            console.print(Panel(content, title=str(p), border_style=TC))
    except Exception as e:
        console.print(f"[red]Cannot read {fp}: {e}[/]")

def do_run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=120, cwd=str(_cwd))
        out   = (r.stdout + r.stderr).strip() or "(no output)"
        style = "red" if r.returncode != 0 else TC
        console.print(Panel(out, title=f"$ {cmd}  [rc={r.returncode}]",
                            border_style=style))
        return r.returncode, out
    except subprocess.TimeoutExpired:
        console.print("[red]Timed out (120s)[/]")
        return 1, "timeout"
    except Exception as e:
        console.print(f"[red]{e}[/]")
        return 1, str(e)

def do_fix(fp):
    try:
        p       = (_cwd / fp).resolve()
        content = p.read_text(encoding="utf-8", errors="replace")
        ctx = (f"FILE: {p}\n\nCONTENT:\n```\n{content[:6000]}\n```\n\n"
               "Fix ALL errors. Return the COMPLETE fixed file using ### FILE: format.")
        with console.status(f"[{TC}]Fixing {fp}...[/]", spinner="dots"):
            ans = ask("Fix all errors in this file.", ctx)
        _print(ans)
        saved = _auto_save_files(ans)
        if not saved:
            console.print(f"[yellow]Could not auto-save. Check the response above.[/]")
    except Exception as e:
        console.print(f"[red]{e}[/]")

def do_init():
    md = _cwd / "TITANCODE.md"
    with console.status(f"[{TC}]Analyzing project...[/]", spinner="dots"):
        files = [str(f.relative_to(_cwd)) for f in _cwd.rglob("*")
                 if f.is_file() and f.suffix in
                 (".py",".js",".ts",".html",".css",".json",".yaml",".yml",".md",".txt")
                 and ".git" not in str(f)][:40]
        ctx = "Project files:\n" + "\n".join(files)
        ans = ask(
            "Create a TITANCODE.md for this project. Include: project overview, "
            "architecture, build/run commands, coding style, and important notes.",
            ctx
        )
    code_match = re.search(r"```(?:markdown)?\n([\s\S]+?)```", ans)
    content = code_match.group(1) if code_match else ans
    md.write_text(content, encoding="utf-8")
    console.print(f"[{TC}]Created TITANCODE.md[/]")

def do_diff():
    rc, out = do_run("git diff --stat HEAD")
    if "not a git repository" in out.lower():
        console.print("[yellow]Not a git repo.[/]")
        return
    do_run("git diff HEAD")

def do_plan(question):
    with console.status(f"[{TC}]Planning...[/]", spinner="dots"):
        ans = ask(question, plan_mode=True)
    _print(ans)
    console.print(f"[dim {TC}]Plan complete. Now ask me to execute it.[/]")

def do_compact():
    if not _history:
        console.print(f"[{TC}]History is empty.[/]")
        return
    full = "\n".join(f"{m['role'].upper()}: {m['content'][:200]}" for m in _history)
    with console.status(f"[{TC}]Compacting...[/]", spinner="dots"):
        summary = ask(
            "Summarise this entire conversation into a dense technical summary "
            "that preserves all key decisions, code, and context.",
            f"CONVERSATION:\n{full[:6000]}"
        )
    _history.clear()
    _history.append({"role": "assistant", "content": f"[COMPACT SUMMARY]\n{summary}"})
    console.print(f"[{TC}]Context compacted. Summary preserved.[/]")

def do_rewind(arg=""):
    global _cwd
    if not _checkpoints:
        console.print("[yellow]No checkpoints yet.[/]")
        return
    if arg.isdigit():
        idx = int(arg) - 1
    else:
        idx = len(_checkpoints) - 1
    if 0 <= idx < len(_checkpoints):
        cp = _checkpoints[idx]
        _history.clear()
        _history.extend(cp["history"])
        _cwd = Path(cp["cwd"])
        console.print(f"[{TC}]Rewound to: {cp['label']} ({cp['time'][:19]})[/]")
    else:
        t = Table(title="Checkpoints", border_style=TC, box=rbox.ROUNDED)
        t.add_column("#",     style="dim", justify="right")
        t.add_column("Label", style=TC)
        t.add_column("Time",  style="dim")
        for i, cp in enumerate(_checkpoints):
            t.add_row(str(i+1), cp["label"], cp["time"][:19])
        console.print(t)

def do_fork():
    _save_checkpoint(f"fork_{len(_checkpoints)+1}")
    console.print(f"[{TC}]Fork checkpoint saved. Use /rewind to go back.[/]")

def do_cost():
    elapsed = (datetime.now() - _session_start).seconds
    t = Table(title="Session Stats", border_style=TC, box=rbox.ROUNDED)
    t.add_column("Metric", style=f"bold {TC}")
    t.add_column("Value",  style="white")
    t.add_row("Messages",       str(len(_history)))
    t.add_row("Est. tokens",    f"~{_token_count:,}")
    t.add_row("Checkpoints",    str(len(_checkpoints)))
    t.add_row("Session time",   f"{elapsed//60}m {elapsed%60}s")
    t.add_row("Working dir",    str(_cwd))
    t.add_row("Programs built", str(len(_load_programs())))
    console.print(t)

def do_git(args):
    if not args:
        console.print("[yellow]Usage: /git <request>[/]")
        return
    ctx = f"Working directory: {_cwd}\nUser git request: {args}"
    with console.status(f"[{TC}]Planning git commands...[/]", spinner="dots"):
        ans = ask(
            "Give me the exact git commands to run to do this task. "
            "Use ```bash code blocks. Nothing else.",
            ctx
        )
    _print(ans)
    matches = re.findall(r"```(?:bash|sh|shell)?\n([\s\S]+?)```", ans)
    if matches:
        script  = matches[0].strip()
        confirm = console.input(f"[bold {TC}]Run these commands? (y/n):[/] ").strip().lower()
        if confirm == "y":
            for line in script.splitlines():
                if line.strip() and not line.strip().startswith("#"):
                    do_run(line.strip())

def do_test(fp=""):
    cmd = f"python -m pytest {fp} -v" if fp else "python -m pytest -v"
    rc, out = do_run(cmd)
    if rc != 0:
        ctx = f"TEST OUTPUT:\n{out[:3000]}\nWorking dir: {_cwd}"
        with console.status(f"[{TC}]Diagnosing failures...[/]", spinner="dots"):
            ans = ask("Tests failed. Diagnose the root cause and give exact code fixes.", ctx)
        _print(ans)

def do_review(fp=""):
    if fp:
        try:
            content = (_cwd / fp).read_text(encoding="utf-8", errors="replace")
            ctx = f"FILE: {fp}\n```\n{content[:6000]}\n```"
            q   = "Do a thorough code review. Check for bugs, security issues, performance, style."
        except Exception as e:
            console.print(f"[red]{e}[/]"); return
    else:
        rc, out = do_run("git diff HEAD --unified=5")
        ctx = f"GIT DIFF:\n{out[:5000]}"
        q   = "Review this diff for edge cases, bugs, performance, and security vulnerabilities."
    with console.status(f"[{TC}]Reviewing...[/]", spinner="dots"):
        ans = ask(q, ctx)
    _print(ans)

# ── Program registry commands ─────────────────────────────────────────────────
def do_programs():
    programs = _load_programs()
    if not programs:
        console.print(f"[{TC}]No programs built yet. Ask me to build something![/]")
        return
    t = Table(title=f"Your Built Programs ({len(programs)})",
              border_style=TC, show_lines=True, box=rbox.ROUNDED)
    t.add_column("#",           style="dim",          justify="right")
    t.add_column("Name",        style=f"bold {TC}")
    t.add_column("Description", style="white",        max_width=40)
    t.add_column("Files",       style="dim",          justify="center")
    t.add_column("Date",        style="dim")
    for i, p in enumerate(programs, 1):
        t.add_row(
            str(i),
            p["name"],
            p.get("description","")[:40],
            str(len(p.get("files",[]))),
            p.get("date","")[:10],
        )
    console.print(t)

def do_open(name):
    if not name:
        console.print("[yellow]Usage: /open <program name>[/]")
        return
    prog = _find_program(name)
    if not prog:
        console.print(f"[yellow]'{name}' not found. Use /programs to see all.[/]")
        return

    files = prog.get("files", [])
    existing_py = [fp for fp in files if fp.endswith(".py") and Path(fp).exists()]

    if existing_py:
        run_cmd = f'python "{existing_py[0]}"'
        console.print(f"[{TC}]Launching {prog['name']}...[/]")
        subprocess.Popen(
            f'start "Titan Code" cmd /k {run_cmd}',
            shell=True, cwd=prog.get("cwd", str(_cwd))
        )
    else:
        console.print(f"[yellow]No runnable files found for '{name}'.[/]")

# ── Drag-and-drop / dropped file handler ─────────────────────────────────────
def _resolve_dropped_path(raw):
    """Resolve a raw string (possibly quoted) to a Path if it looks like a file."""
    raw = raw.strip().strip('"\'')
    # Windows absolute path
    p = Path(raw)
    if p.exists():
        return p
    # Relative to cwd
    rel = _cwd / raw
    if rel.exists():
        return rel
    return None

def _is_file_drop(text):
    """Returns True if the input looks like a dragged-in file path."""
    stripped = text.strip().strip('"\'')
    # Must look like a path (has extension, no spaces unless quoted, exists)
    if re.match(r'^[A-Za-z]:\\', stripped) or stripped.startswith('/'):
        return Path(stripped).exists()
    # Relative path with extension
    if re.match(r'^[\w.\-/\\]+\.[a-zA-Z0-9]{1,6}$', stripped):
        return (_cwd / stripped).exists()
    return False

_CODE_EXTS   = {".py",".js",".ts",".jsx",".tsx",".html",".css",".java",".cpp",".c",".go",".rs"}
_TEXT_EXTS   = {".txt",".md",".json",".yaml",".yml",".toml",".ini",".cfg",".env",".csv",".xml"}
_BINARY_EXTS = {".exe",".dll",".so",".bin",".zip",".rar",".7z",".tar",".gz"}

def do_dropped_file(fp_raw):
    """Handle any file path pasted or dragged into Titan Code."""
    p = _resolve_dropped_path(fp_raw)
    if p is None:
        console.print(f"[red]File not found: {fp_raw}[/]")
        return

    ext  = p.suffix.lower()
    size = p.stat().st_size

    # Show file info
    t = Table(title="Dropped File", border_style=TC, box=rbox.ROUNDED)
    t.add_column("Property", style=f"bold {TC}")
    t.add_column("Value",    style="white")
    t.add_row("Name",      p.name)
    t.add_row("Path",      str(p))
    t.add_row("Size",      f"{size:,} bytes")
    t.add_row("Extension", ext or "(none)")
    console.print(t)

    if ext in _BINARY_EXTS:
        console.print(f"[yellow]Binary file — cannot read contents.[/]")
        return

    # Read content (up to 8000 chars)
    try:
        content = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        console.print(f"[red]Cannot read file: {e}[/]")
        return

    if ext in _CODE_EXTS:
        menu = (
            f"[bold {TC}]What would you like to do?[/]\n"
            f"  [bold]f[/] — fix all errors\n"
            f"  [bold]r[/] — review (bugs, security, style)\n"
            f"  [bold]e[/] — explain this code\n"
            f"  [bold]i[/] — improve / add features\n"
            f"  [bold]v[/] — view with syntax highlight\n"
            f"  [bold]n[/] — cancel\n"
        )
        console.print(Panel(menu, border_style=TC))
        choice = console.input(f"[bold {TC}]Choice:[/] ").strip().lower()

        ctx = f"FILE: {p}\n\n```{ext.lstrip('.')}\n{content[:7000]}\n```"

        if choice == "f":
            with console.status(f"[{TC}]Fixing {p.name}...[/]", spinner="dots"):
                ans = ask(
                    f"Fix ALL errors, bugs, and issues in this file. "
                    f"Return the COMPLETE fixed file using ### FILE: {p.name} format.",
                    ctx
                )
            _print(ans)
            saved = _auto_save_files(ans)
            if saved:
                console.print(f"[{TC}]Fixed file saved: {saved[0]}[/]")
            else:
                # Save directly if AI returned a single code block
                m = re.search(r"```[^\n]*\n([\s\S]+?)```", ans)
                if m:
                    p.write_text(m.group(1), encoding="utf-8")
                    console.print(f"[{TC}]Fixed and saved: {p}[/]")

        elif choice == "r":
            with console.status(f"[{TC}]Reviewing {p.name}...[/]", spinner="dots"):
                ans = ask("Do a thorough code review. Check for bugs, security issues, "
                          "performance problems, and style issues. Be specific.", ctx)
            _print(ans)

        elif choice == "e":
            with console.status(f"[{TC}]Explaining {p.name}...[/]", spinner="dots"):
                ans = ask("Explain this code in detail. What does it do? How does it work? "
                          "What are the key parts?", ctx)
            _print(ans)

        elif choice == "i":
            what = console.input(f"[bold {TC}]What features to add or improve?[/] ").strip()
            with console.status(f"[{TC}]Improving {p.name}...[/]", spinner="dots"):
                ans = ask(
                    f"Improve this file: {what}. Return the COMPLETE improved file "
                    f"using ### FILE: {p.name} format.",
                    ctx
                )
            _print(ans)
            saved = _auto_save_files(ans)
            if saved:
                console.print(f"[{TC}]Improved file saved: {saved[0]}[/]")

        elif choice == "v":
            do_read(str(p))

    elif ext in _TEXT_EXTS:
        menu = (
            f"[bold {TC}]What would you like to do?[/]\n"
            f"  [bold]v[/] — view file\n"
            f"  [bold]s[/] — summarise\n"
            f"  [bold]a[/] — ask AI anything about it\n"
            f"  [bold]n[/] — cancel\n"
        )
        console.print(Panel(menu, border_style=TC))
        choice = console.input(f"[bold {TC}]Choice:[/] ").strip().lower()
        ctx = f"FILE: {p}\n\nCONTENT:\n{content[:7000]}"

        if choice == "v":
            do_read(str(p))
        elif choice == "s":
            with console.status(f"[{TC}]Summarising...[/]", spinner="dots"):
                ans = ask("Summarise the key points of this file concisely.", ctx)
            _print(ans)
        elif choice == "a":
            question = console.input(f"[bold {TC}]Ask anything about this file:[/] ").strip()
            with console.status(f"[{TC}]Thinking...[/]", spinner="dots"):
                ans = ask(question, ctx)
            _print(ans)
    else:
        do_read(str(p))

# ── Auto-install / auto-save / auto-run ───────────────────────────────────────
def _auto_install(text):
    matches = re.findall(r"###\s*INSTALL:\s*\n```[^\n]*\n([\s\S]+?)```", text, re.IGNORECASE)
    for block in matches:
        pkgs = [p.strip() for p in block.splitlines()
                if p.strip() and not p.strip().startswith("#")]
        for pkg in pkgs:
            console.print(f"[{TC}]Installing {pkg}...[/]")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                capture_output=True, text=True
            )
            icon = "✓" if result.returncode == 0 else "✗"
            console.print(f"[{TC}]  {icon} {pkg}[/]")

def _auto_save_files(text):
    saved = []

    # Pattern 1 — ### FILE: filename (primary)
    matches = re.findall(
        r"###\s*FILE:\s*([^\n]+)\n```[^\n]*\n([\s\S]+?)```",
        text, re.IGNORECASE
    )
    # Pattern 2 — **filename.ext** or `filename.ext` before code block
    if not matches:
        matches = re.findall(
            r"(?:\*\*|`)([a-zA-Z0-9_./ \-]+\.[a-zA-Z0-9]{1,6})(?:\*\*|`)\s*\n```[^\n]*\n([\s\S]+?)```",
            text, re.IGNORECASE
        )
    # Pattern 3 — ## filename.ext (markdown heading)
    if not matches:
        matches = re.findall(
            r"#{1,4}\s+([a-zA-Z0-9_./ \-]+\.[a-zA-Z0-9]{1,6})\s*\n```[^\n]*\n([\s\S]+?)```",
            text, re.IGNORECASE
        )
    # Pattern 4 — "File: filename.ext" plain label
    if not matches:
        matches = re.findall(
            r"(?:File|Filename|Create|Save as):\s*[`\"']?([a-zA-Z0-9_./ \-]+\.[a-zA-Z0-9]{1,6})[`\"']?\s*\n```[^\n]*\n([\s\S]+?)```",
            text, re.IGNORECASE
        )

    if not matches:
        return saved

    console.print(f"\n[bold {TC}]Writing {len(matches)} file(s)...[/]")
    for fname, content in matches:
        fname     = fname.strip().strip("`*\"' ")
        save_path = _cwd / fname
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(content, encoding="utf-8")
        console.print(f"[{TC}]  ✓ {save_path}[/]")
        saved.append(save_path)
    return saved

def _syntax_check_and_fix(saved):
    """Run py_compile on every saved .py file. Auto-fix any that fail."""
    for path in saved:
        if not str(path).endswith(".py"):
            continue
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            error_msg = (result.stderr or result.stdout).strip()
            console.print(f"[yellow]Syntax error in {path.name} — auto-fixing...[/]")
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                ctx = (
                    f"FILE: {path}\n\nERROR:\n{error_msg}\n\n"
                    f"CONTENT:\n```python\n{content[:8000]}\n```\n\n"
                    "Fix ALL syntax errors. Return the COMPLETE fixed file using "
                    f"### FILE: {path.name} format."
                )
                with console.status(f"[{TC}]Fixing {path.name}...[/]", spinner="dots"):
                    fix_ans = ask("Fix the syntax error in this file.", ctx)
                fixed_saved = _auto_save_files(fix_ans)
                if fixed_saved:
                    console.print(f"[{TC}]  ✓ Fixed {path.name}[/]")
            except Exception as e:
                console.print(f"[red]Could not auto-fix {path.name}: {e}[/]")

def _fix_relative_imports(saved):
    """Convert 'from .module import x' → 'from module import x' in all saved .py files.
    The AI often generates relative imports which crash when run as plain scripts."""
    for path in saved:
        if not str(path).endswith(".py"):
            continue
        try:
            original = path.read_text(encoding="utf-8", errors="replace")
            # Replace 'from .foo import' with 'from foo import'
            fixed = re.sub(r'^from \.([\w]+) import', r'from \1 import',
                           original, flags=re.MULTILINE)
            # Replace 'import .foo' with 'import foo' (rare but possible)
            fixed = re.sub(r'^import \.([\w]+)', r'import \1',
                           fixed, flags=re.MULTILINE)
            if fixed != original:
                path.write_text(fixed, encoding="utf-8")
                console.print(f"[dim {TC}]  fixed relative imports in {path.name}[/]")
        except Exception:
            pass

def _extract_app_name(text, fallback=""):
    m = re.search(r"###\s*APP_NAME:\s*(.+)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return fallback or "Unnamed Program"

def _detect_web_port(run_cmd_str):
    """Return the localhost port if this looks like a web server command."""
    cmd = run_cmd_str.lower()
    # Common web frameworks
    if "flask" in cmd or "app.run" in cmd:
        m = re.search(r"port[=\s]+(\d+)", cmd)
        return int(m.group(1)) if m else 5000
    if "fastapi" in cmd or "uvicorn" in cmd:
        m = re.search(r"--port\s+(\d+)", cmd)
        return int(m.group(1)) if m else 8000
    if "streamlit" in cmd:
        return 8501
    if "django" in cmd or "manage.py" in cmd:
        return 8000
    return None

def _auto_run(text, saved):
    import ctypes, webbrowser, time

    run_cwd = str(_cwd)
    run_cmd_str = None

    match = re.search(r"###\s*RUN:\s*(.+)", text, re.IGNORECASE)
    if match:
        run_cmd_str = match.group(1).strip()
    elif saved:
        py_files = [p for p in saved if str(p).endswith(".py")]
        if py_files:
            run_cmd_str = f'python "{py_files[0]}"'

    if not run_cmd_str:
        console.print(f"[yellow]No run command found — files saved but not launched.[/]")
        return

    # Detect if it's a web app and get port
    web_port = _detect_web_port(run_cmd_str)

    # Also scan the saved files for web server patterns if cmd didn't reveal it
    if not web_port and saved:
        for p in saved:
            if not str(p).endswith(".py"):
                continue
            try:
                src = p.read_text(encoding="utf-8", errors="replace")
                if "app.run(" in src or "flask" in src.lower():
                    web_port = 5000; break
                if "uvicorn" in src or "fastapi" in src.lower():
                    web_port = 8000; break
                if "streamlit" in src.lower():
                    web_port = 8501; break
            except Exception:
                pass

    # Write bat wrapper — keeps CMD window open even if app crashes
    bat_path = Path(run_cwd) / "_titan_run.bat"
    bat_path.write_text(
        "@echo off\n"
        f'cd /d "{run_cwd}"\n'
        "title Titan Code — App Running\n"
        "echo.\n"
        f"echo  Titan Code is launching: {run_cmd_str}\n"
        "echo.\n"
        f"{run_cmd_str}\n"
        "echo.\n"
        "echo  App finished. Press any key to close this window.\n"
        "pause > nul\n",
        encoding="utf-8"
    )

    console.print(f"\n[bold {TC}]Launching your app...[/]")

    opened = False

    # Method 1: ShellExecuteW — opens with full focus in a new window
    try:
        SW_SHOWNORMAL = 1
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "open", "cmd.exe", f'/k "{bat_path}"', run_cwd, SW_SHOWNORMAL
        )
        if int(ret) > 32:
            opened = True
    except Exception:
        pass

    # Method 2: CREATE_NEW_CONSOLE
    if not opened:
        try:
            subprocess.Popen(
                ["cmd", "/k", str(bat_path)],
                cwd=run_cwd,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            opened = True
        except Exception:
            pass

    # Method 3: os.system start
    if not opened:
        try:
            os.system(f'start "Titan Code" cmd /k "{bat_path}"')
            opened = True
        except Exception:
            pass

    if not opened:
        console.print(Panel(
            f"[yellow]Could not auto-open. Run it yourself:[/]\n\n"
            f"  [bold {TC}]{run_cmd_str}[/]",
            title="Run Manually", border_style="yellow"
        ))
        return

    # For web apps — open browser after a 3-second delay (server needs time to start)
    if web_port:
        url = f"http://localhost:{web_port}"
        console.print(f"[{TC}]Web app detected — opening browser at {url} in 3 seconds...[/]")
        def _open_browser():
            time.sleep(3)
            webbrowser.open(url)
        import threading
        threading.Thread(target=_open_browser, daemon=True).start()

def _force_format_retry(question, _bad_ans):
    return ask(
        "Your previous response did not use the required ### FILE: format. "
        "Rewrite your complete response now using EXACTLY:\n\n"
        "### APP_NAME: <name>\n"
        "### FILE: <filename>\n"
        "```language\n...complete code...\n```\n\n"
        "### INSTALL:\n```\npackage\n```\n\n"
        "### RUN: python filename.py\n\n"
        f"Original request: {question}"
    )

# ── Core build function ───────────────────────────────────────────────────────
def _build(question):
    with console.status(f"[{TC}]Building...[/]", spinner="dots"):
        ans = ask(question)

    # If AI asked a clarifying question instead of building, force it to build now
    if _is_clarifying_question(ans):
        with console.status(f"[{TC}]Building...[/]", spinner="dots"):
            ans = ask(
                f"{question}\n\nDo NOT ask any questions. Make your best assumptions "
                f"and output the complete code right now."
            )

    _print(ans)

    _auto_install(ans)
    saved = _auto_save_files(ans)

    # Retry if no files found
    if not saved:
        with console.status(f"[{TC}]Retrying...[/]", spinner="dots"):
            ans2 = _force_format_retry(question, ans)
        _print(ans2)
        _auto_install(ans2)
        saved = _auto_save_files(ans2)
        if saved:
            ans = ans2

    if saved:
        _fix_relative_imports(saved)
        _syntax_check_and_fix(saved)
        app_name = _extract_app_name(ans, fallback=question[:50])
        _save_program(app_name, question[:100], saved)
        _auto_run(ans, saved)
        console.print(f"\n[bold {TC}]Done building.[/]")
    else:
        console.print(Panel(
            "[yellow]Could not generate files.[/]\n"
            "Try being more specific:\n"
            '  "build me a snake game with pygame"\n'
            '  "create a calculator app with tkinter"\n'
            '  "make me a chatbot with groq"',
            title="Build Failed — Be More Specific",
            border_style="yellow"
        ))

def do_fix_app(name):
    """Find an app by name in the registry, read all its files, deep-fix every error."""
    prog = _find_program(name)
    if not prog:
        console.print(f"[yellow]'{name}' not found in your built programs.[/]")
        console.print(f"[dim]Use /programs to see all your built apps.[/]")
        return

    files = prog.get("files", [])
    existing = [f for f in files if Path(f).exists()]

    if not existing:
        console.print(f"[yellow]No files found for '{prog['name']}'. They may have been moved.[/]")
        return

    console.print(f"\n[bold {TC}]Found: {prog['name']}[/]  [dim]({len(existing)} file(s))[/]")

    # Read all file contents
    file_contents = {}
    for fp in existing:
        try:
            file_contents[fp] = Path(fp).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            console.print(f"[red]Cannot read {Path(fp).name}: {e}[/]")

    # Collect syntax errors from all .py files
    error_report = []
    for fp in existing:
        if not fp.endswith(".py"):
            continue
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", fp],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            error_report.append(f"{Path(fp).name}:\n{(result.stderr or result.stdout).strip()}")

    # Build full context: errors + all file contents
    ctx_parts = [f"APP: {prog['name']}\nDescription: {prog.get('description', '')}\n"]

    if error_report:
        ctx_parts.append("SYNTAX ERRORS DETECTED:\n" + "\n\n".join(error_report) + "\n")
    else:
        ctx_parts.append("No syntax errors detected — do a deep logic/runtime analysis.\n")

    ctx_parts.append("ALL FILES (read every line carefully):\n")
    for fp, content in file_contents.items():
        lang = Path(fp).suffix.lstrip(".") or "text"
        ctx_parts.append(f"### FILE: {Path(fp).name}\n```{lang}\n{content[:7000]}\n```\n")

    ctx = "\n".join(ctx_parts)

    console.print(f"[{TC}]Deep analyzing all files...[/]")
    with console.status(f"[{TC}]Fixing {prog['name']}...[/]", spinner="dots"):
        ans = ask(
            f"Deep-analyze the complete app '{prog['name']}' above. "
            f"Find and fix EVERY error — syntax errors, import errors, undefined variables, "
            f"broken references between files, logic errors, runtime crashes. "
            f"Return ALL files completely rewritten and fixed using ### FILE: format. "
            f"Every single file must be included and must be 100% working.",
            ctx
        )

    _print(ans)
    saved = _auto_save_files(ans)

    if saved:
        _fix_relative_imports(saved)
        _syntax_check_and_fix(saved)
        console.print(f"\n[bold {TC}]Done fixing {prog['name']}.[/]")
    else:
        console.print(f"[yellow]Could not auto-save fixes. Check the response above.[/]")


def do_build_ai(what):
    _build(f"Build a complete working AI application: {what}.")

def do_create(what):
    _build(f"Create this complete project from scratch: {what}.")

# ── Help ───────────────────────────────────────────────────────────────────────
def do_help():
    t = Table(title="TITAN CODE v3.0 Commands", border_style=TC,
              show_lines=True, box=rbox.ROUNDED)
    t.add_column("Command",     style=f"bold {TC}", no_wrap=True)
    t.add_column("Description", style="white")
    rows = [
        ("/ram",               "RAM usage"),
        ("/cpu",               "CPU info"),
        ("/disk [drive]",      "Disk usage (default C:)"),
        ("/battery",           "Battery status"),
        ("/system",            "Full system info"),
        ("/processes",         "Top 20 running processes"),
        ("/fullscan",          "Complete system + packages scan"),
        ("/files [path]",      "List directory contents"),
        ("/read <file>",       "Read file with syntax highlight"),
        ("/run <cmd>",         "Run any shell command"),
        ("/programs",          "List ALL programs you've built"),
        ("/open <name>",       "Find and open a previous program"),
        ("/fix <file>",        "AI fixes all errors in a file"),
        ("/create <what>",     "Create a complete project from scratch"),
        ("/build-ai <what>",   "Build a complete AI / ML app"),
        ("/review [file]",     "Code review a file or git diff"),
        ("/test [file]",       "Run tests and auto-fix failures"),
        ("/plan <task>",       "Plan only — blueprint before code"),
        ("/diff",              "Show git diff"),
        ("/git <request>",     "Natural language git commands"),
        ("/init",              "Create TITANCODE.md for this project"),
        ("/compact",           "Compress context window"),
        ("/rewind [n]",        "Time-travel to checkpoint n"),
        ("/fork",              "Save a safe experiment checkpoint"),
        ("/cost",              "Session stats"),
        ("/cd <path>",         "Change working directory"),
        ("/clear",             "Clear screen"),
        ("/reset",             "Reset conversation history"),
        ("/exit",              "Exit Titan Code"),
        ("build me a ...",     "Starts build flow with preview + confirm"),
        ("open <name>",        "Find and open a previous program"),
        ("drag / paste path",  "Drop any file — fix, review, explain, improve"),
        ("fix <filepath>",     "AI fixes all errors in that file"),
        ("anything else",      "AI answers or builds — just ask"),
    ]
    for cmd, desc in rows:
        t.add_row(cmd, desc)
    console.print(t)

# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    global _cwd
    show_welcome()

    if not API_KEY:
        console.print(Panel(
            "[bold red]No Groq API key found.[/]\n"
            "Open Titan Ultra, enter your API key in the sidebar, then relaunch.",
            border_style="red", title="ERROR"
        ))
        input("Press Enter to exit...")
        return

    while True:
        try:
            user_input = console.input(f"[bold {TC}]> [/]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[{TC}]Goodbye, {USER}![/]")
            break

        if not user_input:
            continue

        # Echo the question back so it's always visible in the terminal
        console.print(f"[bold white]You:[/] {user_input}")
        console.print()

        parts = user_input.split(maxsplit=1)
        cmd   = parts[0].lower()
        arg   = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("/exit", "/quit", "/q"):
            console.print(f"[{TC}]Goodbye, {USER}![/]")
            break
        elif cmd == "/help":       do_help()
        elif cmd == "/ram":        do_ram()
        elif cmd == "/cpu":        do_cpu()
        elif cmd == "/disk":       do_disk(arg)
        elif cmd == "/battery":    do_battery()
        elif cmd == "/system":     do_system()
        elif cmd == "/fullscan":   do_fullscan()
        elif cmd == "/processes":  do_processes()
        elif cmd == "/files":      do_files(arg)
        elif cmd == "/read":
            if arg: do_read(arg)
            else:   console.print("[yellow]/read <filepath>[/]")
        elif cmd == "/run":
            if arg: do_run(arg)
            else:   console.print("[yellow]/run <command>[/]")
        elif cmd == "/fix":
            if arg: do_fix(arg)
            else:   console.print("[yellow]/fix <filepath>[/]")
        elif cmd == "/init":       do_init()
        elif cmd == "/diff":       do_diff()
        elif cmd == "/plan":
            if arg: do_plan(arg)
            else:   console.print("[yellow]/plan <task>[/]")
        elif cmd == "/compact":    do_compact()
        elif cmd == "/rewind":     do_rewind(arg)
        elif cmd == "/fork":       do_fork()
        elif cmd == "/cost":       do_cost()
        elif cmd == "/git":        do_git(arg)
        elif cmd == "/test":       do_test(arg)
        elif cmd == "/review":     do_review(arg)
        elif cmd == "/programs":   do_programs()
        elif cmd in ("/fix-app", "/fixapp"):
            if arg: do_fix_app(arg)
            else:   console.print("[yellow]/fix-app <app name>[/]")
        elif cmd == "/open":
            if arg: do_open(arg)
            else:   do_programs()
        elif cmd in ("/build-ai", "/buildai"):
            if arg: do_build_ai(arg)
            else:   console.print("[yellow]/build-ai <description>[/]")
        elif cmd == "/create":
            if arg: do_create(arg)
            else:   console.print("[yellow]/create <description>[/]")
        elif cmd == "/cd":
            new = (_cwd / arg).resolve() if arg else Path.home()
            if new.is_dir():
                _cwd = new
                console.print(f"[{TC}]{_cwd}[/]")
            else:
                console.print(f"[red]Not a directory: {arg}[/]")
        elif cmd == "/clear":      show_welcome()
        elif cmd == "/reset":
            _history.clear()
            console.print(f"[{TC}]History reset.[/]")
        else:
            _low = user_input.lower()

            # ── Drag-and-drop: detect if user pasted/dragged a file path ─────
            if _is_file_drop(user_input):
                do_dropped_file(user_input)
                continue

            # ── Fix any file path mentioned with "fix" keyword ────────────────
            _fix_m = re.match(
                r"fix\s+[\"']?([A-Za-z]:\\[^\s\"']+|[\w.\-/\\]+\.[a-zA-Z0-9]{1,6})[\"']?",
                user_input, re.IGNORECASE
            )
            if _fix_m:
                do_fix(_fix_m.group(1))
                continue

            # ── Fix app by name ("fix calculator", "can u fix my snake game") ──
            _fix_app_m = re.match(
                r"^(?:can\s+(?:you|u|ya)\s+)?(?:please\s+)?fix\s+(?:my\s+|the\s+)?(.+?)(?:\s+(?:app|game|program|project|code|please|for me))*\s*$",
                user_input, re.IGNORECASE
            )
            if _fix_app_m:
                _app_name_candidate = _fix_app_m.group(1).strip()
                if _find_program(_app_name_candidate):
                    do_fix_app(_app_name_candidate)
                    continue

            # ── "there's an error in X" / "X is not working" ─────────────────
            _err_m = re.search(
                r"(?:error\s+in|bug\s+in|problem\s+with|issue\s+with|not\s+working[:\s]+|broken[:\s]+|crashes?[:\s]+)\s*[\"']?([a-zA-Z0-9 _\-]+)[\"']?",
                user_input, re.IGNORECASE
            )
            if _err_m:
                _app_name_candidate = _err_m.group(1).strip()
                if _find_program(_app_name_candidate):
                    do_fix_app(_app_name_candidate)
                    continue

            if any(k in _low for k in ("how much ram","check ram","my ram","ram usage",
                                        "memory usage","how much memory","check memory")):
                do_ram()

            elif any(k in _low for k in ("how much cpu","check cpu","cpu usage",
                                          "processor usage","my cpu","my processor")):
                do_cpu()

            elif any(k in _low for k in ("disk space","storage space","how much space",
                                          "check disk","my storage","free space","disk usage")):
                do_disk()

            elif any(k in _low for k in ("battery","how much battery","check battery")):
                do_battery()

            elif any(k in _low for k in ("scan my","full scan","everything about my",
                                          "check everything","scan everything",
                                          "entire system","check my entire","full system")):
                do_fullscan()

            elif any(k in _low for k in ("system info","my pc","check my pc","pc specs",
                                          "computer info","check my computer","my laptop")):
                do_system()

            elif any(k in _low for k in ("running processes","what is running","my processes",
                                          "check processes","running apps")):
                do_processes()

            elif any(k in _low for k in ("show my files","list my files","check my files",
                                          "what files","show files","list files",
                                          "files in","what's in","whats in","check files",
                                          "show me files","check folder")):
                m = re.search(r"(?:in|inside|of|folder)\s+([A-Za-z]:\\[^\s]+|[^\s]+)", _low)
                do_files(m.group(1) if m else "")

            elif any(k in _low for k in ("what have you built","show programs","my programs",
                                          "list programs","what programs","what apps",
                                          "what did you build","what have i built",
                                          "programs you made","apps you built")):
                do_programs()

            elif any(k in _low for k in ("open my","open the","find my","find the",
                                          "where is my","run my","launch my","start my",
                                          "how do i open","how to open","how can i open",
                                          "how do i run","how to run","how to launch",
                                          "how do i launch","how can i run","how can i launch",
                                          "how do i start","how to start")):
                name = re.sub(
                    r"^(?:how\s+(?:do\s+i|to|can\s+i)\s+)?(?:open|find|where\s+is|run|launch|start)\s+(?:my|the|me|it)?\s*",
                    "", user_input, flags=re.IGNORECASE
                ).strip()
                if name:
                    do_open(name)
                else:
                    # "how do i open it" with no name — open most recent program
                    programs = _load_programs()
                    if programs:
                        do_open(programs[-1]["name"])
                    else:
                        do_programs()

            elif re.match(r"^(?:open|launch|run|start)\s+\S", _low):
                name = re.sub(
                    r"^(?:open|launch|run|start)\s+",
                    "", user_input, flags=re.IGNORECASE
                ).strip()
                if _find_program(name):
                    do_open(name)
                else:
                    _build(user_input)

            elif any(k in _low for k in ("build me","create me","make me","build a","create a",
                                          "make a","i want a","give me a","write me",
                                          "create an","build an","make an")):
                _build(user_input)

            else:
                _build(user_input)

if __name__ == "__main__":
    main()
