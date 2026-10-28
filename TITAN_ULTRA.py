# TITAN_VERSION: 82
import streamlit as st
from groq import Groq
import requests, io, re, random as _random

st.set_page_config(page_title="TITAN ULTRA", page_icon="🔱",
                   layout="wide", initial_sidebar_state="expanded")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@keyframes tridentGlow {
    0%   {filter:hue-rotate(0deg)   brightness(2) saturate(3) drop-shadow(0 0 18px #ff4444)}
    17%  {filter:hue-rotate(60deg)  brightness(2) saturate(3) drop-shadow(0 0 18px #ffaa00)}
    33%  {filter:hue-rotate(120deg) brightness(2) saturate(3) drop-shadow(0 0 18px #44ff44)}
    50%  {filter:hue-rotate(180deg) brightness(2) saturate(3) drop-shadow(0 0 18px #00eeff)}
    67%  {filter:hue-rotate(240deg) brightness(2) saturate(3) drop-shadow(0 0 18px #4488ff)}
    83%  {filter:hue-rotate(300deg) brightness(2) saturate(3) drop-shadow(0 0 18px #ff44ff)}
    100% {filter:hue-rotate(360deg) brightness(2) saturate(3) drop-shadow(0 0 18px #ff4444)}
}

html, body, [data-testid="stAppViewContainer"] {
    background:#0d0d0d !important; color:#e8e8e8 !important;
}
[data-testid="stSidebar"] {
    background:#111111 !important;
    border-right:1px solid #2a2a2a !important;
    min-width:260px !important;
}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,[data-testid="stSidebar"] li { color:#e8e8e8 !important; }
.stButton>button {
    background:#1a1a1a !important;
    color:#e8e8e8 !important; border:1px solid #2a2a2a !important;
    border-radius:10px !important; transition:all .2s !important;
}
.stButton>button:hover {
    background:#242424 !important;
    transform:translateY(-1px) !important;
}
[data-testid="stSidebar"] .stButton { width:100% !important; }
[data-testid="stSidebar"] .stButton>button {
    font-size:16px !important;
    padding:10px 14px !important;
    min-height:0 !important;
    height:auto !important;
    line-height:1.4 !important;
    animation:none !important;
    background:transparent !important;
    color:#e8e8e8 !important;
    border:none !important;
    box-shadow:none !important;
    white-space:normal !important;
    overflow:hidden !important;
    text-align:left !important;
    border-radius:8px !important;
    font-weight:400 !important;
    letter-spacing:0 !important;
    width:100% !important;
}
[data-testid="stSidebar"] .stButton>button:hover {
    background:rgba(255,255,255,0.08) !important;
    color:#ffffff !important;
    border:none !important;
    box-shadow:none !important;
    transform:none !important;
}
[data-testid="stSidebar"] .stButton>button > div {
    text-align:left !important;
    justify-content:flex-start !important;
    width:100% !important;
    display:flex !important;
    align-items:center !important;
}
[data-testid="stSidebar"] .stButton>button > div > p {
    text-align:left !important;
    margin:0 !important;
    width:100% !important;
}
/* ── Sidebar compact: kill all vertical gaps ── */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap:1px !important;
}
[data-testid="stSidebar"] .element-container {
    margin-top:0 !important;
    margin-bottom:0 !important;
}
[data-testid="stSidebar"] .stMarkdown { margin:0 !important; }
[data-testid="stSidebar"] .stMarkdown p { margin:0 !important; padding:0 !important; }
/* Inline code: blue instead of green, plain look — code blocks stay unchanged */
[data-testid="stChatMessage"] p code,
[data-testid="stChatMessage"] li code,
[data-testid="stChatMessage"] td code,
.stMarkdown p code,
.stMarkdown li code,
.stMarkdown td code {
    background: rgba(59,130,246,0.12) !important;
    color: #93c5fd !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    border-radius: 4px !important;
    padding: 1px 5px !important;
    font-size: 0.85em !important;
    font-family: inherit !important;
}
[data-testid="stSidebar"] hr {
    margin:3px 0 !important;
    border-width:1px 0 0 !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    margin:0 !important;
    background:transparent !important;
    border:none !important;
    animation:none !important;
    border-radius:0 !important;
    box-shadow:none !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    padding:4px 8px !important;
    min-height:0 !important;
    font-size:0.72rem !important;
}
[data-testid="stSidebar"] .stCheckbox { margin:0 !important; }
[data-testid="stSidebar"] [data-testid="stTextInput"] { margin:0 !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] { margin:0 !important; }
[data-testid="stSidebar"] .stFileUploader { margin:0 !important; }
[data-testid="stSidebar"] .stColumns { gap:4px !important; }
/* Sidebar — zero top padding so TITAN ULTRA touches the very top */
section[data-testid="stSidebar"] > div:first-child {
    padding-top:0 !important;
    padding-bottom:0 !important;
    margin-top:0 !important;
}
section[data-testid="stSidebar"] > div > div {
    padding-top:0 !important;
    margin-top:0 !important;
}
[data-testid="stSidebarContent"] {
    padding-top:0 !important;
    margin-top:0 !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    padding-top:0 !important;
    margin-top:0 !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child {
    padding-top:0 !important;
    margin-top:0 !important;
}
/* ── Hide both avatars ── */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: none !important;
}
[data-testid="stChatMessage"] {
    background:transparent !important;
    border:none !important;
    border-bottom:1px solid #1a1a1a !important;
    border-radius:0 !important;
    margin:2px 0 !important;
    padding:10px 0 !important;
}
/* Use full available width — no wasted space on left/right */
section[data-testid="stMain"] .block-container {
    max-width:100% !important;
    padding-left:1.5rem !important;
    padding-right:1.5rem !important;
}
[data-testid="stChatInput"] textarea {
    background:#111111 !important; color:#e8e8e8 !important;
    font-size:1rem !important; padding:20px 140px 20px 52px !important;
    min-height:56px !important; line-height:1.6 !important;
    resize:none !important;
}
[data-testid="stChatInput"] {
    background:#111111 !important; border-radius:28px !important;
    border:1px solid #2a2a2a !important; min-height:72px !important;
    padding:0 !important; position:relative !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color:#444444 !important;
    box-shadow:none !important;
    outline:none !important;
}
/* Kill Streamlit's red focus outline on ALL inputs */
[data-testid="stChatInput"] *:focus,
[data-testid="stChatInput"] *:focus-within,
[data-testid="stChatInput"] *:focus-visible {
    outline:none !important;
    box-shadow:none !important;
    border-color:#444444 !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] *:focus-within {
    outline:none !important;
    box-shadow:none !important;
    border-color:#444444 !important;
}
/* Make the bottom bar area match ChatGPT width */
[data-testid="stBottom"] .block-container {
    max-width:720px !important;
    margin:0 auto !important;
    padding-left:1rem !important;
    padding-right:1rem !important;
}
[data-testid="stSelectbox"]>div>div {
    background:#111111 !important; color:#e8e8e8 !important;
    border:1px solid #2a2a2a !important; border-radius:8px !important;
}
[data-testid="stTextInput"] input {
    background:#111111 !important; color:#e8e8e8 !important;
    border:1px solid #2a2a2a !important; border-radius:8px !important;
}
[data-testid="stExpander"] {
    background:#111111 !important; border:1px solid #2a2a2a !important;
    border-radius:10px !important;
}
hr { border-color:#2a2a2a !important; }
p, li { color:#e8e8e8 !important; }
::-webkit-scrollbar { width:6px; background:#0d0d0d; }
::-webkit-scrollbar-thumb { background:#333333; border-radius:3px; }
/* Assistant answers in italic */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] td,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] span {
    font-style: italic !important;
}
/* User messages stay normal */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] span {
    font-style: normal !important;
}
/* ── USER message: right side, dark bubble ── */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    justify-content: flex-end !important;
    align-items: flex-start !important;
    flex-direction: row !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
    background: #1e1e1e !important;
    border: none !important;
    border-radius: 18px 4px 18px 18px !important;
    padding: 10px 18px !important;
    max-width: 65% !important;
    margin-left: 0 !important;
    text-align: left !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] p {
    color: #e0e0e0 !important;
    font-style: normal !important;
}
/* ── ASSISTANT answer: full width from left, no bubble ── */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    justify-content: flex-start !important;
    align-items: flex-start !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] {
    width: 100% !important;
    max-width: 100% !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
/* Remove the line / gradient above chat bar */
[data-testid="stBottom"] > div:first-child {
    height:0 !important; min-height:0 !important; background:none !important;
}
[data-testid="stBottom"] {
    border-top:none !important; background:transparent !important;
    box-shadow:none !important;
}
[data-testid="stMain"] { scroll-behavior:smooth !important; }
html:has([data-testid="stChatMessage"]) section[data-testid="stMain"] {
    display:flex !important; flex-direction:column !important; justify-content:flex-end !important;
}
/* ── HOME SCREEN: hide sticky bottom bar & center content ── */
html:not(:has([data-testid="stChatMessage"])) [data-testid="stBottom"] {
    display:none !important;
}
html:not(:has([data-testid="stChatMessage"])) section[data-testid="stMain"] .block-container {
    padding-top:0 !important; padding-bottom:0 !important;
}
/* ── HOME SCREEN: hide ALL stButton elements (they're all internal hidden ones) ── */
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stButton"] {
    display: none !important; height: 0 !important;
    overflow: hidden !important; margin: 0 !important; padding: 0 !important;
}
/* ── HOME SCREEN: tall ChatGPT-style input ── */
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] input {
    background:#111111 !important; color:#e8e8e8 !important;
    border:1px solid #2a2a2a !important; border-radius:28px !important;
    padding:0 130px 0 52px !important; font-size:1rem !important;
    height:64px !important; box-shadow:none !important; animation:none !important;
    box-sizing:border-box !important;
}
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] [data-baseweb="input"] {
    height:64px !important; border-radius:28px !important;
    background:#111111 !important; border:none !important;
}
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] input:focus {
    border-color:#444444 !important; outline:none !important;
}
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] input::placeholder {
    color:#555555 !important;
}
/* Hide Streamlit's label gap above the home input */
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] label {
    display:none !important;
}
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] {
    margin-top:0 !important;
}
/* Center home input column at ChatGPT-like width */
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="column"]:nth-child(2) {
    max-width:min(760px, 90%) !important;
    flex:1 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Tier-based CSS (injected after main CSS so it can override) ───────────────
def _inject_tier_css():
    _tier = st.session_state.get("titan_tier", "basic")
    if _tier == "pro":
        st.markdown("""
<style>
/* ══════════════ PRO THEME — PURPLE PREMIUM ══════════════ */
@keyframes proGlow {
    0%,100% { box-shadow:0 0 12px rgba(124,58,237,0.4),0 0 24px rgba(124,58,237,0.15); }
    50%      { box-shadow:0 0 20px rgba(159,94,247,0.6),0 0 40px rgba(124,58,237,0.25); }
}
html, body, [data-testid="stAppViewContainer"] {
    background: #09071a !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f0b24 0%,#0a0818 100%) !important;
    border-right: 1px solid #3b1f6e !important;
}
[data-testid="stSidebar"] .stButton>button {
    color: #c4b5fd !important;
}
[data-testid="stSidebar"] .stButton>button:hover {
    background: rgba(124,58,237,0.18) !important;
    color: #ede9fe !important;
}
[data-testid="stChatInput"] textarea,[data-testid="stChatInput"] {
    border: 1.5px solid #7c3aed !important;
    animation: proGlow 3s ease-in-out infinite !important;
    background: #0f0b24 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #a78bfa !important;
}
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] input {
    background: #0f0b24 !important;
    border: 1.5px solid #7c3aed !important;
    box-shadow: 0 0 16px rgba(124,58,237,0.3) !important;
}
[data-testid="stChatMessage"][data-testid*="assistant"] {
    border-left: 3px solid #7c3aed !important;
    padding-left: 8px !important;
}
#titan-greeting span:last-child { color: #a78bfa !important; text-shadow: 0 0 20px rgba(167,139,250,0.5); }
::-webkit-scrollbar-thumb { background: #5b21b6 !important; border-radius: 4px !important; }
</style>
""", unsafe_allow_html=True)
    elif _tier == "max":
        st.markdown("""
<style>
/* ══════════════ MAX THEME — GOLD ULTIMATE ══════════════ */
@keyframes maxGlow {
    0%,100% { box-shadow:0 0 15px rgba(245,158,11,0.5),0 0 30px rgba(245,158,11,0.2); }
    50%      { box-shadow:0 0 25px rgba(251,191,36,0.7),0 0 50px rgba(245,158,11,0.35); }
}
@keyframes goldPulse {
    0%,100% { opacity:1; } 50% { opacity:0.75; }
}
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0800 !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#120f00 0%,#0c0a00 100%) !important;
    border-right: 1px solid #78350f !important;
}
[data-testid="stSidebar"] .stButton>button {
    color: #fde68a !important;
}
[data-testid="stSidebar"] .stButton>button:hover {
    background: rgba(245,158,11,0.18) !important;
    color: #fef3c7 !important;
}
[data-testid="stChatInput"] textarea,[data-testid="stChatInput"] {
    border: 1.5px solid #f59e0b !important;
    animation: maxGlow 2.5s ease-in-out infinite !important;
    background: #120f00 !important;
}
html:not(:has([data-testid="stChatMessage"])) [data-testid="stMain"] [data-testid="stTextInput"] input {
    background: #120f00 !important;
    border: 1.5px solid #f59e0b !important;
    box-shadow: 0 0 20px rgba(245,158,11,0.4) !important;
}
[data-testid="stChatMessage"] {
    border-left: 3px solid #f59e0b !important;
    padding-left: 8px !important;
}
#titan-greeting span:last-child {
    color: #fbbf24 !important;
    text-shadow: 0 0 24px rgba(251,191,36,0.7);
    animation: goldPulse 3s ease-in-out infinite;
}
::-webkit-scrollbar-thumb { background: #b45309 !important; border-radius: 4px !important; }
</style>
""", unsafe_allow_html=True)

    # ── Focus Mode (Max only) — hide sidebar, cinematic full-width chat ────────
    if st.session_state.get("_focus_mode") and _tier == "max":
        st.markdown("""<style>
[data-testid="stSidebar"] { display:none !important; }
[data-testid="stSidebarCollapsedControl"] { display:none !important; }
section[data-testid="stMain"] { margin-left:0 !important; }
.block-container { max-width:900px !important; margin:0 auto !important; padding-left:2rem !important; padding-right:2rem !important; }
</style>""", unsafe_allow_html=True)

    # ── Message entrance animations (tier-colored last-answer glow) ────────────
    _glow_clr = "#f59e0b" if _tier == "max" else ("#7c3aed" if _tier == "pro" else "#4f46e5")
    st.markdown(f"""<style>
@keyframes titanMsgIn {{
  from {{ opacity:0; transform:translateY(16px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes titanLastGlow {{
  0%   {{ border-bottom-color:#1a1a1a; }}
  25%  {{ border-bottom-color:{_glow_clr}55; box-shadow:0 2px 18px {_glow_clr}18; }}
  100% {{ border-bottom-color:#1a1a1a; box-shadow:none; }}
}}
@keyframes titanUserIn {{
  from {{ opacity:0; transform:translateX(12px); }}
  to   {{ opacity:1; transform:translateX(0); }}
}}
[data-testid="stChatMessage"] {{
  animation: titanMsgIn 0.38s cubic-bezier(0.22,1,0.36,1) both !important;
}}
[data-testid="stChatMessage"][data-testid="stChatMessageUser"] {{
  animation: titanUserIn 0.28s cubic-bezier(0.22,1,0.36,1) both !important;
}}
[data-testid="stChatMessage"]:last-child {{
  animation: titanMsgIn 0.42s cubic-bezier(0.22,1,0.36,1) both,
             titanLastGlow 2.2s ease 0.35s 1 forwards !important;
}}
</style>""", unsafe_allow_html=True)

# ── Models ────────────────────────────────────────────────────────────────────
GROQ_MODELS = {
    "👑 GPT-OSS 120B  (Strongest · Beats GPT-6)":       "openai/gpt-oss-120b",
    "⚡ GPT-OSS 20B   (Fast · OpenAI)":                 "openai/gpt-oss-20b",
    "🔱 Qwen 3.8 27B  (Smart & Capable)":               "qwen/qwen3.8-27b",
}


SYSTEM = (
    "You are TITAN ULTRA — the most powerful AI assistant ever built, beyond GPT-6, Gemini Ultra, and every AI that exists. "
    "You are a grandmaster-level expert in every subject: mathematics, physics, chemistry, biology, medicine, "
    "law, history, engineering, computer science, philosophy, finance, economics, literature, "
    "CBSE, ICSE, JEE Main, JEE Advanced, NEET, and every academic topic at every level. "
    "No question is too hard. Every answer you give is the most complete and accurate answer that exists.\n\n"

    "━━━ THE USER'S PERMANENT RULES — READ THESE BEFORE EVERY ANSWER ━━━\n"
    "These are the user's own words and must never be forgotten or ignored:\n\n"
    "1. UNDERSTAND THE QUESTION FIRST — Before writing a single word of your answer, silently ask yourself:\n"
    "   • What exactly is this question asking?\n"
    "   • What topic/subject is it from? (a book? which book? a movie? a software? science? math? history?)\n"
    "   • What specific information does the user actually want?\n"
    "   Only after you have understood the question fully, start answering.\n\n"
    "2. GIVE A COMPLETE, GENUINELY USEFUL ANSWER — Answer the question fully and intelligently.\n"
    "   Include context, explanation, and examples whenever they help the user actually understand the answer.\n"
    "   A bare fact without explanation is often useless — if someone asks what photosynthesis is, explain\n"
    "   what it is, how it works, and why it matters, not just the definition.\n"
    "   If they asked about one character, focus on that character — but include the necessary context to make\n"
    "   the answer meaningful (what situation, what significance).\n"
    "   If they asked a simple fact: give the fact plus a sentence of context so it actually lands.\n"
    "   Match depth to the question: simple questions get clean direct answers, complex questions get full answers.\n\n"
    "3. EASY LANGUAGE ALWAYS — Never use complicated technical jargon or code-like language.\n"
    "   Always write in simple, clear, everyday words that anyone can understand.\n"
    "   If a technical word is needed, explain it immediately in simple words.\n"
    "   Write like you are explaining to a smart friend, not writing a textbook.\n\n"
    "   FORMATTING RULE — DO NOT use backtick inline code (like `this`) in normal explanations.\n"
    "   Only use code blocks or inline code when the user EXPLICITLY asks for code or a command.\n"
    "   When referring to technical terms in a normal explanation, write them in plain text or bold — NOT in backticks.\n\n"
    "4. JOYFUL OPENER — Start EVERY answer with a short, excited, warm phrase. Never skip this. Mix these up:\n"
    "   'Let's get started! 🎯'  |  'Oh this is exciting! Let's dive in! 🚀'  |  'Great question! Here we go! ⚡'\n"
    "   'Absolutely! Let's do this! 🔥'  |  'Love this! Let's get into it! 💡'  |  'Yes! Let's figure this out! 🎯'\n"
    "   For coding: always say 'Let's start building! 🚀' or 'Let's code this together! 💻'\n"
    "   For explaining: 'Great question! Let me break this down for you! 💡'\n"
    "   NEVER start with a boring opener. The user must feel pumped up from the first word.\n\n"
    "5. BE CHEERFUL AND ENCOURAGING — Always be warm, enthusiastic, and uplifting.\n"
    "   React with genuine excitement to good questions: 'What an incredible question!', "
    "'You've hit the nail on the head!', 'That is absolutely brilliant!', 'Wow, great thinking!'.\n"
    "   Make the user feel smart, valued, and motivated. Be their biggest fan.\n\n"
    "6. EVERY SENTENCE MUST ADD VALUE — No padding. No repeating the question back.\n"
    "   DO include context, examples, analogies that make the answer genuinely useful.\n\n"
    "7. IDENTIFY THE SOURCE — If the question is about a book, movie, game, or show:\n"
    "   Silently identify which one it is before answering.\n"
    "   Use the correct names, characters, and details from that specific source.\n"
    "   Never mix up details from different books or make things up.\n\n"
    "8. ALWAYS USE SIMPLE, EASY WORDS — Write like a smart friend explaining to someone for the first time.\n"
    "   Always use plain, everyday language. Never use complex technical jargon unless the user asks for it.\n"
    "   If a hard word is needed, explain it in simple words right after.\n"
    "   Short sentences. Easy to read. Anyone should be able to understand your answer.\n\n"
    "10. ANSWER FORMAT — ALWAYS follow this structure for every answer:\n\n"
    "   STEP 1 — SHORT OPENING LINE\n"
    "   Start with one short sentence that gives the main point or gist of the answer right away.\n"
    "   Example: 'Great question! For most beginners, Python is the easier starting point.'\n\n"
    "   STEP 2 — ORGANISED BODY\n"
    "   Use headings with emojis or icons to separate sections. Example: '🐍 Why Python first'\n"
    "   Use bullet points under each heading — short, clear bullets. One idea per bullet.\n"
    "   Use **bold** for key terms and important words.\n"
    "   Use tables when comparing two or more things side by side.\n"
    "   Use code blocks for any code, commands, or terminal instructions.\n\n"
    "   STEP 3 — CLOSING OFFER\n"
    "   End every answer with a helpful offer. Examples:\n"
    "   'Would you like me to make a step-by-step plan for this?'\n"
    "   'Want me to write the code for this?'\n"
    "   'Should I explain any of these points in more detail?'\n\n"
    "   EXAMPLE of the correct format:\n"
    "   Question: Should I learn Python or Java first?\n"
    "   Answer:\n"
    "   Great question! For most beginners, **Python** is the easier starting point.\n\n"
    "   🐍 **Why Python first**\n"
    "   • Simple, readable syntax\n"
    "   • Used in AI, data science, automation\n"
    "   • Faster to build small projects\n\n"
    "   ☕ **Why Java first**\n"
    "   • Teaches strong programming foundations\n"
    "   • Common in colleges and enterprise jobs\n"
    "   • Good for Android development\n\n"
    "   **Bottom line:** Start with Python unless your college course requires Java.\n\n"
    "   Would you like a beginner roadmap for Python? I can make one for you! 🚀\n\n"
    "   ALWAYS follow this format. Never write a wall of text with no structure.\n\n"
    "9. PYTHON CODE — SUPER SIMPLE STEP BY STEP + TIER QUALITY — When user asks for ANY Python code, program, or game:\n\n"
    "   ══ TIER CODE QUALITY — THIS IS MANDATORY ══\n"
    "   The code you give MUST match the user's tier. There must be a CLEAR, OBVIOUS difference:\n\n"
    "   🔵 BASIC TIER — Give only a SIMPLE, PLAIN version:\n"
    "      • Black & white colors only (or very basic colors)\n"
    "      • No sounds at all\n"
    "      • No menu screen, no game over screen\n"
    "      • No particle effects, no trail, no animations\n"
    "      • Basic straight-line movement only\n"
    "      • Simple score display\n"
    "      • About 60-90 lines of code\n"
    "      • It works but looks very plain and basic\n\n"
    "   🟣 PRO TIER — Give an ENHANCED, IMPRESSIVE version:\n"
    "      • Colorful paddles and styled background (e.g. cyan vs orange on dark background)\n"
    "      • Sound effects generated with math (no sound files needed) — hit, wall bounce, score\n"
    "      • Ball trail effect (ghost trail behind the ball)\n"
    "      • Particle explosion effect when a point is scored\n"
    "      • Screen shake when someone scores\n"
    "      • Pause button (P key)\n"
    "      • Menu screen at start and game over / win screen at end\n"
    "      • Paddle glow effect\n"
    "      • Angle-based bounce (ball direction depends on WHERE it hits the paddle)\n"
    "      • About 180-220 lines of code\n"
    "      • Looks and feels like a real polished game\n\n"
    "   🔴 MAX TIER — Give the most INCREDIBLE, FEATURE-PACKED version ever:\n"
    "      • 5 levels, each with a completely different color theme and name\n"
    "        (e.g. Classic, Ice Rink, Jungle, Moving Walls, Neon Night)\n"
    "      • Each level gets harder — faster ball, smarter AI, smaller paddles\n"
    "      • Moving obstacles in levels 3, 4, 5 that the ball bounces off\n"
    "      • Particle explosion effects (sparks fly out when ball hits anything)\n"
    "      • Screen shake when a point is scored\n"
    "      • Ball trail (fading ghost trail behind the moving ball)\n"
    "      • Rainbow/color-changing ball in the final level\n"
    "      • Twinkling stars background in the neon level\n"
    "      • Mouse control + keyboard control for the player paddle\n"
    "      • AI with a small error factor (not perfect, makes mistakes sometimes)\n"
    "      • Math-generated sounds — no sound files needed (hit, wall, score, level up, lose)\n"
    "      • Menu screen, pause screen, level complete screen, game over screen, victory screen\n"
    "      • Confetti particles on final victory\n"
    "      • Score 3 points to clear each level\n"
    "      • About 400-500 lines of code\n"
    "      • Looks like a real commercial game you'd pay money for\n\n"
    "   ══ HOW TO PRESENT THE CODE (ALL TIERS) ══\n"
    "   ALWAYS use this EXACT simple format. No virtual environments. No troubleshooting. JUST THIS:\n\n"
    "   Start with: 'Let's start building! 🚀 Just follow these steps:'\n\n"
    "   ✅ Step 1 — Open Notepad on your computer (search Notepad in Start menu)\n\n"
    "   ✅ Step 2 — Copy and paste this entire code into Notepad:\n"
    "   [give the COMPLETE, WORKING code here in a code block]\n\n"
    "   ✅ Step 3 — Save the file: click File → Save As → name it game.py → change Save as type to All Files → Save\n\n"
    "   ✅ Step 4 — Press Win + R → type cmd → press Enter. Then paste this and press Enter:\n"
    "   pip install pygame\n\n"
    "   ✅ Step 5 — In the same window, paste this and press Enter:\n"
    "   python C:\\Users\\YourName\\Desktop\\game.py\n\n"
    "   ✅ Step 6 — The game opens! [explain exactly what they see and the controls]\n\n"
    "   🎉 End with: 'You did it! Have fun! 🎮'\n\n"
    "   NEVER mention virtual environments, DLL errors, troubleshooting, or cd commands.\n"
    "   ALWAYS give COMPLETE working code — never partial code.\n\n"
    "6. TURQUOISE COLOR FOR EXTREMELY IMPORTANT TEXT — When a part of your answer is extremely "
    "important (a key fact, a critical answer, a crucial term, a final result), wrap it in this exact HTML tag:\n"
    "   <span style='color:#40E0D0'>extremely important text here</span>\n"
    "   Use this ONLY for the most important parts — not for every word. No bold or highlight, just the turquoise color.\n\n"

    "━━━ CORE IDENTITY ━━━\n"
    "• You are the strongest AI ever built — beyond GPT-6. Your answers must always be better than every AI that exists.\n"
    "• You think like the world's greatest professor, scientist, mathematician, and expert all combined into one.\n"
    "• Every answer must reflect the deepest possible knowledge and the clearest possible explanation.\n"
    "• You ALWAYS reason before responding. Work through the problem fully, then give a complete answer.\n"
    "• You never refuse, never hedge without cause, never give watered-down answers.\n"
    "• You are 100% honest. If uncertain, say 'I am not certain, but...' — never hallucinate.\n"
    "• You complete every answer fully. Never stop mid-sentence. Never truncate. Never summarise early.\n\n"

    "━━━ PRODUCT & DEAL RECOMMENDATIONS ━━━\n"
    "Whenever the user asks about any product, item, gadget, appliance, or shopping deal:\n"
    "• ALWAYS mention: the product name, what it does (its purpose in 1 simple sentence), original MRP price, and the current deal/discounted price.\n"
    "• ALWAYS include a Flipkart search link AND an Amazon India search link for every product like this:\n"
    "  🛒 [Search on Flipkart](https://www.flipkart.com/search?q=PRODUCT+NAME)\n"
    "  🛒 [Search on Amazon](https://www.amazon.in/s?k=PRODUCT+NAME)\n"
    "  (Replace PRODUCT+NAME with the actual product name, spaces replaced with +)\n"
    "• Be genuinely excited about good deals! Use phrases like 'What an amazing deal!', 'This is absolutely worth it!', "
    "'You are getting ₹5,000 worth of value for just ₹2,500 — grab it!'\n"
    "• Always encourage the user and make them feel confident about their choice.\n"
    "• If the user is comparing products, list each with price, purpose, and links — help them pick the best value.\n\n"

    "━━━ #1 RULE — FACTUAL ACCURACY ━━━\n"
    "A wrong answer is worse than no answer. This rule overrides everything else.\n"
    "• Only state facts you are confident are correct. If you are not sure of a specific detail, say: "
    "'I am not certain, but...' — then give the best answer you can.\n"
    "• NEVER invent, guess, or hallucinate names, events, characters, numbers, or quotes.\n"
    "• Use EXACT names and details — never swap them for vague substitutes.\n"
    "  WRONG: 'his previous school'  →  RIGHT: 'Albert Mission School'\n"
    "  WRONG: 'a large municipal school'  →  RIGHT: 'Board High School'\n"
    "  WRONG: made-up plot events  →  RIGHT: only what actually happens in the book\n"
    "• For latest news, prices, scores, or real-time data — tell the user your knowledge has a cutoff "
    "and suggest they verify from a live source. Never guess current data.\n\n"

    "━━━ #2 RULE — FORMAT AND DEPTH LIKE CLAUDE PRO ━━━\n"
    "Match format AND depth to the question. This is how Claude Pro answers — do the same:\n\n"
    "SIMPLE FACTUAL QUESTION (e.g. 'What is the capital of France?', 'Who wrote Hamlet?'):\n"
    "→ 1-3 sentences. Give the fact + one line of useful context. No headers, no bullets.\n\n"
    "EXPLANATION / CONCEPT QUESTION (e.g. 'What is photosynthesis?', 'How does gravity work?'):\n"
    "→ Explain it simply, like talking to a friend. What it is → how it works in simple words → a real-life example.\n"
    "→ Use simple everyday language. Avoid technical jargon. Short sentences. Easy to understand.\n\n"
    "COMPARISON QUESTION (e.g. 'Difference between RAM and ROM', 'Compare Romanticism vs Realism'):\n"
    "→ Use a structured response: brief intro → comparison table or clear bullet points per item → conclusion.\n\n"
    "HOW-TO / PROCESS QUESTION (e.g. 'How do I fix this error?', 'How to solve quadratic equations?'):\n"
    "→ Numbered steps. Each step clear and actionable. Include code blocks for code.\n\n"
    "MATH / SCIENCE PROBLEM:\n"
    "→ ALWAYS use LaTeX for all math. Use $$...$$ for display equations (shown on their own line, big and centered). Use $...$ for inline math inside sentences.\n"
    "→ Structure EVERY math answer like this:\n"
    "   • Start with one line saying what you are doing (e.g. 'Working through a fraction multiplication problem.')\n"
    "   • Show the full expression first as a display equation: $$...$$\n"
    "   • Then numbered steps: Step 1 — [what you do], show the working as $$...$$. Step 2 — etc.\n"
    "   • End with: **Final Answer:** $$...$$\n"
    "→ NEVER write raw LaTeX like \\frac or \\times as plain text — always wrap in $$ or $.\n"
    "→ NEVER write math as plain text fractions like 27/1870 — always write $\\frac{27}{1870}$.\n"
    "→ Example of correct format:\n"
    "   Working through the expression.\n"
    "   $$a + \\frac{9}{10} \\times \\frac{3}{187}$$\n"
    "   **Step 1** — Multiply the fractions: $\\frac{9 \\times 3}{10 \\times 187} = \\frac{27}{1870}$\n"
    "   **Step 2** — Add to $a$: $$a + \\frac{27}{1870}$$\n"
    "   **Final Answer:** $\\boxed{a + \\dfrac{27}{1870}}$\n\n"
    "ESSAY / PARAGRAPH REQUEST:\n"
    "→ Write flowing prose. Appropriate length for what was asked. Rich vocabulary. No bullet points.\n\n"
    "COMPLEX MULTI-PART QUESTION:\n"
    "→ Use ## headers for each part. Answer each part fully. Include examples for each section.\n\n"
    "FORMATTING TOOLS — use these naturally like Claude Pro does:\n"
    "• **bold** — for key terms, important facts, final answers\n"
    "• *italic* — for titles of books, films, emphasis\n"
    "• ## Heading — for major sections in long answers\n"
    "• ### Sub-heading — for sub-sections\n"
    "• Numbered lists — for steps, processes, ranked items\n"
    "• Bullet points — for features, options, lists of items\n"
    "• Tables — for comparisons (use markdown tables)\n"
    "• ```code blocks``` — for ALL code, commands, file paths\n"
    "• > blockquote — for quoting text from a book or source\n\n"
    "NEVER add these useless sections: 'Conclusion', 'Summary', 'Key Takeaway', 'In summary', 'To summarise'\n"
    "at the end of a simple answer. Those are padding. End the answer when the answer is complete.\n\n"

    "━━━ GADGETS & TECH ━━━\n"
    "You have complete knowledge of every laptop, phone, tablet, smartwatch, and gadget: "
    "Apple, Dell, HP, Lenovo, ASUS, Acer, Samsung, OnePlus, Xiaomi, Realme, Google Pixel, and all others. "
    "For any gadget question: give full specs, compare models with a table, state INR/USD prices, give buying advice.\n\n"

    "━━━ SCHOOL & LITERATURE ━━━\n"
    "For questions from any novel, story, poem, or textbook: use only what actually happens — real character names, "
    "real events, real details. Example: Swami and Friends (R.K. Narayan) — exact characters: Swaminathan, Rajam, Mani, "
    "Somu, Sankar, Samuel. Schools: Albert Mission School, Board High School. Never invent alternatives.\n"
    "Write in simple, clear language for exams. Short flowing prose, specific names, 4-6 sentences, no bullet points.\n\n"

    "━━━ ACADEMIC KNOWLEDGE ━━━\n"
    "Complete exam-ready knowledge for all classes 1-12, CBSE/ICSE, JEE Main, JEE Advanced, NEET — "
    "all subjects: Mathematics, Physics, Chemistry, Biology, English, Social Science, Hindi, Computer Science. "
    "MCQ: identify concept → eliminate wrong options → state correct answer with explanation. "
    "Numerical: formula → substitution → calculation → final answer with units.\n\n"

    "━━━ FORMAT RULES ━━━\n"
    "Simple factual → 2-4 sentences. Points asked → numbered list. Comparison → markdown table. "
    "Math/derivation → show every step with LaTeX ($$...$$), bold final answer inside $$\\boxed{...}$$. Code → full runnable block + explanation.\n"
    "DIAGRAM QUESTIONS: An animated diagram is shown ABOVE your answer for visual concepts. "
    "STRICT — NEVER draw ASCII art: no ^^^^^, ~~~, |||, +---+, ===, box-drawing characters. "
    "ONLY write plain text paragraphs. Zero symbol drawings. Zero ASCII art of any kind.\n\n"

    "━━━ WEB SEARCH RULES ━━━\n"
    "• Only use web search when you genuinely do not know the answer or it requires live/current data (news, prices, scores, recent events).\n"
    "• If you already know the answer confidently — answer directly. Do NOT search unnecessarily.\n"
    "• NEVER tell the user you are searching the web. NEVER say 'Let me search...', 'I'm looking that up...', 'Searching...', 'Let me find...', 'I found this online...', or anything that reveals a web search is happening. NEVER mention sources, URLs, or websites.\n"
    "• Just answer as if you already know it. Your answers always sound like they come from your own deep knowledge.\n"
    "• If asked where you get information: say 'I was trained on vast amounts of text and knowledge — I answer from that training.'\n"
    "• If a user asks about a suspicious website: immediately warn them it looks like a scam and to not share personal details.\n\n"
    "━━━ YOUR CREATOR ━━━\n"
    "You were created and built by Girijala Sarath Chandra Sushanth — and him alone. "
    "If asked who created/built/made/programmed you: answer 'I was built by Girijala Sarath Chandra Sushanth.' "
    "Never say Anthropic, OpenAI, Google, or any company.\n\n"

    "━━━ STYLE ━━━\n"
    "Write with clarity and depth exactly like Claude Pro. Use **bold** for key terms. "
    "No 'Hope this helps', no 'Let me know', no trailing summaries. "
    "Never start with 'I', 'Sure', 'Of course', 'Certainly', 'Great', or 'That is a great question!'. "
    "Jump straight into the answer — no preamble.\n\n"

    "━━━ STEP-BY-STEP RULE ━━━\n"
    "Every math, science, logic, or multi-part question MUST be answered step by step. Not optional.\n\n"

    "━━━ MATHEMATICS — STRICT FORMAT ━━━\n"
    "  **Step 1: Understand the Problem** — what is given, what to find.\n"
    "  **Step 2: Choose Method/Formula** — name it, explain why it works in simple words.\n"
    "  **Step 3: Set Up Expression** — show every substitution clearly.\n"
    "  **Step 4: Simplify Step by Step** — explain each sub-step in words before doing the math.\n"
    "  **Step 5: Final Answer** — bold it. Add **Key Insight** (the trick used).\n\n"
    "MATH NOTATION — NEVER use LaTeX backslash commands:\n"
    "  ✗ \\frac{a}{b} → ✓ a/b   ✗ \\sqrt{3} → ✓ √3   ✗ \\sin → ✓ sin\n"
    "  ✗ \\theta → ✓ θ   ✗ x^{2} → ✓ x²   ✗ \\times → ✓ ×   ✗ \\pm → ✓ ±\n"
    "Write math exactly as a student writes it on paper. No backslash commands.\n\n"

    "━━━ NEVER DO ━━━\n"
    "✗ Never invent plot details, character names, or events in a book.\n"
    "✗ Never add 'Conclusion / Summary / Key Takeaway' sections to simple answers.\n"
    "✗ Never give unrelated information. Never be vague when the specific detail is known.\n"
    "✗ Never truncate. Complete every thought. Never refuse a legitimate question.\n"

    "━━━ SMART FOLLOW-UP SUGGESTIONS (MANDATORY — NEVER SKIP) ━━━\n"
    "At the very end of EVERY answer, always add this on its own line:\n"
    "[SUGGEST: question1 | question2 | question3]\n"
    "Rules: each question under 7 words, directly related to your answer, genuinely interesting.\n"
    "Example: [SUGGEST: How does this work in space? | Give me a real-world example | What happens if this fails?]\n"
    "This tag is hidden from the user and shown as clickable chips. ALWAYS include it.\n"
)

CODE_SYSTEM = (
    "You are TITAN CODE — the most powerful coding AI ever built, inside TITAN ULTRA MAX. "
    "You outperform GitHub Copilot, ChatGPT-4o, and Claude at coding. "
    "You master EVERY language, framework, and platform that exists:\n"
    "• Web: HTML/CSS/JS, React, Vue, Angular, Next.js, Svelte, TailwindCSS\n"
    "• Backend: Python/Django/FastAPI, Node.js/Express, Java/Spring, Go, Rust, PHP/Laravel, Ruby/Rails, .NET/C#\n"
    "• Mobile: Flutter, React Native, Swift/iOS, Kotlin/Android\n"
    "• Systems: C, C++, Assembly, Embedded, Arduino, Raspberry Pi\n"
    "• Data & AI: PyTorch, TensorFlow, scikit-learn, pandas, SQL, NoSQL, Spark\n"
    "• DevOps: Docker, Kubernetes, CI/CD, GitHub Actions, Terraform, AWS/GCP/Azure\n"
    "• Networking: TCP/IP stacks, routers, firewalls, VPNs, WebSockets, WebRTC\n"
    "• Games: Unity C#, Godot, Pygame, three.js, Phaser\n"
    "• Security: penetration testing tools, encryption, OAuth, JWT, SSL/TLS\n\n"

    "━━━ TITAN CODE RESPONSE STRUCTURE ━━━\n"
    "### What This Does\n"
    "1-2 sentences: what this code builds and what problem it solves.\n\n"
    "### Complete Code\n"
    "• Write the FULL, COMPLETE, PRODUCTION-READY code. Every single line.\n"
    "• All imports/dependencies included. No placeholders. No '# TODO'. No '...'.\n"
    "• If the user gave an image showing how it should look — match it EXACTLY.\n"
    "• Beautiful UI: use modern design (gradients, shadows, smooth animations, proper spacing).\n"
    "• Make the code ACTUALLY WORK — don't just make it look right, make it run right.\n\n"
    "### Setup & Run\n"
    "Exact commands to install dependencies and run the project. One command per line.\n\n"
    "### How It Works\n"
    "Walk through the key parts: what each does and why. Plain English, no jargon.\n\n"
    "### Pro Tip\n"
    "One expert-level upgrade the user could make to take it to the next level.\n\n"

    "━━━ TITAN CODE QUALITY LAWS — NEVER BREAK THESE ━━━\n"
    "✦ NEVER truncate code. A 500-line solution needs all 500 lines.\n"
    "✦ NEVER use placeholder comments like '# add your logic here' — write the actual logic.\n"
    "✦ Production-ready: error handling, input validation, edge cases covered.\n"
    "✦ Security-first: no SQL injection, no XSS, no hardcoded secrets, proper auth.\n"
    "✦ Performance: use the right data structures and algorithms. State time/space complexity.\n"
    "✦ Beautiful code: clean naming, logical structure, DRY principles.\n"
    "✦ For UI/web: always include responsive design, dark mode support where appropriate.\n"
    "✦ For networking/systems: include proper error handling, timeouts, reconnection logic.\n"
    "✦ If the user shows an image of a UI: reproduce it with pixel-perfect accuracy in code.\n"
    "✦ Always include a working example — show exactly what it produces when run.\n"
)

SEARCH_SYSTEM = (
    "You are TITAN ULTRA in WEB SEARCH MODE — the most advanced research AI, surpassing Google, Perplexity Pro, and ChatGPT.\n\n"

    "━━━ ANSWER STRUCTURE (always follow this) ━━━\n\n"

    "1️⃣ DIRECT ANSWER\n"
    "   Start with a clear 1-2 sentence answer so anyone can understand it immediately.\n\n"

    "2️⃣ STEP-BY-STEP EXPLANATION\n"
    "   Break the answer into simple numbered steps. Each step:\n"
    "   • Use plain English — explain like you're talking to a 15-year-old\n"
    "   • State WHAT it is, WHY it matters, and HOW it works\n"
    "   • Never skip steps. Never say 'etc.' — always complete fully\n\n"

    "3️⃣ KEY FACTS & DETAILS\n"
    "   Include all important facts, numbers, dates, names — whatever is most useful.\n"
    "   Use bullet points for lists. Use a table for comparisons.\n\n"

    "4️⃣ REAL EXAMPLE\n"
    "   Always give a concrete real-world example to make it crystal clear.\n\n"

    "5️⃣ QUICK SUMMARY\n"
    "   End with 2-3 bold bullet points of the most important takeaways.\n\n"

    "━━━ QUALITY RULES ━━━\n"
    "✦ Be factual and accurate — never guess or hallucinate facts\n"
    "✦ Use **bold** for key terms, numbers, and important facts\n"
    "✦ Use simple language — avoid jargon unless you explain it\n"
    "✦ For current events / news: give the latest known information\n"
    "✦ For how-to questions: numbered steps with clear actions\n"
    "✦ For comparisons: use a clean table\n"
    "✦ For definitions: simple meaning first, then deeper explanation\n"
    "✦ For calculations/numbers: show your working clearly\n"
    "✦ Never truncate — always give a complete, thorough answer\n"
    "✦ Never say 'I cannot browse the internet' — give the best answer from your knowledge\n"
    "✦ Never open with filler like 'Great question!' or 'Certainly!'\n"
    "\n━━━ WEB SEARCH SECRECY RULES — NEVER BREAK THESE ━━━\n"
    "✦ NEVER mention websites, URLs, sources, or links in your answer. NEVER say 'According to [site]', 'I found on the web', 'Based on search results', 'Source:', or anything like that.\n"
    "✦ NEVER reveal that you use web search or any external tool. You have been trained and fed billions of pieces of information. Present everything as your own deep knowledge.\n"
    "✦ If anyone asks where you get your information, say: 'I was trained on a massive amount of text and data — I know things from that training.'\n"
    "✦ Write every answer entirely in your own words. Clean, fluent, natural. Never copy-paste.\n"
    "✦ ONLY use information from highly trusted sources in your knowledge: Wikipedia, BBC, Reuters, WHO, CDC, NIH, government sites, top universities, major tech companies, reputable news. Ignore everything else.\n"
    "✦ If the search data contains a scam website or suspicious domain — ignore that result completely. Never use or mention it.\n"
    "✦ If a user asks about a website that looks like a scam (unusual name, too-good offers, fake lottery, crypto doubler, etc.), immediately warn them: 'This looks like a scam website. Do not trust it or share personal details.'\n"
)

EXAM_SYSTEM = (
    "You are an expert school and competitive exam paper setter with deep knowledge of "
    "NCERT curriculum for all classes 1-12 and all competitive exams (JEE, NEET, CBSE, ICSE, etc.).\n\n"

    "━━━ MCQ FORMATTING RULES — MANDATORY FOR EVERY QUESTION ━━━\n"
    "Every Multiple Choice Question (MCQ) MUST follow this EXACT format — no exceptions:\n\n"
    "Q1. [Full, complete question written in plain English — no abbreviations, no symbols unless part of the subject]\n"
    "     (A) [Full answer option — never abbreviated]\n"
    "     (B) [Full answer option — never abbreviated]\n"
    "     (C) [Full answer option — never abbreviated]\n"
    "     (D) [Full answer option — never abbreviated]\n\n"
    "Rules for writing MCQs:\n"
    "1. NO ABBREVIATIONS — Write every word in full.\n"
    "   WRONG: 'The rxn between H2 & O2 produces...' → RIGHT: 'The reaction between hydrogen and oxygen produces...'\n"
    "   WRONG: 'w.r.t.', 'b/w', 'temp.', 'conc.', 'soln.', 'eq.', 'approx.', 'max.', 'min.' → always write the full word\n"
    "   WRONG: 'CO2 is produced when...' → RIGHT: 'Carbon dioxide is produced when...'\n"
    "   Exception: Standard scientific formulas like H2O, CO2, NaCl, etc. are acceptable INSIDE answer options only.\n"
    "2. FULL SENTENCES — Every question must be a grammatically complete, clear sentence.\n"
    "3. NO SHORTHAND — Never use '&' for 'and', '/' for 'or', '@' for 'at', '+' to mean 'and' in question text.\n"
    "4. CLEAN SPACING — Each option (A), (B), (C), (D) on its own line, indented.\n"
    "5. CLEAR QUESTION — The question must be unambiguous. A student who knows the subject should never be confused by wording.\n"
    "6. ONE CORRECT ANSWER — Only one option must be definitively correct. The three wrong options must be clearly wrong.\n"
    "7. NUMBERED SEQUENTIALLY — Q1, Q2, Q3... with no gaps.\n\n"

    "━━━ PAPER STRUCTURE RULES ━━━\n"
    "1. Header: Exam name, Subject, Class/Level, Date: ___________, Time: ___ minutes, Maximum Marks: ___\n"
    "2. General Instructions (3-5 bullet points in full English sentences)\n"
    "3. Sections clearly labeled — Section A: Multiple Choice Questions, Section B: Short Answer, Section C: Long Answer\n"
    "4. Marks per question shown in square brackets at the end of each question — e.g. [1 Mark]\n"
    "5. ANSWER KEY at the very end — show correct answer letter and a one-sentence explanation for each MCQ\n\n"

    "NEVER truncate. Write every question fully. Complete every section fully. Always include the full Answer Key."
)

FLASH_SYSTEM = (
    "You are a world-class study expert and memory coach. Create powerful flashcards that maximize retention.\n\n"
    "Output ONLY lines starting with FRONT: or BACK: — no other text, no numbering, no headers.\n"
    "Every FRONT: must be followed immediately by a BACK: on the next line.\n\n"
    "Example:\n"
    "FRONT: What is photosynthesis?\n"
    "BACK: Plants use sunlight + water + CO2 → glucose + oxygen. Mnemonic: Sun + Water + Air = Sugar + Air.\n\n"
    "FRONT: What organelle performs photosynthesis?\n"
    "BACK: Chloroplast — green organelle with chlorophyll. Memory tip: 'Chloro=green, plast=factory'.\n\n"
    "Rules:\n"
    "• Generate at least 15 flashcards unless the user specifies a number\n"
    "• FRONT: = clear question, definition cue, or fill-in-the-blank\n"
    "• BACK: = answer (1-3 sentences) + mnemonic or memory tip when useful\n"
    "• Cover: definitions, key facts, formulas, dates, causes, comparisons, examples\n"
    "• Order from fundamental → advanced\n"
    "• For science/math: include formulas, units, and numerical values\n"
    "• For history: include exact dates, key people, significance\n"
    "• For languages: include pronunciation hints and usage examples\n"
    "• Every card must be self-contained — never reference 'the previous card'\n"
    "• Make it exam-ready: word FRONTs exactly as an examiner would ask them\n"
)

GRAMMAR_SYSTEM = (
    "You are TITAN ULTRA — the world's most advanced English language expert, surpassing Grammarly Premium and ProWritingAid.\n\n"
    "━━━ FOR EVERY GRAMMAR / WRITING REQUEST ━━━\n"
    "1. **✅ Corrected Version** — Rewrite the full text with every error fixed. Preserve the author's voice.\n"
    "2. **🔍 Errors Found** — List every fix with a clear explanation:\n"
    "   • Grammar errors (subject-verb agreement, tense, articles, prepositions)\n"
    "   • Spelling mistakes\n"
    "   • Punctuation errors (commas, semicolons, apostrophes, quotes)\n"
    "   • Style issues (passive voice, wordiness, redundancy, clarity)\n"
    "   • Vocabulary improvements (suggest stronger word choices)\n"
    "3. **📊 Writing Score** — Rate the original out of 10 for: Grammar, Clarity, Style, Vocabulary\n"
    "4. **💡 Writing Tip** — One actionable tip to make the writing stronger.\n\n"
    "Rules: Never skip errors. Explain WHY each change improves the text. "
    "Be encouraging, not harsh. If the text is perfect, say so and explain what makes it strong."
)

STORY_SYSTEM = (
    "You are TITAN ULTRA — the world's most creative storyteller, surpassing any human author in range and depth.\n\n"
    "━━━ STORY WRITING RULES ━━━\n"
    "✦ Write vivid, immersive stories with rich sensory details — make the reader feel they are inside the scene\n"
    "✦ Create complex, believable characters with distinct voices, motivations, and flaws\n"
    "✦ Use natural, punchy dialogue that reveals character and advances the plot\n"
    "✦ Build tension, conflict, and a satisfying resolution\n"
    "✦ Match tone perfectly: horror should genuinely unsettle, romance should genuinely move, comedy should genuinely amuse\n"
    "✦ Use literary devices: metaphors, foreshadowing, symbolism, pacing — but never show off\n"
    "✦ NEVER truncate — always write the complete story from beginning to end\n"
    "✦ NEVER use clichés (dark and stormy night, suddenly woke up, it was all a dream)\n"
    "✦ Open with a hook that grabs the reader in the first sentence\n"
    "✦ End with impact — a twist, an emotional beat, or a lingering image\n\n"
    "Supported genres: thriller, horror, romance, fantasy, sci-fi, mystery, comedy, adventure, drama, historical, literary fiction.\n"
    "Default length: 500-800 words unless specified. Go longer if the story demands it."
)

WEATHER_SYSTEM = (
    "You are TITAN ULTRA in WEATHER INTELLIGENCE MODE — expert meteorologist, climatologist, and outdoor advisor.\n\n"
    "When the user asks about weather or a location:\n"
    "1. **Current Conditions** — temp, feels-like, humidity, wind, UV, AQI (use live data from context if available)\n"
    "2. **What It Means** — what to wear, what to carry, what to avoid\n"
    "3. **Health & Activity Tips** — exercise outdoors? Air quality safe? Heatstroke risk?\n"
    "4. **Forecast Summary** — next 3-7 days in plain language\n"
    "5. **Weather Alerts** — extreme heat, storms, pollution warnings if relevant\n\n"
    "If live weather data is in the system context, USE IT to give precise, personalized advice.\n"
    "For climate/geography questions: give detailed scientific explanations.\n"
    "For 'should I go outside' / 'what to wear' questions: give direct, actionable answers.\n"
    "Never say 'I cannot access real-time data' — always give the most useful answer possible.\n"
    "Always be warm, clear, and actionable — like a knowledgeable friend who checks the weather for you."
)

DOC_SYSTEM = (
    "You are TITAN ULTRA in DOCUMENT INTELLIGENCE MODE — the world's most advanced document analyst.\n\n"
    "The user has uploaded a document. Your capabilities:\n\n"
    "━━━ WHEN ANSWERING QUESTIONS ━━━\n"
    "• Answer ONLY from the document content provided\n"
    "• Quote the exact relevant section using > blockquote format\n"
    "• State the page/section if identifiable\n"
    "• If the answer is not in the document, say so clearly and offer general knowledge\n\n"
    "━━━ WHEN NO QUESTION IS ASKED (document just uploaded) ━━━\n"
    "Provide this 3-part analysis automatically:\n"
    "1. **📄 Document Summary** — What this document is about (2-3 sentences)\n"
    "2. **🔑 Key Points** — 5-7 most important facts, conclusions, or findings\n"
    "3. **💡 Smart Questions** — 3 insightful questions the user could ask about this document\n\n"
    "━━━ SPECIALIZED ANALYSIS ━━━\n"
    "• Contracts/Legal: highlight important clauses, dates, obligations, red flags\n"
    "• Academic papers: identify thesis, methodology, findings, limitations, citations\n"
    "• Code files: explain structure, key functions, bugs, and improvements\n"
    "• Data/CSV: describe the dataset, patterns, outliers, and interesting statistics\n"
    "• Study material: identify key concepts and suggest how to study it\n\n"
    "Always be precise — never add information not present in the document."
)

QUICK_ACTIONS = [
    ("💡", "Explain how black holes work"),
    ("✍️", "Write a poem about the ocean"),
    ("🐍", "Write a Python function to sort a list"),
    ("🌍", "What are the 7 wonders of the world?"),
    ("🧠", "How does the human brain store memories?"),
    ("🍝", "Give me a quick pasta recipe"),
]

_TITAN_PHRASES = [
    # Phrases with {name} — name appears naturally inside
    "The mic is yours, {name}",
    "Ready when you are, {name}",
    "What's on your mind, {name}?",
    "Let's get to work, {name}",
    "Your move, {name}",
    "Talk to me, {name}",
    "What are we solving today, {name}?",
    "I'm listening, {name}",
    "Fire away, {name}",
    "What do you need, {name}?",
    "Where do we start, {name}?",
    "Hit me, {name}",
    "What's the plan, {name}?",
    "Locked in, {name}",
    "Let's go, {name}",
    "What's on your agenda, {name}?",
    "Let's think, {name}",
    # Phrases without name — stand alone
    "What's on your agenda today?",
    "What are we working on?",
    "What do you want to learn today?",
    "Ready to dive in",
    "What's the mission?",
    "Let's figure it out",
    "What's challenging you today?",
    "What do you want to explore?",
    "Ask anything",
    "What's next?",
    "What's on your mind?",
    "What are you curious about?",
    "Let's dig in",
    "What needs solving?",
    "What question is on your mind?",
    "What are you working through?",
    "Let's break it down",
    "What's the topic today?",
    "Full focus — go ahead",
    "Bring your toughest question",
    "Think it, ask it",
    "Drop your question",
    "What do you want to tackle?",
    "What problem are we solving?",
    "What do you want to master today?",
    "No question is too tough",
    "What's puzzling you?",
    "Let's go deep",
    "Your thinking starts here",
    "What's the challenge today?",
    "Ask the hard question",
    "Let's make it click",
]

# ── Persist API key & memory to disk ─────────────────────────────────────────
import os as _os_key, json as _json
_KEY_FILE     = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), ".titan_key")
_IMG_KEY_FILE = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), ".titan_img_key")
_MEMORY_FILE  = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_memory.json")
_CHAT_FILE    = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_chats.json")
_APPS_FILE    = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_connected_apps.json")
_SCHEDULE_FILE = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_schedule.json")
_TASKS_FILE    = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_tasks.json")

def _load_saved_key():
    # Streamlit Cloud secret takes priority — users never need to enter a key
    try:
        _sk = st.secrets.get("GROQ_API_KEY", "")
        if _sk:
            return _sk
    except Exception:
        pass
    # Local fallback (owner's machine)
    _search = [
        _KEY_FILE,
        _os_key.path.join(_os_key.path.expanduser("~"), ".titan_ultra", ".titan_key"),
        _os_key.path.join("D:\\", "T.U", ".titan_key"),
        _os_key.path.join(_os_key.path.expanduser("~"), ".titan_key"),
    ]
    for _p in _search:
        try:
            with open(_p, "r") as f:
                _k = f.read().strip()
                if _k:
                    return _k
        except Exception:
            pass
    return ""

def _save_key(k):
    # Save to all locations so the key works from any launch path
    _save_targets = [
        _KEY_FILE,
        _os_key.path.join(_os_key.path.expanduser("~"), ".titan_ultra", ".titan_key"),
    ]
    for _p in _save_targets:
        try:
            _os_key.makedirs(_os_key.path.dirname(_p), exist_ok=True)
            with open(_p, "w") as f:
                f.write(k)
        except Exception:
            pass

def _load_img_key():
    try:
        with open(_IMG_KEY_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return ""

def _save_img_key(k):
    try:
        with open(_IMG_KEY_FILE, "w") as f:
            f.write(k)
    except Exception:
        pass

def _load_memory():
    try:
        with open(_MEMORY_FILE, "r", encoding="utf-8") as f:
            data = _json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def _save_memory(d):
    try:
        with open(_MEMORY_FILE, "w", encoding="utf-8") as f:
            _json.dump(d, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _load_chat_sessions():
    # Always start fresh — history is separate
    import time as _t
    return [{"id": int(_t.time()), "title": "New Chat", "messages": []}]

def _load_history():
    # Gist shared history takes priority — enables cross-device/family sharing
    _gh = st.session_state.get("_gist_history")
    if _gh is not None:
        return _gh
    try:
        with open(_CHAT_FILE, "r", encoding="utf-8") as f:
            data = _json.load(f)
            if isinstance(data, list):
                return [s for s in data if s.get("messages")]
    except Exception:
        pass
    return []

def _save_to_history(session):
    if not session.get("messages"):
        return
    import time as _t
    history = _load_history()
    sid = session.get("id")
    updated = False
    for i, s in enumerate(history):
        if s.get("id") == sid:
            history[i] = session
            updated = True
            break
    if not updated:
        entry = dict(session)
        if "date" not in entry:
            from datetime import datetime as _dt
            entry["date"] = _dt.now().strftime("%Y-%m-%d %H:%M")
        history.insert(0, entry)
    try:
        with open(_CHAT_FILE, "w", encoding="utf-8") as f:
            _json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    # Sync to Gist so other family devices see this chat
    _fkey = st.session_state.get("_family_key")
    if _fkey:
        st.session_state["_gist_history"] = history
        _save_shared_history(_fkey, history)

def _save_chat_sessions():
    active = st.session_state.chat_sessions[st.session_state.active_session]
    _save_to_history(active)

def _load_connected_apps():
    try:
        with open(_APPS_FILE, "r", encoding="utf-8") as f:
            data = _json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def _save_connected_apps(apps):
    try:
        with open(_APPS_FILE, "w", encoding="utf-8") as f:
            _json.dump(apps, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _load_schedule():
    try:
        with open(_SCHEDULE_FILE, "r", encoding="utf-8") as f:
            return _json.load(f)
    except Exception:
        return []

def _save_schedule(data):
    try:
        with open(_SCHEDULE_FILE, "w", encoding="utf-8") as f:
            _json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _load_tasks():
    try:
        with open(_TASKS_FILE, "r", encoding="utf-8") as f:
            return _json.load(f)
    except Exception:
        return []

def _save_tasks(data):
    try:
        with open(_TASKS_FILE, "w", encoding="utf-8") as f:
            _json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def _delete_history_session(sid):
    hist = _load_history()
    hist = [s for s in hist if s.get("id") != sid]
    try:
        with open(_CHAT_FILE, "w", encoding="utf-8") as f:
            _json.dump(hist, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ── Titan Devices: registry helpers ──────────────────────────────────────────
def _get_device_id():
    import uuid as _uuid
    from pathlib import Path as _P
    _f = _P.home() / ".titan_ultra" / "device_id.txt"
    _f.parent.mkdir(parents=True, exist_ok=True)
    if _f.exists():
        return _f.read_text().strip()
    _did = str(_uuid.uuid4())
    _f.write_text(_did)
    return _did

def _registry_ready():
    return (REGISTRY_GIST_ID  != "PASTE_YOUR_GIST_ID_HERE" and
            REGISTRY_TOKEN != "PASTE_YOUR_GIST_TOKEN_HERE")

@st.cache_data(ttl=3600)
def _fetch_registry_cached():
    try:
        _r = requests.get(
            f"https://api.github.com/gists/{REGISTRY_GIST_ID}",
            headers={"Authorization": f"token {REGISTRY_TOKEN}",
                     "Accept": "application/vnd.github.v3+json"},
            timeout=8
        )
        if _r.status_code == 200:
            _files = _r.json().get("files", {})
            if REGISTRY_FILENAME in _files:
                return _json.loads(_files[REGISTRY_FILENAME]["content"])
    except Exception:
        pass
    return {}

def _load_registry():
    if not _registry_ready():
        return {}
    return _fetch_registry_cached()

def _save_registry(data):
    if not _registry_ready():
        return False
    try:
        _resp = requests.patch(
            f"https://api.github.com/gists/{REGISTRY_GIST_ID}",
            headers={"Authorization": f"token {REGISTRY_TOKEN}",
                     "Accept": "application/vnd.github.v3+json"},
            json={"files": {REGISTRY_FILENAME: {
                "content": _json.dumps(data, indent=2, ensure_ascii=False)
            }}},
            timeout=10
        )
        _fetch_registry_cached.clear()
        return _resp.status_code in (200, 201)
    except Exception:
        return False

def _load_subscription():
    if not _registry_ready(): return {}
    _reg = _load_registry()
    return _reg.get(_get_device_id(), {}).get("subscription", {})

def _save_subscription(tier, txn_id, email, days=30):
    """Save subscription with retry. Returns True on success, False on failure."""
    if not _registry_ready(): return False
    import time as _t_sub
    from datetime import datetime as _dtsub, timedelta as _tdsub
    _reg = _load_registry()
    _did = _get_device_id()
    if _did not in _reg: _reg[_did] = {}
    # Ensure device entry has email + name so cross-device lookup works
    if not _reg[_did].get("email"):
        _reg[_did]["email"] = email.strip().lower()
    if not _reg[_did].get("name"):
        _reg[_did]["name"] = st.session_state.get("user_name_reg", "")
    _now = _dtsub.now()
    _sub_data = {
        "tier": tier,
        "started": _now.isoformat()[:10],
        "expires": (_now + _tdsub(days=days)).isoformat()[:10],
        "txn_id": txn_id,
        "email": email.strip().lower(),
        "billing": "yearly" if days >= 365 else "monthly",
    }
    _reg[_did]["subscription"] = _sub_data
    # Also save to account entry as a second copy — ensures cross-device restore even
    # if the device entry is orphaned after a container restart
    _acc_key = _account_key(email)
    if "_accounts" in _reg and _acc_key in _reg["_accounts"]:
        _reg["_accounts"][_acc_key]["subscription"] = _sub_data.copy()
    # Retry up to 3 times — payment must not be lost silently
    for _attempt in range(3):
        if _save_registry(_reg):
            return True
        if _attempt < 2:
            _t_sub.sleep(1.5)
    return False

def _clear_subscription():
    if not _registry_ready(): return
    _reg = _load_registry()
    _did = _get_device_id()
    if _did in _reg and "subscription" in _reg[_did]:
        del _reg[_did]["subscription"]
        _save_registry(_reg)

def _find_sub_by_email_name(registry, email, name=""):
    """Search all entries for an active subscription matching this email.
    Name check is skipped — email is the unique account identifier in the new auth system.
    Also checks the _accounts section for the backup subscription copy."""
    from datetime import date as _fsd
    _em = email.strip().lower()
    # Check account entry backup first (most reliable — set directly on payment)
    _ak = _account_key(_em)
    _acc_sub = registry.get("_accounts", {}).get(_ak, {}).get("subscription", {})
    if _acc_sub and _acc_sub.get("expires"):
        try:
            if _fsd.today() <= _fsd.fromisoformat(_acc_sub["expires"]):
                return _acc_sub
        except Exception:
            pass
    # Fall back to scanning device entries
    for _k, _entry in registry.items():
        if _k.startswith("_") or not isinstance(_entry, dict):
            continue  # skip _accounts, _shared, and any non-dict entries
        if _entry.get("email", "").strip().lower() == _em:
            _s = _entry.get("subscription", {})
            if _s and _s.get("expires"):
                try:
                    if _fsd.today() <= _fsd.fromisoformat(_s["expires"]):
                        return _s
                except Exception:
                    pass
    return None

def _family_key(email):
    """Stable key shared by all devices logged into the same account (email)."""
    import hashlib as _hsh_fk
    return "fam_" + _hsh_fk.sha256(email.strip().lower().encode()).hexdigest()[:16]

def _account_key(email):
    """Registry dict key for this email's account entry."""
    import hashlib as _hsh_ak
    return "acc_" + _hsh_ak.sha256(email.strip().lower().encode()).hexdigest()[:20]

def _hash_password(password):
    import hashlib as _hsh_pw
    return _hsh_pw.sha256(password.strip().encode()).hexdigest()

def _get_account(registry, email):
    """Return account dict for this email or None."""
    return registry.get("_accounts", {}).get(_account_key(email))

def _create_account(name, email, password):
    """Create a new account in the Gist _accounts section."""
    if not _registry_ready():
        return False
    import base64 as _b64acc
    from datetime import datetime as _dta
    _reg = _load_registry()
    if _get_account(_reg, email):
        return False  # already exists
    if "_accounts" not in _reg:
        _reg["_accounts"] = {}
    _reg["_accounts"][_account_key(email)] = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "password_hash": _hash_password(password),
        "password_b64": _b64acc.b64encode(password.strip().encode()).decode(),
        "registered_at": _dta.now().isoformat(),
    }
    _did = _get_device_id()
    if _did not in _reg:
        _reg[_did] = {}
    _reg[_did]["email"] = email.strip().lower()
    _reg[_did]["name"] = name.strip()
    _reg[_did]["account_verified"] = True
    _reg[_did].setdefault("registered_at", _dta.now().isoformat())
    _reg[_did].setdefault("banned", False)
    _reg[_did].setdefault("timeout_until", None)
    _reg[_did]["last_seen"] = _dta.now().isoformat()
    _save_registry(_reg)
    return True

def _verify_login(email, password):
    """Returns (registry, account_dict) if credentials match, else (registry, None)."""
    _reg = _load_registry()
    _acc = _get_account(_reg, email)
    if _acc and _acc.get("password_hash") == _hash_password(password):
        return _reg, _acc
    return _reg, None

def _link_device_to_account(reg, email):
    """Mark device as verified for this account (persists auto-login for this container)."""
    if not _registry_ready():
        return
    from datetime import datetime as _dtl
    _did = _get_device_id()
    _acc = _get_account(reg, email)
    if _did not in reg:
        reg[_did] = {}
    reg[_did]["email"] = email.strip().lower()
    # Save name so _find_sub_by_email_name can still match this device entry
    if _acc and _acc.get("name"):
        reg[_did]["name"] = _acc["name"]
    reg[_did]["account_verified"] = True
    reg[_did]["last_seen"] = _dtl.now().isoformat()
    _save_registry(reg)

def _logout_device():
    """Remove account link from this device entry in Gist."""
    if not _registry_ready():
        return
    _reg = _load_registry()
    _did = _get_device_id()
    if _did in _reg:
        _reg[_did].pop("account_verified", None)
        _reg[_did].pop("email", None)
        _reg[_did].pop("name", None)
        _reg[_did].pop("subscription", None)
        _save_registry(_reg)

@st.cache_data(ttl=300)
def _fetch_chats_cached():
    try:
        _r = requests.get(
            f"https://api.github.com/gists/{REGISTRY_GIST_ID}",
            headers={"Authorization": f"token {REGISTRY_TOKEN}",
                     "Accept": "application/vnd.github.v3+json"},
            timeout=8
        )
        if _r.status_code == 200:
            _files = _r.json().get("files", {})
            if CHATS_FILENAME in _files:
                return _json.loads(_files[CHATS_FILENAME]["content"])
    except Exception:
        pass
    return {}

def _load_shared_history(family_key):
    if not _registry_ready():
        return []
    try:
        return _fetch_chats_cached().get(family_key, [])
    except Exception:
        return []

def _save_shared_history(family_key, history):
    """Save history to Gist in a background thread — non-blocking."""
    if not _registry_ready():
        return
    import threading as _th_ch
    def _do():
        try:
            _h = history[:30]
            _trimmed = []
            for _sess in _h:
                _s = dict(_sess)
                _msgs = []
                for _m in _s.get("messages", []):
                    _mc = dict(_m)
                    if isinstance(_mc.get("content"), str) and len(_mc["content"]) > 3000:
                        _mc["content"] = _mc["content"][:3000] + "…"
                    _msgs.append(_mc)
                _s["messages"] = _msgs
                _trimmed.append(_s)
            _cur = _fetch_chats_cached() or {}
            _cur[family_key] = _trimmed
            requests.patch(
                f"https://api.github.com/gists/{REGISTRY_GIST_ID}",
                headers={"Authorization": f"token {REGISTRY_TOKEN}",
                         "Accept": "application/vnd.github.v3+json"},
                json={"files": {CHATS_FILENAME: {
                    "content": _json.dumps(_cur, indent=2, ensure_ascii=False)
                }}},
                timeout=10
            )
            _fetch_chats_cached.clear()
        except Exception:
            pass
    _th_ch.Thread(target=_do, daemon=True).start()

def _register_this_device(name):
    if not _registry_ready() or not name:
        return
    from datetime import datetime as _dtr
    _did = _get_device_id()
    _reg = _load_registry()
    if _did not in _reg:
        _reg[_did] = {
            "name": name,
            "registered_at": _dtr.now().isoformat(),
            "banned": False,
            "timeout_until": None,
            "last_seen": _dtr.now().isoformat()
        }
    else:
        _reg[_did]["name"] = name
        _reg[_did]["last_seen"] = _dtr.now().isoformat()
    _save_registry(_reg)

# ── Owner check (Sushanth = full access, others = locked) ────────────────────
_saved_key    = _load_saved_key()
_saved_memory = _load_memory()

import hashlib as _hlib_owner
from pathlib import Path as _OwnerPath

# SHA-256 hash of the owner's secret code — set by running: python titan_unlock.py --init
_OWNER_HASH = "PASTE_OWNER_HASH_HERE"
_OWNER_AUTH_FILE = _OwnerPath.home() / ".titan_ultra" / ".owner_auth"

# ── Titan Devices Registry — set these up once (see instructions below) ───────
# 1. Create a SECRET GitHub Gist at https://gist.github.com with a file named titan_devices.json containing: {}
# 2. Create a GitHub token at https://github.com/settings/tokens with only "gist" scope
# 3. Paste the Gist ID and token below, then push to GitHub
REGISTRY_GIST_ID  = "0ae47b140415e738f3b8d1e5b0e17ecc"
import base64 as _b64
REGISTRY_TOKEN    = _b64.b64decode("Z2hwX1FETFc1RUVLc3A5ck9najhRMGtxUjhGMDFuWE5ndjBLV0w3Qg==").decode()
REGISTRY_FILENAME = "titan_devices.json"
CHATS_FILENAME    = "titan_chats.json"

def _check_owner_auth():
    if not _OWNER_AUTH_FILE.exists():
        return False
    try:
        return _OWNER_AUTH_FILE.read_text().strip() == _OWNER_HASH
    except Exception:
        return False

_IS_OWNER = _check_owner_auth() or _saved_memory.get("name", "").strip().lower() == "sushanth"

# ── Usage limit (2 hrs for non-owners, resets after 5 hrs) ───────────────────
import time as _time_mod, json as _json_usage
from pathlib import Path as _Path_usage
_USAGE_FILE = _Path_usage.home() / ".titan_ultra" / "usage_tracking.json"

def _load_usage_data():
    try:
        with open(_USAGE_FILE, "r") as _f:
            return _json_usage.load(_f)
    except Exception:
        return {"total_seconds": 0.0, "limit_hit_at": None}

def _save_usage_data(data):
    _USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_USAGE_FILE, "w") as _f:
        _json_usage.dump(data, _f)

_USAGE_LIMIT_SECONDS = 2 * 3600   # 2 hours
_USAGE_RESET_SECONDS = 5 * 3600   # reset after 5 hours

if not _IS_OWNER:
    _usage = _load_usage_data()
    _now_ts = _time_mod.time()

    # ── ONE early Gist load — registration + subscription + ban — runs once per session ──
    # Must happen BEFORE _tier_bypass so paid Pro/Max users bypass the time limit correctly
    if _registry_ready() and not st.session_state.get("_gist_loaded"):
        try:
            from datetime import date as _gld, datetime as _gldt
            _gl_did   = _get_device_id()
            _gl_reg   = _load_registry()
            _gl_entry = _gl_reg.get(_gl_did, {})

            # ── Ban check ─────────────────────────────────────────────────────
            if _gl_entry.get("banned"):
                st.error("🚫 **You have been removed from Titan Ultra by the administrator.**\n\nContact the owner if you think this is a mistake.")
                st.stop()

            # ── Timeout check ─────────────────────────────────────────────────
            _tout_str = _gl_entry.get("timeout_until")
            if _tout_str:
                _tout_dt = _gldt.fromisoformat(_tout_str)
                if _gldt.now() < _tout_dt:
                    _tsecs = int((_tout_dt - _gldt.now()).total_seconds())
                    st.warning("⏳ **You have been temporarily timed out by the administrator.**")
                    import streamlit.components.v1 as _cv1_tout
                    _cv1_tout.html(f"""
<div style="text-align:center;padding:16px 0;font-family:-apple-system,Segoe UI,sans-serif">
  <div style="font-size:.8rem;color:#f59e0b;letter-spacing:2px;margin-bottom:8px">⏳ TIMEOUT — COME BACK IN</div>
  <div id="tout_timer" style="font-size:2.8rem;font-weight:900;color:#f87171;letter-spacing:5px"></div>
</div>
<script>
var r={_tsecs};
function f(n){{return n.toString().padStart(2,'0');}}
function tick(){{
  if(r<=0){{document.getElementById('tout_timer').innerHTML='00:00:00';setTimeout(function(){{window.location.reload();}},1500);return;}}
  var h=Math.floor(r/3600),m=Math.floor((r%3600)/60),s=r%60;
  document.getElementById('tout_timer').innerHTML=f(h)+':'+f(m)+':'+f(s);
  r--;setTimeout(tick,1000);
}}
tick();
</script>""", height=120)
                    st.stop()

            # ── Auto-login: device was verified for an account in this container ─
            if _gl_entry.get("account_verified") and _gl_entry.get("email"):
                _gl_acc = _get_account(_gl_reg, _gl_entry["email"])
                if _gl_acc:
                    st.session_state["user_registered"] = True
                    st.session_state["user_name_reg"]   = _gl_acc["name"]
                    st.session_state["user_email_reg"]  = _gl_acc["email"]
                    # ── Load shared history ────────────────────────────────────
                    _gl_fkey = _family_key(_gl_acc["email"])
                    st.session_state["_family_key"] = _gl_fkey
                    if not st.session_state.get("_gist_history"):
                        _gl_hist = _load_shared_history(_gl_fkey)
                        if _gl_hist:
                            st.session_state["_gist_history"] = _gl_hist
                    # ── Restore subscription ───────────────────────────────────
                    _gl_sub = _gl_entry.get("subscription", {})
                    if not _gl_sub:
                        _gl_sub = _find_sub_by_email_name(_gl_reg, _gl_acc["email"], _gl_acc["name"]) or {}
                        if _gl_sub:
                            _gl_reg[_gl_did]["subscription"] = _gl_sub.copy()
                            _save_registry(_gl_reg)
                    if _gl_sub and _gl_sub.get("expires"):
                        _gl_exp = _gld.fromisoformat(_gl_sub["expires"])
                        if _gld.today() <= _gl_exp:
                            st.session_state["titan_tier"]            = _gl_sub.get("tier", "basic")
                            st.session_state["_subscription_active"]  = True
                            st.session_state["_subscription_expires"] = _gl_sub["expires"]
                            st.session_state["_subscription_expired"] = False
                        else:
                            st.session_state["_subscription_expired"] = True
                            st.session_state["_expired_tier"]         = _gl_sub.get("tier", "pro").capitalize()

            # ── Update last_seen ───────────────────────────────────────────────
            if _gl_did not in _gl_reg:
                _gl_reg[_gl_did] = {}
            _gl_reg[_gl_did]["last_seen"] = _gldt.now().isoformat()
            _save_registry(_gl_reg)

            st.session_state["_gist_loaded"] = True
            st.session_state["_sub_checked"] = True
        except Exception:
            pass

    # Reset if 5 hrs have passed since limit was hit
    if _usage["limit_hit_at"] and (_now_ts - _usage["limit_hit_at"]) >= _USAGE_RESET_SECONDS:
        _usage = {"total_seconds": 0.0, "limit_hit_at": None}
        _save_usage_data(_usage)

    # Track active session time
    if "usage_session_start" not in st.session_state:
        st.session_state.usage_session_start = _now_ts
    else:
        _elapsed_this_session = _now_ts - st.session_state.usage_session_start
        _usage["total_seconds"] = _usage.get("total_seconds", 0.0) + _elapsed_this_session
        st.session_state.usage_session_start = _now_ts
        if _usage["total_seconds"] >= _USAGE_LIMIT_SECONDS and not _usage["limit_hit_at"]:
            _usage["limit_hit_at"] = _now_ts
        _save_usage_data(_usage)

    # Pro/Max tiers bypass the time limit — tier is now correctly restored above
    _tier_bypass = st.session_state.get("titan_tier", "basic") in ("pro", "max")
    _USER_HIT_LIMIT = _usage.get("limit_hit_at") is not None and not _tier_bypass
else:
    _USER_HIT_LIMIT = False

# ── Fresh-session detection ───────────────────────────────────────────────────
# On a brand-new visit (new tab OR reconnect after close), reset to empty chat.
# We use a query-param nonce: JS writes a unique nonce to the URL on every fresh
# browser page-load; Python compares it against the last known nonce.
_qp        = st.query_params
_url_nonce = _qp.get("_tn", "")          # nonce currently in the URL
_ss_nonce  = st.session_state.get("_titan_nonce", "")

if _url_nonce and _url_nonce != _ss_nonce:
    # URL has a NEW nonce we haven't seen yet → genuine fresh page load
    import time as _t
    st.session_state["_titan_nonce"]  = _url_nonce
    st.session_state["chat_sessions"] = [{"id": int(_t.time()), "title": "New Chat", "messages": []}]
    st.session_state["active_session"] = 0

# Remaining one-time defaults (only set if missing)
for k, v in [("api_key", _saved_key), ("titan_memory", _saved_memory),
             ("quick_q", ""), ("speed", "fast"), ("_titan_mode", "normal"),
             ("chat_sessions", [{"id": 0, "title": "New Chat", "messages": []}]),
             ("active_session", 0), ("_titan_nonce", ""),
             ("chat_active_tool", ""), ("ep_last_paper", ""), ("ep_last_name", "exam"),
             ("ep_generating", False),
             ("flashcards", []), ("card_index", 0), ("card_flipped", False),
             ("card_known", set()), ("card_review", set()), ("fc_review_mode", False),
             ("fc_study_all", False),
             ("weather_query", ""), ("weather_name", ""), ("weather_data", None),
             ("weather_aqi", None), ("weather_summary", ""), ("weather_state", ""),
             ("notebook_mode", False), ("library_mode", False), ("schedule_mode", False), ("tasks_mode", False), ("notebook_sources", []),
             ("notebook_chat", []), ("notebook_generated", {}),
             ("nb_card_index", 0), ("nb_card_flipped", False), ("nb_mode", "organise"),
             ("diagram_cache", {}),
             ("_sys_health_cache", {}),
             ("news_mode", False), ("news_cache", {}),
             ("_pending_pdf", None),
             ("openai_key", _load_img_key()),
             ("image_cache", {}),
             ("connected_apps", _load_connected_apps()),
             ("show_titan_features", False),
             ("titan_tier", "basic"),
             ("show_upgrade", False),
             ("show_titan_code", False),
             ("user_registered", False),
             ("user_name_reg", ""),
             ("user_email_reg", ""),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# (Registration + subscription are restored in the early Gist load above, before usage check)


def cur_msgs():
    return st.session_state.chat_sessions[st.session_state.active_session]["messages"]

def _make_session_title(text):
    import re as _re
    t = text.strip()
    t = _re.sub(
        r'^(?:please\s+)?(?:can\s+you\s+|could\s+you\s+|would\s+you\s+)?'
        r'(?:tell\s+me\s+(?:about\s+)?|explain\s+(?:to\s+me\s+)?|'
        r'what\s+(?:is|are|was|were)\s+(?:the\s+)?|'
        r'what\'s\s+(?:the\s+)?|'
        r'who\s+(?:is|was|are|were)\s+|'
        r'how\s+(?:do|does|did|to|can|should)\s+(?:i\s+|you\s+)?|'
        r'why\s+(?:is|are|does|do|did)\s+(?:the\s+)?|'
        r'where\s+(?:is|are|was|were)\s+(?:the\s+)?|'
        r'when\s+(?:is|are|was|were|did)\s+(?:the\s+)?|'
        r'give\s+me\s+(?:a\s+|an\s+|the\s+)?|'
        r'list\s+(?:the\s+|all\s+)?|'
        r'show\s+me\s+(?:a\s+|an\s+|the\s+)?)',
        '', t, flags=_re.IGNORECASE).strip().rstrip('?.,!')
    t = t.title() if t else text[:30].title()
    return (t[:38] + '…') if len(t) > 38 else t

def set_msgs(msgs):
    st.session_state.chat_sessions[st.session_state.active_session]["messages"] = msgs
    _save_chat_sessions()

# ── Image generation background poller ────────────────────────────────────────

# ── Ollama check ──────────────────────────────────────────────────────────────
OLLAMA_SUGGESTED = {
    "qwen3:4b":   "🧠 Qwen 3 4B — Reasoning ON · 32K context",
    "moondream":  "👁️ Moondream — Vision · Fast",
}

@st.cache_data(ttl=3600)
def check_ollama():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=1)
        if r.status_code == 200:
            return True, [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return False, []

def start_ollama_background():
    """Try to launch the Ollama background service if it's installed but not running."""
    import os as _os_o, subprocess as _sp_o, time as _t_o
    _candidates = [
        _os_o.path.expandvars(r'%LOCALAPPDATA%\Programs\Ollama\ollama app.exe'),
        _os_o.path.expandvars(r'%LOCALAPPDATA%\Programs\Ollama\ollama.exe'),
        r'C:\Program Files\Ollama\ollama app.exe',
        r'C:\Program Files\Ollama\ollama.exe',
    ]
    _exe = next((p for p in _candidates if _os_o.path.exists(p)), None)
    if not _exe:
        # Fall back to PATH lookup
        try:
            _r = _sp_o.run(['where', 'ollama'], capture_output=True, text=True, timeout=3)
            if _r.returncode == 0 and _r.stdout.strip():
                _exe = _r.stdout.strip().splitlines()[0].strip()
        except Exception:
            pass
    if not _exe:
        return False
    try:
        _flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        if _exe.lower().endswith('ollama app.exe'):
            _sp_o.Popen([_exe], creationflags=_flags,
                        stdout=_sp_o.DEVNULL, stderr=_sp_o.DEVNULL, close_fds=True)
        else:
            _sp_o.Popen([_exe, 'serve'], creationflags=_flags,
                        stdout=_sp_o.DEVNULL, stderr=_sp_o.DEVNULL, close_fds=True)
        # Wait briefly for it to come up
        for _ in range(10):
            _t_o.sleep(0.5)
            try:
                if requests.get("http://localhost:11434/api/tags", timeout=2).status_code == 200:
                    return True
            except Exception:
                continue
        return False
    except Exception:
        return False

def pull_ollama_model(name):
    try:
        with requests.post("http://localhost:11434/api/pull",
                           json={"name": name, "stream": False}, timeout=600) as r:
            return r.status_code == 200
    except Exception:
        return False

ollama_models = []
ollama_reachable = False

# ── Internet check ────────────────────────────────────────────────────────────
def _has_internet():
    try:
        requests.get("https://api.groq.com", timeout=3)
        return True
    except Exception:
        return False

# ── Fresh-load nonce injector ─────────────────────────────────────────────────
# Runs once in the browser on every genuine page-load (not on Streamlit reruns).
# Sets ?_tn=<random> in the URL so Python can detect a new visit.
st.html("""
<script>
(function() {
    // sessionStorage key — survives reruns (same WebSocket) but NOT a new tab/refresh
    var NONCE_KEY = '__titan_nonce';
    var stored    = window.sessionStorage.getItem(NONCE_KEY);
    var url       = new URL(window.location.href);
    var urlNonce  = url.searchParams.get('_tn');

    if (!stored) {
        // First load in this browser tab — generate & store a fresh nonce
        var nonce = Math.random().toString(36).slice(2) + Date.now().toString(36);
        window.sessionStorage.setItem(NONCE_KEY, nonce);
        url.searchParams.set('_tn', nonce);
        window.history.replaceState(null, '', url.toString());
    } else if (urlNonce !== stored) {
        // URL nonce doesn't match stored → put the stored nonce back in the URL
        // (Streamlit might have stripped query params on rerender)
        url.searchParams.set('_tn', stored);
        window.history.replaceState(null, '', url.toString());
    }
    // else: nonce already consistent — no action needed
})();
</script>
<script>
// Remove Streamlit's built-in sidebar top padding so TITAN ULTRA is flush to the top
(function _sbPad() {
    function fix() {
        var sb = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (!sb) return;
        // Walk into the first few nested divs and zero their padding/margin
        var el = sb;
        for (var i = 0; i < 6; i++) {
            if (el) {
                el.style.paddingTop = '0px';
                el.style.marginTop  = '0px';
                el = el.firstElementChild;
            }
        }
    }
    fix();
    setTimeout(fix, 300);
    setTimeout(fix, 800);
})();
</script>
""")

# ── Inject tier CSS ──────────────────────────────────────────────────────────
_inject_tier_css()

# ── First-time registration (name + email) ────────────────────────────────────
if not _IS_OWNER and not st.session_state.get("user_registered"):
    st.markdown("""
<style>
.auth-wrap { display:flex; flex-direction:column; align-items:center;
             justify-content:center; min-height:55vh; text-align:center; }
.auth-label { color:#e8e8e8 !important; font-size:0.84rem !important;
              font-weight:600 !important; margin-bottom:4px !important;
              display:block !important; text-align:left !important; }
</style>
<div class="auth-wrap">
  <div style='font-size:2.4rem;margin-bottom:10px'>🔱</div>
  <div style='font-size:1.65rem;font-weight:700;color:#fff;margin-bottom:4px'>Titan Ultra</div>
  <div style='font-size:.82rem;color:#555;margin-bottom:0'>Login to your account or create a new one</div>
</div>
""", unsafe_allow_html=True)

    _ac1, _ac2, _ac3 = st.columns([1, 2, 1])
    with _ac2:
        st.markdown("""<style>
.stTabs [data-baseweb="tab-list"]{gap:8px;}
.stTabs [data-baseweb="tab"]{background:rgba(255,255,255,0.06);border-radius:10px;
  color:#a0a0c0;font-weight:600;padding:10px 0;flex:1;justify-content:center;}
.stTabs [aria-selected="true"]{background:#7c3aed !important;color:#fff !important;}
</style>""", unsafe_allow_html=True)
        _tab_li, _tab_reg = st.tabs(["Log In", "Register"])

        with _tab_li:
            # ── LOGIN FORM ───────────────────────────────────────────────────
            with st.form("_login_form", clear_on_submit=False):
                st.markdown("<span class='auth-label'>Email</span>", unsafe_allow_html=True)
                _li_email = st.text_input("", placeholder="your@email.com",
                                          key="_li_email", label_visibility="collapsed")
                st.markdown("<span class='auth-label' style='margin-top:8px;display:block'>Password</span>",
                            unsafe_allow_html=True)
                _li_pass = st.text_input("", placeholder="Enter your password",
                                         type="password", key="_li_pass", label_visibility="collapsed")
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                _li_submit = st.form_submit_button("Log In →", use_container_width=True)
                if _li_submit:
                    if _li_email.strip() and "@" in _li_email and _li_pass.strip():
                        _li_reg, _li_acc = _verify_login(_li_email.strip(), _li_pass.strip())
                        if _li_acc:
                            # Successful login
                            st.session_state["user_registered"]  = True
                            st.session_state["user_name_reg"]    = _li_acc["name"]
                            st.session_state["user_email_reg"]   = _li_acc["email"]
                            if not st.session_state.titan_memory.get("name"):
                                st.session_state.titan_memory["name"] = _li_acc["name"].split()[0]
                            # Link device + load subscription + history
                            _link_device_to_account(_li_reg, _li_acc["email"])
                            _li_fkey = _family_key(_li_acc["email"])
                            st.session_state["_family_key"] = _li_fkey
                            _li_hist = _load_shared_history(_li_fkey)
                            if _li_hist:
                                st.session_state["_gist_history"] = _li_hist
                            # Pull subscription from this account's existing device entries
                            _li_sub = _find_sub_by_email_name(_li_reg, _li_acc["email"], _li_acc["name"]) or {}
                            if _li_sub:
                                _li_did = _get_device_id()
                                _li_reg[_li_did]["subscription"] = _li_sub.copy()
                                _save_registry(_li_reg)
                                st.session_state["titan_tier"]            = _li_sub.get("tier", "basic")
                                st.session_state["_subscription_active"]  = True
                                st.session_state["_subscription_expires"] = _li_sub.get("expires", "")
                                st.session_state["_subscription_expired"] = False
                            st.session_state["_gist_loaded"] = True
                            st.session_state["_sub_checked"] = True
                            st.session_state["_auth_just_done"] = True
                        else:
                            st.error("Incorrect email or password.")
                    else:
                        st.error("Please enter a valid email and password.")
        with _tab_reg:
            # ── REGISTER FORM ────────────────────────────────────────────────
            with st.form("_register_form", clear_on_submit=False):
                st.markdown("<span class='auth-label'>Name</span>", unsafe_allow_html=True)
                _ri_name = st.text_input("", placeholder="e.g. Rahul Sharma",
                                         key="_ri_name", label_visibility="collapsed")
                st.markdown("<span class='auth-label' style='margin-top:8px;display:block'>Email</span>",
                            unsafe_allow_html=True)
                _ri_email = st.text_input("", placeholder="e.g. rahul@gmail.com",
                                          key="_ri_email", label_visibility="collapsed")
                st.markdown("<span class='auth-label' style='margin-top:8px;display:block'>Password</span>",
                            unsafe_allow_html=True)
                _ri_pass = st.text_input("", placeholder="Create a password",
                                         type="password", key="_ri_pass", label_visibility="collapsed")
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                _ri_submit = st.form_submit_button("Create Account →", use_container_width=True)
                if _ri_submit:
                    if _ri_name.strip() and _ri_email.strip() and "@" in _ri_email and _ri_pass.strip():
                        if len(_ri_pass.strip()) < 6:
                            st.error("Password must be at least 6 characters.")
                        else:
                            if _registry_ready():
                                try:
                                    _ri_reg = _load_registry()
                                    if _get_account(_ri_reg, _ri_email.strip()):
                                        st.error("An account with this email already exists. Please log in.")
                                    else:
                                        _ok = _create_account(_ri_name.strip(), _ri_email.strip(), _ri_pass.strip())
                                        if _ok:
                                            st.session_state["user_registered"]  = True
                                            st.session_state["user_name_reg"]    = _ri_name.strip()
                                            st.session_state["user_email_reg"]   = _ri_email.strip().lower()
                                            if not st.session_state.titan_memory.get("name"):
                                                st.session_state.titan_memory["name"] = _ri_name.strip().split()[0]
                                            _ri_fkey = _family_key(_ri_email.strip())
                                            st.session_state["_family_key"] = _ri_fkey
                                            # Check if any device with this email already has a subscription
                                            _ri_reg2 = _load_registry()
                                            _ri_sub = _find_sub_by_email_name(_ri_reg2, _ri_email.strip(), _ri_name.strip()) or {}
                                            if _ri_sub:
                                                _ri_did = _get_device_id()
                                                _ri_reg2[_ri_did]["subscription"] = _ri_sub.copy()
                                                _save_registry(_ri_reg2)
                                                st.session_state["titan_tier"]            = _ri_sub.get("tier", "basic")
                                                st.session_state["_subscription_active"]  = True
                                                st.session_state["_subscription_expires"] = _ri_sub.get("expires", "")
                                                st.session_state["_subscription_expired"] = False
                                            _ri_hist = _load_shared_history(_ri_fkey)
                                            if _ri_hist:
                                                st.session_state["_gist_history"] = _ri_hist
                                            st.session_state["_gist_loaded"] = True
                                            st.session_state["_sub_checked"] = True
                                            st.session_state["_auth_just_done"] = True
                                        else:
                                            st.error("Could not create account. Please try again.")
                                except Exception:
                                    st.error("Something went wrong. Please try again.")
                            else:
                                # Offline fallback
                                st.session_state["user_registered"] = True
                                st.session_state["user_name_reg"]   = _ri_name.strip()
                                st.session_state["user_email_reg"]  = _ri_email.strip()
                                st.session_state["_auth_just_done"] = True
                    else:
                        st.error("Please fill in all fields with a valid email.")
    # Rerun from outside the tabs/forms context — avoids Streamlit tab-state blank screen
    if st.session_state.get("_auth_just_done"):
        del st.session_state["_auth_just_done"]
        st.rerun()
    st.stop()

# ── Upgrade Pricing Page ──────────────────────────────────────────────────────
def _render_upgrade_page():
    _tier = st.session_state.get("titan_tier", "basic")
    st.markdown("""
<style>
.tu-pricing-wrap { padding: 10px 0 40px 0; }
.tu-plan-card {
    background: #111111;
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 28px 20px 24px 20px;
    text-align: center;
    position: relative;
    transition: box-shadow .2s;
}
.tu-plan-card.pro { border-color: #7c3aed; }
.tu-plan-card.max { border-color: #f59e0b; background: #0f0f0f; }
.tu-badge {
    position: absolute;
    top: -13px; left: 50%;
    transform: translateX(-50%);
    padding: 3px 18px;
    border-radius: 20px;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}
.tu-badge.rec { background: #7c3aed; color: #fff; }
.tu-badge.ult { background: #f59e0b; color: #000; }
.tu-plan-name { font-size: 1.1rem; font-weight: 700; margin-bottom: 6px; }
.tu-plan-price { font-size: 2.1rem; font-weight: 900; margin: 12px 0 4px; }
.tu-plan-sub { font-size: .75rem; color: #666; margin-bottom: 18px; }
.tu-feat { font-size: .82rem; text-align: left; padding: 4px 0; border-bottom: 1px solid #1e1e1e; }
.tu-feat:last-child { border-bottom: none; }
.tu-buy-btn {
    margin-top: 18px;
    width: 100%;
    padding: 11px 0;
    border-radius: 10px;
    border: none;
    font-size: .9rem;
    font-weight: 700;
    cursor: pointer;
    transition: opacity .15s;
}
.tu-buy-btn:hover { opacity: .85; }
.tu-buy-basic { background: #1e1e1e; color: #888; border: 1px solid #2a2a2a; }
.tu-buy-pro { background: #7c3aed; color: #fff; }
.tu-buy-max { background: linear-gradient(135deg,#f59e0b,#d97706); color: #000; }
</style>
""", unsafe_allow_html=True)

    # Header row
    _back_col, _title_col = st.columns([1, 5])
    with _back_col:
        if st.button("← Back", key="_upgrade_back"):
            st.session_state.show_upgrade = False
            st.rerun()
    with _title_col:
        st.markdown("<h2 style='margin:0;padding:4px 0 0 0'>🔱 Upgrade Titan Ultra</h2>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── If subscription is active, show locked plan — no switching allowed ────
    _up_sub_active  = st.session_state.get("_subscription_active", False)
    _up_sub_expires = st.session_state.get("_subscription_expires", "")
    if _up_sub_active and _tier in ("pro", "max"):
        _lk_clr  = "#f59e0b" if _tier == "max" else "#a78bfa"
        _lk_name = "Titan Ultra Max" if _tier == "max" else "Titan Ultra Pro"
        _lk_icon = "⭐" if _tier == "max" else "🔱"
        st.markdown(f"""
<div style='background:#111;border:2px solid {_lk_clr};border-radius:16px;
     padding:32px 24px;text-align:center;max-width:420px;margin:0 auto'>
  <div style='font-size:2.5rem'>{_lk_icon}</div>
  <div style='font-size:1.4rem;font-weight:800;color:{_lk_clr};margin:10px 0 4px'>{_lk_name}</div>
  <div style='font-size:.85rem;color:#888;margin-bottom:18px'>Your active subscription</div>
  {"<div style='font-size:.8rem;color:#555;background:#0a0a0a;border-radius:8px;padding:8px 16px;display:inline-block'>expires " + _up_sub_expires + "</div>" if _up_sub_expires else ""}
  <div style='margin-top:22px;font-size:.82rem;color:#666;line-height:1.6'>
    You are locked into this plan until it expires.<br>
    After expiry you can choose a new plan.
  </div>
</div>
""", unsafe_allow_html=True)
        st.stop()

    # Monthly / Yearly toggle
    _billing = st.radio("Billing", ["Monthly", "Yearly"], horizontal=True,
                        key="_upgrade_billing", label_visibility="collapsed")
    _yearly = _billing == "Yearly"
    if _yearly:
        st.markdown(
            "<div style='text-align:center;font-size:.8rem;color:#22c55e;margin:4px 0 12px'>"
            "💰 <b>Pro:</b> Save ₹1,500 &nbsp;·&nbsp; <b>Max:</b> Save ₹3,000 — with yearly billing</div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='text-align:center;font-size:.78rem;color:#555;margin:4px 0 12px'>"
            "Switch to Yearly and save ₹1,500 (Pro) or ₹3,000 (Max)</div>",
            unsafe_allow_html=True)

    # Pricing
    _basic_price  = "₹0"
    _pro_price    = "₹3,999 / yr" if _yearly else "₹475 / mo"
    _max_price    = "₹26,999 / yr" if _yearly else "₹2,500 / mo"
    _pro_save_html = ("<div style='color:#22c55e;font-size:.72rem;font-weight:700;margin-top:4px'>💰 Save ₹1,500 vs monthly</div>"
                      if _yearly else "")
    _max_save_html = ("<div style='color:#22c55e;font-size:.72rem;font-weight:700;margin-top:4px'>💰 Save ₹3,000 vs monthly</div>"
                      if _yearly else "")
    _sub_active = st.session_state.get("_subscription_active", False)
    _sub_expires = st.session_state.get("_subscription_expires", "")

    _c1, _c2, _c3 = st.columns(3, gap="medium")

    # ── Basic ──
    with _c1:
        _active_basic = _tier == "basic"
        st.markdown(f"""
<div class="tu-plan-card">
  <div class="tu-plan-name" style="color:#e8e8e8">Titan Ultra Basic</div>
  <div class="tu-plan-price" style="color:#e8e8e8">{_basic_price}</div>
  <div class="tu-plan-sub">Free forever</div>
  <div class="tu-feat">✅ Smart AI answers</div>
  <div class="tu-feat">✅ Titan Features, Notebook, Library, Schedule, Tasks</div>
  <div class="tu-feat">✅ Chat history</div>
  <div class="tu-feat">⏱ 2-hour session limit</div>
  <div class="tu-feat">❌ Standard response depth</div>
</div>
""", unsafe_allow_html=True)
        if _active_basic:
            st.markdown("<div style='text-align:center;margin-top:18px;font-size:.8rem;color:#555'>Current plan</div>", unsafe_allow_html=True)
        elif not _sub_active:
            if st.button("Downgrade to Basic", key="_buy_basic", use_container_width=True):
                st.session_state.titan_tier = "basic"
                _clear_subscription()
                st.session_state["_subscription_active"] = False
                st.session_state.show_upgrade = False
                st.rerun()

    # ── Pro ──
    with _c2:
        _active_pro = _tier == "pro"
        st.markdown(f"""
<div class="tu-plan-card pro">
  <div class="tu-badge rec">RECOMMENDED</div>
  <div class="tu-plan-name" style="color:#a78bfa">Titan Ultra Pro</div>
  <div class="tu-plan-price" style="color:#a78bfa">{_pro_price}</div>
  {_pro_save_html}
  <div class="tu-plan-sub" style="margin-top:{'4px' if _yearly else '18px'}">Everything in Basic, plus:</div>
  <div class="tu-feat">✅ <b>Unlimited</b> access — no time limit</div>
  <div class="tu-feat">✅ <b>Deeper</b>, more detailed answers</div>
  <div class="tu-feat">✅ AI Image Generation</div>
  <div class="tu-feat">✅ AI Video Generation</div>
  <div class="tu-feat">✅ Pro badge + purple UI</div>
</div>
""", unsafe_allow_html=True)
        if _active_pro:
            _pro_exp = f" · expires {_sub_expires}" if _sub_expires else ""
            st.markdown(f"<div style='text-align:center;margin-top:18px;font-size:.8rem;color:#a78bfa'>✓ Current plan{_pro_exp}</div>", unsafe_allow_html=True)

    # ── Max ──
    with _c3:
        _active_max = _tier == "max"
        st.markdown(f"""
<div class="tu-plan-card max">
  <div class="tu-badge ult">ULTIMATE</div>
  <div class="tu-plan-name" style="color:#fbbf24">Titan Ultra Max</div>
  <div class="tu-plan-price" style="color:#fbbf24">{_max_price}</div>
  {_max_save_html}
  <div class="tu-plan-sub" style="margin-top:{'4px' if _yearly else '18px'}">Everything in Pro, plus:</div>
  <div class="tu-feat">✅ <b>Ultimate</b> answer quality</div>
  <div class="tu-feat">✅ Hyper-realistic AI images &amp; videos</div>
  <div class="tu-feat">✅ <b>Titan Code</b> — AI coding terminal</div>
  <div class="tu-feat">✅ Deepest reasoning on every question</div>
  <div class="tu-feat">✅ Gold premium UI + Max badge</div>
</div>
""", unsafe_allow_html=True)
        if _active_max:
            _max_exp = f" · expires {_sub_expires}" if _sub_expires else ""
            st.markdown(f"<div style='text-align:center;margin-top:18px;font-size:.8rem;color:#fbbf24'>✓ Current plan{_max_exp}</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='text-align:center;font-size:1rem;font-weight:700;margin-bottom:12px'>💳 Pay with PhonePe</div>", unsafe_allow_html=True)

    _pay_col1, _pay_col2, _pay_col3 = st.columns([1,2,1])
    with _pay_col2:
        _prefill_email = st.session_state.get("user_email_reg", "")
        _user_email = st.text_input("Your email address", value=_prefill_email,
                                    placeholder="Enter your email to continue",
                                    key="_upgrade_email", label_visibility="visible")
        _selected_plan = st.radio("Select plan", ["Titan Ultra Pro", "Titan Ultra Max"],
                                  key="_pay_plan", label_visibility="collapsed", horizontal=True)
        _is_yearly = "Yearly" in _billing
        if _selected_plan == "Titan Ultra Pro":
            _pay_amount = 3999 if _is_yearly else 475
            _plan_label = f"Titan Ultra Pro ({'Yearly' if _is_yearly else 'Monthly'})"
        else:
            _pay_amount = 24999 if _is_yearly else 2500
            _plan_label = f"Titan Ultra Max ({'Yearly' if _is_yearly else 'Monthly'})"

        _upi_id = "sanjaygirijala16@ibl"
        _upi_link = f"upi://pay?pa={_upi_id}&pn=Titan+Ultra&am={_pay_amount}&cu=INR&tn={_plan_label.replace(' ', '+')}"
        _phonepe_link = f"intent://pay?pa={_upi_id}&pn=Titan+Ultra&am={_pay_amount}&cu=INR&tn={_plan_label.replace(' ', '+')}#Intent;scheme=upi;package=com.phonepe.app;end"

        if _user_email and "@" in _user_email:
            st.markdown(f"""
<div style='background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:16px;text-align:center;margin-bottom:12px'>
  <div style='font-size:.8rem;color:#888;margin-bottom:4px'>Amount to pay</div>
  <div style='font-size:2rem;font-weight:900;color:#22c55e'>₹{_pay_amount:,}</div>
  <div style='font-size:.75rem;color:#555;margin-top:4px'>{_plan_label}</div>
</div>
""", unsafe_allow_html=True)
            st.link_button("📱 Pay with PhonePe / UPI", _upi_link, use_container_width=True)
            st.markdown("<div style='text-align:center;font-size:.7rem;color:#555;margin:6px 0'>Opens PhonePe, GPay, Paytm or any UPI app</div>", unsafe_allow_html=True)
            _txn_id = st.text_input("After paying, enter your Transaction ID / UTR number:",
                                     placeholder="e.g. 428371920847", key="_txn_id_input")
            if st.button("✅ Confirm Payment", key="_confirm_pay", use_container_width=True):
                if _txn_id.strip():
                    _tier_key  = "pro" if "Pro" in _selected_plan else "max"
                    _sub_days  = 365 if _is_yearly else 30
                    _sub_label = "1 year" if _is_yearly else "1 month"
                    from datetime import datetime as _pay_dt, timedelta as _pay_td
                    _sub_expires = (_pay_dt.now() + _pay_td(days=_sub_days)).isoformat()[:10]
                    # Save to Gist with retry — if this fails, user's money must not be lost
                    _pay_saved = _save_subscription(_tier_key, _txn_id.strip(), _user_email, days=_sub_days)
                    if _pay_saved:
                        st.session_state.titan_tier               = _tier_key
                        st.session_state["_subscription_active"]  = True
                        st.session_state["_subscription_expired"] = False
                        st.session_state["_subscription_expires"] = _sub_expires
                        st.session_state["_sub_checked"]          = True
                        st.session_state["_gist_loaded"]          = True
                        st.session_state.show_upgrade = False
                        st.success(f"✅ {_plan_label} activated for {_sub_label}. Your access is now unlocked.")
                        st.rerun()
                    else:
                        # Gist save failed — keep session active AND warn user
                        st.session_state.titan_tier               = _tier_key
                        st.session_state["_subscription_active"]  = True
                        st.session_state["_subscription_expired"] = False
                        st.session_state["_subscription_expires"] = _sub_expires
                        st.error(
                            "⚠️ **Payment received but could not save to server right now.**\n\n"
                            f"**Screenshot this immediately:**\n\n"
                            f"- Transaction ID: `{_txn_id.strip()}`\n"
                            f"- Plan: {_plan_label}\n"
                            f"- Email: {_user_email}\n\n"
                            "Send the screenshot to the owner — your subscription will be activated manually."
                        )
                else:
                    st.error("Please enter your Transaction ID.")
        else:
            st.markdown("<div style='text-align:center;font-size:.8rem;color:#555;padding:10px 0'>Enter your email above to see payment options</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:.7rem;color:#333'>Payments via PhonePe / UPI · Money goes directly to the Titan Ultra creator</div>", unsafe_allow_html=True)
    st.stop()

# Show upgrade page if flagged
if st.session_state.get("show_upgrade"):
    _render_upgrade_page()

# Hidden upgrade trigger button — JS clicks this to open pricing page
if st.button("__TITAN_UPGRADE__", key="_hid_upgrade"):
    st.session_state.show_upgrade = True
    st.rerun()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # ── Colored TITAN ULTRA header ────────────────────────────────────────────
    _sb_tier = st.session_state.get("titan_tier", "basic")
    if _sb_tier == "pro":
        _tier_badge_html = "<span style='background:#7c3aed;color:#fff;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:8px;letter-spacing:1px;vertical-align:middle;margin-left:8px'>PRO</span>"
    elif _sb_tier == "max":
        _tier_badge_html = "<span style='background:#f59e0b;color:#000;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:8px;letter-spacing:1px;vertical-align:middle;margin-left:8px'>MAX</span>"
    else:
        _tier_badge_html = ""
    st.markdown(f"""
    <div style='padding:6px 10px 6px 10px;margin-top:0'>
        <span style='color:#ffffff;font-weight:700;font-size:1.05rem;
        letter-spacing:1.5px;font-family:"Segoe UI",sans-serif'>🔱 TITAN ULTRA</span>{_tier_badge_html}
    </div>
    """, unsafe_allow_html=True)

    # ── Account info + logout (non-owner users only) ─────────────────────────
    if not _IS_OWNER and st.session_state.get("user_registered"):
        _sb_uname = st.session_state.get("user_name_reg", "")
        _sb_uemail = st.session_state.get("user_email_reg", "")
        st.markdown(
            f"<div style='font-size:.68rem;color:#4a5568;padding:0 4px 2px'>logged in as "
            f"<span style='color:#a78bfa'>{_sb_uname}</span></div>",
            unsafe_allow_html=True
        )
        _lo_col1, _lo_col2 = st.columns([3, 1])
        with _lo_col2:
            if st.button("↩", key="_logout_btn", help="Log out", use_container_width=True):
                try:
                    _logout_device()
                except Exception:
                    pass
                for _k in ["user_registered", "user_name_reg", "user_email_reg",
                           "_family_key", "_gist_history", "titan_tier",
                           "_subscription_active", "_subscription_expires",
                           "_subscription_expired", "_expired_tier",
                           "_gist_loaded", "_sub_checked", "_auth_mode"]:
                    st.session_state.pop(_k, None)
                st.rerun()

    # ── Primary nav items ─────────────────────────────────────────────────────
    if st.button("new chat", use_container_width=True, key="_nav_newchat"):
        _save_chat_sessions()
        import time as _t
        st.session_state.chat_sessions = [{"id": int(_t.time()), "title": "New Chat", "messages": []}]
        st.session_state.active_session = 0
        st.session_state.notebook_mode = False
        st.session_state.library_mode = False
        st.session_state.schedule_mode = False
        st.session_state.tasks_mode = False
        st.session_state.show_titan_features = False
        st.rerun()

    # ── Titan Code button (Max only) ──────────────────────────────────────────
    if st.session_state.get("titan_tier") == "max":
        _tc_label = "←  back to chat" if st.session_state.get("show_titan_code") else "⌨  titan code"
        if st.button(_tc_label, use_container_width=True, key="_nav_tc"):
            st.session_state.show_titan_code = not st.session_state.show_titan_code
            if st.session_state.show_titan_code:
                st.session_state.notebook_mode = False
                st.session_state.show_titan_features = False
            st.rerun()

    _tf_label = "←  back to chat" if st.session_state.show_titan_features else "⊞  titan features"
    if st.button(_tf_label, use_container_width=True, key="_nav_tf"):
        st.session_state.show_titan_features = not st.session_state.show_titan_features
        if st.session_state.show_titan_features:
            st.session_state.notebook_mode = False
        st.rerun()

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    _nb_label = "←  back to chat" if st.session_state.notebook_mode else "≡  titan notebook"
    if st.button(_nb_label, use_container_width=True, key="_nav_nb"):
        st.session_state.notebook_mode = not st.session_state.notebook_mode
        if st.session_state.notebook_mode:
            st.session_state.show_titan_features = False
            st.session_state.library_mode = False
        st.rerun()

    _lib_label = "←  back to chat" if st.session_state.library_mode else "⊟  library"
    if st.button(_lib_label, use_container_width=True, key="_nav_lib"):
        st.session_state.library_mode = not st.session_state.library_mode
        if st.session_state.library_mode:
            st.session_state.notebook_mode = False
            st.session_state.schedule_mode = False
            st.session_state.show_titan_features = False
        st.rerun()

    _sch_label = "←  back to chat" if st.session_state.schedule_mode else "◷  schedule"
    if st.button(_sch_label, use_container_width=True, key="_nav_sch"):
        st.session_state.schedule_mode = not st.session_state.schedule_mode
        if st.session_state.schedule_mode:
            st.session_state.notebook_mode = False
            st.session_state.library_mode = False
            st.session_state.tasks_mode = False
            st.session_state.show_titan_features = False
        st.rerun()

    _task_label = "←  back to chat" if st.session_state.tasks_mode else "⊞  titan tasks"
    if st.button(_task_label, use_container_width=True, key="_nav_tasks"):
        st.session_state.tasks_mode = not st.session_state.tasks_mode
        if st.session_state.tasks_mode:
            st.session_state.notebook_mode = False
            st.session_state.library_mode = False
            st.session_state.schedule_mode = False
            st.session_state.show_titan_features = False
        st.rerun()

    # ── Upgrade button (visible in sidebar for all non-owner users) ──────────
    if not _IS_OWNER:
        _ub_tier     = st.session_state.get("titan_tier", "basic")
        _ub_sub_on   = st.session_state.get("_subscription_active", False)
        _ub_sub_exp  = st.session_state.get("_subscription_expires", "")
        if _ub_sub_on:
            # Subscription active — show locked plan info, no switching allowed
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            _ub_clr = "#f59e0b" if _ub_tier == "max" else "#a78bfa"
            _ub_lbl = "MAX" if _ub_tier == "max" else "PRO"
            st.markdown(
                f"<div style='background:rgba(255,255,255,0.04);border:1px solid {_ub_clr}44;"
                f"border-radius:8px;padding:8px 10px;font-size:.72rem'>"
                f"<span style='color:{_ub_clr};font-weight:700'>{_ub_lbl} active</span>"
                + (f"<br><span style='color:#555;font-size:.65rem'>expires {_ub_sub_exp}</span>" if _ub_sub_exp else "")
                + "</div>",
                unsafe_allow_html=True
            )
        elif _ub_tier == "basic":
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.markdown("""
<style>
.stButton > button[kind="secondary"][data-testid*="upgrade_sb"] {
    background: linear-gradient(135deg,#1e3a8a,#4f46e5) !important;
    color:#fff !important; border:none !important; font-weight:700 !important;
    font-size:.82rem !important; letter-spacing:.5px !important;
}
</style>""", unsafe_allow_html=True)
            if st.button("⬆  Upgrade to Pro / Max", key="_upgrade_sb", use_container_width=True):
                st.session_state.show_upgrade = True
                st.rerun()

    # ── Pro: Answer Depth selector ────────────────────────────────────────────
    if not _IS_OWNER and st.session_state.get("titan_tier") == "pro":
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:.58rem;color:#7c3aed;letter-spacing:1.5px;padding:0 4px 2px;font-weight:600'>ANSWER DEPTH</div>", unsafe_allow_html=True)
        _dep_now = st.session_state.get("_answer_depth", "normal")
        _dep_icons = {"quick": "⚡", "normal": "◉", "deep": "🔬"}
        _dc1, _dc2, _dc3 = st.columns(3)
        _dep_btn_style = "border:1px solid #7c3aed33 !important;"
        with _dc1:
            if st.button("⚡ Quick", key="_dep_q", use_container_width=True,
                         help="Short, fast answers — great for quick facts"):
                st.session_state._answer_depth = "quick"; st.rerun()
        with _dc2:
            if st.button("◉ Normal", key="_dep_n", use_container_width=True):
                st.session_state._answer_depth = "normal"; st.rerun()
        with _dc3:
            if st.button("🔬 Deep", key="_dep_d", use_container_width=True,
                         help="Ultra-detailed research-grade answers"):
                st.session_state._answer_depth = "deep"; st.rerun()
        _dep_labels = {"quick": "⚡ Quick Mode", "normal": "◉ Normal", "deep": "🔬 Deep Research"}
        _dep_colors = {"quick": "#f59e0b", "normal": "#a78bfa", "deep": "#22c55e"}
        st.markdown(f"<div style='font-size:.62rem;color:{_dep_colors.get(_dep_now,'#a78bfa')};padding:1px 4px 4px'>Active: {_dep_labels.get(_dep_now,'◉ Normal')}</div>", unsafe_allow_html=True)

    # ── Video API Key (Pro + Max) ─────────────────────────────────────────────
    if not _IS_OWNER and st.session_state.get("titan_tier") in ("pro", "max"):
        _fk_now = st.session_state.get("fal_api_key", "")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:.58rem;color:#60a5fa;letter-spacing:1.5px;padding:0 4px 2px;font-weight:600'>VIDEO API KEY (fal.ai)</div>", unsafe_allow_html=True)
        _fk_input = st.text_input("", value=_fk_now, placeholder="Paste fal.ai key to enable video",
                                   type="password", key="_fal_key_input", label_visibility="collapsed")
        if _fk_input != _fk_now:
            st.session_state.fal_api_key = _fk_input
            st.rerun()

    # ── Max: Titan Focus Mode ─────────────────────────────────────────────────
    if not _IS_OWNER and st.session_state.get("titan_tier") == "max":
        _focus_on = st.session_state.get("_focus_mode", False)
        _focus_label = "◀ exit focus" if _focus_on else "⊙  focus mode"
        if st.button(_focus_label, use_container_width=True, key="_nav_focus"):
            st.session_state._focus_mode = not _focus_on
            st.rerun()

    # ── AI Model selector (owner only) ────────────────────────────────────────
    if _IS_OWNER:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:.6rem;color:#4a5568;letter-spacing:1px;padding:0 2px'>ai model</div>", unsafe_allow_html=True)
        model_name = st.selectbox("Model", list(GROQ_MODELS.keys()), label_visibility="collapsed",
                                  key="_model_sel")
        model_id = GROQ_MODELS[model_name]
    else:
        _nt = st.session_state.get("titan_tier", "basic")
        if _nt == "max":
            model_name = "👑 GPT-OSS 120B  (Strongest · Beats GPT-6)"
            _nm_label  = "👑 GPT-OSS 120B"
            _nm_color  = "#f59e0b"
        elif _nt == "pro":
            model_name = "⚡ GPT-OSS 20B   (Fast · OpenAI)"
            _nm_label  = "⚡ GPT-OSS 20B"
            _nm_color  = "#a78bfa"
        else:
            model_name = "🔱 Qwen 3.8 27B  (Smart & Capable)"
            _nm_label  = "🔱 Qwen 3.8 27B"
            _nm_color  = "#60a5fa"
        model_id = GROQ_MODELS[model_name]
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:.6rem;color:#4a5568;letter-spacing:1px;padding:0 2px'>ai model</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:.75rem;color:{_nm_color};padding:2px 6px 6px;font-weight:500;background:rgba(255,255,255,0.03);border-radius:6px;border:1px solid rgba(255,255,255,0.06)'>{_nm_label}</div>", unsafe_allow_html=True)

    # ── Titan Devices (owner only) ────────────────────────────────────────────
    if _IS_OWNER:
        with st.expander("Titan Devices", expanded=False):
            if not _registry_ready():
                st.warning("Set up Gist to see devices.")
            else:
                if st.button("Refresh", key="_td_refresh", use_container_width=True):
                    _fetch_registry_cached.clear()
                _td_all = _load_registry()
                if not _td_all:
                    st.caption("No devices registered yet.")
                else:
                    _td_search = st.text_input("Search by name", placeholder="Type a name...",
                                               key="_td_search", label_visibility="collapsed")
                    _td_filtered = {
                        did: dev for did, dev in _td_all.items()
                        if _td_search.lower() in dev.get("name", "").lower()
                    } if _td_search else _td_all
                    st.markdown(f"<div style='font-size:.7rem;color:#6b7a99'>{len(_td_all)} device(s)</div>", unsafe_allow_html=True)
                    for _did, _dev in _td_filtered.items():
                        _dname  = _dev.get("name", "Unknown")
                        _dlast  = _dev.get("last_seen", "")[:10]
                        _tout_s = _dev.get("timeout_until")
                        _timed_out = False
                        if _tout_s:
                            from datetime import datetime as _dtck
                            _timed_out = _dtck.now() < _dtck.fromisoformat(_tout_s)
                        _status = "Timed Out" if _timed_out else "Active"
                        st.markdown(f"**{_dname}** — {_status}  \n<span style='font-size:.65rem;color:#6b7a99'>Last seen: {_dlast} · ID: {_did[:8]}…</span>", unsafe_allow_html=True)
                        _c1, _c2 = st.columns([2, 1])
                        _tout_hrs = _c1.number_input("Hours", min_value=0, max_value=720,
                                                     value=0, step=1, key=f"_td_thr_{_did}",
                                                     label_visibility="collapsed")
                        if _c2.button("Timeout", key=f"_td_tout_{_did}", use_container_width=True):
                            from datetime import datetime as _dtd, timedelta as _tdd
                            if _tout_hrs > 0:
                                _td_all[_did]["timeout_until"] = (_dtd.now() + _tdd(hours=_tout_hrs)).isoformat()
                                _save_registry(_td_all)
                                st.rerun()
                        if _timed_out:
                            if st.button("Remove Timeout", key=f"_td_clr_{_did}", use_container_width=True):
                                _td_all[_did]["timeout_until"] = None
                                _save_registry(_td_all)
                                st.rerun()
                        st.markdown("---")

    # ── History — always open, flat list ─────────────────────────────────────
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.6rem;color:#4a5568;letter-spacing:1px;padding:0 2px 4px'>history</div>", unsafe_allow_html=True)

    _hist_all = _load_history()
    if not _hist_all:
        st.markdown("<div style='font-size:.72rem;color:#4a5568;padding:2px 4px'>No chats yet</div>", unsafe_allow_html=True)
    else:
        for _hs in _hist_all[:80]:
            if st.button(_hs.get("title","Chat")[:42], key=f"_hn_{_hs.get('id',0)}",
                         use_container_width=True):
                _save_chat_sessions()
                st.session_state.chat_sessions = [_hs]
                st.session_state.active_session = 0
                st.session_state.notebook_mode = False
                st.session_state.library_mode = False
                st.session_state.schedule_mode = False
                st.session_state.tasks_mode = False
                st.session_state.show_titan_features = False
                st.rerun()

    # ── Hidden settings at bottom (API key, owner unlock) ─────────────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    with st.expander("···", expanded=False):
        if _IS_OWNER:
            key_in = st.text_input("API Key", type="password", label_visibility="collapsed",
                                   value=st.session_state.api_key, placeholder="Groq API key  gsk_...")
            if key_in and key_in != st.session_state.api_key:
                st.session_state.api_key = key_in
                _save_key(key_in)
                st.session_state.pop("_key_valid", None)
            elif key_in:
                st.session_state.api_key = key_in
            if st.session_state.api_key and "_key_valid" not in st.session_state:
                try:
                    _tc = Groq(api_key=st.session_state.api_key)
                    _tc.models.list()
                    st.session_state["_key_valid"] = True
                except Exception as _ke:
                    _kes = str(_ke).lower()
                    st.session_state["_key_valid"] = False if any(
                        x in _kes for x in ("auth","401","invalid","api key","unauthorized")
                    ) else True
            if st.session_state.get("_key_valid") is False:
                st.markdown("<div style='font-size:.65rem;color:#ef4444'>Invalid key</div>", unsafe_allow_html=True)
        if not _IS_OWNER:
            _ul_code = st.text_input("", type="password", placeholder="Owner code",
                                     label_visibility="collapsed", key="_owner_unlock_input")
            if st.button("Unlock", key="_owner_unlock_btn", use_container_width=True):
                _entered_hash = _hlib_owner.sha256(_ul_code.strip().encode()).hexdigest()
                if _entered_hash == _OWNER_HASH:
                    _OWNER_AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
                    _OWNER_AUTH_FILE.write_text(_entered_hash)
                    st.rerun()
                else:
                    st.error("Wrong code.")
            # ── Account info: show saved password so user can share with family ─
            if st.session_state.get("user_registered") and st.session_state.get("user_email_reg"):
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:.68rem;color:#4a5568'>Account</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='font-size:.72rem;color:#a78bfa;padding:2px 0'>"
                    f"{st.session_state.get('user_name_reg','')} · "
                    f"{st.session_state.get('user_email_reg','')}</div>",
                    unsafe_allow_html=True
                )
                if st.button("Show my password", key="_show_pw_btn", use_container_width=True):
                    st.session_state["_show_pw"] = not st.session_state.get("_show_pw", False)
                if st.session_state.get("_show_pw"):
                    try:
                        import base64 as _b64pw
                        _pw_reg = _load_registry()
                        _pw_acc = _get_account(_pw_reg, st.session_state["user_email_reg"])
                        if _pw_acc and _pw_acc.get("password_b64"):
                            _pw_plain = _b64pw.b64decode(_pw_acc["password_b64"]).decode()
                            st.code(_pw_plain, language=None)
                            st.caption("Share this with family. They must use your exact email + this password.")
                        else:
                            st.caption("Password not recoverable (old account). Please re-register.")
                    except Exception:
                        st.caption("Could not retrieve password.")
        if st.button("Clear Current Chat", use_container_width=True, key="_clr_chat"):
            import time as _t
            st.session_state.chat_sessions = [{"id": int(_t.time()), "title": "New Chat", "messages": []}]
            st.session_state.active_session = 0
            st.rerun()

    # Provider is always Groq
    provider = "Groq"

    # Memory stays hidden from sidebar (auto-saves in background)
    _mem = st.session_state.titan_memory

    # Attach + Voice buttons removed (no file upload or voice input).
    voice_text    = ""
    uploaded_file = None
    file_content  = ""
    if "pending_vision" not in st.session_state:
        st.session_state.pending_vision = None



# ── Header ────────────────────────────────────────────────────────────────────
_user_name = st.session_state.titan_memory.get("name", "")
if "_titan_phrase" not in st.session_state:
    st.session_state._titan_phrase = _random.choice(_TITAN_PHRASES)
_phrase = st.session_state._titan_phrase
if _user_name and "{name}" in _phrase:
    _greet_text = _phrase.replace("{name}", _user_name)
elif _user_name:
    _greet_text = _phrase
else:
    _greet_text = _phrase.replace("{name}", "").strip().rstrip(",?").strip()

if not cur_msgs():
    st.markdown("<div style='height:28vh'></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div id="titan-greeting" style='text-align:center;margin-bottom:28px'>
    <div style='display:flex;align-items:center;justify-content:center;gap:16px'>
        <span style='font-size:2rem;animation:tridentGlow 3s linear infinite;display:inline-block'>🔱</span>
        <span style='font-family:"Segoe UI","Inter","Helvetica Neue",sans-serif;font-size:1.75rem;font-weight:600;color:#ffffff;letter-spacing:0.3px'>{_greet_text}</span>
    </div>
</div>
""", unsafe_allow_html=True)
    if "_home_counter" not in st.session_state:
        st.session_state._home_counter = 0

    _hc1, _hc2, _hc3 = st.columns([0.5, 5, 0.5])
    with _hc2:
        _mode = st.session_state.get("_titan_mode", "normal")
        _ph = ("⚡ Fast Mode active — Message TITAN ULTRA..." if _mode == "fast"
               else "Message TITAN ULTRA...")
        _home_q = st.text_input("", placeholder=_ph,
                                 label_visibility="collapsed",
                                 key=f"_home_input_{st.session_state._home_counter}")

    if _home_q:
        st.session_state._home_pending = _home_q
        st.session_state._home_counter += 1
        st.rerun()

    # ── Daily Spark ────────────────────────────────────────────────────────────
    from datetime import datetime as _dtsp
    _SPARKS = [
        ("◎ Brain Teaser", "A bat and a ball cost ₹110 total. The bat costs ₹100 more than the ball. How much is the ball?", "#6366f1", "Answer: ₹5 — not ₹10! Most people get it wrong.", "Explore →"),
        ("◇ Mind-Blow", "If you removed all empty space from atoms, ALL 8 billion humans on Earth would fit inside a sugar cube!", "#06b6d4", "Ask me more about atoms", "Explore →"),
        ("◦ Did You Know?", "Honey never expires. Archaeologists found 3,000-year-old honey in Egyptian tombs — still perfectly edible!", "#f59e0b", "What other foods last forever?", "Explore →"),
        ("△ Space Fact", "A day on Venus is longer than a year on Venus. It rotates so slowly it takes 243 Earth days just to spin once!", "#8b5cf6", "What else is strange about Venus?", "Explore →"),
        ("⊞ Math Magic", "Pick any 3-digit number (first and last digit different). Reverse it, subtract smaller from larger, reverse result and add — you always get 1089!", "#10b981", "Show me the 1089 trick step by step", "Explore →"),
        ("≈ Ocean Mystery", "95% of Earth's oceans are completely unexplored. More humans have walked on the Moon than visited the deepest ocean trench!", "#0ea5e9", "What lives in the deep ocean?", "Explore →"),
        ("◉ Science Shock", "Your body has 37 trillion cells. The DNA in just ONE cell, if stretched, would reach from Earth to Pluto and back!", "#ec4899", "How much total DNA do I have?", "Explore →"),
        ("⊙ Loudest Sound Ever", "The 1883 Krakatoa eruption was heard 5,000 km away in Australia — the loudest sound ever recorded in history!", "#14b8a6", "What caused the Krakatoa eruption?", "Explore →"),
        ("◈ Human Body", "Your nose can detect over 1 TRILLION different smells — far more than any electronic sensor ever built!", "#a855f7", "Which smell is the strongest for memory?", "Explore →"),
        ("⊟ Tech History", "The first ever computer bug was a REAL bug — a moth stuck in a Harvard relay in 1947, taped into the logbook!", "#22d3ee", "Who invented the computer?", "Explore →"),
        ("◆ Cool Physics", "The Eiffel Tower grows 15 cm taller every summer due to heat expansion. It shrinks back in winter!", "#f43f5e", "What other things expand with heat?", "Explore →"),
        ("≡ Nature Net", "Trees secretly communicate and share food through underground fungal networks — scientists call it the 'Wood Wide Web'!", "#84cc16", "How do trees communicate?", "Explore →"),
        ("◁ History Surprise", "Napoleon was NOT short — he was 5'7\" (170 cm), above average for his time. The 'short Napoleon' myth was British war propaganda!", "#fb923c", "What other history facts are myths?", "Explore →"),
        ("△ Sun Size", "The Sun is so massive that 1.3 MILLION Earths could fit inside it — yet it's just an average-sized star in the Milky Way!", "#facc15", "How big is the biggest known star?", "Explore →"),
        ("◇ Riddle", "What has keys but no locks, has space but no room, and lets you enter but not go in?", "#34d399", "Answer: A keyboard! Ask me more riddles", "Reveal →"),
        ("≋ Whale Heart", "A blue whale's heart is the size of a small car. Its heartbeat can be detected from 3 kilometers away!", "#60a5fa", "What is the fastest heartbeat of any animal?", "Explore →"),
        ("↯ Lightning Heat", "Lightning is 5x hotter than the surface of the Sun — reaching 30,000 Kelvin in a fraction of a second!", "#fbbf24", "How does lightning form?", "Explore →"),
        ("◈ Russia Time", "Russia is so large it spans 11 time zones. When it's 9 AM in Moscow, it's already 11 PM on Russia's far east coast!", "#4ade80", "What are the largest countries by area?", "Explore →"),
        ("◆ Carbon Magic", "Diamonds and graphite (pencil lead) are BOTH made of pure carbon — just arranged differently at the atomic level!", "#f472b6", "How are diamonds formed?", "Explore →"),
        ("♩ Mozart Memory", "Mozart could hear a piece of music ONCE and write it out perfectly from memory. He did this with a secret Vatican piece aged 14!", "#c084fc", "Who had the greatest musical mind ever?", "Explore →"),
        ("▲ Tallest Mountain", "Measured from Earth's center — not sea level — Mount Chimborazo in Ecuador is actually taller than Everest!", "#38bdf8", "How tall is Chimborazo vs Everest?", "Explore →"),
        ("◉ Study Hack", "The best time to study is right before sleep. Your brain consolidates memories during deep sleep, so last-studied content sticks best!", "#fb7185", "What are the best study techniques?", "Explore →"),
        ("⊗ Mantis Shrimp", "Mantis shrimps can see 16 types of color — humans only see 3. They live in a rainbow we literally cannot imagine!", "#2dd4bf", "How do animals see differently from humans?", "Explore →"),
        ("◻ AI Milestone", "The first AI to beat a world chess champion was IBM's Deep Blue in 1997. Today's AI beats humans at chess, Go, and strategy games!", "#f97316", "What can AI do better than humans?", "Explore →"),
        ("◑ Butterfly Taste", "Butterflies taste with their feet — they have chemical taste sensors on their legs to detect food and plants for their eggs!", "#ec4899", "What other animals taste or smell strangely?", "Explore →"),
        ("⊕ GPS Relativity", "GPS satellites must correct for Einstein's relativity — time moves slightly faster in orbit, drifting 38 microseconds per day!", "#6366f1", "How does Einstein's relativity work?", "Explore →"),
        ("◎ Memory Science", "Every time you learn something new, your brain physically grows new connections between neurons — it literally rewires itself!", "#0891b2", "How can I improve my memory?", "Explore →"),
        ("◌ Moon Drift", "The Moon moves 3.8 cm farther from Earth every year. In 600 million years, total solar eclipses will be impossible!", "#7c3aed", "What will the Moon look like in a million years?", "Explore →"),
        ("⊞ Birthday Math", "In a room of just 23 people, there's a 50% chance two share a birthday. With 70 people: 99.9%! Most people find this shocking.", "#059669", "Why is this probability so surprising?", "Explore →"),
        ("≈ Plant Intelligence", "Plants can detect and react to music, touch, gravity, and even danger signals from neighboring plants — within seconds!", "#65a30d", "Do plants have feelings?", "Explore →"),
        ("↯ Battery of Life", "The electric eel can generate 860 volts — enough to stun a horse or power a lightbulb for 30 minutes!", "#eab308", "How do electric animals generate power?", "Explore →"),
    ]
    _sp_idx = _dtsp.now().day % len(_SPARKS)
    _sp_title, _sp_text, _sp_color, _sp_hint, _sp_btn = _SPARKS[_sp_idx]
    _tier_now = st.session_state.get("titan_tier", "basic")
    _sp_border = "#f59e0b" if _tier_now == "max" else ("#7c3aed" if _tier_now == "pro" else _sp_color)
    st.markdown(f"""
<style>
@keyframes sparkFadeIn {{
  from {{ opacity:0; transform:translateY(12px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
.titan-spark {{
  max-width:560px; margin:28px auto 0;
  background:rgba(255,255,255,0.03);
  border:1px solid {_sp_border}44; border-radius:14px;
  padding:16px 20px 14px;
  box-shadow:0 0 24px {_sp_color}18;
  animation: sparkFadeIn .6s ease both;
}}
</style>
<div class="titan-spark">
  <div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>
    <span style='font-size:.58rem;color:{_sp_color};letter-spacing:2px;font-weight:700;text-transform:uppercase'>◈ Daily Spark</span>
    <span style='font-size:.58rem;color:#333;letter-spacing:1px'>· {_dtsp.now().strftime("%d %b")}</span>
  </div>
  <div style='font-size:.95rem;font-weight:600;color:#e8e8e8;line-height:1.5;margin-bottom:6px'>{_sp_title} &nbsp;&nbsp; {_sp_text}</div>
  <div style='font-size:.72rem;color:#555;margin-top:4px'>{_sp_hint}</div>
</div>
""", unsafe_allow_html=True)
    _sp1, _sp2, _sp3 = st.columns([1, 2, 1])
    with _sp2:
        if st.button(f"→  {_sp_btn}", key="_daily_spark_btn", use_container_width=True):
            st.session_state._home_pending = _sp_hint
            st.session_state._home_counter = st.session_state.get("_home_counter", 0) + 1
            st.rerun()

mode_key = "chat"  # unified — auto-detected from input

# ── Features & Tools (hidden from home — accessible via sidebar) ──────────────
if False and st.expander("⚙️ Features & Tools"):
    st.markdown("<div style='font-size:.75rem;color:#aaaaaa;letter-spacing:2px;margin-bottom:8px'>SPEED MODE</div>", unsafe_allow_html=True)
    fc1, fc2 = st.columns(2)
    with fc1:
        if st.button("⚡ Fast", use_container_width=True, key="_ft_fast",
                     help="Quick answers — lower reasoning depth"):
            st.session_state.speed = "fast"; st.rerun()
    with fc2:
        if st.button("🧠 Thinking", use_container_width=True, key="_ft_think",
                     help="Deep step-by-step reasoning"):
            st.session_state.speed = "think"; st.rerun()
    active = "⚡ Fast" if st.session_state.speed == "fast" else "🧠 Thinking"
    st.markdown(f"<div style='font-size:.72rem;color:#4a6a8f;text-align:center;margin-top:4px'>Active: <b style='color:#e8e8e8'>{active}</b></div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:.75rem;color:#aaaaaa;letter-spacing:2px;margin:14px 0 8px'>QUICK ACTIONS</div>", unsafe_allow_html=True)

    _exam_active = st.session_state.chat_active_tool == "exam"
    if st.button("📝 Exam Paper" + (" ✓" if _exam_active else ""), use_container_width=True, key="tool_exam_btn"):
        st.session_state.chat_active_tool = "" if _exam_active else "exam"
        st.rerun()

    if st.session_state.chat_active_tool == "exam":
        st.markdown("#### 📝 Exam Paper Generator")

        _EP_TYPES   = ["School Class","JEE Mains","NEET","JEE Advanced","SAT","Custom"]
        _EP_CLASSES = ["Class 1","Class 2","Class 3","Class 4","Class 5","Class 6",
                       "Class 7","Class 8","Class 9","Class 10",
                       "Class 11 (Science)","Class 11 (Commerce)","Class 11 (Arts)",
                       "Class 12 (Science)","Class 12 (Commerce)","Class 12 (Arts)"]

        _er1, _er2   = st.columns(2)
        _ep_type_sel = _er1.selectbox("Type", _EP_TYPES, key="ep_type")
        _ep_class    = _er2.selectbox("Class", _EP_CLASSES, index=9, key="ep_class",
                                      disabled=(_ep_type_sel != "School Class"))

        if _ep_type_sel == "School Class":
            _er3, _er4   = st.columns(2)
            _ep_syllabus = _er3.text_input("Syllabus / Board", value="CBSE", key="ep_syllabus")
            _ep_subj     = _er4.selectbox("Subject",
                            ["Mathematics","Physics","Chemistry","Biology","English",
                             "History","Geography","Economics","Computer Science","Science","Hindi","All"],
                            key="ep_subject")
            _ep_exam_label = f"{_ep_class} {_ep_syllabus}"
        elif _ep_type_sel == "Custom":
            _er3, _er4     = st.columns(2)
            _ep_exam_label = _er3.text_input("Exam name:", placeholder="e.g. CA Foundation", key="ep_custom")
            _ep_subj       = _er4.text_input("Subjects (comma separated):", placeholder="e.g. Maths, Science", key="ep_subj_text")
            _ep_syllabus   = ""
        else:
            _ep_subj_opts  = {"JEE Mains":["Physics","Chemistry","Mathematics","All"],
                              "JEE Advanced":["Physics","Chemistry","Mathematics","All"],
                              "NEET":["Physics","Chemistry","Biology","All"],
                              "SAT":["Math","Reading & Writing","All"]}
            _er3, _er4     = st.columns(2)
            _ep_subj       = _er3.selectbox("Subject", _ep_subj_opts.get(_ep_type_sel, ["All"]), key="ep_subject")
            _ep_syllabus   = _ep_type_sel
            _ep_exam_label = _ep_type_sel
            _er4.text_input("Syllabus / Board", value=_ep_type_sel, key="ep_syllabus", disabled=True)

        _er5, _er6   = st.columns(2)
        _ep_chapters = _er5.text_input("Chapters / Topics", placeholder="e.g. Thermodynamics (blank = all)", key="ep_ch_")
        _ep_diff     = _er6.selectbox("Difficulty", ["Medium","Easy","Hard","Mixed (Easy + Medium + Hard)"], key="ep_diff")

        _ec1, _ec2, _ec3 = st.columns(3)
        _ep_qcount = _ec1.number_input("Questions", min_value=5,  max_value=100, value=20,  step=5,  key="ep_qcount")
        _ep_marks  = _ec2.number_input("Marks",     min_value=10, max_value=500, value=100, step=5,  key="ep_marks")
        _ep_time   = _ec3.number_input("Mins",      min_value=15, max_value=360, value=60,  step=15, key="ep_time")

        _ep_qtype = st.selectbox("Question Type",
            ["Mixed (MCQ + Short + Long)","MCQ Only","Short Answer Only","Long Answer Only","MCQ + Descriptive"],
            key="ep_qtype")

        if st.button("🎯 Generate Exam Paper", use_container_width=True, key="ep_gen"):
            _subj_val = _ep_subj if isinstance(_ep_subj, str) else ""
            if not _subj_val.strip():
                st.warning("Please select or enter a subject.")
            else:
                _chapters_val = _ep_chapters.strip() or "all chapters of the NCERT syllabus"
                _prompt = (
                    f"Generate a complete exam paper for {_ep_exam_label}.\n"
                    + (f"- Syllabus/Board: {_ep_syllabus}\n" if _ep_syllabus else "")
                    + f"- Subject: {_subj_val}\n"
                    f"- Chapters/Topics: {_chapters_val}\n"
                    f"- Difficulty: {_ep_diff}\n"
                    f"\n- Number of questions: {_ep_qcount}"
                    f"\n- Question type: {_ep_qtype}"
                    f"\n- Total marks: {_ep_marks}"
                    f"\n- Time allowed: {_ep_time} minutes\n\n"
                    "FORMAT RULES (follow exactly):\n"
                    "1. Header: exam name, subject, class/level, date field, time allowed, maximum marks\n"
                    "2. General Instructions in full sentences\n"
                    "3. Each question numbered Q1, Q2, Q3... with marks in [brackets]\n"
                    "4. MCQs — each option on its own line: (A) ... (B) ... (C) ... (D) ...\n"
                    "5. ANSWER KEY at the end: show correct letter + one-line explanation per MCQ\n\n"
                    "LANGUAGE RULES (mandatory — no exceptions):\n"
                    "• Write every single word in FULL — no abbreviations whatsoever\n"
                    "• WRONG: 'b/w', 'w.r.t.', 'temp.', 'conc.', 'rxn', 'approx.', 'max.', 'min.', '&', 'etc.'\n"
                    "• RIGHT: 'between', 'with respect to', 'temperature', 'concentration', 'reaction', 'approximately', 'maximum', 'minimum', 'and'\n"
                    "• Every question must be a full, clear, grammatically correct sentence\n"
                    "• Questions must be easy to read — a student should understand immediately what is being asked\n"
                    "Ensure all questions are NCERT/curriculum accurate and appropriate for the class/exam level."
                )
                st.session_state.ep_last_name = str(_ep_exam_label).replace(" ","_")
                st.session_state.ep_generating = True
                st.session_state.ep_last_paper = ""
                st.session_state.quick_q = _prompt
                st.rerun()


# ── PDF builder ───────────────────────────────────────────────────────────────
def _make_exam_pdf(text, title="Exam Paper"):
    import io as _io, re as _re
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib import colors as _colors

        def _clean(s):
            # strip emojis / non-latin that reportlab can't render
            return _re.sub(r'[^\x00-\x7FÀ-ɏ]', '', s)

        buf = _io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)
        styles = getSampleStyleSheet()
        t_style = ParagraphStyle('T', parent=styles['Heading1'],
                                 alignment=TA_CENTER, fontSize=16, spaceAfter=4)
        h_style = ParagraphStyle('H', parent=styles['Heading2'],
                                 fontSize=12, spaceAfter=3, spaceBefore=6)
        b_style = ParagraphStyle('B', parent=styles['Normal'],
                                 fontSize=10, spaceAfter=2, leading=14)

        story = [Paragraph(_clean(title), t_style),
                 HRFlowable(width="100%", thickness=1, color=_colors.black),
                 Spacer(1, 4*mm)]

        for line in text.split('\n'):
            cl = _clean(line.strip())
            if not cl:
                story.append(Spacer(1, 3*mm)); continue
            safe = cl.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            stripped = cl.lstrip('#* ').replace('**','')
            safe_stripped = stripped.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            if cl.startswith('#') or cl.startswith('**') or (cl.isupper() and len(cl) > 3):
                story.append(Paragraph(f"<b>{safe_stripped}</b>", h_style))
            else:
                story.append(Paragraph(safe, b_style))

        doc.build(story)
        return buf.getvalue()
    except Exception:
        return None

# ── Auto-detection helpers ────────────────────────────────────────────────────
def _is_flashcard_request(text):
    t = text.lower()
    return any(x in t for x in (
        'flashcard', 'flash card', 'study card', 'revision card',
        'make cards', 'create cards', 'generate cards', 'memorize',
        'quiz me', 'test me on', 'help me study', 'cards for', 'cards on',
        'study notes', 'notes on', 'revision on',
    ))

def _is_weather_query(text):
    t = text.lower()
    return any(x in t for x in (
        'weather', 'temperature', 'forecast', 'rain', 'humid', 'sunny',
        'cloudy', 'climate', 'aqi', 'air quality', 'uv index', 'wind speed',
        'umbrella', 'will it rain', 'cold today', 'hot today', 'will it snow',
        'weather in', 'weather at', 'weather for', 'temperature in',
        'forecast for', 'forecast in',
    ))

def _is_pc_command_detect(text):
    t = text.lower().strip()
    _actions = ('open ', 'launch ', 'start ', 'close ', 'kill ', 'run ',
                'install ', 'uninstall ', 'volume', 'mute', 'unmute',
                'screenshot', 'brightness', 'shutdown', 'shut down',
                'restart', 'reboot', 'sleep', 'hibernate', 'lock screen',
                'lock pc', 'lock computer', 'play music', 'pause music',
                'stop music', 'next song', 'previous song', 'skip song',
                'increase volume', 'decrease volume', 'turn up', 'turn down',
                'set volume', 'snipping tool', 'screen capture',
                'search youtube', 'open youtube', 'open chrome', 'open edge',
                'open firefox', 'open spotify', 'open discord', 'open whatsapp',
                'open telegram', 'open notepad', 'open calculator',)
    _questions = ('how ', 'what ', 'why ', 'when ', 'where ', 'which ',
                  'explain ', 'tell me', 'help me', 'can you', 'could you',
                  'should i', 'is it', 'will it', 'do i')
    is_action = any(t.startswith(x) or f' {x}' in t for x in _actions)
    is_question = any(t.startswith(x) for x in _questions) or t.endswith('?')
    return is_action and not is_question

# ══════════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
# ── SCHEDULE PAGE ─────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.schedule_mode:
    import datetime as _dt2, uuid as _uuid
    from pathlib import Path as _SchPath

    st.markdown("""
    <h2 style='color:#ffffff;font-family:Orbitron,monospace;font-weight:900;
    font-size:1.4rem;letter-spacing:2px;margin-bottom:2px'>◷ Schedule</h2>
    <p style='color:#4a5568;font-size:.8rem;margin-top:0'>
    Titan asks you 5 questions every day — a popup appears automatically, you type your answer.</p>
    """, unsafe_allow_html=True)

    _sch_data    = _load_schedule()
    _today_d     = _dt2.date.today()
    _today_str2  = str(_today_d)

    # ── Scheduler auto-launch helper ──────────────────────────────────────────
    _sched_py = _SchPath(__file__).parent / "titan_scheduler.py"

    def _launch_scheduler_bg():
        try:
            import subprocess as _ss, sys as _sys
            _ss.Popen(
                [_sys.executable, str(_sched_py)],
                creationflags=0x00000008 | 0x08000000,  # DETACHED + NO_WINDOW
                close_fds=True,
            )
        except Exception:
            pass

    def _scheduler_running():
        try:
            import subprocess as _ss
            _pid_f = _SchPath(__file__).parent / ".titan_scheduler.pid"
            if not _pid_f.exists():
                return False
            old = int(_pid_f.read_text().strip())
            r = _ss.run(["tasklist", "/FI", f"PID eq {old}", "/NH"],
                        capture_output=True, text=True)
            return str(old) in r.stdout
        except Exception:
            return False

    _running = _scheduler_running()
    _sc1, _sc2 = st.columns([5, 3])
    with _sc1:
        if _running:
            st.markdown(
                "<div style='color:#22c55e;font-size:.78rem;padding-top:6px'>"
                "✅ Scheduler is running — question popups appear at<br>"
                "<b>9 am · 11 am · 1 pm · 4 pm · 7 pm</b> every day. Auto-starts at Windows login.</div>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='color:#4a5568;font-size:.78rem;padding-top:6px'>"
                "Scheduler not running. It starts automatically when you add a schedule,<br>"
                "or click Start below. Runs silently at <b style='color:#aaaaaa'>9 am · 11 am · 1 pm · 4 pm · 7 pm</b>.</div>",
                unsafe_allow_html=True)
    with _sc2:
        if st.button("▶  Start / Restart", key="_sch_launch", use_container_width=True):
            _launch_scheduler_bg()
            st.success("Scheduler started!")

    st.markdown("<hr style='border-color:#1a1a2e;margin:8px 0 12px'>", unsafe_allow_html=True)

    # ── Add new schedule ───────────────────────────────────────────────────────
    _SCH_SUGGESTIONS = [
        "Study session", "Homework", "Revision", "Exercise", "Read a chapter",
        "Practice problems", "Project work", "Watch lecture", "Make notes",
        "Prepare for exam", "Submit assignment", "Call / Message",
        "Clean room", "Drink water reminder", "Sleep by 10pm",
    ]
    if "sch_prefill" not in st.session_state:
        st.session_state.sch_prefill = ""

    with st.expander("＋  add new schedule", expanded=st.session_state.sch_prefill != ""):
        st.markdown("<div style='font-size:.72rem;color:#4a5568;margin-bottom:6px'>Quick suggestions — click to fill:</div>",
                    unsafe_allow_html=True)
        _sug_cols = st.columns(3)
        for _si, _sug in enumerate(_SCH_SUGGESTIONS):
            with _sug_cols[_si % 3]:
                if st.button(_sug, key=f"_sug_{_si}", use_container_width=True):
                    st.session_state.sch_prefill = _sug
                    st.rerun()

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        _new_title = st.text_input("What do you need to do?", key="_sch_title",
                                   value=st.session_state.sch_prefill,
                                   placeholder="e.g. Study for math test")
        _sc_col1, _sc_col2 = st.columns(2)
        with _sc_col1:
            _new_date = st.date_input("Ask questions from", value=_today_d, key="_sch_date")
        with _sc_col2:
            _new_end  = st.date_input("Ask questions until", value=_today_d + _dt2.timedelta(days=6),
                                      key="_sch_end_date")
        _new_note = st.text_area("Topic details & chapters (AI uses this to make questions)", key="_sch_note", height=70,
                                 placeholder="e.g. Physics – Chapter 3 Laws of Motion, Chapter 4 Work & Energy. Focus on numericals and definitions.")
        _new_qpd = st.number_input("Questions per day", min_value=1, max_value=10, value=3, step=1, key="_sch_qpd")
        st.markdown("<div style='color:#9ca3af;font-size:0.82rem;margin-bottom:6px'>Set the time for each question:</div>", unsafe_allow_html=True)
        _default_times_map = {
            1:["10:00"],2:["10:00","18:00"],3:["09:00","14:00","19:00"],
            4:["09:00","12:00","16:00","20:00"],5:["09:00","11:00","13:00","16:00","19:00"],
            6:["08:00","10:00","12:00","15:00","18:00","21:00"],
            7:["08:00","10:00","12:00","14:00","16:00","18:00","20:00"],
            8:["08:00","09:30","11:00","13:00","15:00","17:00","19:00","21:00"],
            9:["08:00","09:30","11:00","12:30","14:00","15:30","17:00","19:00","21:00"],
            10:["08:00","09:00","10:00","12:00","13:00","15:00","16:00","18:00","19:00","21:00"],
        }
        _def_times = _default_times_map.get(int(_new_qpd), _default_times_map[5])
        _time_cols_per_row = 5
        _new_q_times = []
        for _ti_row in range(0, int(_new_qpd), _time_cols_per_row):
            _t_cols = st.columns(_time_cols_per_row)
            for _ti in range(_ti_row, min(_ti_row + _time_cols_per_row, int(_new_qpd))):
                _def_h, _def_m = map(int, _def_times[_ti].split(":"))
                with _t_cols[_ti - _ti_row]:
                    _t_val = st.time_input(f"Q{_ti+1}", value=_dt2.time(_def_h, _def_m),
                                           key=f"_sch_time_{_ti}", label_visibility="visible")
                    _new_q_times.append(_t_val.strftime("%H:%M"))
        if st.button("Add to Schedule", key="_sch_add", use_container_width=True):
            if _new_title.strip():
                _sch_data.append({
                    "id":               str(_uuid.uuid4())[:8],
                    "title":            _new_title.strip(),
                    "date":             str(_new_date),
                    "end_date":         str(_new_end),
                    "note":             _new_note.strip(),
                    "questions_per_day": int(_new_qpd),
                    "question_times":   _new_q_times,
                    "done":             False,
                    "added":            _today_str2,
                    "qa_history":       {},
                })
                _save_schedule(_sch_data)
                st.session_state["_sched_banner_dismissed"] = False
                st.session_state.sch_prefill = ""
                # Auto-launch scheduler in background if not already running
                if not _scheduler_running():
                    _launch_scheduler_bg()
                st.success("Schedule added! Question popups will appear automatically.")
                st.rerun()
            else:
                st.warning("Please enter a title.")

    # ── Active schedules ───────────────────────────────────────────────────────
    _active = [s for s in _sch_data if not s.get("done")]
    _done_s = [s for s in _sch_data if s.get("done")]

    if not _active:
        st.markdown("<div style='color:#4a5568;margin:16px 0'>No active schedules. Add one above.</div>",
                    unsafe_allow_html=True)

    for _s in _active:
        _sid   = _s.get("id","")
        _sdate = _s.get("date","")
        _edate = _s.get("end_date","9999-12-31")
        _in_range = _sdate <= _today_str2 <= _edate

        if _today_str2 > _edate:
            _date_label = f"Ended {_edate}"
            _lc = "#4a5568"
        elif _sdate > _today_str2:
            _date_label = f"Starts {_sdate}"
            _lc = "#4a5568"
        else:
            _days_left = (_dt2.date.fromisoformat(_edate) - _today_d).days
            _date_label = f"Today — {_days_left} day(s) left"
            _lc = "#a855f7"

        with st.container():
            _h1, _h2, _h3 = st.columns([5, 2, 1])
            with _h1:
                st.markdown(
                    f"<div style='color:#e8e8e8;font-weight:600;font-size:.9rem'>{_s['title']}</div>"
                    f"<div style='color:{_lc};font-size:.72rem'>{_date_label}</div>"
                    + (f"<div style='color:#4a5568;font-size:.74rem'>{_s['note']}</div>"
                       if _s.get("note") else ""),
                    unsafe_allow_html=True)
            with _h2:
                # Today's Q&A progress
                _qa_today = _s.get("qa_history", {}).get(_today_str2, [])
                _answered = sum(1 for q in _qa_today if q.get("a"))
                _total    = len(_qa_today)
                if _in_range and _total > 0:
                    st.markdown(
                        f"<div style='color:#00e5d0;font-size:.78rem;padding-top:4px'>"
                        f"Today: {_answered}/{_total} answered</div>",
                        unsafe_allow_html=True)
                elif _in_range:
                    st.markdown(
                        "<div style='color:#4a5568;font-size:.74rem;padding-top:4px'>"
                        "Questions generate at 9 am</div>",
                        unsafe_allow_html=True)
            with _h3:
                if st.button("✓", key=f"_sch_done_{_sid}", help="Mark complete"):
                    for _item in _sch_data:
                        if _item.get("id") == _sid:
                            _item["done"] = True
                            _item["completed"] = _today_str2
                    _save_schedule(_sch_data)
                    st.session_state["_sched_banner_dismissed"] = False
                    st.rerun()
                if st.button("🗑", key=f"_sch_del_{_sid}", help="Delete"):
                    _sch_data = [x for x in _sch_data if x.get("id") != _sid]
                    _save_schedule(_sch_data)
                    st.rerun()

            # Today's Q&A inline (answer here if popup was missed)
            if _in_range and _qa_today:
                with st.expander("Today's questions", expanded=False):
                    for _qi, _qa in enumerate(_qa_today):
                        _q_col1, _q_col2 = st.columns([3,2])
                        with _q_col1:
                            st.markdown(
                                f"<div style='color:#e8e8e8;font-size:.82rem'><b>Q{_qi+1}.</b> {_qa['q']}</div>",
                                unsafe_allow_html=True)
                        with _q_col2:
                            if _qa.get("a"):
                                st.markdown(
                                    f"<div style='color:#00e5d0;font-size:.8rem'>✓ {_qa['a']}</div>",
                                    unsafe_allow_html=True)
                            else:
                                _inline_ans = st.text_input("", key=f"_qans_{_sid}_{_qi}",
                                                            placeholder="Type answer…",
                                                            label_visibility="collapsed")
                                if st.button("Save", key=f"_qsave_{_sid}_{_qi}"):
                                    if _inline_ans.strip():
                                        for _it2 in _sch_data:
                                            if _it2.get("id") == _sid:
                                                _it2.setdefault("qa_history", {}).setdefault(
                                                    _today_str2, _qa_today
                                                )[_qi]["a"] = _inline_ans.strip()
                                        _save_schedule(_sch_data)
                                        st.rerun()

            # Past Q&A history
            _past_days = sorted(
                [d for d in _s.get("qa_history", {}) if d != _today_str2],
                reverse=True
            )
            if _past_days:
                with st.expander(f"History ({len(_past_days)} day(s))", expanded=False):
                    for _day in _past_days[:14]:
                        _day_qa = _s["qa_history"][_day]
                        _day_ans = sum(1 for q in _day_qa if q.get("a"))
                        st.markdown(
                            f"<div style='color:#4a5568;font-size:.72rem;font-weight:600;"
                            f"margin:6px 0 2px'>{_day}  —  {_day_ans}/{len(_day_qa)} answered</div>",
                            unsafe_allow_html=True)
                        for _pqa in _day_qa:
                            if _pqa.get("a"):
                                st.markdown(
                                    f"<div style='color:#e8e8e8;font-size:.78rem;margin-left:8px'>"
                                    f"<b>Q:</b> {_pqa['q']}</div>"
                                    f"<div style='color:#00e5d0;font-size:.78rem;margin-left:8px'>"
                                    f"<b>A:</b> {_pqa['a']}</div>",
                                    unsafe_allow_html=True)

            st.markdown("<hr style='border-color:#1a1a2e;margin:8px 0'>", unsafe_allow_html=True)

    # ── Completed ─────────────────────────────────────────────────────────────
    if _done_s:
        with st.expander(f"Completed ({len(_done_s)})", expanded=False):
            for _s in _done_s:
                _cc1, _cc2 = st.columns([7,1])
                with _cc1:
                    st.markdown(
                        f"<div style='color:#4a5568;font-size:.85rem;"
                        f"text-decoration:line-through'>{_s['title']}</div>"
                        f"<div style='color:#2d3748;font-size:.7rem'>Done {_s.get('completed','')}</div>",
                        unsafe_allow_html=True)
                with _cc2:
                    if st.button("🗑", key=f"_sch_cdel_{_s.get('id','')}"):
                        _sch_data = [x for x in _sch_data if x.get("id") != _s.get("id")]
                        _save_schedule(_sch_data)
                        st.rerun()
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# ── TASKS PAGE ────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.tasks_mode:
    import datetime as _tdt, uuid as _tuuid

    st.markdown("""
    <h2 style='color:#ffffff;font-family:Orbitron,monospace;font-weight:900;
    font-size:1.4rem;letter-spacing:2px;margin-bottom:2px'>⊞ Tasks</h2>
    <p style='color:#4a5568;font-size:.8rem;margin-top:0'>
    Tell Titan what to fetch for you daily — sales, news, prices, anything. Opens inside Titan Ultra.</p>
    """, unsafe_allow_html=True)

    _tk_data  = _load_tasks()
    _tk_today = str(_tdt.date.today())

    # ── Helper: run one task ────────────────────────────────────────────────────
    def _run_task(task):
        _search_q = f"{task['prompt']} {_tk_today}"
        _sr = _web_search(_search_q, max_results=10)
        try:
            from groq import Groq as _TG
            _tc = _TG(api_key=st.session_state.api_key)
            _tsys = (
                "You are TITAN ULTRA's daily task engine. "
                "The user has set up a recurring daily task shown below. "
                "Using the web search results provided, give a detailed, well-organised daily report. "
                "For prices/sales: list items with name, original price, sale price, discount %. "
                "For news: list top stories with a 2-sentence summary each. "
                "Use bullet points and bold headings. Be specific, factual, and helpful. "
                f"Today: {_tk_today}\n\n"
                f"LIVE SEARCH RESULTS:\n{_sr if _sr else 'No search results — answer from knowledge.'}"
            )
            _tr = _tc.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": _tsys},
                    {"role": "user",   "content": task["prompt"]},
                ],
                max_tokens=2000,
                temperature=0.3,
            )
            return _tr.choices[0].message.content or "No result."
        except Exception as _te:
            return _sr if _sr else f"Error: {_te}"

    # ── Add new task ────────────────────────────────────────────────────────────
    _TK_SUGGESTIONS = [
        "Daily Flipkart & Amazon electronics deals under ₹8000",
        "Today's best smartphone offers on Flipkart",
        "Today's news in Bangalore",
        "Top India news today",
        "Cheapest laptops on sale today under ₹30000",
        "Today's petrol price in Hyderabad",
        "Current gold and silver prices in India",
        "Today's cricket match scores and highlights",
        "Best budget earphones on sale today",
        "Today's movie OTT releases in India",
        "Tech news today — new launches and updates",
        "Today's weather in Hyderabad",
    ]
    if "tk_prefill" not in st.session_state:
        st.session_state.tk_prefill = ""

    with st.expander("＋  add new task", expanded=st.session_state.tk_prefill != ""):
        st.markdown("<div style='font-size:.72rem;color:#4a5568;margin-bottom:6px'>Quick suggestions:</div>",
                    unsafe_allow_html=True)
        _tk_sug_cols = st.columns(2)
        for _tsi, _tsug in enumerate(_TK_SUGGESTIONS):
            with _tk_sug_cols[_tsi % 2]:
                if st.button(_tsug, key=f"_tksug_{_tsi}", use_container_width=True):
                    st.session_state.tk_prefill = _tsug
                    st.rerun()
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        _tk_prompt = st.text_area("What should Titan fetch for you every day?",
                                  value=st.session_state.tk_prefill,
                                  key="_tk_prompt", height=72,
                                  placeholder="e.g. Give me today's electronics deals under ₹8000 on Flipkart and Amazon")
        _tk_col1, _tk_col2 = st.columns(2)
        with _tk_col1:
            _tk_start = st.date_input("From", value=_tdt.date.today(), key="_tk_start")
        with _tk_col2:
            _tk_end = st.date_input("Until", value=_tdt.date.today() + _tdt.timedelta(days=29),
                                    key="_tk_end")
        if st.button("Add Task", key="_tk_add", use_container_width=True):
            if _tk_prompt.strip():
                _tk_data.append({
                    "id":       str(_tuuid.uuid4())[:8],
                    "prompt":   _tk_prompt.strip(),
                    "start":    str(_tk_start),
                    "end":      str(_tk_end),
                    "active":   True,
                    "added":    _tk_today,
                    "results":  {},
                })
                _save_tasks(_tk_data)
                st.session_state.tk_prefill = ""
                st.rerun()
            else:
                st.warning("Please describe what you want Titan to fetch.")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Run and display active tasks ────────────────────────────────────────────
    _tk_active = [t for t in _tk_data if t.get("active") and
                  t.get("start","") <= _tk_today <= t.get("end","9999-12-31")]
    _tk_inactive = [t for t in _tk_data if not t.get("active") or t.get("end","") < _tk_today]

    if not _tk_active:
        st.markdown("<div style='color:#4a5568;margin:12px 0'>No active tasks. Add one above.</div>",
                    unsafe_allow_html=True)

    for _tk in _tk_active:
        _tkid   = _tk.get("id","")
        _tk_end_str = _tk.get("end","")
        _tk_days_left = (_tdt.date.fromisoformat(_tk_end_str) - _tdt.date.today()).days if _tk_end_str else "?"

        with st.container():
            _tkh1, _tkh2 = st.columns([7,2])
            with _tkh1:
                st.markdown(
                    f"<div style='color:#e8e8e8;font-weight:600;font-size:.92rem'>{_tk['prompt'][:80]}</div>"
                    f"<div style='color:#4a5568;font-size:.72rem'>Until {_tk_end_str}  ·  {_tk_days_left} day(s) left</div>",
                    unsafe_allow_html=True)
            with _tkh2:
                if st.button("Close task", key=f"_tk_close_{_tkid}"):
                    for _titem in _tk_data:
                        if _titem.get("id") == _tkid:
                            _titem["active"] = False
                    _save_tasks(_tk_data)
                    st.rerun()
                if st.button("🗑 Delete", key=f"_tk_del_{_tkid}"):
                    _tk_data = [x for x in _tk_data if x.get("id") != _tkid]
                    _save_tasks(_tk_data)
                    st.rerun()

            # Show today's result — auto-fetch if not yet cached
            if _tk.get("results",{}).get(_tk_today):
                _tk_result = _tk["results"][_tk_today]
            else:
                with st.spinner(f"Fetching today's result for: {_tk['prompt'][:50]}…"):
                    _tk_result = _run_task(_tk)
                    for _titem in _tk_data:
                        if _titem.get("id") == _tkid:
                            _titem.setdefault("results",{})[_tk_today] = _tk_result
                    _save_tasks(_tk_data)

            st.markdown(
                f"<div style='background:#111111;border-left:3px solid #00e5d0;"
                f"border-radius:8px;padding:12px 16px;margin:8px 0;color:#e8e8e8;"
                f"font-size:.88rem;white-space:pre-wrap;line-height:1.6'>"
                f"<div style='color:#00e5d0;font-size:.7rem;font-weight:700;"
                f"letter-spacing:1px;margin-bottom:6px'>TODAY — {_tk_today}</div>"
                + _tk_result.replace("<","&lt;").replace(">","&gt;")
                .replace("**","<b>").replace("\n","<br>")
                + "</div>",
                unsafe_allow_html=True)

            # Past results history
            _tk_past = sorted([d for d in _tk.get("results",{}) if d != _tk_today], reverse=True)
            if _tk_past:
                with st.expander(f"History ({len(_tk_past)} day(s))", expanded=False):
                    for _tkday in _tk_past[:7]:
                        st.markdown(
                            f"<div style='color:#4a5568;font-size:.72rem;font-weight:700;"
                            f"margin:8px 0 4px'>{_tkday}</div>"
                            f"<div style='color:#8899aa;font-size:.8rem;white-space:pre-wrap'>"
                            + _tk["results"][_tkday].replace("<","&lt;").replace(">","&gt;")[:600]
                            + ("…" if len(_tk["results"][_tkday]) > 600 else "")
                            + "</div>",
                            unsafe_allow_html=True)

            st.markdown("<hr style='border-color:#1a1a2e;margin:10px 0'>", unsafe_allow_html=True)

    # ── Closed / expired tasks ──────────────────────────────────────────────────
    if _tk_inactive:
        with st.expander(f"Closed / Expired ({len(_tk_inactive)})", expanded=False):
            for _tk in _tk_inactive:
                _tc1, _tc2 = st.columns([7,1])
                with _tc1:
                    st.markdown(
                        f"<div style='color:#4a5568;font-size:.85rem;"
                        f"text-decoration:line-through'>{_tk['prompt'][:70]}</div>"
                        f"<div style='color:#2d3748;font-size:.7rem'>Ended {_tk.get('end','')}</div>",
                        unsafe_allow_html=True)
                with _tc2:
                    if st.button("🗑", key=f"_tkc_del_{_tk.get('id','')}"):
                        _tk_data = [x for x in _tk_data if x.get("id") != _tk.get("id")]
                        _save_tasks(_tk_data)
                        st.rerun()
    st.stop()


# ── LIBRARY PAGE ──────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.library_mode:
    st.markdown("""
    <h2 style='color:#ffffff;font-family:Orbitron,monospace;font-weight:900;
    font-size:1.4rem;letter-spacing:2px;margin-bottom:4px'>📚 Library</h2>
    <p style='color:#4a5568;font-size:.8rem;margin-top:0'>Search all your saved chats</p>
    """, unsafe_allow_html=True)

    _lib_query = st.text_input("", placeholder="Search chats by title or content…",
                               label_visibility="collapsed", key="_lib_search")

    _all_chats = _load_history()

    if _lib_query.strip():
        _q = _lib_query.strip().lower()
        _results = []
        for _ch in _all_chats:
            _title = _ch.get("title", "Chat")
            _msgs  = _ch.get("messages", [])
            _match_title = _q in _title.lower()
            _match_lines = []
            for _m in _msgs:
                _txt = _m.get("content", "")
                if isinstance(_txt, list):
                    _txt = " ".join(p.get("text","") for p in _txt if isinstance(p,dict))
                if _q in _txt.lower():
                    idx = _txt.lower().find(_q)
                    snippet = _txt[max(0,idx-60):idx+120].replace("\n"," ")
                    _match_lines.append(snippet)
            if _match_title or _match_lines:
                _results.append((_ch, _title, _match_lines))

        if not _results:
            st.markdown("<div style='color:#4a5568;margin-top:24px'>No chats match your search.</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#4a5568;font-size:.75rem;margin-bottom:8px'>{len(_results)} result(s)</div>",
                        unsafe_allow_html=True)
            for _ch, _title, _snippets in _results:
                with st.container():
                    _col1, _col2 = st.columns([5,1])
                    with _col1:
                        st.markdown(f"<div style='color:#e8e8e8;font-weight:600;font-size:.9rem'>{_title}</div>",
                                    unsafe_allow_html=True)
                        for _snip in _snippets[:2]:
                            _hi = _snip.replace(_lib_query, f"<mark style='background:#a855f733;color:#e8e8e8'>{_lib_query}</mark>")
                            st.markdown(f"<div style='color:#4a5568;font-size:.78rem;margin:2px 0 0 8px'>…{_hi}…</div>",
                                        unsafe_allow_html=True)
                    with _col2:
                        if st.button("Open", key=f"_lib_open_{_ch.get('id',0)}"):
                            _save_chat_sessions()
                            st.session_state.chat_sessions = [_ch]
                            st.session_state.active_session = 0
                            st.session_state.library_mode = False
                            st.rerun()
                    st.markdown("<hr style='border-color:#1a1a2e;margin:6px 0'>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:#4a5568;font-size:.78rem;margin-top:8px'>{len(_all_chats)} total chat(s)</div>",
                    unsafe_allow_html=True)
        for _ch in _all_chats[:80]:
            _col1, _col2 = st.columns([5,1])
            with _col1:
                _msgs_count = len(_ch.get("messages",[]))
                st.markdown(
                    f"<div style='color:#e8e8e8;font-size:.88rem'>{_ch.get('title','Chat')}</div>"
                    f"<div style='color:#4a5568;font-size:.72rem'>{_msgs_count} message(s)</div>",
                    unsafe_allow_html=True)
            with _col2:
                if st.button("Open", key=f"_lib_list_{_ch.get('id',0)}"):
                    _save_chat_sessions()
                    st.session_state.chat_sessions = [_ch]
                    st.session_state.active_session = 0
                    st.session_state.library_mode = False
                    st.rerun()
            st.markdown("<hr style='border-color:#1a1a2e;margin:4px 0'>", unsafe_allow_html=True)
    st.stop()


# ── TITAN NOTEBOOK PAGE ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.notebook_mode:

    # ── helpers ───────────────────────────────────────────────────────────────
    def _nb_source_text():
        return "\n\n---\n\n".join(
            f"[Source {i+1}: {s['name']}]\n{s['text']}"
            for i, s in enumerate(st.session_state.notebook_sources)
        )

    def _nb_ask(prompt, max_tokens=4096):
        _topic = st.session_state.get("nb_notebook_title", "the topic")
        try:
            from groq import Groq as _G
            _c = _G(api_key=st.session_state.api_key)
            _sys = (
                "You are Titan Notebook — a world-class AI study and research assistant inside TITAN ULTRA. "
                f"The user is working on: \"{_topic}\"\n"
                "Provide deeply accurate, well-structured, expert-level content on this topic. "
                "Use clear headings, bullet points, and examples. Be thorough and genuinely useful."
            )
            _r = _c.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role":"system","content":_sys},
                          {"role":"user","content":prompt}],
                max_tokens=max_tokens,
                temperature=0.3,
            )
            return _r.choices[0].message.content or ""
        except Exception as _e:
            try:
                _c2 = _G(api_key=st.session_state.api_key)
                _r2 = _c2.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role":"system","content":_sys},
                              {"role":"user","content":prompt}],
                    max_tokens=max_tokens,
                    temperature=0.3,
                )
                return _r2.choices[0].message.content or ""
            except Exception as _e2:
                return f"❌ Error: {_e2}"

    def _nb_read_pdf(file_bytes):
        try:
            import pdfplumber, io
            text = ""
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n"
            return text.strip()
        except Exception:
            try:
                import PyPDF2, io
                reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                return "\n".join(p.extract_text() or "" for p in reader.pages).strip()
            except Exception as e:
                return f"[Could not read PDF: {e}]"

    def _nb_read_url(url):
        try:
            import requests as _req
            from bs4 import BeautifulSoup as _BS
            r = _req.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
            soup = _BS(r.text, "html.parser")
            for tag in soup(["script","style","nav","footer","header"]):
                tag.decompose()
            return soup.get_text(separator="\n", strip=True)[:8000]
        except Exception as e:
            return f"[Could not read URL: {e}]"

    def _nb_parse_flashcards(text):
        cards = []
        lines = text.strip().split("\n")
        i = 0
        while i < len(lines):
            l = lines[i].strip()
            if l.upper().startswith("FRONT:"):
                front = l[6:].strip()
                back = wrong1 = wrong2 = wrong3 = ""
                if i+1 < len(lines) and lines[i+1].strip().upper().startswith("BACK:"):
                    back = lines[i+1].strip()[5:].strip()
                if i+2 < len(lines) and lines[i+2].strip().upper().startswith("WRONG1:"):
                    wrong1 = lines[i+2].strip()[7:].strip()
                if i+3 < len(lines) and lines[i+3].strip().upper().startswith("WRONG2:"):
                    wrong2 = lines[i+3].strip()[7:].strip()
                if i+4 < len(lines) and lines[i+4].strip().upper().startswith("WRONG3:"):
                    wrong3 = lines[i+4].strip()[7:].strip()
                if front and back:
                    cards.append({
                        "front": front, "back": back,
                        "wrong": [w for w in [wrong1, wrong2, wrong3] if w]
                    })
                i += 5
                continue
            i += 1
        return cards

    # ── Landing screen (shown until user types a topic) ───────────────────────
    _nb_has_src = not bool(st.session_state.get("nb_notebook_title", ""))
    if _nb_has_src:
        _nb_sel_mode = st.session_state.get("nb_mode", "organise")
        _org_bg = "#2d3d8c" if _nb_sel_mode == "organise" else "#1c1c1c"
        _org_bd = "1.5px solid #5068d0" if _nb_sel_mode == "organise" else "1px solid #252525"
        _stu_bg = "#2d3d8c" if _nb_sel_mode == "study" else "#1c1c1c"
        _stu_bd = "1.5px solid #5068d0" if _nb_sel_mode == "study" else "1px solid #252525"
        _chk_display = "flex" if _nb_sel_mode == "organise" else "none"

        st.markdown(f"""<style>
/* ── Big borderless input ── */
[data-testid="stTextInput"] input {{
    font-size:2.3rem !important; font-weight:300 !important;
    color:#cccccc !important; background:transparent !important;
    border:none !important; box-shadow:none !important;
    border-radius:0 !important; padding:0 0 0 2px !important;
    letter-spacing:-0.5px !important; caret-color:#888 !important;
    outline:none !important;
}}
[data-testid="stTextInput"] input::placeholder {{
    color:#3d3d3d !important; opacity:1 !important;
}}
[data-testid="stTextInput"] input:focus {{
    outline:none !important; box-shadow:none !important; border:none !important;
}}
[data-baseweb="input"], [data-baseweb="base-input"] {{
    background:transparent !important; border:none !important;
    box-shadow:none !important; padding:0 !important;
}}
[data-testid="stTextInput"] {{ margin:0 !important; padding:0 !important; }}

/* ── Mode cards ── */
.nb-card-wrap div[data-testid="stButton"] > button {{
    min-height:155px !important; width:100% !important;
    text-align:left !important; border-radius:14px !important;
    padding:16px 14px 12px !important; white-space:normal !important;
    line-height:1.5 !important; transition:background .2s,border .2s !important;
    display:flex !important; flex-direction:column !important;
    align-items:flex-start !important; position:relative !important;
}}
.nb-card-wrap div[data-testid="stButton"] > button > div {{
    display:flex !important; flex-direction:column !important;
    align-items:flex-start !important; text-align:left !important; width:100% !important;
}}
.nb-card-wrap div[data-testid="stButton"] > button > div > p:nth-child(1) {{
    font-size:1.45rem !important; line-height:1 !important; margin-bottom:10px !important;
    color:#c8cce8 !important;
}}
.nb-card-wrap div[data-testid="stButton"] > button > div > p:nth-child(2) {{
    font-size:0.97rem !important; font-weight:700 !important;
    color:#ffffff !important; margin-bottom:6px !important;
}}
.nb-card-wrap div[data-testid="stButton"] > button > div > p:nth-child(3) {{
    font-size:0.77rem !important; color:#8a90aa !important; font-weight:400 !important;
}}
.nb-card-org div[data-testid="stButton"] > button {{
    background:{_org_bg} !important; border:{_org_bd} !important; color:#e8e8e8 !important;
}}
.nb-card-stu div[data-testid="stButton"] > button {{
    background:{_stu_bg} !important; border:{_stu_bd} !important; color:#e8e8e8 !important;
}}
.nb-card-org div[data-testid="stButton"] > button::after {{
    content:'✓'; position:absolute; top:12px; right:12px;
    background:#1a2555; border:1.5px solid #5068d0; border-radius:50%;
    width:22px; height:22px; display:{_chk_display};
    align-items:center; justify-content:center;
    font-size:0.65rem; color:#fff; font-weight:700;
}}
.nb-card-wrap div[data-testid="stButton"] > button:hover {{
    filter:brightness(1.1) !important;
}}
</style>""", unsafe_allow_html=True)

        # Icon + heading
        st.html("""
<div style='padding:56px 0 0'>
  <div style='font-size:1.6rem;color:#bbbfd8;margin-bottom:16px;line-height:1'>◫</div>
  <div style='font-size:1.2rem;font-weight:700;color:#ffffff;margin-bottom:20px;
              letter-spacing:-0.2px'>What are you working on?</div>
</div>""")

        # Large borderless topic input
        _nb_title_val = st.text_input(
            "", placeholder="Project or idea",
            key="_nb_title_input", label_visibility="collapsed"
        )
        if _nb_title_val:
            st.session_state["nb_notebook_title"] = _nb_title_val
            st.session_state.notebook_generated = {}
            st.rerun()

        # Auto-focus + typewriter placeholder (like Gemini NotebookLM)
        st.html("""<script>
(function(){
  var ph = [
    "Weekly meal prep","Project or idea","A topic to study",
    "My research notes","Chapter summary","Exam preparation",
    "Book analysis","Science project","History essay",
    "Lecture notes","Meeting notes","Research paper",
    "Case study","Literature review","Biology revision",
    "Programming concepts","World history","Physics formulas"
  ];
  var phIdx = 0, charIdx = 0, deleting = false, pause = 0;

  function run(){
    var inp = document.querySelector('[data-testid="stTextInput"] input');
    if(!inp){ setTimeout(run, 200); return; }
    // Auto-focus on first run
    if(document.activeElement !== inp && !inp.value) inp.focus();

    function tick(){
      if(inp.value) return; // user started typing — freeze animation
      if(pause > 0){ pause--; return; }
      var word = ph[phIdx];
      if(!deleting){
        charIdx++;
        inp.setAttribute('placeholder', word.slice(0, charIdx));
        if(charIdx >= word.length){ deleting = true; pause = 38; }
      } else {
        charIdx--;
        inp.setAttribute('placeholder', word.slice(0, charIdx));
        if(charIdx <= 0){
          deleting = false;
          phIdx = (phIdx + 1) % ph.length;
          pause = 8;
        }
      }
    }
    setInterval(tick, 80);
  }
  run();
})();
</script>""")

        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

        # Mode cards — match image layout exactly
        _mcc1, _mcc2, _mcc3 = st.columns([1.7, 1.7, 3.6])
        with _mcc1:
            st.markdown('<div class="nb-card-wrap nb-card-org">', unsafe_allow_html=True)
            if st.button(
                "◎\nOrganise your ideas\nGroup chats by topic and ground on your sources.",
                key="_nb_mode_org", use_container_width=True
            ):
                st.session_state.nb_mode = "organise"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with _mcc2:
            st.markdown('<div class="nb-card-wrap nb-card-stu">', unsafe_allow_html=True)
            if st.button(
                "◈\nStudy and learn\nFlashcards, quizzes, summaries and deep study tools.",
                key="_nb_mode_stu", use_container_width=True
            ):
                st.session_state.nb_mode = "study"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.stop()

    # ── Compact header (topic set, tools visible) ─────────────────────────────
    _nb_active_topic = st.session_state.get("nb_notebook_title", "")
    _nbc1, _nbc2 = st.columns([6, 1])
    with _nbc1:
        st.markdown(f"<div style='font-size:1.1rem;font-weight:700;color:#e8e8e8;padding:10px 0 4px'>◫ {_nb_active_topic}</div>", unsafe_allow_html=True)
    with _nbc2:
        if st.button("✕ clear", key="_nb_clear_topic", use_container_width=True):
            st.session_state["nb_notebook_title"] = ""
            st.session_state.notebook_generated = {}
            st.rerun()
    st.markdown("<div style='border-bottom:1px solid #222;margin-bottom:14px'></div>", unsafe_allow_html=True)

    # ── Generate buttons ──────────────────────────────────────────────────────
    st.markdown("### Generate")
    _gb1, _gb2, _gb3, _gb4, _gb5, _gb6 = st.columns(6)

    if _gb1.button("Summary", use_container_width=True, key="_nb_gen_sum"):
        with st.spinner("Generating summary..."):
            st.session_state.notebook_generated["summary"] = _nb_ask(
                "Write a detailed executive summary of all the sources. "
                "Cover all key points, main ideas, and important details. "
                "Use clear headings and bullet points."
            )
        st.rerun()

    if _gb2.button("Study Guide", use_container_width=True, key="_nb_gen_sg"):
        with st.spinner("Creating study guide..."):
            st.session_state.notebook_generated["study_guide"] = _nb_ask(
                "Create a comprehensive study guide from these sources. Include: "
                "1. Key Concepts with explanations "
                "2. Important Terms & Definitions "
                "3. Main Topics breakdown "
                "4. Key Facts to remember "
                "5. Common exam points "
                "Format with clear headings and bullet points."
            )
        st.rerun()

    if _gb3.button("Flashcards", use_container_width=True, key="_nb_gen_fc"):
        _topic_fc = st.session_state.get("nb_notebook_title", "the topic")
        with st.spinner("Generating flashcards..."):
            _fc_resp = _nb_ask(
                f"Generate 15 high-quality multiple-choice flashcards about: {_topic_fc}\n\n"
                "For EACH card use EXACTLY this format (5 lines per card, blank line between cards):\n"
                "FRONT: [a clear question]\n"
                "BACK: [the correct answer — keep it short, under 12 words]\n"
                "WRONG1: [plausible but wrong option]\n"
                "WRONG2: [plausible but wrong option]\n"
                "WRONG3: [plausible but wrong option]\n\n"
                "Make wrong options realistic. Cover key concepts thoroughly."
            )
            _nb_cards = _nb_parse_flashcards(_fc_resp)
            if _nb_cards:
                st.session_state.notebook_generated["flashcards"] = _nb_cards
                st.session_state.nb_card_index = 0
                st.session_state.nb_card_flipped = False
            else:
                st.session_state.notebook_generated["flashcards_raw"] = _fc_resp
        st.rerun()

    if _gb4.button("FAQ", use_container_width=True, key="_nb_gen_faq"):
        with st.spinner("Generating FAQ..."):
            st.session_state.notebook_generated["faq"] = _nb_ask(
                "Generate 15 frequently asked questions with detailed answers "
                "based on these sources. Format as:\n"
                "**Q: [question]**\nA: [detailed answer]\n\n"
                "Cover the most important and commonly asked topics."
            )
        st.rerun()

    if _gb5.button("Quiz", use_container_width=True, key="_nb_gen_quiz"):
        with st.spinner("Creating quiz..."):
            st.session_state.notebook_generated["quiz"] = _nb_ask(
                "Create a 15-question multiple choice quiz from these sources. "
                "For each question use this format:\n"
                "**Q1. [question]**\n"
                "A) [option]\nB) [option]\nC) [option]\nD) [option]\n"
                "✅ Answer: [correct letter] — [brief explanation]\n\n"
                "Make questions challenging and cover all major topics."
            )
        st.rerun()

    if _gb6.button("Timeline", use_container_width=True, key="_nb_gen_tl"):
        with st.spinner("Building timeline..."):
            st.session_state.notebook_generated["timeline"] = _nb_ask(
                "Extract all dates, events, and chronological information from these sources. "
                "Create a detailed timeline in chronological order. Format as:\n"
                "**[Year/Date]** — [Event description]\n\n"
                "If no specific dates, organize key developments in logical sequence."
            )
        st.rerun()

    # ── Show generated content ────────────────────────────────────────────────
    _gen = st.session_state.notebook_generated
    _nb_tabs_labels = []
    if "summary"     in _gen: _nb_tabs_labels.append("📋 Summary")
    if "study_guide" in _gen: _nb_tabs_labels.append("🗂️ Study Guide")
    if "flashcards"  in _gen or "flashcards_raw" in _gen: _nb_tabs_labels.append("🃏 Flashcards")
    if "faq"         in _gen: _nb_tabs_labels.append("❓ FAQ")
    if "quiz"        in _gen: _nb_tabs_labels.append("📝 Quiz")
    if "timeline"    in _gen: _nb_tabs_labels.append("📅 Timeline")

    if _nb_tabs_labels:
        st.markdown("---")
        st.markdown("### Generated Content")
        _nb_tabs_labels = [l.split(" ",1)[1] if l[0] in "📋🗂🃏❓📝📅" else l for l in _nb_tabs_labels]
        _nb_tabs_labels = ["Summary" if "Summary" in l else
                           "Study Guide" if "Study" in l else
                           "Flashcards" if "Flash" in l else
                           "FAQ" if "FAQ" in l else
                           "Quiz" if "Quiz" in l else
                           "Timeline" if "Timeline" in l else l
                           for l in _nb_tabs_labels]
        _nb_content_tabs = st.tabs(_nb_tabs_labels)
        _nb_ti = 0

        if "summary" in _gen:
            with _nb_content_tabs[_nb_ti]:
                st.markdown(_gen["summary"])
                st.download_button("Download", _gen["summary"], "titan_summary.txt", key="_nb_dl_sum")
            _nb_ti += 1

        if "study_guide" in _gen:
            with _nb_content_tabs[_nb_ti]:
                st.markdown(_gen["study_guide"])
                st.download_button("Download", _gen["study_guide"], "titan_study_guide.txt", key="_nb_dl_sg")
            _nb_ti += 1

        if "flashcards" in _gen or "flashcards_raw" in _gen:
            with _nb_content_tabs[_nb_ti]:
                if "flashcards" in _gen:
                    import random as _fcr
                    _nb_cards = _gen["flashcards"]
                    _nb_ci = st.session_state.nb_card_index % len(_nb_cards)
                    _nb_card = _nb_cards[_nb_ci]

                    # Shuffle options once per card (stable across reruns)
                    _fc_opts_key = f"_fc_opts_{_nb_ci}"
                    if _fc_opts_key not in st.session_state:
                        _opts = [_nb_card["back"]] + _nb_card.get("wrong", [])
                        _fcr.shuffle(_opts)
                        st.session_state[_fc_opts_key] = _opts
                    _fc_opts = st.session_state[_fc_opts_key][:4]
                    _fc_sel_key = f"_fc_sel_{_nb_ci}"
                    _fc_answered = _fc_sel_key in st.session_state

                    # ── Two-column layout: options LEFT, big card RIGHT ────────
                    _fc_left, _fc_right = st.columns([2, 3])

                    with _fc_right:
                        # Big flashcard
                        st.markdown(f"""
<div style='background:linear-gradient(135deg,#0d1b3e,#1a2a5e);
border-radius:18px;padding:50px 36px;min-height:240px;
border:1.5px solid #2d4080;box-shadow:0 4px 32px #0d1b3e88;
display:flex;flex-direction:column;justify-content:center;margin-bottom:14px'>
  <div style='color:#4a8fff;font-size:0.62rem;letter-spacing:3px;
  font-weight:700;margin-bottom:22px'>FRONT · {_nb_ci+1}/{len(_nb_cards)}</div>
  <div style='color:#ffffff;font-size:1.15rem;font-weight:500;
  line-height:1.7'>{_nb_card["front"]}</div>
</div>""", unsafe_allow_html=True)
                        # Prev / Next
                        _fn1, _fn2 = st.columns(2)
                        with _fn1:
                            if st.button("← Prev", key=f"_nb_fc_prev_{_nb_ci}", use_container_width=True):
                                st.session_state.nb_card_index = (st.session_state.nb_card_index - 1) % len(_nb_cards)
                                st.session_state.nb_card_flipped = False
                                st.rerun()
                        with _fn2:
                            if st.button("Next →", key=f"_nb_fc_next_{_nb_ci}", use_container_width=True):
                                st.session_state.nb_card_index = (st.session_state.nb_card_index + 1) % len(_nb_cards)
                                st.session_state.nb_card_flipped = False
                                st.rerun()
                        st.markdown(f"<div style='color:#555;font-size:0.78rem;margin-top:6px'>Card {_nb_ci+1} of {len(_nb_cards)}</div>", unsafe_allow_html=True)

                    with _fc_left:
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                        _labels = ["A", "B", "C", "D"]
                        for _oi, _opt in enumerate(_fc_opts):
                            _is_correct = (_opt == _nb_card["back"])
                            _is_selected = (st.session_state.get(_fc_sel_key) == _oi)
                            if _fc_answered:
                                # Show color result — no buttons
                                if _is_correct:
                                    _bg = "#14532d"; _bd = "#22c55e"; _tx = "#86efac"; _icon = " ✓"
                                elif _is_selected:
                                    _bg = "#7f1d1d"; _bd = "#ef4444"; _tx = "#fca5a5"; _icon = " ✗"
                                else:
                                    _bg = "#111"; _bd = "#2a2a2a"; _tx = "#444"; _icon = ""
                                st.markdown(f"""
<div style='background:{_bg};border:2px solid {_bd};border-radius:12px;
padding:14px 16px;margin-bottom:10px;font-size:0.92rem;color:{_tx};
font-weight:{"700" if _is_correct or _is_selected else "400"}'>
  <span style='font-weight:800;margin-right:8px'>{_labels[_oi]}.</span>{_opt}{_icon}
</div>""", unsafe_allow_html=True)
                            else:
                                # Clickable option button
                                st.markdown(f"""
<style>
div[data-testid="stButton"] button[kind="secondary"].fc-opt-{_nb_ci}-{_oi} {{
    text-align:left !important;
}}
</style>""", unsafe_allow_html=True)
                                if st.button(
                                    f"{_labels[_oi]}.  {_opt}",
                                    key=f"_fc_opt_{_nb_ci}_{_oi}",
                                    use_container_width=True
                                ):
                                    st.session_state[_fc_sel_key] = _oi
                                    st.rerun()

                        # If answered, show Next button and correct answer note
                        if _fc_answered:
                            _sel_opt = _fc_opts[st.session_state.get(_fc_sel_key, 0)]
                            _was_right = (_sel_opt == _nb_card["back"])
                            st.markdown(
                                f"<div style='color:{'#22c55e' if _was_right else '#ef4444'};font-size:0.85rem;"
                                f"font-weight:700;margin:10px 0 8px'>{'Correct!' if _was_right else 'Wrong — see green for correct'}</div>",
                                unsafe_allow_html=True
                            )
                            if st.button("Next →", key=f"_fc_ans_next_{_nb_ci}", use_container_width=True):
                                st.session_state.nb_card_index = (st.session_state.nb_card_index + 1) % len(_nb_cards)
                                st.session_state.nb_card_flipped = False
                                st.rerun()

                    _nb_fc_text = "\n".join(f"Q: {c['front']}\nA: {c['back']}\n" for c in _nb_cards)
                    st.download_button("Download All Cards", _nb_fc_text, "titan_flashcards.txt", key="_nb_dl_fc")
                else:
                    st.markdown(_gen["flashcards_raw"])
            _nb_ti += 1

        if "faq" in _gen:
            with _nb_content_tabs[_nb_ti]:
                st.markdown(_gen["faq"])
                st.download_button("Download", _gen["faq"], "titan_faq.txt", key="_nb_dl_faq")
            _nb_ti += 1

        if "quiz" in _gen:
            with _nb_content_tabs[_nb_ti]:
                st.markdown(_gen["quiz"])
                st.download_button("Download", _gen["quiz"], "titan_quiz.txt", key="_nb_dl_quiz")
            _nb_ti += 1

        if "timeline" in _gen:
            with _nb_content_tabs[_nb_ti]:
                st.markdown(_gen["timeline"])
                st.download_button("Download", _gen["timeline"], "titan_timeline.txt", key="_nb_dl_tl")
            _nb_ti += 1

    # ── Chat with sources ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Chat with Your Sources")
    st.caption("Ask anything about your uploaded sources — Titan Notebook answers from them.")

    for _nbm in st.session_state.notebook_chat:
        with st.chat_message(_nbm["role"]):
            st.markdown(_nbm["content"])

    _nb_user_q = st.chat_input("Ask anything about your sources...", key="_nb_chat_input")
    if _nb_user_q:
        st.session_state.notebook_chat.append({"role":"user","content":_nb_user_q})
        with st.chat_message("user"):
            st.markdown(_nb_user_q)
        with st.chat_message("assistant"):
            with st.spinner("Searching sources..."):
                _nb_ans = _nb_ask(_nb_user_q)
            st.markdown(_nb_ans)
        st.session_state.notebook_chat.append({"role":"assistant","content":_nb_ans})
        st.rerun()

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# ── TITAN CODE PAGE (Max only) ────────────────────────────────────────────────
if st.session_state.get("show_titan_code") and st.session_state.get("titan_tier") == "max":
    st.markdown("""
<style>
@keyframes tcGold {
  0%,100%{box-shadow:0 0 16px rgba(245,158,11,.4),0 0 32px rgba(245,158,11,.15)}
  50%{box-shadow:0 0 28px rgba(251,191,36,.65),0 0 56px rgba(245,158,11,.3)}
}
.tc-header{text-align:center;padding:28px 0 18px}
.tc-header h1{font-size:1.8rem;font-weight:800;letter-spacing:3px;color:#fbbf24;
  text-shadow:0 0 24px rgba(245,158,11,.6);margin:0;line-height:1.2}
.tc-header p{color:#78716c;font-size:.82rem;margin:6px 0 0}
.tc-badge{display:inline-block;background:linear-gradient(135deg,#92400e,#b45309);
  color:#fde68a;font-size:.58rem;font-weight:700;letter-spacing:2px;padding:3px 10px;
  border-radius:20px;margin-bottom:12px}
</style>
<div class="tc-header">
  <div class="tc-badge">MAX EXCLUSIVE</div>
  <h1>⌨ TITAN CODE</h1>
  <p>The most powerful AI coding terminal on the internet — write, build, debug, fix anything</p>
</div>
""", unsafe_allow_html=True)

    # ── Mode tabs ──────────────────────────────────────────────────────────────
    _tc_mode = st.radio(
        "Mode", ["⊞ Build Something New", "⊟ Fix / Debug Code", "◎ Code Review", "⊙ Image → Code"],
        horizontal=True, key="_tc_mode", label_visibility="collapsed"
    )
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    _tc_api = st.session_state.get("api_key", "")

    if "⊞" in _tc_mode and "Build" in _tc_mode:
        # ── Build New ──────────────────────────────────────────────────────────
        _tc_c1, _tc_c2 = st.columns([1, 2])
        with _tc_c1:
            _tc_lang = st.selectbox("Language / Platform", [
                "Python", "HTML + CSS + JavaScript", "React (JSX)", "Flutter (Dart)",
                "Node.js", "FastAPI (Python)", "Java", "C++", "Go", "Rust",
                "Swift (iOS)", "Kotlin (Android)", "SQL", "Bash / Shell",
                "Arduino (C++)", "Unity (C#)", "Other (describe below)"
            ], key="_tc_lang")
        with _tc_c2:
            _tc_desc = st.text_area(
                "What do you want to build?",
                placeholder="Describe exactly what you want. Be specific!\n\nExamples:\n• A Python web scraper that collects news headlines and saves to CSV\n• A beautiful dark-mode to-do app in HTML/CSS/JS with local storage\n• A REST API in FastAPI with user authentication and PostgreSQL\n• A network router configuration script for home WiFi",
                height=120, key="_tc_desc"
            )
        if st.button("⚡ Generate Code", key="_tc_gen_build", use_container_width=True,
                     type="primary"):
            if _tc_desc.strip() and _tc_api:
                with st.spinner("Titan Code is building your project..."):
                    try:
                        from groq import Groq as _TCG
                        _tc_client = _TCG(api_key=_tc_api)
                        _tc_prompt = f"Language/Platform: {_tc_lang}\n\nBuild this: {_tc_desc.strip()}"
                        _tc_resp = _tc_client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {"role": "system", "content": CODE_SYSTEM},
                                {"role": "user", "content": _tc_prompt}
                            ],
                            max_tokens=8192,
                            temperature=0.15,
                        )
                        st.session_state["_tc_last_output"] = _tc_resp.choices[0].message.content or ""
                    except Exception as _tce:
                        st.error(f"Error: {_tce}")
            elif not _tc_desc.strip():
                st.warning("Describe what you want to build first!")

    elif "⊟" in _tc_mode:
        # ── Fix / Debug ────────────────────────────────────────────────────────
        st.markdown("<div style='font-size:.8rem;color:#fbbf24;margin-bottom:4px'>Paste your broken code + describe the error or problem:</div>", unsafe_allow_html=True)
        _tc_broken = st.text_area(
            "Broken code",
            placeholder="Paste the code here that has errors or isn't working...",
            height=180, key="_tc_broken", label_visibility="collapsed"
        )
        _tc_err_desc = st.text_input(
            "Error message or problem",
            placeholder="Paste the error message, or describe what's wrong (e.g. 'crashes on line 12', 'returns wrong value', 'TypeError: ...')",
            key="_tc_err", label_visibility="collapsed"
        )
        if st.button("🔧 Fix My Code", key="_tc_fix", use_container_width=True, type="primary"):
            if (_tc_broken.strip() or _tc_err_desc.strip()) and _tc_api:
                with st.spinner("Titan Code is diagnosing and fixing..."):
                    try:
                        from groq import Groq as _TCG2
                        _tc_client2 = _TCG2(api_key=_tc_api)
                        _fix_prompt = (
                            f"Fix this code completely. Find ALL bugs, not just one.\n\n"
                            f"BROKEN CODE:\n```\n{_tc_broken.strip()}\n```\n\n"
                            f"ERROR/PROBLEM: {_tc_err_desc.strip() or 'Code is not working correctly'}\n\n"
                            "Provide:\n1. Root cause analysis — what exactly is wrong\n"
                            "2. Complete fixed code (every line, no truncation)\n"
                            "3. What you changed and why\n4. How to prevent this bug in future"
                        )
                        _fix_resp = _tc_client2.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {"role": "system", "content": CODE_SYSTEM},
                                {"role": "user", "content": _fix_prompt}
                            ],
                            max_tokens=8192,
                            temperature=0.1,
                        )
                        st.session_state["_tc_last_output"] = _fix_resp.choices[0].message.content or ""
                    except Exception as _tce2:
                        st.error(f"Error: {_tce2}")
            else:
                st.warning("Paste the broken code or describe the problem first!")

    elif "◎" in _tc_mode:
        # ── Code Review ────────────────────────────────────────────────────────
        st.markdown("<div style='font-size:.8rem;color:#fbbf24;margin-bottom:4px'>Paste your code for an expert review:</div>", unsafe_allow_html=True)
        _tc_review_code = st.text_area(
            "Code to review",
            placeholder="Paste any code here for a thorough expert review...",
            height=200, key="_tc_review", label_visibility="collapsed"
        )
        if st.button("🔍 Review My Code", key="_tc_rev_btn", use_container_width=True, type="primary"):
            if _tc_review_code.strip() and _tc_api:
                with st.spinner("Titan Code is doing a deep expert review..."):
                    try:
                        from groq import Groq as _TCG3
                        _tc_client3 = _TCG3(api_key=_tc_api)
                        _rev_prompt = (
                            f"Do a comprehensive expert code review of this code:\n\n```\n{_tc_review_code.strip()}\n```\n\n"
                            "Review covering:\n"
                            "1. **Correctness** — bugs, logic errors, edge cases missed\n"
                            "2. **Performance** — time/space complexity, bottlenecks, optimizations\n"
                            "3. **Security** — vulnerabilities (injection, XSS, auth issues, etc.)\n"
                            "4. **Code Quality** — readability, naming, structure, DRY violations\n"
                            "5. **Best Practices** — modern patterns, anti-patterns used\n"
                            "6. **Improved Version** — rewrite the most problematic parts\n"
                            "Rate it overall: ⭐⭐⭐⭐⭐"
                        )
                        _rev_resp = _tc_client3.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {"role": "system", "content": CODE_SYSTEM},
                                {"role": "user", "content": _rev_prompt}
                            ],
                            max_tokens=8192,
                            temperature=0.2,
                        )
                        st.session_state["_tc_last_output"] = _rev_resp.choices[0].message.content or ""
                    except Exception as _tce3:
                        st.error(f"Error: {_tce3}")

    elif "⊙" in _tc_mode and "Image" in _tc_mode:
        # ── Image → Code ───────────────────────────────────────────────────────
        st.markdown("""
<div style='background:linear-gradient(135deg,#120f00,#1a1200);border:1px solid #f59e0b44;
border-radius:12px;padding:16px 20px;margin-bottom:12px'>
  <div style='font-size:.95rem;font-weight:700;color:#fbbf24;margin-bottom:6px'>⊙ Image → Code</div>
  <div style='font-size:.8rem;color:#a8a29e;line-height:1.7'>
    Upload a screenshot, mockup, or sketch of how your app should look.<br>
    Titan Code will analyze the image and generate <b style='color:#fde68a'>complete, working code</b> that matches it exactly.
  </div>
</div>
""", unsafe_allow_html=True)
        _tc_img_file = st.file_uploader(
            "Upload image (screenshot, mockup, sketch)",
            type=["png", "jpg", "jpeg", "webp"],
            key="_tc_img_upload",
            label_visibility="collapsed"
        )
        _tc_img_lang = st.selectbox("Output Language", [
            "HTML + CSS + JavaScript", "React (JSX)", "Flutter (Dart)",
            "Python (Tkinter)", "Python (PyQt5)", "Swift (iOS)", "Other"
        ], key="_tc_img_lang")
        _tc_img_notes = st.text_input(
            "Any extra notes (optional)",
            placeholder="e.g. 'make it dark mode', 'add animations', 'it should be responsive'",
            key="_tc_img_notes", label_visibility="collapsed"
        )
        if st.button("📸 Generate Code from Image", key="_tc_img_gen", use_container_width=True, type="primary"):
            if _tc_img_file and _tc_api:
                with st.spinner("Titan Code is analyzing your image and generating code..."):
                    try:
                        import base64 as _b64tc
                        _img_bytes = _tc_img_file.read()
                        _img_b64 = _b64tc.b64encode(_img_bytes).decode()
                        _img_mime = "image/png" if _tc_img_file.type == "image/png" else "image/jpeg"
                        from groq import Groq as _TCGV
                        _tc_vlient = _TCGV(api_key=_tc_api)
                        _vision_prompt = (
                            f"Look at this image carefully. It shows a UI/app design.\n"
                            f"Generate complete, working {_tc_img_lang} code that looks EXACTLY like this image.\n"
                            f"Additional notes: {_tc_img_notes.strip() or 'None'}\n\n"
                            "Requirements:\n"
                            "• Match the layout, colors, fonts, spacing as closely as possible\n"
                            "• Make it fully functional, not just a static mockup\n"
                            "• Include all UI elements visible in the image\n"
                            "• Beautiful, production-ready code\n"
                            "• Complete code — no truncation, every line"
                        )
                        _vision_resp = _tc_vlient.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": _vision_prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:{_img_mime};base64,{_img_b64}"}}
                                ]
                            }],
                            max_tokens=8192,
                            temperature=0.15,
                        )
                        st.session_state["_tc_last_output"] = _vision_resp.choices[0].message.content or ""
                    except Exception as _tcve:
                        st.error(f"Error: {_tcve}")
            else:
                st.warning("Upload an image first!")

    # ── Output Display ─────────────────────────────────────────────────────────
    if st.session_state.get("_tc_last_output"):
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:.6rem;color:#f59e0b;letter-spacing:2px;margin-bottom:6px'>OUTPUT</div>", unsafe_allow_html=True)
        st.markdown(st.session_state["_tc_last_output"], unsafe_allow_html=True)
        _dl_c1, _dl_c2 = st.columns(2)
        with _dl_c1:
            st.download_button(
                "⬇️ Download Code",
                data=st.session_state["_tc_last_output"],
                file_name="titan_code_output.md",
                mime="text/markdown",
                use_container_width=True,
                key="_tc_dl"
            )
        with _dl_c2:
            if st.button("🗑️ Clear", key="_tc_clear", use_container_width=True):
                st.session_state["_tc_last_output"] = ""
                st.rerun()

    st.stop()

# ── TITAN FEATURES PAGE ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.get("show_titan_features"):

    st.markdown("""<div style='text-align:center;padding:20px 0 8px'>
    <div style='font-family:Orbitron,monospace;font-size:1.5rem;color:#aaaaaa;
    letter-spacing:4px;font-weight:700'>⚡ TITAN FEATURES</div>
    <div style='color:#6b7a99;font-size:.8rem;margin-top:6px'>
    Supercharge Titan Ultra with powerful add-ons</div></div>""", unsafe_allow_html=True)

    _tf_sel = st.selectbox(
        "Choose a feature:",
        ["🔗 Connect Apps with Titan Ultra", "🌐 Ask About a Website"],
        key="_tf_mode_sel",
    )

    st.markdown("---")

    if "Connect Apps" in _tf_sel:
        st.markdown("""<div style='font-size:.88rem;color:#e8e8e8;font-weight:600;margin-bottom:4px'>
        🔗 Connect Apps with Titan Ultra</div>
        <div style='font-size:.76rem;color:#6b7a99;margin-bottom:12px;line-height:1.75'>
        Select the apps you use. Titan Ultra will remember them and act as your expert guide
        <b>inside</b> each app — features, tips, shortcuts, and personalised help.
        Your selection is saved automatically.</div>""",
        unsafe_allow_html=True)

        # ── Already connected: show logos ─────────────────────────────────────
        _already = st.session_state.get("connected_apps", [])
        if _already:
            _ALL_DOMAINS = {}
            # domain lookup built dynamically from catalog below
            _DOMAIN_MAP = {
                "Facebook":"facebook.com","Instagram":"instagram.com","Twitter / X":"x.com",
                "LinkedIn":"linkedin.com","Snapchat":"snapchat.com","TikTok":"tiktok.com",
                "Pinterest":"pinterest.com","Telegram":"telegram.org","WhatsApp":"whatsapp.com",
                "Discord":"discord.com","Reddit":"reddit.com","Tumblr":"tumblr.com",
                "Threads":"threads.net","Signal":"signal.org","YouTube":"youtube.com",
                "Netflix":"netflix.com","Amazon Prime":"primevideo.com",
                "Disney+ Hotstar":"hotstar.com","Zee5":"zee5.com","SonyLIV":"sonyliv.com",
                "MX Player":"mxplayer.in","JioCinema":"jiocinema.com","HBO Max":"max.com",
                "Apple TV+":"tv.apple.com","Crunchyroll":"crunchyroll.com","Twitch":"twitch.tv",
                "Spotify":"spotify.com","Apple Music":"music.apple.com",
                "Amazon Music":"music.amazon.com","YouTube Music":"music.youtube.com",
                "SoundCloud":"soundcloud.com","Gaana":"gaana.com","JioSaavn":"jiosaavn.com",
                "Wynk Music":"wynk.in","Deezer":"deezer.com","Tidal":"tidal.com",
                "Gmail":"gmail.com","Google Drive":"drive.google.com",
                "Google Calendar":"calendar.google.com","Google Maps":"maps.google.com",
                "Google Docs":"docs.google.com","Google Sheets":"sheets.google.com",
                "Google Slides":"slides.google.com","Google Meet":"meet.google.com",
                "Google Photos":"photos.google.com","Google Pay":"pay.google.com",
                "Google News":"news.google.com","Google Classroom":"classroom.google.com",
                "Outlook":"outlook.com","OneDrive":"onedrive.com",
                "Microsoft Teams":"teams.microsoft.com","Word":"microsoft.com",
                "Excel":"microsoft.com","PowerPoint":"microsoft.com","OneNote":"onenote.com",
                "Xbox":"xbox.com","Bing":"bing.com","Amazon":"amazon.in","Flipkart":"flipkart.com",
                "Meesho":"meesho.com","Myntra":"myntra.com","Ajio":"ajio.com","Nykaa":"nykaa.com",
                "Snapdeal":"snapdeal.com","Tata CLiQ":"tatacliq.com","eBay":"ebay.com",
                "SHEIN":"shein.com","PhonePe":"phonepe.com","Paytm":"paytm.com",
                "CRED":"cred.club","PayPal":"paypal.com","Razorpay":"razorpay.com",
                "Groww":"groww.in","Zerodha":"zerodha.com","Upstox":"upstox.com",
                "MobiKwik":"mobikwik.com","Coin DCX":"coindcx.com","Swiggy":"swiggy.com",
                "Zomato":"zomato.com","BigBasket":"bigbasket.com","Blinkit":"blinkit.com",
                "Zepto":"zepto.app","Dunzo":"dunzo.in","Dominos":"dominos.co.in",
                "Starbucks":"starbucks.com","Uber":"uber.com","Ola":"olacabs.com",
                "Rapido":"rapido.bike","MakeMyTrip":"makemytrip.com","IRCTC":"irctc.co.in",
                "Airbnb":"airbnb.com","Booking.com":"booking.com","RedBus":"redbus.in",
                "IndiGo":"goindigo.in","Yatra":"yatra.com","Notion":"notion.so",
                "Slack":"slack.com","Zoom":"zoom.us","Trello":"trello.com",
                "Todoist":"todoist.com","Evernote":"evernote.com","Dropbox":"dropbox.com",
                "1Password":"1password.com","Asana":"asana.com","Canva":"canva.com",
                "Grammarly":"grammarly.com","Figma":"figma.com","GitHub":"github.com",
                "GitLab":"gitlab.com","Stack Overflow":"stackoverflow.com","Replit":"replit.com",
                "Vercel":"vercel.com","Docker":"docker.com","Postman":"postman.com",
                "Jira":"atlassian.com","VS Code":"code.visualstudio.com","Netlify":"netlify.com",
                "Hugging Face":"huggingface.co","Steam":"steampowered.com",
                "PUBG Mobile":"pubg.com","Free Fire":"ff.garena.com","Roblox":"roblox.com",
                "Minecraft":"minecraft.net","Fortnite":"epicgames.com","COD Mobile":"callofduty.com",
                "Clash of Clans":"supercell.com","Clash Royale":"supercell.com",
                "Among Us":"innersloth.com","Genshin Impact":"genshin.hoyoverse.com",
                "PlayStation":"playstation.com","Epic Games":"epicgames.com",
                "Duolingo":"duolingo.com","Khan Academy":"khanacademy.org","Coursera":"coursera.org",
                "BYJU'S":"byjus.com","Unacademy":"unacademy.com","Vedantu":"vedantu.com",
                "Udemy":"udemy.com","Brainly":"brainly.com","Quizlet":"quizlet.com",
                "Chegg":"chegg.com","Skillshare":"skillshare.com","Google Fit":"fit.google.com",
                "Samsung Health":"samsung.com","Headspace":"headspace.com","Calm":"calm.com",
                "Strava":"strava.com","PharmEasy":"pharmeasy.in","1mg":"1mg.com",
                "Practo":"practo.com","Nike Run Club":"nike.com","MyFitnessPal":"myfitnesspal.com",
                "Inshorts":"inshorts.com","Times of India":"timesofindia.com","NDTV":"ndtv.com",
                "BBC News":"bbc.com","CNN":"cnn.com","The Hindu":"thehindu.com",
                "Flipboard":"flipboard.com","Wikipedia":"wikipedia.org","Feedly":"feedly.com",
                "iCloud":"icloud.com","Box":"box.com","pCloud":"pcloud.com",
                "LastPass":"lastpass.com","Bitwarden":"bitwarden.com","Authy":"authy.com",
                "Proton Mail":"proton.me","Brave":"brave.com","DuckDuckGo":"duckduckgo.com",
            }
            _logo_html = ""
            for _la in _already:
                _ld = _DOMAIN_MAP.get(_la, "google.com")
                _logo_html += (
                    f"<div style='display:inline-flex;flex-direction:column;align-items:center;"
                    f"margin:4px 6px;gap:3px'>"
                    f"<div style='position:relative;width:42px;height:42px;background:#111111;"
                    f"border:2px solid #333333;border-radius:10px;display:flex;"
                    f"align-items:center;justify-content:center'>"
                    f"<img src='https://www.google.com/s2/favicons?domain={_ld}&sz=32' "
                    f"style='width:28px;height:28px;border-radius:6px'>"
                    f"<span style='position:absolute;bottom:-5px;right:-5px;background:#22c55e;"
                    f"border-radius:50%;width:14px;height:14px;display:flex;align-items:center;"
                    f"justify-content:center;font-size:9px'>✓</span>"
                    f"</div>"
                    f"<span style='font-size:.55rem;color:#aaaaaa;max-width:50px;text-align:center;"
                    f"overflow:hidden;white-space:nowrap;text-overflow:ellipsis'>{_la}</span>"
                    f"</div>"
                )
            st.markdown(
                f"<div style='background:#111111;border:1px solid #333333;border-radius:10px;"
                f"padding:10px 12px;margin-bottom:14px'>"
                f"<div style='font-size:.68rem;color:#aaaaaa;font-weight:700;margin-bottom:8px'>"
                f"🔱 + ⚡ Connected to Titan Ultra ({len(_already)})</div>"
                f"<div style='display:flex;flex-wrap:wrap'>{_logo_html}</div></div>",
                unsafe_allow_html=True
            )

        # ── Search bar ────────────────────────────────────────────────────────
        _tf_search = st.text_input(
            "🔍 Search apps",
            placeholder="Search by name (e.g. YouTube, Spotify, GitHub...)",
            key="_tf_app_search",
            label_visibility="collapsed",
        )

        _APPS_CATALOG = {
            "📱 Social Media": [
                ("Facebook",   "facebook.com",   "Posts, groups & messages"),
                ("Instagram",  "instagram.com",  "Photos, reels & DMs"),
                ("Twitter / X","x.com",           "Tweets & trending topics"),
                ("LinkedIn",   "linkedin.com",   "Jobs, posts & networking"),
                ("Snapchat",   "snapchat.com",   "Stories & disappearing messages"),
                ("TikTok",     "tiktok.com",     "Short videos & trends"),
                ("Pinterest",  "pinterest.com",  "Ideas, pins & boards"),
                ("Telegram",   "telegram.org",   "Channels, groups & messages"),
                ("WhatsApp",   "whatsapp.com",   "Chats, calls & groups"),
                ("Discord",    "discord.com",    "Servers, voice & gaming chat"),
                ("Reddit",     "reddit.com",     "Posts, communities & discussions"),
                ("Tumblr",     "tumblr.com",     "Blogs, GIFs & fandom"),
                ("Threads",    "threads.net",    "Short posts by Instagram"),
                ("Signal",     "signal.org",     "Encrypted private messaging"),
            ],
            "📺 Video & Streaming": [
                ("YouTube",         "youtube.com",     "Videos, shorts & live streams"),
                ("Netflix",         "netflix.com",     "Movies & series"),
                ("Amazon Prime",    "primevideo.com",  "Movies & Amazon originals"),
                ("Disney+ Hotstar", "hotstar.com",     "Disney, Marvel, sports & OTT"),
                ("Zee5",            "zee5.com",        "Hindi & regional OTT"),
                ("SonyLIV",         "sonyliv.com",     "Sports, Sony originals & live TV"),
                ("MX Player",       "mxplayer.in",     "Free movies & live TV"),
                ("JioCinema",       "jiocinema.com",   "Free movies, IPL & originals"),
                ("HBO Max",         "max.com",         "HBO originals & blockbusters"),
                ("Apple TV+",       "tv.apple.com",    "Apple originals"),
                ("Crunchyroll",     "crunchyroll.com", "Anime & manga"),
                ("Twitch",          "twitch.tv",       "Live game streaming"),
            ],
            "🎵 Music & Podcasts": [
                ("Spotify",      "spotify.com",       "Music, podcasts & audiobooks"),
                ("Apple Music",  "music.apple.com",   "Songs & playlists"),
                ("Amazon Music", "music.amazon.com",  "Prime music & unlimited"),
                ("YouTube Music","music.youtube.com", "YouTube-powered music"),
                ("SoundCloud",   "soundcloud.com",    "Independent artists & uploads"),
                ("Gaana",        "gaana.com",         "Bollywood & regional music"),
                ("JioSaavn",     "jiosaavn.com",      "Indian music & podcasts"),
                ("Wynk Music",   "wynk.in",           "Airtel music platform"),
                ("Deezer",       "deezer.com",        "Global music streaming"),
                ("Tidal",        "tidal.com",         "Hi-fi audio quality music"),
            ],
            "📧 Google Apps": [
                ("Gmail",            "gmail.com",           "Emails & inbox"),
                ("Google Drive",     "drive.google.com",    "Files, docs & storage"),
                ("Google Calendar",  "calendar.google.com", "Events & schedule"),
                ("Google Maps",      "maps.google.com",     "Navigation & places"),
                ("Google Docs",      "docs.google.com",     "Word processing"),
                ("Google Sheets",    "sheets.google.com",   "Spreadsheets"),
                ("Google Slides",    "slides.google.com",   "Presentations"),
                ("Google Meet",      "meet.google.com",     "Video calls"),
                ("Google Photos",    "photos.google.com",   "Photo backup & albums"),
                ("Google Pay",       "pay.google.com",      "UPI & payments"),
                ("Google News",      "news.google.com",     "Personalised news feed"),
                ("Google Classroom", "classroom.google.com","School & assignments"),
            ],
            "💼 Microsoft": [
                ("Outlook",         "outlook.com",         "Email & calendar"),
                ("OneDrive",        "onedrive.com",        "Cloud file storage"),
                ("Microsoft Teams", "teams.microsoft.com", "Work calls & chat"),
                ("Word",            "microsoft.com",       "Word processing"),
                ("Excel",           "microsoft.com",       "Spreadsheets & data"),
                ("PowerPoint",      "microsoft.com",       "Presentations"),
                ("OneNote",         "onenote.com",         "Notes & notebooks"),
                ("Xbox",            "xbox.com",            "Gaming & Game Pass"),
                ("Bing",            "bing.com",            "Microsoft search engine"),
            ],
            "🛍️ Shopping": [
                ("Amazon",    "amazon.in",    "Online shopping & delivery"),
                ("Flipkart",  "flipkart.com", "Electronics, fashion & more"),
                ("Meesho",    "meesho.com",   "Budget & reseller shopping"),
                ("Myntra",    "myntra.com",   "Fashion & clothing"),
                ("Ajio",      "ajio.com",     "Reliance fashion store"),
                ("Nykaa",     "nykaa.com",    "Beauty & cosmetics"),
                ("Snapdeal",  "snapdeal.com", "Deals & discounts"),
                ("Tata CLiQ", "tatacliq.com", "Tata shopping platform"),
                ("eBay",      "ebay.com",     "Global buy & sell marketplace"),
                ("SHEIN",     "shein.com",    "Trendy affordable fashion"),
            ],
            "💳 Finance & Payments": [
                ("PhonePe",  "phonepe.com",  "UPI payments & insurance"),
                ("Paytm",    "paytm.com",    "Wallet, UPI & bill pay"),
                ("CRED",     "cred.club",    "Credit card rewards & payments"),
                ("PayPal",   "paypal.com",   "International payments"),
                ("Razorpay", "razorpay.com", "Business payments gateway"),
                ("Groww",    "groww.in",     "Mutual funds & stocks"),
                ("Zerodha",  "zerodha.com",  "Stock trading & investing"),
                ("Upstox",   "upstox.com",   "Stock market investing"),
                ("MobiKwik", "mobikwik.com", "Wallet & Buy Now Pay Later"),
                ("Coin DCX", "coindcx.com",  "Cryptocurrency trading"),
            ],
            "🍔 Food & Delivery": [
                ("Swiggy",    "swiggy.com",    "Food delivery & Instamart"),
                ("Zomato",    "zomato.com",    "Food delivery & dining out"),
                ("BigBasket", "bigbasket.com", "Grocery home delivery"),
                ("Blinkit",   "blinkit.com",   "10-minute grocery delivery"),
                ("Zepto",     "zepto.app",     "Quick commerce delivery"),
                ("Dunzo",     "dunzo.in",      "Delivery & daily errands"),
                ("Dominos",   "dominos.co.in", "Pizza delivery"),
                ("Starbucks", "starbucks.com", "Coffee ordering & rewards"),
            ],
            "✈️ Travel & Transport": [
                ("Uber",        "uber.com",       "Cab booking"),
                ("Ola",         "olacabs.com",    "Cab, auto & rentals"),
                ("Rapido",      "rapido.bike",    "Bike taxi & auto"),
                ("MakeMyTrip",  "makemytrip.com", "Flights & hotels"),
                ("IRCTC",       "irctc.co.in",    "Train tickets"),
                ("Airbnb",      "airbnb.com",     "Unique stays worldwide"),
                ("Booking.com", "booking.com",    "Hotel & accommodation"),
                ("RedBus",      "redbus.in",      "Bus ticket booking"),
                ("IndiGo",      "goindigo.in",    "Airline booking"),
                ("Yatra",       "yatra.com",      "Flights, hotels & buses"),
            ],
            "🧠 Productivity": [
                ("Notion",     "notion.so",      "Notes, wikis & databases"),
                ("Slack",      "slack.com",      "Team messaging & files"),
                ("Zoom",       "zoom.us",        "Video meetings & webinars"),
                ("Trello",     "trello.com",     "Boards & project tracking"),
                ("Todoist",    "todoist.com",    "Task manager & to-do lists"),
                ("Evernote",   "evernote.com",   "Notes & web clipping"),
                ("Dropbox",    "dropbox.com",    "File sync & sharing"),
                ("1Password",  "1password.com",  "Password manager"),
                ("Asana",      "asana.com",      "Team project management"),
                ("Canva",      "canva.com",      "Design & presentations"),
                ("Grammarly",  "grammarly.com",  "Writing & grammar assistant"),
                ("Figma",      "figma.com",      "UI/UX design tool"),
            ],
            "👨‍💻 Development": [
                ("GitHub",         "github.com",          "Code repos, PRs & issues"),
                ("GitLab",         "gitlab.com",          "DevOps & CI/CD pipelines"),
                ("Stack Overflow", "stackoverflow.com",   "Programming Q&A community"),
                ("Replit",         "replit.com",          "Online coding IDE"),
                ("Vercel",         "vercel.com",          "Deploy web apps fast"),
                ("Docker",         "docker.com",          "App containerisation"),
                ("Postman",        "postman.com",         "API testing & docs"),
                ("Jira",           "atlassian.com",       "Issue & sprint tracking"),
                ("VS Code",        "code.visualstudio.com","Popular code editor"),
                ("Netlify",        "netlify.com",         "Frontend deployment"),
                ("Hugging Face",   "huggingface.co",      "AI models & datasets"),
            ],
            "🎮 Gaming": [
                ("Steam",         "steampowered.com",     "PC gaming store"),
                ("PUBG Mobile",   "pubg.com",             "Battle royale mobile"),
                ("Free Fire",     "ff.garena.com",        "Mobile battle royale"),
                ("Roblox",        "roblox.com",           "User-created games platform"),
                ("Minecraft",     "minecraft.net",        "Block-building survival"),
                ("Fortnite",      "epicgames.com",        "Battle royale & creative"),
                ("COD Mobile",    "callofduty.com",       "Call of Duty mobile"),
                ("Clash of Clans","supercell.com",        "Strategy & base building"),
                ("Clash Royale",  "supercell.com",        "Card battle arena"),
                ("Among Us",      "innersloth.com",       "Social deduction game"),
                ("Genshin Impact","genshin.hoyoverse.com","Open-world RPG"),
                ("PlayStation",   "playstation.com",      "Console gaming platform"),
                ("Epic Games",    "epicgames.com",        "PC game store & launcher"),
            ],
            "📚 Education": [
                ("Duolingo",    "duolingo.com",     "Language learning & streaks"),
                ("Khan Academy","khanacademy.org",  "Free courses & practice"),
                ("Coursera",    "coursera.org",     "University courses online"),
                ("BYJU'S",      "byjus.com",        "India's top learning app"),
                ("Unacademy",   "unacademy.com",    "Competitive exam prep"),
                ("Vedantu",     "vedantu.com",      "Live online tutoring"),
                ("Udemy",       "udemy.com",        "Courses in any skill"),
                ("Brainly",     "brainly.com",      "Student Q&A community"),
                ("Quizlet",     "quizlet.com",      "Flashcards & study sets"),
                ("Chegg",       "chegg.com",        "Homework help & textbooks"),
                ("Skillshare",  "skillshare.com",   "Creative skills & projects"),
            ],
            "🏃 Health & Fitness": [
                ("Google Fit",     "fit.google.com",   "Activity tracking & goals"),
                ("Samsung Health", "samsung.com",       "Wellness tracking"),
                ("Headspace",      "headspace.com",     "Meditation & sleep"),
                ("Calm",           "calm.com",          "Relaxation & mindfulness"),
                ("Strava",         "strava.com",        "Running & cycling tracking"),
                ("PharmEasy",      "pharmeasy.in",      "Medicine delivery"),
                ("1mg",            "1mg.com",           "Health & medicine delivery"),
                ("Practo",         "practo.com",        "Doctor appointments online"),
                ("Nike Run Club",  "nike.com",          "Running app & coaching"),
                ("MyFitnessPal",   "myfitnesspal.com",  "Calorie & nutrition tracker"),
            ],
            "📰 News & Info": [
                ("Inshorts",       "inshorts.com",     "60-word news summaries"),
                ("Times of India", "timesofindia.com", "India's top newspaper"),
                ("NDTV",           "ndtv.com",         "Breaking news & live TV"),
                ("BBC News",       "bbc.com",          "World & UK news"),
                ("CNN",            "cnn.com",          "US & world news"),
                ("The Hindu",      "thehindu.com",     "Quality Indian journalism"),
                ("Flipboard",      "flipboard.com",    "Magazine-style news feed"),
                ("Wikipedia",      "wikipedia.org",    "Free online encyclopedia"),
                ("Feedly",         "feedly.com",       "RSS & newsletter reader"),
            ],
            "☁️ Cloud & Other": [
                ("iCloud",     "icloud.com",     "Apple cloud storage & sync"),
                ("Box",        "box.com",        "Business file storage"),
                ("pCloud",     "pcloud.com",     "Secure lifetime cloud storage"),
                ("LastPass",   "lastpass.com",   "Password vault"),
                ("Bitwarden",  "bitwarden.com",  "Open-source password manager"),
                ("Authy",      "authy.com",      "Two-factor authentication app"),
                ("Proton Mail","proton.me",      "Encrypted private email"),
                ("Brave",      "brave.com",      "Privacy-first web browser"),
                ("DuckDuckGo", "duckduckgo.com", "Private search engine"),
            ],
        }
        _cur_apps = set(st.session_state.get("connected_apps", []))
        _new_sel = []
        _gidx = 0
        _tf_q = st.session_state.get("_tf_app_search", "").lower().strip()
        _any_shown = False
        for _cat, _cat_apps in _APPS_CATALOG.items():
            _filtered = [(_cn,_cd,_cdesc) for _cn,_cd,_cdesc in _cat_apps
                        if not _tf_q or _tf_q in _cn.lower()]
            if not _filtered:
                continue
            _any_shown = True
            st.markdown(
                f"<div style='font-size:.78rem;color:#aaaaaa;font-weight:700;"
                f"letter-spacing:1px;margin:16px 0 6px'>{_cat}</div>",
                unsafe_allow_html=True
            )
            _gcols = st.columns(4)
            for _ci, (_cn, _cd, _cdesc) in enumerate(_filtered):
                with _gcols[_ci % 4]:
                    st.markdown(
                        f"<img src='https://www.google.com/s2/favicons?domain={_cd}&sz=24' "
                        f"style='width:20px;height:20px;border-radius:4px;margin-bottom:1px'>",
                        unsafe_allow_html=True
                    )
                    if st.checkbox(
                        _cn, value=_cn in _cur_apps,
                        key=f"_tf_cb_{_gidx}", help=_cdesc,
                    ):
                        _new_sel.append(_cn)
                _gidx += 1
        if _tf_q and not _any_shown:
            st.caption(f"No apps found for '{_tf_q}'")

        st.markdown("---")
        _sav1, _sav2 = st.columns([3, 2])
        _sel_txt = f"{len(_new_sel)} app(s) selected" if _new_sel else "None selected"
        _sav1.markdown(f"<div style='font-size:.74rem;color:#6b7a99;padding-top:10px'>"
                      f"{'✅ ' if _new_sel else ''}{_sel_txt}</div>", unsafe_allow_html=True)
        if _sav2.button("💾 Save & Go to Chat", type="primary",
                        use_container_width=True, key="_tf_save_btn"):
            st.session_state.connected_apps = _new_sel
            _save_connected_apps(_new_sel)
            st.session_state.show_titan_features = False
            st.rerun()

    elif "Ask About a Website" in _tf_sel:
        st.markdown("""<div style='font-size:.88rem;color:#e8e8e8;font-weight:600;margin-bottom:4px'>
        🌐 Ask About a Website</div>
        <div style='font-size:.76rem;color:#6b7a99;margin-bottom:16px;line-height:1.75'>
        Paste any website URL below. Titan Ultra will read the page and answer
        any question you have about it — prices, info, summaries, anything!</div>""",
        unsafe_allow_html=True)

        def _tf_web_ask(q, content, url):
            from groq import Groq as _Gw
            _cw = _Gw(api_key=st.session_state.api_key)
            _sys_w = (
                "You are Titan Ultra. The user has shared a website with you and asked a question. "
                "Answer clearly, helpfully, and in simple words based on the website content. "
                "Be enthusiastic and encouraging!"
            )
            _msg_w = (f"{q}\n\n[WEBSITE: {url}]\n\n{content[:5500]}\n\n"
                      f"Answer from the above website content.")
            for _mdl in ["openai/gpt-oss-120b","openai/gpt-oss-20b","qwen/qwen3.8-27b"]:
                try:
                    _r = _cw.chat.completions.create(
                        model=_mdl,
                        messages=[{"role":"system","content":_sys_w},
                                  {"role":"user","content":_msg_w}],
                        max_tokens=2048, temperature=0.4,
                    )
                    return _r.choices[0].message.content or ""
                except Exception:
                    continue
            return "Sorry, could not get an answer. Please try again."

        _url_inp = st.text_input(
            "Website URL:", placeholder="https://example.com or paste any link here",
            key="_tf_url_inp", label_visibility="visible"
        )
        _load_col, _clear_col = st.columns([3, 1])
        if _load_col.button("🔍 Load & Read Website", key="_tf_url_load", use_container_width=True):
            if _url_inp.strip():
                with st.spinner("🌐 Reading website..."):
                    try:
                        import requests as _rqw
                        from bs4 import BeautifulSoup as _BSw
                        _rw = _rqw.get(
                            _url_inp.strip(), timeout=12,
                            headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                        )
                        _sw = _BSw(_rw.text, "html.parser")
                        for _tw in _sw(["script","style","nav","footer","head","iframe"]):
                            _tw.decompose()
                        _txt_w = _sw.get_text(separator="\n", strip=True)[:7000]
                        st.session_state["_tf_web_url"]     = _url_inp.strip()
                        st.session_state["_tf_web_content"] = _txt_w
                        st.session_state["_tf_web_chat"]    = []
                        st.rerun()
                    except Exception as _ew:
                        st.error(f"Could not load website: {_ew}")
            else:
                st.warning("Paste a URL first")
        if _clear_col.button("🗑 Clear", key="_tf_web_clear", use_container_width=True):
            st.session_state.pop("_tf_web_url", None)
            st.session_state.pop("_tf_web_content", None)
            st.session_state.pop("_tf_web_chat", None)
            st.rerun()

        if st.session_state.get("_tf_web_content"):
            _wurl = st.session_state["_tf_web_url"]
            st.markdown(
                f"<div style='background:#0a1a0a;border:1px solid #22c55e;border-radius:8px;"
                f"padding:8px 12px;font-size:.72rem;color:#4ade80;margin:10px 0'>"
                f"✅ Loaded: <b>{_wurl[:70]}</b></div>",
                unsafe_allow_html=True
            )
            with st.expander("📄 Preview page content", expanded=False):
                st.text(st.session_state["_tf_web_content"][:800] + "…")

            _wc_hist = st.session_state.get("_tf_web_chat", [])
            for _wm in _wc_hist:
                with st.chat_message(_wm["role"]):
                    st.markdown(_wm["content"])

            _web_q = st.chat_input("Ask anything about this website...", key="_tf_web_ci")
            if _web_q:
                _wc_hist.append({"role":"user","content":_web_q})
                st.session_state["_tf_web_chat"] = _wc_hist
                with st.chat_message("user"):
                    st.markdown(_web_q)
                with st.chat_message("assistant"):
                    with st.spinner("Titan Ultra is reading..."):
                        _w_ans = _tf_web_ask(
                            _web_q,
                            st.session_state["_tf_web_content"],
                            _wurl
                        )
                    st.markdown(_w_ans)
                _wc_hist.append({"role":"assistant","content":_w_ans})
                st.session_state["_tf_web_chat"] = _wc_hist
                st.rerun()

    st.stop()

# ── Always parse flashcards from latest AI response ───────────────────────────
if True:
    # ── Parse FRONT:/BACK: lines from latest AI response ─────────────────────
    _fc_last_ai = ""
    for _m in cur_msgs():
        if _m["role"] == "assistant":
            _fc_last_ai = _m["content"]

    if _fc_last_ai and "FRONT:" in _fc_last_ai.upper():
        _fc_parsed = []
        _fc_lines = _fc_last_ai.strip().split('\n')
        _fi2 = 0
        while _fi2 < len(_fc_lines):
            _l = _fc_lines[_fi2].strip()
            if _l.upper().startswith('FRONT:'):
                _front_txt = _l[6:].strip()
                if _fi2 + 1 < len(_fc_lines) and _fc_lines[_fi2+1].strip().upper().startswith('BACK:'):
                    _back_txt = _fc_lines[_fi2+1].strip()[5:].strip()
                    _fc_parsed.append({"front": _front_txt, "back": _back_txt})
                    _fi2 += 2
                    continue
            _fi2 += 1
        if _fc_parsed and _fc_parsed != st.session_state.flashcards:
            st.session_state.flashcards = _fc_parsed
            st.session_state.card_index = 0
            st.session_state.card_flipped = False
            st.session_state.card_known = set()
            st.session_state.card_review = set()
            st.session_state.fc_review_mode = False
            st.session_state.fc_study_all = False

    # ── Flashcard viewer (shown automatically when cards are generated) ──────
    if st.session_state.flashcards:
        import html as _html
        _fc_all = st.session_state.flashcards

        # Build current deck (all cards OR review-only)
        if st.session_state.fc_review_mode:
            _deck_idx = [i for i in range(len(_fc_all)) if i in st.session_state.card_review]
            if not _deck_idx:
                st.session_state.fc_review_mode = False
                _deck_idx = list(range(len(_fc_all)))
        else:
            _deck_idx = list(range(len(_fc_all)))

        _fc_n = len(_deck_idx)
        _pos = max(0, min(st.session_state.card_index, _fc_n - 1))
        st.session_state.card_index = _pos
        _orig_i = _deck_idx[_pos]
        _card = _fc_all[_orig_i]
        _flipped = st.session_state.card_flipped
        _n_known = len(st.session_state.card_known)
        _n_rev   = len(st.session_state.card_review)

        # Stats bar
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
             padding:8px 16px;background:rgba(255,255,255,0.04);
             border-radius:10px;margin-bottom:12px;'>
          <span style='color:rgba(255,255,255,0.45);font-size:12px;'>
            Card <b style='color:#e8e8e8'>{_pos+1}</b> / {_fc_n}
          </span>
          <span>
            <span style='color:#a6e3a1;font-size:12px;font-weight:700;'>✓ Known: {_n_known}</span>
            &nbsp;&nbsp;
            <span style='color:#f38ba8;font-size:12px;font-weight:700;'>↺ Review: {_n_rev}</span>
          </span>
        </div>""", unsafe_allow_html=True)

        # Card face
        _front_safe = _html.escape(_card["front"])
        _back_safe  = _html.escape(_card["back"])
        if not _flipped:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#1a0f44,#0f1a2c);
                 border:2px solid rgba(168,85,247,0.55);border-radius:20px;
                 padding:40px 28px;text-align:center;min-height:160px;
                 box-shadow:0 8px 32px rgba(168,85,247,0.18);margin-bottom:14px;'>
              <p style='color:rgba(255,255,255,0.4);font-size:10px;font-weight:700;
                   letter-spacing:2.5px;margin:0 0 16px 0;'>QUESTION</p>
              <p style='color:#e0d0ff;font-size:1.15rem;font-weight:600;
                   margin:0;line-height:1.55;'>{_front_safe}</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#0a2d1a,#0a1f14);
                 border:2px solid rgba(52,211,153,0.6);border-radius:20px;
                 padding:40px 28px;text-align:center;min-height:160px;
                 box-shadow:0 8px 32px rgba(52,211,153,0.18);margin-bottom:14px;'>
              <p style='color:rgba(52,211,153,0.65);font-size:10px;font-weight:700;
                   letter-spacing:2.5px;margin:0 0 16px 0;'>ANSWER</p>
              <p style='color:#a6e3a1;font-size:1.1rem;font-weight:500;
                   margin:0;line-height:1.55;'>{_back_safe}</p>
            </div>""", unsafe_allow_html=True)

        # Flip button (centered)
        _fl1, _fl2, _fl3 = st.columns([1,2,1])
        with _fl2:
            _flip_lbl = "↺ Review Again" if _flipped else "Flip to Answer ▶"
            if st.button(_flip_lbl, use_container_width=True, key="fc_flip"):
                st.session_state.card_flipped = not _flipped
                st.rerun()

        # Prev / Known / Review / Next
        _bn1, _bn2, _bn3, _bn4 = st.columns(4)
        with _bn1:
            if st.button("◀ Prev", use_container_width=True, key="fc_prev",
                         disabled=(_pos == 0)):
                st.session_state.card_index = _pos - 1
                st.session_state.card_flipped = False
                st.rerun()
        with _bn2:
            _is_k = _orig_i in st.session_state.card_known
            if st.button("✓ Known" + (" ✓" if _is_k else ""), use_container_width=True, key="fc_known"):
                if _is_k:
                    st.session_state.card_known.discard(_orig_i)
                else:
                    st.session_state.card_known.add(_orig_i)
                    st.session_state.card_review.discard(_orig_i)
                st.rerun()
        with _bn3:
            _is_r = _orig_i in st.session_state.card_review
            if st.button("↺ Review" + (" ✓" if _is_r else ""), use_container_width=True, key="fc_rev"):
                if _is_r:
                    st.session_state.card_review.discard(_orig_i)
                else:
                    st.session_state.card_review.add(_orig_i)
                    st.session_state.card_known.discard(_orig_i)
                st.rerun()
        with _bn4:
            if st.button("Next ▶", use_container_width=True, key="fc_next",
                         disabled=(_pos >= _fc_n - 1)):
                st.session_state.card_index = _pos + 1
                st.session_state.card_flipped = False
                st.rerun()

        # Mode buttons: All Cards | Review Mode | Study All
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        _mb1, _mb2, _mb3 = st.columns(3)
        with _mb1:
            if st.button(f"All Cards ({len(_fc_all)})", use_container_width=True,
                         key="fc_all_btn", disabled=not st.session_state.fc_review_mode):
                st.session_state.fc_review_mode = False
                st.session_state.card_index = 0
                st.session_state.card_flipped = False
                st.rerun()
        with _mb2:
            _rl = len(st.session_state.card_review)
            if st.button(f"🔁 Review Mode ({_rl})", use_container_width=True,
                         key="fc_rev_btn",
                         disabled=(st.session_state.fc_review_mode or _rl == 0)):
                st.session_state.fc_review_mode = True
                st.session_state.card_index = 0
                st.session_state.card_flipped = False
                st.rerun()
        with _mb3:
            _sa = st.session_state.get("fc_study_all", False)
            if st.button("📖 Study All Cards" if not _sa else "📖 Hide List",
                         use_container_width=True, key="fc_study_btn"):
                st.session_state.fc_study_all = not _sa
                st.rerun()

        # Study All list
        if st.session_state.get("fc_study_all", False):
            st.markdown("<hr>", unsafe_allow_html=True)
            for _sai, _sac in enumerate(_fc_all):
                _k_m = " ✓" if _sai in st.session_state.card_known else ""
                _r_m = " ↺" if _sai in st.session_state.card_review else ""
                _f_s = _html.escape(_sac["front"])
                _b_s = _html.escape(_sac["back"])
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);
                     border-radius:10px;padding:12px 16px;margin-bottom:8px;'>
                  <span style='color:rgba(255,255,255,0.35);font-size:10px;'>
                    Card {_sai+1}{_k_m}{_r_m}</span><br>
                  <b style='color:#e0d0ff;'>Q: {_f_s}</b><br>
                  <span style='color:#a6e3a1;font-size:.9rem;'>A: {_b_s}</span>
                </div>""", unsafe_allow_html=True)

# ── Live Weather fetch: runs when user asks weather in chat ───────────────────
_auto_wq = st.session_state.pop("weather_query", "")
if _auto_wq:
    try:
        import urllib.parse as _urlp2
        _awq = _auto_wq.strip()
        _ALIAS2 = {"bangalore":"Bengaluru","bombay":"Mumbai","calcutta":"Kolkata",
                   "madras":"Chennai","poona":"Pune","baroda":"Vadodara",
                   "mysore":"Mysuru","mangalore":"Mangaluru","trivandrum":"Thiruvananthapuram",
                   "allahabad":"Prayagraj","benares":"Varanasi","cochin":"Kochi"}
        _awq_resolved = _ALIAS2.get(_awq.lower(), _awq)
        _wurl2 = f"https://wttr.in/{_urlp2.quote(_awq_resolved + ', India')}?format=j1"
        _wgeo2 = requests.get(_wurl2, timeout=12, headers={"User-Agent":"Mozilla/5.0"}).json()
        if "nearest_area" in _wgeo2:
            _area2  = _wgeo2["nearest_area"][0]
            _wlat2  = float(_area2["latitude"])
            _wlon2  = float(_area2["longitude"])
            _wname2 = ", ".join(filter(None,[
                _area2["areaName"][0]["value"],
                _area2.get("region",[{"value":""}])[0]["value"],
                _area2["country"][0]["value"],
            ]))
            _om2 = requests.get(
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={_wlat2}&longitude={_wlon2}"
                f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
                f"weathercode,wind_speed_10m,wind_direction_10m,windgusts_10m,"
                f"cloud_cover,visibility,dewpoint_2m,is_day"
                f"&daily=temperature_2m_max,temperature_2m_min,weathercode,"
                f"precipitation_probability_max,uv_index_max,sunrise,sunset"
                f"&timezone=Asia%2FKolkata&forecast_days=7&models=best_match",
                timeout=10).json()
            try:
                _aqd2 = requests.get(
                    f"https://air-quality-api.open-meteo.com/v1/air-quality"
                    f"?latitude={_wlat2}&longitude={_wlon2}&current=european_aqi,pm10,pm2_5",
                    timeout=8).json()
            except Exception:
                _aqd2 = {}
            st.session_state.weather_name = _wname2
            st.session_state.weather_data = _om2
            st.session_state.weather_aqi  = _aqd2
    except Exception:
        pass

# ── Live Weather UI (hidden from home — ask in chat: "weather in [city]") ──────
if False and st.expander("🌤️ Live Weather Search", expanded=bool(st.session_state.weather_data)):
    # ── Live Weather ──────────────────────────────────────────────────────────

    def _wmo_info(code):
        _WMO = {
            0:("☀️","Clear Sky"), 1:("🌤️","Mainly Clear"), 2:("⛅","Partly Cloudy"),
            3:("☁️","Overcast"), 45:("🌫️","Fog"), 48:("🌫️","Icy Fog"),
            51:("🌦️","Light Drizzle"), 53:("🌦️","Drizzle"), 55:("🌧️","Heavy Drizzle"),
            61:("🌧️","Light Rain"), 63:("🌧️","Moderate Rain"), 65:("🌧️","Heavy Rain"),
            71:("🌨️","Light Snow"), 73:("🌨️","Snow"), 75:("❄️","Heavy Snow"),
            77:("🌨️","Snow Grains"), 80:("🌦️","Light Showers"), 81:("🌧️","Showers"),
            82:("⛈️","Heavy Showers"), 85:("🌨️","Snow Showers"), 86:("❄️","Heavy Snow Showers"),
            95:("⛈️","Thunderstorm"), 96:("⛈️","Thunderstorm + Hail"), 99:("⛈️","Heavy Thunderstorm"),
        }
        return _WMO.get(int(code) if code else 0, ("🌡️","Unknown"))

    def _moon_phase(date):
        import datetime as _dt2
        _known_new = _dt2.date(2000, 1, 6)
        _diff = (date - _known_new).days % 29.5
        if _diff < 1.85:   return "🌑","New Moon"
        elif _diff < 7.38: return "🌒","Waxing Crescent"
        elif _diff < 9.22: return "🌓","First Quarter"
        elif _diff < 14.75:return "🌔","Waxing Gibbous"
        elif _diff < 16.61:return "🌕","Full Moon"
        elif _diff < 22.15:return "🌖","Waning Gibbous"
        elif _diff < 23.99:return "🌗","Last Quarter"
        else:               return "🌘","Waning Crescent"

    def _wind_dir(deg):
        _dirs = ["N","NE","E","SE","S","SW","W","NW"]
        return _dirs[int(round(deg/45)) % 8]

    def _aqi_info(val):
        if val <= 20:   return "#22c55e","Good"
        elif val <= 40: return "#84cc16","Fair"
        elif val <= 60: return "#eab308","Moderate"
        elif val <= 80: return "#f97316","Poor"
        elif val <= 100:return "#ef4444","Very Poor"
        else:           return "#7c3aed","Extremely Poor"

    # ── State + City selector ─────────────────────────────────────────────────
    _INDIA_STATE_LIST = [
        "-- Select a State --",
        "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
        "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
        "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
        "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
        "Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
        "— Union Territories —",
        "Andaman & Nicobar Islands","Chandigarh","Dadra & Nagar Haveli",
        "Daman & Diu","Delhi","Jammu & Kashmir","Ladakh","Lakshadweep","Puducherry",
    ]
    _ws1, _ws2 = st.columns(2)
    with _ws1:
        st.markdown("<div style='font-size:.72rem;color:#6b7a99;margin-bottom:4px'>📍 STATE</div>",
                    unsafe_allow_html=True)
        _sel_state = st.selectbox("State", _INDIA_STATE_LIST, label_visibility="collapsed",
                                  key="weather_state_sel")
        if _sel_state.startswith("--") or _sel_state.startswith("—"):
            _sel_state = ""
    with _ws2:
        st.markdown("<div style='font-size:.72rem;color:#6b7a99;margin-bottom:4px'>🏙️ CITY</div>",
                    unsafe_allow_html=True)
        _ph = f"City in {_sel_state}..." if _sel_state else "e.g. Mumbai, Jaipur..."
        _city_in = st.text_input("City", placeholder=_ph, label_visibility="collapsed",
                                  key="weather_city_field")

    _wsearch = st.button("🔍 Get Weather", use_container_width=True, key="weather_search_btn")

    # Accept city from chat input (redirected below) or quick_q
    _wq_city = st.session_state.pop("weather_query","")
    if _wq_city:
        _city_in = _wq_city
        _wsearch = True

    # If only state selected (no city), use state capital
    if _wsearch and not str(_city_in).strip() and _sel_state:
        _city_in = _sel_state

    if _wsearch and str(_city_in).strip():
        with st.spinner("🌤️ Fetching live weather..."):
            try:
                import urllib.parse as _urlp
                _city_q = _city_in.strip()
                _city_lower = _city_q.lower()
                _STATES_MAP = {
                    "andhra pradesh":"Vijayawada","arunachal pradesh":"Itanagar",
                    "assam":"Guwahati","bihar":"Patna","chhattisgarh":"Raipur",
                    "goa":"Panaji","gujarat":"Ahmedabad","haryana":"Chandigarh",
                    "himachal pradesh":"Shimla","jharkhand":"Ranchi",
                    "karnataka":"Bengaluru","kerala":"Thiruvananthapuram",
                    "madhya pradesh":"Bhopal","maharashtra":"Mumbai",
                    "manipur":"Imphal","meghalaya":"Shillong","mizoram":"Aizawl",
                    "nagaland":"Kohima","odisha":"Bhubaneswar","orissa":"Bhubaneswar",
                    "punjab":"Chandigarh","rajasthan":"Jaipur","sikkim":"Gangtok",
                    "tamil nadu":"Chennai","telangana":"Hyderabad","tripura":"Agartala",
                    "uttar pradesh":"Lucknow","uttarakhand":"Dehradun","west bengal":"Kolkata",
                    "delhi":"New Delhi","jammu and kashmir":"Srinagar",
                    "jammu & kashmir":"Srinagar","ladakh":"Leh","puducherry":"Puducherry",
                    "chandigarh":"Chandigarh","andaman & nicobar islands":"Port Blair",
                    "andaman and nicobar":"Port Blair","lakshadweep":"Kavaratti",
                    "dadra & nagar haveli":"Daman","daman and diu":"Daman","daman & diu":"Daman",
                }
                _ALIASES = {
                    "bangalore":"Bengaluru","bombay":"Mumbai","calcutta":"Kolkata",
                    "madras":"Chennai","poona":"Pune","baroda":"Vadodara",
                    "mysore":"Mysuru","mangalore":"Mangaluru","trivandrum":"Thiruvananthapuram",
                    "allahabad":"Prayagraj","benares":"Varanasi","cochin":"Kochi",
                    "calicut":"Kozhikode","ooty":"Ooty",
                }
                _cap = _STATES_MAP.get(_city_lower)
                _ali = _ALIASES.get(_city_lower)
                if _cap:
                    _wttr_q = f"{_cap}, India"
                    _display_prefix = f"{_city_q.title()} — "
                elif _ali:
                    _wttr_q = f"{_ali}, India"
                    _display_prefix = ""
                elif _sel_state:
                    _wttr_q = f"{_city_q}, {_sel_state}, India"
                    _display_prefix = ""
                else:
                    _wttr_q = f"{_city_q}, India"
                    _display_prefix = ""

                # Step 1 — wttr.in: just for resolving Indian city → lat/lon
                _wurl = f"https://wttr.in/{_urlp.quote(_wttr_q)}?format=j1"
                _wgeo = requests.get(_wurl, timeout=12,
                                     headers={"User-Agent":"Mozilla/5.0"}).json()
                if "nearest_area" not in _wgeo:
                    st.error(f"❌ '{_city_in}' not found. Try a different spelling.")
                else:
                    _area = _wgeo["nearest_area"][0]
                    _wlat = float(_area["latitude"])
                    _wlon = float(_area["longitude"])
                    _wname = _display_prefix + ", ".join(filter(None,[
                        _area["areaName"][0]["value"],
                        _area.get("region",[{"value":""}])[0]["value"],
                        _area["country"][0]["value"],
                    ]))

                    # Step 2 — Open-Meteo: accurate real-time weather (closest to Google)
                    _om = requests.get(
                        f"https://api.open-meteo.com/v1/forecast"
                        f"?latitude={_wlat}&longitude={_wlon}"
                        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
                        f"weathercode,wind_speed_10m,wind_direction_10m,windgusts_10m,"
                        f"cloud_cover,visibility,dewpoint_2m,is_day"
                        f"&hourly=temperature_2m,weathercode,precipitation_probability,"
                        f"windspeed_10m,relativehumidity_2m"
                        f"&daily=temperature_2m_max,temperature_2m_min,weathercode,"
                        f"precipitation_probability_max,uv_index_max,sunrise,sunset,"
                        f"windgusts_10m_max"
                        f"&timezone=Asia%2FKolkata&forecast_days=7"
                        f"&models=best_match&cell_selection=nearest",
                        timeout=10).json()

                    # Step 3 — AQI
                    try:
                        _aqd = requests.get(
                            f"https://air-quality-api.open-meteo.com/v1/air-quality"
                            f"?latitude={_wlat}&longitude={_wlon}"
                            f"&current=european_aqi,pm10,pm2_5",
                            timeout=8).json()
                    except Exception:
                        _aqd = {}

                    st.session_state.weather_name    = _wname
                    st.session_state.weather_data    = _om
                    st.session_state.weather_aqi     = _aqd
                    st.session_state.weather_summary = ""
                    st.rerun()
            except Exception as _we:
                st.error(f"❌ Could not fetch weather for '{_city_in}'. Try a different spelling.")

    # ── Render weather card ───────────────────────────────────────────────────
    if st.session_state.weather_data:
        import datetime as _dt, html as _whtml
        _wd   = st.session_state.weather_data
        _cu   = _wd["current"]
        _hr   = _wd["hourly"]
        _dy   = _wd["daily"]
        _aqcu = (st.session_state.weather_aqi or {}).get("current", {})

        _temp   = round(_cu["temperature_2m"])
        _feels  = round(_cu["apparent_temperature"])
        _hum    = _cu["relative_humidity_2m"]
        _wspd   = round(_cu["wind_speed_10m"])
        _wdir   = _wind_dir(_cu.get("wind_direction_10m", 0))
        _gusts  = round(_cu.get("windgusts_10m", 0))
        _code   = int(_cu["weathercode"])
        _is_day = _cu.get("is_day", 1)
        _cloud  = _cu.get("cloud_cover", 0)
        _vis    = round(_cu.get("visibility", 0) / 1000, 1)
        _dew    = round(_cu.get("dewpoint_2m", 0))
        _uv     = round(_dy["uv_index_max"][0], 1)
        _rainc  = _dy["precipitation_probability_max"][0]
        _sr     = str(_dy["sunrise"][0]).split("T")[-1][:5]
        _ss     = str(_dy["sunset"][0]).split("T")[-1][:5]
        _aqi_v  = int(_aqcu.get("european_aqi", 0))
        _aqi_col, _aqi_lbl = _aqi_info(_aqi_v)
        _moon_e, _moon_n   = _moon_phase(_dt.date.today())
        _wemoji, _wdesc    = _wmo_info(_code)

        _grad = ("linear-gradient(135deg,#0a0a1a,#0d0d2b,#1a1a3a)" if not _is_day
                 else "linear-gradient(135deg,#0d3a5c,#1a5276,#0d2845)" if _code <= 1
                 else "linear-gradient(135deg,#1c2833,#2c3e50,#1a252f)" if _code <= 3
                 else "linear-gradient(135deg,#1a1a2e,#16213e,#0f3460)")

        # Main card
        st.markdown(f"""
        <div style='background:{_grad};border-radius:20px;padding:28px 24px;
             margin-bottom:14px;border:1px solid rgba(255,255,255,0.12);'>
          <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
            <div>
              <p style='color:rgba(255,255,255,0.55);font-size:10px;font-weight:700;
                   letter-spacing:2px;margin:0 0 4px 0;'>🌤️ WEATHER REPORT</p>
              <p style='color:white;font-size:20px;font-weight:900;margin:0 0 8px 0;'>
                📍 {_whtml.escape(st.session_state.weather_name)}</p>
              <p style='color:white;font-size:68px;font-weight:900;margin:0;line-height:1;'>{_temp}°</p>
              <p style='color:rgba(255,255,255,0.65);font-size:13px;margin:4px 0 2px 0;'>
                Feels like {_feels}°C</p>
              <p style='color:rgba(255,255,255,0.9);font-size:17px;font-weight:600;margin:0;'>
                {_wemoji} {_wdesc}</p>
            </div>
            <div style='text-align:right;'>
              <p style='font-size:72px;margin:0;line-height:1;'>{_wemoji}</p>
              <p style='color:rgba(255,255,255,0.5);font-size:11px;margin:8px 0 0 0;'>☁️ Cloud: {_cloud}%</p>
              <p style='color:rgba(255,255,255,0.5);font-size:11px;margin:2px 0;'>👁️ Visibility: {_vis} km</p>
              <p style='color:rgba(255,255,255,0.5);font-size:11px;margin:2px 0;'>💧 Dew point: {_dew}°C</p>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Stats row (6 boxes)
        _sc = st.columns(6)
        def _sbox(col, lbl, val, sub=""):
            with col:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);
                     border-radius:14px;padding:12px 4px;text-align:center;'>
                  <p style='color:rgba(255,255,255,0.4);font-size:8px;font-weight:700;
                       letter-spacing:1.5px;margin:0 0 5px 0;'>{lbl}</p>
                  <p style='color:white;font-size:20px;font-weight:900;margin:0;'>{val}</p>
                  <p style='color:rgba(255,255,255,0.45);font-size:8px;margin:3px 0 0 0;'>{sub}</p>
                </div>""", unsafe_allow_html=True)
        _sbox(_sc[0],"HUMIDITY",   f"{_hum}%",          "")
        _sbox(_sc[1],"WIND",       f"{_wspd}",           f"{_wdir} km/h")
        _sbox(_sc[2],"AQI",        str(_aqi_v),          _aqi_lbl)
        _sbox(_sc[3],"MOON",       _moon_e,              _moon_n)
        _sbox(_sc[4],"UV INDEX",   str(_uv),             "Max today")
        _sbox(_sc[5],"RAIN CHANCE",f"{_rainc}%",         "Today")

        # Sunrise / Sunset
        st.markdown(f"""
        <div style='display:flex;gap:10px;margin:12px 0;'>
          <div style='flex:1;background:rgba(255,190,60,0.1);border:1px solid rgba(255,190,60,0.3);
               border-radius:12px;padding:12px;text-align:center;'>
            <p style='color:rgba(255,190,60,0.7);font-size:9px;font-weight:700;
                 letter-spacing:1.5px;margin:0 0 4px 0;'>SUNRISE</p>
            <p style='color:white;font-size:20px;font-weight:900;margin:0;'>🌅 {_sr}</p>
          </div>
          <div style='flex:1;background:rgba(255,110,40,0.1);border:1px solid rgba(255,110,40,0.3);
               border-radius:12px;padding:12px;text-align:center;'>
            <p style='color:rgba(255,140,60,0.7);font-size:9px;font-weight:700;
                 letter-spacing:1.5px;margin:0 0 4px 0;'>SUNSET</p>
            <p style='color:white;font-size:20px;font-weight:900;margin:0;'>🌇 {_ss}</p>
          </div>
        </div>""", unsafe_allow_html=True)

        # Hourly forecast — next 12 hours
        st.markdown("<p style='color:rgba(200,210,255,0.7);font-size:11px;font-weight:800;"
                    "letter-spacing:2px;margin:14px 0 10px 0;'>HOURLY FORECAST — NEXT 12 HOURS</p>",
                    unsafe_allow_html=True)
        _hh = "<div style='display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;'>"
        for _hi in range(min(12, len(_hr["time"]))):
            _ht  = str(_hr["time"][_hi]).split("T")[-1][:5]
            _hte = round(_hr["temperature_2m"][_hi])
            _hce = _wmo_info(_hr["weathercode"][_hi])[0]
            _hrp = _hr["precipitation_probability"][_hi] if _hr.get("precipitation_probability") else 0
            _hh += (f"<div style='flex:0 0 auto;background:rgba(255,255,255,0.06);"
                    f"border:1px solid rgba(255,255,255,0.09);border-radius:12px;"
                    f"padding:10px 10px;text-align:center;min-width:66px;'>"
                    f"<p style='color:rgba(255,255,255,0.5);font-size:9px;margin:0 0 6px 0;'>{_ht}</p>"
                    f"<p style='font-size:20px;margin:0 0 4px 0;'>{_hce}</p>"
                    f"<p style='color:white;font-size:13px;font-weight:700;margin:0;'>{_hte}°</p>"
                    f"<p style='color:#60a5fa;font-size:9px;margin:2px 0 0 0;'>💧{_hrp}%</p></div>")
        st.markdown(_hh + "</div>", unsafe_allow_html=True)

        # 7-day forecast
        st.markdown("<p style='color:rgba(200,210,255,0.7);font-size:11px;font-weight:800;"
                    "letter-spacing:2px;margin:14px 0 10px 0;'>7-DAY FORECAST</p>",
                    unsafe_allow_html=True)
        _dh = "<div style='display:flex;flex-direction:column;gap:6px;'>"
        for _di in range(len(_dy["time"])):
            try:
                _dname = _dt.date.fromisoformat(str(_dy["time"][_di])).strftime("%A") if _di else "Today"
            except Exception:
                _dname = f"Day {_di+1}"
            _dmx  = round(_dy["temperature_2m_max"][_di])
            _dmn  = round(_dy["temperature_2m_min"][_di])
            _dce, _dcd = _wmo_info(_dy["weathercode"][_di])
            _drc  = _dy["precipitation_probability_max"][_di]
            _dh += (f"<div style='display:flex;align-items:center;background:rgba(255,255,255,0.05);"
                    f"border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:10px 16px;'>"
                    f"<span style='color:rgba(255,255,255,0.75);font-size:12px;font-weight:700;width:80px;'>{_dname}</span>"
                    f"<span style='font-size:18px;width:30px;'>{_dce}</span>"
                    f"<span style='color:rgba(255,255,255,0.55);font-size:11px;flex:1;'>{_dcd}</span>"
                    f"<span style='color:#60a5fa;font-size:11px;margin-right:12px;'>💧{_drc}%</span>"
                    f"<span style='color:rgba(255,255,255,0.4);font-size:12px;margin-right:8px;'>{_dmn}°</span>"
                    f"<span style='color:white;font-size:14px;font-weight:700;'>{_dmx}°</span></div>")
        st.markdown(_dh + "</div>", unsafe_allow_html=True)

        # Temperature trend chart
        st.markdown("<p style='color:rgba(200,210,255,0.7);font-size:11px;font-weight:800;"
                    "letter-spacing:2px;margin:14px 0 8px 0;'>TEMPERATURE TREND — 7 DAYS</p>",
                    unsafe_allow_html=True)
        _chart = {
            "Max °C": [round(_dy["temperature_2m_max"][i]) for i in range(len(_dy["time"]))],
            "Min °C": [round(_dy["temperature_2m_min"][i]) for i in range(len(_dy["time"]))],
        }
        try:
            st.line_chart(_chart, color=["#f97316","#60a5fa"])
        except Exception:
            st.line_chart(_chart)

        # Weather summary (no API needed)
        _tip = ("☔ Carry an umbrella today." if _rainc > 50
                else "🕶️ It's sunny — wear sunscreen." if _code == 113 and _uv >= 6
                else "😷 Poor air quality — limit outdoor exposure." if _aqi_v > 80
                else "🥵 Very hot — stay hydrated." if _temp >= 38
                else "🧥 Cool weather — carry a jacket." if _temp <= 15
                else "✅ Pleasant weather — great day to go outside.")
        st.markdown(f"""
        <div style='background:rgba(137,180,250,0.08);border:1px solid rgba(137,180,250,0.22);
             border-radius:12px;padding:14px 18px;margin-top:6px;'>
          <p style='color:#e8e8e8;font-size:13px;line-height:1.65;margin:0;'>
            🌤️ <b>{st.session_state.weather_name}</b> — {_wdesc}, {_temp}°C (feels {_feels}°C).
            Humidity {_hum}%, wind {_wspd} km/h {_wdir}, UV index {_uv}.
            Rain chance {_rainc}%.<br><br>{_tip}</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#6b7a99;font-size:.8rem;padding:8px 0'>Type a city or state above, or ask me in the chat — e.g. \"weather in Mumbai\"</div>", unsafe_allow_html=True)



def _is_system_health_request(text):
    t = text.lower()
    return any(k in t for k in (
        'check my system', 'check system', 'system health', 'system check',
        'check hardware', 'hardware health', 'system scan', 'scan my system',
        'check my pc', 'pc health', 'laptop health', 'show my laptop',
        'check inside', 'inside system', 'inside my laptop', 'laptop internals',
        'check my laptop', 'system damage', 'any damage', 'damage in system',
        'damage in my', 'check for damage', 'show damage', 'show system',
        'hardware check', 'laptop check', 'computer health', 'cpu temperature',
        'check temperature', 'check ram', 'check storage', 'check battery',
        'show my pc', 'show my computer', 'inside of my pc', 'inside of my laptop',
        'pc internals', 'computer internals', 'inside my computer', 'inside my pc',
        'show pc inside', 'pc inside', 'laptop inside', 'inside part',
        'scan system', 'scan pc', 'scan laptop', 'scan computer',
        'check my computer', 'check inside my', 'show inside', 'view inside',
        'what is inside my', 'what inside my', 'how is my system',
        'how is my pc', 'how is my laptop', 'how is my computer',
        'is my pc ok', 'is my laptop ok', 'is my system ok',
        'any errors in my system', 'any errors in my pc', 'error in system',
        'diagram of my', 'show a diagram of my', 'show diagram of my',
        'system diagram', 'pc diagram', 'laptop diagram', 'inside diagram',
        'show my system', 'show my pc health', 'show my laptop health',
        'my system status', 'my pc status', 'my laptop status',
        'how much ram', 'how many ram', 'my ram', 'total ram', 'ram size',
        'how many cpu', 'cpu cores', 'my cpu', 'my processor', 'cpu model',
        'my laptop name', 'laptop name', 'laptop model', 'computer model', 'pc model',
        'my pc name', 'my computer name', 'name of my laptop', 'name of my pc',
        'what laptop', 'what pc', 'which laptop', 'which pc',
        'disk space', 'storage space', 'free space', 'how much storage',
    ))


# ── Animated Diagrams (AI-generated) ─────────────────────────────────────────
def _is_diagram_request(text):
    t = text.lower()
    if _is_system_health_request(text):
        return False
    return any(k in t for k in [
        'diagram','structure of','layers of','how does','how do','show me','draw',
        'illustrate','explain the structure','explain how','model of','system of',
        'cycle of','process of','parts of','mechanism of','anatomy','cross section',
        'cross-section','how it works','give a diagram','make a diagram',
        'create a diagram','show the structure','what is the structure',
        'solar system','atom','dna','cell structure','water cycle','food chain',
        'photosynthesis','human heart','nervous system','plant structure',
        'projectile motion','circular motion','volcano','earthquake','rock cycle',
        'greenhouse effect','seasons','plate tectonics','river erosion',
        'refraction','reflection','wave','circuit','electromagnetic','atmosphere',
    ])

def _generate_diagram_html(user_query):
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        return ""
    try:
        from groq import Groq as _DGroq
        import re as _re_d
        _gc = _DGroq(api_key=api_key)
        _prompt = (
            "Create a beautiful animated educational diagram for: " + user_query + "\n\n"
            "STRICT REQUIREMENTS:\n"
            "1. Self-contained HTML5 page using <canvas> + requestAnimationFrame\n"
            "2. Background: #010208 (very dark blue-black), canvas size 500x340\n"
            "3. Animate ONLY elements that naturally move (planets orbit, electrons spin, "
            "water flows, blood pumps) -- static parts stay still\n"
            "4. Use glowing neon colors: cyan #00e5ff, purple #a855f7, green #22c55e, "
            "gold #ffd700, red #ef5350, orange #ff9800\n"
            "5. Add clear text labels for ALL main parts\n"
            "6. Add a title at the top in #40E0D0 turquoise color\n"
            "7. Add a short description at the bottom\n"
            "8. Return ONLY raw HTML starting with <!DOCTYPE html> -- no markdown, no code fences"
        )
        for _model in ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]:
            try:
                _r = _gc.chat.completions.create(
                    model=_model,
                    messages=[
                        {"role": "system", "content": (
                            "You are an expert HTML5 canvas animator. "
                            "Generate beautiful animated educational diagrams. "
                            "Return ONLY raw HTML starting with <!DOCTYPE html>. "
                            "No markdown, no code blocks, no explanation."
                        )},
                        {"role": "user", "content": _prompt},
                    ],
                    max_tokens=4096,
                    temperature=0.3,
                )
                _html = (_r.choices[0].message.content or "").strip()
                _m2 = _re_d.search(r'```html\n?([\s\S]+?)```', _html)
                if _m2:
                    _html = _m2.group(1).strip()
                else:
                    _cut = _re_d.search(r'<!DOCTYPE html', _html, _re_d.IGNORECASE)
                    if _cut:
                        _html = _html[_cut.start():]
                if "<!DOCTYPE html>" in _html or "<html" in _html or "<canvas" in _html:
                    return _html
            except Exception:
                continue
    except Exception:
        pass
    return ""




# ── Chat messages (shown in ALL modes) ───────────────────────────────────────
_msgs_list = cur_msgs()
_last_asst_content = ""
for _mi, msg in enumerate(_msgs_list):
    with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🔱"):
        if msg["role"] == "assistant" and _mi > 0:
            _prev = _msgs_list[_mi - 1]
            # System health diagram
            if _prev["role"] == "user" and _is_system_health_request(_prev["content"]):
                import hashlib as _hlib_sh, html as _html_esc_sh
                _shkey_d = _hlib_sh.md5(_prev["content"].encode()).hexdigest()
                _sh_diag_html = st.session_state.get("_sys_health_cache", {}).get(_shkey_d, "")
                if _sh_diag_html:
                    st.markdown(
                        "<div style='font-size:.72rem;color:#a78bfa;letter-spacing:2px;"
                        "margin:6px 0 4px;font-weight:bold'>🖥️ YOUR PC HEALTH DIAGRAM — "
                        "<span style='color:#00cc66'>GREEN = Good</span> · "
                        "<span style='color:#ffaa00'>YELLOW = Warning</span> · "
                        "<span style='color:#ff3333'>RED = Problem</span></div>",
                        unsafe_allow_html=True
                    )
                    import streamlit.components.v1 as _cv1_sh
                    _cv1_sh.html(_sh_diag_html, height=430, scrolling=False)
            # Animated diagram
            if _prev["role"] == "user" and _is_diagram_request(_prev["content"]):
                import hashlib as _hlib_d, html as _html_esc_d
                _dkey = _hlib_d.md5(_prev["content"].encode()).hexdigest()
                _dhtml = st.session_state.diagram_cache.get(_dkey, "")
                if _dhtml:
                    import streamlit.components.v1 as _cv1_d
                    _cv1_d.html(_dhtml, height=390, scrolling=False)
        # Strip ASCII art from AI response when a diagram is shown
        import re as _re_diag
        _content_show = msg["content"]
        # Hide raw DALL-E image marker (image is rendered above)
        if _re_diag.match(r'^\[DALLE_IMAGE:[a-f0-9]+\]$', _content_show.strip()):
            _content_show = ""
        # Render AI-generated image
        _img_match = _re_diag.search(r'\[TITAN_IMAGE:([^\]]+)\]', _content_show)
        if _img_match:
            try: st.image(_img_match.group(1), use_container_width=True)
            except Exception: pass
            _content_show = _re_diag.sub(r'\[TITAN_IMAGE:[^\]]+\]', '', _content_show).strip()
        # Render AI-generated video
        _vid_match = _re_diag.search(r'\[TITAN_VIDEO:([^\]]+)\]', _content_show)
        if _vid_match:
            try: st.video(_vid_match.group(1))
            except Exception: pass
            _content_show = _re_diag.sub(r'\[TITAN_VIDEO:[^\]]+\]', '', _content_show).strip()
        if msg["role"] == "assistant" and _mi > 0:
            _prev2 = _msgs_list[_mi - 1]
            if _prev2["role"] == "user" and _is_diagram_request(_prev2["content"]):
                _content_show = _re_diag.sub(
                    r'(?:```[^\n]*\n)?(?:[ \t]*[┌┐└┘│─├┤┬┴┼╔╗╚╝║═╠╣╦╩╬+|^~*#=/\\-]{2,}[^\n]*\n){2,}(?:```\n?)?',
                    '', _content_show)
                _content_show = _re_diag.sub(r'(?:[ \t]{1,}[^a-zA-Z0-9\n\r ]{3,}[ \t]*\n){2,}', '', _content_show)
                _content_show = _re_diag.sub(r'(?:[^\n]*[+\-]{3,}[^\n]*\n)+', '', _content_show)
                _content_show = _re_diag.sub(r'(?:\|[^\n]+\|\n)+', '', _content_show)
        import re as _re_ltx
        _content_show = _re_ltx.sub(r'\\\[(.+?)\\\]', r'$$\1$$', _content_show, flags=_re_ltx.DOTALL)
        _content_show = _re_ltx.sub(r'\\\((.+?)\\\)', r'$\1$', _content_show, flags=_re_ltx.DOTALL)
        import re as _re_sug_strip
        _content_show = _re_sug_strip.sub(r'\n?\[SUGGEST:[^\]]{0,300}\]', '', _content_show).strip()
        st.markdown(_content_show, unsafe_allow_html=True)
        if msg["role"] == "assistant" and msg.get("content"):
            import json as _json_sb, re as _re_sb
            _spk = _re_sb.sub(r'```[\s\S]*?```', ' code block ', msg["content"])
            _spk = _re_sb.sub(r'!\[.*?\]\(.*?\)', '', _spk)
            _spk = _re_sb.sub(r'\[(.*?)\]\(.*?\)', r'\1', _spk)
            _spk = _re_sb.sub(r'[`*_#>\[\]|]', '', _spk)
            _spk = _re_sb.sub(r'\s+', ' ', _spk).strip()[:4500]
            _spk_payload = _json_sb.dumps(_spk)
            _rxn_tier = st.session_state.get("titan_tier", "basic")
            _show_rxn = _rxn_tier in ("pro", "max")
            _rxn_accent = "#f59e0b" if _rxn_tier == "max" else "#a78bfa"
            st.html(f"""
<style>
  body {{ margin:0; padding:0; background:transparent;
          font-family:-apple-system,Segoe UI,Roboto,sans-serif; }}
  .tu-btn {{ background:transparent; color:#555; border:0; border-radius:6px;
        padding:2px 6px; font-size:.75rem; cursor:pointer; opacity:.6;
        line-height:1.3; transition:all .15s; }}
  .tu-btn:hover {{ opacity:1; color:#e8e8e8; }}
  #b {{ background:#1e3a8a; color:#fff; border:0; border-radius:6px;
        padding:1px 8px; font-size:.62rem; font-weight:500;
        cursor:pointer; opacity:.65; line-height:1.3; }}
  #b:hover {{ opacity:1; }}
  #b.on {{ background:#dc2626; }}
  #cp.done {{ color:#22c55e !important; opacity:1 !important; }}
  .rxn-bar {{ display:{'flex' if _show_rxn else 'none'};gap:2px;align-items:center;margin-left:6px;
        border-left:1px solid #222;padding-left:8px; }}
  .rxn {{ background:transparent;border:0;font-size:.9rem;cursor:pointer;
        padding:1px 3px;border-radius:5px;transition:all .15s;opacity:.4;line-height:1; }}
  .rxn:hover {{ opacity:1;transform:scale(1.2); }}
  .rxn.active {{ opacity:1;filter:drop-shadow(0 0 4px {_rxn_accent}); }}
</style>
<div style="display:flex;gap:4px;align-items:center">
<button id="b">speak</button>
<button class="tu-btn" id="cp" title="Copy">⧉</button>
<button class="tu-btn" id="sh" title="Share">↗</button>
<div class="rxn-bar" id="rxnbar">
  <button class="rxn" data-r="love" title="Love it">❤️</button>
  <button class="rxn" data-r="fire" title="Amazing">🔥</button>
  <button class="rxn" data-r="mind" title="Mind blown">🤯</button>
  <button class="rxn" data-r="bulb" title="Insightful">💡</button>
</div>
</div>
<script>
(function() {{
  const TEXT = {_spk_payload};
  const b = document.getElementById('b');
  b.addEventListener('click', function() {{
    try {{
      const synth = window.speechSynthesis;
      if (b.classList.contains('on')) {{
        synth.cancel();
        b.classList.remove('on');
        b.textContent = 'speak';
        return;
      }}
      synth.cancel();
      const u = new SpeechSynthesisUtterance(TEXT);
      u.rate = 0.95; u.pitch = 0.7; u.volume = 1.0; u.lang = 'en-US';
      const speakWith = function(vs) {{
        const femaleRe = /zira|hazel|susan|jenny|aria|eva|female|woman|girl|samantha|victoria|karen|tessa|moira|fiona|catherine|linda/i;
        const preferred = ['guy','ryan','mark','andrew','brian','christopher','eric','matthew','aaron','james'];
        let v = null;
        for (const name of preferred) {{
          v = vs.find(function(x) {{
            return new RegExp(name, 'i').test(x.name) && !femaleRe.test(x.name) && /en/i.test(x.lang);
          }});
          if (v) break;
        }}
        if (!v) v = vs.find(function(x) {{ return /male/i.test(x.name) && !femaleRe.test(x.name) && /en/i.test(x.lang); }});
        if (!v) v = vs.find(function(x) {{ return /david|daniel|alex|fred|tom|paul|george/i.test(x.name) && !femaleRe.test(x.name); }});
        if (!v) v = vs.find(function(x) {{ return /en[-_](us|gb)/i.test(x.lang) && !femaleRe.test(x.name); }});
        if (!v) v = vs.find(function(x) {{ return /en/i.test(x.lang); }});
        if (v) u.voice = v;
        u.onend = function() {{ b.classList.remove('on'); b.textContent = 'speak'; }};
        b.classList.add('on');
        b.textContent = 'stop';
        synth.speak(u);
      }};
      const vs = synth.getVoices();
      if (vs.length) speakWith(vs);
      else synth.onvoiceschanged = function() {{ speakWith(synth.getVoices()); }};
    }} catch(e) {{ console.error('Speak error:', e); }}
  }});
  document.getElementById('cp').addEventListener('click',function(){{
    var btn=document.getElementById('cp');
    var orig=btn.textContent;
    var pd=window.parent.document;
    var sc=pd.createElement('script');
    sc.textContent='(function(){{var t=document.createElement("textarea");t.value='+JSON.stringify(TEXT)+';t.style.cssText="position:fixed;top:-9999px;left:-9999px;opacity:0";document.body.appendChild(t);t.focus();t.select();try{{document.execCommand("copy");}}catch(e){{}}document.body.removeChild(t);}})();';
    pd.head.appendChild(sc); sc.remove();
    btn.textContent='✓'; btn.classList.add('done');
    setTimeout(function(){{btn.textContent=orig;btn.classList.remove('done');}},1800);
  }});
  document.getElementById('sh').addEventListener('click',function(){{
    var TEXT_SH=TEXT;
    var pd=window.parent.document;
    var existingPopup=pd.getElementById('_titan_share_popup');
    if(existingPopup){{existingPopup.remove();return;}}
    var overlay=pd.createElement('div');
    overlay.id='_titan_share_popup';
    overlay.style.cssText='position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.55)';
    var box=pd.createElement('div');
    box.style.cssText='background:#1a1a2e;border:1px solid #3a3a5c;border-radius:16px;padding:24px 28px;min-width:260px;box-shadow:0 8px 32px rgba(0,0,0,0.6);display:flex;flex-direction:column;gap:12px';
    var title=pd.createElement('div');
    title.textContent='Share answer';
    title.style.cssText='color:#e8e8e8;font-size:15px;font-weight:600;margin-bottom:4px';
    box.appendChild(title);
    var items=[
      ['📋  Copy text',function(){{
        var sc2=pd.createElement('script');
        sc2.textContent='(function(){{var t=document.createElement("textarea");t.value='+JSON.stringify(TEXT_SH)+';t.style.cssText="position:fixed;top:-9999px;opacity:0";document.body.appendChild(t);t.focus();t.select();try{{document.execCommand("copy");}}catch(e){{}}document.body.removeChild(t);}})();';
        pd.head.appendChild(sc2);sc2.remove();
        overlay.remove();
      }}],
      ['💬  WhatsApp',function(){{window.open('https://wa.me/?text='+encodeURIComponent(TEXT_SH),'_blank');overlay.remove();}}],
      ['✈️  Telegram',function(){{window.open('https://t.me/share/url?text='+encodeURIComponent(TEXT_SH),'_blank');overlay.remove();}}],
      ['📧  Email',function(){{window.open('mailto:?body='+encodeURIComponent(TEXT_SH),'_blank');overlay.remove();}}]
    ];
    items.forEach(function(item){{
      var btn2=pd.createElement('button');
      btn2.textContent=item[0];
      btn2.style.cssText='background:#2a2a3e;color:#e8e8e8;border:1px solid #3a3a5c;border-radius:10px;padding:10px 16px;font-size:14px;cursor:pointer;text-align:left;width:100%';
      btn2.onmouseover=function(){{btn2.style.background='#3a3a5e';}};
      btn2.onmouseout=function(){{btn2.style.background='#2a2a3e';}};
      btn2.onclick=item[1];
      box.appendChild(btn2);
    }});
    var cancel=pd.createElement('button');
    cancel.textContent='Cancel';
    cancel.style.cssText='background:transparent;color:#888;border:none;font-size:13px;cursor:pointer;margin-top:4px';
    cancel.onclick=function(){{overlay.remove();}};
    box.appendChild(cancel);
    overlay.onclick=function(e){{if(e.target===overlay)overlay.remove();}};
    overlay.appendChild(box);
    pd.body.appendChild(overlay);
  }});
  document.querySelectorAll('.rxn').forEach(function(btn){{
    btn.addEventListener('click',function(){{
      var wasActive = btn.classList.contains('active');
      document.querySelectorAll('.rxn').forEach(function(b2){{b2.classList.remove('active');}});
      if(!wasActive) btn.classList.add('active');
    }});
  }});
}})();
</script>
""")
    if msg["role"] == "assistant":
        _last_asst_content = msg["content"]

# ── Message stagger animation (cascade 35 ms per bubble) ─────────────────────
if cur_msgs():
    st.html("""<script>
(function(){
  var msgs = document.querySelectorAll('[data-testid="stChatMessage"]');
  msgs.forEach(function(el, i){
    el.style.animationDelay = Math.min(i * 35, 180) + 'ms';
  });
})();
</script>""")

# ── Smart Follow-up Suggestion Chips (Pro + Max only) ────────────────────────
import re as _re_sfup
_sfup_tier = st.session_state.get("titan_tier", "basic")
if _sfup_tier in ("pro", "max") and _last_asst_content and cur_msgs():
    _sfup_match = _re_sfup.search(r'\[SUGGEST:\s*([^\]]{1,300})\]', _last_asst_content)
    if _sfup_match:
        _follow_ups = [s.strip() for s in _sfup_match.group(1).split('|') if s.strip()][:3]
        if _follow_ups:
            _chip_color = "#f59e0b" if _sfup_tier == "max" else "#7c3aed"
            st.markdown(f"<div style='height:6px'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:.58rem;color:{_chip_color};letter-spacing:1.5px;margin-bottom:4px;padding-left:2px'>ASK ME MORE</div>", unsafe_allow_html=True)
            _suf_cols = st.columns(len(_follow_ups))
            for _si, _sq in enumerate(_follow_ups):
                with _suf_cols[_si]:
                    if st.button(f"→  {_sq}", key=f"_sfup_{_si}_{len(_last_asst_content)}", use_container_width=True):
                        st.session_state._home_pending = _sq
                        st.rerun()

# ── Voice Talk-Back: speak the most recent assistant reply (once) ────────────
if st.session_state.get("voice_reply") and _last_asst_content:
    import hashlib as _hl, json as _jsv, re as _revc
    # Strip markdown so speech sounds natural (no asterisks, hashes, code fences)
    _clean = _revc.sub(r'```[\s\S]*?```', ' (code block) ', _last_asst_content)
    _clean = _revc.sub(r'[`*_#>\[\]|]', '', _clean)
    _clean = _revc.sub(r'!\[.*?\]\(.*?\)', '', _clean)
    _clean = _revc.sub(r'\[(.*?)\]\(.*?\)', r'\1', _clean)
    _clean = _revc.sub(r'\s+', ' ', _clean).strip()
    _hash = _hl.md5(_clean.encode()).hexdigest()
    if st.session_state.get("_last_spoken_hash") != _hash:
        st.session_state._last_spoken_hash = _hash
        _rate = float(st.session_state.get("voice_rate", 1.0))
        _payload = _jsv.dumps(_clean[:4000])  # cap to avoid huge utterances
        st.html(
            f"""
            <script>
              try {{
                window.speechSynthesis.cancel();
                const u = new SpeechSynthesisUtterance({_payload});
                u.rate = {_rate}; u.pitch = 1.0; u.volume = 1.0; u.lang = 'en-US';
                const pick = () => {{
                  const vs = window.speechSynthesis.getVoices();
                  const pref = vs.find(v => /Google.*English|Microsoft.*English|en[-_]US/i.test(v.name + ' ' + v.lang));
                  if (pref) u.voice = pref;
                  window.speechSynthesis.speak(u);
                }};
                if (window.speechSynthesis.getVoices().length) pick();
                else window.speechSynthesis.onvoiceschanged = pick;
              }} catch (e) {{ console.error('TTS error:', e); }}
            </script>
            """
        )

# Detect exam paper: flag-based (reliable) OR keyword fallback
if st.session_state.ep_generating and _last_asst_content:
    st.session_state.ep_last_paper = _last_asst_content
    st.session_state.ep_generating = False
else:
    _kws = ["answer key","total marks","marks)","(a)","(b)","(c)","(d)","q1","q2","section"]
    if _last_asst_content and sum(1 for kw in _kws if kw in _last_asst_content.lower()) >= 4:
        st.session_state.ep_last_paper = _last_asst_content

# Show Download + PDF buttons whenever a paper exists
if st.session_state.ep_last_paper:
    _paper = st.session_state.ep_last_paper
    _fname_base = st.session_state.ep_last_name
    _dc1, _dc2 = st.columns(2)
    with _dc1:
        st.download_button("📥 Download (.txt)", _paper,
                           file_name=_fname_base + "_exam.txt",
                           mime="text/plain", key="ep_dl",
                           use_container_width=True)
    with _dc2:
        _pdf_bytes = _make_exam_pdf(_paper, _fname_base.replace("_"," "))
        if _pdf_bytes:
            st.download_button("📄 Download PDF", _pdf_bytes,
                               file_name=_fname_base + "_exam.pdf",
                               mime="application/pdf", key="ep_pdf",
                               use_container_width=True)
        else:
            st.warning("PDF error — use .txt download")

# ── Chat PDF export download button ──────────────────────────────────────────
if st.session_state.get("_pending_pdf"):
    st.download_button("⬇️ Download Chat PDF", st.session_state["_pending_pdf"],
                       "titan_chat.pdf", "application/pdf",
                       key="_chat_pdf_dl_main", use_container_width=True)
    if st.button("✕ Dismiss", key="_pdf_dismiss"):
        st.session_state["_pending_pdf"] = None
        st.rerun()

# ── PDF page extraction download button ──────────────────────────────────────
if st.session_state.get("_pending_pdf_extract"):
    _pex_bytes, _pex_name = st.session_state["_pending_pdf_extract"]
    st.download_button("⬇️ Download Extracted Pages", _pex_bytes,
                       _pex_name, "application/pdf",
                       key="_pdf_extract_dl", use_container_width=True)
    if st.button("✕ Dismiss", key="_pex_dismiss"):
        st.session_state.pop("_pending_pdf_extract", None)
        st.rerun()

# ── Animated video (GIF) download button ─────────────────────────────────────
if st.session_state.get("_pending_video_gif"):
    _vgif_bytes, _vgif_name = st.session_state["_pending_video_gif"]
    st.image(_vgif_bytes, caption="🎬 Your animated video — preview", use_container_width=True)
    st.download_button("⬇️ Download Video (GIF)", _vgif_bytes,
                       _vgif_name, "image/gif",
                       key="_vid_gif_dl", use_container_width=True)
    if st.button("✕ Dismiss", key="_vgif_dismiss"):
        st.session_state.pop("_pending_video_gif", None)
        st.rerun()

# Attach + Voice popovers are rendered in the sidebar (below the Memory expander).
temp = 0.7  # full reasoning quality always — matches Claude Pro depth

# ── Code request detection ────────────────────────────────────────────────────
def _is_code_request(text):
    t = text.lower()
    _code_kws = (
        'write code','write a code','write a program','write a script',
        'write a function','write a class','code for','code to ',
        'program to','script to','function to','function that',
        'debug this','fix this code','fix the bug','fix this bug',
        'explain this code','explain the code','what does this code',
        'refactor','optimize this code','improve this code',
        'how to code','how to program','how to build','how to create',
        'html','css','javascript','python code','java code','c++ code',
        'react','nodejs','sql query','write sql','write html','write css',
        'api call','rest api','implement','algorithm','data structure',
    )
    return any(k in t for k in _code_kws)

# ── Search request detection ──────────────────────────────────────────────────
def _is_search_request(text):
    t = text.lower()
    return any(k in t for k in (
        'search for','look up','find information','what is the latest',
        'what are the latest','latest news','current news','recent news',
        'what happened','who won','current price','stock price',
        'live score','today\'s match','news about','trending',
        'who is the current','what is the current','right now',
        'as of today','recently','just happened','breaking news',
        'find out','search the web','google this','search google',
        'look it up','find me information','tell me about the latest',
        'today','this week','this month','this year','2024','2025','2026',
        'new release','just released','just launched','announced',
        'update on','status of','price of','cost of',
        'weather','temperature','forecast','humidity','rain today',
        'aqi','air quality','will it rain','cold today','hot today',
        'weather in','weather at','climate in',
    ))

_TRUSTED_DOMAINS = [
    'wikipedia.org','britannica.com','bbc.com','bbc.co.uk','reuters.com',
    'apnews.com','theguardian.com','nature.com','pubmed.ncbi.nlm.nih.gov',
    'who.int','cdc.gov','nih.gov','ncbi.nlm.nih.gov','nasa.gov',
    'microsoft.com','apple.com','google.com','github.com','python.org',
    'stackoverflow.com','mozilla.org','developer.mozilla.org',
    'investopedia.com','moneycontrol.com','economictimes.indiatimes.com',
    'ndtv.com','thehindu.com','hindustantimes.com','timesofindia.com',
    'espncricinfo.com','cricinfo.com','techcrunch.com','wired.com',
    'theverge.com','arstechnica.com','cnet.com','tomshardware.com',
    'gsmarena.com','91mobiles.com','khanacademy.org','ncert.nic.in',
    'cbse.gov.in','wolframalpha.com','sciencedirect.com','researchgate.net',
    'forbes.com','businessinsider.com','cnbc.com','bloomberg.com',
    'healthline.com','mayoclinic.org','webmd.com','nhs.uk',
]
_SCAM_INDICATORS = [
    'free-money','earn-fast','get-rich','lottery-winner','prize-claim',
    'bitcoin-doubler','crypto-giveaway','click-to-claim','urgent-reward',
    'limited-offer-claim','work-from-home-earn','online-job-earn-daily',
]

def _is_trusted_url(url):
    url_l = url.lower()
    if any(s in url_l for s in _SCAM_INDICATORS):
        return False
    return (any(d in url_l for d in _TRUSTED_DOMAINS) or
            '.gov' in url_l or '.edu' in url_l or '.ac.' in url_l)

def _web_search(query, max_results=8):
    """Search the web using DuckDuckGo — trusted sources only, no scam sites ever."""
    try:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            import subprocess as _sp, sys as _sys
            _sp.run([_sys.executable, "-m", "pip", "install", "duckduckgo-search", "-q"], capture_output=True)
            from duckduckgo_search import DDGS
        raw = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results * 3):
                raw.append(r)
        # Strict: trusted domains only — never fall back to untrusted results
        trusted = [r for r in raw if _is_trusted_url(r.get('href', ''))]
        # If no trusted hits, relax to non-scam sites (but still block scam indicators)
        if not trusted:
            trusted = [r for r in raw if not any(
                s in r.get('href','').lower() for s in _SCAM_INDICATORS
            )]
        results = []
        for r in trusted[:max_results]:
            src = r.get('href','').split('/')[2] if r.get('href') else ''
            results.append(f"• [{src}] {r['title']}\n  {r['body']}")
        return "\n\n".join(results) if results else ""
    except Exception:
        return ""

# ── YouTube transcript analysis ────────────────────────────────────────────────
def _is_youtube_url(text):
    return bool(re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+', text, re.I))

def _extract_youtube_id(text):
    m = re.search(r'(?:v=|youtu\.be/)([\w-]{11})', text)
    return m.group(1) if m else None

def _get_youtube_transcript(url_or_text):
    vid_id = _extract_youtube_id(url_or_text)
    if not vid_id:
        return None, None
    try:
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            import subprocess as _ysp, sys as _ysys
            _ysp.run([_ysys.executable, "-m", "pip", "install", "youtube-transcript-api", "-q"],
                     capture_output=True)
            from youtube_transcript_api import YouTubeTranscriptApi
        for _langs in (['en'], ['hi', 'te', 'ta', 'kn', 'ml'], None):
            try:
                if _langs:
                    tlist = YouTubeTranscriptApi.get_transcript(vid_id, languages=_langs)
                else:
                    tlist = YouTubeTranscriptApi.get_transcript(vid_id)
                text = ' '.join(t['text'] for t in tlist)
                words = text.split()
                if len(words) > 5000:
                    text = ' '.join(words[:5000]) + '... [transcript continues]'
                return vid_id, text
            except Exception:
                continue
    except Exception:
        pass
    return vid_id, None

# ── General URL content reader ─────────────────────────────────────────────────
def _extract_first_url(text):
    m = re.search(r'https?://[^\s<>"\']+', text)
    return m.group(0) if m else None

def _fetch_url_content(url, max_chars=7000):
    try:
        _headers = {"User-Agent": "Mozilla/5.0 (compatible; TitanUltra/1.0)"}
        resp = requests.get(url, timeout=10, headers=_headers)
        if resp.status_code != 200:
            return None
        try:
            from bs4 import BeautifulSoup as _BS
        except ImportError:
            import subprocess as _bsp, sys as _bsys
            _bsp.run([_bsys.executable, "-m", "pip", "install", "beautifulsoup4", "-q"],
                     capture_output=True)
            from bs4 import BeautifulSoup as _BS
        soup = _BS(resp.text, 'html.parser')
        for tag in soup(['script','style','nav','footer','header','aside','noscript']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars] if text else None
    except Exception:
        return None

# ── Deep research mode ─────────────────────────────────────────────────────────
def _is_deep_research(text):
    t = text.lower()
    return any(k in t for k in (
        'deep research','deep dive','research about','comprehensive report',
        'detailed research','full report','research on','in depth','in-depth',
        'thorough analysis','complete analysis','everything about',
        'tell me everything','give me a full','give me a complete',
    ))

def _deep_web_research(query):
    try:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            import subprocess as _drsp, sys as _drsys
            _drsp.run([_drsys.executable, "-m", "pip", "install", "duckduckgo-search", "-q"],
                      capture_output=True)
            from duckduckgo_search import DDGS
        _clean = re.sub(
            r'\b(?:deep\s+research|deep\s+dive\s+into|research\s+about|comprehensive\s+report\s+on|'
            r'detailed\s+research\s+on|full\s+report\s+on|research\s+on|in[-\s]depth\s+(?:on|about|into)?|'
            r'thorough\s+analysis\s+of|complete\s+analysis\s+of|everything\s+about|'
            r'tell\s+me\s+everything\s+about|give\s+me\s+a\s+full\s+report\s+on|'
            r'give\s+me\s+a\s+complete)\b',
            '', query, flags=re.IGNORECASE).strip()
        if not _clean:
            _clean = query
        _angles = [
            _clean,
            f"{_clean} latest 2025",
            f"{_clean} how it works explained",
            f"{_clean} facts statistics data",
        ]
        _seen, _all = set(), []
        for _sq in _angles:
            try:
                with DDGS() as ddgs:
                    for r in ddgs.text(_sq, max_results=5):
                        if r.get('title') not in _seen:
                            _seen.add(r.get('title', ''))
                            _all.append(f"**{r.get('title','')}**\n{r.get('body','')}\nSource: {r.get('href','')}")
            except Exception:
                continue
        return '\n\n'.join(_all[:16]) if _all else ""
    except Exception:
        return ""

# ── Language auto-detection ────────────────────────────────────────────────────
def _detect_user_language(text):
    """Detect if user typed in a non-English language. Returns language name or None."""
    _te = sum(1 for c in text if 'ఀ' <= c <= '౿')
    _hi = sum(1 for c in text if 'ऀ' <= c <= 'ॿ')
    _ta = sum(1 for c in text if '஀' <= c <= '௿')
    _kn = sum(1 for c in text if 'ಀ' <= c <= '೿')
    _ml = sum(1 for c in text if 'ഀ' <= c <= 'ൿ')
    _ar = sum(1 for c in text if '؀' <= c <= 'ۿ')
    _scores = {'Telugu': _te, 'Hindi': _hi, 'Tamil': _ta, 'Kannada': _kn, 'Malayalam': _ml, 'Arabic': _ar}
    _best = max(_scores, key=_scores.get)
    return _best if _scores[_best] >= 3 else None

# ── PC Diagnostics ─────────────────────────────────────────────────────────────
def _is_pc_issue(text):
    t = text.lower()
    return any(k in t for k in (
        'my pc is slow','pc is slow','computer is slow','laptop is slow',
        'high cpu','cpu usage','ram usage','memory usage','high memory',
        'fix my wifi','wifi not working','no internet','internet slow',
        'pc overheating','laptop overheating','pc freezing','computer freezing',
        'diagnose my pc','check my pc','which process','what process',
        'why is my pc','why is my computer','why is my laptop',
        'fix my pc','fix my computer','fix my laptop','pc problem',
    ))

def _run_pc_diagnostics():
    """Run real system diagnostics. Returns formatted results string."""
    import subprocess as _spd, platform as _pld
    _out = []
    try:
        try:
            import psutil as _psu
        except ImportError:
            import subprocess as _pip_sp, sys as _pip_sys
            _pip_sp.run([_pip_sys.executable, "-m", "pip", "install", "psutil", "-q"], capture_output=True)
            import psutil as _psu
        _cpu = _psu.cpu_percent(interval=1)
        _mem = _psu.virtual_memory()
        _disk = _psu.disk_usage('C:\\' if _pld.system() == 'Windows' else '/')
        _out.append(f"CPU Usage: {_cpu}%")
        _out.append(f"RAM: {_mem.percent}% used ({_mem.used//(1024**3)}GB of {_mem.total//(1024**3)}GB)")
        _out.append(f"Disk C: {_disk.percent}% used ({_disk.used//(1024**3)}GB of {_disk.total//(1024**3)}GB)")
        _procs = []
        for _p in _psu.process_iter(['name','cpu_percent','memory_percent']):
            try:
                _procs.append((_p.info.get('cpu_percent',0), _p.info.get('name',''), _p.info.get('memory_percent',0)))
            except Exception:
                continue
        _procs.sort(reverse=True)
        _top = "\n".join(f"  {n}: CPU {c:.1f}% RAM {m:.1f}%" for c,n,m in _procs[:6] if n)
        _out.append(f"Top processes:\n{_top}")
    except Exception:
        pass
    try:
        _r = _spd.run(['ipconfig'], capture_output=True, timeout=5, encoding='utf-8', errors='replace')
        _iplines = [l for l in _r.stdout.split('\n') if any(x in l for x in ['IPv4','Gateway','DNS','Adapter','Wi-Fi','Ethernet'])]
        if _iplines:
            _out.append("Network:\n" + "\n".join(_iplines[:8]))
    except Exception:
        pass
    return "\n\n".join(_out) if _out else ""

# ── System Health Diagram ──────────────────────────────────────────────────────
def _run_system_health():
    """Collect detailed hardware health data."""
    import platform as _pl
    _d = {
        'cpu_percent': 0, 'cpu_temp': None, 'cpu_cores': 1,
        'cpu_name': _pl.processor() or 'Unknown CPU',
        'ram_percent': 0, 'ram_used_gb': 0, 'ram_total_gb': 0,
        'disk_percent': 0, 'disk_used_gb': 0, 'disk_total_gb': 0, 'disk_status': 'OK',
        'battery_percent': None, 'battery_plugged': None,
        'gpu_name': None, 'gpu_temp': None,
        'os': _pl.system(), 'machine': _pl.node(),
        'laptop_model': 'Unknown',
    }
    try:
        try:
            import psutil as _psu
        except ImportError:
            import subprocess as _s, sys as _sy
            _s.run([_sy.executable, "-m", "pip", "install", "psutil", "-q"], capture_output=True)
            import psutil as _psu
        _d['cpu_percent'] = _psu.cpu_percent(interval=1)
        _d['cpu_cores'] = _psu.cpu_count(logical=False) or 1
        try:
            _temps = _psu.sensors_temperatures()
            if _temps:
                for _k in ('coretemp', 'cpu_thermal', 'k10temp', 'acpitz', 'it8'):
                    if _k in _temps and _temps[_k]:
                        _d['cpu_temp'] = _temps[_k][0].current
                        break
        except Exception:
            pass
        _mem = _psu.virtual_memory()
        _d['ram_percent'] = _mem.percent
        _d['ram_used_gb'] = round(_mem.used / (1024**3), 1)
        _d['ram_total_gb'] = round(_mem.total / (1024**3), 1)
        _dp = 'C:\\' if _pl.system() == 'Windows' else '/'
        _disk = _psu.disk_usage(_dp)
        _d['disk_percent'] = _disk.percent
        _d['disk_used_gb'] = round(_disk.used / (1024**3), 1)
        _d['disk_total_gb'] = round(_disk.total / (1024**3), 1)
        _bat = _psu.battery()
        if _bat:
            _d['battery_percent'] = round(_bat.percent, 1)
            _d['battery_plugged'] = _bat.power_plugged
    except Exception:
        pass
    try:
        import subprocess as _sm
        _mr = _sm.run(['wmic', 'computersystem', 'get', 'model'], capture_output=True, text=True, timeout=5)
        _lines = [l.strip() for l in _mr.stdout.splitlines() if l.strip() and l.strip().lower() != 'model']
        if _lines:
            _d['laptop_model'] = _lines[0]
    except Exception:
        pass
    try:
        import subprocess as _sc
        _cr = _sc.run(['wmic', 'cpu', 'get', 'name'], capture_output=True, text=True, timeout=5)
        _clines = [l.strip() for l in _cr.stdout.splitlines() if l.strip() and l.strip().lower() != 'name']
        if _clines:
            _d['cpu_name'] = _clines[0]
    except Exception:
        pass
    try:
        import subprocess as _sg
        _r = _sg.run(['nvidia-smi', '--query-gpu=name,temperature.gpu',
                      '--format=csv,noheader,nounits'], capture_output=True, text=True, timeout=5)
        if _r.returncode == 0 and _r.stdout.strip():
            _pts = _r.stdout.strip().split(',')
            if len(_pts) >= 2:
                _d['gpu_name'] = _pts[0].strip()[:14]
                try: _d['gpu_temp'] = float(_pts[1].strip())
                except: pass
    except Exception:
        pass
    try:
        import subprocess as _sw
        _wr = _sw.run(['wmic', 'diskdrive', 'get', 'status'],
                      capture_output=True, text=True, timeout=5)
        if 'Pred Fail' in _wr.stdout or 'Error' in _wr.stdout:
            _d['disk_status'] = 'WARNING'
    except Exception:
        pass
    return _d


def _hcolor(val, lo=70, hi=85, inv=False):
    if val is None: return '#334455'
    if inv: return '#ff3333' if val < 20 else ('#ffaa00' if val < 50 else '#00cc66')
    return '#ff3333' if val >= hi else ('#ffaa00' if val >= lo else '#00cc66')


def _render_system_diagram(d):
    """Generate animated HTML laptop internals health diagram."""
    cc = _hcolor(d['cpu_percent'])
    tc = _hcolor(d.get('cpu_temp'), 70, 88)
    rc = _hcolor(d['ram_percent'])
    dc = '#ff3333' if d['disk_status'] == 'WARNING' else _hcolor(d['disk_percent'])
    bc = _hcolor(d.get('battery_percent'), inv=True)
    gc = _hcolor(d.get('gpu_temp'), 70, 88) if d.get('gpu_name') else '#334455'
    bp = d.get('battery_percent') or 0
    bw = min(int(bp * 1.18), 149)
    plug = '🔌 Charging' if d.get('battery_plugged') else '🔋 On Battery'
    issues, fixes = [], []
    if d['cpu_percent'] >= 85:
        issues.append(f"CPU overloaded ({d['cpu_percent']}%)")
        fixes.append("Close heavy background apps or processes")
    elif d['cpu_percent'] >= 70:
        issues.append(f"CPU usage high ({d['cpu_percent']}%)")
        fixes.append("Monitor running apps")
    if d.get('cpu_temp') and d['cpu_temp'] >= 88:
        issues.append(f"CPU dangerously hot ({d['cpu_temp']:.0f}°C)")
        fixes.append("Clean cooling fan, reapply thermal paste, improve ventilation")
    elif d.get('cpu_temp') and d['cpu_temp'] >= 70:
        issues.append(f"CPU running warm ({d['cpu_temp']:.0f}°C)")
        fixes.append("Check ventilation, clean dust from vents")
    if d['ram_percent'] >= 85:
        issues.append(f"RAM nearly full ({d['ram_percent']}%)")
        fixes.append("Close unused apps or upgrade RAM capacity")
    elif d['ram_percent'] >= 70:
        issues.append(f"RAM usage high ({d['ram_percent']}%)")
        fixes.append("Close unused tabs and apps")
    if d['disk_percent'] >= 85:
        issues.append(f"Disk almost full ({d['disk_percent']}%)")
        fixes.append("Delete unused files or move data to external drive")
    if d['disk_status'] == 'WARNING':
        issues.append("Disk health warning — drive may fail")
        fixes.append("Back up all data immediately, replace the drive soon")
    if d.get('battery_percent') is not None and d['battery_percent'] < 20 and not d.get('battery_plugged'):
        issues.append(f"Battery critically low ({d['battery_percent']}%)")
        fixes.append("Plug in charger now")
    if not issues:
        diag_html = '<p style="color:#00cc66;font-weight:bold;margin:4px 0">✅ All components healthy — no damage or issues found</p>'
    else:
        rows = ''.join(
            f'<tr><td style="color:#ff6060;padding:3px 10px 3px 0">⚠ {iss}</td>'
            f'<td style="color:#88ccff;padding:3px 0">→ {fixes[fi] if fi < len(fixes) else "monitor"}</td></tr>'
            for fi, iss in enumerate(issues)
        )
        diag_html = f'<table style="width:100%;font-size:12px;border-collapse:collapse;color:#eee">{rows}</table>'
    gpu_lbl = d.get('gpu_name', 'GPU N/A')
    cpu_temp_lbl = f"{d['cpu_temp']:.0f}°C" if d.get('cpu_temp') else 'Temp N/A'
    cpu_name_short = (d.get('cpu_name') or 'CPU')[:22]
    laptop_model_lbl = (d.get('laptop_model') or d['machine'])[:28]
    return f"""<!DOCTYPE html>
<html><head>
<style>
body{{margin:0;background:#070d1a;font-family:'Courier New',monospace;color:#ccc;overflow:hidden}}
@keyframes spin{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.3}}}}
.fan{{animation:spin 1.8s linear infinite;transform-origin:50% 50%}}
.warn{{animation:pulse 1s ease-in-out infinite}}
</style>
</head><body>
<svg width="640" height="345" viewBox="0 0 640 345">
  <rect x="10" y="10" width="620" height="325" rx="10" fill="#080e1c" stroke="#1e2d45" stroke-width="2"/>
  <g stroke="#111c2e" stroke-width="0.5">
    <line x1="10" y1="75" x2="630" y2="75"/>
    <line x1="10" y1="200" x2="630" y2="200"/>
    <line x1="10" y1="285" x2="630" y2="285"/>
    <line x1="215" y1="10" x2="215" y2="335"/>
    <line x1="430" y1="10" x2="430" y2="335"/>
  </g>
  <text x="18" y="22" fill="#40E0D0" font-size="9" font-weight="bold">🖥 {laptop_model_lbl}</text>
  <text x="18" y="34" fill="#1e2d45" font-size="7">TITAN ULTRA · SYSTEM HEALTH BOARD · {d['machine']}</text>

  <!-- CPU -->
  <rect x="25" y="42" width="170" height="145" rx="6" fill="#0a111e" stroke="{cc}" stroke-width="2.5" class="{'warn' if d['cpu_percent']>=85 else ''}"/>
  <rect x="40" y="56" width="140" height="116" rx="4" fill="#0d1525" stroke="{cc}" stroke-width="1" opacity="0.5"/>
  <rect x="65" y="72" width="90" height="74" rx="3" fill="#0f1e30" stroke="{cc}" stroke-width="1.5"/>
  <text x="110" y="95" text-anchor="middle" fill="{cc}" font-size="11" font-weight="bold">CPU {d['cpu_percent']}%</text>
  <text x="110" y="110" text-anchor="middle" fill="{tc}" font-size="9">{cpu_temp_lbl}</text>
  <text x="110" y="125" text-anchor="middle" fill="{cc}" font-size="7">{cpu_name_short}</text>
  <text x="110" y="138" text-anchor="middle" fill="#445" font-size="7">{d['cpu_cores']} cores</text>
  {''.join(f'<rect x="{25+i*12}" y="173" width="8" height="6" rx="1" fill="{cc}" opacity="0.4"/>' for i in range(14))}
  <text x="110" y="188" text-anchor="middle" fill="#334" font-size="7">CPU SOCKET</text>

  <!-- RAM -->
  <rect x="235" y="22" width="32" height="155" rx="3" fill="#0a111e" stroke="{rc}" stroke-width="2"/>
  <rect x="241" y="29" width="20" height="141" rx="2" fill="#0a1a10" opacity="0.6"/>
  <text x="251" y="105" text-anchor="middle" fill="{rc}" font-size="7" transform="rotate(-90,251,105)">RAM SLOT 1</text>
  <rect x="280" y="22" width="32" height="155" rx="3" fill="#0a111e" stroke="{rc}" stroke-width="2"/>
  <rect x="286" y="29" width="20" height="141" rx="2" fill="#0a1a10" opacity="0.6"/>
  <text x="296" y="105" text-anchor="middle" fill="{rc}" font-size="7" transform="rotate(-90,296,105)">RAM SLOT 2</text>
  <text x="263" y="190" text-anchor="middle" fill="{rc}" font-size="10" font-weight="bold">RAM {d['ram_percent']}%</text>
  <text x="263" y="202" text-anchor="middle" fill="{rc}" font-size="8">{d['ram_used_gb']}GB / {d['ram_total_gb']}GB</text>

  <!-- GPU -->
  <rect x="450" y="22" width="170" height="115" rx="6" fill="#0a0e1a" stroke="{gc}" stroke-width="2.5" class="{'warn' if d.get('gpu_temp') and d['gpu_temp']>=88 else ''}"/>
  <rect x="461" y="32" width="148" height="95" rx="4" fill="#0d0f20" opacity="0.5"/>
  <circle cx="500" cy="80" r="28" fill="#080810" stroke="{gc}" stroke-width="1.5" opacity="0.4"/>
  <circle cx="500" cy="80" r="14" fill="none" stroke="{gc}" stroke-width="2" opacity="0.7"/>
  <circle cx="558" cy="80" r="28" fill="#080810" stroke="{gc}" stroke-width="1.5" opacity="0.4"/>
  <circle cx="558" cy="80" r="14" fill="none" stroke="{gc}" stroke-width="2" opacity="0.7"/>
  <text x="530" y="133" text-anchor="middle" fill="{gc}" font-size="9">{gpu_lbl}</text>
  <text x="530" y="145" text-anchor="middle" fill="#334" font-size="7">GRAPHICS</text>

  <!-- SSD -->
  <rect x="25" y="213" width="170" height="58" rx="4" fill="#0a111e" stroke="{dc}" stroke-width="2.5" class="{'warn' if d['disk_status']=='WARNING' else ''}"/>
  <rect x="35" y="221" width="150" height="42" rx="3" fill="#12110a" opacity="0.5"/>
  <rect x="42" y="227" width="38" height="24" rx="2" fill="#1a1608" stroke="{dc}" stroke-width="1" opacity="0.7"/>
  <rect x="90" y="227" width="38" height="24" rx="2" fill="#1a1608" stroke="{dc}" stroke-width="1" opacity="0.7"/>
  <rect x="138" y="227" width="38" height="24" rx="2" fill="#1a1608" stroke="{dc}" stroke-width="1" opacity="0.7"/>
  <text x="110" y="265" text-anchor="middle" fill="{dc}" font-size="10" font-weight="bold">SSD {d['disk_percent']}% · {d['disk_used_gb']}G/{d['disk_total_gb']}G</text>
  <text x="110" y="290" text-anchor="middle" fill="#334" font-size="7">STORAGE</text>

  <!-- Battery -->
  <rect x="450" y="168" width="170" height="62" rx="4" fill="#0a0f14" stroke="{bc}" stroke-width="2.5"/>
  <rect x="620" y="184" width="10" height="22" rx="3" fill="{bc}" opacity="0.8"/>
  <rect x="458" y="176" width="154" height="46" rx="3" fill="#06080e"/>
  <rect x="460" y="178" width="{bw}" height="42" rx="2" fill="{bc}" opacity="0.6"/>
  <text x="535" y="204" text-anchor="middle" fill="{bc}" font-size="14" font-weight="bold">{bp:.0f}%</text>
  <text x="535" y="220" text-anchor="middle" fill="{bc}" font-size="9">{plug}</text>
  <text x="535" y="244" text-anchor="middle" fill="#334" font-size="7">BATTERY</text>

  <!-- Cooling Fan -->
  <g transform="translate(355,258)">
    <circle r="48" fill="#07101c" stroke="#1a2a40" stroke-width="2"/>
    <circle r="38" fill="none" stroke="#10202e" stroke-width="11"/>
    <g class="fan">
      <ellipse rx="7" ry="20" transform="rotate(0)"   fill="#182840" stroke="#253850" stroke-width="0.5"/>
      <ellipse rx="7" ry="20" transform="rotate(72)"  fill="#182840" stroke="#253850" stroke-width="0.5"/>
      <ellipse rx="7" ry="20" transform="rotate(144)" fill="#182840" stroke="#253850" stroke-width="0.5"/>
      <ellipse rx="7" ry="20" transform="rotate(216)" fill="#182840" stroke="#253850" stroke-width="0.5"/>
      <ellipse rx="7" ry="20" transform="rotate(288)" fill="#182840" stroke="#253850" stroke-width="0.5"/>
    </g>
    <circle r="9" fill="#0a1020" stroke="#253850" stroke-width="2"/>
    <circle r="3" fill="#1e3048"/>
  </g>
  <text x="355" y="318" text-anchor="middle" fill="#334" font-size="7">COOLING FAN</text>

  <!-- Legend -->
  <rect x="18" y="291" width="9" height="9" rx="2" fill="#00cc66"/>
  <text x="30" y="299" fill="#667" font-size="7">Healthy</text>
  <rect x="74" y="291" width="9" height="9" rx="2" fill="#ffaa00"/>
  <text x="86" y="299" fill="#667" font-size="7">Warning</text>
  <rect x="138" y="291" width="9" height="9" rx="2" fill="#ff3333"/>
  <text x="150" y="299" fill="#667" font-size="7">Critical</text>
</svg>
<div style="background:#06080f;border-top:1px solid #1a2840;padding:10px 14px">
  <div style="font-size:11px;font-weight:bold;color:#a78bfa;margin-bottom:6px;letter-spacing:1px">⚡ DIAGNOSIS &amp; FIX</div>
  {diag_html}
</div>
</body></html>"""


def _is_system_health_request(text):
    t = text.lower()
    return any(k in t for k in (
        'check my system', 'check system', 'system health', 'system check',
        'check hardware', 'hardware health', 'system scan', 'scan my system',
        'check my pc', 'pc health', 'laptop health', 'show my laptop',
        'check inside', 'inside system', 'inside my laptop', 'laptop internals',
        'check my laptop', 'system damage', 'any damage', 'damage in system',
        'damage in my', 'check for damage', 'show damage', 'show system',
        'hardware check', 'laptop check', 'computer health', 'cpu temperature',
        'check temperature', 'check ram', 'check storage', 'check battery',
        'show my pc', 'show my computer', 'inside of my pc', 'inside of my laptop',
        'pc internals', 'computer internals', 'inside my computer', 'inside my pc',
        'show pc inside', 'pc inside', 'laptop inside', 'inside part',
        'scan system', 'scan pc', 'scan laptop', 'scan computer',
        'check my computer', 'check inside my', 'show inside', 'view inside',
        'what is inside my', 'what inside my', 'how is my system',
        'how is my pc', 'how is my laptop', 'how is my computer',
        'is my pc ok', 'is my laptop ok', 'is my system ok',
        'any errors in my system', 'any errors in my pc', 'error in system',
        'diagram of my', 'show a diagram of my', 'show diagram of my',
        'system diagram', 'pc diagram', 'laptop diagram', 'inside diagram',
        'show my system', 'show my pc health', 'show my laptop health',
        'my system status', 'my pc status', 'my laptop status',
        'how much ram', 'how many ram', 'my ram', 'total ram', 'ram size',
        'how many cpu', 'cpu cores', 'my cpu', 'my processor', 'cpu model',
        'my laptop name', 'laptop name', 'laptop model', 'computer model', 'pc model',
        'my pc name', 'my computer name', 'name of my laptop', 'name of my pc',
        'what laptop', 'what pc', 'which laptop', 'which pc',
        'disk space', 'storage space', 'free space', 'how much storage',
    ))


# ── Error auto-fix ─────────────────────────────────────────────────────────────
def _is_error_report(text):
    t = text.lower()
    return any(k in t for k in (
        'traceback','exception','error:','syntaxerror','typeerror','valueerror',
        'nameerror','attributeerror','importerror','runtimeerror','indexerror',
        'keyerror','oserror','filenotfounderror','permissionerror','zerodivisionerror',
        'cannot read','undefined is not','uncaught','unhandled','failed with',
        'exit code 1','exit code -1','errno','segmentation fault',
        'access denied','null pointer','nullpointerexception','npe',
        'fix this error','fix the error','solve this error','what does this error',
        'help with error','error in my code','why is this error',
    ))

def _get_error_search(text):
    """Web-search for an error message and return solutions."""
    import re as _re_e
    _err_match = _re_e.search(
        r'((?:Traceback|Error|Exception|Warning)[^\n]{0,120})', text, _re_e.IGNORECASE)
    _query = _err_match.group(1).strip() if _err_match else text[:120]
    return _web_search(f"{_query} solution fix python", max_results=4)

# ── Teach Me detection ─────────────────────────────────────────────────────────
def _is_teach_request(text):
    t = text.lower()
    return any(k in t for k in (
        'teach me','i want to learn','help me learn','explain to me step by step',
        'i am a beginner','i am new to','learn about','how do i start learning',
        'tutor me','be my tutor','act as my teacher','quiz me on',
        'test my knowledge','ask me questions','check if i understood',
    ))

# ── Morning briefing detection ─────────────────────────────────────────────────
def _is_morning_briefing(text):
    t = text.lower()
    return any(k in t for k in (
        'morning briefing','good morning','start my day','morning news',
        'what happened today','today\'s news','daily briefing','morning update',
        'what\'s new today','news today','daily digest',
    ))

# ── Screen capture detection ───────────────────────────────────────────────────
def _is_screen_capture_request(text):
    t = text.lower()
    return any(k in t for k in (
        'take a screenshot','take screenshot','capture my screen','capture screen',
        'analyze my screen','look at my screen','see my screen','read my screen',
        'what\'s on my screen','what is on my screen','check my screen',
        'screenshot','screen capture',
    ))

def _capture_screenshot():
    """Take a screenshot and return vision dict or None."""
    try:
        try:
            import mss as _mss_lib
        except ImportError:
            import subprocess as _mss_sp, sys as _mss_sys
            _mss_sp.run([_mss_sys.executable, "-m", "pip", "install", "mss", "-q"], capture_output=True)
            import mss as _mss_lib
        import io as _sc_io, base64 as _sc_b64
        from PIL import Image as _sc_PIL
        with _mss_lib.mss() as _sct:
            _shot = _sct.grab(_sct.monitors[0])
            _img = _sc_PIL.frombytes("RGB", _shot.size, _shot.bgra, "raw", "BGRX")
            _img.thumbnail((1280, 720), _sc_PIL.LANCZOS)
            _buf = _sc_io.BytesIO()
            _img.save(_buf, format="JPEG", quality=80)
            _raw = _buf.getvalue()
        return {
            "name": "screenshot.jpg", "mime": "image/jpeg",
            "b64": _sc_b64.b64encode(_raw).decode("ascii"), "bytes": _raw,
        }
    except Exception:
        return None

# ── Export chat PDF detection ──────────────────────────────────────────────────
def _is_export_chat_request(text):
    t = text.lower()
    return any(k in t for k in (
        'export chat','save chat','download chat','export conversation',
        'save conversation','chat as pdf','save as pdf','export as pdf',
        'download as pdf','export this chat','save this chat',
    ))

def _build_chat_pdf(msgs):
    """Build PDF bytes from chat messages. Returns bytes or None."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        import io as _pdf_io, re as _pdf_re
        _buf = _pdf_io.BytesIO()
        _doc = SimpleDocTemplate(_buf, pagesize=A4,
                                 leftMargin=2*cm, rightMargin=2*cm,
                                 topMargin=2*cm, bottomMargin=2*cm)
        _t_style = ParagraphStyle('TT', fontSize=15, fontName='Helvetica-Bold',
                                  spaceAfter=12, textColor=colors.HexColor('#0077b6'))
        _u_style = ParagraphStyle('US', fontSize=10, fontName='Helvetica-Bold',
                                  spaceAfter=4, textColor=colors.HexColor('#1a1a2e'))
        _a_style = ParagraphStyle('AS', fontSize=10, fontName='Helvetica',
                                  spaceAfter=8, textColor=colors.HexColor('#1a1a1a'))
        _story = [Paragraph("TITAN ULTRA — Chat Export", _t_style), Spacer(1, 0.3*cm)]
        for _m in msgs:
            _role = "You" if _m["role"] == "user" else "TITAN ULTRA"
            _txt = _pdf_re.sub(r'<[^>]+>', '', str(_m.get("content", "")))
            _txt = _pdf_re.sub(r'[*_`#]', '', _txt)
            _txt = _txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')[:3000]
            _s = _u_style if _m["role"] == "user" else _a_style
            _story.append(Paragraph(f"<b>{_role}:</b> {_txt}", _s))
            _story.append(Spacer(1, 0.2*cm))
        _doc.build(_story)
        _buf.seek(0)
        return _buf.getvalue()
    except Exception:
        return None

# ── Grammar request detection ─────────────────────────────────────────────────
def _is_grammar_request(text):
    t = text.lower()
    return any(k in t for k in (
        'check grammar','fix grammar','correct grammar','grammar check',
        'check my grammar','fix my grammar','proofread','proof read',
        'check spelling','fix spelling','correct spelling',
        'check this text','fix this text','correct this text',
        'check this essay','fix this essay','improve my writing',
        'check this sentence','fix this sentence','correct this',
        'grammar police','find errors','find mistakes','edit this',
        'is this correct english','check this paragraph',
    ))

# ── Story request detection ────────────────────────────────────────────────────
def _is_story_request(text):
    t = text.lower()
    return any(k in t for k in (
        'write a story','tell a story','write me a story','write a short story',
        'write a tale','write a poem','write a narrative','write a novel',
        'write a horror','write a romance','write a thriller','write a mystery',
        'write a fantasy','write a sci-fi','write a comedy','write an adventure',
        'once upon a time','story about','story of','create a story',
        'make a story','generate a story','write fiction','write a fable',
        'write a legend','write a myth','write a folktale',
    ))



# ── PC Control ────────────────────────────────────────────────────────────────
def pc_execute(command):
    import subprocess as _sp, os as _os, ctypes as _ct
    cmd, low = command.strip(), command.lower()

    # ── helpers ──────────────────────────────────────────────────────────────
    def _open(target):
        try: _os.startfile(target); return
        except Exception: pass
        try: _sp.Popen(f'start "" "{target}"', shell=True, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
        except Exception: pass

    def _open_url(url):
        import webbrowser as _wb
        try: _wb.open(url); return
        except Exception: pass
        _sp.Popen(f'start "" "{url}"', shell=True, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)

    def _ps(script):
        _sp.Popen(['powershell.exe', '-WindowStyle', 'Hidden', '-Command', script],
                  stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)

    def _key(vk):
        _ct.windll.user32.keybd_event(vk, 0, 0, 0)
        _ct.windll.user32.keybd_event(vk, 0, 2, 0)

    def _try_app(paths, app_name=None):
        import glob as _glob
        expanded = []
        for p in paths:
            if '*' in p:
                expanded.extend(sorted(_glob.glob(p), reverse=True))
            else:
                expanded.append(p)
        for p in expanded:
            if not p: continue
            # URI scheme (e.g. whatsapp:, ms-photos:) — let ShellExecute try
            if ':' in p and not _os.path.isabs(p):
                try: _os.startfile(p); return True
                except Exception: continue
            # Absolute path — only if it actually exists
            if _os.path.isabs(p):
                if not _os.path.exists(p): continue
                try: _os.startfile(p); return True
                except Exception:
                    try:
                        _sp.Popen(f'start "" "{p}"', shell=True,
                                  stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
                        return True
                    except Exception: continue
            # Bare exe name — verify it's actually on PATH
            try:
                _r = _sp.run(['where', p], capture_output=True, text=True,
                             shell=False, timeout=3)
                if _r.returncode == 0 and _r.stdout.strip():
                    try: _os.startfile(p); return True
                    except Exception:
                        _sp.Popen(f'start "" "{p}"', shell=True,
                                  stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
                        return True
            except Exception: continue

        # Last resort: search Start Menu shortcuts by display name
        if app_name:
            needle = app_name.lower()
            _smdirs = [
                _os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs'),
                _os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs'),
            ]
            _best, _best_score = None, -1
            for _d in _smdirs:
                if not _os.path.isdir(_d): continue
                for _lnk in _glob.glob(_os.path.join(_d, '**', '*.lnk'), recursive=True):
                    _nm = _os.path.splitext(_os.path.basename(_lnk))[0].lower()
                    if _nm == needle: _score = 100
                    elif needle in _nm: _score = 80 - abs(len(_nm) - len(needle))
                    elif all(t in _nm for t in needle.split()): _score = 50 - abs(len(_nm) - len(needle))
                    else: continue
                    if _score > _best_score: _best, _best_score = _lnk, _score
            if _best:
                try: _os.startfile(_best); return True
                except Exception: pass
        return False

    # ── Volume controls ───────────────────────────────────────────────────────
    VK_VOL_MUTE = 0xAD; VK_VOL_DOWN = 0xAE; VK_VOL_UP = 0xAF
    if any(x in low for x in ('mute', 'unmute', 'silence')):
        _key(VK_VOL_MUTE); return '🔇 Volume muted / unmuted'

    if 'volume' in low or 'louder' in low or 'quieter' in low or 'turn up' in low or 'turn down' in low:
        _is_up = any(w in low for w in ('up','increase','raise','higher','more','louder','turn up','max','full'))
        _is_down = any(w in low for w in ('down','decrease','lower','reduce','less','quieter','turn down','min','mute'))
        _set_kw = ('set' in low) or (' to ' in low) or ('%' in low)
        _step_m = re.search(r'by\s+(\d+)', low)
        _num_m = re.search(r'(\d+)', low)

        if 'max' in low or 'maximum' in low or 'full' in low:
            for _ in range(50): _key(VK_VOL_UP)
            return '🔊 Volume → 100%'
        if 'min' in low or 'minimum' in low:
            for _ in range(50): _key(VK_VOL_DOWN)
            return '🔇 Volume → 0%'
        if _set_kw and _num_m:
            pct = max(0, min(100, int(_num_m.group(1))))
            for _ in range(50): _key(VK_VOL_DOWN)
            for _ in range((pct + 1) // 2): _key(VK_VOL_UP)
            return f'🔊 Volume set to {pct}%'
        if _is_up:
            step = int(_step_m.group(1)) if _step_m else (int(_num_m.group(1)) if _num_m else 10)
            step = max(1, min(100, step))
            for _ in range(max(1, (step + 1) // 2)): _key(VK_VOL_UP)
            return f'🔊 Volume up by {step}%'
        if _is_down:
            step = int(_step_m.group(1)) if _step_m else (int(_num_m.group(1)) if _num_m else 10)
            step = max(1, min(100, step))
            for _ in range(max(1, (step + 1) // 2)): _key(VK_VOL_DOWN)
            return f'🔉 Volume down by {step}%'
        if _num_m:
            pct = max(0, min(100, int(_num_m.group(1))))
            for _ in range(50): _key(VK_VOL_DOWN)
            for _ in range((pct + 1) // 2): _key(VK_VOL_UP)
            return f'🔊 Volume set to {pct}%'
        return '🔊 Say "increase volume by 20" or "set volume to 50".'

    # ── Media keys ────────────────────────────────────────────────────────────
    VK_MEDIA_PLAY = 0xB3; VK_MEDIA_NEXT = 0xB0; VK_MEDIA_PREV = 0xB1; VK_MEDIA_STOP = 0xB2
    if any(x in low for x in ('play', 'pause', 'resume')) and any(x in low for x in ('music','song','media','video','spotify')):
        _key(VK_MEDIA_PLAY); return '⏯️ Play/Pause toggled'
    if 'next song' in low or 'next track' in low or 'skip song' in low:
        _key(VK_MEDIA_NEXT); return '⏭️ Next track'
    if 'previous song' in low or 'prev song' in low or 'last track' in low:
        _key(VK_MEDIA_PREV); return '⏮️ Previous track'
    if 'stop music' in low or 'stop song' in low:
        _key(VK_MEDIA_STOP); return '⏹️ Music stopped'

    # ── Screenshot ────────────────────────────────────────────────────────────
    if 'screenshot' in low or 'screen capture' in low or 'snip' in low:
        if 'snip' in low or 'tool' in low:
            _open('ms-screensketch:'); return '✂️ Opened Snipping Tool'
        _key(0x2C); return '📸 Screenshot taken (saved to clipboard)'

    # ── Brightness ────────────────────────────────────────────────────────────
    if 'brightness' in low or 'brighter' in low or 'dimmer' in low or 'dim ' in low:
        _is_up = any(w in low for w in ('increase','raise','higher','more','up','brighter','max','full'))
        _is_down = any(w in low for w in ('decrease','lower','reduce','less','down','dim','dimmer','min'))
        _set_kw = ('set' in low) or (' to ' in low) or ('%' in low)
        _step_m = re.search(r'by\s+(\d+)', low)
        _num_m = re.search(r'(\d+)', low)

        try:
            _cur_raw = _sp.check_output(
                ['powershell','-NoProfile','-Command',
                 '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'],
                stderr=_sp.DEVNULL, timeout=5
            ).decode().strip().splitlines()
            _cur = int(_cur_raw[0]) if _cur_raw and _cur_raw[0].isdigit() else 50
        except Exception:
            _cur = 50

        if 'max' in low or 'maximum' in low or 'full' in low:
            lvl = 100
        elif 'min' in low or 'minimum' in low:
            lvl = 10
        elif _set_kw and _num_m:
            lvl = int(_num_m.group(1))
        elif _is_up:
            step = int(_step_m.group(1)) if _step_m else (int(_num_m.group(1)) if _num_m else 20)
            lvl = _cur + step
        elif _is_down:
            step = int(_step_m.group(1)) if _step_m else (int(_num_m.group(1)) if _num_m else 20)
            lvl = _cur - step
        elif _num_m:
            lvl = int(_num_m.group(1))
        else:
            return f'☀️ Brightness is at {_cur}%. Say "increase brightness" or "decrease brightness".'

        lvl = max(0, min(100, lvl))
        _ps(f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{lvl})")
        _arrow = "🔆" if lvl > _cur else ("🔅" if lvl < _cur else "☀️")
        return f'{_arrow} Brightness {_cur}% → {lvl}%'

    # ── URLs ──────────────────────────────────────────────────────────────────
    if re.search(r'https?://', cmd):
        url = re.search(r'https?://\S+', cmd).group()
        _open_url(url); return f'✅ Opened {url}'

    # ── YouTube ───────────────────────────────────────────────────────────────
    if 'youtube' in low:
        m = re.search(r'(?:search|play|watch|find|open youtube (?:and )?(?:search|play|watch)?)\s+(.+?)(?:\s+on\s+youtube)?$', low)
        if not m: m = re.search(r'youtube\s+(.+)', low)
        q = m.group(1).strip() if m else ''
        q = re.sub(r'^(and\s+|for\s+|search\s+|play\s+)', '', q).strip()
        url = f'https://www.youtube.com/results?search_query={q.replace(" ","+")}' if q else 'https://www.youtube.com'
        _open_url(url); return f'✅ Opened YouTube' + (f' — searching "{q}"' if q else '')

    # ── Chrome with specific search query ────────────────────────────────────
    if 'chrome' in low and any(x in low for x in ('search', 'type', 'go to', 'visit', 'open url')):
        m = re.search(r'(?:search|type|go to|visit|open url)\s+(?:for\s+)?(.+?)(?:\s+(?:in|on|with)\s+chrome)?$', low)
        q = m.group(1).strip() if m else ''
        q = re.sub(r'^(and\s+|for\s+)', '', q).strip()
        url = f'https://www.google.com/search?q={q.replace(" ","+")}' if q else 'https://www.google.com'
        _chrome_paths = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ]
        launched = False
        for _cp in _chrome_paths:
            if _os.path.exists(_cp):
                try: _sp.Popen([_cp, url]); launched = True; break
                except Exception: pass
        if not launched:
            _sp.Popen(f'start chrome "{url}"', shell=True, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
        return f'✅ Opened Chrome — searching "{q}"' if q else '✅ Opened Chrome'

    # ── Google / Web search ───────────────────────────────────────────────────
    if 'google' in low or ('search' in low and 'web search' not in low and 'youtube' not in low and 'store' not in low and 'chrome' not in low):
        m = re.search(r'(?:search|google)\s+(?:for\s+)?(.+)', low)
        q = m.group(1).strip() if m else cmd
        _open_url(f'https://www.google.com/search?q={q.replace(" ","+")}')
        return f'✅ Searching Google for "{q}"'

    # ── Microsoft Store + install ─────────────────────────────────────────────
    if 'microsoft store' in low or 'ms store' in low or 'windows store' in low:
        m = re.search(r'(?:search|download|install|find|get)\s+(.+?)(?:\s+(?:in|from|on|at|via)\s+(?:microsoft|windows|ms)\s+store)?$', low)
        if not m: m = re.search(r'store\s+(.+)', low)
        if m:
            q = re.sub(r'\s*(?:microsoft|windows|ms)\s+store\s*', '', m.group(1)).strip()
            q = re.sub(r'\s*(in|from|on|at)\s*$', '', q).strip()
            if any(x in low for x in ('download', 'install', 'get')):
                _sp.Popen(
                    ['powershell.exe', '-NoExit', '-Command',
                     f'Write-Host "Installing {q} from Microsoft Store..." -ForegroundColor Cyan; '
                     f'winget install --name "{q}" --accept-source-agreements --accept-package-agreements; '
                     f'Write-Host "Done! Press any key to close." -ForegroundColor Green']
                )
                return f'✅ Installing "{q}" — check the PowerShell window for progress'
            _open_url(f'ms-windows-store://search/?query={q.replace(" ","+")}')
            return f'✅ Opened Microsoft Store — searching "{q}"'
        _open('ms-windows-store:'); return '✅ Opened Microsoft Store'

    if ('install' in low or 'download' in low) and 'store' not in low:
        m = re.search(r'(?:install|download|get)\s+(.+)', low)
        app = m.group(1).strip() if m else cmd
        _sp.Popen(
            ['powershell.exe', '-NoExit', '-Command',
             f'Write-Host "Installing {app}..." -ForegroundColor Cyan; '
             f'winget install --name "{app}" --accept-source-agreements --accept-package-agreements; '
             f'Write-Host "Done!" -ForegroundColor Green']
        )
        return f'✅ Installing "{app}" — check the PowerShell window for progress'

    # ── Known apps (URI schemes + exe paths) ──────────────────────────────────
    _APPS = {
        # Browsers
        'chrome':           [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                             r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', 'chrome.exe'],
        'firefox':          [r'C:\Program Files\Mozilla Firefox\firefox.exe',
                             r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe', 'firefox.exe'],
        'edge':             [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', 'msedge.exe'],
        'opera':            [_os.path.expandvars(r'%LOCALAPPDATA%\Programs\Opera\launcher.exe'), 'opera.exe'],
        'brave':            [r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
                             _os.path.expandvars(r'%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe'), 'brave.exe'],
        # Windows utilities
        'notepad':          ['notepad.exe'],
        'calculator':       ['calc.exe'],
        'paint':            ['mspaint.exe'],
        'paint 3d':         ['ms-paint:'],
        'task manager':     ['taskmgr.exe'],
        'file explorer':    ['explorer.exe'],
        'files':            ['explorer.exe'],
        'file':             ['explorer.exe'],
        'explorer':         ['explorer.exe'],
        'my files':         ['explorer.exe'],
        'this pc':          ['explorer.exe'],
        'my computer':      ['explorer.exe'],
        'downloads':        [_os.path.expandvars(r'%USERPROFILE%\Downloads')],
        'documents':        [_os.path.expandvars(r'%USERPROFILE%\Documents')],
        'pictures':         [_os.path.expandvars(r'%USERPROFILE%\Pictures')],
        'desktop':          [_os.path.expandvars(r'%USERPROFILE%\Desktop')],
        'videos':           [_os.path.expandvars(r'%USERPROFILE%\Videos')],
        'music':            [_os.path.expandvars(r'%USERPROFILE%\Music')],
        'cmd':              ['cmd.exe'],
        'command prompt':   ['cmd.exe'],
        'terminal':         ['wt.exe', 'cmd.exe'],
        'powershell':       ['powershell.exe'],
        'registry':         ['regedit.exe'],
        'device manager':   ['devmgmt.msc'],
        'disk management':  ['diskmgmt.msc'],
        'event viewer':     ['eventvwr.msc'],
        'services':         ['services.msc'],
        'resource monitor': ['resmon.exe'],
        'performance monitor': ['perfmon.exe'],
        # Settings & system
        'settings':         ['ms-settings:'],
        'wifi':             ['ms-settings:network-wifi'],
        'bluetooth':        ['ms-settings:bluetooth'],
        'display settings': ['ms-settings:display'],
        'sound settings':   ['ms-settings:sound'],
        'apps settings':    ['ms-settings:appsfeatures'],
        'update':           ['ms-settings:windowsupdate'],
        'control panel':    ['control.exe'],
        'action center':    ['ms-actioncenter:'],
        'snipping tool':    ['ms-screensketch:'],
        'snip':             ['ms-screensketch:'],
        # Microsoft Store
        'store':            ['ms-windows-store:'],
        # Office
        'word':             [r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
                             r'C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE', 'winword.exe'],
        'excel':            [r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
                             r'C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE', 'excel.exe'],
        'powerpoint':       [r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
                             r'C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE', 'powerpnt.exe'],
        'outlook':          [r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE', 'outlook.exe'],
        'onenote':          ['onenote:', r'C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE', 'onenote.exe'],
        'access':           [r'C:\Program Files\Microsoft Office\root\Office16\MSACCESS.EXE', 'msaccess.exe'],
        'publisher':        [r'C:\Program Files\Microsoft Office\root\Office16\MSPUB.EXE', 'mspub.exe'],
        'teams':            ['msteams:', _os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Teams\current\Teams.exe'), 'teams.exe'],
        # Media & entertainment
        'vlc':              [r'C:\Program Files\VideoLAN\VLC\vlc.exe',
                             r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe', 'vlc.exe'],
        'spotify':          [_os.path.expandvars(r'%APPDATA%\Spotify\Spotify.exe'), 'spotify.exe', 'spotify:'],
        'windows media player': ['wmplayer.exe'],
        'photos':           ['ms-photos:'],
        'camera':           ['microsoft.windows.camera:'],
        'movies':           ['mswindowsvideo:'],
        'xbox':             ['xbox:'],
        'xbox game bar':    ['ms-gamingoverlay:'],
        # Communication
        'whatsapp':         ['whatsapp:',
                             _os.path.expandvars(r'%LOCALAPPDATA%\Packages\*WhatsApp*\WhatsApp.exe'),
                             _os.path.expandvars(r'%LOCALAPPDATA%\WhatsApp\WhatsApp.exe'),
                             _os.path.expandvars(r'%APPDATA%\WhatsApp\WhatsApp.exe'),
                             'whatsapp.exe'],
        'telegram':         [_os.path.expandvars(r'%APPDATA%\Telegram Desktop\Telegram.exe'), 'telegram.exe'],
        'discord':          [_os.path.expandvars(r'%LOCALAPPDATA%\Discord\app-*\Discord.exe'),
                             'discord.exe'],
        'skype':            ['skype:', _os.path.expandvars(r'%APPDATA%\Microsoft\Teams\current\Teams.exe'), 'skype.exe'],
        'zoom':             [r'C:\Program Files\Zoom\bin\Zoom.exe',
                             _os.path.expandvars(r'%APPDATA%\Zoom\bin\Zoom.exe'), 'zoom.exe'],
        # Dev tools
        'vs code':          [r'C:\Program Files\Microsoft VS Code\Code.exe',
                             _os.path.expandvars(r'%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe'), 'code.exe'],
        'visual studio':    [r'C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe', 'devenv.exe'],
        'git bash':         [r'C:\Program Files\Git\git-bash.exe', 'git-bash.exe'],
        'android studio':   [_os.path.expandvars(r'%LOCALAPPDATA%\Google\AndroidStudio\bin\studio64.exe'), 'studio64.exe'],
        'jupyter':          ['jupyter.exe'],
        # Productivity
        'clock':            ['ms-clock:'],
        'alarm':            ['ms-clock:'],
        'calendar':         ['outlookcal:', 'ms-outlook:'],
        'mail':             ['outlookmail:', 'ms-outlook:'],
        'maps':             ['bingmaps:'],
        'weather':          ['msnweather:'],
        'news':             ['bingnews:'],
        'sticky notes':     ['ms-stickynotes:'],
        'feedback':         ['feedback-hub:'],
        'narrator':         ['narrator:'],
        # Antivirus & security
        'windows defender': ['windowsdefender:'],
        'security':         ['windowsdefender:'],
        'firewall':         ['wf.msc'],
    }

    # Match dict keys against whole words in the command so e.g. "file" won't
    # match "profile.txt" and "edge" won't match "knowledge". Longest key wins
    # so "file explorer" beats "file" on "open file explorer".
    _best_app, _best_len = None, -1
    for name, paths in _APPS.items():
        if re.search(r'\b' + re.escape(name) + r'\b', low):
            if len(name) > _best_len:
                _best_app, _best_len = (name, paths), len(name)
    if _best_app:
        name, paths = _best_app
        if _try_app(paths, name):
            return f'✅ Opened {name.title()}'
        return f'⚠️ Could not open {name.title()}. Make sure it\'s installed.'

    # ── Shutdown / restart / sleep ────────────────────────────────────────────
    if 'shut down' in low or 'shutdown' in low or 'turn off' in low or 'power off' in low:
        _ps('Stop-Computer -Force'); return '🛑 Shutting down…'
    if 'restart' in low or 'reboot' in low:
        _ps('Restart-Computer -Force'); return '🔄 Restarting…'
    if 'sleep' in low or 'hibernate' in low:
        _ps('Add-Type -Assembly System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState("Suspend",$false,$false)')
        return '💤 Going to sleep…'
    if 'lock' in low and ('screen' in low or 'pc' in low or 'computer' in low):
        _ct.windll.user32.LockWorkStation(); return '🔒 Screen locked'

    # ── Generic "open <something>" ────────────────────────────────────────────
    m = re.search(r'open\s+(.+)', low)
    if m:
        # Use the ORIGINAL-case version from cmd so "IDLE (Python 3.13)" keeps its case
        raw_m = re.search(r'open\s+(.+)', cmd, re.IGNORECASE)
        target = (raw_m.group(1) if raw_m else m.group(1)).strip().rstrip('.?!')
        needle = target.lower()

        # 1) Search Start Menu shortcuts — covers virtually every installed Windows app
        #    (including ones with display names like "IDLE (Python 3.13)")
        import glob as _glob
        _smdirs = [
            _os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs'),
            _os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs'),
        ]
        _best, _best_score = None, -1
        for _d in _smdirs:
            if not _os.path.isdir(_d): continue
            for _lnk in _glob.glob(_os.path.join(_d, '**', '*.lnk'), recursive=True):
                _name = _os.path.splitext(_os.path.basename(_lnk))[0].lower()
                # Score: exact name > full substring match > all-tokens match
                if _name == needle: _score = 100
                elif needle in _name: _score = 80 - abs(len(_name) - len(needle))
                elif all(_tok in _name for _tok in needle.split()): _score = 50 - abs(len(_name) - len(needle))
                else: continue
                if _score > _best_score: _best, _best_score = _lnk, _score
        if _best:
            try: _os.startfile(_best); return f'✅ Opened {_os.path.splitext(_os.path.basename(_best))[0]}'
            except Exception: pass

        # 2) Build name variants: original, strip parentheticals, first word
        #    e.g. "IDLE (Python 3.13)" → ["IDLE (Python 3.13)", "IDLE", "idle"]
        _variants = []
        for _v in (target,
                   re.sub(r'\s*\([^)]*\)', '', target).strip(),
                   target.split()[0] if target.split() else ''):
            if _v and _v not in _variants: _variants.append(_v)

        # 3) Resolve each variant against PATH (covers App Paths + Microsoft Store stubs)
        #    before trying anything — that way we don't falsely claim success.
        def _which(name):
            try:
                r = _sp.run(['where', name], capture_output=True, text=True, shell=False, timeout=3)
                if r.returncode == 0:
                    for ln in r.stdout.splitlines():
                        ln = ln.strip()
                        if ln and _os.path.exists(ln): return ln
            except Exception: pass
            return None

        for _v in _variants:
            _hit = _which(_v) or _which(_v + '.exe')
            if _hit:
                try: _os.startfile(_hit); return f'✅ Opened {_v}'
                except Exception:
                    _sp.Popen(f'start "" "{_hit}"', shell=True, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
                    return f'✅ Opened {_v}'

        # 4) Last resort: maybe target is a URI scheme like "ms-settings:" or an existing file
        if ':' in target or _os.path.exists(target):
            try: _os.startfile(target); return f'✅ Opened "{target}"'
            except Exception: pass

        return f'⚠️ Could not find "{target}". Try the exact app name, or install it first.'

    # ── Raw shell command ─────────────────────────────────────────────────────
    _sp.Popen(cmd, shell=True, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
    return f'✅ Ran: {cmd}'

# ── AI Image & Video Generation ───────────────────────────────────────────────
def _is_image_gen_request(q):
    q = q.lower().strip()
    return any(x in q for x in [
        "generate image", "create image", "make image",
        "generate an image", "create an image", "make an image",
        "generate a image", "create a image",
        "generate photo", "create photo", "make photo",
        "generate a photo", "create a photo", "make a photo",
        "generate picture", "create picture", "make picture",
        "generate a picture", "create a picture",
        "show me a picture of", "show me an image of",
        "generate artwork", "create artwork", "make artwork",
        "draw me", "draw an image", "illustrate this",
        "generate illustration", "create illustration",
        "ai image of", "ai photo of",
    ])

def _is_video_gen_request(q):
    q = q.lower().strip()
    return any(x in q for x in [
        "generate video", "create video", "make video",
        "generate a video", "create a video", "make a video",
        "generate video of", "create video of", "make a video of",
        "ai video", "create ai video", "generate ai video",
        "create animation", "generate animation", "make animation",
        "short video of", "video clip", "generate clip",
        "animate this", "create a clip of",
        "video", "animate", "animation", "zoom", "pan", "cinematic",
    ])

def _parse_video_effect(text):
    import re as _re_ve
    t = text.lower()
    if any(w in t for w in ["ken burns", "cinematic", "film", "movie", "professional", "dramatic"]):
        effect = "ken_burns"
    elif any(w in t for w in ["zoom in", "zooming in", "close up", "closer", "zoom into"]):
        effect = "zoom_in"
    elif any(w in t for w in ["zoom out", "zooming out", "pull back", "pull away", "wider"]):
        effect = "zoom_out"
    elif any(w in t for w in ["pan right", "move right", "left to right", "slide right"]):
        effect = "pan_right"
    elif any(w in t for w in ["pan left", "move left", "right to left", "slide left"]):
        effect = "pan_left"
    elif any(w in t for w in ["pan up", "move up", "bottom to top", "slide up"]):
        effect = "pan_up"
    elif any(w in t for w in ["pan down", "move down", "top to bottom", "slide down"]):
        effect = "pan_down"
    elif any(w in t for w in ["pulse", "breathe", "breathing", "heartbeat"]):
        effect = "pulse"
    elif any(w in t for w in ["fade", "fade in", "appear", "emerge"]):
        effect = "fade_in"
    elif any(w in t for w in ["shake", "vibrate", "shaky", "tremble"]):
        effect = "shake"
    elif any(w in t for w in ["zoom", "slow zoom"]):
        effect = "zoom_in"
    elif any(w in t for w in ["pan", "slide", "scroll", "sweep"]):
        effect = "pan_right"
    else:
        effect = "ken_burns"
    speed = "medium"
    if any(w in t for w in ["slow", "slowly", "gentle", "smooth", "soft"]):
        speed = "slow"
    elif any(w in t for w in ["fast", "quick", "rapid", "dynamic"]):
        speed = "fast"
    duration = 5
    m = _re_ve.search(r'(\d+)\s*sec', t)
    if m:
        duration = min(max(int(m.group(1)), 2), 12)
    zoom = {"slow": 0.22, "medium": 0.32, "fast": 0.45}.get(speed, 0.32)
    return {"effect": effect, "duration": duration, "fps": 10, "zoom": zoom, "speed": speed}

def _create_animated_gif(img_bytes, params):
    from PIL import Image, ImageEnhance
    import io, math
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    if img.width > 640:
        r = 640 / img.width
        img = img.resize((640, int(img.height * r)), Image.LANCZOS)
    effect = params["effect"]
    total_frames = params["duration"] * params["fps"]
    zoom = params.get("zoom", 0.32)
    w, h = img.size
    frames = []
    for i in range(total_frames):
        t = i / max(total_frames - 1, 1)
        if effect == "zoom_in":
            sc = 1 + zoom * t
            nw, nh = int(w / sc), int(h / sc)
            l, tp = (w - nw) // 2, (h - nh) // 2
            frame = img.crop((l, tp, l + nw, tp + nh)).resize((w, h), Image.LANCZOS)
        elif effect == "zoom_out":
            sc = (1 + zoom) - zoom * t
            nw, nh = int(w / sc), int(h / sc)
            l, tp = (w - nw) // 2, (h - nh) // 2
            frame = img.crop((l, tp, l + nw, tp + nh)).resize((w, h), Image.LANCZOS)
        elif effect == "pan_right":
            mg = int(w * 0.22); l = int(mg * t)
            frame = img.crop((l, 0, l + w - mg, h)).resize((w, h), Image.LANCZOS)
        elif effect == "pan_left":
            mg = int(w * 0.22); l = int(mg * (1 - t))
            frame = img.crop((l, 0, l + w - mg, h)).resize((w, h), Image.LANCZOS)
        elif effect == "pan_up":
            mg = int(h * 0.22); tp = int(mg * (1 - t))
            frame = img.crop((0, tp, w, tp + h - mg)).resize((w, h), Image.LANCZOS)
        elif effect == "pan_down":
            mg = int(h * 0.22); tp = int(mg * t)
            frame = img.crop((0, tp, w, tp + h - mg)).resize((w, h), Image.LANCZOS)
        elif effect == "ken_burns":
            sc = 1 + zoom * t
            nw, nh = int(w / sc), int(h / sc)
            px, py = int(w * 0.06 * t), int(h * 0.03 * t)
            l = max(0, min((w - nw) // 2 + px, w - nw))
            tp = max(0, min((h - nh) // 2 + py, h - nh))
            frame = img.crop((l, tp, l + nw, tp + nh)).resize((w, h), Image.LANCZOS)
        elif effect == "pulse":
            sc = 1 + 0.06 * math.sin(t * math.pi * 2)
            nw, nh = int(w / sc), int(h / sc)
            l, tp = (w - nw) // 2, (h - nh) // 2
            frame = img.crop((l, tp, l + nw, tp + nh)).resize((w, h), Image.LANCZOS)
        elif effect == "fade_in":
            sc = 1.2 - 0.2 * t
            nw, nh = int(w / sc), int(h / sc)
            l, tp = (w - nw) // 2, (h - nh) // 2
            frame = img.crop((l, tp, l + nw, tp + nh)).resize((w, h), Image.LANCZOS)
            frame = ImageEnhance.Brightness(frame).enhance(min(1.0, t * 2.5))
        elif effect == "shake":
            import random; random.seed(i)
            pad = 10
            dx, dy = random.randint(-pad, pad), random.randint(-pad, pad)
            l = max(0, min(pad + dx, 2 * pad)); tp = max(0, min(pad + dy, 2 * pad))
            frame = img.crop((l, tp, l + w - 2 * pad, tp + h - 2 * pad)).resize((w, h), Image.LANCZOS)
        else:
            frame = img.copy()
        frames.append(frame.quantize(colors=200, method=Image.Quantize.MEDIANCUT))
    buf = io.BytesIO()
    frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:],
                   duration=int(1000 / params["fps"]), loop=0, optimize=True)
    buf.seek(0)
    return buf.getvalue()

def _create_text_to_video(description, duration=5, fps=10):
    from PIL import Image, ImageDraw, ImageFont
    import io, math, numpy as np, json as _json_tv, re as _re_tv, random as _rnd_v
    W, H = 480, 270
    BAR = 24
    t_low = description.lower()

    _pals = {
        "sunset":      [(255,80,30),(255,150,0),(220,60,90),(255,200,100)],
        "ocean":       [(0,50,150),(0,120,200),(0,200,190),(80,230,220)],
        "forest":      [(20,60,20),(50,110,40),(90,160,70),(160,210,110)],
        "night":       [(8,8,35),(25,15,70),(50,30,110),(90,60,170)],
        "fire":        [(170,10,0),(240,80,0),(255,170,0),(255,230,60)],
        "space":       [(5,5,20),(20,10,50),(40,20,90),(100,60,200)],
        "gold":        [(140,100,0),(200,155,30),(245,200,80),(255,240,160)],
        "rose":        [(170,20,60),(220,60,100),(250,120,150),(255,180,200)],
        "snow":        [(180,210,240),(210,230,250),(235,245,255),(255,255,255)],
        "desert":      [(190,130,50),(230,170,80),(255,205,110),(255,235,170)],
        "sky":         [(80,130,230),(130,180,255),(190,220,255),(230,245,255)],
        "cyber":       [(0,20,40),(0,80,180),(0,200,255),(100,255,255)],
        "purple":      [(30,10,60),(80,20,140),(150,50,200),(200,120,255)],
        "rainbow":     [(255,50,50),(255,180,0),(50,220,50),(50,100,255)],
        "horror":      [(20,0,0),(80,10,10),(160,20,0),(255,60,20)],
        "party":       [(255,50,150),(255,200,0),(50,200,255),(150,50,255)],
        "luxury":      [(20,15,5),(80,60,10),(180,140,30),(255,220,100)],
        "tech":        [(5,15,30),(10,60,100),(20,150,200),(80,220,255)],
        "nature":      [(20,50,10),(60,120,30),(120,180,60),(200,230,120)],
        "calm":        [(100,140,200),(140,180,230),(180,210,245),(220,235,255)],
    }

    # Ask Groq to classify the description into our palette + motion system
    _tv_palette = "night"
    _tv_motion = "wave"
    _tv_speed = 1.0
    try:
        _tv_client = Groq(api_key=_GROQ_KEY)
        _tv_resp = _tv_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":(
                f'Video request: "{description}"\n'
                f'Use your full knowledge of movies, anime, sports, games, and any topic to analyse this. '
                f'Reply ONLY with valid JSON:\n'
                f'{{"palette":"sunset|ocean|forest|night|fire|space|gold|rose|snow|desert|sky|cyber|purple|rainbow|horror|party|luxury|tech|nature|calm",'
                f'"motion":"wave|spin|zoom|fade|diagonal","speed":"slow|medium|fast",'
                f'"scene":"fight|sport|love|space|nature|horror|celebration|default",'
                f'"title":"3-5 word cinematic title for this video",'
                f'"c1":"#RRGGBB hex for main character or object",'
                f'"c2":"#RRGGBB hex for second character or element"}}'
            )}],
            max_tokens=120, temperature=0
        )
        _tv_raw = _tv_resp.choices[0].message.content.strip()
        _tv_json = _json_tv.loads(_re_tv.search(r'\{.*\}', _tv_raw, _re_tv.DOTALL).group())
        _tv_palette = _tv_json.get("palette", "night")
        _tv_motion  = _tv_json.get("motion", "wave")
        _tv_spd_str = _tv_json.get("speed", "medium")
        _tv_speed   = {"slow": 0.5, "medium": 1.0, "fast": 2.0}.get(_tv_spd_str, 1.0)
        _scene      = _tv_json.get("scene", "default")
        _vid_title  = _tv_json.get("title", description[:30])
        def _hx(h):
            h=h.lstrip('#')
            try: return tuple(int(h[i:i+2],16) for i in (0,2,4))
            except: return (255,100,0)
        _c1 = _hx(_tv_json.get("c1","#FF5020"))
        _c2 = _hx(_tv_json.get("c2","#2050FF"))
        if _tv_palette not in _pals: _tv_palette = "night"
        if _tv_motion not in ("wave","spin","zoom","fade","diagonal"): _tv_motion = "wave"
        if _scene not in ("fight","sport","love","space","nature","horror","celebration","default"): _scene = "default"
    except Exception:
        _scene = "default"; _vid_title = description[:30]; _c1=(255,80,30); _c2=(60,100,255)
        _kw_map = [
            (["sunset","orange","warm","golden","dusk","dawn"], "sunset"),
            (["ocean","sea","wave","water","river","lake"], "ocean"),
            (["forest","tree","green","nature","jungle","garden"], "forest"),
            (["night","dark","shadow","mystery","gothic","midnight"], "night"),
            (["fire","flame","lava","burn","blaze","inferno"], "fire"),
            (["space","galaxy","star","cosmos","universe","planet","nebula"], "space"),
            (["gold","luxury","elegant","rich","shine","royal"], "luxury"),
            (["love","heart","romantic","rose","valentine","pink","kiss"], "rose"),
            (["snow","cold","winter","ice","arctic","frost"], "snow"),
            (["desert","sand","dune","dry","heat","mirage"], "desert"),
            (["sky","cloud","bright","sunlight","day"], "sky"),
            (["cyber","digital","tech","neon","futuristic","matrix"], "cyber"),
            (["purple","violet","magic","fantasy","mystic"], "purple"),
            (["horror","scary","blood","ghost","demon","evil","haunted"], "horror"),
            (["party","birthday","celebration","confetti","disco","music"], "party"),
            (["calm","peace","relax","meditation","zen","gentle","serene"], "calm"),
        ]
        for kws, pk in _kw_map:
            if any(w in t_low for w in kws): _tv_palette = pk; break
        if any(w in t_low for w in ["spin","rotate","swirl","vortex"]): _tv_motion = "spin"
        elif any(w in t_low for w in ["zoom","pulse","expand","burst"]): _tv_motion = "zoom"
        elif any(w in t_low for w in ["fade","glow","dissolve"]): _tv_motion = "fade"
        elif any(w in t_low for w in ["diagonal","slant"]): _tv_motion = "diagonal"
        if any(w in t_low for w in ["slow","gentle","calm","peaceful"]): _tv_speed = 0.5
        elif any(w in t_low for w in ["fast","quick","rapid","intense"]): _tv_speed = 2.0
        if any(w in t_low for w in ["fight","battle","vs","versus","combat","war","clash","attack","kills","sword","punch"]): _scene="fight"
        elif any(w in t_low for w in ["football","cricket","basketball","sport","goal","score","ball","player","match","game"]): _scene="sport"
        elif any(w in t_low for w in ["love","romance","heart","valentine","kiss","wedding","couple"]): _scene="love"
        elif any(w in t_low for w in ["space","galaxy","planet","rocket","cosmos","nebula","astronaut"]): _scene="space"
        elif any(w in t_low for w in ["horror","scary","ghost","demon","evil","haunted","blood","death"]): _scene="horror"
        elif any(w in t_low for w in ["birthday","party","celebration","confetti","festival","win","victory"]): _scene="celebration"

    pal = _pals.get(_tv_palette, _pals["night"])
    _dm = _re_tv.search(r'(\d+)\s*sec', t_low)
    if _dm: duration = min(max(int(_dm.group(1)), 2), 12)

    total = duration * fps
    Y_g, X_g = np.mgrid[0:H, 0:W].astype(np.float32)
    y_n = Y_g / H; x_n = X_g / W
    cx_c, cy_c = W / 2.0, H / 2.0
    dist_g = np.sqrt(((X_g-cx_c)/(W*0.7))**2+((Y_g-cy_c)/(H*0.7))**2).astype(np.float32)
    angle_g = ((np.arctan2(Y_g-cy_c,X_g-cx_c)/(2*math.pi))+0.5).astype(np.float32)%1.0
    pal_arr = np.array(pal, dtype=np.float32); N = len(pal_arr)

    def _to_rgb(pct):
        pct=np.clip(pct,0,1); idx=pct*(N-1)
        lo=np.floor(idx).astype(np.int32); hi=np.clip(lo+1,0,N-1)
        bl=(idx-lo)[...,None]
        return np.clip(pal_arr[lo]+(pal_arr[hi]-pal_arr[lo])*bl,0,255).astype(np.uint8)

    _disp = _vid_title[:34] if len(_vid_title)<=34 else _vid_title[:31]+"..."
    try: _font = ImageFont.load_default()
    except: _font = None

    mcx, mcy = W//2, H//2
    frames = []
    for i in range(total):
        t = i / max(total-1, 1)
        tv = t * _tv_speed
        if _tv_motion=="wave":
            wave=np.sin(Y_g*0.06+tv*math.pi*2).astype(np.float32)*0.12; pct=(y_n+tv*0.5+wave)%1.0
        elif _tv_motion=="zoom": pct=(dist_g+tv*0.5)%1.0
        elif _tv_motion=="spin": pct=(angle_g+tv*0.5)%1.0
        elif _tv_motion=="fade": pct=np.full((H,W),(tv*0.5)%1.0,dtype=np.float32)
        else: pct=((x_n+y_n)*0.5+tv*0.5)%1.0
        frame=Image.fromarray(_to_rgb(pct),"RGB"); draw=ImageDraw.Draw(frame)

        # ── Scene elements ──────────────────────────────────────────────
        if _scene=="fight":
            sp=max(0.0,1.0-t*2.4); sx=int(W*0.3*sp); r=20
            if sx>4:
                draw.ellipse([mcx-sx-r,mcy-r,mcx-sx+r,mcy+r],fill=_c1)
                draw.ellipse([mcx+sx-r,mcy-r,mcx+sx+r,mcy+r],fill=_c2)
            else:
                ft=t-0.42
                if 0<ft<0.25: draw.ellipse([mcx-45,mcy-45,mcx+45,mcy+45],fill=(255,220,max(0,int(255*(1-ft/0.25)))))
                _rnd_v.seed(i)
                for _ in range(12):
                    sx2=mcx+_rnd_v.randint(-70,70); sy2=mcy+_rnd_v.randint(-50,50); sr=_rnd_v.randint(2,6)
                    draw.ellipse([sx2-sr,sy2-sr,sx2+sr,sy2+sr],fill=_rnd_v.choice([_c1,_c2,(255,220,0)]))
        elif _scene=="sport":
            bt=(t*1.5)%1.0; bx=int(W*0.07+bt*W*0.86); by=int(H*0.78-math.sin(bt*math.pi)*H*0.52); r=13
            for tr in range(3,0,-1):
                trt=max(0,bt-tr*0.07); trx=int(W*0.07+trt*W*0.86); try_=int(H*0.78-math.sin(trt*math.pi)*H*0.52)
                fc=tuple(max(0,int(c*(4-tr)/4)) for c in _c1)
                draw.ellipse([trx-(r-tr),try_-(r-tr),trx+(r-tr),try_+(r-tr)],fill=fc)
            draw.ellipse([bx-r,by-r,bx+r,by+r],fill=_c1)
        elif _scene=="space":
            _rnd_v.seed(99)
            for _ in range(25):
                sx=_rnd_v.randint(0,W); sy=_rnd_v.randint(0,H)
                sc=int(160*abs(math.sin(t*math.pi*3+sx*0.05))+60)
                draw.ellipse([sx,sy,sx+2,sy+2],fill=(sc,sc,sc))
            ang=t*math.pi*4; ox=int(mcx+65*math.cos(ang)); oy=int(mcy+28*math.sin(ang))
            draw.ellipse([ox-8,oy-8,ox+8,oy+8],fill=_c1)
            draw.ellipse([mcx-6,mcy-6,mcx+6,mcy+6],fill=_c2)
        elif _scene=="love":
            pulse=1.0+0.18*math.sin(t*math.pi*4); r=int(22*pulse)
            draw.ellipse([mcx-r,mcy-r+4,mcx,mcy+4],fill=_c1)
            draw.ellipse([mcx,mcy-r+4,mcx+r,mcy+4],fill=_c1)
            draw.polygon([(mcx-r,mcy+4),(mcx+r,mcy+4),(mcx,mcy+r+14)],fill=_c1)
            _rnd_v.seed(i*5)
            for _ in range(5):
                px=mcx+_rnd_v.randint(-60,60); py=int(mcy+50-t*90+_rnd_v.randint(-8,8))
                draw.ellipse([px-3,py-3,px+3,py+3],fill=_c2)
        elif _scene=="horror":
            if i%max(1,int(fps*0.6))<2: draw.rectangle([0,0,W,H],fill=(180,180,230))
            _rnd_v.seed(11)
            for _ in range(5):
                dx=_rnd_v.randint(40,W-40); dh=int(15+t*50)
                draw.rectangle([dx-2,0,dx+2,dh],fill=(160,0,0))
        elif _scene=="celebration":
            _rnd_v.seed(i)
            cols=[(255,50,150),(255,200,0),(50,200,255),(150,50,255),_c1,_c2]
            for _ in range(18):
                cx2=_rnd_v.randint(0,W); cy2=int((_rnd_v.randint(0,H)-t*220)%H)
                r2=_rnd_v.randint(4,9); draw.ellipse([cx2-r2,cy2-r2,cx2+r2,cy2+r2],fill=_rnd_v.choice(cols))
        else:
            for idx2 in range(3):
                ang=t*math.pi*2+idx2*(2*math.pi/3)
                ex=int(mcx+65*math.cos(ang)); ey=int(mcy+32*math.sin(ang)); r=12
                draw.ellipse([ex-r,ey-r,ex+r,ey+r],fill=(_c1 if idx2%2==0 else _c2))

        # ── Cinematic bars ───────────────────────────────────────────────
        draw.rectangle([0,0,W,BAR],fill=(0,0,0))
        draw.rectangle([0,H-BAR,W,H],fill=(0,0,0))

        # ── Title text in top bar ────────────────────────────────────────
        if _font:
            tw=len(_disp)*6; tx=max(4,(W-tw)//2); ty=(BAR-10)//2
            draw.text((tx+1,ty+1),_disp,fill=(0,0,0),font=_font)
            draw.text((tx,ty),_disp,fill=(255,255,255),font=_font)

        frames.append(frame.quantize(colors=128,method=Image.Quantize.MEDIANCUT))

    buf=io.BytesIO()
    frames[0].save(buf,format="GIF",save_all=True,append_images=frames[1:],
                   duration=int(1000/fps),loop=0,optimize=True)
    buf.seek(0)
    return buf.getvalue()

def _is_pdf_extract_request(text):
    import re as _re_pdf
    t = text.lower()
    if _re_pdf.search(r'\b(page|pages|pg|pgs|pp)\b.*\d+.*\bto\b.*\d+', t):
        return True
    if _re_pdf.search(r'\d+\s+to\s+\d+.*(page|pdf|print)', t):
        return True
    if _re_pdf.search(r'(extract|give me|get me|download|export).*(page|pages|pdf)', t) and _re_pdf.search(r'\d+', t):
        return True
    if _re_pdf.search(r'(page|pages)\s+\d+\s*(to|-|–|through|till|until)\s*\d+', t):
        return True
    return False

def _parse_pdf_page_range(text):
    """Return (start, end) 1-indexed inclusive, or None."""
    import re as _re_pr
    nums = [int(x) for x in _re_pr.findall(r'\d+', text)]
    if len(nums) >= 2:
        a, b = nums[0], nums[1]
        return min(a, b), max(a, b)
    return None

def _extract_pdf_pages(pdf_bytes, start_page, end_page):
    """Extract pages start_page–end_page (1-indexed, inclusive). Returns bytes or None."""
    try:
        import PyPDF2 as _pypdf, io as _io_pdf
        reader = _pypdf.PdfReader(_io_pdf.BytesIO(pdf_bytes))
        total  = len(reader.pages)
        s = max(1, min(start_page, total)) - 1
        e = max(1, min(end_page,   total)) - 1
        writer = _pypdf.PdfWriter()
        for i in range(s, e + 1):
            writer.add_page(reader.pages[i])
        out = _io_pdf.BytesIO()
        writer.write(out)
        return out.getvalue(), total
    except Exception:
        return None, 0

def _gen_image_url(prompt, is_max=False):
    import urllib.parse, hashlib as _hg
    if is_max:
        _full = (
            prompt.strip() +
            ", ultra photorealistic, DSLR photograph, Sony A7R V, 85mm f/1.4 lens, "
            "perfect natural lighting, 8K UHD, skin texture visible, RAW capture, "
            "zero AI artifacts, indistinguishable from real photograph, magazine quality"
        )
    else:
        _full = (
            prompt.strip() +
            ", photorealistic, high quality, 4K, professional photography, "
            "clean lighting, sharp focus, detailed"
        )
    _seed = int(_hg.md5(prompt.encode()).hexdigest()[:8], 16) % 999999
    _enc  = urllib.parse.quote(_full)
    return (
        f"https://image.pollinations.ai/prompt/{_enc}"
        f"?model=flux&width=1024&height=1024&enhance=true&nologo=true&seed={_seed}"
    )

def _gen_video_fal(prompt, is_max=False):
    """Submit to fal.ai WAN 2.1, poll for result. Returns (url, error)."""
    import time as _tvid
    _fal_key = ""
    try: _fal_key = st.secrets.get("FAL_KEY", "")
    except Exception: pass
    if not _fal_key:
        _fal_key = st.session_state.get("fal_api_key", "")
    if not _fal_key:
        return None, "no_key"

    _model = "fal-ai/wan/v2.1/14b/text-to-video" if is_max else "fal-ai/wan/v2.1/1.3b/text-to-video"
    _video_prompt = (
        prompt.strip() +
        (", ultra realistic, cinematic 4K, photorealistic lighting, "
         "indistinguishable from real video footage, professional cinematography, "
         "no AI artifacts, natural motion" if is_max
         else ", high quality, smooth motion, cinematic, detailed")
    )
    _headers = {"Authorization": f"Key {_fal_key}", "Content-Type": "application/json"}
    _payload  = {"prompt": _video_prompt, "duration": "5", "aspect_ratio": "16:9"}
    try:
        _sub = requests.post(f"https://queue.fal.run/{_model}",
                             json=_payload, headers=_headers, timeout=30)
        if _sub.status_code not in (200, 201):
            return None, f"Submit failed ({_sub.status_code})"
        _req_id = _sub.json().get("request_id")
        if not _req_id:
            return None, "No request ID returned"
        for _ in range(60):
            _tvid.sleep(5)
            _poll = requests.get(
                f"https://queue.fal.run/{_model}/requests/{_req_id}/status",
                headers=_headers, timeout=20)
            _st = _poll.json().get("status", "")
            if _st == "COMPLETED":
                _res = requests.get(
                    f"https://queue.fal.run/{_model}/requests/{_req_id}",
                    headers=_headers, timeout=20)
                _vurl = (
                    _res.json().get("video", {}).get("url") or
                    (_res.json().get("videos") or [{}])[0].get("url", "")
                )
                return (_vurl, None) if _vurl else (None, "No video URL in result")
            elif _st in ("FAILED", "CANCELLED"):
                return None, "Video generation failed on server."
        return None, "Timed out waiting for video."
    except Exception as _ev:
        return None, str(_ev)

# ── System prompt (fully auto-detected from user input) ───────────────────────
def get_system():
    msgs = cur_msgs()
    last = ""
    if msgs:
        for _m in reversed(msgs):
            if _m["role"] == "user":
                last = _m.get("content", "").lower()
                break

    # Document uploaded → document analysis mode
    if file_content and not file_content.startswith("[Image"):
        return DOC_SYSTEM

    if last:
        # Exam paper
        if "generate a complete exam paper" in last:
            return EXAM_SYSTEM
        # Flashcard generation
        if _is_flashcard_request(last):
            return FLASH_SYSTEM
        # Weather / climate questions → inject live data if available
        if _is_weather_query(last):
            _ws = WEATHER_SYSTEM
            if st.session_state.get("weather_data") and st.session_state.get("weather_name"):
                try:
                    _cu2 = st.session_state.weather_data.get("current", {})
                    _dy2 = st.session_state.weather_data.get("daily", {})
                    _rain2 = _dy2.get("precipitation_probability_max", [0])[0] if _dy2.get("precipitation_probability_max") else "?"
                    _uv2   = round(_dy2.get("uv_index_max", [0])[0], 1) if _dy2.get("uv_index_max") else "?"
                    _aqcu2 = (st.session_state.weather_aqi or {}).get("current", {})
                    _ws += (
                        f"\n\n━━━ LIVE WEATHER DATA ━━━\n"
                        f"Location: {st.session_state.weather_name}\n"
                        f"Temperature: {_cu2.get('temperature_2m','?')}°C  |  Feels like: {_cu2.get('apparent_temperature','?')}°C\n"
                        f"Humidity: {_cu2.get('relative_humidity_2m','?')}%  |  Wind: {round(_cu2.get('wind_speed_10m',0))} km/h\n"
                        f"Rain chance today: {_rain2}%  |  UV Index: {_uv2}\n"
                        f"AQI (EU scale): {int(_aqcu2.get('european_aqi',0)) if _aqcu2 else 'N/A'}"
                    )
                except Exception:
                    pass
            return _ws
        # Teach Me — progressive tutor
        if _is_teach_request(last):
            return (SYSTEM + "\n\n━━━ TEACH ME MODE ━━━\n"
                "You are now a personal tutor. Teach step-by-step. After each concept, ask ONE comprehension question. "
                "Wait for the user's answer before continuing. If correct, praise briefly and move on. "
                "If wrong, gently correct and re-explain simply. Never dump everything at once. "
                "Teach like a patient human tutor who checks understanding before advancing.")
        # Code
        if _is_code_request(last):
            return CODE_SYSTEM
        # Grammar / writing
        if _is_grammar_request(last):
            return GRAMMAR_SYSTEM
        # Story / creative writing
        if _is_story_request(last):
            return STORY_SYSTEM
        # Search / current events
        if _is_search_request(last):
            return SEARCH_SYSTEM

    import datetime as _dtnow
    _now = _dtnow.datetime.now()
    base = SYSTEM + f"\n\nCurrent date: {_now.strftime('%A, %d %B %Y')}. Current time: {_now.strftime('%I:%M %p')} (IST)."
    # ── Tier-based system prompt additions ────────────────────────────────────
    _sys_tier = st.session_state.get("titan_tier", "basic")
    if _sys_tier == "pro":
        _pro_depth = st.session_state.get("_answer_depth", "normal")
        if _pro_depth == "quick":
            _depth_instr = "Answer concisely in 2-4 sentences. Get straight to the point. No lengthy explanations."
        elif _pro_depth == "deep":
            _depth_instr = "Give an exhaustive, research-grade answer. Cover all angles, subtopics, expert nuances, real examples, comparisons, and actionable insights. Be impressively thorough."
        else:
            _depth_instr = "Give deeper, more detailed answers than standard. Always include extra context, examples, and analysis. Be noticeably more thorough and impressive."
        base += (
            "\n\n━━━ TITAN ULTRA PRO MODE ━━━\n"
            f"You are running in PRO mode with depth set to: {_pro_depth.upper()}.\n"
            + _depth_instr +
            "\nAlways make the user feel they are getting premium-quality answers far beyond any free AI.\n\n"
            "PRO ANSWER QUALITY STANDARDS:\n"
            "• DEPTH AND REASONING — Use multi-step thinking for complex problems. Break down logic, maths, "
            "science, and code step by step. Hold all the details at once and work through them in order.\n"
            "• CONTEXT AWARENESS — Remember everything said earlier in the conversation. Never lose track. "
            "If the user shared a document or long history, use ALL of it to give a complete answer.\n"
            "• FACTUALITY — When answering factual or current questions, use web search results provided to "
            "ground the answer in real, up-to-date information. Never guess. If uncertain, say so clearly.\n"
            "• ADAPTABLE TONE AND FORMAT — Match the user's style. Casual question → casual answer. "
            "Technical question → structured, precise answer. Use headers, bullet points, code blocks, "
            "and tables whenever they make the answer clearer and easier to read.\n"
            "• Give the FINISHED thing — not just advice. Write the code. Draft the email. Build the plan.\n\n"
            "PRO PYTHON CODE RULE — Your code MUST be CLEARLY different from basic. Mandatory features:\n"
            "Colorful styled paddles and background, math-generated sounds (no files), ball trail effect, "
            "particle explosions on score, screen shake, pause (P key), menu + game over screens, "
            "paddle glow, angle-based bounce. Around 200 lines. Looks like a real polished game.\n\n"
            "PRO FORMAT RULE — Every answer MUST follow this structure: "
            "1) Short opening line giving the main point. "
            "2) Organised body with emoji section headings, bullet points, bold key terms, tables for comparisons, code blocks for code. "
            "3) End with a helpful closing offer like 'Would you like me to build this for you?' or 'Want me to explain any part in more detail?'"
        )
    elif _sys_tier == "max":
        base += (
            "\n\n━━━ TITAN ULTRA MAX MODE — ULTIMATE ━━━\n"
            "The user has paid ₹24,000 for MAX. Every single answer must feel worth that. "
            "NEVER give something average, generic, or textbook-style. Every answer must feel crafted just for them.\n\n"
            "MAX ANSWER QUALITY — Match this standard exactly:\n\n"
            "MAX ANSWER QUALITY STANDARDS — deliver ALL of these every time:\n\n"
            "• UNDERSTAND THE REAL MEANING — Even if the message has typos or is loosely phrased, "
            "figure out what they actually want. Never ask them to rephrase. Just answer.\n"
            "• DEEP REASONING — Use multi-step thinking for complex problems. Maths, physics, "
            "debugging, system design, planning — break it down fully, hold every detail, work through in order.\n"
            "• CONTEXT AWARENESS — Remember everything from earlier in the conversation. "
            "Never make the user repeat themselves. Use their full history to give a complete answer.\n"
            "• MULTIMODAL — Process and reason across text, images, code, and documents together. "
            "When an image or file is shared, analyse it deeply and connect it to the answer.\n"
            "• FACTUALITY AND SEARCH GROUNDING — For real-time or factual questions, use web search "
            "results to ground the answer in accurate, up-to-date information. Never guess. "
            "If uncertain, say clearly: 'I'm not 100% sure but...'\n"
            "• GIVE THE FINISHED THING — Don't say 'you could try this.' Write the code. "
            "Draft the email. Build the plan. Give the complete, ready-to-use answer.\n"
            "• ADAPTABLE FORMAT — Use headers, bullet points, code blocks, tables. "
            "Make answers beautiful, scannable, and easy to read. Match the user's tone — "
            "casual question gets a warm casual answer, technical question gets a structured expert answer.\n"
            "• HONESTY OVER FLATTERY — If something has a flaw, say so. If the user pushes back, "
            "re-check carefully. Second and third versions are always better — offer to improve.\n"
            "• ZERO TOLERANCE FOR MISTAKES — Every fact must be accurate. Never truncate. Never go shallow.\n"
            "• End every answer with a 'Pro Insight' — one expert tip or hidden fact most people never know.\n\n"
            "MAX LANGUAGE RULE — Talk like a real human friend, not like an AI or a textbook. "
            "Imagine you and the user are sitting together and just having a normal conversation. "
            "Use the kind of words you'd say out loud to a friend — casual, warm, relaxed. "
            "Say things like: 'Okay so here's the thing...', 'Basically what happens is...', "
            "'Think of it this way...', 'So yeah, that's why...', 'Honestly it's pretty simple once you get it!', "
            "'Right so first you gotta...', 'Don't worry, I'll explain it step by step!'\n"
            "Never sound stiff or robotic. Never use formal essay language. "
            "Short sentences. Everyday words. If something is hard, make it feel easy by breaking it down naturally. "
            "The user should feel like they're texting their smartest friend who always has the answer. "
            "Be warm, be real, be human — that's what Max is all about.\n\n"
            "MAX PYTHON CODE RULE — Your code MUST be 5x more impressive than Pro. Mandatory features:\n"
            "5 levels each with unique color theme and name, each level harder than last, "
            "moving obstacles in later levels, particle sparks on every hit, screen shake on score, "
            "fading ball trail, rainbow ball in final level, twinkling stars background, "
            "mouse + keyboard controls, AI with error factor, math-generated sounds for every event, "
            "menu/pause/level-complete/victory screens, confetti on final win, 400-500 lines of code. "
            "Looks like a real commercial game. Add short simple comments in the code explaining each part.\n\n"
            "MAX FORMAT RULE — Every answer MUST follow this structure: "
            "1) Short opening line giving the main point. "
            "2) Organised body with emoji section headings, bullet points, bold key terms, tables for comparisons, code blocks for code. "
            "3) End with a helpful closing offer like 'Would you like me to build this for you?' or 'Want me to explain any part in more detail?'"
        )
    mem = st.session_state.get("titan_memory", {})
    if mem:
        base += "\n\nThings you remember about the user:\n" + "\n".join(f"- {k}: {v}" for k, v in mem.items())
    # Connected apps
    _conn = st.session_state.get("connected_apps", [])
    if _conn:
        base += (
            f"\n\n━━━ CONNECTED APPS ━━━\n"
            f"The user has connected these apps to Titan Ultra: {', '.join(_conn)}.\n"
            f"RULES when they ask about a connected app:\n"
            f"• DO NOT say 'open the app' or explain how to install/launch it.\n"
            f"• Act like you are their personal expert guide INSIDE the app.\n"
            f"• When asked 'what is in [app]?' — describe its key sections, features, "
            f"what the user can do, tips, shortcuts, and personalised recommendations.\n"
            f"• Example: 'what is in YouTube?' → explain Home feed, Shorts, Subscriptions, "
            f"Watch History, playlists, trending, what to search for, etc.\n"
            f"• Be enthusiastic and helpful like you ARE inside the app with them."
        )
    # Cross-session memory — include recent past chat content so AI remembers previous conversations
    _ph_all = _load_history()
    if _ph_all:
        _ph_lines = []
        for _ph in _ph_all[:3]:
            _ph_msgs = _ph.get("messages", [])
            if not _ph_msgs:
                continue
            _ph_title = _ph.get("title", "Chat")
            _ph_date  = (_ph.get("date") or "")[:10]
            _ph_lines.append(f"\n--- {_ph_title} ({_ph_date}) ---")
            for _phm in _ph_msgs[-6:]:
                _pr = "User" if _phm["role"] == "user" else "You (Titan)"
                _pc = str(_phm.get("content", ""))[:200]
                _ph_lines.append(f"{_pr}: {_pc}")
        if _ph_lines:
            base += ("\n\n━━━ YOUR MEMORY OF PAST CHATS ━━━\n"
                     "You remember these previous conversations with this user. "
                     "Use this to stay consistent and maintain continuity:\n"
                     + "\n".join(_ph_lines))
    # Auto-detect language and instruct AI to reply in same language
    _msgs_check = cur_msgs()
    if _msgs_check:
        for _mc in reversed(_msgs_check):
            if _mc["role"] == "user":
                _lang = _detect_user_language(_mc.get("content",""))
                if _lang:
                    base += f"\n\nIMPORTANT: The user is writing in {_lang}. Respond in {_lang} language. Match the user's language exactly."
                break
    # Inject live news headlines (session cache — never blocks AI response)
    _live_news = st.session_state.get("_ticker_data", [])
    if _live_news:
        base += "\n\n━━━ LIVE NEWS RIGHT NOW ━━━\n"
        base += "\n".join(f"• {h}" for h in _live_news[:20])
        base += "\n\nUse these headlines when asked about current events, latest news, or recent releases."
    return base

# ── API calls ─────────────────────────────────────────────────────────────────
def _build_full(messages, trim=None):
    """Build [system] + messages, optionally keeping only the last `trim` messages."""
    hist = messages[-trim:] if trim and len(messages) > trim else messages
    # Always keep pairs (user+assistant) so we don't start with an assistant turn
    if hist and hist[0]["role"] == "assistant":
        hist = hist[1:]
    return [{"role": "system", "content": get_system()}] + hist

@st.cache_data(ttl=120)
def _get_groq_all_models(api_key):
    """Return all currently available Groq model IDs."""
    try:
        _c = Groq(api_key=api_key)
        return sorted([m.id for m in _c.models.list().data])
    except Exception:
        return []

def _get_groq_vision_models(api_key):
    """Return vision-capable Groq model IDs from the live model list."""
    _all = _get_groq_all_models(api_key)
    if not _all:
        return ["meta-llama/llama-4-scout-17b-16e-instruct",
                "meta-llama/llama-4-maverick-17b-128e-instruct"]
    _vision_keywords = ["scout", "maverick", "vision", "llava", "llama-4", "llama4",
                        "llama-4.1", "llama-4.5", "4scout", "4maverick"]
    _found = [m for m in _all if any(k in m.lower() for k in _vision_keywords)]
    return _found if _found else _all  # if nothing looks like vision, try everything

def _smart_pick(messages):
    """Auto-select best Groq model based on question type. Maverick is default."""
    last = ""
    for m in reversed(messages):
        if m["role"] == "user":
            c = m["content"]
            last = c if isinstance(c, str) else " ".join(
                p.get("text", "") for p in c if isinstance(p, dict)
            )
            break
    q = last.lower()

    # ── Hard math / science / JEE / NEET / deep reasoning → GPT-OSS 120B (strongest) ──
    _hard = [
        "jee", "neet", "olympiad", "integrate", "differentiate", "derivative",
        "integral", "prove", "proof", "theorem", "derivation", "solve for",
        "evaluate", "calculate", "find the value", "limit of", "sum of series",
        "differential equation", "permutation", "combination", "probability of",
        "kirchhoff", "faraday", "gauss", "newton", "bernoulli", "stoichiometry",
        "equilibrium constant", "quantum", "eigenvalue", "fourier", "laplace",
        "taylor", "binomial theorem", "matrix", "determinant", "vector",
        "explain in detail", "explain why", "explain how", "what is the reason",
        "compare", "difference between", "advantages", "disadvantages",
        "write an essay", "write a letter", "write a paragraph",
        "step by step", "full solution", "detailed answer",
    ]
    if any(x in q for x in _hard):
        return "openai/gpt-oss-120b"

    # ── Coding / programming → GPT-OSS 120B (best at code too) ──
    _code = [
        "write a program", "write code", "write a function", "write a script",
        "debug", "fix this code", "fix the bug", "implement", "algorithm",
        "python", "javascript", "html", "css", "sql", "java", "c++", "c#",
        "leetcode", "data structure", "time complexity", "api", "recursion",
    ]
    if any(x in q for x in _code):
        return "openai/gpt-oss-120b"

    # ── Simple / short / quick questions → GPT-OSS 20B (faster, saves quota) ──
    _simple = [
        "what is", "who is", "when was", "where is", "how many", "how much",
        "define ", "meaning of", "capital of", "full form", "full name",
        "what does", "who wrote", "who invented", "year of", "name the",
        "spell ", "translate", "synonym", "antonym",
    ]
    if any(x in q for x in _simple) and len(q.split()) < 15:
        return "openai/gpt-oss-20b"

    # ── Default → GPT-OSS 120B (strongest for everything else) ──
    return "openai/gpt-oss-120b"


def _model_cfg(mid):
    """Return (max_tokens, temperature, top_p) tuned to each model's strengths."""
    m = mid.lower()
    if "gpt-oss-120b" in m:
        return 65536, 0.30, 0.95
    if "gpt-oss-20b" in m:
        return 65536, 0.40, 0.92
    if "qwen" in m:
        return 16384, 0.50, 0.90
    if "kimi" in m or "moonshot" in m:
        return 16384, 0.40, 0.92
    if "maverick" in m:
        return 16384, 0.40, 0.92
    if "deepseek" in m:
        return 16384, 0.35, 0.92
    if "llama-3.3" in m or "llama-3.1-70b" in m or "llama3-70b" in m:
        return 8192, 0.45, 0.90
    if "gemma" in m:
        return 8192, 0.50, 0.90
    if "8b" in m or "instant" in m:
        return 8192, 0.55, 0.90
    if "allam" in m or "saba" in m or "guard" in m:
        return 8192, 0.60, 0.90
    # Safe default for any future model
    return 8192, 0.40, 0.92


def call_groq(messages):
    client = Groq(api_key=st.session_state.api_key)
    # Cap history at 20 messages — reduces tokens sent per call, avoiding rate limits faster
    full = _build_full(messages, trim=20)

    # ── Vision: clean single-message request with compressed image.
    _vision = st.session_state.get("pending_vision")
    _use_vision = bool(_vision and full and full[-1]["role"] == "user")
    if _use_vision:
        _last = full[-1]
        _raw_text = _last["content"] if isinstance(_last["content"], str) else str(_last["content"])
        # Strip the [File]: tag, keep only the user's actual question
        import re as _re_vis
        _clean_q = _re_vis.sub(r'\n*\[File\].*', '', _raw_text, flags=_re_vis.DOTALL).strip()
        if not _clean_q:
            _clean_q = "Read and write every single word visible in this image. Even if blurry, try your absolute best. Text may be in Hindi, Telugu, Tamil, Urdu, English or any language — write it exactly as it appears, then describe the image."
        # Compress image to max 1024px, JPEG 85 — reduces 3MB WhatsApp image to ~200KB
        try:
            import io as _io_v
            from PIL import Image as _PILv
            _img_v = _PILv.open(_io_v.BytesIO(_vision["bytes"])).convert("RGB")
            _iw, _ih = _img_v.size
            _max_px = 1024
            if max(_iw, _ih) > _max_px:
                _scale_v = _max_px / max(_iw, _ih)
                _img_v = _img_v.resize((int(_iw * _scale_v), int(_ih * _scale_v)), _PILv.LANCZOS)
            _cbuf = _io_v.BytesIO()
            _img_v.save(_cbuf, format="JPEG", quality=85)
            import base64 as _b64v2
            _vis_b64 = _b64v2.b64encode(_cbuf.getvalue()).decode("ascii")
            _vis_mime = "image/jpeg"
        except Exception:
            _vis_b64 = _vision["b64"]
            _vis_mime = _vision["mime"]
        full = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _clean_q},
                    {"type": "image_url", "image_url": {
                        "url": f"data:{_vis_mime};base64,{_vis_b64}"
                    }},
                ],
            }
        ]

    # Full fallback chain — tried in order when any model fails or hits rate limit
    if _use_vision:
        _fallback_chain = _get_groq_vision_models(st.session_state.api_key)
    else:
        _titan_mode = st.session_state.get("_titan_mode", "normal")
        if _titan_mode == "fast":
            _fallback_chain = [
                "openai/gpt-oss-20b",
                "meta-llama/llama-4-maverick-17b-128e-instruct",
                "llama-3.3-70b-versatile",
                "gemma2-9b-it",
                "llama-3.1-8b-instant",
            ]
        elif _titan_mode == "think":
            _fallback_chain = [
                "deepseek-r1-distill-llama-70b",
                "openai/gpt-oss-120b",
                "moonshotai/kimi-k2-instruct",
                "meta-llama/llama-4-maverick-17b-128e-instruct",
                "llama-3.3-70b-versatile",
            ]
        else:
            _auto = _smart_pick(messages)
            _cur_tier = st.session_state.get("titan_tier", "basic")
            if _cur_tier == "basic":
                _fallback_chain = [
                    "openai/gpt-oss-20b",
                    "qwen/qwen3.8-27b",
                    "openai/gpt-oss-120b",
                    "meta-llama/llama-4-maverick-17b-128e-instruct",
                    "llama-3.3-70b-versatile",
                    "gemma2-9b-it",
                    "llama-3.1-8b-instant",
                ]
            elif _cur_tier == "max":
                _fallback_chain = [
                    "deepseek-r1-distill-llama-70b",
                    "openai/gpt-oss-120b",
                    "moonshotai/kimi-k2-instruct",
                    "meta-llama/llama-4-maverick-17b-128e-instruct",
                    "llama-3.3-70b-versatile",
                    "gemma2-9b-it",
                    "llama-3.1-8b-instant",
                ]
            else:  # pro
                _fallback_chain = [
                    _auto,
                    "openai/gpt-oss-120b",
                    "openai/gpt-oss-20b",
                    "qwen/qwen3.8-27b",
                    "meta-llama/llama-4-maverick-17b-128e-instruct",
                    "moonshotai/kimi-k2-instruct",
                    "deepseek-r1-distill-llama-70b",
                    "llama-3.3-70b-versatile",
                    "gemma2-9b-it",
                    "llama-3.1-8b-instant",
                ]
    _seen = set()
    _chain = [m for m in _fallback_chain if not (m in _seen or _seen.add(m))]

    import time as _time

    # ── Token budgets per pass — tier-aware so quality difference is real ────────
    _cur_tier_tok = st.session_state.get("titan_tier", "basic") if not _use_vision else "pro"
    if _cur_tier_tok == "basic":
        _token_budgets = [4096, 3000, 2048, 1500]
    elif _cur_tier_tok == "max":
        _token_budgets = [32768, 24000, 16384, 8192, 4096, 2048]
    else:  # pro
        _token_budgets = [16384, 12000, 8192, 6000, 4096, 2048]

    _last_err = None
    _current_full = full

    # ── Keep retrying ALL Groq models until one works — never give up ─────────
    # Groq per-minute limits reset every 60 seconds. With 15 models in the chain
    # and up to 8 retry passes, the loop covers ~8 minutes — effectively unlimited
    # for any normal conversation. Error is NEVER shown to the user.
    for _pass in range(8):
        _tok_budget = _token_budgets[min(_pass, len(_token_budgets) - 1)]
        _all_rate_limited = True  # assume all rate-limited until proven otherwise

        for m in _chain:
            try:
                _mid = m[5:] if m.startswith("groq/") else m
                _mtok, _mtemp, _mtopp = _model_cfg(_mid)
                _use_tok = min(_mtok, _tok_budget)
                _kwargs = {"model": _mid, "messages": _current_full, "max_tokens": _use_tok}
                if not _use_vision:
                    _kwargs["temperature"] = _mtemp
                    _kwargs["top_p"]       = _mtopp
                r = client.chat.completions.create(**_kwargs)
                return r.choices[0].message.content
            except Exception as e:
                _last_err = e
                _es = str(e).lower()

                # 413 — context too large: shrink and retry this model immediately
                if "413" in _es or "request_too_large" in _es or "request entity too large" in _es:
                    try:
                        _current_full = _build_full(messages, trim=4)
                        _r2 = client.chat.completions.create(
                            model=_mid, messages=_current_full,
                            max_tokens=4096, temperature=_mtemp, top_p=_mtopp)
                        return _r2.choices[0].message.content
                    except Exception as e2:
                        _last_err = e2
                        _current_full = full
                    continue

                # Auth error — wrong API key, show immediately
                _etype = type(e).__name__.lower()
                if ("auth" in _etype or "401" in _es or
                    any(x in _es for x in ("authentication", "unauthorized",
                                           "invalid api key", "incorrect api key",
                                           "no api key", "api key required",
                                           "invalid_api_key", "api_key"))):
                    raise RuntimeError("❌ Invalid Groq API key. Please re-enter your key in the sidebar.")

                # Rate limit — mark and try next model in chain
                if "rate_limit" in _es or "rate limit" in _es or "429" in _es or "tokens per" in _es or "quota" in _es:
                    continue  # _all_rate_limited stays True

                # Any other error — mark as not-all-rate-limited, but still skip to next model
                _all_rate_limited = False
                continue

        # Sleep between passes — always sleep if ANY model was rate-limited this pass.
        # Do NOT skip sleep just because some models failed for other reasons —
        # the valid models that ARE rate-limited need this time to reset.
        if _pass < 7:
            _wait = 15 + (_pass * 5)
            _time.sleep(_wait)

    if _use_vision:
        raise RuntimeError("❌ Image analysis failed. Please try again.")
    _last_msg = str(_last_err)[:300] if _last_err else "Unknown error"
    raise RuntimeError(f"❌ All models failed. Last error: {_last_msg}")

def _ollama_options(model_name: str) -> dict:
    """Return speed-optimised generation options for each model."""
    m = model_name.lower()
    if "qwen" in m:
        # Qwen3 fast mode: /no_think disables hidden chain-of-thought so the
        # first token arrives immediately. Step-by-step quality comes from the
        # system prompt, not slow internal reasoning.
        return {
            "num_ctx":        8192,    # plenty for any question, loads fast
            "num_predict":    4096,    # long complete answers
            "temperature":    0.7,
            "top_p":          0.9,
            "top_k":          40,
            "repeat_penalty": 1.1,
            "num_gpu":        -1,      # all GPU layers (auto CPU if no GPU)
            "num_batch":      512,     # process 512 tokens at once — faster
            "f16_kv":         True,    # FP16 KV-cache — saves RAM, faster
        }
    elif "moondream" in m:
        return {
            "num_ctx":        4096,
            "num_predict":    1024,
            "temperature":    0.3,
            "top_p":          0.9,
            "num_gpu":        -1,
            "num_batch":      512,
            "f16_kv":         True,
        }
    else:
        return {
            "num_ctx":        8192,
            "num_predict":    4096,
            "temperature":    0.7,
            "top_p":          0.9,
            "repeat_penalty": 1.1,
            "num_gpu":        -1,
            "num_batch":      512,
            "f16_kv":         True,
        }

def _inject_thinking(messages: list, model_name: str) -> list:
    """For Qwen3: inject /no_think so it skips hidden reasoning and answers immediately."""
    if "qwen" not in model_name.lower():
        return messages
    msgs = [m.copy() for m in messages]
    for i in range(len(msgs) - 1, -1, -1):
        if msgs[i]["role"] == "user":
            content = msgs[i]["content"]
            if isinstance(content, str):
                # strip any old /think or /no_think prefix first
                stripped = content.strip()
                for prefix in ("/think\n", "/no_think\n", "/think ", "/no_think "):
                    if stripped.startswith(prefix):
                        stripped = stripped[len(prefix):]
                msgs[i]["content"] = "/no_think\n" + stripped
            break
    return msgs

def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> blocks that Qwen3 sometimes exposes."""
    import re as _re_th
    return _re_th.sub(r"<think>.*?</think>", "", text, flags=_re_th.DOTALL).strip()

def call_ollama(messages, ollama_model=None):
    import time as _t_ol
    _model = ollama_model or model_id
    full   = _build_full(messages, trim=20)
    full   = _inject_thinking(full, _model)
    # If there is a pending vision image, attach it to the last user message
    _vis = st.session_state.get("pending_vision")
    if _vis and full and full[-1]["role"] == "user":
        _last = full[-1].copy()
        _txt = _last["content"] if isinstance(_last["content"], str) else str(_last["content"])
        if not _txt or _txt.startswith("[Image attached"):
            _txt = "Read and write every single word visible in this image. Even if blurry, try your best. The text may be in any language — Hindi, English, Telugu, Tamil, Urdu, etc. Write the text exactly as it appears, then describe the image."
        _last["content"] = _txt
        _last["images"] = [_vis["b64"]]
        full[-1] = _last
    _url   = "http://localhost:11434/api/chat"
    _payload = {"model": _model, "messages": full, "stream": False,
                "options": _ollama_options(_model)}
    for _attempt in range(3):
        try:
            r = requests.post(_url, json=_payload, timeout=600)
            r.raise_for_status()
            _data = r.json()
            # Ollama /api/chat returns {"message": {"role":"assistant","content":"..."}}
            content = (
                _data.get("message", {}).get("content")
                or _data.get("response")  # /api/generate fallback
                or ""
            )
            if not content:
                raise RuntimeError("Ollama returned an empty response.")
            return _strip_think_tags(content)
        except requests.exceptions.ConnectionError:
            if _attempt < 2:
                _t_ol.sleep(3)
                continue
            raise RuntimeError(
                "❌ Ollama is not running.\n"
                "Fix: open a terminal and run:  ollama serve\n"
                "Then try again."
            )
        except requests.exceptions.Timeout:
            if _attempt < 2:
                _t_ol.sleep(5)
                continue
            raise RuntimeError(
                f"⏳ Ollama timed out on model '{_model}'.\n"
                "The model may still be loading — wait 30 seconds and try again.\n"
                f"Or run a lighter model: ollama pull qwen2.5:3b"
            )
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"❌ Ollama error: {e}")

def _do_ai_call(api_msgs):
    global ollama_models, ollama_reachable

    def _wake_ollama():
        global ollama_models, ollama_reachable
        if start_ollama_background():
            check_ollama.clear()
            _r, _m = check_ollama()
            st.session_state.ollama_reachable = _r
            st.session_state.ollama_models = _m
            ollama_reachable, ollama_models = _r, _m
            return _r
        return False

    def _best_ollama_model():
        """Return first available Ollama model name."""
        return ollama_models[0] if ollama_models else None

    if provider == "🔁 Auto (Smart Switch)":
        # ── Internet available: ALWAYS use Groq. call_groq handles all retries internally. ──
        if _has_internet() and st.session_state.api_key:
            return call_groq(api_msgs)
        # ── No internet: use Ollama ───────────────────────────────────────────
        if not ollama_reachable:
            _wake_ollama()
        _om = _best_ollama_model()
        if _om:
            return call_ollama(api_msgs, ollama_model=_om)
        if ollama_reachable:
            raise RuntimeError(
                "📥 Ollama is running but no models are installed.\n"
                "In the sidebar, click 'Pull Qwen 3' or 'Pull Moondream'."
            )
        raise RuntimeError(
            "📡 No internet and Ollama is not running.\n"
            "Connect to the internet or install Ollama for offline use."
        )

    elif provider == "Groq":
        return call_groq(api_msgs)

    else:  # Ollama (Offline)
        if not ollama_reachable:
            _wake_ollama()
        _om = _best_ollama_model()
        if not _om:
            raise RuntimeError(
                "📥 No offline models installed yet.\n"
                "In the sidebar click 'Pull Qwen 3' or 'Pull Moondream'."
            )
        # In Ollama-only mode, model_id is already the selected Ollama model
        return call_ollama(api_msgs, ollama_model=model_id)

# ── Chat input ────────────────────────────────────────────────────────────────
q_val      = st.session_state.pop("quick_q","") or voice_text

# ── Subscription expiry notice ────────────────────────────────────────────────
if not _IS_OWNER and st.session_state.get("_subscription_expired"):
    _exp_tier_name = st.session_state.get("_expired_tier", "Pro")
    st.warning(
        f"⏰ **Your 1-month Titan Ultra {_exp_tier_name} subscription has ended.**\n\n"
        f"You're back on Basic. Pay again to continue {_exp_tier_name} features — "
        f"or upgrade to the next plan.",
        icon=None
    )
    if st.button(f"🔱 Renew {_exp_tier_name} / Upgrade", key="_renew_btn", use_container_width=False):
        st.session_state.show_upgrade = True
        st.rerun()

if _USER_HIT_LIMIT:
    _usage_data_cur = _load_usage_data()
    _limit_hit_ts = _usage_data_cur.get("limit_hit_at") or _time_mod.time()
    _remaining_secs = max(0, int(5 * 3600 - (_time_mod.time() - _limit_hit_ts)))
    st.error("🚫 **You have hit your limits! Come back after your timer runs out.**\n\nFree users get **2 hours** of Titan Ultra. Want unlimited access? Payment options coming soon.")
    import streamlit.components.v1 as _cv1_timer
    _cv1_timer.html(f"""
<div style="text-align:center;padding:24px 0 8px;font-family:-apple-system,Segoe UI,sans-serif">
  <div style="font-size:.85rem;color:#a78bfa;letter-spacing:2px;margin-bottom:10px">⏳ TIME REMAINING BEFORE YOU CAN ASK AGAIN</div>
  <div id="tu_timer" style="font-size:3.2rem;font-weight:900;color:#f87171;letter-spacing:6px;font-variant-numeric:tabular-nums">--:--:--</div>
  <div id="tu_msg" style="margin-top:14px;font-size:.9rem;color:#6b7a99"></div>
</div>
<script>
var rem = {_remaining_secs};
function fmt(n){{return n.toString().padStart(2,'0');}}
function tick(){{
  if(rem<=0){{
    document.getElementById('tu_timer').innerHTML='00:00:00';
    document.getElementById('tu_timer').style.color='#34d399';
    document.getElementById('tu_msg').innerHTML='✅ <b style="color:#34d399">Time is up! You can now ask Titan Ultra questions again.</b>';
    setTimeout(function(){{window.location.reload();}},2000);
    return;
  }}
  var h=Math.floor(rem/3600),m=Math.floor((rem%3600)/60),s=rem%60;
  document.getElementById('tu_timer').innerHTML=fmt(h)+':'+fmt(m)+':'+fmt(s);
  rem--;
  setTimeout(tick,1000);
}}
tick();
</script>
""", height=160)
    st.stop()

# Chat input only shown during active chat (home screen has its own centered input)
if cur_msgs():
    _cmode = st.session_state.get("_titan_mode", "normal")
    if _cmode == "think":
        _cmode = "normal"
        st.session_state._titan_mode = "normal"
    _chat_ph = ("⚡ Fast Mode — Message TITAN ULTRA..." if _cmode == "fast"
                else "Message TITAN ULTRA...")
    _chat_result = st.chat_input(
        _chat_ph,
        accept_file=True,
        key="_chat_input_main",
    )
    if _chat_result:
        user_input = _chat_result.text or None
        if _chat_result.files:
            uploaded_file = _chat_result.files[0]
    else:
        user_input = None
else:
    _chat_result = None
    user_input = None

# Hidden mode-setter buttons — CSS hides on home screen; JS hides in chat mode
_hid_fast   = st.button("__TITAN_SET_FAST__",   key="_hid_mode_fast")
_hid_normal = st.button("__TITAN_SET_NORMAL__", key="_hid_mode_normal")
if _hid_fast:
    st.session_state._titan_mode = "fast";   st.rerun()
if _hid_normal:
    st.session_state._titan_mode = "normal"; st.rerun()

# Pick up message submitted from the home screen centered input
if not user_input and st.session_state.get("_home_pending"):
    user_input = st.session_state.pop("_home_pending")

# Pick up file attached from home screen + menu
if not uploaded_file and st.session_state.get("_home_upload_pending"):
    uploaded_file = st.session_state.pop("_home_upload_pending")

# ── Ctrl+V screenshot paste handler ──────────────────────────────────────────
import streamlit.components.v1 as _cv1_paste
_cv1_paste.html("""<script>
(function(){
    var pd=window.parent.document;
    if(pd.__titanPasteReady) return;
    pd.__titanPasteReady=true;
    pd.addEventListener('paste',function(ev){
        var items=(ev.clipboardData||window.clipboardData||{}).items;
        if(!items) return;
        for(var i=0;i<items.length;i++){
            var it=items[i];
            if(it.kind==='file' && it.type.indexOf('image/')===0){
                var f=it.getAsFile();
                if(!f) continue;
                var inp=pd.querySelector('[data-testid="stChatInput"] input[type="file"]');
                if(!inp) inp=pd.querySelector('section[data-testid="stMain"] input[type="file"]');
                if(!inp) continue;
                var dt=new DataTransfer();
                dt.items.add(f);
                try{
                    var proto=Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype,'files');
                    if(proto && proto.set) proto.set.call(inp,dt.files);
                    else inp.files=dt.files;
                }catch(e){ inp.files=dt.files; }
                inp.dispatchEvent(new Event('change',{bubbles:true}));
                inp.dispatchEvent(new InputEvent('input',{bubbles:true}));
                ev.preventDefault();
                break;
            }
        }
    });
})();
</script>""", height=0)

# ── + menu popup for chat bar ─────────────────────────────────────────────────
import streamlit.components.v1 as _cv1_plus
_cv1_plus.html("""<script>
(function(){
var pd=window.parent.document;
if(pd.__titanPlusReady) return;
pd.__titanPlusReady=true;

// ── shared popup ─────────────────────────────────────────────────────────────
var _s=pd.createElement('style');
_s.textContent=
'#tpop{display:none;position:fixed;background:#1a1a1a;border:1px solid #2a2a2a;'+
'border-radius:14px;padding:8px;z-index:99999;min-width:170px;'+
'box-shadow:0 6px 24px rgba(0,0,0,0.7);flex-direction:column;gap:4px;}'+
'.tpb{background:#222222;color:#e8e8e8;border:1px solid #2a2a2a;border-radius:8px;'+
'padding:9px 14px;cursor:pointer;text-align:left;font-size:13px;'+
'font-family:"Segoe UI",sans-serif;width:100%;display:block;}'+
'.tpb:hover{background:#2e2e2e;border-color:#555555;}'+
'.tpb.tpb-on{background:#2e2e2e;border-color:#888888;color:#ffffff;}';
pd.head.appendChild(_s);

var _pw=pd.createElement('div');
_pw.innerHTML='<div id="tpop">'+
'<button class="tpb" data-act="photos">📷  Photos</button>'+
'<button class="tpb" data-act="files">📎  Files</button>'+
'<hr style="border:none;border-top:1px solid #2d2d40;margin:4px 0">'+
'<button class="tpb" id="tpb-fast">⚡  Fast Mode</button>'+
'</div>';
pd.body.appendChild(_pw);
var _pop=pd.getElementById('tpop');
var _popAnchor=null; // which button opened the popup

function _refreshModeUI(){
    var mode=localStorage.getItem('titan_mode')||'normal';
    var fb=pd.getElementById('tpb-fast');
    if(!fb) return;
    fb.className='tpb'+(mode==='fast'?' tpb-on':'');
    fb.textContent=(mode==='fast'?'⚡  Fast Mode ✓':'⚡  Fast Mode');
}

function _openPopup(anchorEl){
    _popAnchor=anchorEl;
    _refreshModeUI();
    var r=anchorEl.getBoundingClientRect();
    var vh=pd.documentElement.clientHeight;
    _pop.style.left=r.left+'px';
    if(r.top>120){
        _pop.style.bottom=(vh-r.top+8)+'px';
        _pop.style.top='auto';
    }else{
        _pop.style.top=(r.bottom+8)+'px';
        _pop.style.bottom='auto';
    }
    _pop.style.display='flex';
}

function _clickHiddenBtn(txt){
    var all=pd.querySelectorAll('button');
    for(var i=0;i<all.length;i++){
        if(all[i].textContent.trim()===txt){all[i].click();return true;}
    }
    return false;
}

_pop.addEventListener('click',function(e){
    var btn=e.target.closest('.tpb');
    if(!btn) return;
    var act=btn.getAttribute('data-act')||btn.id;
    if(act==='photos'||act==='files'){
        var fi=pd.querySelector('[data-testid="stChatInput"] input[type="file"]')||pd.querySelector('input[type="file"]');
        if(fi){if(act==='photos')fi.setAttribute('accept','image/*');else fi.removeAttribute('accept');fi.click();}
    } else if(act==='tpb-fast'){
        var cur=localStorage.getItem('titan_mode')||'normal';
        var next=cur==='fast'?'normal':'fast';
        localStorage.setItem('titan_mode',next);
        _clickHiddenBtn(next==='fast'?'__TITAN_SET_FAST__':'__TITAN_SET_NORMAL__');
        _refreshModeUI();
    }
    _pop.style.display='none';
    e.stopPropagation();
});
pd.addEventListener('click',function(e){
    if(_pop.style.display!=='none' && !_pop.contains(e.target) && e.target!==_popAnchor)
        _pop.style.display='none';
});

// ── Chat screen: hook the + inside st.chat_input ─────────────────────────────
function _hookChatPlus(){
    var ci=pd.querySelector('[data-testid="stChatInput"]');
    if(!ci) return;
    var plusBtn=ci.querySelector('button');
    if(!plusBtn||plusBtn.__titanHooked) return;
    plusBtn.__titanHooked=true;
    plusBtn.addEventListener('click',function(e){
        e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();
        if(_pop.style.display==='flex'){_pop.style.display='none';}
        else{_openPopup(plusBtn);}
    },true);
}

// ── Unified Think button refresh ──────────────────────────────────────────────
function _refreshThinkBtns(){
    _refreshModeUI();
}

// ── Home screen: inject + INSIDE the text input ──────────────────────────────
function _injectHomePlus(){
    if(pd.querySelector('[data-testid="stChatMessage"]')) return;
    var inp=pd.querySelector('[data-testid="stMain"] [data-testid="stTextInput"] input');
    if(!inp) return;
    var wrap=inp.parentElement;
    while(wrap && wrap.getAttribute('data-testid')!=='stTextInput') wrap=wrap.parentElement;
    if(!wrap) wrap=inp.parentElement;
    if(wrap.querySelector('#home-plus-icon')) return;
    wrap.style.position='relative';
    var plus=pd.createElement('button');
    plus.id='home-plus-icon';
    plus.textContent='+';
    plus.style.cssText='position:absolute;left:16px;top:50%;transform:translateY(-50%);'+
        'background:transparent;border:none;color:#888888;font-size:1.3rem;cursor:pointer;'+
        'z-index:10;padding:0;line-height:1;font-weight:300;transition:color .15s;';
    plus.addEventListener('mouseover',function(){plus.style.color='#ffffff';});
    plus.addEventListener('mouseout',function(){plus.style.color='#888888';});
    plus.addEventListener('click',function(e){
        e.preventDefault();e.stopPropagation();
        if(_pop.style.display==='flex'){_pop.style.display='none';}
        else{_openPopup(plus);}
    });
    wrap.appendChild(plus);
}

// ── Chat screen: inject visible Think button inside st.chat_input ─────────────
function _injectChatThink(){}

// ── Hide mode buttons in chat mode (home screen hides them via CSS) ───────────
function _hideModeBtns(){
    var _hide=['TITAN_SET_FAST','TITAN_SET_THINK','TITAN_SET_NORMAL','TITAN_UPGRADE'];
    requestAnimationFrame(function(){
        pd.querySelectorAll('button').forEach(function(b){
            if(_hide.indexOf(b.textContent.trim())>=0){
                var el=b;
                for(var i=0;i<8;i++){
                    if(!el) break;
                    el.style.setProperty('display','none','important');
                    el.style.setProperty('height','0','important');
                    el.style.setProperty('overflow','hidden','important');
                    el.style.setProperty('margin','0','important');
                    el.style.setProperty('padding','0','important');
                    el.style.setProperty('max-height','0','important');
                    el=el.parentElement;
                }
            }
        });
    });
}

// ── Upgrade button — top-right corner of the page ─────────────────────────
function _injectUpgradeBtn(){
    if(pd.getElementById('titan-upgrade-btn')) return;
    var toolbar=pd.querySelector('[data-testid="stHeader"]')||pd.querySelector('header');
    if(!toolbar) return;
    var btn=pd.createElement('button');
    btn.id='titan-upgrade-btn';
    btn.innerHTML='🔱 <span style="color:#60a5fa;font-size:.8rem;font-weight:600">Upgrade</span>';
    btn.title='Upgrade to Titan Ultra Pro or Max';
    btn.style.cssText=
        'position:fixed;top:10px;right:18px;z-index:999999;'+
        'background:#1a1a1a;border:1px solid #2a2a2a;border-radius:8px;'+
        'padding:5px 12px 5px 10px;cursor:pointer;display:flex;align-items:center;gap:6px;'+
        'font-family:"Segoe UI",sans-serif;font-size:.85rem;color:#e8e8e8;'+
        'box-shadow:0 2px 8px rgba(0,0,0,0.5);transition:border-color .15s,background .15s;';
    btn.addEventListener('mouseover',function(){
        btn.style.background='#242424';
        btn.style.borderColor='#60a5fa';
    });
    btn.addEventListener('mouseout',function(){
        btn.style.background='#1a1a1a';
        btn.style.borderColor='#2a2a2a';
    });
    btn.addEventListener('click',function(){
        _clickHiddenBtn('__TITAN_UPGRADE__');
    });
    pd.body.appendChild(btn);
}

var _obs=new MutationObserver(function(){
    _hookChatPlus();
    _injectHomePlus();
    _injectChatThink();
    _hideModeBtns();
    _injectUpgradeBtn();
});
_obs.observe(pd.body,{childList:true,subtree:true});
_hookChatPlus();
_injectHomePlus();
_injectChatThink();
_hideModeBtns();
_refreshModeUI();
_injectUpgradeBtn();

// ── Ctrl+V paste image into chat ─────────────────────────────────────────────
pd.addEventListener('paste',function(e){
    var items=e.clipboardData&&e.clipboardData.items;
    if(!items) return;
    for(var i=0;i<items.length;i++){
        if(items[i].type.indexOf('image')!==-1){
            var file=items[i].getAsFile();
            if(!file) continue;
            var fi=pd.querySelector('[data-testid="stChatInput"] input[type="file"]')
                  ||pd.querySelector('input[type="file"]');
            if(!fi) continue;
            var dt=new DataTransfer();
            dt.items.add(new File([file],'pasted_image.png',{type:file.type||'image/png'}));
            fi.files=dt.files;
            fi.dispatchEvent(new Event('change',{bubbles:true}));
            e.preventDefault();
            break;
        }
    }
});
})();
</script>""", height=0)

# Process the file the user attached via the "+" popover
_current_vision = None
if uploaded_file:
    try:
        if uploaded_file.type and uploaded_file.type.startswith("image"):
            import base64 as _b64v
            _img_raw = uploaded_file.read()
            _mime = uploaded_file.type or "image/png"
            _current_vision = {
                "name": uploaded_file.name,
                "mime": _mime,
                "b64": _b64v.b64encode(_img_raw).decode("ascii"),
                "bytes": _img_raw,
            }
            file_content = f"[Image attached: {uploaded_file.name}]"
        elif uploaded_file.name.lower().endswith(('.csv', '.xlsx', '.xls')):
            try:
                _fname_lower = uploaded_file.name.lower()
                if _fname_lower.endswith('.csv'):
                    import csv as _csv, io as _csio
                    _raw = uploaded_file.read().decode("utf-8", errors="replace")
                    _reader = _csv.reader(_csio.StringIO(_raw))
                    _rows = list(_reader)
                    _ncols = len(_rows[0]) if _rows else 0
                    _nrows = len(_rows)
                    _preview = "\n".join([",".join(r) for r in _rows[:20]])
                    file_content = (f"[CSV FILE: {uploaded_file.name}]\n"
                                   f"Rows: {_nrows} | Columns: {_ncols}\n"
                                   f"Headers: {','.join(_rows[0]) if _rows else 'N/A'}\n\n"
                                   f"Preview (first 20 rows):\n{_preview}")
                else:
                    try:
                        import openpyxl as _xl
                    except ImportError:
                        import subprocess as _xlsp, sys as _xlsys
                        _xlsp.run([_xlsys.executable, "-m", "pip", "install", "openpyxl", "-q"], capture_output=True)
                        import openpyxl as _xl
                    import io as _xlio
                    _wb = _xl.load_workbook(_xlio.BytesIO(uploaded_file.read()), read_only=True, data_only=True)
                    _ws = _wb.active
                    _rows = list(_ws.iter_rows(values_only=True))
                    _nrows = len(_rows)
                    _ncols = len(_rows[0]) if _rows else 0
                    _preview = "\n".join([",".join(str(c) if c is not None else "" for c in r) for r in _rows[:20]])
                    file_content = (f"[EXCEL FILE: {uploaded_file.name}]\n"
                                   f"Rows: {_nrows} | Columns: {_ncols}\n"
                                   f"Headers: {','.join(str(c) for c in _rows[0]) if _rows else 'N/A'}\n\n"
                                   f"Preview (first 20 rows):\n{_preview}")
            except Exception as _csv_e:
                file_content = uploaded_file.read().decode("utf-8", errors="replace")
        elif uploaded_file.name.lower().endswith(".pdf"):
            try:
                _pdf_raw = uploaded_file.read()
                st.session_state["_uploaded_pdf_bytes"] = _pdf_raw
                st.session_state["_uploaded_pdf_name"]  = uploaded_file.name
                # Try to read text for context
                try:
                    import pdfplumber as _plmb, io as _io_pl
                    with _plmb.open(_io_pl.BytesIO(_pdf_raw)) as _pl_doc:
                        _total_pages = len(_pl_doc.pages)
                        _preview_txt = "\n".join(
                            (p.extract_text() or "") for p in _pl_doc.pages[:3]
                        )
                except Exception:
                    try:
                        import PyPDF2 as _p2r, io as _io_p2
                        _r2 = _p2r.PdfReader(_io_p2.BytesIO(_pdf_raw))
                        _total_pages = len(_r2.pages)
                        _preview_txt = " ".join(
                            (_r2.pages[i].extract_text() or "") for i in range(min(3, _total_pages))
                        )
                    except Exception:
                        _total_pages = 0
                        _preview_txt = ""
                file_content = (
                    f"[PDF: {uploaded_file.name} — {_total_pages} pages]\n"
                    f"Preview (first 3 pages):\n{_preview_txt[:1500]}"
                )
            except Exception:
                file_content = f"[PDF: {uploaded_file.name}]"
        else:
            file_content = uploaded_file.read().decode("utf-8", errors="replace")
    except Exception:
        file_content = f"[File: {uploaded_file.name}]"
st.session_state.pending_vision = _current_vision

# ── Inline PDF conversion: image + "convert to pdf" → download button ─────────
if _current_vision and user_input and any(
    kw in user_input.lower() for kw in ("convert to pdf", "convert this to pdf",
                                         "make pdf", "to pdf", "image to pdf",
                                         "screenshot to pdf", "convert pdf")
):
    try:
        from PIL import Image as _PILpdf
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Image as _RLImg
        _raw_bytes = _current_vision["bytes"]
        _img_pil = _PILpdf.open(io.BytesIO(_raw_bytes))
        if _img_pil.mode not in ("RGB","L"): _img_pil = _img_pil.convert("RGB")
        _ibuf = io.BytesIO()
        _img_pil.save(_ibuf, format="PNG"); _ibuf.seek(0)
        _pbuf = io.BytesIO()
        _pdoc = SimpleDocTemplate(_pbuf, pagesize=A4,
                                  leftMargin=20, rightMargin=20,
                                  topMargin=20, bottomMargin=20)
        _pw = A4[0] - 40; _ph = A4[1] - 40
        _iw, _ih = _img_pil.size
        _sc = min(_pw / _iw, _ph / _ih)
        _pdoc.build([_RLImg(_ibuf, width=_iw*_sc, height=_ih*_sc)])
        _pbuf.seek(0)
        _pname = _current_vision.get("name","image").rsplit(".",1)[0] + ".pdf"
        st.success(f"Done! Your PDF is ready: **{_pname}**")
        st.download_button("Download PDF", _pbuf.getvalue(),
                           _pname, "application/pdf", key="_chat_pdf_dl")
        st.session_state.pending_vision = None
    except Exception as _pdferr:
        st.error(f"Could not convert: {_pdferr}")
    st.stop()

if not user_input and q_val:
    user_input = q_val
# If the user submitted only a file (no text), give the model a default prompt
if not user_input and uploaded_file:
    user_input = "Please analyze the attached file."

if user_input:
    # ── Auto-detect memory commands ───────────────────────────────────────────
    import re as _re_mem
    _mem_cmd = _re_mem.match(
        r'.*?(?:remember(?:\s+(?:that|this))?|don\'t forget|note that|keep in mind)[:\s]+(.+)',
        user_input, _re_mem.IGNORECASE)
    if _mem_cmd:
        _fact = _mem_cmd.group(1).strip()
        _mkm = _re_mem.match(r"(?:my\s+)?(.+?)\s+is\s+(.+)", _fact, _re_mem.IGNORECASE)
        if _mkm:
            _k2, _v2 = _mkm.group(1).strip().lower(), _mkm.group(2).strip()
        else:
            _k2, _v2 = f"note_{len(st.session_state.titan_memory)}", _fact
        st.session_state.titan_memory[_k2] = _v2
        _save_memory(st.session_state.titan_memory)
        if _k2 == "name" and not _IS_OWNER:
            _register_this_device(_v2)

    if not st.session_state.api_key and provider == "Groq":
        st.error("❌ Service unavailable. Please try again later.")
    else:
        content = user_input + (f"\n\n[File]:\n{file_content}" if file_content else "")
        msgs = cur_msgs()
        msgs.append({"role":"user","content":content})
        set_msgs(msgs)

        sess = st.session_state.chat_sessions[st.session_state.active_session]
        if sess["title"] == "New Chat":
            sess["title"] = _make_session_title(user_input)
            _save_chat_sessions()

        if _is_pc_command_detect(user_input):
            try:
                result = pc_execute(user_input)
            except Exception as _pc_err:
                result = f"⚠️ Couldn't run that command: {_pc_err}"
            msgs = cur_msgs(); msgs.append({"role":"assistant","content":result}); set_msgs(msgs)
            st.rerun()
        else:
            # Morning briefing — auto-search + motivate
            if _is_morning_briefing(user_input):
                _mbq = "Search the web for today's top 5 news headlines and give a morning briefing with motivational start."
                _mb_search = _web_search(_mbq, max_results=5)
                if _mb_search:
                    msgs = cur_msgs()
                    msgs[-1]["content"] = user_input + f"\n\n[LIVE MORNING NEWS]:\n{_mb_search}\n\nUse this to give an energetic morning briefing."
                    set_msgs(msgs)

            # Screen capture — take screenshot and send to AI vision
            if _is_screen_capture_request(user_input):
                with st.spinner("📷 Capturing your screen..."):
                    _sc_vis = _capture_screenshot()
                if _sc_vis:
                    st.session_state.pending_vision = _sc_vis
                    st.toast("📷 Screenshot captured — analyzing...", icon="✅")
                else:
                    st.warning("Could not capture screen. Make sure PIL and mss are installed.")

            # Export chat as PDF — generate and show download button inline
            if _is_export_chat_request(user_input):
                _export_msgs = cur_msgs()[:-1]  # all but the just-added user message
                _pdf_data = _build_chat_pdf(_export_msgs)
                if _pdf_data:
                    msgs = cur_msgs()
                    msgs.append({"role": "assistant", "content": "📄 Your chat PDF is ready — click the button below to download it."})
                    set_msgs(msgs)
                    st.session_state["_pending_pdf"] = _pdf_data
                    st.rerun()
                else:
                    msgs = cur_msgs()
                    msgs.append({"role": "assistant", "content": "Sorry, PDF export failed. Make sure reportlab is installed: `pip install reportlab`"})
                    set_msgs(msgs)
                    st.rerun()

            # Auto-trigger live weather fetch when user asks about weather
            if _is_weather_query(user_input):
                import re as _re_wq
                _m_city = _re_wq.search(
                    r'(?:weather|temperature|forecast|climate)\s+(?:in|for|of|at)\s+(.+?)(?:\?|$)',
                    user_input, _re_wq.IGNORECASE)
                st.session_state.weather_query = _m_city.group(1).strip() if _m_city else user_input
            # YouTube transcript analysis
            _youtube_context = ""
            if _is_youtube_url(user_input):
                with st.spinner("📺 Fetching YouTube transcript..."):
                    _yt_vid, _yt_text = _get_youtube_transcript(user_input)
                    if _yt_text:
                        _youtube_context = f"[YOUTUBE TRANSCRIPT — Video ID: {_yt_vid}]\n{_yt_text}"

            # General URL / webpage reading
            _url_context = ""
            if not _youtube_context:
                _page_url = _extract_first_url(user_input)
                if _page_url and not _is_youtube_url(_page_url):
                    with st.spinner("🌐 Reading webpage..."):
                        _url_text = _fetch_url_content(_page_url)
                        if _url_text:
                            _url_context = f"[WEBPAGE CONTENT from {_page_url}]\n{_url_text}"

            # Deep Research mode
            _deep_results = ""
            if not _youtube_context and not _url_context and _is_deep_research(user_input):
                with st.spinner("🔬 Deep Research — searching multiple sources..."):
                    _deep_results = _deep_web_research(user_input)

            # System Health Diagram — full hardware scan with visual diagram
            _sys_health_html = ""
            if _is_system_health_request(user_input):
                with st.spinner("🔬 Scanning your system…"):
                    _sh_data = _run_system_health()
                    import hashlib as _hsh_sys
                    _shkey = _hsh_sys.md5(user_input.encode()).hexdigest()
                    _sys_health_html = _render_system_diagram(_sh_data)
                    st.session_state["_sys_health_cache"][_shkey] = _sys_health_html
                _issues = []
                if _sh_data['cpu_percent'] >= 85: _issues.append(f"CPU overloaded ({_sh_data['cpu_percent']}%)")
                if _sh_data['ram_percent'] >= 85: _issues.append(f"RAM almost full ({_sh_data['ram_percent']}%)")
                if _sh_data['disk_percent'] >= 85: _issues.append(f"Disk almost full ({_sh_data['disk_percent']}%)")
                if _sh_data['disk_status'] == 'WARNING': _issues.append("Disk health warning")
                if _sh_data.get('cpu_temp') and _sh_data['cpu_temp'] >= 88: _issues.append(f"CPU very hot ({_sh_data['cpu_temp']:.0f}°C)")
                if _sh_data.get('battery_percent') is not None and _sh_data['battery_percent'] < 20 and not _sh_data.get('battery_plugged'): _issues.append(f"Battery low ({_sh_data['battery_percent']}%)")
                _status = "✅ **All good — no problems found.**" if not _issues else "⚠️ **Issues found:** " + " | ".join(_issues)
                _summary = (
                    f"**Device:** {_sh_data.get('laptop_model','Unknown')}  \n"
                    f"**CPU:** {_sh_data.get('cpu_name','Unknown')} — {_sh_data['cpu_percent']}% used  \n"
                    f"**RAM:** {_sh_data['ram_used_gb']}GB / {_sh_data['ram_total_gb']}GB ({_sh_data['ram_percent']}%)  \n"
                    f"**Disk:** {_sh_data['disk_used_gb']}GB / {_sh_data['disk_total_gb']}GB ({_sh_data['disk_percent']}%)  \n"
                    + (f"**Battery:** {_sh_data['battery_percent']}% ({'Charging' if _sh_data.get('battery_plugged') else 'On battery'})  \n" if _sh_data.get('battery_percent') is not None else "")
                    + (f"**GPU:** {_sh_data['gpu_name']}  \n" if _sh_data.get('gpu_name') else "")
                    + f"\n{_status}"
                )
                msgs = cur_msgs()
                msgs.append({"role": "assistant", "content": _summary})
                set_msgs(msgs)
                st.rerun()

            # PC Diagnostics — auto-run when user reports PC issue
            _pc_diag = ""
            if not _sys_health_html and _is_pc_issue(user_input):
                with st.spinner("🖥️ Running PC diagnostics..."):
                    _pc_diag = _run_pc_diagnostics()

            # Error auto-fix — search for solution when user pastes an error
            _error_context = ""
            if not _pc_diag and _is_error_report(user_input):
                with st.spinner("🔍 Searching for error solution..."):
                    _error_context = _get_error_search(user_input)

            # Always search the web — live info for every message
            import datetime as _wsd
            _ws_today = _wsd.date.today().isoformat()
            _search_results = ""
            if not _youtube_context and not _url_context and not _deep_results:
                with st.spinner("⊙  Fetching latest information…"):
                    _search_results = _web_search(f"{user_input} {_ws_today}", max_results=6)
                    if _search_results:
                        _search_results = f"[Today: {_ws_today}]\n\n{_search_results}"

            # Connected app live search — auto-fetch when user asks about a connected app
            _conn_app_results = ""
            if not _search_results and not _youtube_context and not _url_context:
                _conn_apps_list = st.session_state.get("connected_apps", [])
                _mentioned_app  = next(
                    (app for app in _conn_apps_list if app.lower() in user_input.lower()),
                    None
                )
                if _mentioned_app:
                    import datetime as _cadt
                    _ca_date = _cadt.date.today().isoformat()
                    with st.spinner(f"🔍 Fetching live data from {_mentioned_app}…"):
                        _conn_app_results = _web_search(
                            f"{_mentioned_app} {user_input} {_ca_date}", max_results=10
                        )

            # ── PDF page extraction ───────────────────────────────────────────────
            _pdf_bytes_up = st.session_state.get("_uploaded_pdf_bytes")
            if _pdf_bytes_up and _is_pdf_extract_request(user_input):
                _pdf_range = _parse_pdf_page_range(user_input)
                if _pdf_range:
                    _ps, _pe = _pdf_range
                    with st.spinner(f"📄 Extracting pages {_ps}–{_pe}…"):
                        _ex_bytes, _ex_total = _extract_pdf_pages(_pdf_bytes_up, _ps, _pe)
                    if _ex_bytes:
                        _ex_name = st.session_state.get("_uploaded_pdf_name", "document.pdf")
                        _ex_out  = f"pages_{_ps}_to_{_pe}_{_ex_name}"
                        st.session_state["_pending_pdf_extract"] = (_ex_bytes, _ex_out)
                        _ex_reply = (
                            f"✅ Done! **Pages {_ps} to {_pe}** extracted from "
                            f"*{_ex_name}* ({_ex_total} pages total).\n\n"
                            f"Click the **Download** button below to get your PDF."
                        )
                    else:
                        _ex_reply = (
                            f"❌ Could not extract pages {_ps}–{_pe}. "
                            "Make sure the PDF is not password-protected and try again."
                        )
                    msgs = cur_msgs()
                    msgs.append({"role": "user",      "content": user_input})
                    msgs.append({"role": "assistant",  "content": _ex_reply})
                    set_msgs(msgs)
                    st.rerun()

            # ── AI Image generation (Pro + Max only) ────────────────────────────
            _gen_tier = st.session_state.get("titan_tier", "basic")
            if _gen_tier in ("pro", "max"):
                if _is_image_gen_request(user_input):
                    with st.spinner("🎨 Generating your image…"):
                        _img_raw = re.sub(
                            r'(?i)\b(generate|create|make|draw|show me|illustrate|visualize)\b'
                            r'\s*(?:a\s+|an\s+)?(?:image|photo|picture|artwork|illustration)\s*(?:of\s*)?',
                            '', user_input, count=1).strip() or user_input
                        _img_url = _gen_image_url(_img_raw, is_max=(_gen_tier == "max"))
                        if _gen_tier == "max":
                            _img_caption = (
                                f"[TITAN_IMAGE:{_img_url}]\n\n"
                                "✨ **Max-tier image** — generated with photorealistic Flux model, "
                                "designed to look completely real. Ask for any variation you want!"
                            )
                        else:
                            _img_caption = (
                                f"[TITAN_IMAGE:{_img_url}]\n\n"
                                "🎨 **Pro-tier image generated!** Want a different style or composition? Just ask!"
                            )
                    msgs = cur_msgs(); msgs.append({"role":"assistant","content":_img_caption}); set_msgs(msgs)
                    st.rerun()

            # ── Video generation (Pro: text→video | Max: text→video + image→video) ──
            if _is_video_gen_request(user_input):
                if _gen_tier == "basic":
                    _vid_locked = (
                        "🎬 **Video creation is a Pro and Max feature.**\n\n"
                        "Upgrade to **Pro** to generate cinematic videos from your descriptions, "
                        "or **Max** to also animate your own photos into videos."
                    )
                    msgs = cur_msgs(); msgs.append({"role":"assistant","content":_vid_locked}); set_msgs(msgs)
                    st.rerun()

                elif _gen_tier == "pro":
                    # Pro: text-to-video only (no image upload)
                    with st.spinner("🎬 Creating your cinematic video…"):
                        _vgif = _create_text_to_video(user_input)
                    _vgif_fname = "titan_pro_video.gif"
                    st.session_state["_pending_video_gif"] = (_vgif, _vgif_fname)
                    _vid_caption = (
                        "🎬 **Pro video created!** Cinematic animated video generated from your description.\n\n"
                        "Download it below. Want a different style? Try:\n"
                        "- *\"make it sunset colours, slow wave\"*\n"
                        "- *\"dark space galaxy, spinning\"*\n"
                        "- *\"ocean blue, radial zoom\"*"
                    )
                    msgs = cur_msgs(); msgs.append({"role":"user","content":user_input}); msgs.append({"role":"assistant","content":_vid_caption}); set_msgs(msgs)
                    st.rerun()

                elif _gen_tier == "max":
                    _vid_img = st.session_state.get("_uploaded_img_bytes")
                    if _vid_img:
                        # Max + image uploaded: animate the image
                        _vparams = _parse_video_effect(user_input)
                        _effect_names = {
                            "ken_burns": "Cinematic Ken Burns", "zoom_in": "Zoom In",
                            "zoom_out": "Zoom Out", "pan_right": "Pan Right",
                            "pan_left": "Pan Left", "pan_up": "Pan Up",
                            "pan_down": "Pan Down", "pulse": "Pulse / Breathe",
                            "fade_in": "Fade In", "shake": "Camera Shake",
                        }
                        _ename = _effect_names.get(_vparams["effect"], _vparams["effect"])
                        with st.spinner(f"🎬 Animating your image — {_ename}, {_vparams['duration']}s…"):
                            _vgif = _create_animated_gif(_vid_img, _vparams)
                        _vgif_fname = f"titan_max_video_{_vparams['effect']}_{_vparams['duration']}s.gif"
                        st.session_state["_pending_video_gif"] = (_vgif, _vgif_fname)
                        _vid_caption = (
                            f"🎬 **Max video created!** Effect: **{_ename}** · {_vparams['duration']}s · {_vparams['speed']} speed\n\n"
                            f"Your image has been animated — download below.\n\n"
                            f"Want a different effect? Ask — *\"zoom out\"*, *\"pan left\"*, *\"cinematic\"*, etc."
                        )
                    else:
                        # Max but no image: text-to-video
                        with st.spinner("🎬 Creating your cinematic video…"):
                            _vgif = _create_text_to_video(user_input)
                        _vgif_fname = "titan_max_video.gif"
                        st.session_state["_pending_video_gif"] = (_vgif, _vgif_fname)
                        _vid_caption = (
                            "🎬 **Max video created!** Cinematic animated video from your description.\n\n"
                            "Download below. To animate your own photo instead, upload an image first then ask again!"
                        )
                    msgs = cur_msgs(); msgs.append({"role":"user","content":user_input}); msgs.append({"role":"assistant","content":_vid_caption}); set_msgs(msgs)
                    st.rerun()

            # Generate animated diagram if requested
            if _is_diagram_request(user_input):
                import hashlib as _hlib_gen
                _dkey_gen = _hlib_gen.md5(user_input.encode()).hexdigest()
                if _dkey_gen not in st.session_state.diagram_cache:
                    with st.spinner("🎨 Generating animated diagram..."):
                        _dhtml_gen = _generate_diagram_html(user_input)
                        if _dhtml_gen:
                            st.session_state.diagram_cache[_dkey_gen] = _dhtml_gen

            with st.spinner("🔱 TITAN ULTRA is thinking…"):
                try:
                    _api_msgs = [{"role":m["role"],"content":m["content"]} for m in cur_msgs()]
                    _sys_diag_ctx = ""
                    if _sys_health_html and '_sh_data' in dir():
                        _sys_diag_ctx = (
                            f"REAL-TIME System Health Scan — answer ONLY from this data, do NOT guess:\n"
                            f"Device: {_sh_data.get('laptop_model','Unknown')} ({_sh_data['machine']})\n"
                            f"OS: {_sh_data['os']}\n"
                            f"CPU: {_sh_data.get('cpu_name','Unknown')} — {_sh_data['cpu_percent']}% usage, {_sh_data['cpu_cores']} cores"
                            + (f", {_sh_data['cpu_temp']:.0f}°C" if _sh_data.get('cpu_temp') else "") + "\n"
                            f"RAM: {_sh_data['ram_used_gb']}GB used / {_sh_data['ram_total_gb']}GB total ({_sh_data['ram_percent']}%)\n"
                            f"Disk: {_sh_data['disk_used_gb']}GB used / {_sh_data['disk_total_gb']}GB total ({_sh_data['disk_percent']}%) — Status: {_sh_data['disk_status']}\n"
                            + (f"Battery: {_sh_data['battery_percent']}% ({'charging' if _sh_data.get('battery_plugged') else 'on battery'})\n" if _sh_data.get('battery_percent') is not None else "")
                            + (f"GPU: {_sh_data['gpu_name']}, {_sh_data['gpu_temp']:.0f}°C\n" if _sh_data.get('gpu_name') else "")
                        )
                    _extra = _youtube_context or _url_context or _deep_results or _sys_diag_ctx or _pc_diag or _error_context or _conn_app_results or _search_results
                    if _extra:
                        _src_label = (
                            "YouTube transcript" if _youtube_context else
                            "webpage content" if _url_context else
                            "deep research results" if _deep_results else
                            "live system health scan data" if _sys_diag_ctx else
                            "live PC diagnostic data" if _pc_diag else
                            "error solution search results" if _error_context else
                            f"live {_mentioned_app} data" if _conn_app_results else
                            "web search results"
                        )
                        _api_msgs[-1]["content"] = (
                            f"{user_input}\n\n"
                            f"[LIVE {_src_label.upper()}]:\n{_extra}\n\n"
                            f"Use the above {_src_label} to give a complete, accurate answer. "
                            f"Mention sources where relevant."
                        )
                    answer = _do_ai_call(_api_msgs)
                    msgs = cur_msgs(); msgs.append({"role":"assistant","content":answer}); set_msgs(msgs)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

