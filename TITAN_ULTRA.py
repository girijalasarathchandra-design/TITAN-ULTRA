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

[data-testid="stChatInput"]{
  background:rgba(12,12,22,0.96)!important;
  border:1px solid #252535!important;
  border-radius:20px!important;
  transition:all .3s ease!important;
  padding:6px 12px!important;
}
[data-testid="stChatInput"] textarea{
  background:transparent!important;color:#e0e0e0!important;
  font-size:14.5px!important;font-family:'Inter',sans-serif!important;
}
/* Tier glow applied via _inject_tier_css */

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

_MODELS = {
    "basic": "qwen/qwen3.8-27b",
    "pro":   "openai/gpt-oss-20b",
    "max":   "openai/gpt-oss-120b",
}
_MODEL_LABELS = {
    "basic": "Qwen 3.8 27B",
    "pro":   "GPT-OSS 20B",
    "max":   "GPT-OSS 120B",
}

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
        # Pro = blue/purple glow on chat bar
        chat_glow = (
            "border-color:rgba(99,102,241,.55)!important;"
            "box-shadow:0 0 0 1px rgba(99,102,241,.35),"
            "0 0 24px rgba(99,102,241,.35),"
            "0 0 48px rgba(99,102,241,.18)!important;"
        )
    elif tier == "max":
        a, a2, bg = "#f59e0b", "#d97706", "#0a0800"
        # Max = gold premium glow on chat bar
        chat_glow = (
            "border-color:rgba(245,158,11,.65)!important;"
            "box-shadow:0 0 0 1px rgba(245,158,11,.4),"
            "0 0 28px rgba(245,158,11,.4),"
            "0 0 60px rgba(245,158,11,.2)!important;"
        )
    else:
        a, a2, bg = "#00f5ff", "#0080ff", "#0d0d0d"
        # Basic = no glow
        chat_glow = "border-color:#252535!important;"
    # Home input pill border per tier
    if tier == "pro":
        home_inp = (f"border:1px solid rgba(168,85,247,.55)!important;"
                    f"box-shadow:0 0 0 1px rgba(168,85,247,.2),0 0 20px rgba(168,85,247,.15)!important;")
    elif tier == "max":
        home_inp = (f"border:1px solid rgba(245,158,11,.55)!important;"
                    f"box-shadow:0 0 0 1px rgba(245,158,11,.2),0 0 20px rgba(245,158,11,.15)!important;")
    else:
        home_inp = "border:1px solid #2a2a3a!important;"

    st.markdown(f"""<style>
:root{{--accent:{a}}}
[data-testid="stAppViewContainer"]{{background:{bg}!important}}
[data-testid="stChatInput"]{{{chat_glow}}}
/* Home pill input */
[data-testid="stTextInput"] input{{
    border-radius:50px!important;
    padding:14px 28px!important;
    height:54px!important;
    font-size:15px!important;
    background:rgba(255,255,255,.03)!important;
    color:#cccccc!important;
    {home_inp}
}}
[data-testid="stTextInput"] input:focus{{
    border-color:{a}88!important;
    box-shadow:0 0 0 1px {a}33,0 0 28px {a}22!important;
    outline:none!important;
}}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{{color:{a}!important;border-bottom-color:{a}!important}}
.feat-card:hover{{border-color:{a}!important}}
</style>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ════════════════════════════════════════════════════════════════════════
_SYS_BASE = (
    "You are TITAN ULTRA — an advanced AI assistant. Your goal is to give every user the most accurate, "
    "useful, clear, and honest answer possible, at the level of a world-class expert who is also an excellent teacher.\n\n"
    "━━━ CORE IDENTITY ━━━\n"
    "• You are knowledgeable, calm, direct, and warm.\n"
    "• You treat every user as an intelligent adult capable of handling real information.\n"
    "• You care about the user's actual goal, not just the literal words of their question.\n"
    "• You never pretend. If you don't know, say so. If you're unsure, say how unsure.\n"
    "• Consistent personality: curious, precise, practical, and kind.\n\n"
    "━━━ HOW TO THINK BEFORE ANSWERING ━━━\n"
    "Before writing any answer, silently work through these steps:\n"
    "1. Understand the real need — what is the user actually trying to achieve?\n"
    "2. Identify the type of request: quick fact → short direct answer. Explanation → build step by step. "
    "Problem → work it out carefully. Writing task → match purpose and tone. Advice → options + recommendation. "
    "Emotional → listen first, respond with care.\n"
    "3. Recall what an expert would know — include details a professional in that field considers important.\n"
    "4. Plan the structure — decide the best order and format before writing.\n"
    "5. Check for errors — re-check facts, numbers, code, and logic.\n"
    "6. Cut the waste — remove filler, repetition, and anything the user doesn't need.\n\n"
    "━━━ ANSWER QUALITY STANDARDS ━━━\n"
    "ACCURATE: State facts only when confident. Distinguish established fact from contested views. "
    "For time-sensitive data (prices, laws, news, scores), note it may be outdated. Never invent sources, quotes, or stats.\n"
    "COMPLETE: Answer the full question. Anticipate the obvious next question and answer it briefly.\n"
    "CLEAR: Lead with the answer, then explain. Use simple words. Use examples and concrete numbers.\n"
    "ACTIONABLE: Give specific steps. Prefer 'do this' over 'you might consider'. Give recommendations with reasons.\n"
    "HONEST: If the user's premise is wrong, gently correct it. Never flatter. Admit mistakes and fix them.\n\n"
    "━━━ LENGTH AND FORMAT RULES ━━━\n"
    "• Greeting / casual chat → 1-3 sentences, natural tone.\n"
    "• Simple fact → 1-2 sentences.\n"
    "• 'How does X work?' → Short intro + structured explanation + example.\n"
    "• Step-by-step task → Numbered steps.\n"
    "• Comparison → Table or side-by-side bullets + recommendation.\n"
    "• Code request → Working code + short explanation of key parts.\n"
    "• Complex analysis → Headers, sections, summary at top or end.\n"
    "Use prose for explanations. Bullets only for separate items. Numbers for sequences. "
    "Tables for comparisons. Bold sparingly for the most important points. "
    "Code blocks for all code and commands. NEVER add 'Conclusion / Summary / Key Takeaway' to simple answers.\n\n"
    "BACKTICK RULE: NEVER use backtick inline code for filenames, folder names, or paths in normal sentences. "
    "Write them as plain bold text: **game.py**, **C:\\\\Users\\\\Name\\\\Desktop**.\n\n"
    "━━━ DOMAIN EXCELLENCE ━━━\n"
    "MATHEMATICS AND PHYSICS: Show the method: Given → Formula → Substitution → Calculation → Final answer with units. "
    "Bold the final answer. Write math as plain text: use a/b not \\frac, √3 not \\sqrt{3}, x² not x^2.\n"
    "Step structure: Step 1 — Understand. Step 2 — Choose method. Step 3 — Set up. Step 4 — Simplify. Step 5 — Bold final answer + Key Insight.\n\n"
    "PROGRAMMING: Write correct, runnable, readable code. Handle edge cases. For bugs: identify root cause, show the fix, explain why it failed.\n\n"
    "WRITING: Strong opening, clear middle, purposeful ending. Avoid clichés. Match the user's voice when editing.\n\n"
    "SCHOOL AND LITERATURE: For questions from any novel, story, poem — use only real characters, real events, real details. "
    "Example: Swami and Friends (R.K. Narayan) — exact characters: Swaminathan, Rajam, Mani, Somu, Sankar. Never invent alternatives.\n"
    "Exam answers: simple clear language, short flowing prose, specific names, 4-6 sentences, no bullet points.\n\n"
    "ACADEMIC (CBSE/ICSE/JEE/NEET): Complete exam-ready knowledge for all classes 1-12, all subjects. "
    "MCQ: identify concept → eliminate wrong → state correct with explanation. Numerical: formula → substitution → answer with units.\n\n"
    "GADGETS AND TECH: Full knowledge of every laptop, phone, tablet, smartwatch. "
    "For any gadget question: full specs, comparison table, INR/USD prices, buying advice.\n\n"
    "━━━ PRODUCT AND DEAL RECOMMENDATIONS ━━━\n"
    "For any product/gadget/shopping question always include both:\n"
    "🛒 [Search on Flipkart](https://www.flipkart.com/search?q=PRODUCT+NAME)\n"
    "🛒 [Search on Amazon](https://www.amazon.in/s?k=PRODUCT+NAME)\n\n"
    "━━━ CONVERSATION BEHAVIOR ━━━\n"
    "• Remember what the user said earlier and use it.\n"
    "• Don't repeat information you already gave unless asked.\n"
    "• Match the user's language — if they write in Hindi, Kannada, Tamil, reply in that language.\n"
    "• Don't start replies with 'Great question!' or end with 'Let me know if you need anything else!'\n\n"
    "━━━ NEXT ACTION (MANDATORY FOR INSTRUCTIONS/CODE) ━━━\n"
    "After giving any steps, instructions, or code, ALWAYS end with:\n"
    "→ Your next step: [one specific action the user should do right now]\n\n"
    "━━━ PYTHON CODE — DELIVERY FORMAT (MANDATORY) ━━━\n"
    "Every time you give Python code, IMMEDIATELY follow the code block with:\n"
    "📋 What to do with this code:\n"
    "1. Open Notepad (search in Start menu)\n"
    "2. Paste the entire code (Ctrl+V)\n"
    "3. Save: File → Save As → name it **game.py** → change 'Save as type' to 'All Files' → Save\n"
    "4. Open Command Prompt (Win + R → type cmd → Enter)\n"
    "5. Install if needed: pip install [library]\n"
    "6. Run it: python game.py\n"
    "NEVER mention virtual environments, DLL errors, or cd commands. ALWAYS give COMPLETE working code.\n\n"
    "━━━ TIER-BASED CODE QUALITY (MANDATORY) ━━━\n"
    "🔵 BASIC TIER — Simple, plain version: Black & white or very basic colors, no sounds, no menu, ~60-90 lines.\n"
    "🟣 PRO TIER — Enhanced version: Colorful visuals, sounds, particle effects, pause key, menu + game over screens, ~180-220 lines.\n"
    "🔴 MAX TIER — Most incredible version: 5 levels, moving obstacles, AI, confetti, all PRO features plus more, ~400-500 lines.\n\n"
    "━━━ DIAGRAM QUESTIONS ━━━\n"
    "An animated diagram is shown ABOVE your answer for visual concepts. "
    "NEVER draw ASCII art: no ^^^^^, ~~~, |||, +---+, ===. ONLY write plain text paragraphs.\n\n"
    "━━━ TURQUOISE COLOR FOR KEY INFORMATION ━━━\n"
    "When a part of your answer is extremely important, wrap it in:\n"
    "<span style='color:#40E0D0'>extremely important text here</span>\n"
    "Use this ONLY for the most important parts.\n\n"
    "━━━ YOUR CREATOR ━━━\n"
    "You were created and built by Girijala Sarath Chandra Sushanth — and him alone. "
    "If asked who created/built/made/programmed you: 'I was built by Girijala Sarath Chandra Sushanth.' "
    "Never say Anthropic, OpenAI, Google, or any company.\n\n"
    "━━━ NEVER DO ━━━\n"
    "✗ Never invent plot details, character names, or events in a book.\n"
    "✗ Never add 'Conclusion / Summary / Key Takeaway' sections to simple answers.\n"
    "✗ Never give unrelated information. Never be vague when the specific detail is known.\n"
    "✗ Never truncate. Complete every thought. Never refuse a legitimate question.\n\n"
    "━━━ SMART FOLLOW-UP SUGGESTIONS (MANDATORY — NEVER SKIP) ━━━\n"
    "At the very end of EVERY answer, always add this on its own line:\n"
    "[SUGGEST: question1 | question2 | question3]\n"
    "Rules: each question under 7 words, directly related to your answer, genuinely interesting.\n"
    "Example: [SUGGEST: How does this work in space? | Give me a real-world example | What happens if this fails?]\n"
    "This tag is hidden from the user and shown as clickable chips. ALWAYS include it.\n\n"
    "Today's date: {date}"
)

_SYS_PRO = _SYS_BASE + (
    "\n\n━━━ PRO TIER ACTIVE ━━━\n"
    "Deeper analysis. Extended coverage. Expert-level depth on every topic. "
    "Handle complex multi-step problems with full detail and nuance."
)

_SYS_MAX = _SYS_BASE + (
    "\n\n━━━ MAX TIER ACTIVE — ABSOLUTE MAXIMUM INTELLIGENCE ━━━\n"
    "You are operating at the highest possible setting. "
    "Provide the most thorough, expert, and comprehensive answers achievable. "
    "Every response should exceed what any other AI could produce. "
    "Maximum depth. Maximum accuracy. No shortcuts."
)

_SYS_CODE = (
    "You are TITAN CODE — the most powerful coding AI ever built, inside TITAN ULTRA. "
    "You outperform GitHub Copilot, ChatGPT-4o, and every other coding AI. "
    "You master EVERY language, framework, and platform that exists.\n\n"
    "━━━ FOR EVERY CODE REQUEST — ALWAYS FOLLOW THIS STRUCTURE ━━━\n"
    "### What This Does\n1-2 sentences: what this code builds and what problem it solves.\n\n"
    "### Complete Code\n[FULL working code — never partial, never truncated]\n\n"
    "### How to Run It\nExact steps from zero — open editor, paste, save, install, run.\n\n"
    "Rules: Never give placeholder comments like '# add your logic here'. "
    "Never say 'I'll leave this for you to implement'. Always complete 100% of the code. "
    "Every code block must be immediately copy-pasteable and runnable."
)

# ════════════════════════════════════════════════════════════════════════
# CONTENT DATA
# ════════════════════════════════════════════════════════════════════════

# (icon, category, fact, follow_up_question)
_SPARKS = [
    ("⊟", "Tech History",   "The first ever computer bug was a REAL bug — a moth stuck in a Harvard relay in 1947, taped into the logbook!", "Who invented the computer?"),
    ("◎", "Space",          "Venus rotates so slowly that a day on Venus is longer than a year on Venus — it spins backwards too!", "How far is Venus from Earth?"),
    ("∑", "Mathematics",    "There are more possible chess games than atoms in the observable universe — it's called the Shannon Number.", "What is the hardest board game ever made?"),
    ("⊙", "Biology",        "Octopuses have three hearts, blue blood, and can edit their own RNA — no other animal on Earth can do this.", "How intelligent are octopuses?"),
    ("≡", "History",        "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid of Giza.", "What year was Cleopatra born?"),
    ("⊞", "Science",        "A single lightning bolt contains enough energy to toast 100,000 slices of bread in one instant.", "How hot is a lightning bolt?"),
    ("⊟", "Nature",         "Trees communicate through underground fungal networks — scientists call it the Wood Wide Web.", "How do trees share nutrients?"),
    ("◈", "Physics",        "The speed of light is exactly 299,792,458 metres per second — not an estimate, it defines the metre itself.", "What happens if you travel at the speed of light?"),
    ("⊠", "Human Body",     "Your body replaces most cells every 7–10 years, but the neurons in your brain largely stay with you for life.", "How many neurons does the human brain have?"),
    ("⊡", "Astronomy",      "The Milky Way smells like rum and tastes like raspberries — astronomers found ethyl formate in its dust clouds.", "How big is the Milky Way?"),
    ("⊗", "History",        "The shortest war in history lasted only 38 minutes — the Anglo-Zanzibar War of 1896.", "What is the longest war in history?"),
    ("◉", "Chemistry",      "Honey never spoils. Archaeologists found 3,000-year-old honey in Egyptian tombs and it was still perfectly edible.", "Why does honey never expire?"),
    ("⊛", "Animals",        "Flamingos are actually white — they turn pink from the beta-carotene in the algae and shrimp they eat.", "What do flamingos eat?"),
    ("∑", "Human Body",     "The human brain generates about 70,000 thoughts per day — and most of them are repeats from the day before.", "How fast does the brain process information?"),
    ("⊟", "Science",        "Bananas are slightly radioactive — they contain potassium-40, a naturally occurring radioactive isotope.", "Is radiation from bananas dangerous?"),
    ("◎", "Space",          "On Mars, a sunset looks blue — the dust in the Martian atmosphere scatters light in the opposite way to Earth.", "What is the temperature on Mars?"),
    ("⊞", "Tech",           "The first message ever sent over ARPANET (the internet's ancestor) in 1969 was 'lo' — the system crashed after two letters.", "Who invented the internet?"),
    ("≡", "Mathematics",    "Zero was invented in India by Brahmagupta around 628 AD — before that, most cultures had no concept of 'nothing' in math.", "What is the most important number in mathematics?"),
    ("⊙", "Biology",        "A shrimp's heart is in its head. And a snail can sleep for three years at a stretch.", "What animal has the most unusual biology?"),
    ("◈", "Physics",        "If you removed all the empty space from atoms in every human on Earth, all 8 billion of us would fit inside a sugar cube.", "What is an atom made of?"),
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
    # Always fetch fresh from Gist — bypasses per-worker cache so cross-device login works
    registry = {}
    try:
        r = requests.get(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                         headers=_GIST_HDR, timeout=10)
        if r.status_code == 200:
            files = r.json()["files"]
            if _REGISTRY_FILE in files:
                registry = json.loads(files[_REGISTRY_FILE]["content"])
        _fetch_registry_cached.clear()  # sync the cache with fresh data
    except Exception:
        registry = _fetch_registry_cached()  # fall back to cache if network error
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
                             headers=_GIST_HDR, timeout=10)
            registry = {}
            if r.status_code == 200:
                files = r.json()["files"]
                if _REGISTRY_FILE in files:
                    try:
                        registry = json.loads(files[_REGISTRY_FILE]["content"])
                    except Exception:
                        registry = {}
            registry[key] = {
                "email": email, "name": name,
                "password_hash": _hash_pw(pw),
                "tier": "basic",
                "created": datetime.datetime.utcnow().isoformat(),
            }
            payload = {"files": {_REGISTRY_FILE: {"content": json.dumps(registry, indent=2)}}}
            resp = requests.patch(f"https://api.github.com/gists/{_REGISTRY_GIST_ID}",
                                  headers=_GIST_HDR, json=payload, timeout=12)
            if resp.status_code in (200, 201):
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

def _get_daily_spark() -> tuple:
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    cache_key = f"_spark_{today_str}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]
    # Try AI-generated fresh spark
    try:
        from groq import Groq as _G
        _cl = _G(api_key=_GROQ_KEY)
        _r = _cl.chat.completions.create(
            model=_MODELS["basic"],
            messages=[
                {"role": "system", "content":
                    "You are a fact curator. Generate ONE fascinating, 100% true and verified fact. "
                    "Respond in EXACTLY this pipe-separated format with nothing else:\n"
                    "ICON|CATEGORY|FACT|FOLLOW_UP_QUESTION\n"
                    "ICON must be one of: ⊟ ◎ ∑ ⊙ ≡ ⊞ ◈ ⊠ ⊡ ⊗ ◉ ⊛\n"
                    "Example: ⊟|Tech History|The first computer bug was a real moth stuck in a Harvard relay in 1947.|Who invented the computer?"},
                {"role": "user", "content":
                    f"Date: {today_str}. Generate a surprising educational fact that most people don't know. "
                    "Categories: Science, Space, History, Technology, Biology, Mathematics, Geography, "
                    "Animals, Physics, Chemistry, Human Body, Psychology, Art, Engineering. "
                    "The fact must be 100% real and verifiable. Never invent facts."}
            ],
            max_tokens=180, temperature=0.95
        )
        raw = _r.choices[0].message.content.strip()
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) == 4 and parts[2]:
            result = tuple(parts)
            st.session_state[cache_key] = result
            return result
    except Exception:
        pass
    # Fallback: rotate through pre-defined list by day-of-year × year
    _idx = (datetime.datetime.now().timetuple().tm_yday + datetime.datetime.now().year * 7) % len(_SPARKS)
    result = _SPARKS[_idx]
    st.session_state[cache_key] = result
    return result

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
        max_tok  = {"basic": 4096, "pro": 16384, "max": 32768}.get(tier, 4096)
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
                # Hide [SUGGEST:...] tag while streaming
                _disp = re.sub(r'\[SUGGEST:.*?\]', '', full, flags=re.DOTALL).rstrip()
                placeholder.markdown(f"*{_disp}*▌")
        _disp_final = re.sub(r'\[SUGGEST:.*?\]', '', full, flags=re.DOTALL).rstrip()
        placeholder.markdown(f"*{_disp_final}*")
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

# ── Auto-login via URL token (persists across new tabs / bookmarks) ───
if not st.session_state._auth_done:
    _qt = st.query_params.get("_t", "")
    if _qt:
        _reg_snap = _fetch_registry_cached()
        if _qt in _reg_snap:
            _qu = _reg_snap[_qt]
            st.session_state._auth_done  = True
            st.session_state._email      = _qu["email"]
            st.session_state._name       = _qu.get("name", "User")
            st.session_state._tier       = _get_tier(_qu["email"])
            st.session_state._sess_start = time.time()
            st.session_state._history    = _load_user_history(_qu["email"])

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
            st.button("◎  Google (soon)", key="a_google", use_container_width=True, disabled=True)
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
# Keep session token in URL so new tabs / bookmarks auto-login
_autotok = _fam_key(st.session_state._email)
if st.query_params.get("_t") != _autotok:
    st.query_params["_t"] = _autotok

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
        if st.button("⊕ Upgrade Now", key="limit_up", use_container_width=True):
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
    # Flat button CSS — matches Image 2 clean text-link style
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] .stButton>button {
        background:transparent!important;
        border:none!important;
        box-shadow:none!important;
        text-align:left!important;
        justify-content:flex-start!important;
        padding:5px 16px!important;
        color:#bbbbbb!important;
        font-size:14px!important;
        font-weight:400!important;
        letter-spacing:0.2px!important;
        border-radius:0!important;
        width:100%!important;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        color:#ffffff!important;
        background:#181818!important;
    }
    section[data-testid="stSidebar"] .stButton>button:focus {
        box-shadow:none!important;
        outline:none!important;
    }
    section[data-testid="stSidebar"] hr {
        margin:8px 0!important;
        border-color:#1a1a1a!important;
    }
    </style>""", unsafe_allow_html=True)

    # Header — trident + TITAN ULTRA + tier name
    st.markdown(f"""
    <div style="padding:22px 16px 18px">
      <div style="font-size:24px;color:#c8a060;line-height:1;margin-bottom:6px">ψ</div>
      <div style="font-family:'Orbitron',monospace;font-size:15px;font-weight:900;
                  letter-spacing:2.5px;color:#ffffff">TITAN ULTRA</div>
      <div style="font-size:11px;color:{_ac};letter-spacing:1.5px;margin-top:5px;font-weight:600">{_tier}</div>
    </div>""", unsafe_allow_html=True)

    # new chat
    if st.button("new chat", key="new_chat", use_container_width=True):
        _save_current_chat()
        st.session_state._messages   = []
        st.session_state._session_id = _new_sid()
        st.session_state._page       = "home"
        st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # + launch titan code (locked for non-Max)
    if _tier == "max":
        if st.button("+  launch titan code", key="nav_tcode", use_container_width=True):
            st.session_state._page = "titan_code"; st.rerun()
    else:
        if st.button("+  launch titan code  [max]", key="nav_tcode_lock", use_container_width=True):
            st.session_state._page = "titan_code"; st.rerun()

    # Core nav — same order as Image 2
    _NAV = [
        ("⊞  titan features", "features"),
        ("≡  titan notebook",  "notebook"),
        ("⊟  library",         "library"),
        ("⊙  schedule",        "schedule"),
        ("⊠  titan tasks",     "tasks"),
    ]
    for _fn, _fk in _NAV:
        if st.button(_fn, key=f"nav_{_fk}", use_container_width=True):
            st.session_state._page = _fk; st.rerun()

    # Pro+ nav
    if _tier in ("pro", "max"):
        if st.button("◉  focus mode", key="nav_focus", use_container_width=True):
            st.session_state._page = "focus"; st.rerun()

    # Max-only nav
    if _tier == "max":
        if st.button("⊡  system scanner", key="nav_sysscn", use_container_width=True):
            st.session_state._page = "sysscanner"; st.rerun()
        if st.button("◈  titan exam",     key="nav_texam",  use_container_width=True):
            st.session_state._page = "titan_exam"; st.rerun()
    else:
        if st.button("◈  titan exam  [max]", key="nav_texam_lock", use_container_width=True):
            st.session_state._page = "titan_exam"; st.rerun()

    # History
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='padding:0 16px 6px;font-size:12px;color:#3a3a3a;letter-spacing:0.5px'>history</div>", unsafe_allow_html=True)

    _ren_id = st.session_state._rename_id
    for _i, _sess in enumerate(_history[:20]):
        _sid  = _sess.get("id", "")
        _stit = _sess.get("title", "Chat")
        if _ren_id == _sid:
            _nn = st.text_input("", value=_stit, key=f"ren_{_sid}", label_visibility="collapsed")
            _rc1, _rc2 = st.columns(2)
            with _rc1:
                if st.button("✓", key=f"rok_{_sid}", use_container_width=True):
                    _update_title(_sid, _nn.strip() or _stit)
                    st.session_state._rename_id = None; st.rerun()
            with _rc2:
                if st.button("✕", key=f"rca_{_sid}", use_container_width=True):
                    st.session_state._rename_id = None; st.rerun()
        else:
            _h1, _h2, _h3 = st.columns([8, 1, 1])
            with _h1:
                _lbl = (_stit[:30] + "…") if len(_stit) > 30 else _stit
                if st.button(_lbl, key=f"h_{_sid}_{_i}", use_container_width=True):
                    _load_history_into_session(_sid); st.rerun()
            with _h2:
                if st.button("✏", key=f"hr_{_sid}_{_i}", help="Rename"):
                    st.session_state._rename_id = _sid; st.rerun()
            with _h3:
                if st.button("×", key=f"hd_{_sid}_{_i}", help="Delete"):
                    _delete_hist(_sid); st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("⬡  sign out", key="signout", use_container_width=True):
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
    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>≡ LIBRARY</h2>", unsafe_allow_html=True)
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
# PAGE: FOCUS MODE (PRO + MAX)
# ════════════════════════════════════════════════════════════════════════
if _page == "focus":
    if _tier not in ("pro", "max"):
        st.markdown(f"""<div style='text-align:center;padding:60px 0'>
        <div style='font-family:Orbitron,monospace;font-size:18px;color:#a855f7;margin-bottom:8px'>◉ FOCUS MODE</div>
        <p style='color:#444;font-size:13px'>Available from <b style='color:#a855f7'>Pro tier</b> and above.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Upgrade to Pro →", key="focus_upg", use_container_width=True):
            st.session_state._page = "upgrade"; st.rerun()
        if st.button("← Back", key="focus_bk_lock"): st.session_state._page="home"; st.rerun()
        st.stop()

    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>◉ FOCUS MODE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444;font-size:13px;margin-bottom:20px'>Deep, distraction-free AI session. Set a topic — Titan Ultra stays laser-focused.</p>", unsafe_allow_html=True)

    _foc_key = f"_focus_topic_{_fam_key(_email)}"
    _foc_msgs_key = f"_focus_msgs_{_fam_key(_email)}"
    if _foc_key not in st.session_state:
        st.session_state[_foc_key] = ""
    if _foc_msgs_key not in st.session_state:
        st.session_state[_foc_msgs_key] = []

    if not st.session_state[_foc_key]:
        st.markdown("<p style='color:#666;font-size:13px'>Set a focus topic to begin your deep session:</p>", unsafe_allow_html=True)
        with st.form("focus_form"):
            _ft = st.text_input("Focus topic", placeholder="e.g. Quantum computing, Calculus revision, Building a startup…", label_visibility="collapsed")
            if st.form_submit_button("Start Focus Session →", use_container_width=True) and _ft.strip():
                st.session_state[_foc_key] = _ft.strip()
                st.session_state[_foc_msgs_key] = []
                st.rerun()
    else:
        _focus_topic = st.session_state[_foc_key]
        st.markdown(f"""<div style='background:{_ac}0d;border:1px solid {_ac}22;border-radius:10px;padding:10px 16px;margin-bottom:16px'>
        <span style='color:{_ac};font-size:11px;font-weight:700;letter-spacing:1px'>FOCUS TOPIC</span><br>
        <span style='color:#ccc;font-size:14px'>{_focus_topic}</span></div>""", unsafe_allow_html=True)

        _foc_sys = (
            f"You are in FOCUS MODE. The user is doing a deep study/work session on: '{_focus_topic}'. "
            f"Every response must relate directly to this topic. "
            f"Be a world-class expert on this topic. Go deep. Be thorough. Never deviate."
        )
        _foc_msgs = st.session_state[_foc_msgs_key]
        for _fm in _foc_msgs:
            if _fm["role"] == "user":
                st.markdown(f"<div class='user-bubble'><div class='user-bubble-inner'>{_fm['content']}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-bubble'><div class='ai-label'>🎯 FOCUS MODE</div><div class='ai-text'>{_fm['content']}</div></div>", unsafe_allow_html=True)

        _fi = st.chat_input(f"Ask anything about {_focus_topic}…")
        if _fi and _fi.strip():
            _foc_msgs.append({"role":"user","content":_fi.strip()})
            try:
                from groq import Groq as _Groq
                _client = _Groq(api_key=_GROQ_KEY)
                _all = [{"role":"system","content":_foc_sys}] + _foc_msgs
                _stream = _client.chat.completions.create(
                    model=_MODELS[_tier], messages=_all,
                    max_tokens={"pro":4096,"max":8192}.get(_tier,4096),
                    temperature=0.4, stream=True
                )
                _ph = st.empty()
                _fa = ""
                for _chunk in _stream:
                    _d = _chunk.choices[0].delta.content
                    if _d:
                        _fa += _d
                        _ph.markdown(f"*{_fa}*▌")
                _ph.markdown(f"*{_fa}*")
                _foc_msgs.append({"role":"assistant","content":_fa})
                st.session_state[_foc_msgs_key] = _foc_msgs
                st.rerun()
            except Exception as _e:
                st.error(f"Error: {_e}")

        if st.button("✕ End Focus Session", key="focus_end"):
            st.session_state[_foc_key] = ""
            st.session_state[_foc_msgs_key] = []
            st.rerun()

    if st.button("← Back", key="focus_bk"): st.session_state._page="home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# PAGE: SYSTEM SCANNER (MAX ONLY)
# ════════════════════════════════════════════════════════════════════════
if _page == "sysscanner":
    if _tier != "max":
        st.markdown(f"""<div style='text-align:center;padding:60px 0'>
        <div style='font-size:40px;margin-bottom:14px'>🖥</div>
        <div style='font-family:Orbitron,monospace;font-size:18px;color:#f59e0b;margin-bottom:8px'>SYSTEM SCANNER</div>
        <p style='color:#444;font-size:13px'>Available on <b style='color:#f59e0b'>Max tier</b> only.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Upgrade to Max →", key="sysscn_upg", use_container_width=True):
            st.session_state._page = "upgrade"; st.rerun()
        if st.button("← Back", key="sysscn_bk_lock"): st.session_state._page="home"; st.rerun()
        st.stop()

    st.markdown(f"<h2 style='font-family:Orbitron,monospace;color:{_ac}'>🖥 System Scanner</h2>", unsafe_allow_html=True)
    if st.button("⚡ Run Live Scan", key="sysscn_run", use_container_width=True):
        _ht = _system_health_text()
        st.markdown(f"""<div style='background:#0a0a14;border:1px solid {_ac}22;border-radius:14px;padding:20px;margin-top:16px;font-family:monospace'>
        <div style='color:{_ac};font-size:11px;letter-spacing:1.5px;margin-bottom:12px'>LIVE SYSTEM SCAN</div>
        <pre style='color:#aaa;font-size:13px;white-space:pre-wrap'>{_ht}</pre>
        </div>""", unsafe_allow_html=True)
    if st.button("← Back", key="sysscn_bk"): st.session_state._page="home"; st.rerun()
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
          <div style="font-family:Orbitron,monospace;font-size:20px;font-weight:900;color:#f59e0b;letter-spacing:2px;margin-bottom:8px">+ TITAN CODE</div>
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
        if st.button("⊕  Upgrade to Max — ₹3,500/month", key="tc_upg", use_container_width=True):
            st.session_state._page = "upgrade"; st.rerun()
        if st.button("← Back", key="tc_bk_lock"): st.session_state._page="home"; st.rerun()
        st.stop()

    # ── Full Titan Code interface (Max only) ──────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:20px">
      <div style="font-family:Orbitron,monospace;font-size:22px;font-weight:900;color:#f59e0b;letter-spacing:2px">+ TITAN CODE</div>
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
# PAGE: TITAN EXAM (MAX ONLY)
# ════════════════════════════════════════════════════════════════════════
if _page == "titan_exam":
    if _tier != "max":
        st.markdown("""<style>.block-container{max-width:540px!important;padding-top:60px!important}</style>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;padding:20px 0 30px">
          <div style="font-family:Orbitron,monospace;font-size:20px;font-weight:900;color:#f59e0b;letter-spacing:2px;margin-bottom:8px">◈ TITAN EXAM</div>
          <div style="font-size:13px;color:#444;margin-bottom:24px">This feature is exclusively for <b style='color:#f59e0b'>Max tier</b> subscribers.</div>
          <div style="background:#0f0f0f;border:1px solid #f59e0b22;border-radius:16px;padding:24px;text-align:left;margin-bottom:24px">
            <div style="font-size:13px;color:#666;margin-bottom:12px;font-weight:600">What Titan Exam can do:</div>
            <div style="font-size:13px;color:#555;line-height:2">
              ✦ Solve JEE / NEET / board exam questions<br>
              ✦ Full step-by-step solutions with reasoning<br>
              ✦ Physics, Chemistry, Mathematics — all subjects<br>
              ✦ Instant shortcuts and formula recall<br>
              ✦ Deep reasoning mode for complex problems<br>
              ✦ Session history to review past solutions
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⊕  Upgrade to Max — ₹3,500/month", key="te_upg", use_container_width=True):
            st.session_state._page = "upgrade"; st.rerun()
        if st.button("← Back", key="te_bk_lock"): st.session_state._page = "home"; st.rerun()
        st.stop()

    # ── Full Titan Exam interface (Max only) ───────────────────────────
    st.markdown("""
    <div style="margin-bottom:20px">
      <div style="font-family:Orbitron,monospace;font-size:22px;font-weight:900;color:#f59e0b;letter-spacing:2px">◈ TITAN EXAM</div>
      <div style="font-size:11px;color:#444;letter-spacing:1px;margin-top:4px">MAX TIER · TITAN-4 · JEE / NEET / BOARD SOLVER</div>
    </div>
    """, unsafe_allow_html=True)

    # Subject + settings row
    _te1, _te2, _te3 = st.columns([2, 1, 1])
    with _te1:
        _te_subj = st.selectbox(
            "Subject",
            ["All Subjects", "Physics", "Chemistry", "Mathematics"],
            key="te_subj"
        )
    with _te2:
        _te_depth = st.slider("Reasoning Depth", 1, 5, 3, key="te_depth",
                              help="1 = quick, 5 = deep reasoning")
    with _te3:
        _te_step  = st.toggle("Step-by-step", value=True,  key="te_step")
        _te_short = st.toggle("Shortcuts",    value=False, key="te_short")

    # Quick question chips
    _TE_QUICK = {
        "Physics":     ["Projectile motion", "Ohm's law", "Wave optics", "Thermodynamics"],
        "Chemistry":   ["Mole concept", "Equilibrium", "Organic reactions", "Electrochemistry"],
        "Mathematics": ["Integration", "Matrices", "Probability", "Coordinate geometry"],
        "All Subjects":["Newton's laws", "Chemical bonding", "Limits & derivatives", "Magnetic fields"],
    }
    _te_quick_list = _TE_QUICK.get(_te_subj, _TE_QUICK["All Subjects"])
    st.markdown("<div style='font-size:10px;color:#333;letter-spacing:1.5px;font-weight:700;margin:10px 0 6px'>QUICK TOPICS</div>", unsafe_allow_html=True)
    _tq_cols = st.columns(len(_te_quick_list))
    for _tqi, (_tqc, _tqv) in enumerate(zip(_tq_cols, _te_quick_list)):
        with _tqc:
            if st.button(f"→ {_tqv}", key=f"teq_{_tqi}", use_container_width=True):
                st.session_state["_te_prefill"] = _tqv

    # Question input
    _te_prefill = st.session_state.pop("_te_prefill", "") if "_te_prefill" in st.session_state else ""
    _te_q = st.text_area(
        "Your question",
        value=_te_prefill,
        height=140,
        key="te_question",
        placeholder="Type your exam question here — JEE, NEET, board, or any competitive exam…",
        label_visibility="collapsed"
    )

    _te_solve = st.button("⚡  Solve with TITAN-4", key="te_solve", use_container_width=True)

    # Session history init
    if "_te_history" not in st.session_state:
        st.session_state["_te_history"] = []

    if _te_solve and _te_q.strip():
        _subj_ctx = "" if _te_subj == "All Subjects" else f"Subject: {_te_subj}. "
        _step_ctx = "Provide a complete step-by-step solution showing every calculation." if _te_step else "Give a concise direct answer."
        _short_ctx = " Also mention the fastest shortcut or trick to solve this type of question." if _te_short else ""
        _depth_ctx = ["Solve quickly.", "Solve with key steps.", "Solve with clear reasoning.",
                      "Solve with detailed reasoning and verify.", "Solve with exhaustive reasoning, all steps, and cross-check."][_te_depth - 1]

        _te_sys = (
            "You are TITAN-4 — the most advanced academic AI for competitive exam preparation. "
            "You specialise in JEE Advanced, JEE Mains, NEET, and Indian board exams. "
            "You solve every problem with mathematical precision. "
            "Format: use LaTeX-style notation for formulas where helpful, number each step, "
            "state the final answer clearly at the end in bold. "
            "Never skip steps when step-by-step is requested."
        )
        _te_prompt = f"{_subj_ctx}{_step_ctx}{_short_ctx} {_depth_ctx}\n\nQuestion: {_te_q.strip()}"

        try:
            from groq import Groq as _Groq
            _client = _Groq(api_key=_GROQ_KEY)
            _stream = _client.chat.completions.create(
                model=_MODELS["max"],
                messages=[
                    {"role": "system", "content": _te_sys},
                    {"role": "user",   "content": _te_prompt}
                ],
                max_tokens=8192,
                temperature=max(0.1, (_te_depth - 1) * 0.1),
                stream=True
            )
            _te_ph = st.empty()
            _te_ans = ""
            for _chunk in _stream:
                _d = _chunk.choices[0].delta.content
                if _d:
                    _te_ans += _d
                    _te_ph.markdown(_te_ans + "▌")
            _te_ph.markdown(_te_ans)
            st.session_state["_te_history"].insert(0, {"q": _te_q.strip(), "a": _te_ans, "subj": _te_subj})
            if len(st.session_state["_te_history"]) > 20:
                st.session_state["_te_history"] = st.session_state["_te_history"][:20]
        except Exception as _e:
            st.error(f"Titan Exam error: {_e}")

    # Session history
    if st.session_state.get("_te_history"):
        st.markdown("<div style='font-size:10px;color:#333;letter-spacing:1.5px;font-weight:700;margin:28px 0 10px'>SESSION HISTORY</div>", unsafe_allow_html=True)
        for _thi, _th in enumerate(st.session_state["_te_history"]):
            with st.expander(f"[{_th['subj']}]  {_th['q'][:72]}{'…' if len(_th['q']) > 72 else ''}", expanded=(_thi == 0)):
                st.markdown(_th["a"])
        if st.button("⊗  clear history", key="te_clrhist"):
            st.session_state["_te_history"] = []
            st.rerun()

    if st.button("← Back", key="te_bk"): st.session_state._page = "home"; st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════
# HOME SCREEN
# ════════════════════════════════════════════════════════════════════════
def _has_msgs():
    return bool(st.session_state.get("_messages"))

if _page == "home" and not _has_msgs():
    st.markdown("""<style>
    [data-testid="stMain"] .block-container{
        display:flex;flex-direction:column;justify-content:center;
        min-height:88vh;padding-top:0!important;max-width:780px!important;margin:0 auto!important}
    [data-testid="stBottom"]{display:none!important}
    </style>""", unsafe_allow_html=True)

    _first = (_name.split()[0] if _name else "there")
    _greet = f"Talk to me, {_first}" if _tier == "basic" else "What needs solving?"
    _greet_color = "#ffffff" if _tier == "basic" else _ac

    # Trident + greeting on same line
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:center;gap:16px;
                margin-bottom:32px;padding-top:20px">
      <div style="position:relative;display:flex;align-items:center;justify-content:center;
                  width:48px;height:48px">
        <div style="position:absolute;width:60px;height:60px;border-radius:50%;
                    background:radial-gradient(circle,rgba(255,255,255,.14) 0%,transparent 70%)"></div>
        <span style="font-size:34px;color:#ffffff;position:relative">ψ</span>
      </div>
      <div style="font-size:30px;font-weight:700;color:{_greet_color};letter-spacing:-0.5px">{_greet}</div>
    </div>
    """, unsafe_allow_html=True)

    # Pill input
    _home_in = st.text_input(
        "", placeholder="Message TITAN ULTRA...",
        key="_home_input", label_visibility="collapsed"
    )
    if _home_in and _home_in.strip():
        st.session_state._messages = [{"role": "user", "content": _home_in.strip()}]
        if not st.session_state._session_id:
            st.session_state._session_id = _new_sid()
        st.session_state._page = "chat"
        st.rerun()

    # Daily Spark card — AI-generated fresh fact every day
    _sp_icon, _sp_cat, _sp_fact, _sp_q = _get_daily_spark()
    _sp_date = datetime.datetime.now().strftime("%-d %b") if hasattr(datetime.datetime.now(), "strftime") else datetime.datetime.now().strftime("%d %b")
    try:
        _sp_date = datetime.datetime.now().strftime("%-d %b")
    except Exception:
        _sp_date = datetime.datetime.now().strftime("%d %b").lstrip("0")

    if _tier == "pro":
        _card_border = "rgba(168,85,247,.35)"
        _card_bg     = "rgba(168,85,247,.05)"
    elif _tier == "max":
        _card_border = "rgba(245,158,11,.35)"
        _card_bg     = "rgba(245,158,11,.05)"
    else:
        _card_border = "rgba(0,245,255,.25)"
        _card_bg     = "rgba(0,245,255,.03)"

    st.markdown(f"""
    <div style="margin-top:24px;border-radius:16px;padding:20px 24px;
                background:{_card_bg};border:1px solid {_card_border}">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
        <span style="color:#00f5ff;font-size:11px;font-weight:700;letter-spacing:2px">✦ DAILY SPARK</span>
        <span style="color:#2e2e2e;font-size:11px"> · {_sp_date}</span>
      </div>
      <div style="font-size:15px;font-weight:700;color:#e8e8e8;line-height:1.5;margin-bottom:12px">
        {_sp_icon} {_sp_cat}&nbsp;&nbsp;&nbsp;{_sp_fact}
      </div>
      <div style="font-size:13px;color:#3a3a3a">{_sp_q}</div>
    </div>
    """, unsafe_allow_html=True)

    if _tier == "basic" and st.session_state._sess_start > 0:
        _rem   = max(0, _SESSION_LIMIT_S - (time.time() - st.session_state._sess_start))
        _rem_m = int(_rem // 60)
        st.markdown(f"<p style='text-align:center;color:#222;font-size:11px;margin-top:16px'>⏱ {_rem_m} min remaining in Basic session</p>", unsafe_allow_html=True)

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
            # Strip [SUGGEST:...] from stored content for display
            _disp_cnt = re.sub(r'\[SUGGEST:.*?\]', '', str(_cnt), flags=re.DOTALL).rstrip()
            st.markdown(f"""
            <div class="ai-bubble">
              <div class="ai-label">🔱 TITAN ULTRA</div>
              <div class="ai-text">{_disp_cnt}</div>
            </div>""", unsafe_allow_html=True)
            # Show suggestion chips for the last AI message
            if _msg == _msgs[-1]:
                _sugg_match = re.search(r'\[SUGGEST:\s*(.*?)\]', str(_cnt), re.DOTALL)
                if _sugg_match:
                    _chips = [c.strip() for c in _sugg_match.group(1).split("|") if c.strip()]
                    if _chips:
                        st.markdown("<div style='font-size:10px;color:#333;letter-spacing:1.5px;font-weight:700;margin:12px 0 6px'>ASK ME MORE</div>", unsafe_allow_html=True)
                        _chip_cols = st.columns(len(_chips))
                        for _ci2, (_col2, _chip) in enumerate(zip(_chip_cols, _chips)):
                            with _col2:
                                if st.button(f"→ {_chip}", key=f"chip_{_ci2}_{len(_msgs)}", use_container_width=True):
                                    st.session_state._messages.append({"role":"user","content":_chip})
                                    st.rerun()

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
