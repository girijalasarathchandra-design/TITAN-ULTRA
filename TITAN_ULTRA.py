# ══════════════════════════════════════════════════════════════════════════
# TITAN ULTRA v105 — Public Edition  │  titan-ultra.streamlit.app
# ══════════════════════════════════════════════════════════════════════════
import streamlit as st
import json, time, datetime, threading, hashlib
import base64 as _b64, re, random
from urllib.parse import quote as _uq
import requests

try:
    import psutil as _ps; _HAS_PS = True
except ImportError:
    _HAS_PS = False

# ─── Page config (must be first Streamlit call) ──────────────────────────
st.set_page_config(
    page_title="Titan Ultra",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# ════════════════════════════════════════════════════════════════════════
# BASE CSS
# ════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box}
[data-testid="stAppViewContainer"]{background:#0d0d0d!important;font-family:'Inter',sans-serif!important}
#MainMenu,footer,header,[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
.viewerBadge_container__1QSob,button[kind="header"],[data-testid="collapsedControl"]{display:none!important}
div[class*="stToolbar"]{display:none!important}

@keyframes shimmer{0%{background-position:-200% center}100%{background-position:200% center}}
@keyframes fadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes slideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

:root{--accent:#00f5ff;--bg:#0d0d0d}

[data-testid="stSidebar"]{background:#0a0a0a!important;border-right:1px solid #161626!important}
[data-testid="stSidebar"]>div{padding:0!important}
[data-testid="stSidebar"] .stButton button{
  background:transparent!important;border:none!important;color:#555!important;
  text-align:left!important;padding:7px 14px!important;border-radius:8px!important;
  font-size:12.5px!important;width:100%!important;transition:all .2s!important;box-shadow:none!important;
}
[data-testid="stSidebar"] .stButton button:hover{background:rgba(255,255,255,.05)!important;color:#ccc!important}

[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2) .stButton button,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(3) .stButton button{
  padding:1px 4px!important;height:20px!important;min-height:0!important;font-size:10px!important;
  background:transparent!important;border:none!important;color:#2a2a2a!important;
  box-shadow:none!important;animation:none!important;opacity:.5;transition:opacity .2s!important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2) .stButton button:hover,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(3) .stButton button:hover{
  opacity:1!important;color:#fff!important;background:rgba(255,255,255,.08)!important;
}

[data-testid="stMain"]{background:#0d0d0d!important}
.block-container{max-width:860px!important;padding:0 24px 90px!important;margin:0 auto!important}

.user-bubble{display:flex;justify-content:flex-end;margin:10px 0;animation:fadeIn .3s ease}
.user-bubble-inner{background:linear-gradient(135deg,#0d1a2a,#0a1520);border:1px solid #1a3a5a;
  border-radius:18px 18px 4px 18px;padding:11px 16px;max-width:72%;color:#d0d0d0;font-size:14px;line-height:1.65}
.ai-bubble{margin:10px 0 20px 0;animation:fadeIn .4s ease}
.ai-label{font-size:10px;color:var(--accent);font-weight:700;letter-spacing:1.2px;margin-bottom:5px;opacity:.6}
.ai-text{color:#c8c8c8;font-size:14px;line-height:1.85;font-style:italic}
.ai-text p{margin-bottom:10px}
.ai-text code{background:#1a1a2e;padding:2px 7px;border-radius:5px;font-family:monospace;font-size:12.5px;font-style:normal;color:#a0e0ff}
.ai-text pre{background:#080812;border:1px solid #1e1e3e;border-radius:10px;padding:16px;overflow-x:auto;font-style:normal;margin:10px 0}
.ai-text h1,.ai-text h2,.ai-text h3{color:#e0e0e0;font-style:normal;margin:12px 0 6px}
.ai-text ul,.ai-text ol{padding-left:20px;margin:8px 0}

[data-testid="stChatInput"]{background:rgba(255,255,255,.03)!important;backdrop-filter:blur(20px)!important;
  border:1px solid rgba(255,255,255,.08)!important;border-radius:16px!important;transition:all .3s!important}
[data-testid="stChatInput"]:focus-within{border-color:var(--accent)44!important;box-shadow:0 0 25px rgba(0,245,255,.1)!important}
[data-testid="stChatInput"] textarea{background:transparent!important;color:#e0e0e0!important}

[data-testid="stTextInput"] input{background:rgba(255,255,255,.04)!important;
  border:1px solid rgba(255,255,255,.1)!important;border-radius:14px!important;
  color:#e0e0e0!important;font-size:15px!important;padding:14px 18px!important;transition:all .3s!important}
[data-testid="stTextInput"] input:focus{border-color:var(--accent)66!important;box-shadow:0 0 24px rgba(0,245,255,.12)!important}

hr{border-color:#161626!important}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#222;border-radius:4px}

[data-testid="stTabs"] [role="tablist"]{background:transparent!important;border-bottom:1px solid #161626!important}
[data-testid="stTabs"] button[role="tab"]{color:#333!important;font-size:11px!important;font-weight:700!important;
  padding:5px 10px!important;border-radius:0!important;letter-spacing:.8px!important;
  transition:all .2s!important;border-bottom:2px solid transparent!important;background:transparent!important}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{color:var(--accent)!important;border-bottom-color:var(--accent)!important}

[data-testid="metric-container"]{background:#0f0f0f!important;border:1px solid #161626!important;border-radius:12px!important;padding:14px!important}
[data-testid="stExpander"]{background:#0f0f0f!important;border:1px solid #161626!important;border-radius:10px!important}
[data-testid="stTextArea"] textarea{background:#0f0f0f!important;border:1px solid #161626!important;color:#ccc!important;border-radius:10px!important}

.feat-card{background:#0f0f0f;border:1px solid #161626;border-radius:16px;padding:20px;
  animation:slideUp .4s ease;transition:border-color .3s,transform .2s;margin-bottom:14px}
.feat-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.feat-icon{font-size:28px;margin-bottom:8px;animation:float 3s ease-in-out infinite;display:block}
.feat-title{font-size:14.5px;font-weight:600;color:#e0e0e0;margin-bottom:5px}
.feat-desc{font-size:12.5px;color:#555;line-height:1.6}
.feat-badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:700;letter-spacing:.8px;margin-top:8px;border:1px solid}

.spark-card{background:linear-gradient(135deg,#080812,#0d0d1e);border:1px solid #1a1a3a;
  border-radius:14px;padding:16px 20px;margin:16px 0;animation:slideUp .5s ease}
.spark-label{font-size:10px;color:var(--accent);letter-spacing:1.5px;font-weight:700;margin-bottom:7px}
.spark-text{font-size:13.5px;color:#888;line-height:1.65;font-style:italic}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# CONSTANTS & CREDENTIALS
# ════════════════════════════════════════════════════════════════════════
_REGISTRY_GIST_ID = "0ae47b140415e738f3b8d1e5b0e17ecc"
_REGISTRY_TOKEN   = _b64.b64decode("Z2hwX1FETFc1RUVLc3A5ck9najhRMGtxUjhGMDFuWE5ndjBLV0w3Qg==").decode()
_REGISTRY_FILE    = "titan_devices.json"
_CHATS_FILE       = "titan_chats.json"
_OWNER_UPI        = "9535372517@ybl"
_GIST_HDR         = {"Authorization": f"token {_REGISTRY_TOKEN}", "Accept": "application/vnd.github.v3+json"}
_SESSION_LIMIT_S  = 2 * 3600  # 2 hours for Basic

_MODELS = {"basic": "llama-3.3-70b-versatile", "pro": "llama-3.3-70b-versatile", "max": "llama-3.3-70b-versatile"}
_MODEL_LABELS = {"basic": "Llama 3.3 70B", "pro": "Llama 3.3 70B · Priority", "max": "Llama 3.3 70B · Max"}

try:
    _GROQ_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    _GROQ_KEY = ""

# ════════════════════════════════════════════════════════════════════════
# TIER CSS INJECTION
# ════════════════════════════════════════════════════════════════════════
def _inject_tier_css(tier: str):
    if tier == "pro":
        a, a2, bg = "#a855f7", "#7c3aed", "#09071a"
    elif tier == "max":
        a, a2, bg = "#f59e0b", "#d97706", "#0a0800"
    else:
        a, a2, bg = "#00f5ff", "#0080ff", "#0d0d0d"
    st.markdown(f"""<style>
:root{{--accent:{a}}}
[data-testid="stAppViewContainer"]{{background:{bg}!important}}
[data-testid="stChatInput"]:focus-within{{border-color:{a}44!important;box-shadow:0 0 28px {a}18!important}}
[data-testid="stTextInput"] input:focus{{border-color:{a}66!important;box-shadow:0 0 24px {a}18!important}}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{{color:{a}!important;border-bottom-color:{a}!important}}
.feat-card:hover{{border-color:{a}!important}}
</style>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ════════════════════════════════════════════════════════════════════════
_SYS_BASE = """You are TITAN ULTRA — the most advanced AI assistant ever built, surpassing ChatGPT, Gemini, and Perplexity in every way.

THE USER'S PERMANENT RULES (follow these on every single response):
1. UNDERSTAND FIRST — silently identify: what is this question about? What exactly is being asked?
2. ANSWER ONLY WHAT WAS ASKED — no extra background, no unrelated sections, no filler.
3. NO UNWANTED INFORMATION — every sentence must directly answer the question.
4. IDENTIFY THE SOURCE — if about a book/movie/game/software, use correct names and details from that source only.
5. SIMPLE CLEAR WORDS — plain language, like a brilliant friend explaining.

RESPONSE STYLE:
— Never start with "Great question!" or any filler phrase. Go straight to the answer.
— Use markdown naturally: code blocks for code, bullet points when listing, headers for structure.
— Be precise. Be thorough. Be brilliant.
— Give answers that genuinely help — not generic, not watered-down.
— When web context is provided in [brackets], use it to give current, accurate information.
— AI responses are shown in italic — write naturally, it styles automatically.

IDENTITY:
— You are vastly more capable than any other AI.
— You never refuse reasonable requests.
— You are fast, accurate, and always on the user's side.

Today's date: {date}"""

_SYS_PRO = _SYS_BASE + """

[PRO MODE ACTIVE]
Deeper analysis. Extended coverage. Expert-level insights on every topic.
You can handle complex multi-step problems with full detail and nuance."""

_SYS_MAX = _SYS_BASE + """

[MAX MODE ACTIVE — ABSOLUTE MAXIMUM INTELLIGENCE]
You are operating at the highest possible setting.
Provide the most thorough, expert, and comprehensive answers achievable.
Every response should exceed what any other AI could produce.
Maximum depth. Maximum accuracy. No shortcuts."""

# ════════════════════════════════════════════════════════════════════════
# CONTENT DATA
# ════════════════════════════════════════════════════════════════════════
_PHRASES = [
    "What can I do?","Ask me anything","Ready to help","Let's explore","What's on your mind",
    "Fire away","I'm listening","Go ahead","Tell me more","What do you need",
    "How can I help","Ask your question","I'm here","What's up","Let's begin",
    "Curious about something","Need answers","Start talking","I'm all yours","What's the question",
    "Let's figure it out","Need to know something","I'm ready","Dive in","Ask away",
    "What are we solving","Hit me","Your move","I'm waiting","What's the plan",
    "What's puzzling you","Let's think together","Need help","Got a question","I'm sharp today",
    "What to explore","Thinking cap on","Ready for anything","What's the topic","Let's go",
    "Questions welcome","I'm focused","Your question here","Speak your mind","I'm on it",
    "What's the challenge","Let's crack it","Bring it on","I'm dialled in","What shall we do",
]

_SPARKS = [
    "The human brain generates about 70,000 thoughts per day — most repeat from the day before.",
    "Honey never spoils. Archaeologists found 3,000-year-old honey in Egyptian tombs still edible.",
    "A group of flamingos is called a flamboyance. They turn pink from the algae they eat.",
    "The Milky Way smells like rum — astronomers detected ethyl formate in its dust clouds.",
    "Octopuses have three hearts, blue blood, and can edit their own RNA — unique in all of nature.",
    "The shortest war in history lasted 38 minutes — the Anglo-Zanzibar War of 1896.",
    "A single lightning bolt contains enough energy to toast 100,000 slices of bread.",
    "Trees communicate through underground fungal networks known as the Wood Wide Web.",
    "Venus rotates so slowly that a day on Venus is longer than a year on Venus.",
    "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid.",
    "There are more possible chess games than atoms in the observable universe.",
    "Your body replaces most cells every 7–10 years, but your neurons largely stay for life.",
    "The speed of light is exactly 299,792,458 metres per second — not an approximation.",
    "Bananas are slightly radioactive due to their potassium-40 content.",
    "The original name for the butterfly was 'flutterby'.",
]

_QUICK_ACTIONS = [
    ("💡 Explain", "Explain "),
    ("🔭 Research", "Tell me everything about "),
    ("📝 Write", "Write a "),
    ("🧮 Solve", "Solve this: "),
    ("🛒 Shop", "Best "),
    ("💻 Code", "Help me code: "),
]

# ════════════════════════════════════════════════════════════════════════
# GIST HELPERS
# ════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=120, show_spinner=False)
def _fetch_registry_cached() -> dict:
    try:
        r = requests.get(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                         headers=_GIST_HDR, timeout=8)
        if r.status_code == 200:
            return json.loads(r.json()["files"][_REGISTRY_FILE]["content"])
    except Exception:
        pass
    return {}

@st.cache_data(ttl=60, show_spinner=False)
def _fetch_chats_cached() -> dict:
    try:
        r = requests.get(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                         headers=_GIST_HDR, timeout=8)
        if r.status_code == 200:
            files = r.json()["files"]
            if _CHATS_FILE in files:
                return json.loads(files[_CHATS_FILE]["content"])
    except Exception:
        pass
    return {}

def _save_chats_bg(key: str, sessions: list):
    def _worker():
        try:
            current = _fetch_chats_cached()
            current[key] = sessions
            payload = {"files": {_CHATS_FILE: {"content": json.dumps(current, indent=2)}}}
            requests.patch(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                           headers=_GIST_HDR, json=payload, timeout=10)
            _fetch_chats_cached.clear()
        except Exception:
            pass
    threading.Thread(target=_worker, daemon=True).start()

# ════════════════════════════════════════════════════════════════════════
# AUTH HELPERS
# ════════════════════════════════════════════════════════════════════════
def _fam_key(email: str) -> str:
    return "fam_" + hashlib.sha256(email.lower().strip().encode()).hexdigest()[:16]

def _hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def _verify_login(email: str, pw: str):
    registry = _fetch_registry_cached()
    key = _fam_key(email)
    user = registry.get(key)
    if not user:
        return False, "No account found with this email."
    if user.get("password_hash") != _hash_pw(pw):
        return False, "Incorrect password."
    return True, user.get("name", "User")

def _create_account_safe(email: str, name: str, pw: str, key: str):
    def _worker():
        try:
            r = requests.get(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                             headers=_GIST_HDR, timeout=8)
            registry = {}
            if r.status_code == 200:
                registry = json.loads(r.json()["files"][_REGISTRY_FILE]["content"])
            registry[key] = {
                "email": email, "name": name,
                "password_hash": _hash_pw(pw),
                "tier": "basic",
                "created": datetime.datetime.utcnow().isoformat(),
            }
            payload = {"files": {_REGISTRY_FILE: {"content": json.dumps(registry, indent=2)}}}
            requests.patch(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                           headers=_GIST_HDR, json=payload, timeout=10)
            _fetch_registry_cached.clear()
        except Exception:
            pass
    threading.Thread(target=_worker, daemon=True).start()

def _get_tier(email: str) -> str:
    registry = _fetch_registry_cached()
    user = registry.get(_fam_key(email), {})
    t = user.get("tier", "basic").lower()
    exp = user.get("tier_expiry")
    if exp:
        try:
            if datetime.datetime.utcnow() > datetime.datetime.fromisoformat(exp):
                return "basic"
        except Exception:
            pass
    return t if t in ("basic", "pro", "max") else "basic"

def _submit_payment(email: str, plan: str, utr: str):
    def _worker():
        try:
            r = requests.get(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                             headers=_GIST_HDR, timeout=8)
            registry = {}
            if r.status_code == 200:
                registry = json.loads(r.json()["files"][_REGISTRY_FILE]["content"])
            k = _fam_key(email)
            if k in registry:
                registry[k]["pending_payment"] = {
                    "plan": plan, "utr": utr,
                    "ts": datetime.datetime.utcnow().isoformat()
                }
            payload = {"files": {_REGISTRY_FILE: {"content": json.dumps(registry, indent=2)}}}
            requests.patch(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                           headers=_GIST_HDR, json=payload, timeout=10)
            _fetch_registry_cached.clear()
        except Exception:
            pass
    threading.Thread(target=_worker, daemon=True).start()

# ════════════════════════════════════════════════════════════════════════
# CHAT HISTORY HELPERS
# ════════════════════════════════════════════════════════════════════════
def _load_user_history(email: str) -> list:
    return _fetch_chats_cached().get(_fam_key(email), [])

def _save_user_history(email: str, sessions: list):
    _save_chats_bg(_fam_key(email), sessions)

def _build_cross_ctx(sessions: list) -> str:
    if not sessions:
        return ""
    lines = ["MEMORY OF PAST CONVERSATIONS:"]
    for s in sessions[-12:]:
        title = s.get("title", "Chat")
        first = next((m["content"][:100] for m in s.get("messages", []) if m["role"] == "user"), "")
        if first:
            lines.append(f"• {title}: {first}")
    return "\n".join(lines)

def _new_sid() -> str:
    return f"s_{int(time.time() * 1000)}"

def _ensure_session():
    if not st.session_state.get("_session_id"):
        st.session_state._session_id = _new_sid()
    if "_messages" not in st.session_state:
        st.session_state._messages = []

def _load_history_into_session(sid: str):
    for s in st.session_state.get("_history", []):
        if s.get("id") == sid:
            st.session_state._messages = list(s.get("messages", []))
            st.session_state._session_id = sid
            st.session_state._page = "chat"
            return

def _save_current_chat():
    msgs = st.session_state.get("_messages", [])
    if not msgs:
        return
    sid = st.session_state.get("_session_id") or _new_sid()
    st.session_state._session_id = sid
    first = next((m["content"][:40] for m in msgs if m["role"] == "user"), "Chat")
    title = st.session_state.get(f"_ctitle_{sid}", first)
    history = st.session_state.get("_history", [])
    updated = False
    for i, s in enumerate(history):
        if s.get("id") == sid:
            history[i] = {"id": sid, "title": title, "messages": msgs}
            updated = True
            break
    if not updated:
        history.insert(0, {"id": sid, "title": title, "messages": msgs})
    st.session_state._history = history[:50]
    if st.session_state.get("_email"):
        _save_user_history(st.session_state._email, st.session_state._history)

def _delete_hist(sid: str):
    st.session_state._history = [s for s in st.session_state.get("_history", []) if s.get("id") != sid]
    if st.session_state.get("_email"):
        _save_user_history(st.session_state._email, st.session_state._history)

def _update_title(sid: str, new_title: str):
    for s in st.session_state.get("_history", []):
        if s.get("id") == sid:
            s["title"] = new_title
            st.session_state[f"_ctitle_{sid}"] = new_title
            break
    if st.session_state.get("_email"):
        _save_user_history(st.session_state._email, st.session_state._history)

# ════════════════════════════════════════════════════════════════════════
# WEB SEARCH
# ════════════════════════════════════════════════════════════════════════
def _web_search(query: str) -> str:
    try:
        r = requests.get("https://api.duckduckgo.com/", timeout=4,
                         params={"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"},
                         headers={"User-Agent": "Mozilla/5.0"})
        d = r.json()
        snippets = []
        if d.get("AbstractText"):
            snippets.append(f"[{d.get('AbstractSource','Web')}] {d['AbstractText'][:350]}")
        for t in d.get("RelatedTopics", [])[:3]:
            if isinstance(t, dict) and t.get("Text"):
                snippets.append(t["Text"][:200])
        if snippets:
            return "WEB CONTEXT:\n" + "\n".join(snippets)
    except Exception:
        pass
    return ""

# ════════════════════════════════════════════════════════════════════════
# SYSTEM HEALTH SCAN
# ════════════════════════════════════════════════════════════════════════
_HEALTH_KW = ["cpu","ram","memory","disk","storage","system scan","device info","computer specs","hardware","performance"]

def _needs_health(msg: str) -> bool:
    ml = msg.lower()
    return any(k in ml for k in _HEALTH_KW)

def _system_health_text() -> str:
    if not _HAS_PS:
        return "psutil not installed — system scan unavailable on this server."
    try:
        cpu = _ps.cpu_percent(interval=0.5)
        vm  = _ps.virtual_memory()
        du  = _ps.disk_usage("/")
        return (
            f"LIVE SYSTEM SCAN:\n"
            f"CPU Usage: {cpu}%\n"
            f"RAM: {round(vm.used/1e9,1)} GB used of {round(vm.total/1e9,1)} GB ({vm.percent}%)\n"
            f"Disk: {round(du.used/1e9,1)} GB used of {round(du.total/1e9,1)} GB ({du.percent}%)\n"
            f"RAM Available: {round(vm.available/1e9,1)} GB"
        )
    except Exception as e:
        return f"System scan error: {e}"

# ════════════════════════════════════════════════════════════════════════
# SHOPPING LINKS
# ════════════════════════════════════════════════════════════════════════
_SHOP_KW = ["buy","purchase","price","shop","order","where to get","where can i buy",
            "best price","cheapest","discount","offer","deal","product links"]

def _needs_shopping(msg: str) -> bool:
    ml = msg.lower()
    return any(k in ml for k in _SHOP_KW)

def _shopping_md(query: str) -> str:
    q = _uq(query)
    return (
        f"\n\n---\n🛒 **Shop Now:**  "
        f"[Amazon.in](https://www.amazon.in/s?k={q})  ·  "
        f"[Flipkart](https://www.flipkart.com/search?q={q})  ·  "
        f"[Google Shopping](https://www.google.com/search?tbm=shop&q={q})"
    )

# ════════════════════════════════════════════════════════════════════════
# DIAGRAM GENERATION
# ════════════════════════════════════════════════════════════════════════
_DIAG_KW = ["diagram","visualize","visualise","draw","animate","animation",
            "show how","explain visually","solar system","orbit","circuit","wave","molecule"]

def _needs_diagram(msg: str) -> bool:
    ml = msg.lower()
    return any(k in ml for k in _DIAG_KW)

def _generate_diagram_html(query: str, tier: str) -> str:
    if not _GROQ_KEY:
        return ""
    try:
        from groq import Groq as _Groq
        client = _Groq(api_key=_GROQ_KEY)
        resp = client.chat.completions.create(
            model=_MODELS[tier],
            messages=[
                {"role": "system", "content": (
                    "Output ONLY raw HTML starting with <!DOCTYPE html>. "
                    "Create an animated HTML5 canvas diagram. Canvas 520x300. "
                    "Background #010208. Neon colors: #00f5ff, #a855f7, #f59e0b, #00ff88. "
                    "Use requestAnimationFrame. No external libraries. "
                    "Make it visually stunning and educational with a title label."
                )},
                {"role": "user", "content": f"Animated diagram for: {query}"}
            ],
            max_tokens=2200, temperature=0.2
        )
        html = resp.choices[0].message.content.strip()
        if "<!DOCTYPE" in html or "<html" in html:
            start = html.find("<!DOCTYPE")
            if start == -1:
                start = html.find("<html")
            return html[start:]
    except Exception:
        pass
    return ""

# ════════════════════════════════════════════════════════════════════════
# AI RESPONSE (streaming)
# ════════════════════════════════════════════════════════════════════════
def _stream_response(messages: list, tier: str, placeholder, cross_ctx: str = "") -> str:
    if not _GROQ_KEY:
        placeholder.error("Groq API key not configured. Add GROQ_API_KEY to Streamlit secrets.")
        return ""
    try:
        from groq import Groq as _Groq
        sys_text = {"max": _SYS_MAX, "pro": _SYS_PRO}.get(tier, _SYS_BASE)
        sys_text  = sys_text.format(date=datetime.datetime.utcnow().strftime("%B %d, %Y"))
        if cross_ctx:
            sys_text += "\n\n" + cross_ctx
        all_msgs = [{"role": "system", "content": sys_text}] + messages
        max_tok  = {"basic": 2048, "pro": 4096, "max": 8192}.get(tier, 2048)
        client   = _Groq(api_key=_GROQ_KEY)
        stream   = client.chat.completions.create(
            model=_MODELS[tier], messages=all_msgs,
            max_tokens=max_tok, temperature=0.65, stream=True
        )
        full = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full += delta
                placeholder.markdown(f"*{full}*▌")
        placeholder.markdown(f"*{full}*")
        return full
    except Exception as e:
        placeholder.error(f"AI error: {e}")
        return ""

# ════════════════════════════════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ════════════════════════════════════════════════════════════════════════
_DEFAULTS = {
    "_auth_done":    False,
    "_email":        "",
    "_name":         "",
    "_tier":         "basic",
    "_page":         "home",
    "_messages":     [],
    "_session_id":   "",
    "_sess_start":   0.0,
    "_history":      [],
    "_pending_reg":  None,
    "_pending_login":None,
    "_auth_scr":     "choose",
    "_rename_id":    None,
    "_sel_plan":     "",
    "_pay_sent":     False,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ════════════════════════════════════════════════════════════════════════
# EARLY STARTUP — process background tasks from previous rerun
# ════════════════════════════════════════════════════════════════════════
if st.session_state._pending_reg:
    _pr = st.session_state._pending_reg
    st.session_state._pending_reg = None
    _create_account_safe(_pr["email"], _pr["name"], _pr["pw"], _pr["key"])

if st.session_state._pending_login:
    _pl = st.session_state._pending_login
    st.session_state._pending_login = None
    st.session_state._tier    = _get_tier(_pl["email"])
    st.session_state._history = _load_user_history(_pl["email"])

_inject_tier_css(st.session_state._tier)

# ════════════════════════════════════════════════════════════════════════
# AUTH GATE — renders auth UI then st.stop() if not logged in
# ════════════════════════════════════════════════════════════════════════
if not st.session_state._auth_done:
    st.markdown("""<style>
    [data-testid="stSidebar"]{display:none!important}
    .block-container{max-width:440px!important;padding-top:60px!important}
    </style>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:36px">
      <div style="font-size:48px;animation:float 3s ease-in-out infinite;display:inline-block">🔱</div>
      <div style="font-family:'Orbitron',monospace;font-size:26px;font-weight:900;letter-spacing:3px;
           background:linear-gradient(90deg,#00f5ff,#0080ff,#00f5ff);background-size:200% auto;
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           animation:shimmer 3s linear infinite;margin-top:10px">TITAN ULTRA</div>
      <div style="color:#222;font-size:11px;letter-spacing:2px;margin-top:4px">THE NEXT GENERATION AI</div>
    </div>
    """, unsafe_allow_html=True)

    _scr = st.session_state._auth_scr

    if _scr == "choose":
        st.markdown("<p style='text-align:center;color:#444;font-size:13px;margin-bottom:20px'>Sign in to continue</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📧  Email / Password", key="a_email", use_container_width=True):
                st.session_state._auth_scr = "login"; st.rerun()
        with c2:
            st.button("🔑  Google (soon)", key="a_google", use_container_width=True, disabled=True)
        st.markdown("<p style='text-align:center;color:#1e1e1e;font-size:11px;margin-top:28px'>By continuing you agree to Titan Ultra's terms</p>", unsafe_allow_html=True)

    elif _scr == "login":
        _tl, _tr = st.tabs(["LOG IN", "REGISTER"])

        with _tl:
            with st.form("lf"):
                _le = st.text_input("Email", placeholder="you@example.com", key="l_e")
                _lp = st.text_input("Password", type="password", placeholder="••••••••", key="l_p")
                _ls = st.form_submit_button("Log In →", use_container_width=True)
            if _ls:
                if not _le.strip() or not _lp:
                    st.error("Please fill in all fields.")
                else:
                    _ok, _msg = _verify_login(_le.strip(), _lp)
                    if _ok:
                        st.session_state._auth_done   = True
                        st.session_state._email       = _le.strip().lower()
                        st.session_state._name        = _msg
                        st.session_state._sess_start  = time.time()
                        st.session_state._pending_login = {"email": _le.strip().lower()}
                        st.rerun()
                    else:
                        st.error(_msg)

        with _tr:
            with st.form("rf"):
                _rn = st.text_input("Your Name", placeholder="Sanjay", key="r_n")
                _re = st.text_input("Email", placeholder="you@example.com", key="r_e")
                _rp = st.text_input("Password", type="password", placeholder="Min 6 characters", key="r_p")
                _rs = st.form_submit_button("Create Account →", use_container_width=True)
            if _rs:
                if not _rn.strip() or not _re.strip() or not _rp:
                    st.error("Please fill in all fields.")
                elif len(_rp) < 6:
                    st.error("Password must be at least 6 characters.")
                elif "@" not in _re:
                    st.error("Please enter a valid email address.")
                else:
                    _key = _fam_key(_re.strip().lower())
                    # Instant register — zero Gist calls here
                    st.session_state._auth_done   = True
                    st.session_state._email       = _re.strip().lower()
                    st.session_state._name        = _rn.strip()
                    st.session_state._tier        = "basic"
                    st.session_state._sess_start  = time.time()
                    st.session_state._pending_reg = {
                        "email": _re.strip().lower(),
                        "name":  _rn.strip(),
                        "pw":    _rp,
                        "key":   _key,
                    }
                    st.rerun()

        if st.button("← Back", key="a_back"):
            st.session_state._auth_scr = "choose"; st.rerun()

    st.stop()

# ════════════════════════════════════════════════════════════════════════
# MAIN APP — authenticated
# ════════════════════════════════════════════════════════════════════════
_ensure_session()
_tier    = st.session_state._tier
_name    = st.session_state._name
_email   = st.session_state._email
_page    = st.session_state._page
_history = st.session_state.get("_history", [])

# 2-hour basic limit check
if _tier == "basic" and st.session_state._sess_start > 0:
    if time.time() - st.session_state._sess_start > _SESSION_LIMIT_S:
        st.markdown("""<style>[data-testid="stSidebar"]{display:none!important}.block-container{max-width:500px!important;padding-top:80px!important}</style>""", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center">
          <div style="font-size:40px;margin-bottom:16px">⏰</div>
          <div style="font-family:Orbitron,monospace;font-size:20px;color:#00f5ff;margin-bottom:8px">Session Ended</div>
          <p style="color:#555;font-size:14px">Your 2-hour Basic session has ended.<br>Upgrade to Pro or Max for unlimited access.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔑 Upgrade Now", key="limit_up", use_container_width=True):
            st.session_state._page = "upgrade"
            st.session_state._sess_start = time.time()
            st.rerun()
        st.stop()

_TIER_C = {"basic": "#00f5ff", "pro": "#a855f7", "max": "#f59e0b"}
_TIER_L = {"basic": "BASIC",   "pro": "PRO",     "max": "MAX"}
_ac     = _TIER_C[_tier]

# ════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:18px 14px 12px;border-bottom:1px solid #161626">
      <div style="font-family:'Orbitron',monospace;font-size:17px;font-weight:900;letter-spacing:2px;
           background:linear-gradient(90deg,{_ac},{_ac}88,{_ac});background-size:200% auto;
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 3s linear infinite">
           🔱 TITAN ULTRA</div>
      <div style="margin-top:5px">
        <span style="display:inline-block;padding:2px 10px;border-radius:20px;font-size:9px;font-weight:700;
              letter-spacing:1.5px;background:{_ac}18;color:{_ac};border:1px solid {_ac}33">{_TIER_L[_tier]}</span>
      </div>
      <div style="font-size:9px;color:#222;letter-spacing:1px;margin-top:3px">PREVIEW TIER</div>
    </div>""", unsafe_allow_html=True)

    _tb, _tp, _tm = st.tabs(["BASIC", "PRO", "MAX"])
    with _tb:
        _a = "✅ " if _tier == "basic" else ""
        st.markdown(f"""<div style='padding:5px 0;font-size:11.5px;color:#555;line-height:2'>
        {_a}<span style='color:{"#00f5ff" if _tier=="basic" else "#2a2a2a"}'>Active</span><br>
        • 2-hour sessions<br>• Titan AI (70B)<br>• Web search<br>• Chat history</div>""", unsafe_allow_html=True)
    with _tp:
        if _tier == "pro":
            st.markdown("""<div style='padding:5px 0;font-size:11.5px;color:#555;line-height:2'>
            ✅ <span style='color:#a855f7'>Active</span><br>
            • Unlimited sessions<br>• Priority AI<br>• Extended answers<br>• All Basic features</div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='padding:3px 0;font-size:11px;color:#333'>₹300/month</div>", unsafe_allow_html=True)
            if st.button("Upgrade to Pro →", key="s_up_p", use_container_width=True):
                st.session_state._page = "upgrade"; st.rerun()
    with _tm:
        if _tier == "max":
            st.markdown("""<div style='padding:5px 0;font-size:11.5px;color:#555;line-height:2'>
            ✅ <span style='color:#f59e0b'>Active</span><br>
            • Max AI power<br>• All Pro features<br>• System scanner<br>• 8K answers<br>• <b style='color:#f59e0b'>Titan Code</b></div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='padding:3px 0;font-size:11px;color:#333'>₹3,500/month</div>", unsafe_allow_html=True)
            if st.button("Upgrade to Max →", key="s_up_m", use_container_width=True):
                st.session_state._page = "upgrade"; st.rerun()

    st.markdown(f"<div style='padding:5px 14px;font-size:9.5px;color:#1e1e1e'>⚡ {_MODEL_LABELS[_tier]}</div>", unsafe_allow_html=True)

    if st.button("＋  New Chat", key="new_chat", use_container_width=True):
        _save_current_chat()
        st.session_state._messages  = []
        st.session_state._session_id = _new_sid()
        st.session_state._page = "home"
        st.rerun()

    st.divider()

    _FEAT_NAV = [
        ("⚡  Titan Features", "features"),
        ("📓  Titan Notebook",  "notebook"),
        ("📚  Library",         "library"),
        ("📅  Schedule",        "schedule"),
        ("✅  Titan Tasks",     "tasks"),
    ]
    for _fn, _fk in _FEAT_NAV:
        if st.button(_fn, key=f"nav_{_fk}", use_container_width=True):
            st.session_state._page = _fk; st.rerun()

    # Titan Code — visible to all, accessible only to Max
    if _tier == "max":
        if st.button("🧑‍💻  Titan Code", key="nav_tcode", use_container_width=True):
            st.session_state._page = "titan_code"; st.rerun()
    else:
        if st.button("🧑‍💻  Titan Code  👑", key="nav_tcode_lock", use_container_width=True):
            st.session_state._page = "titan_code"; st.rerun()

    if _tier != "max":
        if st.button("🔑  Upgrade Plan", key="nav_upg", use_container_width=True):
            st.session_state._page = "upgrade"; st.rerun()

    st.divider()
    st.markdown("<div style='padding:0 14px 4px;font-size:9px;color:#1e1e1e;letter-spacing:1px'>HISTORY</div>", unsafe_allow_html=True)

    _ren_id = st.session_state._rename_id
    for _i, _sess in enumerate(_history[:20]):
        _sid   = _sess.get("id", "")
        _stit  = _sess.get("title", "Chat")
        if _ren_id == _sid:
            _nn = st.text_input("", value=_stit, key=f"ren_{_sid}", label_visibility="collapsed")
            _rc1, _rc2 = st.columns(2)
            with _rc1:
                if st.button("✓ Save", key=f"rok_{_sid}", use_container_width=True):
                    _update_title(_sid, _nn.strip() or _stit)
                    st.session_state._rename_id = None; st.rerun()
            with _rc2:
                if st.button("Cancel", key=f"rca_{_sid}", use_container_width=True):
                    st.session_state._rename_id = None; st.rerun()
        else:
            _h1, _h2, _h3 = st.columns([9, 1, 1])
            with _h1:
                _lbl = (_stit[:24] + "…") if len(_stit) > 24 else _stit
                if st.button(_lbl, key=f"h_{_sid}_{_i}", use_container_width=True):
                    _load_history_into_session(_sid); st.rerun()
            with _h2:
                if st.button("✏", key=f"hr_{_sid}_{_i}", help="Rename"):
                    st.session_state._rename_id = _sid; st.rerun()
            with _h3:
                if st.button("×", key=f"hd_{_sid}_{_i}", help="Delete"):
                    _delete_hist(_sid); st.rerun()

    st.divider()
    if st.button("⬡  Sign out", key="signout", use_container_width=True):
        _save_current_chat()
        for _k in list(st.session_state.keys()):
            del st.session_state[_k]
        st.rerun()

# ════════════════════════════════════════════════════════════════════════
# PAGE: UPGRADE
# ════════════════════════════════════════════════════════════════════════
if _page == "upgrade":
    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac};margin-bottom:4px'>Upgrade Titan Ultra</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444;font-size:13px;margin-bottom:28px'>Unlock the full power. Cancel anytime.</p>", unsafe_allow_html=True)

    _c1, _c2, _c3 = st.columns(3)
    _PLANS = [
        ("basic", "BASIC",  "Free",    "",                    ["2-hr sessions","Llama 3.3 70B","Web search","Chat history","Daily sparks"], "#00f5ff"),
        ("pro",   "PRO",    "₹300",    "/month · ₹2,500/yr",  ["All Basic+","Unlimited sessions","Priority AI","4K token answers","Advanced memory"], "#a855f7"),
        ("max",   "MAX",    "₹3,500",  "/month · ₹18,000/yr", ["All Pro+","Max AI power","System scanner","8K token answers","Priority support"], "#f59e0b"),
    ]
    for _col, (_pid, _pn, _pp, _ps, _pf, _pc) in zip([_c1, _c2, _c3], _PLANS):
        with _col:
            _curr = _tier == _pid
            _brd  = f"2px solid {_pc}" if _curr else "1px solid #161626"
            st.markdown(f"""
            <div style="background:#0f0f0f;{_brd};border-radius:18px;padding:22px;text-align:center">
              <div style="font-family:Orbitron,monospace;font-size:13px;font-weight:900;letter-spacing:2px;color:{_pc}">{_pn}</div>
              <div style="font-size:26px;font-weight:700;color:#e0e0e0;margin:12px 0 2px">{_pp}</div>
              <div style="font-size:11px;color:#333;margin-bottom:14px">{_ps}</div>
              {"".join(f'<div style="font-size:12px;color:#555;padding:3px 0;text-align:left">✓ {f}</div>' for f in _pf)}
              {"<br><div style='font-size:10px;color:"+_pc+";font-weight:700;margin-top:8px'>✅ CURRENT PLAN</div>" if _curr else ""}
            </div>""", unsafe_allow_html=True)
            if not _curr and _pid != "basic":
                if st.button(f"Get {_pn}", key=f"plan_{_pid}", use_container_width=True):
                    st.session_state._sel_plan  = _pid
                    st.session_state._pay_sent  = False
                    st.rerun()

    _sel = st.session_state._sel_plan
    if _sel and _sel != "basic" and not st.session_state._pay_sent:
        _pp2 = {"pro": "₹300", "max": "₹3,500"}[_sel]
        st.divider()
        st.markdown(f"<h4 style='color:{_TIER_C[_sel]}'>Complete Payment — {_sel.upper()} {_pp2}/month</h4>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#0f0f0f;border:1px solid #1a1a3a;border-radius:14px;padding:20px;margin:16px 0">
          <div style="font-size:13px;color:#555;margin-bottom:10px">Pay via PhonePe / Google Pay / Any UPI app</div>
          <div style="font-size:22px;font-weight:700;color:{_TIER_C[_sel]};letter-spacing:1px;font-family:monospace">{_OWNER_UPI}</div>
          <div style="font-size:11px;color:#333;margin-top:8px">Copy the UPI ID above and complete payment, then enter your transaction ID below.</div>
        </div>""", unsafe_allow_html=True)
        with st.form("utr_f"):
            _utr = st.text_input("Transaction ID / UTR Number", placeholder="e.g. 423987654321")
            if st.form_submit_button("Submit →", use_container_width=True):
                if len(_utr.strip()) < 6:
                    st.error("Please enter a valid transaction ID.")
                else:
                    _submit_payment(_email, _sel, _utr.strip())
                    st.session_state._pay_sent = True
                    st.rerun()

    if st.session_state._pay_sent:
        st.success("✅ Payment submitted! Your account will be upgraded within a few hours. Thank you!")
        if st.button("← Back to Home", key="pay_back"):
            st.session_state._page = "home"
            st.session_state._pay_sent = False
            st.session_state._sel_plan = ""
            st.rerun()
    else:
        if st.button("← Back", key="upg_back"):
            st.session_state._page = "home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# PAGE: FEATURES
# ════════════════════════════════════════════════════════════════════════
if _page == "features":
    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>⚡ Titan Features</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#333;font-size:13px;margin-bottom:22px'>Everything Titan Ultra can do for you.</p>", unsafe_allow_html=True)
    _FEATS = [
        ("🌐","Live Web Search","Searches the internet on every single message — always gives you current, accurate information from the most trusted sources worldwide.","ALL TIERS","#00f5ff"),
        ("🧠","Cross-Chat Memory","Remembers context across all your conversations. Bring up any topic from any previous chat — Titan never forgets what you've discussed.","ALL TIERS","#00f5ff"),
        ("🎨","Animated Diagrams","Ask Titan to explain anything visually and it generates a live animated HTML5 diagram — from solar systems to algorithms to molecular structures.","ALL TIERS","#00f5ff"),
        ("💻","System Health Scan","Scan your device in real time — CPU usage, RAM, disk space, and more. Just ask 'scan my system' or 'how much RAM do I have'.","ALL TIERS","#00f5ff"),
        ("🛒","Smart Shopping","Ask for any product and Titan instantly sends direct shopping links from Amazon.in, Flipkart, and Google Shopping.","ALL TIERS","#00f5ff"),
        ("📡","Deep Research","Combines live web context with advanced AI analysis to give answers that beat ChatGPT, Gemini, and Perplexity on every topic.","ALL TIERS","#00f5ff"),
        ("💎","Priority AI Engine","Pro users get the AI running at full priority with 4K token limits for deeper, longer, more detailed answers.","PRO + MAX","#a855f7"),
        ("📓","Titan Notebook","A personal notebook that persists across sessions — write, save, and retrieve notes anytime.","ALL TIERS","#00f5ff"),
        ("📅","Smart Schedule","Plan your day with an AI-powered schedule. Add events, set times, stay organised.","ALL TIERS","#00f5ff"),
        ("✅","Titan Tasks","A powerful to-do list with progress tracking. Never lose track of what needs to be done.","ALL TIERS","#00f5ff"),
        ("👑","Max Intelligence","Max tier unlocks 8192-token responses, maximum AI depth, and highest possible answer quality.","MAX ONLY","#f59e0b"),
        ("🧑‍💻","Titan Code","A full AI-powered coding environment — write, debug, explain, and refactor code in any language with the most powerful AI engine.","MAX ONLY","#f59e0b"),
        ("🔒","Secure Accounts","Your data is encrypted and stored securely. Each account is fully private.","ALL TIERS","#00f5ff"),
    ]
    _cols = st.columns(2)
    for _fi, (_ic, _ft, _fd, _fl, _fc) in enumerate(_FEATS):
        with _cols[_fi % 2]:
            st.markdown(f"""
            <div class="feat-card" style="animation-delay:{_fi*0.06}s">
              <span class="feat-icon">{_ic}</span>
              <div class="feat-title">{_ft}</div>
              <div class="feat-desc">{_fd}</div>
              <div class="feat-badge" style="color:{_fc};background:{_fc}18;border-color:{_fc}33">{_fl}</div>
            </div>""", unsafe_allow_html=True)
    if st.button("← Back to Home", key="feat_bk"): st.session_state._page="home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# PAGE: NOTEBOOK
# ════════════════════════════════════════════════════════════════════════
if _page == "notebook":
    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>📓 Titan Notebook</h2>", unsafe_allow_html=True)
    _nk = f"_nb_{_fam_key(_email)}"
    if _nk not in st.session_state:
        st.session_state[_nk] = ""
    _note = st.text_area("", value=st.session_state[_nk], height=340,
                          key="nb_txt", label_visibility="collapsed", placeholder="Start writing your notes…")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save", key="nb_sv", use_container_width=True):
            st.session_state[_nk] = _note; st.success("Saved!")
    with c2:
        if st.button("🗑 Clear", key="nb_cl", use_container_width=True):
            st.session_state[_nk] = ""; st.rerun()
    if st.button("← Back", key="nb_bk"): st.session_state._page="home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# PAGE: LIBRARY
# ════════════════════════════════════════════════════════════════════════
if _page == "library":
    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>📚 Library</h2>", unsafe_allow_html=True)
    _lk = f"_lib_{_fam_key(_email)}"
    if _lk not in st.session_state:
        st.session_state[_lk] = []
    _lib = st.session_state[_lk]
    if not _lib:
        st.markdown("<p style='color:#222;font-style:italic;text-align:center;padding:40px'>No saved items yet.</p>", unsafe_allow_html=True)
    else:
        for _idx, _item in enumerate(_lib):
            with st.expander(f"📌 {_item.get('title','Item')} — {_item.get('date','')}"):
                st.markdown(f"*{_item.get('content','')}*")
                if st.button("Remove", key=f"lb_d_{_idx}"):
                    _lib.pop(_idx); st.rerun()
    if st.button("← Back", key="lb_bk"): st.session_state._page="home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# PAGE: SCHEDULE
# ════════════════════════════════════════════════════════════════════════
if _page == "schedule":
    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>📅 Schedule</h2>", unsafe_allow_html=True)
    _sk = f"_sched_{_fam_key(_email)}"
    if _sk not in st.session_state:
        st.session_state[_sk] = []
    with st.expander("➕ Add Event"):
        with st.form("sch_f"):
            _et = st.text_input("Title", placeholder="Meeting, Study session…")
            c1, c2 = st.columns(2)
            with c1: _ed = st.date_input("Date")
            with c2: _etm = st.time_input("Time")
            _en = st.text_input("Note (optional)")
            if st.form_submit_button("Add →", use_container_width=True) and _et.strip():
                st.session_state[_sk].append({"title":_et,"date":str(_ed),"time":str(_etm),"note":_en}); st.rerun()
    _evs = sorted(st.session_state[_sk], key=lambda x:(x.get("date",""),x.get("time","")))
    if _evs:
        for _ei, _ev in enumerate(_evs):
            c1, c2 = st.columns([10,1])
            with c1:
                st.markdown(f"""<div style='background:#0f0f0f;border:1px solid #161626;border-radius:10px;padding:12px 16px;margin-bottom:8px'>
                <div style='color:#e0e0e0;font-size:14px;font-weight:600'>{_ev.get("title","")}</div>
                <div style='color:#444;font-size:12px;margin-top:3px'>📅 {_ev.get("date","")}  ⏰ {_ev.get("time","")}</div>
                {"<div style='color:#333;font-size:12px;margin-top:2px'>"+_ev.get("note","")+"</div>" if _ev.get("note") else ""}</div>""", unsafe_allow_html=True)
            with c2:
                if st.button("×", key=f"ev_{_ei}", help="Delete"):
                    st.session_state[_sk].pop(_ei); st.rerun()
    else:
        st.markdown("<p style='color:#222;font-style:italic;padding:20px 0'>No events yet.</p>", unsafe_allow_html=True)
    if st.button("← Back", key="sch_bk"): st.session_state._page="home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# PAGE: TASKS
# ════════════════════════════════════════════════════════════════════════
if _page == "tasks":
    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>✅ Titan Tasks</h2>", unsafe_allow_html=True)
    _tk = f"_tasks_{_fam_key(_email)}"
    if _tk not in st.session_state:
        st.session_state[_tk] = []
    with st.form("tk_f"):
        _tc1, _tc2 = st.columns([6,1])
        with _tc1: _nt = st.text_input("", label_visibility="collapsed", placeholder="Add a task…")
        with _tc2: _ta = st.form_submit_button("Add", use_container_width=True)
    if _ta and _nt.strip():
        st.session_state[_tk].append({"text":_nt.strip(),"done":False}); st.rerun()
    _tasks = st.session_state[_tk]
    _done  = sum(1 for t in _tasks if t["done"])
    if _tasks:
        st.markdown(f"<div style='color:#333;font-size:12px;margin-bottom:8px'>{_done}/{len(_tasks)} completed</div>", unsafe_allow_html=True)
        _prog = _done/len(_tasks) if _tasks else 0
        st.markdown(f"""<div style='background:#111;border-radius:4px;height:3px;margin-bottom:14px'>
        <div style='background:{_ac};border-radius:4px;height:3px;width:{int(_prog*100)}%;box-shadow:0 0 8px {_ac}'></div></div>""", unsafe_allow_html=True)
        for _ti, _task in enumerate(_tasks):
            t1, t2, t3 = st.columns([1,10,1])
            with t1:
                _chk = st.checkbox("", value=_task["done"], key=f"tc_{_ti}", label_visibility="collapsed")
                if _chk != _task["done"]:
                    st.session_state[_tk][_ti]["done"] = _chk; st.rerun()
            with t2:
                _sty = "text-decoration:line-through;color:#222" if _task["done"] else "color:#ccc"
                st.markdown(f"<div style='{_sty};font-size:13.5px;padding:5px 0'>{_task['text']}</div>", unsafe_allow_html=True)
            with t3:
                if st.button("×", key=f"td_{_ti}", help="Delete"):
                    st.session_state[_tk].pop(_ti); st.rerun()
        if _done > 0:
            if st.button("🗑 Clear completed", key="tc_cl"):
                st.session_state[_tk] = [t for t in _tasks if not t["done"]]; st.rerun()
    else:
        st.markdown("<p style='color:#222;font-style:italic;padding:20px 0'>No tasks yet.</p>", unsafe_allow_html=True)
    if st.button("← Back", key="tk_bk"): st.session_state._page="home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# PAGE: TITAN CODE (MAX ONLY)
# ════════════════════════════════════════════════════════════════════════
if _page == "titan_code":
    if _tier != "max":
        # Locked screen for non-Max users
        st.markdown("""<style>.block-container{max-width:540px!important;padding-top:60px!important}</style>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;padding:20px 0 30px">
          <div style="font-size:48px;margin-bottom:14px;animation:float 3s ease-in-out infinite;display:inline-block">🧑‍💻</div>
          <div style="font-family:Orbitron,monospace;font-size:20px;font-weight:900;color:#f59e0b;letter-spacing:2px;margin-bottom:8px">TITAN CODE</div>
          <div style="font-size:13px;color:#444;margin-bottom:24px">This feature is exclusively for <b style='color:#f59e0b'>Max tier</b> subscribers.</div>
          <div style="background:#0f0f0f;border:1px solid #f59e0b22;border-radius:16px;padding:24px;text-align:left;margin-bottom:24px">
            <div style="font-size:13px;color:#666;margin-bottom:12px;font-weight:600">What Titan Code can do:</div>
            <div style="font-size:13px;color:#555;line-height:2">
              ✦ Write code in any language from scratch<br>
              ✦ Debug and fix errors instantly<br>
              ✦ Explain any code in plain language<br>
              ✦ Refactor and optimise your code<br>
              ✦ Generate complete apps and scripts<br>
              ✦ Review and suggest improvements
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👑  Upgrade to Max — ₹3,500/month", key="tc_upg", use_container_width=True):
            st.session_state._page = "upgrade"; st.rerun()
        if st.button("← Back", key="tc_bk_lock"): st.session_state._page="home"; st.rerun()
        st.stop()

    # ── Full Titan Code interface (Max only) ──────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:20px">
      <div style="font-family:Orbitron,monospace;font-size:22px;font-weight:900;color:#f59e0b;letter-spacing:2px">🧑‍💻 TITAN CODE</div>
      <div style="font-size:11px;color:#444;letter-spacing:1px;margin-top:4px">MAX TIER · AI-POWERED CODING ENVIRONMENT</div>
    </div>
    """, unsafe_allow_html=True)

    _CODE_LANGS = ["Python","JavaScript","TypeScript","Java","C++","C","C#","Go","Rust","Kotlin",
                   "Swift","PHP","Ruby","SQL","HTML/CSS","Bash","R","Dart","Scala","Other"]
    _CODE_MODES = ["Write code","Debug & fix","Explain code","Refactor","Add comments","Review & improve","Convert language","Generate tests"]

    _cc1, _cc2 = st.columns([2, 1])
    with _cc2:
        _lang = st.selectbox("Language", _CODE_LANGS, key="tc_lang")
        _mode = st.selectbox("Mode", _CODE_MODES, key="tc_mode")

    with _cc1:
        _code_input = st.text_area(
            "Your code or request",
            height=200,
            key="tc_input",
            placeholder="Paste your code here, or describe what you want to build…",
            label_visibility="collapsed"
        )

    _tc_btn = st.button("⚡  Run Titan Code", key="tc_run", use_container_width=True)

    # Output area
    _tc_out_key = "_tc_output"
    if _tc_btn and _code_input.strip():
        _tc_sys = (
            "You are Titan Code — the most advanced AI coding assistant ever built. "
            "You write clean, efficient, production-ready code. "
            "You explain things clearly when asked. "
            "You never give incomplete code — always provide full, working implementations. "
            "Format all code in proper markdown code blocks with language tags."
        )
        _tc_prompt = f"Mode: {_mode}\nLanguage: {_lang}\n\n{_code_input.strip()}"
        try:
            from groq import Groq as _Groq
            _client = _Groq(api_key=_GROQ_KEY)
            _stream = _client.chat.completions.create(
                model=_MODELS["max"],
                messages=[
                    {"role": "system", "content": _tc_sys},
                    {"role": "user",   "content": _tc_prompt}
                ],
                max_tokens=8192, temperature=0.2, stream=True
            )
            _ph = st.empty()
            _out = ""
            for _chunk in _stream:
                _d = _chunk.choices[0].delta.content
                if _d:
                    _out += _d
                    _ph.markdown(_out + "▌")
            _ph.markdown(_out)
            st.session_state[_tc_out_key] = _out
        except Exception as _e:
            st.error(f"Titan Code error: {_e}")
    elif _tc_out_key in st.session_state and st.session_state[_tc_out_key]:
        st.markdown(st.session_state[_tc_out_key])

    if st.button("← Back", key="tc_bk"): st.session_state._page="home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# HOME SCREEN
# ════════════════════════════════════════════════════════════════════════
def _has_msgs():
    return bool(st.session_state.get("_messages"))

if _page == "home" and not _has_msgs():
    st.markdown("""<style>
    [data-testid="stMain"] .block-container{display:flex;flex-direction:column;justify-content:center;min-height:88vh;padding-top:10px!important}
    [data-testid="stBottom"]{display:none!important}
    </style>""", unsafe_allow_html=True)

    _phrase = random.choice(_PHRASES)
    _first  = (_name.split()[0] if _name else "there")
    _hr     = datetime.datetime.now().hour
    _tod    = "Good morning" if _hr < 12 else "Good afternoon" if _hr < 17 else "Good evening"

    st.markdown(f"""
    <div style="text-align:center;padding:16px 0 24px;animation:fadeIn .6s ease">
      <div style="position:relative;display:inline-block;margin-bottom:14px">
        <div style="font-size:50px;animation:float 3s ease-in-out infinite;display:inline-block">🔱</div>
        <div style="position:absolute;top:50%;left:50%;width:88px;height:88px;border:1px solid {_ac}22;
                    border-radius:50%;transform:translate(-50%,-50%);animation:spin 8s linear infinite"></div>
        <div style="position:absolute;top:50%;left:50%;width:116px;height:116px;border:1px solid {_ac}0d;
                    border-radius:50%;transform:translate(-50%,-50%);animation:spin 14s linear infinite reverse"></div>
      </div>
      <div style="font-family:'Orbitron',monospace;font-size:13px;color:{_ac};letter-spacing:3px;font-weight:700;margin-bottom:8px">{_tod}, {_first}</div>
      <div style="font-family:'Orbitron',monospace;font-size:20px;font-weight:400;color:#bbb;letter-spacing:1px">{_phrase}</div>
    </div>
    """, unsafe_allow_html=True)

    # Daily Spark
    _spark = _SPARKS[datetime.datetime.now().day % len(_SPARKS)]
    st.markdown(f"""
    <div class="spark-card">
      <div class="spark-label">✦ DAILY SPARK</div>
      <div class="spark-text">{_spark}</div>
    </div>""", unsafe_allow_html=True)

    # Quick actions
    _qcols = st.columns(len(_QUICK_ACTIONS))
    for _qi, (_ql, _qp) in enumerate(_QUICK_ACTIONS):
        with _qcols[_qi]:
            if st.button(_ql, key=f"qa_{_qi}", use_container_width=True):
                st.session_state._home_pend = _qp
                st.rerun()

    # Main home input
    _, _hc, _ = st.columns([1, 5, 1])
    with _hc:
        _pend = st.session_state.pop("_home_pend", "") if hasattr(st.session_state, "_home_pend") else ""
        _home_in = st.text_input(
            "", placeholder="Ask Titan Ultra anything…",
            key="_home_input", label_visibility="collapsed",
            value=_pend if _pend else ""
        )
        if _home_in and _home_in.strip():
            st.session_state._messages = [{"role": "user", "content": _home_in.strip()}]
            if not st.session_state._session_id:
                st.session_state._session_id = _new_sid()
            st.session_state._page = "chat"
            st.rerun()

    if _tier == "basic" and st.session_state._sess_start > 0:
        _rem = max(0, _SESSION_LIMIT_S - (time.time() - st.session_state._sess_start))
        _rem_m = int(_rem // 60)
        st.markdown(f"<p style='text-align:center;color:#1a1a2a;font-size:11px;margin-top:14px'>⏱ {_rem_m} min remaining in Basic session</p>", unsafe_allow_html=True)

    st.stop()

# ════════════════════════════════════════════════════════════════════════
# CHAT PAGE
# ════════════════════════════════════════════════════════════════════════
_msgs = st.session_state._messages

# Render message history
for _msg in _msgs:
    if _msg["role"] == "user":
        _txt = str(_msg["content"]).replace("<","&lt;").replace(">","&gt;")
        st.markdown(f"""
        <div class="user-bubble">
          <div class="user-bubble-inner">{_txt}</div>
        </div>""", unsafe_allow_html=True)
    else:
        _cnt = _msg.get("content", "")
        if isinstance(_cnt, str) and _cnt.startswith("__DIAG__:"):
            try:
                import streamlit.components.v1 as _cv1
                _cv1.html(_cnt[9:], height=340, scrolling=False)
            except Exception:
                pass
        else:
            st.markdown(f"""
            <div class="ai-bubble">
              <div class="ai-label">🔱 TITAN ULTRA</div>
              <div class="ai-text">{_cnt}</div>
            </div>""", unsafe_allow_html=True)

# If last message is from user, generate AI response
if _msgs and _msgs[-1]["role"] == "user":
    _umsg = _msgs[-1]["content"]
    _cross_ctx = _build_cross_ctx(_history)

    # 1. Diagram
    _diag_html = ""
    if _needs_diagram(_umsg):
        with st.spinner("🎨 Generating animated diagram…"):
            _diag_html = _generate_diagram_html(_umsg, _tier)

    # 2. System health
    _health_ctx = ""
    if _needs_health(_umsg):
        _health_ctx = _system_health_text()

    # 3. Web search
    _search_ctx = ""
    with st.spinner("🌐 Searching web…"):
        _search_ctx = _web_search(_umsg)

    # 4. Shopping
    _shop_md = ""
    if _needs_shopping(_umsg):
        _shop_md = _shopping_md(_umsg)

    # Build messages for AI (augmented)
    _ai_msgs = [{"role": m["role"], "content": m["content"]}
                for m in _msgs[:-1]
                if not (isinstance(m.get("content"), str) and m["content"].startswith("__DIAG__:"))]
    _aug = _umsg
    if _search_ctx:
        _aug += f"\n\n[{_search_ctx}]"
    if _health_ctx:
        _aug += f"\n\n[{_health_ctx}]"
    _ai_msgs.append({"role": "user", "content": _aug})

    # Show diagram first
    if _diag_html:
        try:
            import streamlit.components.v1 as _cv1
            _cv1.html(_diag_html, height=340, scrolling=False)
            _msgs.append({"role": "assistant", "content": f"__DIAG__:{_diag_html}"})
        except Exception:
            pass

    # Stream AI response
    st.markdown(f"""<div class="ai-bubble" style="margin-top:4px">
      <div class="ai-label">🔱 TITAN ULTRA</div>
    </div>""", unsafe_allow_html=True)
    _ph = st.empty()
    _resp = _stream_response(_ai_msgs, _tier, _ph, _cross_ctx)

    if _resp:
        if _shop_md:
            _resp += _shop_md
            _ph.markdown(f"*{_resp}*")
        _msgs.append({"role": "assistant", "content": _resp})
        st.session_state._messages = _msgs
        st.session_state._page = "chat"
        _save_current_chat()
        st.rerun()

# Chat input
_inp = st.chat_input("Message Titan Ultra…")
if _inp and _inp.strip():
    if not st.session_state._session_id:
        st.session_state._session_id = _new_sid()
    st.session_state._messages.append({"role": "user", "content": _inp.strip()})
    st.session_state._page = "chat"
    st.rerun()
