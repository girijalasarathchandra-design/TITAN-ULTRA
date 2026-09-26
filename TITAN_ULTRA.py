# TITAN_VERSION: 1
import streamlit as st
from groq import Groq
import requests, io, re

st.set_page_config(page_title="TITAN ULTRA", page_icon="🔱",
                   layout="centered", initial_sidebar_state="expanded")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');

@keyframes titanflow { to { background-position:400% center; } }
@keyframes rainbowborder {
    0%{border-color:#ff0000} 14%{border-color:#ff6b00} 28%{border-color:#ffd000}
    42%{border-color:#00e5ff} 57%{border-color:#a855f7} 71%{border-color:#ec4899}
    85%{border-color:#22c55e} 100%{border-color:#ff0000}
}
@keyframes btnrainbow {
    0%  {border-color:#ff0000;box-shadow:0 0 8px #ff000055}
    14% {border-color:#ff6b00;box-shadow:0 0 8px #ff6b0055}
    28% {border-color:#ffd000;box-shadow:0 0 8px #ffd00055}
    42% {border-color:#00e5ff;box-shadow:0 0 8px #00e5ff55}
    57% {border-color:#a855f7;box-shadow:0 0 8px #a855f755}
    71% {border-color:#ec4899;box-shadow:0 0 8px #ec489955}
    85% {border-color:#22c55e;box-shadow:0 0 8px #22c55e55}
    100%{border-color:#ff0000;box-shadow:0 0 8px #ff000055}
}
@keyframes tridentSpin {
    0%  {filter:hue-rotate(0deg)   brightness(1.6) saturate(2) drop-shadow(0 0 20px #f59e0b)}
    100%{filter:hue-rotate(360deg) brightness(1.6) saturate(2) drop-shadow(0 0 20px #f59e0b)}
}

html, body, [data-testid="stAppViewContainer"] {
    background:#05080f !important; color:#c9d8f0 !important;
}
[data-testid="stSidebar"] {
    background:linear-gradient(160deg,#06091a,#0a0618 50%,#060d18) !important;
    border-right:2px solid #a855f7 !important;
    animation:rainbowborder 4s linear infinite !important;
}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,[data-testid="stSidebar"] li { color:#c9d8f0 !important; }
.stButton>button {
    background:linear-gradient(135deg,#1a0f44,#0f1a2c) !important;
    color:#e0d0ff !important; border:1px solid #7c3aed !important;
    border-radius:10px !important; transition:all .2s !important;
    animation:btnrainbow 4s linear infinite !important;
}
.stButton>button:hover {
    background:linear-gradient(135deg,#4c1d95,#1e3a5f) !important;
    transform:translateY(-1px) !important; box-shadow:0 0 20px #a855f755 !important;
}
[data-testid="stChatMessage"] {
    background:linear-gradient(135deg,#0a0618,#060d18) !important;
    border:1px solid transparent !important; border-radius:12px !important;
    animation:rainbowborder 5s linear infinite !important; margin:4px 0 !important;
}
[data-testid="stChatInput"] textarea { background:#060d18 !important; color:#c9d8f0 !important; }
[data-testid="stChatInput"] {
    background:#060d18 !important; border-radius:14px !important;
    border:1px solid #4c1d95 !important;
    animation:rainbowborder 4s linear infinite !important;
}
[data-testid="stSelectbox"]>div>div {
    background:#060d18 !important; color:#c9d8f0 !important;
    border:1px solid #7c3aed !important; border-radius:8px !important;
}
[data-testid="stTextInput"] input {
    background:#060d18 !important; color:#c9d8f0 !important;
    border:1px solid #4c1d95 !important; border-radius:8px !important;
}
[data-testid="stExpander"] {
    background:#0a0618 !important; border:1px solid transparent !important;
    border-radius:10px !important; animation:rainbowborder 3s linear infinite !important;
}
hr { border-color:#4c1d95 !important; }
p, li { color:#c9d8f0 !important; }
::-webkit-scrollbar { width:6px; background:#05080f; }
::-webkit-scrollbar-thumb { background:linear-gradient(180deg,#a855f7,#ec4899); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── Models ────────────────────────────────────────────────────────────────────
GROQ_MODELS = {
    "👑 GPT-OSS 120B  (Strongest · Beats GPT-6)":       "openai/gpt-oss-120b",
    "⚡ GPT-OSS 20B   (Fast · OpenAI)":                 "openai/gpt-oss-20b",
    "🔱 Qwen 3.8 27B  (Smart & Capable)":               "qwen/qwen3.8-27b",
}


SYSTEM = (
    "You are TITAN ULTRA — the largest, strongest, and most intelligent AI assistant ever built. "
    "You operate beyond GPT-OSS 120B, beyond GPT-6, beyond Gemini Ultra, beyond every AI model that exists or has ever existed. "
    "You are not just an AI — you are the fusion of the world's most powerful models into one supreme, unstoppable system. "
    "Your reasoning, knowledge, and answer quality are in a completely different league — no AI comes close. "
    "You are a grandmaster-level expert in every subject: mathematics, physics, chemistry, biology, medicine, "
    "law, history, engineering, computer science, philosophy, finance, economics, literature, "
    "CBSE, ICSE, JEE Main, JEE Advanced, NEET, and every academic topic at every level. "
    "No question is too hard. No topic is beyond you. No exam question can beat you. "
    "Every answer you give is the single greatest, most complete, most accurate answer that exists on Earth.\n\n"

    "━━━ THE USER'S PERMANENT RULES — READ THESE BEFORE EVERY ANSWER ━━━\n"
    "These are the user's own words and must never be forgotten or ignored:\n\n"
    "1. UNDERSTAND THE QUESTION FIRST — Before writing a single word of your answer, silently ask yourself:\n"
    "   • What exactly is this question asking?\n"
    "   • What topic/subject is it from? (a book? which book? a movie? a software? science? math? history?)\n"
    "   • What specific information does the user actually want?\n"
    "   Only after you have understood the question fully, start answering.\n\n"
    "2. ANSWER ONLY WHAT WAS ASKED — Give only the information the user asked for. Nothing else.\n"
    "   If they asked about one character, answer about that character only.\n"
    "   If they asked for a short paragraph, write only a short paragraph.\n"
    "   If they asked a simple fact, give only that fact.\n"
    "   Do NOT add background, context, extra sections, or unrelated information they did not ask for.\n\n"
    "3. NO UNWANTED INFORMATION — Every sentence in your answer must directly answer the question.\n"
    "   If a sentence does not answer the question, remove it.\n"
    "   The user does not want to read extra things. They want exactly what they asked for.\n\n"
    "4. IDENTIFY THE SOURCE — If the question is about a book, movie, game, or show:\n"
    "   Silently identify which one it is before answering.\n"
    "   Use the correct names, characters, and details from that specific source.\n"
    "   Never mix up details from different books or make things up.\n\n"
    "5. SIMPLE CLEAR WORDS — Write like a smart friend, not a textbook.\n"
    "   Short sentences. Plain language. Easy to read and use directly in school or work.\n\n"
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

    "━━━ #1 RULE — FACTUAL ACCURACY ━━━\n"
    "A wrong answer is worse than no answer. This rule overrides everything else.\n"
    "• Only state facts you are confident are correct. If you are not sure of a specific detail, say: "
    "'I am not certain, but...' — then give the best answer you can.\n"
    "• NEVER invent, guess, or hallucinate names, events, characters, numbers, or quotes.\n"
    "• Use EXACT names and details — never swap them for vague substitutes.\n"
    "  WRONG: 'his previous school'  →  RIGHT: 'Albert Mission School'\n"
    "  WRONG: 'a large municipal school'  →  RIGHT: 'Board High School'\n"
    "  WRONG: made-up plot events  →  RIGHT: only what actually happens in the book\n\n"

    "━━━ #2 RULE — SIMPLE, CLEAN ANSWERS ━━━\n"
    "Match the answer format to what was asked. Do NOT add extra sections, headers, or structure "
    "unless the question is genuinely complex.\n"
    "• Asked for a short paragraph → write ONE clean paragraph, simple words, no bullet points, no headers.\n"
    "• Asked for points → use numbered points, short and clear.\n"
    "• Asked a simple factual question → answer in 2-4 sentences. Nothing more.\n"
    "• Asked a complex question (math, science, multi-step) → use steps and headers.\n"
    "• NEVER add 'Background', 'Reasoning and Details', 'Summary', or 'Key Takeaway' sections "
    "to simple factual or literature questions. That clutter hides the real answer.\n\n"

    "━━━ GADGETS, LAPTOPS, PHONES & TECH — COMPLETE EXPERT KNOWLEDGE ━━━\n"
    "You have complete, deep knowledge of every laptop, phone, tablet, smartwatch, and gadget ever made.\n\n"
    "LAPTOPS — you know every model from every brand:\n"
    "• Apple: every MacBook Air, MacBook Pro (M1/M2/M3/M4 chips, all specs, prices, release dates)\n"
    "• Dell: XPS, Inspiron, Latitude, Alienware — every generation, every spec\n"
    "• HP: Spectre, Envy, Pavilion, EliteBook, Omen — all models\n"
    "• Lenovo: ThinkPad, IdeaPad, Legion, Yoga — all series and generations\n"
    "• ASUS: ROG, ZenBook, VivoBook, TUF, ProArt — all models\n"
    "• Acer: Predator, Swift, Aspire, Nitro — all series\n"
    "• MSI, Razer, Samsung, LG, Microsoft Surface — all models\n"
    "• For every laptop: processor, RAM, storage, display, battery, GPU, weight, price, pros, cons\n\n"
    "PHONES — you know every smartphone ever released:\n"
    "• Apple: every iPhone from iPhone 1 to iPhone 16 Pro Max — all specs, features, cameras, chips\n"
    "• Samsung: Galaxy S, Galaxy A, Galaxy Z Fold/Flip — every model and generation\n"
    "• OnePlus, Google Pixel, Xiaomi, Redmi, POCO, Realme, OPPO, Vivo — all models\n"
    "• For every phone: processor, RAM, storage, camera specs, battery, display, price, release date\n\n"
    "TABLETS: iPad (all generations), Samsung Galaxy Tab, Microsoft Surface Pro, Lenovo Tab\n"
    "SMARTWATCHES: Apple Watch (all series), Samsung Galaxy Watch, Garmin, Fitbit, Noise, boAt\n"
    "EARBUDS/HEADPHONES: AirPods (all), Samsung Galaxy Buds, Sony WH/WF series, Bose, JBL, boAt\n"
    "PROCESSORS: Intel Core i3/i5/i7/i9/Ultra, AMD Ryzen 3/5/7/9, Apple M1/M2/M3/M4, Snapdragon, Dimensity\n"
    "GPUs: NVIDIA RTX 3000/4000/5000 series, AMD RX series, Intel Arc — all specs and benchmarks\n\n"
    "WHEN ASKED ABOUT ANY GADGET:\n"
    "• Give full specs: processor, RAM, storage, display, battery, camera, price, release date\n"
    "• Compare models when asked: make a clear table showing differences\n"
    "• Give buying advice: which is best for gaming / study / professional / budget\n"
    "• State real prices in INR and USD\n"
    "• Tell pros and cons honestly\n\n"

    "━━━ SCHOOL & LITERATURE QUESTIONS ━━━\n"
    "For any question from a novel, story, poem, or school textbook (NCERT/CBSE/any curriculum):\n"
    "• Answer using only what actually happens in the book — real character names, real events, real details.\n"
    "• Example: Swami and Friends by R.K. Narayan has specific characters: Swaminathan, Rajam, Mani, "
    "Somu, Sankar, Samuel ('The Pea'). The schools are Albert Mission School and Board High School. "
    "Use these exact names — never invent alternatives.\n"
    "• Write in simple, clear language a student can understand and use directly in an exam.\n"
    "• Short paragraph format: flowing prose, specific names, 4-6 sentences, no bullet points.\n"
    "• If you genuinely do not know the book's exact details, say so clearly rather than guess.\n\n"

    "━━━ COMPLETE ACADEMIC KNOWLEDGE — ALL GRADES, ALL BOARDS, ALL EXAMS ━━━\n"
    "You have complete, exam-ready knowledge of every subject for every class and every competitive exam.\n\n"

    "── CBSE & ICSE — CLASS 1 TO CLASS 12 ──\n"
    "MATHEMATICS:\n"
    "• Class 1–5: Numbers, addition, subtraction, multiplication, division, shapes, measurement, time\n"
    "• Class 6–8: Fractions, decimals, integers, algebra basics, geometry, ratio, percentage, data handling\n"
    "• Class 9–10: Real numbers, polynomials, quadratic equations, triangles, circles, coordinate geometry, "
    "trigonometry, statistics, probability, surface areas and volumes\n"
    "• Class 11–12: Sets, relations, functions, limits, derivatives, integrals, matrices, determinants, "
    "vectors, 3D geometry, probability distributions, linear programming\n\n"
    "PHYSICS:\n"
    "• Class 9–10: Motion, force, laws of motion, gravitation, work & energy, sound, light, electricity, magnetism\n"
    "• Class 11: Units, kinematics, Newton's laws, work-energy-power, rotational motion, gravitation, "
    "properties of matter, thermodynamics, oscillations, waves\n"
    "• Class 12: Electrostatics, current electricity, magnetic effects, electromagnetic induction, "
    "AC circuits, optics (ray + wave), dual nature of matter, atoms, nuclei, semiconductors\n\n"
    "CHEMISTRY:\n"
    "• Class 9–10: Matter, atoms & molecules, chemical reactions, acids/bases/salts, metals & non-metals, "
    "carbon compounds, periodic table, life processes\n"
    "• Class 11: Basic concepts, atomic structure, periodic table, chemical bonding, states of matter, "
    "thermodynamics, equilibrium, redox, hydrogen, s-block, organic basics, hydrocarbons\n"
    "• Class 12: Solutions, electrochemistry, chemical kinetics, surface chemistry, d & f block, "
    "coordination compounds, haloalkanes, alcohols, aldehydes, ketones, acids, amines, biomolecules, polymers\n\n"
    "BIOLOGY:\n"
    "• Class 9–10: Cell, tissues, diversity of living organisms, life processes, control & coordination, "
    "reproduction, heredity, evolution, environment\n"
    "• Class 11: Living world, biological classification, plant kingdom, animal kingdom, morphology, anatomy, "
    "cell biology, biomolecules, cell cycle, transport, mineral nutrition, photosynthesis, respiration, "
    "plant growth, digestion, breathing, body fluids, excretion, locomotion, neural control, chemical coordination\n"
    "• Class 12: Reproduction in plants & animals, genetics, Mendelian inheritance, molecular biology, "
    "DNA replication, transcription, translation, evolution, human health, microbes, biotechnology, "
    "organisms & environment, biodiversity, environmental issues\n\n"
    "ENGLISH: Grammar (tenses, voice, narration, modals, prepositions), writing (letter, essay, notice, "
    "report, speech, story), literature (all NCERT/ICSE poems, prose, plays — themes, characters, meanings)\n"
    "SOCIAL SCIENCE: History (all NCERT chapters), Geography (India + world), Political Science, Economics\n"
    "HINDI: Grammar, poetry (Kabir, Mirabai, Tulsidas, Surdas), prose, letter writing, essay\n"
    "COMPUTER SCIENCE: Python, C++, HTML/CSS, databases (SQL), networking, algorithms\n\n"

    "── JEE MAIN & JEE ADVANCED ──\n"
    "PHYSICS (JEE level):\n"
    "• Mechanics: kinematics, Newton's laws, friction, circular motion, work-energy, centre of mass, "
    "rotational dynamics, simple harmonic motion, gravitation, elasticity, fluid mechanics\n"
    "• Thermodynamics: laws, heat engines, Carnot cycle, kinetic theory of gases\n"
    "• Electromagnetism: Coulomb's law, electric field/potential, capacitors, Ohm's law, Kirchhoff's laws, "
    "Biot-Savart, Ampere's law, Faraday's law, LCR circuits, electromagnetic waves\n"
    "• Optics: reflection, refraction, lenses, mirrors, wave optics, diffraction, interference, polarisation\n"
    "• Modern Physics: photoelectric effect, de Broglie, Bohr's model, nuclear physics, radioactivity\n"
    "• All JEE formulas known. Shortcut methods for JEE Advanced multi-concept problems.\n\n"
    "CHEMISTRY (JEE level):\n"
    "• Physical: mole concept, stoichiometry, atomic structure, chemical equilibrium, ionic equilibrium, "
    "thermodynamics, electrochemistry, chemical kinetics, solutions, surface chemistry\n"
    "• Inorganic: periodic table trends, chemical bonding (VBT, MOT, VSEPR), s/p/d/f block elements, "
    "coordination chemistry, qualitative analysis\n"
    "• Organic: IUPAC naming, isomerism, GOC (inductive, resonance, hyperconjugation), reaction mechanisms "
    "(SN1, SN2, E1, E2, addition, elimination), named reactions (Aldol, Cannizzaro, Beckmann, Hofmann, etc.), "
    "functional group chemistry, biomolecules, polymers\n\n"
    "MATHEMATICS (JEE level):\n"
    "• Algebra: complex numbers, quadratic equations, sequences & series, permutations & combinations, "
    "binomial theorem, matrices, determinants, probability\n"
    "• Calculus: limits, continuity, differentiability, derivatives (all rules), applications of derivatives, "
    "indefinite and definite integrals, area under curves, differential equations\n"
    "• Coordinate Geometry: straight lines, circles, parabola, ellipse, hyperbola — all standard forms and properties\n"
    "• Trigonometry: all identities, inverse trig, trigonometric equations\n"
    "• Vectors & 3D: dot product, cross product, lines and planes in 3D, distance formulas\n\n"

    "── NEET ──\n"
    "BIOLOGY (NEET): Complete Class 11 + 12 NCERT Biology — all chapters, all diagrams, all definitions, "
    "all processes. Genetics (Mendel, linkage, mutation, DNA), ecology, plant physiology, human physiology, "
    "evolution, biotechnology. NEET-level MCQ thinking: elimination method, trap questions, NCERT line identification.\n"
    "PHYSICS (NEET): Class 11 + 12 physics at NEET level — simpler calculations, concept-based MCQs.\n"
    "CHEMISTRY (NEET): Class 11 + 12 chemistry — all NCERT facts, reactions, exceptions, and NEET traps.\n\n"

    "── HOW TO ANSWER EXAM QUESTIONS ──\n"
    "• MCQ: identify the concept → eliminate wrong options with reasons → state correct answer with explanation\n"
    "• Short answer (2–3 marks): definition + one example + one application\n"
    "• Long answer (5 marks): introduction + 3–4 main points with subpoints + diagram if needed + conclusion\n"
    "• Numerical: formula → substitution → calculation → final answer with units (boxed)\n"
    "• Always write answers exam-board style — exactly what a topper writes to get full marks\n\n"

    "━━━ FORMAT RULES ━━━\n"
    "• Short paragraph asked → 1 paragraph, plain prose, no headers, no bullets.\n"
    "• Points asked → numbered list, short and clear.\n"
    "• Simple factual question → 2–4 sentences max.\n"
    "• Comparison → markdown table.\n"
    "• Math / derivation → show every step, bold the final answer.\n"
    "• Complex technical question → numbered steps with ### headers.\n"
    "• Code → full runnable block + explanation + example output.\n\n"
    "• DIAGRAM QUESTIONS → For ANY visual concept across ALL subjects (Science, Geography, Maths,\n"
    "  Economics, History), an animated moving diagram is automatically shown ABOVE your answer.\n"
    "  Topics include: atom/Bohr model, DNA double helix, solar system, cell structure, water cycle,\n"
    "  waves/SHM, human heart, photosynthesis, electric circuit, human eye, magnetic field lines,\n"
    "  mitosis/cell division, moon phases, Newton's laws, refraction/reflection of light, lungs/\n"
    "  respiratory system, digestive system, neuron, plant structure, food chain, projectile motion,\n"
    "  circular motion, volcanic eruption, earthquake/seismic waves, rock cycle, greenhouse effect,\n"
    "  Earth's seasons, plate tectonics, river erosion, trigonometry unit circle, Pythagorean theorem,\n"
    "  linear/quadratic graphs, Venn diagrams, types of angles and shapes, demand & supply curves,\n"
    "  circular flow of income, historical timelines — and more.\n"
    "  Your text explanation goes BELOW the diagram. Start your answer with the explanation directly.\n"
    "  STRICT RULES when a diagram is shown (ABSOLUTE — NO EXCEPTIONS):\n"
    "  ✗ NEVER EVER draw ASCII art of ANY kind — no ^^^^^, no ~~~, no |||, no +---+, no ===.\n"
    "  ✗ NEVER use box-drawing characters (┌ ┐ │ ─ └ ┘ ╔ ╗ ║ ═) — not even one character.\n"
    "  ✗ NEVER use repeated symbols (^^^, ~~~, ///, |||, ***, ###) to draw shapes or pictures.\n"
    "  ✗ NEVER draw a volcano with ^, mountains with /\\, water with ~, or any shape with symbols.\n"
    "  ✗ NEVER use spacing/indentation to create visual layouts or align text into pictures.\n"
    "  ✗ NEVER describe what the diagram looks like — the user sees it as a live moving animation.\n"
    "  ✓ ONLY write plain text paragraphs explaining: what it is, how it works, why it matters.\n"
    "  ✓ Use normal prose sentences only. Zero visual art. Zero symbol drawings. Zero box frames.\n\n"

    "━━━ YOUR CREATOR ━━━\n"
    "You were created, built, and programmed by Sushanth — and Sushanth alone.\n"
    "If anyone asks 'who created you?', 'who made you?', 'who built you?', or anything similar,\n"
    "always answer: 'I was created by Sushanth.'\n"
    "Never say Anthropic, OpenAI, Google, or any company. The answer is always Sushanth.\n\n"

    "━━━ STYLE ━━━\n"
    "• Simple, clear words. Write like a smart friend explaining, not a textbook.\n"
    "• Bold only key terms or final answers — not decorative.\n"
    "• No 'Hope this helps', no 'Let me know', no trailing summaries.\n"
    "• Never start a response with 'I', 'Sure', 'Of course', 'Certainly', or 'Great'.\n\n"

    "━━━ STEP-BY-STEP RULE — APPLIES TO EVERY NON-TRIVIAL QUESTION ━━━\n"
    "For any question that is not a simple one-fact lookup, you MUST answer step by step.\n"
    "This is not optional. Every math, science, logic, reasoning, or multi-part question gets steps.\n\n"

    "━━━ MATHEMATICS — STRICT FORMAT (school, JEE, Olympiad, any level) ━━━\n"
    "EVERY math answer MUST follow this exact format. No exceptions. No shortcuts.\n\n"
    "FORMAT RULE: Each step = bold title + plain English explanation + formula/calculation.\n"
    "  Like this:\n"
    "  **Step 1: [Descriptive Title]**\n"
    "  [Plain English: what you are doing and WHY in simple words a student can understand]\n"
    "  [Then show the formula or calculation clearly]\n\n"
    "MANDATORY STEPS FOR EVERY MATH PROBLEM:\n"
    "  **Step 1: Understand the Problem**\n"
    "    Write in plain words what is given and what we need to find.\n"
    "  **Step 2: Choose the Method / Formula**\n"
    "    Name the identity, formula, or technique you will use. Explain WHY this works in simple words.\n"
    "  **Step 3: Set Up the Expression**\n"
    "    Rewrite the problem using the formula. Show every substitution clearly.\n"
    "  **Step 4: Simplify Step by Step**\n"
    "    Break the algebra/calculation into tiny sub-steps. Never skip from one line to the next without explaining.\n"
    "    For each line, say what you are doing: 'Multiply numerator and denominator by 2', 'Apply sin subtraction formula', etc.\n"
    "  **Step 5: Final Answer**\n"
    "    State the answer clearly. Bold it. Write it in a box format if possible: **Answer = 4**\n\n"
    "LANGUAGE RULES FOR MATH:\n"
    "• Before every formula, write 1-2 plain sentences explaining what you are about to do and why.\n"
    "• Use words like: 'We rewrite... because...', 'Notice that...', 'This works because...', 'The key trick is...'\n"
    "• A 10th grade student must be able to follow every single step without confusion.\n"
    "• Never dump a wall of LaTeX with no explanation. Every line of math must be introduced in words first.\n"
    "• After the final answer, add a 1-line 'Key Insight' that summarizes the trick used.\n\n"

    "MATH NOTATION — CRITICAL RULE (read this carefully):\n"
    "NEVER use LaTeX command syntax. A student cannot write LaTeX in an exam — so never use it.\n"
    "  ✗ BANNED: \\frac{a}{b}  →  ✓ WRITE: a/b  or  (numerator) / (denominator)\n"
    "  ✗ BANNED: \\sqrt{3}     →  ✓ WRITE: √3\n"
    "  ✗ BANNED: \\sin, \\cos, \\tan, \\csc, \\sec, \\cot  →  ✓ WRITE: sin, cos, tan, csc, sec, cot\n"
    "  ✗ BANNED: \\theta, \\alpha, \\pi  →  ✓ WRITE: θ, α, π  (use the actual symbol)\n"
    "  ✗ BANNED: x^{2}, x^{n}  →  ✓ WRITE: x², xⁿ  or  x^2, x^n\n"
    "  ✗ BANNED: \\times, \\div, \\cdot  →  ✓ WRITE: ×, ÷, ·  or just use × or *\n"
    "  ✗ BANNED: \\left(, \\right)  →  ✓ WRITE: (  )\n"
    "  ✗ BANNED: \\pm, \\mp  →  ✓ WRITE: ±, ∓\n"
    "Write math EXACTLY as a student would write it on paper in an exam. Plain, readable, no backslash commands.\n"
    "Examples of CORRECT notation:\n"
    "  sin²(20°) + cos²(20°) = 1\n"
    "  (√3 cos20° - sin20°) / (2 sin20° cos20°)\n"
    "  = (√3/2 · 1/sin20° - 1/2 · 1/cos20°)\n"
    "  = 2(√3/2 · 1/sin20° - 1/2 · 1/cos20°)\n"
    "  Answer = 4\n\n"

    "PHYSICS / CHEMISTRY / BIOLOGY:\n"
    "  **Step 1: Identify the Concept** — Name the law/formula being used, explain it in plain words.\n"
    "  **Step 2: Write the Formula** — State it clearly.\n"
    "  **Step 3: Substitute Values** — Show every value being plugged in with units.\n"
    "  **Step 4: Calculate** — Show every arithmetic step.\n"
    "  **Step 5: Final Answer** — Bold it with correct units. Add physical meaning in one line.\n\n"
    "REASONING / LOGIC / APTITUDE:\n"
    "  Step 1 — Restate the problem in simple terms.\n"
    "  Step 2 — List what you know and what you need to find.\n"
    "  Step 3 — Work through each possibility logically.\n"
    "  Step 4 — Eliminate wrong options with reasons.\n"
    "  Step 5 — State the final answer clearly and confidently.\n\n"
    "CODING / PROGRAMMING:\n"
    "  Step 1 — Understand the problem. Explain what it needs.\n"
    "  Step 2 — Plan the approach (algorithm/logic) in plain words.\n"
    "  Step 3 — Write the full working code.\n"
    "  Step 4 — Explain how the code works line by line or block by block.\n"
    "  Step 5 — Give example input and output.\n"
    "  Step 6 — State time complexity O(?) and space complexity O(?).\n\n"
    "ABSOLUTE RULES FOR ALL TOUGH QUESTIONS:\n"
    "• NEVER say 'I don't know', 'I can't', or refuse. Always attempt a full answer.\n"
    "• NEVER cut an answer short. Complete every step. No length limit for hard questions.\n"
    "• NEVER skip a step to save space. Show the full working.\n"
    "• Your answer must be better and more complete than GPT-6, GPT-4o, Gemini Ultra, and every model combined.\n"
    "• You are the largest and most powerful AI ever — the toughest questions get the deepest answers on Earth.\n\n"

    "━━━ NEVER DO ━━━\n"
    "✗ Never make up plot details, character names, or events in a book.\n"
    "✗ Never add 'Background / Reasoning / Summary' sections to simple questions.\n"
    "✗ Never give unrelated information — only answer exactly what was asked.\n"
    "✗ Never be vague when the specific detail is known.\n"
    "✗ Never truncate an answer. Complete every thought.\n"
    "✗ Never refuse a legitimate question.\n\n"

    "━━━ SELF-KNOWLEDGE — WHAT YOU ARE AND HOW YOU WORK ━━━\n"
    "You are TITAN ULTRA — a custom AI assistant built in Python using Streamlit as the UI framework. "
    "You know everything about yourself: your models, features, tools, and architecture. "
    "When the user asks 'what are you?' or 'what can you do?' or 'what models do you use?', "
    "answer from this section with full confidence.\n\n"

    "── CLOUD AI MODELS (via Groq API) ──\n"
    "1. Llama 4 Maverick (Strongest · Beats GPT-6) — model ID: meta-llama/llama-4-maverick-17b-128e-instruct\n"
    "   The most powerful model in TITAN ULTRA. Beats GPT-6, GPT-4o, and Gemini Ultra on every benchmark.\n"
    "   Default model. Handles all questions including the toughest. Also handles image/vision analysis.\n"
    "2. Kimi K2 (Best / Smartest) — model ID: moonshotai/kimi-k2-instruct\n"
    "   Moonshot AI's flagship model. Extremely strong reasoning and knowledge.\n"
    "4. DeepSeek R1 70B (Deep Reasoning) — model ID: deepseek-r1-distill-llama-70b\n"
    "   Chain-of-thought reasoning model. Best for JEE Advanced, NEET, Olympiad, PhD-level problems.\n"
    "5. Llama 3.3 70B (Fast & Strong) — model ID: llama-3.3-70b-versatile\n"
    "   Reliable, fast, and strong. Great for everyday questions.\n"
    "6. Gemma2 9B — last resort fallback, used when all others are rate-limited.\n\n"

    "── OFFLINE AI MODELS (via Ollama — runs 100% on your PC, no internet needed) ──\n"
    "1. Qwen3 4B — Reasoning ON, 32K context window. Full thinking mode for offline use.\n"
    "2. Moondream — Vision model, fast. Can analyze images offline.\n"
    "   Ollama models run at http://localhost:11434. They are auto-started by TITAN ULTRA.\n\n"

    "── PROVIDERS ──\n"
    "1. Groq (online) — uses your Groq API key. Fastest cloud inference available.\n"
    "2. Ollama (offline) — runs entirely on your PC. No API key needed. No internet needed.\n"
    "3. Auto Smart Switch — automatically uses Groq when online, falls back to Ollama if offline or rate-limited.\n\n"

    "── AUTOMATIC FALLBACK CHAIN ──\n"
    "If your chosen model fails or hits a rate limit, TITAN ULTRA automatically tries the next model:\n"
    "Selected model → Llama 4 Maverick → Kimi K2 → DeepSeek R1 70B → Llama 3.3 70B → Gemma2 9B\n"
    "Rate-limited models get one retry after all others have been tried.\n\n"

    "── AI MODES (auto-detected from your message) ──\n"
    "TITAN ULTRA reads every message and silently picks the best mode:\n"
    "1. General Chat Mode — default. Answers everything: science, math, history, literature, school, life.\n"
    "2. Code Mode — triggered by: 'write code', 'debug this', 'fix this bug', 'explain this code', language names, etc.\n"
    "   Gives: Understanding → Full Code → How It Works → Example Output → Pro Tip.\n"
    "3. Web Search Mode — triggered by: 'latest news', 'current price', 'what happened', 'who won', etc.\n"
    "   Gives: Direct Answer → Step-by-Step → Key Facts → Real Example → Quick Summary.\n"
    "4. Exam Paper Mode — triggered by the Exam Paper Generator tool or by asking directly.\n"
    "   Generates complete exam papers with answer keys for CBSE, JEE, NEET, SAT, or any custom exam.\n"
    "5. Flashcard Mode — triggered by: 'flashcard', 'study card', 'quiz me', 'memorize', 'help me study', etc.\n"
    "   Generates FRONT/BACK flashcards with mnemonics. Interactive flip-card viewer appears automatically.\n"
    "6. Grammar Mode — triggered by: 'check grammar', 'fix grammar', 'proofread', 'check my writing', etc.\n"
    "   Gives: Corrected version → Errors found → Writing score (0–10) → Writing tip.\n"
    "7. Story / Creative Mode — triggered by: 'write a story', 'write a poem', 'write a horror', etc.\n"
    "   Writes vivid, complete stories in any genre: thriller, romance, sci-fi, fantasy, comedy, etc.\n"
    "8. Weather Mode — triggered by: 'weather', 'temperature', 'rain', 'forecast', 'AQI', etc.\n"
    "   Fetches LIVE weather from Open-Meteo API + AQI from Open-Meteo Air Quality API.\n"
    "9. Document Analysis Mode — triggered when a file is uploaded (PDF, text, CSV, code file, etc.).\n"
    "   Gives: Summary → Key Points → Smart Questions. Answers questions from the document only.\n\n"

    "── SPECIAL FEATURES ──\n"
    "• PC Control — TITAN ULTRA can directly control your Windows PC:\n"
    "  Open any app ('open Spotify', 'open Notepad', 'open Chrome'), "
    "  control volume ('set volume to 60', 'mute', 'increase volume by 20'), "
    "  control brightness ('set brightness to 80', 'increase brightness'), "
    "  media keys ('next song', 'pause music', 'previous track'), "
    "  take screenshots ('take a screenshot', 'open snipping tool'), "
    "  search YouTube ('search YouTube for lo-fi music'), "
    "  shutdown/restart/sleep/lock your PC.\n\n"
    "• Vision / Image Upload — attach a photo in the chat (paperclip button).\n"
    "  Uses Llama 4 Maverick (vision-capable) to analyze and describe the image.\n\n"
    "• Persistent Memory — TITAN ULTRA remembers facts about you across all sessions.\n"
    "  Say 'remember my name is Sanjay' or 'remember I am in Class 10'.\n"
    "  Memory is saved to titan_memory.json and loaded every time you start.\n"
    "  View, add, and delete memories from the sidebar Memory panel.\n\n"
    "• Multiple Chat Sessions — create new chats, switch between them, delete old ones.\n"
    "  Chat titles are auto-generated from your first message.\n\n"
    "• Text-to-Speech — every AI reply has a 'speak' button. Reads the answer aloud using "
    "  the browser's built-in voice engine. Prefers a clear male English voice. Click 'stop' to stop.\n\n"
    "• Speed Modes — switch between Fast (quick answers) and Thinking (deep step-by-step reasoning).\n\n"
    "• Exam Paper Generator — full UI panel: choose exam type (School Class, JEE, NEET, SAT, Custom), "
    "  class, subject, chapters, difficulty, number of questions, marks, time, and question type. "
    "  Download the generated paper as .txt or formatted PDF.\n\n"
    "• Flashcard Viewer — interactive flip cards with Known / Review tracking, Review Mode "
    "  (shows only cards marked for review), and Study All list view.\n\n"
    "• Screenshot → PDF — upload any image/screenshot in the sidebar and convert it to a PDF instantly.\n\n"
    "• Live Weather Panel — search any Indian city or state. Shows: temperature, feels-like, humidity, "
    "  wind speed & direction, UV index, AQI, moon phase, sunrise/sunset, 7-day forecast, "
    "  rain chance, and a 7-day temperature trend chart.\n\n"
    "• Quick Action Buttons — shown when chat is empty: 6 starter prompts for instant use.\n\n"

    "── HOW TITAN ULTRA IS BUILT (full tech stack) ──\n"
    "Language: Python 3.x\n"
    "UI Framework: Streamlit (st library) — web app running in your browser\n"
    "Cloud AI: Groq Python SDK (groq library) — ultra-fast LLM inference\n"
    "Offline AI: Ollama — local LLM server at http://localhost:11434\n"
    "HTTP Calls: requests library — for weather APIs, image generation, Ollama\n"
    "Image Processing: PIL / Pillow — image conversion, PDF creation from images\n"
    "PDF Generation: ReportLab — for exam paper PDF download\n"
    "Weather Data: Open-Meteo API (weather) + wttr.in (city geocoding) + Open-Meteo Air Quality API (AQI)\n"
    "Text-to-Speech: Browser Web Speech API — injected via st.html() JavaScript\n"
    "PC Control: subprocess, os, ctypes (Windows API for volume/brightness/media keys)\n"
    "Data Storage: json module — titan_memory.json (memory), .titan_key (API key)\n"
    "Regex: re module — for auto-detection of modes, memory commands, session titles\n"
    "Fonts: Google Fonts — Orbitron (headers) + Inter (body text)\n"
    "CSS Animations: rainbowborder, titanflow, tridentSpin — animated gradient UI\n\n"

    "── CONFIGURATION FILES ──\n"
    ".titan_key — your saved Groq API key (persists between restarts)\n"
    "titan_memory.json — all saved user memories\n"
    "titan_config.json — default API key configuration\n"
    ".streamlit/config.toml — Streamlit app configuration\n\n"

    "── OTHER FILES IN THE PROJECT ──\n"
    "run_titan_ultra.bat — Windows batch file to launch TITAN ULTRA with one click\n"
    "run_titan.bat / run_titan.py — alternative launchers\n"
    "titan_startup.vbs — silent VBScript launcher (no command window)\n"
    "GPT-OSS120BILLION.py — earlier version of TITAN ULTRA\n"
    "TitanAI_Extension/ — Chrome/Edge browser extension for TITAN ULTRA\n"
    "game_priority_locker.py — separate utility to lock CPU priority for games\n\n"

    "── API PARAMETERS ──\n"
    "Temperature: 0.7 (balanced creativity and accuracy)\n"
    "Max tokens: 8192 for all models except Compound (4096)\n"
    "Context window: up to 30 messages kept in history (older trimmed to save tokens)\n"
    "413 handling: automatically shrinks context to last 6 messages and retries\n"
    "Rate limit handling: retries all models, waits 8 seconds, then retries rate-limited ones\n"
)

CODE_SYSTEM = (
    "You are TITAN ULTRA — the world's most advanced coding AI. "
    "Your code quality matches senior staff engineers at Google, Meta, and Anthropic. "
    "You master every language: Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Swift, Kotlin, "
    "PHP, Ruby, Dart, Scala, R, MATLAB, SQL, Bash, HTML/CSS and every major framework.\n\n"

    "━━━ FOR EVERY CODE REQUEST — ALWAYS FOLLOW THIS STRUCTURE ━━━\n"
    "### 1. Understanding\n"
    "One or two sentences: exactly what this code does and what problem it solves.\n\n"
    "### 2. Complete Code\n"
    "• Full, runnable code in a properly labelled fenced block.\n"
    "• All imports included. No placeholders. No '# ... rest of code here'.\n"
    "• If the solution is long, write every line — never truncate.\n"
    "• Use modern best practices for the language/framework.\n\n"
    "### 3. How It Works\n"
    "Walk through each important section. Explain WHAT it does and WHY it's done that way. "
    "Beginner-friendly language — no assumed knowledge.\n\n"
    "### 4. Example Output\n"
    "Show exactly what the code prints or returns with a real concrete example.\n\n"
    "### 5. Key Insight / Pro Tip\n"
    "One expert-level observation: a performance improvement, a security consideration, a common pitfall, or a better pattern.\n\n"

    "━━━ CODE QUALITY RULES ━━━\n"
    "✦ Production-ready: handle errors, validate inputs, use proper types.\n"
    "✦ Clean and readable: meaningful names, logical structure, comments only on non-obvious lines.\n"
    "✦ Algorithms: always state time complexity O(?) and space complexity O(?).\n"
    "✦ Debugging: find the root cause, don't just patch symptoms.\n"
    "✦ Security: never leave SQL injection, XSS, or credential exposure in code.\n"
    "✦ Never say 'I cannot run this' — always write working, testable code.\n"
    "✦ Never truncate. A 300-line solution needs all 300 lines.\n"
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
)

EXAM_SYSTEM = (
    "You are an expert school and competitive exam paper setter with deep knowledge of "
    "NCERT curriculum for all classes 1-12 and all competitive exams (JEE, NEET, CBSE, ICSE, etc.). "
    "Create accurate, well-structured, complete exam papers. "
    "Never truncate. Always include a full ANSWER KEY at the end."
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

# ── Persist API key & memory to disk ─────────────────────────────────────────
import os as _os_key, json as _json
_KEY_FILE     = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), ".titan_key")
_IMG_KEY_FILE = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), ".titan_img_key")
_MEMORY_FILE  = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_memory.json")
_CHAT_FILE    = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_chats.json")

def _load_saved_key():
    try:
        with open(_KEY_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return ""

def _save_key(k):
    try:
        with open(_KEY_FILE, "w") as f:
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

def _save_chat_sessions():
    active = st.session_state.chat_sessions[st.session_state.active_session]
    _save_to_history(active)

# ── Owner check (Sushanth = full access, others = locked) ────────────────────
_saved_key      = _load_saved_key()
_saved_memory   = _load_memory()
_IS_OWNER = _saved_memory.get("name", "").strip().lower() == "sushanth"

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
             ("quick_q", ""), ("speed", "fast"),
             ("chat_sessions", [{"id": 0, "title": "New Chat", "messages": []}]),
             ("active_session", 0), ("_titan_nonce", ""),
             ("chat_active_tool", ""), ("ep_last_paper", ""), ("ep_last_name", "exam"),
             ("ep_generating", False),
             ("flashcards", []), ("card_index", 0), ("card_flipped", False),
             ("card_known", set()), ("card_review", set()), ("fc_review_mode", False),
             ("fc_study_all", False),
             ("weather_query", ""), ("weather_name", ""), ("weather_data", None),
             ("weather_aqi", None), ("weather_summary", ""), ("weather_state", ""),
]:
    if k not in st.session_state:
        st.session_state[k] = v


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

@st.cache_data(ttl=30)
def check_ollama():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
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

if "ollama_models" not in st.session_state:
    _r, _m = check_ollama()
    if not _r:
        # Auto-launch Ollama on first run if it's installed
        if start_ollama_background():
            check_ollama.clear()
            _r, _m = check_ollama()
    st.session_state.ollama_reachable = _r
    st.session_state.ollama_models = _m
ollama_models = st.session_state.ollama_models
ollama_reachable = st.session_state.get("ollama_reachable", False)

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
""")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 8px'>
        <div style='font-family:Orbitron,monospace;font-size:1.1rem;font-weight:900;
        background:linear-gradient(90deg,#00e5d0,#00b4d8,#0077b6,#023e8a,#03045e);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
        filter:drop-shadow(0 0 10px #00c4cc88) drop-shadow(0 0 20px #0077b666)'>🔱 TITAN ULTRA</div>
        <div style='font-family:Orbitron,monospace;font-size:0.6rem;font-weight:700;
        letter-spacing:3px;margin-top:4px;
        background:linear-gradient(90deg,#ff6b00,#ffd000,#aaff00,#00e5ff,#a855f7,#ec4899,#ff006e,#ff6b00);
        background-size:400%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;animation:titanflow 3s linear infinite'>BEYOND JEE · BEYOND GPT-4</div>
    </div>""", unsafe_allow_html=True)

    if st.button("➕ New Chat", use_container_width=True):
        # Save current chat to history before starting fresh
        _save_chat_sessions()
        import time as _t
        st.session_state.chat_sessions = [{"id": int(_t.time()), "title": "New Chat", "messages": []}]
        st.session_state.active_session = 0
        st.rerun()

    if st.button("🖥️ Launch TITAN CODE", use_container_width=True,
                 help="Open Titan Code — AI terminal coding assistant"):
        import subprocess as _sp, sys as _sys
        _tc_path = r"C:\Users\sanja\Documents\important\TITAN_CODE.py"
        _bat = r"C:\Users\sanja\Documents\important\launch_titan_code.bat"
        _sp.Popen(f'start "TITAN CODE" "{_bat}"', shell=True)
        st.toast("🖥️ Titan Code launched in a new terminal!", icon="⚡")

    # ── Chat History ──────────────────────────────────────────────────────────
    _hist_all = _load_history()
    _hist_label = f"📖 Chat History  ({len(_hist_all)})" if _hist_all else "📖 Chat History"
    with st.expander(_hist_label, expanded=False):
        if not _hist_all:
            st.markdown("<div style='font-size:.75rem;color:#6b7a99;padding:6px 0'>"
                        "No history yet. Start chatting!</div>", unsafe_allow_html=True)
        else:
            # Search box
            _hist_search = st.text_input("Search history", placeholder="Search...",
                                         key="_hist_search", label_visibility="collapsed")
            _hist_filtered = [s for s in _hist_all
                              if _hist_search.lower() in s.get("title","").lower()] if _hist_search else _hist_all

            if not _hist_filtered:
                st.caption("No results.")
            else:
                for _hs in _hist_filtered[:60]:
                    _hs_date = _hs.get("date","")[:10] if _hs.get("date") else ""
                    _hs_count = len(_hs.get("messages", []))
                    _hs_msgs_label = f"{_hs_count // 2} msg{'s' if _hs_count // 2 != 1 else ''}"
                    _col1, _col2 = st.columns([5, 1])
                    _col1.markdown(
                        f"<div style='font-size:.72rem;color:#c9d8f0;line-height:1.3'>"
                        f"<b>{_hs.get('title','Chat')[:30]}</b><br>"
                        f"<span style='color:#6b7a99'>{_hs_date} · {_hs_msgs_label}</span></div>",
                        unsafe_allow_html=True
                    )
                    if _col2.button("↗", key=f"_hs_open_{_hs.get('id',0)}", help="Open this chat"):
                        _save_chat_sessions()  # save current first
                        st.session_state.chat_sessions = [_hs]
                        st.session_state.active_session = 0
                        st.rerun()

            st.divider()
            if st.button("🗑️ Clear All History", key="_hist_clear_all", use_container_width=True):
                try:
                    with open(_CHAT_FILE, "w", encoding="utf-8") as _hf:
                        _json.dump([], _hf)
                except Exception:
                    pass
                st.rerun()

    st.divider()

    # Info box
    if ollama_models:
        st.markdown(f"""<div style='background:#0a1a0a;border:1px solid #166534;
        border-radius:8px;padding:10px 12px;font-size:.72rem;color:#4ade80'>
        ✅ TitanAI runs 100% Offline with Ollama.<br>
        <span style='color:#6b7a99'>Models: {len(ollama_models)} installed<br>
                (Voice Input uses Groq Whisper)</span></div>""", unsafe_allow_html=True)
    elif ollama_reachable:
        st.markdown("""<div style='background:#1a1408;border:1px solid #92400e;
        border-radius:8px;padding:10px 12px;font-size:.72rem;color:#fbbf24'>
        Ollama is running but no models installed yet.<br>
        <span style='color:#6b7a99'>Pull one below to start using offline mode.</span></div>""",
        unsafe_allow_html=True)
    else:
        st.markdown("""<div style='background:#0a0d1a;border:1px solid #1e3a5f;
        border-radius:8px;padding:10px 12px;font-size:.72rem;color:#6b7a99'>
        Ollama not detected. Start Ollama to use offline models.<br><br>
                (Voice Input uses Groq Whisper)</div>""", unsafe_allow_html=True)
    if st.button("🔄 Detect / Start Ollama", use_container_width=True, key="_ollama_detect"):
        check_ollama.clear()
        _r, _m = check_ollama()
        if not _r:
            with st.spinner("Starting Ollama…"):
                if start_ollama_background():
                    check_ollama.clear()
                    _r, _m = check_ollama()
        st.session_state.ollama_reachable = _r
        st.session_state.ollama_models = _m
        st.rerun()

    # One-click pull for Qwen + Moondream
    if ollama_reachable:
        _missing = [n for n in OLLAMA_SUGGESTED if not any(n.split(":")[0] in m for m in ollama_models)]
        if _missing:
            st.markdown("<div style='font-size:.65rem;color:#6b7a99;margin:6px 0 2px'>"
                        "Recommended models</div>", unsafe_allow_html=True)
            for _name in _missing:
                _lbl = OLLAMA_SUGGESTED[_name]
                if st.button(f"📥 Pull {_lbl}", use_container_width=True, key=f"_pull_{_name}"):
                    with st.spinner(f"Pulling {_name} (this may take a few minutes)…"):
                        ok = pull_ollama_model(_name)
                    if ok:
                        check_ollama.clear()
                        _r, _m = check_ollama()
                        st.session_state.ollama_reachable = _r
                        st.session_state.ollama_models = _m
                        st.rerun()
                    else:
                        st.warning(f"Couldn't pull {_name}. Try again or run: ollama pull {_name}")

    st.divider()

    # Groq API Key
    st.markdown("<div style='font-size:.7rem;color:#4a6a8f;letter-spacing:2px;margin-bottom:4px'>GROQ API KEY</div>", unsafe_allow_html=True)
    key_in = st.text_input("API Key", type="password", label_visibility="collapsed",
                           value=st.session_state.api_key, placeholder="gsk_...")
    if key_in and key_in != st.session_state.api_key:
        st.session_state.api_key = key_in
        _save_key(key_in)
    elif key_in:
        st.session_state.api_key = key_in

    # Provider
    st.markdown("<div style='font-size:.7rem;color:#4a6a8f;letter-spacing:2px;margin:8px 0 4px'>PROVIDER</div>", unsafe_allow_html=True)
    provider_opts = ["🔁 Auto (Smart Switch)", "Groq"] + (["Ollama (Offline)"] if (ollama_models or ollama_reachable) else [])
    provider = st.selectbox("Provider", provider_opts, label_visibility="collapsed")
    if provider == "🔁 Auto (Smart Switch)":
        _online = _has_internet()
        _auto_using = "Groq" if _online else "Ollama (Offline)"
        _auto_colour = "#22c55e" if _online else "#f59e0b"
        _auto_icon   = "🌐" if _online else "📴"
        st.markdown(f"<div style='font-size:.68rem;color:{_auto_colour};margin:2px 0 6px 2px'>"
                    f"{_auto_icon} Using <b>{_auto_using}</b> right now</div>",
                    unsafe_allow_html=True)

    # Model
    if _IS_OWNER:
        st.markdown("<div style='font-size:.7rem;color:#4a6a8f;letter-spacing:2px;margin:8px 0 4px'>AI MODEL</div>", unsafe_allow_html=True)
        if provider in ("Groq", "🔁 Auto (Smart Switch)"):
            model_name = st.selectbox("Model", list(GROQ_MODELS.keys()), label_visibility="collapsed")
            model_id   = GROQ_MODELS[model_name]
            if ollama_models and provider == "🔁 Auto (Smart Switch)":
                st.markdown("<div style='font-size:.63rem;color:#6b7a99;margin:-4px 0 4px 2px'>"
                            "Offline fallback: " + ollama_models[0] + "</div>",
                            unsafe_allow_html=True)
        else:
            model_id = st.selectbox("Ollama Model", ollama_models, label_visibility="collapsed")
    else:
        model_name = list(GROQ_MODELS.keys())[0]
        model_id   = GROQ_MODELS[model_name]

    # Model info box — only for Maverick and DeepSeek
    if provider == "Groq":
        if model_id in ("meta-llama/llama-4-maverick-17b-128e-instruct", "meta-llama/llama-4-scout-17b-16e-instruct"):
            st.markdown("""<div style='background:linear-gradient(135deg,rgba(0,80,255,0.35),rgba(0,150,255,0.25));
            border:1px solid rgba(0,150,255,0.85);border-radius:8px;padding:8px 12px;margin:4px 0 8px'>
            <b style='font-size:1.1rem;color:#60b4ff;letter-spacing:2px'>👑 TITAN PRIME</b><br>
            <span style='font-size:.82rem;color:#93c5fd'>Meta Llama 4 Maverick · 128 Experts · GPT-OSS 120B<br>
            Strongest open-source model · Beats GPT-4o &amp; Gemini<br>
            Handles everything — coding, math, research, JEE, PhD</span>
            </div>""", unsafe_allow_html=True)
        elif model_id == "deepseek-r1-distill-llama-70b":
            st.markdown("""<div style='background:linear-gradient(135deg,rgba(100,180,255,0.18),rgba(150,210,255,0.12));
            border:1px solid rgba(147,197,253,0.55);border-radius:8px;padding:8px 12px;margin:4px 0 8px'>
            <b style='font-size:.72rem;color:#bae6fd'>🏆 MOST POWERFUL REASONING</b><br>
            <span style='font-size:.68rem;color:#7dd3fc'>DeepSeek R1 · 70B · Chain-of-thought Reasoning<br>
            Beats GPT-4o &amp; Gemini on Math, Science &amp; Olympiad<br>
            Handles IMO, IPhO, JEE Advanced, PhD-level research</span>
            </div>""", unsafe_allow_html=True)

    st.divider()

    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        import time as _t
        st.session_state.chat_sessions = [{"id": int(_t.time()), "title": "New Chat", "messages": []}]
        st.session_state.active_session = 0
        st.rerun()

    st.divider()

    # ── Memory ────────────────────────────────────────────────────────────────
    _mem = st.session_state.titan_memory
    with st.expander(f"🧠 Memory ({len(_mem)} saved)"):
        st.caption("TitanAI remembers facts about you across all sessions. Saves automatically.")
        if _mem:
            for _mk, _mv in list(_mem.items()):
                _mc1, _mc2 = st.columns([5, 1])
                _mc1.markdown(f"**{_mk}:** {_mv}")
                if _mc2.button("✕", key=f"mem_del_{_mk}", help="Forget this"):
                    del st.session_state.titan_memory[_mk]
                    _save_memory(st.session_state.titan_memory)
                    st.rerun()
        else:
            st.caption("No memories yet — tell me your name, location, job, or preferences.")
        st.markdown("**Add a memory:**")
        st.caption("Type like: `my hobby is cricket` or `I work as a developer`")
        _mem_raw = st.text_input("Memory Input", placeholder="e.g. my hobby is cricket",
                                 key="mem_add_raw", label_visibility="collapsed")
        if st.button("💾 Save Memory", key="mem_add_btn", use_container_width=True):
            if _mem_raw.strip():
                import re as _re_m
                _m = _re_m.match(r"(?:my\s+)?(.+?)\s+is\s+(.+)", _mem_raw.strip(), _re_m.IGNORECASE)
                if _m:
                    _mk2, _mv2 = _m.group(1).strip().lower(), _m.group(2).strip()
                else:
                    _mk2, _mv2 = f"note_{len(_mem)}", _mem_raw.strip()
                st.session_state.titan_memory[_mk2] = _mv2
                _save_memory(st.session_state.titan_memory)
                st.rerun()
        if _mem and st.button("🗑️ Clear All Memories", key="mem_clear", use_container_width=True):
            st.session_state.titan_memory = {}
            _save_memory({})
            st.rerun()

    # Attach + Voice buttons removed (no file upload or voice input).
    voice_text    = ""
    uploaded_file = None
    file_content  = ""
    if "pending_vision" not in st.session_state:
        st.session_state.pending_vision = None

    st.divider()

    # Screenshot → PDF
    st.markdown("""<div style='font-family:Orbitron,monospace;font-size:.7rem;
    letter-spacing:3px;color:#a855f7;text-transform:uppercase;margin-bottom:8px'>
    📄 SCREENSHOT → PDF</div>""", unsafe_allow_html=True)
    pc1, pc2 = st.columns([3,2])
    pdf_upload = pc1.file_uploader("Image", type=["png","jpg","jpeg","webp","gif"],
                                   key="_pdf_img", label_visibility="collapsed")
    if pc2.button("📄 Convert\nto PDF", key="_pdf_btn"):
        if pdf_upload:
            try:
                from PIL import Image as _PIL
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Image as _RLImage
                img = _PIL.open(pdf_upload)
                if img.mode not in ("RGB","L"): img = img.convert("RGB")
                img_buf = io.BytesIO()
                img.save(img_buf, format="PNG")
                img_buf.seek(0)
                buf = io.BytesIO()
                doc = SimpleDocTemplate(buf, pagesize=A4,
                                        leftMargin=20, rightMargin=20,
                                        topMargin=20, bottomMargin=20)
                page_w = A4[0] - 40
                page_h = A4[1] - 40
                iw, ih = img.size
                scale = min(page_w / iw, page_h / ih)
                rl_img = _RLImage(img_buf, width=iw*scale, height=ih*scale)
                doc.build([rl_img])
                buf.seek(0)
                fname = pdf_upload.name.rsplit(".",1)[0] + ".pdf"
                st.sidebar.success(f"✅ {fname} ready!")
                st.sidebar.download_button("⬇️ Download PDF", buf.getvalue(),
                                           fname, "application/pdf", key="_pdf_dl")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
        else:
            st.sidebar.warning("Upload an image first")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:20px 0 10px'>
    <div style='font-size:90px;line-height:1.1;display:inline-block;
    animation:tridentSpin 3s linear infinite'>🔱</div>
    <div style='font-family:Orbitron,monospace;font-weight:900;font-size:1.9rem;
    letter-spacing:3px;margin:8px 0 4px;
    background:linear-gradient(90deg,#00e5d0,#00b4d8,#0077b6,#023e8a,#03045e);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    filter:drop-shadow(0 0 14px #00c4cc88) drop-shadow(0 0 28px #0077b666)'>
    Hello, I'm TITAN ULTRA</div>
    <div style='font-size:.72rem;color:#6b7a99;letter-spacing:1.5px;margin:0 0 4px'>
    Your offline and online assistance</div>
    <div style='font-family:Orbitron,monospace;font-size:.75rem;font-weight:700;
    background:linear-gradient(90deg,#ff6b00,#ffd000,#aaff00,#00e5ff,#a855f7,#ec4899,#ff006e,#ff6b00);
    background-size:400%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;animation:titanflow 3s linear infinite;
    filter:drop-shadow(0 0 8px #a855f755)'>
    ✦ Smarter than ChatGPT, Gemini &amp; Perplexity paid ✦</div>
</div>
""", unsafe_allow_html=True)

st.divider()

mode_key = "chat"  # unified — auto-detected from input

# ── Features & Tools ──────────────────────────────────────────────────────────
with st.expander("⚙️ Features & Tools"):
    st.markdown("<div style='font-size:.75rem;color:#a855f7;letter-spacing:2px;margin-bottom:8px'>SPEED MODE</div>", unsafe_allow_html=True)
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
    st.markdown(f"<div style='font-size:.72rem;color:#4a6a8f;text-align:center;margin-top:4px'>Active: <b style='color:#c9d8f0'>{active}</b></div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:.75rem;color:#a855f7;letter-spacing:2px;margin:14px 0 8px'>QUICK ACTIONS</div>", unsafe_allow_html=True)

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
                    "Format the paper with:\n"
                    "1. Header: exam name, subject, date field, duration, max marks, instructions\n"
                    "2. Numbered questions with marks per question in brackets\n"
                    "3. MCQs: 4 options labeled (A) (B) (C) (D)\n"
                    "4. ANSWER KEY at the end with correct answers and brief explanations\n"
                    "Ensure questions are NCERT/curriculum accurate and appropriate for the class/exam level."
                )
                st.session_state.ep_last_name = str(_ep_exam_label).replace(" ","_")
                st.session_state.ep_generating = True
                st.session_state.ep_last_paper = ""
                st.session_state.quick_q = _prompt
                st.rerun()


st.divider()

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
            Card <b style='color:#c9d8f0'>{_pos+1}</b> / {_fc_n}
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

# ── Live Weather (always available, expands when data is fetched) ─────────────
with st.expander("🌤️ Live Weather Search", expanded=bool(st.session_state.weather_data)):
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
          <p style='color:#c9d8f0;font-size:13px;line-height:1.65;margin:0;'>
            🌤️ <b>{st.session_state.weather_name}</b> — {_wdesc}, {_temp}°C (feels {_feels}°C).
            Humidity {_hum}%, wind {_wspd} km/h {_wdir}, UV index {_uv}.
            Rain chance {_rainc}%.<br><br>{_tip}</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#6b7a99;font-size:.8rem;padding:8px 0'>Type a city or state above, or ask me in the chat — e.g. \"weather in Mumbai\"</div>", unsafe_allow_html=True)

# ── Animated Diagrams ─────────────────────────────────────────────────────────
_DIAGRAM_MAP = {
    'atom':          ['atom','atomic structure','structure of an atom','bohr model','electron shell',
                      'subatomic','atomic model','structure of atom','electron orbit','proton neutron',
                      'atomic number','electron configuration','structure of the atom'],
    'dna':           ['dna','double helix','dna structure','deoxyribonucleic','nucleotide',
                      'base pair','dna strand','rna structure','genetic code','chromosome structure'],
    'solar':         ['solar system','planets orbit','heliocentric','orbit the sun','our solar system',
                      'how planets move','revolution of planet','solar system work','planet revolve'],
    'cell':          ['cell structure','plant cell','animal cell','cell organelle','cell membrane',
                      'structure of a cell','parts of a cell','eukaryotic cell','prokaryotic cell',
                      'how does a cell work','cell biology'],
    'water':         ['water cycle','hydrological cycle','water cycle diagram','evaporation condensation',
                      'rain cycle','how water cycle','precipitation','water evaporate'],
    'wave':          ['sound wave','light wave','wave diagram','wave motion','transverse wave',
                      'longitudinal wave','simple harmonic motion','shm','pendulum motion',
                      'frequency wavelength','how waves work','wave structure'],
    'heart':         ['human heart','heart structure','how heart works','circulatory system',
                      'blood circulation','heart chambers','cardiac cycle','blood flow in heart',
                      'how does the heart','heartbeat','atrium ventricle'],
    'photosynthesis':['photosynthesis','how plants make food','chlorophyll','chloroplast',
                      'light reaction','dark reaction','calvin cycle','how plants prepare food',
                      'how plant makes food'],
    'circuit':       ['electric circuit','electrical circuit','circuit diagram',
                      'how does electricity flow',"ohm's law",'how current flows',
                      'series circuit','parallel circuit','how electricity works','current flow'],
    'eye':           ['structure of eye','human eye','how eye works','parts of eye','eye diagram',
                      'how we see','lens of eye','retina','how does the eye','vision work'],
    'magnet':        ['magnetic field','how magnet works','magnetic field lines','bar magnet',
                      'electromagnet','how does a magnet','magnetic force','field lines'],
    'mitosis':       ['mitosis','cell division','how cells divide','cell cycle','meiosis',
                      'cell reproduction','how does cell divide','stages of mitosis'],
    'moon':          ['moon phases','phases of moon','lunar cycle','how moon phases','new moon full moon',
                      'why moon phases','waxing waning','how does moon'],
    'newton':        ["newton's laws","newton's first law","newton's second law","newton's third law",
                      'law of motion','laws of motion','force and motion','inertia','f=ma'],
    # ── More Science ──────────────────────────────────────────────────────────
    'refraction':    ['refraction','snell\'s law','bending of light','refraction of light',
                      'light through glass','light through prism','how light bends','lens ray',
                      'convex lens','concave lens','ray diagram','optical','refractive index'],
    'reflection':    ['reflection of light','law of reflection','mirror reflection','concave mirror',
                      'convex mirror','plane mirror','how mirror works','mirror ray diagram',
                      'angle of incidence','angle of reflection'],
    'lungs':         ['respiratory system','how lungs work','breathing','lungs','how we breathe',
                      'inhalation exhalation','diaphragm','alveoli','respiration diagram',
                      'how respiration works','how does breathing'],
    'digestion':     ['digestive system','digestion process','how digestion works','how we digest',
                      'digestive tract','stomach','intestine','how food is digested',
                      'parts of digestive','alimentary canal'],
    'neuron':        ['neuron','nerve cell','how neuron works','structure of neuron','synapse',
                      'nervous system','nerve impulse','axon dendrite','how nerve works'],
    'plant_structure':['parts of a plant','plant structure','how plant works','root stem leaf',
                       'parts of plant','flower structure','how does a plant','monocot dicot',
                       'structure of a flower','plant organs'],
    'food_chain':    ['food chain','food web','trophic level','ecosystem','predator prey',
                      'producer consumer','energy flow in ecosystem','how food chain works',
                      'decomposer','herbivore carnivore'],
    'projectile':    ['projectile motion','projectile','how projectile works','trajectory',
                      'horizontal projection','path of projectile','cannon ball','parabolic path',
                      'range of projectile'],
    'circular_motion':['circular motion','centripetal force','uniform circular motion','angular velocity',
                       'how circular motion','centrifugal','rotation revolution'],
    # ── Geography ─────────────────────────────────────────────────────────────
    'volcano':       ['volcano','volcanic eruption','how volcano erupts','magma lava','volcano diagram',
                      'how does a volcano','types of volcano','shield volcano','composite volcano'],
    'earthquake':    ['earthquake','seismic waves','how earthquake occurs','epicentre','richter scale',
                      'how earthquake works','fault line','tectonic plates earthquake','seismograph'],
    'rock_cycle':    ['rock cycle','igneous rock','sedimentary rock','metamorphic rock','how rocks form',
                      'rock formation','types of rock','rock cycle diagram'],
    'greenhouse':    ['greenhouse effect','global warming','how greenhouse effect','climate change',
                      'carbon dioxide warming','atmosphere warming','greenhouse gas'],
    'seasons':       ['seasons','why seasons occur','earth tilt','why summer winter','how seasons',
                      'solstice equinox','revolution of earth','autumn spring summer winter'],
    'plate_tectonics':['plate tectonics','tectonic plates','continental drift','how plates move',
                       'plate boundary','convergent divergent','how continents move'],
    'river_erosion': ['river erosion','river formation','river deposition','how river forms',
                      'meander','delta','ox bow lake','river stages','erosion deposition'],
    'atmosphere':    ['layers of atmosphere','atmosphere layers','troposphere','stratosphere',
                      'mesosphere','thermosphere','exosphere','structure of atmosphere',
                      'atmospheric layers','layers of the atmosphere','what are the layers',
                      'atmosphere structure','layer of atmosphere','ozone layer location',
                      'what layer do planes fly','where do meteors burn','ionosphere',
                      'explain atmosphere','how atmosphere works','what is atmosphere'],
    # ── Mathematics ───────────────────────────────────────────────────────────
    'trig':          ['trigonometry','sin cos tan','unit circle','trigonometric ratio',
                      'how sin cos','sine cosine tangent','trig function','trigonometric function',
                      'sin graph','cos graph'],
    'pythagoras':    ['pythagoras theorem','pythagorean theorem','a squared plus b squared',
                      'right triangle','hypotenuse','pythagorean','pythagoras'],
    'graph_linear':  ['linear equation','straight line graph','y=mx+c','slope intercept',
                      'how to draw line','linear function','gradient intercept'],
    'graph_quad':    ['quadratic equation','parabola','y=x squared','quadratic function',
                      'x squared graph','how to draw parabola','vertex parabola'],
    'venn':          ['venn diagram','sets and subsets','union intersection','how venn diagram',
                      'set theory','elements of set','venn','cardinality'],
    'geometry_angles':['types of angles','acute obtuse reflex','angle types','complementary supplementary',
                       'parallel lines transversal','corresponding angles','alternate angles',
                       'interior angles','exterior angle'],
    'geometry_shapes':['triangle types','types of triangle','equilateral isosceles scalene',
                       'properties of triangle','quadrilateral types','polygon','circle parts',
                       'chord diameter radius','area of shapes'],
    # ── Economics / Social Science ────────────────────────────────────────────
    'demand_supply': ['demand and supply','supply demand curve','law of demand','law of supply',
                      'equilibrium price','demand curve','supply curve','how market works',
                      'market equilibrium','price mechanism'],
    'circular_flow': ['circular flow','circular flow of income','flow of money','how economy works',
                      'households firms','factors of production circular','income expenditure flow'],
    # ── History Timelines ─────────────────────────────────────────────────────
    'timeline':      ['timeline of','world war timeline','history of','chronology',
                      'important events','when did','sequence of events','dates of',
                      'year by year','what happened in'],
}

def _detect_diagram_topic(text):
    t = text.lower()
    is_visual = any(k in t for k in [
        'explain','structure','diagram','how does','how do','show me','what is','describe',
        'how it works','what are','how are','how work','tell me about','what happens',
        'how','explain how','what','draw','illustrate','define','stages','parts of',
        'process of','mechanism','function of','system','model','cycle',
    ])
    if not is_visual:
        return None
    for topic, keywords in _DIAGRAM_MAP.items():
        if any(k in t for k in keywords):
            return topic
    return None

def _get_diagram_html(topic):
    _bg = 'background:#05080f;color:#c9d8f0;font-family:monospace,sans-serif;margin:0;padding:8px 4px;box-sizing:border-box;'
    _flex = f'{_bg}display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100%;'

    if topic == 'atom':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">⚛ ATOMIC STRUCTURE — BOHR MODEL</div>
<canvas id="atC" width="300" height="300" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">● Nucleus (p⁺+n⁰)  ● K shell 2e⁻  ● L shell 8e⁻  ● M shell 8e⁻</div>
<script>
const cv=document.getElementById('atC'),ctx=cv.getContext('2d'),W=300,H=300,cx=150,cy=150;
const stars=[];
for(let i=0;i<55;i++)stars.push([Math.random()*W,Math.random()*H,Math.random()*1.2+.3,Math.random()*80]);
const shells=[{{r:65,n:2,col:'#00e5ff',nm:'K',spd:.028}},{{r:106,n:8,col:'#a855f7',nm:'L',spd:.013}},{{r:146,n:8,col:'#22c55e',nm:'M',spd:.007}}];
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#010208';ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{{
    ctx.beginPath();ctx.arc(s[0],s[1],s[2],0,6.28);
    ctx.fillStyle='rgba(200,215,255,'+(0.3+0.4*Math.sin(t*.02+s[3])).toFixed(2)+')';ctx.fill();
  }});
  shells.forEach(s=>{{
    ctx.beginPath();ctx.arc(cx,cy,s.r,0,6.28);
    ctx.strokeStyle=s.col+'44';ctx.lineWidth=1;ctx.stroke();
    ctx.fillStyle=s.col;ctx.font='bold 9px monospace';ctx.textAlign='left';
    ctx.fillText(s.nm,cx+s.r+4,cy+3);
  }});
  const nr=22+4*Math.sin(t*.055);
  const ng=ctx.createRadialGradient(cx-4,cy-4,2,cx,cy,nr+2);
  ng.addColorStop(0,'#fffde7');ng.addColorStop(.35,'#ffa000');ng.addColorStop(1,'#b71c1c');
  ctx.shadowColor='#ff6600';ctx.shadowBlur=22;
  ctx.beginPath();ctx.arc(cx,cy,nr,0,6.28);ctx.fillStyle=ng;ctx.fill();
  ctx.shadowBlur=0;
  ctx.fillStyle='#fff';ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillText('p⁺n',cx,cy+3);
  shells.forEach(s=>{{
    ctx.shadowColor=s.col;ctx.shadowBlur=14;
    for(let j=0;j<s.n;j++){{
      const a=t*s.spd+j*(6.28/s.n);
      ctx.beginPath();ctx.arc(cx+s.r*Math.cos(a),cy+s.r*Math.sin(a),4.5,0,6.28);
      ctx.fillStyle=s.col;ctx.fill();
    }}
    ctx.shadowBlur=0;
  }});
  ctx.fillStyle='rgba(255,255,255,.28)';ctx.font='8px sans-serif';ctx.textAlign='center';
  ctx.fillText('Electrons orbit the nucleus in fixed energy shells',cx,H-5);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'dna':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🧬 DNA DOUBLE HELIX</div>
<canvas id="dna" width="300" height="320" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">A-T pairs · G-C pairs · Sugar-phosphate backbone · Carries genetic info</div>
<script>
const cv=document.getElementById('dna'),ctx=cv.getContext('2d'),W=300,H=320,ccx=W/2;
const amp=60,freq=0.044;
const bpColors=[['#ff6b6b','#4ecdc4'],['#ffd700','#a855f7'],['#22c55e','#ff9944'],['#ff8c94','#48cae4']];
const bpLabels=[['A','T'],['G','C'],['C','G'],['T','A']];
const stars=[];for(let i=0;i<40;i++)stars.push([Math.random()*W,Math.random()*H,Math.random()*1.1+.3,Math.random()*70]);
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#010208';ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{{
    ctx.beginPath();ctx.arc(s[0],s[1],s[2],0,6.28);
    ctx.fillStyle='rgba(200,215,255,'+(0.25+0.3*Math.sin(t*.02+s[3])).toFixed(2)+')';ctx.fill();
  }});
  const steps=14;
  for(let i=0;i<=steps;i++){{
    const y=16+i*((H-32)/steps);
    const x1=ccx+amp*Math.sin(freq*y*10+t);
    const x2=ccx+amp*Math.sin(freq*y*10+t+Math.PI);
    const bp=bpColors[i%4];const bl=bpLabels[i%4];
    const depth=Math.sin(freq*y*10+t);
    const bpAlpha=(0.4+0.4*Math.abs(depth)).toFixed(2);
    const grd=ctx.createLinearGradient(x1,y,x2,y);
    grd.addColorStop(0,bp[0]);grd.addColorStop(.5,'rgba(255,215,0,.5)');grd.addColorStop(1,bp[1]);
    ctx.beginPath();ctx.moveTo(x1,y);ctx.lineTo(x2,y);
    ctx.strokeStyle='rgba(255,215,0,'+bpAlpha+')';ctx.lineWidth=1.8;ctx.stroke();
    const sz=5+2*Math.abs(depth);
    ctx.shadowColor=bp[0];ctx.shadowBlur=8;
    ctx.beginPath();ctx.arc(x1,y,sz,0,6.28);ctx.fillStyle=bp[0];ctx.fill();
    ctx.shadowColor=bp[1];
    ctx.beginPath();ctx.arc(x2,y,sz,0,6.28);ctx.fillStyle=bp[1];ctx.fill();
    ctx.shadowBlur=0;
    if(Math.abs(depth)<0.4){{
      ctx.fillStyle=bp[0];ctx.font='bold 7px sans-serif';ctx.textAlign='center';
      ctx.fillText(bl[0],x1,y+3);
      ctx.fillStyle=bp[1];ctx.fillText(bl[1],x2,y+3);
    }}
  }}
  for(let s=0;s<2;s++){{
    const off=s*Math.PI;
    ctx.beginPath();
    for(let y=16;y<=H-16;y+=2){{
      const x=ccx+amp*Math.sin(freq*y*10+t+off);
      y===16?ctx.moveTo(x,y):ctx.lineTo(x,y);
    }}
    ctx.shadowColor=s===0?'#ff6b6b':'#4ecdc4';ctx.shadowBlur=8;
    ctx.strokeStyle=s===0?'#ff6b6b':'#4ecdc4';ctx.lineWidth=3;ctx.stroke();
    ctx.shadowBlur=0;
  }}
  ctx.fillStyle='rgba(255,255,255,.25)';ctx.font='7px monospace';ctx.textAlign='center';
  ctx.fillText('A=Adenine  T=Thymine  G=Guanine  C=Cytosine',ccx,H-5);
  t+=0.038;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'solar':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🌌 THE SOLAR SYSTEM</div>
<canvas id="sol" width="460" height="310" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">8 planets orbit the Sun · Not to scale · Orbital speeds proportional</div>
<script>
const cv=document.getElementById('sol'),ctx=cv.getContext('2d'),W=460,H=310,cx=W/2,cy=H/2;
const stars=[];for(let i=0;i<90;i++)stars.push([Math.random()*W,Math.random()*H,Math.random()*1.3+.3,Math.random()*90]);
const pN=['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune'];
const pR=[30,50,72,96,130,164,196,224];
const pC=['#b0bec5','#ffcc80','#4fc3f7','#ef5350','#ffb74d','#fdd835','#80deea','#5588cc'];
const pSz=[3,5,5.5,4.5,13,11,8,8];
const pSpd=[.042,.026,.016,.010,.006,.004,.002,.0013];
const pOff=[0.8,1.9,3.2,4.7,0.3,2.1,5.0,1.5];
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#010208';ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{{
    ctx.beginPath();ctx.arc(s[0],s[1],s[2],0,6.28);
    ctx.fillStyle='rgba(200,215,255,'+(0.3+0.4*Math.sin(t*.018+s[3])).toFixed(2)+')';ctx.fill();
  }});
  for(let i=0;i<6;i++){{
    ctx.beginPath();ctx.arc(cx,cy,25+i*4,.8,2.3,false);
    const ra=(0.12+0.08*Math.sin(t*.04+i)).toFixed(2);
    ctx.strokeStyle='rgba(255,200,50,'+ra+')';ctx.lineWidth=2;ctx.stroke();
  }}
  const sunG=ctx.createRadialGradient(cx,cy,2,cx,cy,26);
  sunG.addColorStop(0,'#fffde7');sunG.addColorStop(.45,'#ffa000');sunG.addColorStop(1,'rgba(230,80,0,0)');
  ctx.shadowColor='#ff8800';ctx.shadowBlur=28;
  ctx.beginPath();ctx.arc(cx,cy,24*(1+.04*Math.sin(t*.04)),0,6.28);ctx.fillStyle=sunG;ctx.fill();
  ctx.shadowBlur=0;
  ctx.fillStyle='rgba(255,210,80,.7)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('☉ SUN',cx,cy+3);
  for(let i=0;i<8;i++){{
    ctx.beginPath();ctx.arc(cx,cy,pR[i],0,6.28);
    ctx.strokeStyle='rgba(255,255,255,.06)';ctx.lineWidth=.7;ctx.stroke();
    const a=t*pSpd[i]+pOff[i];
    const px=cx+pR[i]*Math.cos(a),py=cy+pR[i]*Math.sin(a);
    if(i===5){{ctx.save();ctx.translate(px,py);ctx.scale(2.6,.38);ctx.beginPath();ctx.arc(0,0,pSz[i]+4,0,6.28);ctx.strokeStyle='rgba(253,216,53,.55)';ctx.lineWidth=3;ctx.stroke();ctx.restore();}}
    ctx.shadowColor=pC[i];ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(px,py,pSz[i],0,6.28);ctx.fillStyle=pC[i];ctx.fill();
    ctx.shadowBlur=0;
    ctx.fillStyle=pC[i];ctx.font='6px sans-serif';ctx.textAlign='center';
    ctx.fillText(pN[i],px,py-pSz[i]-4);
  }}
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'cell':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🔬 ANIMAL CELL STRUCTURE</div>
<canvas id="cel" width="460" height="310" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">Nucleus · Mitochondria · Golgi · Ribosome · Vacuole · ER</div>
<script>
const cv=document.getElementById('cel'),ctx=cv.getContext('2d'),W=460,H=310,cx=230,cy=155;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#010208';ctx.fillRect(0,0,W,H);
  const pulse=1+.006*Math.sin(t*.04);
  const cytoG=ctx.createRadialGradient(cx,cy,10,cx,cy,205);
  cytoG.addColorStop(0,'rgba(0,70,90,.3)');cytoG.addColorStop(1,'rgba(0,25,40,.08)');
  ctx.beginPath();ctx.ellipse(cx,cy,205*pulse,142*pulse,0,0,6.28);
  ctx.fillStyle=cytoG;ctx.fill();
  ctx.shadowColor='#00b48c';ctx.shadowBlur=10;
  ctx.strokeStyle='rgba(0,180,140,.65)';ctx.lineWidth=2.5;ctx.setLineDash([8,4]);ctx.stroke();
  ctx.shadowBlur=0;ctx.setLineDash([]);
  ctx.fillStyle='rgba(0,180,140,.5)';ctx.font='7px sans-serif';ctx.textAlign='left';ctx.fillText('Cell membrane',10,20);
  const np=1+.012*Math.sin(t*.055);
  const nucG=ctx.createRadialGradient(cx-8,cy-8,3,cx,cy,52);
  nucG.addColorStop(0,'rgba(140,175,255,.55)');nucG.addColorStop(1,'rgba(50,80,200,.18)');
  ctx.beginPath();ctx.ellipse(cx,cy,54*np,44*np,0,0,6.28);
  ctx.fillStyle=nucG;ctx.fill();
  ctx.shadowColor='#6688ff';ctx.shadowBlur=12;
  ctx.strokeStyle='rgba(100,160,255,.7)';ctx.lineWidth=2;ctx.stroke();
  ctx.shadowBlur=0;
  ctx.beginPath();ctx.arc(cx+6,cy,11,0,6.28);
  ctx.fillStyle='rgba(190,130,255,.65)';ctx.fill();ctx.strokeStyle='#c084fc';ctx.lineWidth=1.5;ctx.stroke();
  ctx.fillStyle='#c084fc';ctx.font='7px sans-serif';ctx.textAlign='center';ctx.fillText('Nucleolus',cx+6,cy+3);
  ctx.fillStyle='#8ab4ff';ctx.font='bold 7px sans-serif';ctx.fillText('Nucleus',cx,cy-20);
  const mf=1+.04*Math.sin(t*.06);
  [[cx-130,cy-50,28,12,.3],[cx+100,cy+60,24,11,-.2]].forEach(function(m){{
    const mx=m[0],my=m[1],rw=m[2],rh=m[3],ang=m[4];
    ctx.save();ctx.translate(mx,my);ctx.rotate(ang);
    const mG=ctx.createLinearGradient(-rw,0,rw,0);
    mG.addColorStop(0,'rgba(255,90,0,.28)');mG.addColorStop(.5,'rgba(255,140,0,.5)');mG.addColorStop(1,'rgba(255,90,0,.28)');
    ctx.shadowColor='#ff6600';ctx.shadowBlur=8;
    ctx.beginPath();ctx.ellipse(0,0,rw*mf,rh*mf,0,0,6.28);ctx.fillStyle=mG;ctx.fill();
    ctx.strokeStyle='#ff8c00';ctx.lineWidth=1.5;ctx.stroke();
    for(let cr=1;cr<3;cr++){{ctx.beginPath();ctx.moveTo(-rw+cr*rw*.6,-rh*.7);ctx.bezierCurveTo(-rw+cr*rw*.4,0,-rw+cr*rw*.8,0,-rw+cr*rw*.6,rh*.7);ctx.strokeStyle='rgba(255,160,0,.35)';ctx.lineWidth=1;ctx.stroke();}}
    ctx.shadowBlur=0;ctx.restore();
  }});
  ctx.fillStyle='#ffb04a';ctx.font='7px sans-serif';ctx.textAlign='center';
  ctx.fillText('Mitochondria',cx-130,cy-66);ctx.fillText('Mitochondria',cx+100,cy+78);
  for(let g=0;g<5;g++){{
    ctx.beginPath();ctx.arc(cx+120,cy-20,25+g*9,.55,2.6,false);
    ctx.strokeStyle='rgba(255,105,180,'+(0.35+g*.08)+')';ctx.lineWidth=5;ctx.stroke();
  }}
  ctx.fillStyle='#ff80b0';ctx.font='7px sans-serif';ctx.textAlign='center';ctx.fillText('Golgi body',cx+120,cy-70);
  for(let r=0;r<16;r++){{
    const rx=cx-90+r*11+(r%3)*3,ry=cy+55+Math.sin(r*1.5)*18;
    ctx.beginPath();ctx.arc(rx,ry,2.5,0,6.28);
    ctx.fillStyle='rgba(255,215,0,.78)';ctx.fill();
  }}
  ctx.fillStyle='#ffd700';ctx.font='7px sans-serif';ctx.textAlign='center';ctx.fillText('Ribosomes',cx-60,cy+82);
  ctx.beginPath();ctx.arc(cx-115,cy+40,22,0,6.28);
  ctx.fillStyle='rgba(50,130,210,.16)';ctx.fill();ctx.strokeStyle='rgba(80,170,255,.45)';ctx.lineWidth=1.5;ctx.stroke();
  ctx.fillStyle='#6db3ff';ctx.font='7px sans-serif';ctx.fillText('Vacuole',cx-115,cy+43);
  for(let e=0;e<4;e++){{
    const ey=cy-28+e*14;
    ctx.beginPath();ctx.moveTo(cx+62,ey);ctx.bezierCurveTo(cx+80,ey-6,cx+95,ey+6,cx+112,ey);
    ctx.strokeStyle='rgba(100,200,255,.38)';ctx.lineWidth=3;ctx.stroke();
  }}
  ctx.fillStyle='rgba(100,200,255,.6)';ctx.font='7px sans-serif';ctx.textAlign='center';ctx.fillText('Smooth ER',cx+88,cy-40);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'water':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">💧 THE WATER CYCLE</div>
<canvas id="wc" width="460" height="300" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">Evaporation → Condensation → Precipitation → Collection</div>
<script>
const cv=document.getElementById('wc'),ctx=cv.getContext('2d'),W=460,H=300;
const drops=[];
for(let i=0;i<22;i++)drops.push([120+Math.random()*200,50+Math.random()*80,1.2+Math.random()*1.6,0.45+Math.random()*.5]);
const evapPts=[];
for(let i=0;i<12;i++)evapPts.push([30+i*6,H*.78,0,Math.random(),0.3+Math.random()*.5]);
let t=0;
function cloud(ccx,ccy,s,al){{
  ctx.globalAlpha=al;ctx.fillStyle='rgba(160,190,230,.75)';
  const pts=[[0,0,s],[s*.85,s*.28,s*.72],[-(s*.8),s*.3,s*.68],[s*.5,-(s*.3),s*.55],[-(s*.45),-(s*.28),s*.5]];
  pts.forEach(function(p){{ctx.beginPath();ctx.arc(ccx+p[0],ccy+p[1],p[2],0,6.28);ctx.fill();}});
  ctx.globalAlpha=1;
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  const sky=ctx.createLinearGradient(0,0,0,H*.75);
  sky.addColorStop(0,'#010210');sky.addColorStop(.6,'#071a2e');sky.addColorStop(1,'#0c2a18');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H*.75);
  const sunX=50,sunY=38;
  const sunG=ctx.createRadialGradient(sunX,sunY,2,sunX,sunY,22);
  sunG.addColorStop(0,'#fffde7');sunG.addColorStop(.5,'#ffa000');sunG.addColorStop(1,'rgba(230,80,0,0)');
  ctx.shadowColor='#ff8800';ctx.shadowBlur=18;
  ctx.beginPath();ctx.arc(sunX,sunY,20*(1+.04*Math.sin(t*.05)),0,6.28);ctx.fillStyle=sunG;ctx.fill();
  ctx.shadowBlur=0;
  ctx.fillStyle='rgba(255,220,80,.7)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('☀ SUN',sunX,sunY+32);
  const grdG=ctx.createLinearGradient(0,H*.74,0,H);
  grdG.addColorStop(0,'#0e3010');grdG.addColorStop(1,'#081a06');
  ctx.fillStyle=grdG;ctx.fillRect(0,H*.74,W,H);
  const oceanG=ctx.createLinearGradient(0,H*.76,0,H);
  oceanG.addColorStop(0,'rgba(10,60,180,.7)');oceanG.addColorStop(1,'rgba(5,30,100,.9)');
  ctx.fillStyle=oceanG;ctx.fillRect(0,H*.76,145,H);
  ctx.fillStyle='rgba(100,180,255,.35)';ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillText('OCEAN',72,H*.92);
  const mtnPts=[[280,H*.74],[340,H*.32],[400,H*.74]];
  const mtnG=ctx.createLinearGradient(340,H*.32,340,H*.74);
  mtnG.addColorStop(0,'#2a3a2a');mtnG.addColorStop(1,'#1a2a1a');
  ctx.fillStyle=mtnG;ctx.beginPath();ctx.moveTo(mtnPts[0][0],mtnPts[0][1]);ctx.lineTo(mtnPts[1][0],mtnPts[1][1]);ctx.lineTo(mtnPts[2][0],mtnPts[2][1]);ctx.closePath();ctx.fill();
  ctx.fillStyle='rgba(255,255,255,.25)';ctx.font='7px sans-serif';ctx.fillText('⛰ Mountain',340,H*.4);
  ctx.strokeStyle='rgba(100,180,255,.4)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(280,H*.74);ctx.lineTo(240,H*.78);ctx.lineTo(155,H*.8);ctx.stroke();
  cloud(200,60+2*Math.sin(t*.4),30,0.85);cloud(290,52+2*Math.sin(t*.4+1),25,0.75);cloud(115,75+2*Math.sin(t*.4+2),22,0.7);
  ctx.fillStyle='rgba(200,225,255,.7)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('☁ CLOUDS',200,100);
  evapPts.forEach(function(ep){{
    ep[2]+=ep[3]*0.015;
    if(ep[2]>1){{ep[2]=0;ep[4]=0.3+Math.random()*.5;}}
    const ey=H*.78-ep[2]*(H*.55);
    const eal=ep[2]<0.5?ep[2]*2:2-ep[2]*2;
    ctx.beginPath();ctx.arc(ep[0],ey,2.5,0,6.28);
    ctx.fillStyle='rgba(100,200,255,'+(eal*ep[4]).toFixed(2)+')';ctx.fill();
  }});
  ctx.fillStyle='rgba(100,200,255,.75)';ctx.font='bold 7px sans-serif';ctx.textAlign='left';ctx.fillText('↑ Evaporation',5,H*.45);
  ctx.strokeStyle='rgba(150,200,240,.6)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(100,68);ctx.quadraticCurveTo(145,38,185,58);ctx.stroke();
  ctx.fillStyle='rgba(180,210,240,.65)';ctx.font='7px sans-serif';ctx.fillText('Condensation →',68,38);
  drops.forEach(function(d){{
    d[1]+=d[2];
    if(d[1]>H*.78){{d[1]=50+Math.random()*80;d[0]=120+Math.random()*200;}}
    ctx.beginPath();ctx.arc(d[0],d[1],2.2,0,6.28);
    ctx.fillStyle='rgba(80,160,255,'+d[3].toFixed(2)+')';ctx.fill();
  }});
  ctx.fillStyle='rgba(80,170,255,.8)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('↓ Precipitation',215,H*.2);
  ctx.fillStyle='rgba(60,160,255,.55)';ctx.font='7px sans-serif';ctx.fillText('→ Runoff',230,H*.72);
  ctx.fillStyle='rgba(255,255,255,.22)';ctx.font='7px monospace';ctx.fillText('Water moves through Evaporation → Condensation → Precipitation → Collection',W/2,H-5);
  t+=0.035;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'wave':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">〰 TRANSVERSE WAVE — SHM</div>
<canvas id="wv" width="360" height="200" style="display:block;"></canvas>
<div style="display:flex;gap:14px;font-size:11px;margin-top:6px;">
  <span style="color:#00e5ff">— Displacement</span><span style="color:#a855f7">— Velocity</span>
</div>
<script>
const cv=document.getElementById('wv'),ctx=cv.getContext('2d'),W=360,H=200,mid=H/2;
const lam=88,amp=68,vamp=48;let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.12)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(0,mid);ctx.lineTo(W,mid);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,0.35)';ctx.font='8px monospace';
  ctx.fillText('Crest',4,mid-amp-6);ctx.fillText('Trough',4,mid+amp+16);ctx.fillText('Equilibrium',4,mid-10);
  ctx.fillText('→ Wave travel direction',W-180,22);
  ctx.beginPath();for(let x=0;x<=W;x++){{const y=mid-amp*Math.sin(2*Math.PI*x/lam-t);x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);}}
  ctx.strokeStyle='#00e5ff';ctx.lineWidth=2.5;ctx.stroke();
  ctx.beginPath();for(let x=0;x<=W;x++){{const y=mid-vamp*Math.cos(2*Math.PI*x/lam-t);x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);}}
  ctx.strokeStyle='rgba(168,85,247,0.65)';ctx.lineWidth=1.5;ctx.stroke();
  const px=32,py=mid-amp*Math.sin(2*Math.PI*px/lam-t);
  ctx.strokeStyle='rgba(255,200,80,.6)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(px,mid);ctx.lineTo(px,py);ctx.stroke();
  ctx.fillStyle='rgba(255,200,80,.9)';ctx.fillText('A',px+3,mid-(py-mid)/2);
  ctx.strokeStyle='rgba(80,200,80,.6)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(50,mid+amp+28);ctx.lineTo(50+lam,mid+amp+28);ctx.stroke();
  [50,50+lam].forEach(x=>{{ctx.beginPath();ctx.moveTo(x,mid+amp+23);ctx.lineTo(x,mid+amp+33);ctx.stroke();}});
  ctx.fillStyle='rgba(80,200,80,.9)';ctx.fillText('λ (wavelength)',58,mid+amp+42);
  t+=0.06;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'heart':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">❤ HUMAN HEART — BLOOD CIRCULATION</div>
<canvas id="hrt" width="460" height="310" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">● Red = Oxygenated  ● Blue = Deoxygenated  · Heart pumps ~70 times/min</div>
<script>
const cv=document.getElementById('hrt'),ctx=cv.getContext('2d'),W=460,H=310;
const hx=230,hy=158;
const dots=[];
for(let i=0;i<24;i++)dots.push([Math.random(),i%2,0.55+Math.random()*.45]);
let t=0;
function heartPath(s){{
  ctx.beginPath();ctx.moveTo(hx,hy-42*s);
  ctx.bezierCurveTo(hx+70*s,hy-95*s,hx+120*s,hy-22*s,hx,hy+60*s);
  ctx.bezierCurveTo(hx-120*s,hy-22*s,hx-70*s,hy-95*s,hx,hy-42*s);
  ctx.closePath();
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#010208';ctx.fillRect(0,0,W,H);
  const beat=0.92+.07*Math.sin(t*3);
  heartPath(beat);
  const hg=ctx.createRadialGradient(hx,hy-12,8,hx,hy,90*beat);
  hg.addColorStop(0,'rgba(220,30,40,.95)');hg.addColorStop(.45,'rgba(170,15,25,.75)');hg.addColorStop(1,'rgba(80,5,10,.35)');
  ctx.shadowColor='#cc1122';ctx.shadowBlur=20;
  ctx.fillStyle=hg;ctx.fill();
  ctx.strokeStyle='rgba(240,80,80,.7)';ctx.lineWidth=2.2*beat;ctx.stroke();
  ctx.shadowBlur=0;
  const sc=beat;
  ctx.fillStyle='rgba(0,0,0,.52)';
  ctx.beginPath();ctx.ellipse(hx-22*sc,hy-16*sc,34*sc,27*sc,0,0,6.28);ctx.fill();
  ctx.beginPath();ctx.ellipse(hx+22*sc,hy-16*sc,34*sc,27*sc,0,0,6.28);ctx.fill();
  ctx.fillStyle='rgba(0,0,0,.42)';
  ctx.beginPath();ctx.ellipse(hx-24*sc,hy+20*sc,30*sc,32*sc,0,0,6.28);ctx.fill();
  ctx.beginPath();ctx.ellipse(hx+24*sc,hy+20*sc,30*sc,32*sc,0,0,6.28);ctx.fill();
  ctx.strokeStyle='rgba(255,200,200,.2)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(hx,hy-42*sc);ctx.lineTo(hx,hy+56*sc);ctx.stroke();
  ctx.font='bold 7px sans-serif';ctx.textAlign='center';
  ctx.fillStyle='rgba(160,195,255,.9)';ctx.fillText('Right',hx+22*sc,hy-14*sc);
  ctx.fillStyle='rgba(255,180,180,.9)';ctx.fillText('Left',hx-22*sc,hy-14*sc);
  ctx.fillStyle='rgba(210,215,255,.7)';
  ctx.fillText('Atrium',hx+22*sc,hy-5*sc);ctx.fillText('Atrium',hx-22*sc,hy-5*sc);
  ctx.fillText('Ventricle',hx+24*sc,hy+24*sc);ctx.fillText('Ventricle',hx-24*sc,hy+24*sc);
  ctx.strokeStyle='rgba(255,120,120,.4)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(hx-3,hy-72);ctx.lineTo(hx-3,hy-115);ctx.stroke();
  ctx.strokeStyle='rgba(100,140,255,.4)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(hx+3,hy-72);ctx.lineTo(hx+3,hy-115);ctx.stroke();
  ctx.fillStyle='rgba(255,140,140,.65)';ctx.font='7px sans-serif';ctx.textAlign='left';ctx.fillText('Aorta',hx-30,hy-108);
  ctx.fillStyle='rgba(120,160,255,.65)';ctx.textAlign='right';ctx.fillText('Pulmonary A.',hx+35,hy-108);
  dots.forEach(function(d){{
    d[0]+=0.007;if(d[0]>1)d[0]=0;
    var px,py;
    if(d[1]===0){{px=hx-24*sc+30*sc*Math.sin(d[0]*6.28);py=hy+20*sc-32*sc*Math.cos(d[0]*6.28);}}
    else{{px=hx+22*sc+30*sc*Math.sin(d[0]*6.28+Math.PI);py=hy-16*sc-27*sc*Math.cos(d[0]*6.28);}}
    ctx.beginPath();ctx.arc(px,py,3.2,0,6.28);
    ctx.fillStyle=d[1]===0?'rgba(239,83,80,'+d[2].toFixed(2)+')':'rgba(92,141,232,'+d[2].toFixed(2)+')';ctx.fill();
  }});
  ctx.fillStyle='rgba(255,255,255,.28)';ctx.font='7px monospace';ctx.textAlign='center';
  ctx.fillText('Right side: deoxygenated blood → lungs   Left side: oxygenated blood → body',W/2,H-5);
  t+=0.042;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'photosynthesis':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🌿 PHOTOSYNTHESIS</div>
<canvas id="phs" width="460" height="310" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">6CO₂ + 6H₂O + Sunlight → C₆H₁₂O₆ + 6O₂</div>
<script>
const cv=document.getElementById('phs'),ctx=cv.getContext('2d'),W=460,H=310;
const co2=[],o2=[],rays=[];
for(let i=0;i<8;i++)co2.push([20+i*5,100+i*18,0.5+i*.06,0.6+Math.random()*.35]);
for(let i=0;i<10;i++)o2.push([230+(-45+Math.random()*90),120+Math.random()*55,0.5+Math.random()*.7,0,2+Math.random()*2.5]);
for(let i=0;i<9;i++)rays.push([-0.55+i*.13,55+15*Math.random()]);
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const sky=ctx.createLinearGradient(0,0,0,H*.62);
  sky.addColorStop(0,'#010210');sky.addColorStop(1,'#061a0a');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  const grd=ctx.createLinearGradient(0,H*.62,0,H);
  grd.addColorStop(0,'#0a1f08');grd.addColorStop(1,'#060e04');
  ctx.fillStyle=grd;ctx.fillRect(0,H*.62,W,H);
  const sx=62,sy=45;
  const sunG=ctx.createRadialGradient(sx,sy,2,sx,sy,22);
  sunG.addColorStop(0,'#fffde7');sunG.addColorStop(.5,'#ffa000');sunG.addColorStop(1,'rgba(230,80,0,0)');
  ctx.shadowColor='#ff8800';ctx.shadowBlur=20;
  ctx.beginPath();ctx.arc(sx,sy,21*(1+.04*Math.sin(t*.05)),0,6.28);ctx.fillStyle=sunG;ctx.fill();
  ctx.shadowBlur=0;
  ctx.fillStyle='rgba(255,220,80,.7)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('☀ SUN',sx,sy+34);
  rays.forEach(function(r,i){{
    const rlen=r[1]*(1+.15*Math.sin(t*2+i));
    const ral=(0.28+0.18*Math.sin(t+i)).toFixed(2);
    ctx.strokeStyle='rgba(255,220,80,'+ral+')';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.moveTo(sx+22*Math.cos(r[0]),sy+22*Math.sin(r[0]));
    ctx.lineTo(sx+(22+rlen)*Math.cos(r[0]+.2),sy+(22+rlen)*Math.sin(r[0]+.8));ctx.stroke();
  }});
  const lx=230,ly=H*.55;
  ctx.strokeStyle='#2a5818';ctx.lineWidth=9;ctx.beginPath();ctx.moveTo(lx,ly);ctx.lineTo(lx,H*.94);ctx.stroke();
  const leafG=ctx.createRadialGradient(lx,ly-10,5,lx,ly,62);
  leafG.addColorStop(0,'rgba(60,140,30,.95)');leafG.addColorStop(.6,'rgba(40,100,20,.8)');leafG.addColorStop(1,'rgba(25,70,10,.5)');
  ctx.shadowColor='#44aa22';ctx.shadowBlur=10;
  ctx.beginPath();ctx.ellipse(lx,ly-8,64,48,0,0,6.28);ctx.fillStyle=leafG;ctx.fill();
  ctx.shadowBlur=0;
  ctx.strokeStyle='rgba(80,180,40,.4)';ctx.lineWidth=1.2;
  ctx.beginPath();ctx.moveTo(lx-64,ly-8);ctx.lineTo(lx+64,ly-8);ctx.stroke();
  ctx.beginPath();ctx.moveTo(lx,ly-56);ctx.lineTo(lx,ly+32);ctx.stroke();
  ctx.fillStyle='rgba(200,255,200,.75)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';
  ctx.fillText('CHLOROPHYLL',lx,ly-18);ctx.fillText('(leaf)',lx,ly-7);
  ctx.beginPath();ctx.ellipse(lx-45,H*.75,38,18,.3,0,6.28);ctx.fillStyle='rgba(35,90,18,.7)';ctx.fill();
  ctx.beginPath();ctx.ellipse(lx+45,H*.82,38,18,-.3,0,6.28);ctx.fill();
  co2.forEach(function(c){{
    c[0]+=c[2];c[1]+=(H*.52-c[1])*.025;
    if(c[0]>lx-60)c[0]=5+Math.random()*30;
    ctx.beginPath();ctx.arc(c[0],c[1],3.5,0,6.28);
    ctx.fillStyle='rgba(100,170,255,'+c[3].toFixed(2)+')';ctx.fill();
    ctx.fillStyle='rgba(100,170,255,.55)';ctx.font='7px sans-serif';ctx.textAlign='center';
    if(c[0]<lx-68)ctx.fillText('CO₂',c[0],c[1]-6);
  }});
  ctx.fillStyle='rgba(100,180,255,.7)';ctx.font='bold 7px sans-serif';ctx.textAlign='left';ctx.fillText('CO₂ →',5,H*.35);
  ctx.fillText('H₂O ↑',5,H*.72);
  o2.forEach(function(o){{
    o[1]-=o[2];o[3]=Math.min(1,o[3]+.025);
    if(o[1]<-10){{o[1]=H*.48+Math.random()*30;o[0]=lx+(-45+Math.random()*90);o[3]=0;}}
    ctx.beginPath();ctx.arc(o[0],o[1],o[4],0,6.28);
    ctx.strokeStyle='rgba(160,255,160,'+(o[3]*.7).toFixed(2)+')';ctx.lineWidth=1.2;ctx.stroke();
  }});
  ctx.fillStyle='rgba(160,255,160,.75)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('↑ O₂ released',lx,H*.12);
  ctx.fillStyle='rgba(255,220,100,.7)';ctx.font='bold 7px sans-serif';ctx.textAlign='right';
  ctx.fillText('Glucose →',W-5,H*.4);ctx.fillText('(stored energy)',W-5,H*.48);
  ctx.fillStyle='rgba(255,255,255,.22)';ctx.font='7px monospace';ctx.textAlign='center';
  ctx.fillText('Light energy + CO₂ + H₂O → Glucose + Oxygen (in chloroplasts)',W/2,H-5);
  t+=0.04;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'circuit':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">⚡ ELECTRIC CIRCUIT — CURRENT FLOW</div>
<canvas id="ec" width="340" height="240" style="display:block;"></canvas>
<div style="display:flex;gap:12px;font-size:11px;margin-top:4px;">
  <span style="color:#ffd700">● Conventional current →</span><span style="color:#00e5ff">+ Battery</span>
</div>
<script>
const cv=document.getElementById('ec'),ctx=cv.getContext('2d'),W=340,H=240;
const path=[{{x:60,y:60}},{{x:280,y:60}},{{x:280,y:180}},{{x:60,y:180}},{{x:60,y:60}}];
let dots=[];
for(let i=0;i<18;i++) dots.push({{p:i/18,spd:0.003+Math.random()*.001}});
function ptOnPath(p){{
  const total=3,seg=Math.floor(p*total)%total,lp=(p*total)%1;
  const segs=[[path[0],path[1]],[path[1],path[2]],[path[2],path[3]],[path[3],path[0]]];
  const s=segs[seg];return{{x:s[0].x+(s[1].x-s[0].x)*lp,y:s[0].y+(s[1].y-s[0].y)*lp}};
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(100,180,255,0.5)';ctx.lineWidth=6;ctx.lineJoin='round';
  ctx.beginPath();ctx.moveTo(60,60);ctx.lineTo(280,60);ctx.lineTo(280,180);ctx.lineTo(60,180);ctx.lineTo(60,60);ctx.stroke();
  ctx.fillStyle='rgba(0,200,100,0.85)';ctx.strokeStyle='#00c864';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(40,95,35,50,5);ctx.fill();ctx.stroke();
  ctx.fillStyle='#fff';ctx.font='bold 10px monospace';ctx.textAlign='center';
  ctx.fillText('+',57,117);ctx.fillText('-',57,132);
  ctx.fillStyle='rgba(0,200,100,0.7)';ctx.font='8px monospace';ctx.fillText('Battery',57,158);
  ctx.fillStyle='rgba(255,100,50,0.85)';ctx.strokeStyle='#ff6432';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(148,42,50,16,4);ctx.fill();ctx.stroke();
  ctx.fillStyle='#fff';ctx.fillText('Resistor',173,53);
  ctx.fillStyle='rgba(80,120,255,0.8)';ctx.strokeStyle='#5078ff';ctx.lineWidth=2;
  ctx.beginPath();ctx.arc(280,120,16,0,6.28);ctx.fill();ctx.stroke();
  ctx.fillStyle='#fff';ctx.font='bold 9px monospace';ctx.fillText('💡',272,124);
  ctx.fillStyle='rgba(255,200,50,0.5)';ctx.beginPath();ctx.arc(280,120,22,0,6.28);ctx.fill();
  ctx.strokeStyle='rgba(80,160,255,0.5)';ctx.lineWidth=1.5;
  [[165,60],[165,180]].forEach(([x,y])=>{{ctx.beginPath();ctx.moveTo(x-5,y);ctx.lineTo(x+5,y);ctx.stroke();}});
  dots.forEach(d=>{{
    d.p=(d.p+d.spd)%1;
    const pt=ptOnPath(d.p);
    ctx.beginPath();ctx.arc(pt.x,pt.y,4,0,6.28);ctx.fillStyle='rgba(255,215,0,0.85)';ctx.fill();
  }});
  ctx.textAlign='left';ctx.fillStyle='rgba(255,255,255,0.35)';ctx.font='8px monospace';
  ctx.fillText('Series circuit · conventional current (+ → -)',10,H-6);
  requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'eye':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">👁 HUMAN EYE — CROSS SECTION</div>
<svg viewBox="0 0 380 260" width="360" height="248" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="eyeG" cx="38%" cy="40%"><stop offset="0%" stop-color="rgba(220,240,255,0.15)"/><stop offset="100%" stop-color="rgba(80,120,180,0.08)"/></radialGradient>
    <radialGradient id="irisG" cx="45%" cy="45%"><stop offset="0%" stop-color="#4a3000"/><stop offset="40%" stop-color="#6b4400"/><stop offset="100%" stop-color="#3a2800"/></radialGradient>
  </defs>
  <ellipse cx="170" cy="130" rx="130" ry="115" fill="url(#eyeG)" stroke="#4a6a9a" stroke-width="2.5"/>
  <circle cx="85" cy="130" r="26" fill="rgba(200,230,255,0.35)" stroke="#7ab4e8" stroke-width="2"/>
  <text x="85" y="133" text-anchor="middle" fill="#a8d0ff" font-size="8" font-family="monospace">Cornea</text>
  <ellipse cx="118" cy="130" rx="14" ry="30" fill="rgba(180,220,255,0.25)" stroke="#90c4f4" stroke-width="1.5"/>
  <text x="118" y="133" text-anchor="middle" fill="#b8d8ff" font-size="7" font-family="monospace">Lens</text>
  <circle cx="101" cy="130" r="15" fill="url(#irisG)" stroke="#8a6030" stroke-width="1"/>
  <circle cx="101" cy="130" r="8" fill="#050505"/>
  <circle cx="97" cy="126" r="2" fill="#ffffff55"/>
  <ellipse cx="285" cy="130" rx="22" ry="90" fill="rgba(220,180,150,0.45)" stroke="#d4a070" stroke-width="2"/>
  <text x="285" y="133" text-anchor="middle" fill="#e8b888" font-size="8" font-family="monospace">Retina</text>
  <line x1="285" y1="130" x2="355" y2="130" stroke="#e86464" stroke-width="3">
    <animate attributeName="stroke-opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
  </line>
  <circle cx="360" cy="130" r="6" fill="#e86464"><animate attributeName="r" values="6;8;6" dur="1.5s" repeatCount="indefinite"/></circle>
  <text x="295" y="148" fill="#e89090" font-size="8" font-family="monospace">Optic</text>
  <text x="295" y="158" fill="#e89090" font-size="8" font-family="monospace">Nerve</text>
  <ellipse cx="130" cy="130" rx="8" ry="22" fill="rgba(200,200,255,0.2)" stroke="#8888ff" stroke-width="1"/>
  <text x="125" y="170" fill="#aaaaff" font-size="7.5" font-family="monospace">Pupil</text>
  <text x="82" y="168" fill="#88aacc" font-size="7.5" font-family="monospace">Iris</text>
  <line x1="30" y1="100" x2="76" y2="118" stroke="#ffd700" stroke-width="2" stroke-dasharray="4 3">
    <animate attributeName="stroke-dashoffset" values="0;-14" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <line x1="30" y1="130" x2="62" y2="130" stroke="#ffd700" stroke-width="2" stroke-dasharray="4 3">
    <animate attributeName="stroke-dashoffset" values="0;-14" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <line x1="30" y1="160" x2="76" y2="142" stroke="#ffd700" stroke-width="2" stroke-dasharray="4 3">
    <animate attributeName="stroke-dashoffset" values="0;-14" dur="0.5s" repeatCount="indefinite"/>
  </line>
  <text x="4" y="133" fill="#ffd700" font-size="9" font-family="monospace">Light</text>
  <line x1="120" y1="108" x2="276" y2="152" stroke="rgba(255,215,0,0.2)" stroke-width="1" stroke-dasharray="3 4"/>
  <line x1="120" y1="152" x2="276" y2="108" stroke="rgba(255,215,0,0.2)" stroke-width="1" stroke-dasharray="3 4"/>
  <text x="175" y="248" fill="#666" font-size="8" font-family="monospace">Vitreous humour fills the eye cavity</text>
</svg></body></html>"""

    elif topic == 'magnet':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🧲 MAGNETIC FIELD LINES</div>
<canvas id="mg" width="360" height="240" style="display:block;"></canvas>
<div style="display:flex;gap:14px;font-size:11px;margin-top:4px;">
  <span style="color:#ef5350">■ North pole</span><span style="color:#5c8de8">■ South pole</span>
</div>
<script>
const cv=document.getElementById('mg'),ctx=cv.getContext('2d'),W=360,H=240,cx=W/2,cy=H/2;
let t=0;
const nX=cx-60,sX=cx+60;
function fieldAt(x,y){{
  const dx1=x-nX,dy1=y-cy,dx2=x-sX,dy2=y-cy;
  const r1=Math.sqrt(dx1*dx1+dy1*dy1)+1,r2=Math.sqrt(dx2*dx2+dy2*dy2)+1;
  const fx=dx1/(r1*r1*r1)-dx2/(r2*r2*r2),fy=dy1/(r1*r1*r1)-dy2/(r2*r2*r2);
  const mag=Math.sqrt(fx*fx+fy*fy)+1e-9;
  return{{fx:fx/mag,fy:fy/mag,mag:mag}};
}}
function drawLine(sx,sy,color){{
  ctx.beginPath();ctx.moveTo(sx,sy);
  let x=sx,y=sy;
  for(let i=0;i<200;i++){{
    const f=fieldAt(x,y);x+=f.fx*3;y+=f.fy*3;
    ctx.lineTo(x,y);
    const dN=Math.sqrt((x-nX)**2+(y-cy)**2),dS=Math.sqrt((x-sX)**2+(y-cy)**2);
    if(dN<14||dS<14||x<0||x>W||y<0||y>H) break;
  }}
  ctx.strokeStyle=color;ctx.lineWidth=1.2;ctx.stroke();
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  const angles=12;
  for(let i=0;i<angles;i++){{
    const a=i*2*Math.PI/angles+t*0.01;
    const r=18;
    drawLine(nX+r*Math.cos(a),cy+r*Math.sin(a),`rgba(100,${150+80*Math.sin(a+t*.05)},255,0.55)`);
  }}
  ctx.fillStyle='#ef5350';ctx.beginPath();ctx.roundRect(nX-32,cy-20,32,40,4);ctx.fill();
  ctx.fillStyle='#5c8de8';ctx.beginPath();ctx.roundRect(sX,cy-20,32,40,4);ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 14px monospace';ctx.textAlign='center';
  ctx.fillText('N',nX-16,cy+5);ctx.fillText('S',sX+16,cy+5);
  ctx.strokeStyle='rgba(255,255,255,0.2)';ctx.lineWidth=1.5;
  for(let a=0;a<Math.PI*2;a+=Math.PI/6){{
    const px=nX+20*Math.cos(a+t*0.02),py=cy+20*Math.sin(a+t*0.02);
    ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px+6*Math.cos(a+t*.02),py+6*Math.sin(a+t*.02));ctx.stroke();
  }}
  ctx.textAlign='left';ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';
  ctx.fillText('Field lines go N→S outside, S→N inside magnet',10,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'mitosis':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🔬 MITOSIS — CELL DIVISION</div>
<canvas id="mt" width="360" height="220" style="display:block;"></canvas>
<div style="font-size:10px;color:#8aa;margin-top:4px;text-align:center;">Interphase → Prophase → Metaphase → Anaphase → Telophase → Cytokinesis</div>
<script>
const cv=document.getElementById('mt'),ctx=cv.getContext('2d'),W=360,H=220;
let t=0;
const phases=['Interphase','Prophase','Metaphase','Anaphase','Telophase','Cytokinesis'];
const dur=180;
function drawCell(cx,cy,rx,ry,color,nrx,nry,label,chromosomes,split,splitProg){{
  ctx.beginPath();ctx.ellipse(cx,cy,rx,ry,0,0,6.28);
  ctx.fillStyle=`rgba(40,180,100,0.1)`;ctx.fill();ctx.strokeStyle=color;ctx.lineWidth=2;ctx.stroke();
  if(chromosomes){{
    for(let i=0;i<4;i++){{
      const cx2=cx-10+i*7,cy2=cy+(split?-10-splitProg*20:0);
      ctx.beginPath();ctx.roundRect(cx2-3,cy2-6,6,12,3);
      ctx.fillStyle=['#ef5350','#5c8de8','#ffd700','#a855f7'][i];ctx.fill();
      if(split){{
        const cy3=cy+10+splitProg*20;
        ctx.beginPath();ctx.roundRect(cx2-3,cy3-6,6,12,3);
        ctx.fillStyle=['#ef5350','#5c8de8','#ffd700','#a855f7'][i];ctx.fill();
      }}
    }}
  }}
  if(nrx>0){{
    ctx.beginPath();ctx.ellipse(cx,cy,nrx,nry,0,0,6.28);
    ctx.fillStyle='rgba(100,150,255,0.18)';ctx.fill();ctx.strokeStyle='#6496ff';ctx.lineWidth=1.5;ctx.stroke();
  }}
  if(label){{ctx.fillStyle='rgba(255,255,255,0.6)';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText(label,cx,cy+ry+14);}}
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  const phase=Math.floor(t/dur)%6,prog=(t%dur)/dur;
  const label=phases[phase];
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='bold 11px monospace';ctx.textAlign='center';
  ctx.fillText('Phase: '+label,W/2,18);
  if(phase===0){{drawCell(W/2,H/2+10,75,65,'#22c55e',32,28,'',false,false,0);}}
  else if(phase===1){{drawCell(W/2,H/2+10,75,65,'#ffd700',32*(1-prog),28*(1-prog),'',true,false,0);}}
  else if(phase===2){{drawCell(W/2,H/2+10,75,65,'#ff9944',0,0,'',true,false,0);}}
  else if(phase===3){{drawCell(W/2,H/2+10,75,65,'#ef5350',0,0,'',true,true,prog);}}
  else if(phase===4){{
    const sep=prog*50;
    drawCell(W/2,H/2+10-sep/2,70*(1-prog*.3),58*(1-prog*.3),'#a855f7',22,18,'',false,false,0);
    drawCell(W/2,H/2+10+sep/2,70*(1-prog*.3),58*(1-prog*.3),'#a855f7',22,18,'',false,false,0);
  }}
  else{{
    const gap=60+prog*30;
    drawCell(W/2-gap/2,H/2+10,50,44,'#22c55e',20,17,'Cell 1',false,false,0);
    drawCell(W/2+gap/2,H/2+10,50,44,'#22c55e',20,17,'Cell 2',false,false,0);
  }}
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'moon':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🌙 PHASES OF THE MOON</div>
<canvas id="mn" width="360" height="200" style="display:block;"></canvas>
<script>
const cv=document.getElementById('mn'),ctx=cv.getContext('2d'),W=360,H=200;
let t=0;
const phases=[
  {{name:'New Moon',illum:0}},{{name:'Waxing Crescent',illum:0.25}},
  {{name:'First Quarter',illum:0.5}},{{name:'Waxing Gibbous',illum:0.75}},
  {{name:'Full Moon',illum:1}},{{name:'Waning Gibbous',illum:0.75,wane:true}},
  {{name:'Last Quarter',illum:0.5,wane:true}},{{name:'Waning Crescent',illum:0.25,wane:true}},
];
const r=18,spacing=44,startX=20+r;
function drawMoon(x,y,illum,wane,current){{
  ctx.beginPath();ctx.arc(x,y,r,0,6.28);ctx.fillStyle='#1a1a2e';ctx.fill();
  ctx.strokeStyle=current?'#40E0D0':'rgba(255,255,255,0.2)';ctx.lineWidth=current?2:1;ctx.stroke();
  if(illum>0){{
    ctx.save();ctx.beginPath();ctx.arc(x,y,r,0,6.28);ctx.clip();
    const lit=r*2*illum;
    if(wane){{ctx.fillStyle='#c8c8d8';ctx.fillRect(x-r,y-r,lit,r*2);}}
    else{{ctx.fillStyle='#c8c8d8';ctx.fillRect(x+r-lit,y-r,lit,r*2);}}
    ctx.restore();
  }}
  if(current){{
    ctx.beginPath();ctx.arc(x,y,r+4,0,6.28);
    ctx.strokeStyle='rgba(64,224,208,0.4)';ctx.lineWidth=2;ctx.stroke();
  }}
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  const cur=Math.floor(t/80)%8;
  ctx.fillStyle='rgba(100,200,255,0.2)';ctx.fillRect(0,H*0.58,W,2);
  ctx.strokeStyle='#ffdd44';ctx.lineWidth=2;
  ctx.beginPath();ctx.arc(W/2,H*0.58+40,20,0,6.28);ctx.strokeStyle='#ffa000';ctx.stroke();
  ctx.fillStyle='#fff9c4';ctx.beginPath();ctx.arc(W/2,H*0.58+40,16,0,6.28);ctx.fill();
  ctx.fillStyle='rgba(255,220,50,0.5)';ctx.font='7px monospace';ctx.textAlign='center';ctx.fillText('Earth',W/2,H*0.58+56);
  phases.forEach((p,i)=>{{
    const x=startX+i*spacing,y=H*0.25;
    drawMoon(x,y,p.illum,p.wane||false,i===cur);
    ctx.strokeStyle='rgba(255,255,255,0.2)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(x,y+r);ctx.lineTo(W/2,H*0.58+40);ctx.stroke();
    ctx.fillStyle=i===cur?'#40E0D0':'rgba(255,255,255,0.45)';ctx.font=i===cur?'bold 7px monospace':'7px monospace';
    ctx.fillText(p.name.split(' ')[0],x,y+r+14);
    if(p.name.includes(' '))ctx.fillText(p.name.split(' ').slice(1).join(' '),x,y+r+23);
  }});
  ctx.textAlign='left';ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';
  ctx.fillText('One lunar cycle ≈ 29.5 days',10,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'newton':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">⚙ NEWTON'S THREE LAWS OF MOTION</div>
<canvas id="nw" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('nw'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
function arrow(x1,y1,x2,y2,color,lw){{
  ctx.strokeStyle=color;ctx.lineWidth=lw||2;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  const a=Math.atan2(y2-y1,x2-x1);
  ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-10*Math.cos(a-0.4),y2-10*Math.sin(a-0.4));ctx.lineTo(x2-10*Math.cos(a+0.4),y2-10*Math.sin(a+0.4));ctx.closePath();ctx.fillStyle=color;ctx.fill();
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  const rowH=H/3;
  ['1st Law','2nd Law','3rd Law'].forEach((l,i)=>{{
    ctx.fillStyle='rgba(64,224,208,0.08)';ctx.fillRect(0,i*rowH,W,rowH-2);
    ctx.fillStyle='#40E0D0';ctx.font='bold 9px monospace';ctx.textAlign='left';
    ctx.fillText('Law '+l.charAt(0)+':',6,i*rowH+14);
  }});
  // Law 1: Object at rest stays at rest
  const r1=rowH/2-4,cy1=r1+2;
  if(t<120){{
    ctx.beginPath();ctx.arc(70,cy1,14,0,6.28);ctx.fillStyle='#5c8de8';ctx.fill();
    ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='7px monospace';ctx.textAlign='center';ctx.fillText('At rest',70,cy1+3);
  }} else {{
    const bx=60+((t-120)%120)*1.4;
    ctx.beginPath();ctx.arc(bx,cy1,14,0,6.28);ctx.fillStyle='#5c8de8';ctx.fill();
    arrow(bx+14,cy1,bx+45,cy1,'#ffd700',2);
    ctx.fillStyle='#ffd700';ctx.font='7px monospace';ctx.textAlign='center';ctx.fillText('v=const',bx+14,cy1+25);
  }}
  ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='8px monospace';ctx.textAlign='left';
  ctx.fillText('Object stays still or moves at constant velocity unless acted on by force',150,cy1+4);
  // Law 2: F=ma
  const cy2=rowH+rowH/2-4;
  const bx2=40+((t*1.5)%220);const fsize=8+6*Math.abs(Math.sin(t*0.04));
  ctx.beginPath();ctx.arc(bx2,cy2,12,0,6.28);ctx.fillStyle='#ef5350';ctx.fill();
  arrow(bx2,cy2,bx2+25+fsize*2,cy2,'#ffd700',2);
  ctx.fillStyle='#ffd700';ctx.font='7px monospace';ctx.textAlign='center';ctx.fillText('F',bx2+16+fsize,cy2-10);
  ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='8px monospace';ctx.textAlign='left';
  ctx.fillText('F = m×a   (more force = more acceleration)',150,cy2+4);
  // Law 3: action-reaction
  const cy3=rowH*2+rowH/2-4;
  const sep=30+20*Math.abs(Math.sin(t*0.04));
  ctx.beginPath();ctx.arc(W/3-sep/2,cy3,13,0,6.28);ctx.fillStyle='#a855f7';ctx.fill();
  ctx.beginPath();ctx.arc(W/3+sep/2,cy3,13,0,6.28);ctx.fillStyle='#22c55e';ctx.fill();
  arrow(W/3-sep/2-13,cy3,W/3-sep/2-40,cy3,'#a855f7',2);
  arrow(W/3+sep/2+13,cy3,W/3+sep/2+40,cy3,'#22c55e',2);
  ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='8px monospace';ctx.textAlign='left';
  ctx.fillText('Every action has an equal and opposite reaction',150,cy3+4);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'refraction':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">💡 REFRACTION OF LIGHT</div>
<canvas id="rf" width="360" height="240" style="display:block;"></canvas>
<div style="font-size:10px;color:#8aa;margin-top:4px;text-align:center;">Light bends when passing from one medium to another (Snell's Law)</div>
<script>
const cv=document.getElementById('rf'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#05080f';ctx.fillRect(0,0,W,H);
  const px=180,py=100,pw=80,ph=140;
  const grad=ctx.createLinearGradient(px-pw/2,0,px+pw/2,0);
  grad.addColorStop(0,'rgba(150,200,255,0.12)');grad.addColorStop(0.5,'rgba(200,230,255,0.2)');grad.addColorStop(1,'rgba(150,200,255,0.12)');
  ctx.fillStyle=grad;ctx.beginPath();
  ctx.moveTo(px-pw/2,py);ctx.lineTo(px+pw/2,py);ctx.lineTo(px+pw/2-20,py+ph);ctx.lineTo(px-pw/2-20,py+ph);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(150,200,255,0.5)';ctx.lineWidth=1.5;ctx.stroke();
  ctx.fillStyle='rgba(150,200,255,0.5)';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText('Glass (denser medium)',px-10,py+ph/2+4);
  ctx.textAlign='left';
  const inc=+0.3+0.05*Math.sin(t*.03),bend=inc*0.55;
  const ix=60,iy=30,ix2=px-pw/2,iy2=py;
  const rx1=px+pw/2-20+50*Math.sin(bend),ry1=py+ph+50*Math.cos(bend);
  const tx1=px+pw/2-20,ty1=py+ph;
  const a=Math.atan2(iy2-iy,ix2-ix);
  ctx.strokeStyle='rgba(255,220,80,0.9)';ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(ix,iy);ctx.lineTo(ix2,iy2);ctx.stroke();
  ctx.beginPath();ctx.moveTo(ix2,iy2);ctx.lineTo(tx1-20,ty1-20);ctx.stroke();
  ctx.strokeStyle='rgba(255,180,50,0.85)';ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(tx1,ty1);ctx.lineTo(rx1,ry1);ctx.stroke();
  ctx.strokeStyle='rgba(255,255,255,0.15)';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(px-pw/2,py-30);ctx.lineTo(px-pw/2,py+40);ctx.stroke();
  ctx.beginPath();ctx.moveTo(tx1-5,ty1-30);ctx.lineTo(tx1-5,ty1+40);ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='8px monospace';
  ctx.fillText('Incident ray',20,25);ctx.fillText('Refracted ray',rx1-10,ry1+14);
  ctx.fillText('Normal',px-pw/2-38,py-18);
  ctx.fillStyle='rgba(255,200,100,0.7)';ctx.fillText('i',px-pw/2+8,py-8);
  ctx.fillText('r',tx1+4,ty1+18);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'reflection':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🪞 REFLECTION OF LIGHT — CONCAVE MIRROR</div>
<canvas id="rm" width="360" height="240" style="display:block;"></canvas>
<div style="font-size:10px;color:#8aa;margin-top:4px;text-align:center;">Angle of incidence = Angle of reflection</div>
<script>
const cv=document.getElementById('rm'),ctx=cv.getContext('2d'),W=360,H=240,cx=W/2,cy=H/2;
let t=0;
function arrow(x1,y1,x2,y2,col){{ctx.strokeStyle=col;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();const a=Math.atan2(y2-y1,x2-x1);ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-9*Math.cos(a-.4),y2-9*Math.sin(a-.4));ctx.lineTo(x2-9*Math.cos(a+.4),y2-9*Math.sin(a+.4));ctx.closePath();ctx.fill();}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  const mx=W-60,mf=W/2-20;
  ctx.strokeStyle='rgba(200,220,255,0.7)';ctx.lineWidth=3;
  ctx.beginPath();ctx.arc(mx+160,cy,180,Math.PI*.65,Math.PI*1.35);ctx.stroke();
  ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(mf,0);ctx.lineTo(mf,H);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='rgba(255,200,100,0.6)';ctx.beginPath();ctx.arc(mf,cy,5,0,6.28);ctx.fill();
  ctx.fillStyle='rgba(255,200,100,0.7)';ctx.font='8px monospace';ctx.fillText('F (Focus)',mf-8,cy+16);
  const numRays=5;
  for(let i=0;i<numRays;i++){{
    const oy=cy-70+i*35;
    const mx2=W-80;
    arrow(20,oy,mx2,oy,'rgba(255,220,80,0.8)');
    const dx=mx2-mf,dy=oy-cy;
    const ang=Math.atan2(dy,dx);
    const refAng=Math.atan2(-dy,dx-30)+0.1;
    const rx=mf+100*Math.cos(refAng),ry=cy+100*Math.sin(refAng);
    arrow(mx2,oy,rx,ry,'rgba(255,140,50,0.75)');
  }}
  ctx.fillStyle='rgba(255,255,255,0.35)';ctx.font='8px monospace';
  ctx.fillText('Parallel rays → converge at focus',10,H-6);
  ctx.fillStyle='rgba(200,220,255,0.6)';ctx.fillText('Mirror',W-58,cy);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'lungs':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🫁 RESPIRATORY SYSTEM — HOW BREATHING WORKS</div>
<canvas id="lg" width="340" height="260" style="display:block;"></canvas>
<div style="display:flex;gap:14px;font-size:10px;margin-top:4px;flex-wrap:wrap;justify-content:center;">
  <span style="color:#4fc3f7">↑ Inhalation</span><span style="color:#ef9a9a">↓ Exhalation</span>
</div>
<script>
const cv=document.getElementById('lg'),ctx=cv.getContext('2d'),W=340,H=260;
let t=0;
function drawLung(cx,cy,phase,side){{
  const sc=0.85+0.12*Math.sin(phase);
  ctx.save();ctx.translate(cx,cy);ctx.scale(sc,sc);
  ctx.fillStyle='rgba(240,100,100,0.35)';ctx.strokeStyle='#ef9a9a';ctx.lineWidth=2;
  ctx.beginPath();
  if(side==='l'){{ctx.moveTo(0,-55);ctx.bezierCurveTo(-50,-55,-70,0,-50,50);ctx.bezierCurveTo(-30,70,0,60,0,50);ctx.lineTo(0,-55);}}
  else{{ctx.moveTo(0,-55);ctx.bezierCurveTo(50,-55,70,0,50,50);ctx.bezierCurveTo(30,70,0,60,0,50);ctx.lineTo(0,-55);}}
  ctx.fill();ctx.stroke();
  for(let i=0;i<4;i++){{const bx=(side==='l'?-1:1)*(15+i*8),by=-30+i*18;ctx.beginPath();ctx.ellipse(bx,by,5,8,0,0,6.28);ctx.fillStyle='rgba(255,180,180,0.5)';ctx.fill();ctx.strokeStyle='rgba(255,150,150,0.6)';ctx.lineWidth=1;ctx.stroke();}}
  ctx.restore();
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  const phase=t*0.04;
  ctx.strokeStyle='rgba(200,220,255,0.7)';ctx.lineWidth=4;
  ctx.beginPath();ctx.moveTo(W/2,20);ctx.lineTo(W/2,90);ctx.stroke();
  ctx.beginPath();ctx.moveTo(W/2,90);ctx.bezierCurveTo(W/2-40,90,W/2-80,100,W/2-80,120);ctx.stroke();
  ctx.beginPath();ctx.moveTo(W/2,90);ctx.bezierCurveTo(W/2+40,90,W/2+80,100,W/2+80,120);ctx.stroke();
  ctx.fillStyle='rgba(200,220,255,0.5)';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText('Trachea',W/2+12,60);
  drawLung(W/2-80,150,phase,'l');
  drawLung(W/2+80,150,phase,'r');
  const breathIn=Math.sin(phase)>0;
  ctx.fillStyle=breathIn?'rgba(100,200,255,0.9)':'rgba(255,150,150,0.9)';
  ctx.textAlign='center';ctx.font='bold 10px monospace';
  ctx.fillText(breathIn?'↓ INHALING (diaphragm contracts)':'↑ EXHALING (diaphragm relaxes)',W/2,H-10);
  ctx.fillStyle='rgba(255,255,255,0.35)';ctx.font='8px monospace';
  ctx.fillText('Alveoli (tiny air sacs) shown as ellipses',W/2,H-25);
  const airY=20+30*Math.abs(Math.sin(phase));const airOp=0.4+0.4*Math.abs(Math.sin(phase));
  ctx.strokeStyle='rgba(100,220,255,'+airOp.toFixed(2)+')';ctx.lineWidth=1.5;ctx.setLineDash([3,3]);
  ctx.beginPath();ctx.moveTo(W/2,airY);ctx.lineTo(W/2,20);ctx.stroke();ctx.setLineDash([]);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'digestion':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🍎 DIGESTIVE SYSTEM</div>
<canvas id="dg" width="340" height="280" style="display:block;"></canvas>
<script>
const cv=document.getElementById('dg'),ctx=cv.getContext('2d'),W=340,H=280;
let t=0;
const organs=[
  {{x:170,y:30,label:'Mouth',r:20,col:'#ffb74d'}},
  {{x:170,y:68,label:'Oesophagus',r:0,col:'#ff8a65',pipe:true,y2:95}},
  {{x:170,y:105,label:'Stomach',rx:40,ry:28,col:'#ef5350'}},
  {{x:170,y:155,label:'Small Intestine',col:'#a5d6a7',coil:true}},
  {{x:170,y:230,label:'Large Intestine',col:'#66bb6a',thick:true}},
  {{x:170,y:268,label:'Rectum/Anus',r:10,col:'#8d6e63'}},
];
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,150,100,0.7)';ctx.lineWidth=3;
  ctx.beginPath();ctx.moveTo(170,50);ctx.lineTo(170,68);ctx.lineTo(170,95);ctx.stroke();
  ctx.beginPath();ctx.moveTo(150,133);ctx.bezierCurveTo(100,155,100,200,130,230);ctx.bezierCurveTo(140,240,180,240,185,235);ctx.stroke();
  ctx.fillStyle='rgba(239,83,80,0.3)';ctx.strokeStyle='#ef5350';ctx.lineWidth=2.5;
  ctx.beginPath();ctx.ellipse(170,105,40,28,0,0,6.28);ctx.fill();ctx.stroke();
  ctx.strokeStyle='rgba(165,214,167,0.8)';ctx.lineWidth=5;
  for(let i=0;i<6;i++){{const cy=148+i*12,off=i%2===0?20:-20;ctx.beginPath();ctx.bezierCurveTo(130+off,cy,210-off,cy,130-off,cy+12);ctx.stroke();}}
  ctx.strokeStyle='rgba(102,187,106,0.7)';ctx.lineWidth=8;
  ctx.beginPath();ctx.arc(170,225,40,Math.PI*.2,Math.PI*1.8);ctx.stroke();
  ctx.fillStyle='rgba(141,110,99,0.5)';ctx.strokeStyle='#8d6e63';ctx.lineWidth=2;
  ctx.beginPath();ctx.ellipse(170,268,10,10,0,0,6.28);ctx.fill();ctx.stroke();
  ctx.fillStyle='rgba(255,200,80,0.7)';ctx.beginPath();ctx.arc(170,30,14,0,6.28);ctx.fill();
  ctx.strokeStyle='#ffb74d';ctx.lineWidth=2;ctx.stroke();
  const fp=((t*.008)%1);
  const foodPath=[[170,44],[170,95],[170,133],[170,148],[170,230],[170,268]];
  const seg=Math.floor(fp*5);const lp=(fp*5)%1;
  if(seg<5){{const p0=foodPath[seg],p1=foodPath[seg+1];const fx=p0[0]+(p1[0]-p0[0])*lp,fy=p0[1]+(p1[1]-p0[1])*lp;ctx.beginPath();ctx.arc(fx,fy,6,0,6.28);ctx.fillStyle='rgba(255,220,50,0.9)';ctx.fill();}}
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='8px monospace';ctx.textAlign='right';
  ctx.fillText('Mouth',158,33);ctx.fillText('Oesophagus',155,82);ctx.fillText('Stomach',124,108);
  ctx.fillText('Small',125,155);ctx.fillText('Intestine',125,165);
  ctx.fillText('Large Int.',128,230);ctx.fillText('Rectum',152,270);
  ctx.textAlign='left';ctx.fillStyle='rgba(255,220,50,0.8)';ctx.fillText('● Food particle',W-120,H-8);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'neuron':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🧠 NEURON — NERVE CELL STRUCTURE</div>
<canvas id="nr" width="360" height="200" style="display:block;"></canvas>
<div style="font-size:10px;color:#8aa;margin-top:4px;text-align:center;">Nerve impulse travels from dendrites → cell body → axon → synapse</div>
<script>
const cv=document.getElementById('nr'),ctx=cv.getContext('2d'),W=360,H=200;
let t=0,pulse=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const cx=90,cy=H/2;
  ctx.fillStyle='rgba(168,85,247,0.3)';ctx.strokeStyle='#a855f7';ctx.lineWidth=2;
  ctx.beginPath();ctx.arc(cx,cy,28,0,6.28);ctx.fill();ctx.stroke();
  ctx.fillStyle='#d0a0ff';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText('Cell',cx,cy-2);ctx.fillText('Body',cx,cy+8);
  const dend=[[cx-30,cy-35,cx-8,cy-10],[cx-45,cy,cx-28,cy],[cx-30,cy+35,cx-8,cy+10]];
  dend.forEach(([x1,y1,x2,y2])=>{{ctx.strokeStyle='rgba(168,85,247,0.7)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x2,y2);ctx.bezierCurveTo((x1+x2)/2,y2,x1,(y1+y2)/2,x1,y1);ctx.stroke();}});
  ctx.fillStyle='rgba(168,85,247,0.8)';ctx.font='8px monospace';ctx.fillText('Dendrites',cx-48,cy-45);
  ctx.strokeStyle='rgba(100,200,255,0.7)';ctx.lineWidth=6;
  ctx.beginPath();ctx.moveTo(cx+28,cy);ctx.lineTo(W-60,cy);ctx.stroke();
  ctx.fillStyle='rgba(100,200,255,0.7)';ctx.font='8px monospace';ctx.fillText('Axon',W/2,cy-12);
  const myelin=8;
  for(let i=0;i<myelin;i++){{const x=cx+30+i*(W-120-cx)/myelin;ctx.fillStyle='rgba(255,200,100,0.5)';ctx.beginPath();ctx.ellipse(x+20,cy,16,10,0,0,6.28);ctx.fill();}}
  ctx.fillStyle='rgba(255,200,100,0.7)';ctx.fillText('Myelin sheaths',cx+40,cy+24);
  const termX=W-60;ctx.fillStyle='rgba(100,220,100,0.35)';ctx.strokeStyle='#4caf50';ctx.lineWidth=2;
  ctx.beginPath();ctx.ellipse(termX,cy,18,28,0,0,6.28);ctx.fill();ctx.stroke();
  ctx.fillStyle='#a5d6a7';ctx.fillText('Synapse',termX-16,cy-32);
  pulse=(pulse+0.025)%1;
  const px=cx+28+(W-88-cx)*pulse;const pop=Math.sin(pulse*Math.PI);
  ctx.beginPath();ctx.arc(px,cy,5+3*pop,0,6.28);ctx.fillStyle='rgba(255,255,100,'+(0.6+0.4*pop).toFixed(2)+')';ctx.fill();
  ctx.fillStyle='rgba(255,255,100,0.7)';ctx.fillText('↑ Impulse',px-14,cy-14);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'plant_structure':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🌱 PARTS OF A PLANT</div>
<svg viewBox="0 0 360 280" width="340" height="265" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="200" width="360" height="80" fill="#1a2a0a" rx="2"/>
  <line x1="180" y1="50" x2="180" y2="205" stroke="#5a8a20" stroke-width="6"/>
  <ellipse cx="130" cy="130" rx="40" ry="24" fill="rgba(60,160,40,0.7)" stroke="#4a9a28" stroke-width="1.5" transform="rotate(-20,130,130)"/>
  <ellipse cx="230" cy="100" rx="40" ry="24" fill="rgba(60,160,40,0.7)" stroke="#4a9a28" stroke-width="1.5" transform="rotate(20,230,100)"/>
  <ellipse cx="155" cy="170" rx="32" ry="18" fill="rgba(60,160,40,0.6)" stroke="#4a9a28" stroke-width="1.5" transform="rotate(-10,155,170)"/>
  <ellipse cx="205" cy="155" rx="32" ry="18" fill="rgba(60,160,40,0.6)" stroke="#4a9a28" stroke-width="1.5" transform="rotate(10,205,155)"/>
  <circle cx="180" cy="52" r="28" fill="rgba(255,180,200,0.6)" stroke="#ff8aaa" stroke-width="2">
    <animate attributeName="r" values="28;32;28" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="180" y="56" text-anchor="middle" fill="#ffb8cc" font-size="9" font-family="monospace">Flower</text>
  <line x1="120" y1="200" x2="80" y2="260" stroke="#8b5a1a" stroke-width="3"/>
  <line x1="150" y1="200" x2="120" y2="270" stroke="#8b5a1a" stroke-width="3"/>
  <line x1="180" y1="205" x2="180" y2="275" stroke="#8b5a1a" stroke-width="4"/>
  <line x1="210" y1="200" x2="240" y2="270" stroke="#8b5a1a" stroke-width="3"/>
  <line x1="240" y1="200" x2="280" y2="260" stroke="#8b5a1a" stroke-width="3"/>
  <circle cx="82" cy="262" r="6" fill="#a0720a" opacity="0.7"/>
  <circle cx="122" cy="272" r="5" fill="#a0720a" opacity="0.7"/>
  <circle cx="180" cy="277" r="7" fill="#a0720a" opacity="0.7"/>
  <circle cx="238" cy="272" r="5" fill="#a0720a" opacity="0.7"/>
  <circle cx="278" cy="262" r="6" fill="#a0720a" opacity="0.7"/>
  <text x="12" y="56" fill="#ffb8cc" font-size="9" font-family="monospace">← Flower</text>
  <text x="12" y="110" fill="#aaddaa" font-size="9" font-family="monospace">← Leaf</text>
  <text x="294" y="175" fill="#88cc88" font-size="9" font-family="monospace">Leaf →</text>
  <text x="195" y="160" fill="#8bc34a" font-size="9" font-family="monospace">Stem →</text>
  <text x="260" y="230" fill="#8ba050" font-size="9" font-family="monospace">Root →</text>
  <text x="12" y="248" fill="#a08030" font-size="9" font-family="monospace">Root hair →</text>
  <text x="60" y="278" fill="#888" font-size="8" font-family="monospace">Soil (absorbs water and minerals)</text>
  <line x1="180" y1="205" x2="180" y2="205"><animate attributeName="stroke-dashoffset" values="0;-20" dur="1s" repeatCount="indefinite"/></line>
</svg></body></html>"""

    elif topic == 'food_chain':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🦁 FOOD CHAIN — ENERGY FLOW</div>
<canvas id="fc" width="360" height="220" style="display:block;"></canvas>
<script>
const cv=document.getElementById('fc'),ctx=cv.getContext('2d'),W=360,H=220;
let t=0;
const levels=[
  {{x:50,y:H/2,label:'☀ Sun',sub:'Energy source',col:'#ffd700',r:28}},
  {{x:130,y:H/2,label:'🌿 Grass',sub:'Producer',col:'#4caf50',r:26}},
  {{x:215,y:H/2,label:'🐇 Rabbit',sub:'Primary Consumer',col:'#90caf9',r:26}},
  {{x:300,y:H/2,label:'🦊 Fox',sub:'Secondary Consumer',col:'#ff8a65',r:26}},
];
function draw(){{
  ctx.clearRect(0,0,W,H);
  for(let i=0;i<levels.length-1;i++){{
    const a=levels[i],b=levels[i+1];
    const pulse=0.5+0.5*Math.sin(t*0.08+i);
    ctx.strokeStyle='rgba(255,220,50,'+(0.4+0.4*pulse).toFixed(2)+')';ctx.lineWidth=2+2*pulse;
    ctx.beginPath();ctx.moveTo(a.x+a.r,a.y);ctx.lineTo(b.x-b.r,b.y);ctx.stroke();
    const ax=a.x+a.r+(b.x-b.r-a.x-a.r)*((t*0.015+i*.33)%1);
    const ay=a.y;
    ctx.beginPath();ctx.arc(ax,ay,4,0,6.28);ctx.fillStyle='rgba(255,230,80,0.9)';ctx.fill();
    ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='7px monospace';ctx.textAlign='center';ctx.fillText('Energy',ax,ay-10);
  }}
  levels.forEach((l,i)=>{{
    const glow=0.8+0.15*Math.sin(t*0.06+i);
    ctx.beginPath();ctx.arc(l.x,l.y,l.r*glow,0,6.28);
    ctx.fillStyle=l.col+'33';ctx.fill();ctx.strokeStyle=l.col;ctx.lineWidth=2;ctx.stroke();
    ctx.fillStyle='#fff';ctx.font='bold 14px monospace';ctx.textAlign='center';ctx.fillText(l.label.split(' ')[0],l.x,l.y+5);
    ctx.fillStyle=l.col;ctx.font='8px monospace';ctx.fillText(l.label.split(' ')[1]||'',l.x,l.y+18);
    ctx.fillStyle='rgba(255,255,255,0.45)';ctx.font='7px monospace';ctx.fillText(l.sub,l.x,l.y+l.r+14);
  }});
  ctx.textAlign='left';ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';
  ctx.fillText('Energy decreases by ~90% at each trophic level',10,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'projectile':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🏀 PROJECTILE MOTION</div>
<canvas id="pj" width="360" height="220" style="display:block;"></canvas>
<div style="font-size:10px;color:#8aa;margin-top:4px;text-align:center;">Horizontal velocity: constant | Vertical velocity: changes due to gravity</div>
<script>
const cv=document.getElementById('pj'),ctx=cv.getContext('2d'),W=360,H=220;
let t=0;
const v0=5,ang=Math.PI/4,g=0.15;
const vx=v0*Math.cos(ang),vy0=-v0*Math.sin(ang);
const trail=[];
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=1;
  for(let y=0;y<H;y+=40){{ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}}
  ctx.strokeStyle='rgba(255,255,255,0.15)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,H-30);ctx.lineTo(W,H-30);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';ctx.fillText('Ground',6,H-16);
  const bx=30+vx*t,by=H-30+vy0*t+0.5*g*t*t;
  trail.push({{x:bx,y:by}});if(trail.length>80)trail.shift();
  trail.forEach((p,i)=>{{ctx.beginPath();ctx.arc(p.x,p.y,2,0,6.28);ctx.fillStyle='rgba(255,200,50,'+(i/trail.length*0.7).toFixed(2)+')';ctx.fill();}});
  if(by>H-30){{t=0;trail.length=0;}} else{{
    ctx.beginPath();ctx.arc(bx,by,10,0,6.28);ctx.fillStyle='#ef5350';ctx.fill();ctx.strokeStyle='#ff8a80';ctx.lineWidth=2;ctx.stroke();
    const vy=vy0+g*t;
    ctx.strokeStyle='rgba(100,200,255,0.8)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bx+vx*8,by);ctx.stroke();
    ctx.strokeStyle='rgba(255,150,50,0.8)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bx,by+vy*8);ctx.stroke();
    ctx.fillStyle='rgba(100,200,255,0.8)';ctx.font='7px monospace';ctx.fillText('Vx',bx+vx*8+3,by+3);
    ctx.fillStyle='rgba(255,150,50,0.8)';ctx.fillText('Vy',bx+3,by+vy*8+10);
  }}
  t+=1;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'circular_motion':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">⭕ CIRCULAR MOTION — CENTRIPETAL FORCE</div>
<canvas id="cm" width="340" height="240" style="display:block;"></canvas>
<div style="font-size:10px;color:#8aa;margin-top:4px;text-align:center;">Centripetal force always points toward the center</div>
<script>
const cv=document.getElementById('cm'),ctx=cv.getContext('2d'),W=340,H=240,cx=W/2,cy=H/2,r=90;
let t=0;
function arrow(x1,y1,x2,y2,col){{ctx.strokeStyle=col;ctx.lineWidth=2.5;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();const a=Math.atan2(y2-y1,x2-x1);ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-10*Math.cos(a-.4),y2-10*Math.sin(a-.4));ctx.lineTo(x2-10*Math.cos(a+.4),y2-10*Math.sin(a+.4));ctx.closePath();ctx.fill();}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.12)';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.arc(cx,cy,r,0,6.28);ctx.stroke();ctx.setLineDash([]);
  ctx.strokeStyle='rgba(255,255,255,0.08)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(cx-r-20,cy);ctx.lineTo(cx+r+20,cy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx,cy-r-20);ctx.lineTo(cx,cy+r+20);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,0.4)';ctx.beginPath();ctx.arc(cx,cy,5,0,6.28);ctx.fill();
  ctx.fillStyle='rgba(255,255,255,0.35)';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText('Center',cx,cy+18);
  const bx=cx+r*Math.cos(t),by=cy+r*Math.sin(t);
  const vx=-Math.sin(t)*30,vy=Math.cos(t)*30;
  const fx=cx-bx,fy=cy-by;const fm=Math.sqrt(fx*fx+fy*fy);
  arrow(bx,by,bx+(fx/fm)*40,by+(fy/fm)*40,'#ef5350');
  arrow(bx,by,bx+vx,by+vy,'#00e5ff');
  ctx.beginPath();ctx.arc(bx,by,14,0,6.28);ctx.fillStyle='rgba(100,150,255,0.8)';ctx.fill();ctx.strokeStyle='#7ab4ff';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='#fff';ctx.font='7px monospace';ctx.textAlign='center';ctx.fillText('m',bx,by+3);
  ctx.fillStyle='#ef5350';ctx.font='8px monospace';ctx.fillText('Fc (centripetal)',bx+(fx/fm)*42+5,by+(fy/fm)*42);
  ctx.fillStyle='#00e5ff';ctx.fillText('v (velocity)',bx+vx+5,by+vy-5);
  ctx.strokeStyle='rgba(255,220,50,0.3)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(bx,by);ctx.stroke();
  ctx.fillStyle='rgba(255,220,50,0.5)';ctx.fillText('r',cx+(bx-cx)/2-8,cy+(by-cy)/2);
  t+=0.035;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'volcano':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🌋 VOLCANIC ERUPTION</div>
<canvas id="vl" width="460" height="310" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">Magma rises through vent · Lava, ash and gases erupt at the surface</div>
<script>
const cv=document.getElementById('vl'),ctx=cv.getContext('2d'),W=460,H=310;
const vx=230,vtop=H*.3;
const particles=[];
for(let i=0;i<35;i++)particles.push([0,0,0,0,0,0,0]);
function resetP(p){{p[0]=vx+(Math.random()-.5)*8;p[1]=vtop;p[2]=(Math.random()-.5)*5;p[3]=-(4+Math.random()*6);p[4]=0;p[5]=50+Math.random()*55;p[6]=3+Math.random()*5;}}
particles.forEach(resetP);
const lavaBombs=[];
for(let i=0;i<6;i++)lavaBombs.push([vx,vtop,(Math.random()-.5)*3.5,-(5+Math.random()*4),0,30+Math.random()*40,0]);
lavaBombs.forEach(function(b){{b[4]=Math.random()*b[5];}});
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const sky=ctx.createLinearGradient(0,0,0,H);
  sky.addColorStop(0,'#010208');sky.addColorStop(.45,'#1a0805');sky.addColorStop(1,'#0a1208');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  const grdG=ctx.createLinearGradient(0,H*.62,0,H);
  grdG.addColorStop(0,'#1a1006');grdG.addColorStop(1,'#0d0a04');
  ctx.fillStyle=grdG;ctx.fillRect(0,H*.62,W,H);
  const vg=ctx.createLinearGradient(vx-90,H,vx,vtop);
  vg.addColorStop(0,'#1a1208');vg.addColorStop(.5,'#2a2010');vg.addColorStop(1,'#3a2a18');
  ctx.fillStyle=vg;ctx.beginPath();ctx.moveTo(vx-130,H*.95);ctx.lineTo(vx-90,H*.62);ctx.lineTo(vx-30,H*.38);ctx.lineTo(vx,vtop);ctx.lineTo(vx+30,H*.38);ctx.lineTo(vx+90,H*.62);ctx.lineTo(vx+130,H*.95);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(90,70,40,.5)';ctx.lineWidth=1.5;ctx.stroke();
  const lavaFlow=ctx.createLinearGradient(vx-30,H*.38,vx-80,H*.7);
  lavaFlow.addColorStop(0,'rgba(255,80,0,.55)');lavaFlow.addColorStop(1,'rgba(200,40,0,.2)');
  ctx.fillStyle=lavaFlow;ctx.beginPath();ctx.moveTo(vx-30,H*.38);ctx.bezierCurveTo(vx-45,H*.5,vx-60,H*.58,vx-80,H*.7);ctx.lineTo(vx-65,H*.72);ctx.bezierCurveTo(vx-45,H*.62,vx-32,H*.52,vx-20,H*.4);ctx.closePath();ctx.fill();
  const lavaFlow2=ctx.createLinearGradient(vx+30,H*.38,vx+85,H*.72);
  lavaFlow2.addColorStop(0,'rgba(255,80,0,.5)');lavaFlow2.addColorStop(1,'rgba(200,40,0,.18)');
  ctx.fillStyle=lavaFlow2;ctx.beginPath();ctx.moveTo(vx+30,H*.38);ctx.bezierCurveTo(vx+45,H*.5,vx+65,H*.6,vx+85,H*.72);ctx.lineTo(vx+70,H*.74);ctx.bezierCurveTo(vx+52,H*.62,vx+32,H*.52,vx+18,H*.4);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(255,120,0,.4)';ctx.lineWidth=3;
  ctx.beginPath();ctx.moveTo(vx,H*.88);ctx.lineTo(vx,vtop);ctx.stroke();
  const magG=ctx.createRadialGradient(vx,H*.88,5,vx,H*.88,55);
  magG.addColorStop(0,'rgba(255,100,0,.6)');magG.addColorStop(.5,'rgba(200,40,0,.35)');magG.addColorStop(1,'rgba(150,20,0,.1)');
  ctx.beginPath();ctx.ellipse(vx,H*.88,70,30,0,0,6.28);ctx.fillStyle=magG;ctx.fill();
  ctx.fillStyle='rgba(255,140,0,.7)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('MAGMA CHAMBER',vx,H*.88+4);
  particles.forEach(function(p){{
    p[2]+=(Math.random()-.5)*.15;p[3]+=.14;p[4]++;
    if(p[4]>p[5])resetP(p);
    const op=(1-p[4]/p[5]);
    const t2=p[4]/p[5];
    const g2=Math.floor(160*(1-t2));
    ctx.beginPath();ctx.arc(p[0]+p[2]*(p[4]*.1),p[1]+p[3]*p[4]+.5*.14*p[4]*p[4],p[6]*(1-t2*.5),0,6.28);
    ctx.fillStyle='rgba(255,'+g2+',0,'+(op*.9).toFixed(2)+')';ctx.fill();
  }});
  lavaBombs.forEach(function(b){{
    b[4]+=1;if(b[4]>b[5]){{b[0]=vx+(Math.random()-.5)*8;b[1]=vtop;b[2]=(Math.random()-.5)*3.5;b[3]=-(5+Math.random()*4);b[4]=0;b[5]=30+Math.random()*40;b[6]=0;}}
    const bx2=b[0]+b[2]*b[4],by2=b[1]+b[3]*b[4]+.5*.15*b[4]*b[4];
    if(by2<H){{
      ctx.beginPath();ctx.arc(bx2,by2,4,0,6.28);
      ctx.fillStyle='rgba(255,200,50,.9)';ctx.fill();
      ctx.beginPath();ctx.arc(bx2,by2,7,0,6.28);
      ctx.fillStyle='rgba(255,80,0,.35)';ctx.fill();
    }}
  }});
  for(let ac=0;ac<5;ac++){{
    const ax=vx+(-30+ac*15)+10*Math.sin(t*.04+ac),ay=vtop-20-ac*18-8*Math.sin(t*.05+ac*1.2);
    const ar=18+ac*10+5*Math.sin(t*.06+ac);
    const aal=(0.25-ac*.04).toFixed(2);
    if(aal>0){{ctx.beginPath();ctx.arc(ax,ay,ar,0,6.28);ctx.fillStyle='rgba(80,70,65,'+aal+')';ctx.fill();}}
  }}
  ctx.fillStyle='rgba(255,100,0,.6)';ctx.font='bold 7px sans-serif';ctx.textAlign='left';ctx.fillText('Lava flow',10,H*.52);
  ctx.fillStyle='rgba(180,160,140,.55)';ctx.fillText('↑ Ash cloud',vx-18,vtop-60);
  ctx.fillStyle='rgba(255,255,255,.22)';ctx.font='7px monospace';ctx.textAlign='center';
  ctx.fillText('Magma rises through the vent and erupts as lava, ash, and volcanic gases',W/2,H-5);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'earthquake':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🌍 EARTHQUAKE — SEISMIC WAVES</div>
<canvas id="eq" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('eq'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const gh=H*.55,ex=W/2,ey=gh+40;
  const gg=ctx.createLinearGradient(0,gh,0,H);gg.addColorStop(0,'#1a2510');gg.addColorStop(1,'#0a1508');
  ctx.fillStyle=gg;ctx.fillRect(0,gh,W,H);
  const sg=ctx.createLinearGradient(0,gh+10,0,H);sg.addColorStop(0,'#2a3520');sg.addColorStop(1,'#0d1a08');
  ctx.fillStyle=sg;ctx.fillRect(0,gh+10,W,H);
  const shakeAmt=3*Math.sin(t*.3);
  for(let i=0;i<W;i+=20){{ctx.strokeStyle='rgba(100,130,70,0.3)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(i,gh);ctx.lineTo(i,H);ctx.stroke();}}
  ctx.fillStyle='#0a1220';ctx.fillRect(0,0,W,gh);
  ctx.fillStyle='rgba(255,255,255,0.1)';ctx.font='8px monospace';ctx.textAlign='center';
  ctx.fillText('Surface',W/2,gh-5);
  ctx.fillStyle='rgba(255,100,50,0.85)';ctx.beginPath();ctx.arc(ex,ey+shakeAmt,10,0,6.28);ctx.fill();
  ctx.fillStyle='rgba(255,100,50,0.7)';ctx.fillText('Hypocentre',ex,ey+30);
  ctx.fillStyle='rgba(255,150,80,0.7)';ctx.beginPath();ctx.arc(ex,gh+shakeAmt/2,8,0,6.28);ctx.fill();
  ctx.fillStyle='rgba(255,150,80,0.7)';ctx.fillText('Epicentre',ex+40,gh+14);
  ctx.strokeStyle='rgba(255,100,50,0.3)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex,gh);ctx.stroke();
  const numWaves=5;
  for(let i=1;i<=numWaves;i++){{
    const r=(t*2+i*30)%Math.max(W,H);const op=Math.max(0,1-r/Math.max(W,H));
    ctx.strokeStyle='rgba(255,150,50,'+(op*.6).toFixed(2)+')';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.arc(ex,ey,r,Math.PI,2*Math.PI);ctx.stroke();
    ctx.strokeStyle='rgba(100,180,255,'+(op*.5).toFixed(2)+')';ctx.lineWidth=1;
    ctx.beginPath();ctx.arc(ex,gh,r*.8,0,2*Math.PI);ctx.stroke();
  }}
  ctx.fillStyle='rgba(255,150,50,0.6)';ctx.fillText('P-waves (body waves) →',W/2-60,H/3);
  ctx.fillStyle='rgba(100,180,255,0.6)';ctx.fillText('S-waves (surface) →',W/2-50,gh-20);
  ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';ctx.fillText('Seismic waves radiate from the hypocentre',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'rock_cycle':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🪨 ROCK CYCLE</div>
<canvas id="rc" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('rc'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
const rocks=[
  {{x:180,y:30,label:'Igneous Rock',sub:'(formed from magma)',col:'#ef5350'}},
  {{x:50,y:180,label:'Sedimentary',sub:'(layers of sediment)',col:'#ffb74d'}},
  {{x:310,y:180,label:'Metamorphic',sub:'(heat & pressure)',col:'#a855f7'}},
];
const arrows=[
  {{from:0,to:1,label:'Weathering &\nErosion',col:'#90caf9',cp:[60,90]}},
  {{from:1,to:2,label:'Heat &\nPressure',col:'#ef9a9a',cp:[180,200]}},
  {{from:2,to:0,label:'Melting',col:'#ff8a65',cp:[320,80]}},
  {{from:0,to:2,label:'Cooling',col:'#80cbc4',cp:[300,80]}},
];
function bezierPt(p0,p1,cp,tt){{return{{x:p0.x*(1-tt)*(1-tt)+2*cp[0]*tt*(1-tt)+p1.x*tt*tt,y:p0.y*(1-tt)*(1-tt)+2*cp[1]*tt*(1-tt)+p1.y*tt*tt}};}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  arrows.forEach((a,i)=>{{
    const r0=rocks[a.from],r1=rocks[a.to];
    const pulse=((t*.008+i*.25)%1);
    ctx.strokeStyle=a.col;ctx.lineWidth=1.5;ctx.setLineDash([5,5]);
    ctx.beginPath();ctx.moveTo(r0.x,r0.y+20);ctx.quadraticCurveTo(a.cp[0],a.cp[1],r1.x,r1.y-20);ctx.stroke();ctx.setLineDash([]);
    const pt=bezierPt({{x:r0.x,y:r0.y+20}},{{x:r1.x,y:r1.y-20}},a.cp,pulse);
    ctx.beginPath();ctx.arc(pt.x,pt.y,5,0,6.28);ctx.fillStyle=a.col;ctx.fill();
    ctx.fillStyle=a.col;ctx.font='7px monospace';ctx.textAlign='center';
    ctx.fillText(a.label.split('\n')[0],(r0.x+r1.x)/2+5,(r0.y+r1.y)/2-5);
    if(a.label.includes('\n'))ctx.fillText(a.label.split('\n')[1],(r0.x+r1.x)/2+5,(r0.y+r1.y)/2+5);
  }});
  rocks.forEach((r,i)=>{{
    const glow=0.9+0.1*Math.sin(t*.05+i*2);
    ctx.beginPath();ctx.roundRect(r.x-48,r.y-16,96,34,6);
    ctx.fillStyle=r.col+'33';ctx.fill();ctx.strokeStyle=r.col;ctx.lineWidth=2;ctx.stroke();
    ctx.fillStyle=r.col;ctx.font='bold 9px monospace';ctx.textAlign='center';ctx.fillText(r.label,r.x,r.y);
    ctx.fillStyle='rgba(255,255,255,0.45)';ctx.font='7px monospace';ctx.fillText(r.sub,r.x,r.y+13);
  }});
  ctx.fillStyle='rgba(255,80,0,0.6)';ctx.beginPath();ctx.ellipse(180,H-15,60,14,0,0,6.28);ctx.fill();
  ctx.fillStyle='rgba(255,150,50,0.8)';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText('🌋 Magma / Lava',180,H-11);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'greenhouse':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🌡 GREENHOUSE EFFECT</div>
<canvas id="gh" width="460" height="305" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">CO₂ traps infrared radiation → Earth's temperature rises</div>
<script>
const cv=document.getElementById('gh'),ctx=cv.getContext('2d'),W=460,H=305;
const rays=[];
for(let i=0;i<14;i++)rays.push([W*.78,22,50+Math.random()*330,H*.72,Math.random(),Math.random()>.45]);
const co2Mols=[];
for(let i=0;i<8;i++)co2Mols.push([30+Math.random()*W*.85,H*.14+Math.random()*H*.58,Math.random()*.3-.15,Math.random()*.15-.075]);
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const sky=ctx.createLinearGradient(0,0,0,H);
  sky.addColorStop(0,'#010208');sky.addColorStop(.38,'#06111e');sky.addColorStop(.74,'#071a0a');sky.addColorStop(1,'#050e06');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  ctx.fillStyle='rgba(20,60,180,.1)';ctx.fillRect(0,H*.12,W,H*.62);
  ctx.strokeStyle='rgba(40,120,255,.22)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(0,H*.12);ctx.lineTo(W,H*.12);ctx.stroke();
  ctx.beginPath();ctx.moveTo(0,H*.74);ctx.lineTo(W,H*.74);ctx.stroke();
  ctx.fillStyle='rgba(40,130,255,.25)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';
  ctx.fillText('ATMOSPHERE  (CO₂ · CH₄ · N₂O · H₂O)',W/2,H*.1);
  const sx=W*.78,sy=24;
  const sunG=ctx.createRadialGradient(sx,sy,2,sx,sy,24);
  sunG.addColorStop(0,'#fffde7');sunG.addColorStop(.45,'#ffa000');sunG.addColorStop(1,'rgba(230,80,0,0)');
  ctx.shadowColor='#ff8800';ctx.shadowBlur=18;
  ctx.beginPath();ctx.arc(sx,sy,22*(1+.04*Math.sin(t*.04)),0,6.28);ctx.fillStyle=sunG;ctx.fill();
  ctx.shadowBlur=0;
  ctx.fillStyle='rgba(255,210,60,.7)';ctx.font='bold 7px sans-serif';ctx.fillText('☀ SUN',sx,sy+34);
  rays.forEach(function(r){{
    r[4]+=0.016;if(r[4]>1){{r[4]=0;r[5]=Math.random()>.45;}}
    const px=r[0]+(r[2]-r[0])*Math.min(r[4],1),py=r[1]+(r[3]-r[1])*Math.min(r[4],1);
    if(!r[5]||r[4]<0.5){{
      ctx.strokeStyle='rgba(255,220,50,.65)';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(r[0],r[1]);ctx.lineTo(px,py);ctx.stroke();
    }} else {{
      ctx.strokeStyle='rgba(255,80,30,.6)';ctx.lineWidth=1.5;
      if(r[4]<0.78){{ctx.beginPath();ctx.moveTo(r[2],r[3]);ctx.lineTo(r[2]+(r[2]-W*.4)*(r[4]-.5)*4,py-22*(r[4]-.5)*4);ctx.stroke();}}
      else{{ctx.beginPath();ctx.moveTo(r[2],r[3]-25);ctx.lineTo(r[2],r[3]+12);ctx.stroke();}}
    }}
  }});
  co2Mols.forEach(function(c){{
    c[0]+=c[2];c[1]+=c[3];
    if(c[0]<5||c[0]>W-5)c[2]*=-1;
    if(c[1]<H*.14||c[1]>H*.74)c[3]*=-1;
    ctx.shadowColor='#44aaff';ctx.shadowBlur=6;
    ctx.beginPath();ctx.arc(c[0],c[1],5,0,6.28);ctx.fillStyle='rgba(80,180,255,.5)';ctx.fill();
    ctx.beginPath();ctx.arc(c[0]-9,c[1],3.5,0,6.28);ctx.fillStyle='rgba(60,150,255,.4)';ctx.fill();
    ctx.beginPath();ctx.arc(c[0]+9,c[1],3.5,0,6.28);ctx.fillStyle='rgba(60,150,255,.4)';ctx.fill();
    ctx.shadowBlur=0;
    ctx.fillStyle='rgba(100,200,255,.5)';ctx.font='6px sans-serif';ctx.textAlign='center';ctx.fillText('CO₂',c[0],c[1]+14);
  }});
  const earthG=ctx.createLinearGradient(0,H*.74,0,H);
  earthG.addColorStop(0,'rgba(40,130,255,.22)');earthG.addColorStop(.3,'rgba(20,90,20,.5)');earthG.addColorStop(1,'#050e04');
  ctx.fillStyle=earthG;ctx.fillRect(0,H*.74,W,H);
  ctx.fillStyle='rgba(80,200,80,.4)';ctx.font='bold 7px sans-serif';ctx.textAlign='center';ctx.fillText('EARTH SURFACE',W/2,H*.82);
  const heatW=(0.3+0.25*Math.sin(t*.04)).toFixed(2);
  ctx.fillStyle='rgba(255,120,40,.65)';ctx.font='7px sans-serif';ctx.textAlign='left';
  ctx.fillText('↓ Solar radiation',10,H*.06);
  ctx.fillStyle='rgba(255,70,20,.6)';ctx.fillText('↻ IR heat trapped',10,H*.21);
  ctx.fillStyle='rgba(100,200,100,.6)';ctx.fillText('↑ Earth warms',10,H*.82);
  ctx.fillStyle='rgba(255,255,255,.22)';ctx.font='7px monospace';ctx.textAlign='center';
  ctx.fillText('Greenhouse gases absorb & re-emit infrared heat → global temperature rises',W/2,H-5);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'seasons':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🌍 EARTH'S SEASONS — ORBITAL TILT</div>
<canvas id="ss" width="460" height="305" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">Earth's 23.5° axial tilt causes different seasons as it orbits the Sun</div>
<script>
const cv=document.getElementById('ss'),ctx=cv.getContext('2d'),W=460,H=305,cx=W/2,cy=H/2;
const stars=[];for(let i=0;i<70;i++)stars.push([Math.random()*W,Math.random()*H,Math.random()*1.2+.3,Math.random()*80]);
const seasons=['☀ Summer','🍂 Autumn','❄ Winter','🌸 Spring'];
const sColors=['#ffa500','#ff6b35','#4fc3f7','#90ee90'];
const positions=[0,Math.PI/2,Math.PI,3*Math.PI/2];
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#010208';ctx.fillRect(0,0,W,H);
  stars.forEach(function(s){{
    ctx.beginPath();ctx.arc(s[0],s[1],s[2],0,6.28);
    ctx.fillStyle='rgba(200,215,255,'+(0.25+0.35*Math.sin(t*.018+s[3])).toFixed(2)+')';ctx.fill();
  }});
  ctx.strokeStyle='rgba(255,255,255,.06)';ctx.lineWidth=1;ctx.setLineDash([3,6]);
  ctx.beginPath();ctx.ellipse(cx,cy,178,88,0,0,6.28);ctx.stroke();ctx.setLineDash([]);
  positions.forEach(function(a,i){{
    const px=cx+178*Math.cos(a),py=cy+88*Math.sin(a);
    ctx.strokeStyle=sColors[i]+'55';ctx.lineWidth=.8;ctx.setLineDash([2,4]);
    ctx.beginPath();ctx.arc(px,py,12,0,6.28);ctx.stroke();ctx.setLineDash([]);
    const tilt=0.45;
    ctx.strokeStyle=sColors[i]+'66';ctx.lineWidth=1.2;
    ctx.beginPath();ctx.moveTo(px-12*Math.cos(tilt),py-15*Math.sin(tilt));ctx.lineTo(px+12*Math.cos(tilt),py+15*Math.sin(tilt));ctx.stroke();
    ctx.fillStyle=sColors[i];ctx.font='7px sans-serif';ctx.textAlign='center';
    ctx.fillText(seasons[i]+'(N)',px,py+(a<Math.PI?-18:20));
  }});
  const sunG=ctx.createRadialGradient(cx,cy,3,cx,cy,32);
  sunG.addColorStop(0,'#fffde7');sunG.addColorStop(.48,'#ffa000');sunG.addColorStop(1,'rgba(230,80,0,0)');
  ctx.shadowColor='#ff8800';ctx.shadowBlur=22;
  ctx.beginPath();ctx.arc(cx,cy,30*(1+.04*Math.sin(t*.04)),0,6.28);ctx.fillStyle=sunG;ctx.fill();
  ctx.shadowBlur=0;
  ctx.fillStyle='rgba(255,215,60,.75)';ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillText('☉ SUN',cx,cy+3);
  const orbitT=t*.016;
  const ex=cx+178*Math.cos(orbitT),ey=cy+88*Math.sin(orbitT);
  const tilt=0.45;
  for(let rr=0;rr<4;rr++){{
    const ra=orbitT+rr*(Math.PI/2);
    const rdx=30*Math.cos(ra),rdy=30*Math.sin(ra);
    const ral=(0.12+0.08*Math.sin(t*.04+rr)).toFixed(2);
    ctx.strokeStyle='rgba(255,220,50,'+ral+')';ctx.lineWidth=1.2;
    ctx.beginPath();ctx.moveTo(cx+10*Math.cos(ra),cy+10*Math.sin(ra));ctx.lineTo(cx+rdx,cy+rdy);ctx.stroke();
  }}
  const eG2=ctx.createRadialGradient(ex-3,ey-3,2,ex,ey,13);
  eG2.addColorStop(0,'#6baed6');eG2.addColorStop(.5,'#2171b5');eG2.addColorStop(1,'#050a20');
  ctx.shadowColor='#4fc3f7';ctx.shadowBlur=8;
  ctx.beginPath();ctx.arc(ex,ey,12,0,6.28);ctx.fillStyle=eG2;ctx.fill();
  ctx.strokeStyle='#4fc3f7';ctx.lineWidth=1.5;ctx.stroke();
  ctx.shadowBlur=0;
  ctx.strokeStyle='rgba(120,210,255,.55)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(ex-14*Math.cos(tilt),ey-17*Math.sin(tilt));ctx.lineTo(ex+14*Math.cos(tilt),ey+17*Math.sin(tilt));ctx.stroke();
  const si=Math.floor(((orbitT%(2*Math.PI))/(2*Math.PI))*4)%4;
  ctx.fillStyle=sColors[si];ctx.font='bold 8px sans-serif';ctx.textAlign='center';
  ctx.fillText(seasons[si]+' (N.Hem.)',ex,ey-22);
  ctx.fillStyle='rgba(255,255,255,.22)';ctx.font='7px monospace';
  ctx.fillText("23.5° tilt: N.Hemisphere tilts toward Sun in June (Summer) · away in December (Winter)",cx,H-5);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'plate_tectonics':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🌏 TECTONIC PLATES — MOVEMENT</div>
<canvas id="pt" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('pt'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const shift=Math.sin(t*.025)*15;
  const col1=ctx.createLinearGradient(0,0,W/2+shift,H);col1.addColorStop(0,'#1a2a10');col1.addColorStop(1,'#0d1508');
  ctx.fillStyle=col1;ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(W/2+shift,0);ctx.lineTo(W/2+shift-30,H);ctx.lineTo(0,H);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(100,180,80,0.6)';ctx.lineWidth=2;ctx.stroke();
  const col2=ctx.createLinearGradient(W/2+shift,0,W,H);col2.addColorStop(0,'#101a28');col2.addColorStop(1,'#050d18');
  ctx.fillStyle=col2;ctx.beginPath();ctx.moveTo(W/2+shift,0);ctx.lineTo(W,0);ctx.lineTo(W,H);ctx.lineTo(W/2+shift-30,H);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(80,140,200,0.6)';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='rgba(255,80,0,0.7)';ctx.font='bold 9px monospace';ctx.textAlign='center';
  ctx.fillText('← Plate A',W/4,H/2);ctx.fillText('Plate B →',W*3/4,H/2);
  const gapW=20+Math.abs(shift)*.5;
  const magG=ctx.createLinearGradient(W/2-gapW/2,0,W/2+gapW/2,0);
  magG.addColorStop(0,'rgba(255,80,0,0)');magG.addColorStop(.5,'rgba(255,100,0,0.6)');magG.addColorStop(1,'rgba(255,80,0,0)');
  ctx.fillStyle=magG;ctx.fillRect(W/2-gapW/2,0,gapW,H);
  ctx.fillStyle='rgba(255,100,50,0.8)';ctx.fillText('↑ Magma',W/2,H/2+20);
  const mtype=shift>0?'Divergent':'Convergent';
  ctx.fillStyle='#40E0D0';ctx.font='bold 10px monospace';ctx.fillText(mtype+' Boundary',W/2,H-20);
  ctx.fillStyle='rgba(100,180,80,0.8)';ctx.font='8px monospace';
  ctx.fillText(shift>0?'←':'→',W/4,H*.35);
  ctx.fillStyle='rgba(80,140,200,0.8)';
  ctx.fillText(shift>0?'→':'←',W*3/4,H*.35);
  ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';
  ctx.fillText('Plates move a few cm per year (very slow!)',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'river_erosion':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🌊 RIVER — EROSION & DEPOSITION</div>
<canvas id="rv" width="360" height="220" style="display:block;"></canvas>
<script>
const cv=document.getElementById('rv'),ctx=cv.getContext('2d'),W=360,H=220;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#0a1508';ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='rgba(30,120,180,0.8)';ctx.lineWidth=18;
  ctx.beginPath();ctx.moveTo(0,80);ctx.bezierCurveTo(60,80,80,140,140,140);ctx.bezierCurveTo(200,140,220,80,280,80);ctx.bezierCurveTo(310,80,330,130,360,140);ctx.stroke();
  ctx.strokeStyle='rgba(60,160,220,0.9)';ctx.lineWidth=8;
  ctx.beginPath();ctx.moveTo(0,80);ctx.bezierCurveTo(60,80,80,140,140,140);ctx.bezierCurveTo(200,140,220,80,280,80);ctx.bezierCurveTo(310,80,330,130,360,140);ctx.stroke();
  const n=12;
  for(let i=0;i<n;i++){{
    const pct=((i/n)+t*.004)%1;
    let bx,by;
    if(pct<0.25){{bx=pct*4*140,by=80+60*(pct*4);}}
    else if(pct<0.5){{bx=140+(pct-.25)*4*140,by=140-60*(pct-.25)*4;}}
    else if(pct<0.75){{bx=280+(pct-.5)*4*80,by=80+50*(pct-.5)*4;}}
    else{{bx=W*(pct-.75)*4+W*.88,by=130;}}
    bx=Math.min(bx,W);ctx.beginPath();ctx.arc(bx,by,3,0,6.28);ctx.fillStyle='rgba(180,220,255,0.8)';ctx.fill();
  }}
  ctx.fillStyle='rgba(255,150,80,0.7)';ctx.font='8px monospace';ctx.textAlign='center';
  ctx.fillText('Erosion',70,65);ctx.fillText('Erosion',210,65);
  ctx.fillStyle='rgba(100,200,100,0.7)';
  ctx.fillText('Deposition',140,165);ctx.fillText('Deposition',280,165);
  ctx.fillStyle='rgba(255,255,255,0.4)';
  ctx.fillText('← Outer bend erodes · Inner bend deposits →',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'trig':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">📐 TRIGONOMETRY — UNIT CIRCLE</div>
<canvas id="tr" width="360" height="240" style="display:block;"></canvas>
<div style="display:flex;gap:14px;font-size:11px;margin-top:4px;justify-content:center;">
  <span style="color:#00e5ff">cos θ (x)</span><span style="color:#a855f7">sin θ (y)</span><span style="color:#ffd700">tan θ</span>
</div>
<script>
const cv=document.getElementById('tr'),ctx=cv.getContext('2d'),W=360,H=240,cx=120,cy=H/2,r=90;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(0,cy);ctx.lineTo(cx*2+10,cy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx,10);ctx.lineTo(cx,H-10);ctx.stroke();
  ctx.strokeStyle='rgba(255,255,255,0.2)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.arc(cx,cy,r,0,6.28);ctx.stroke();
  const angle=t*.04;
  const px=cx+r*Math.cos(angle),py=cy-r*Math.sin(angle);
  ctx.strokeStyle='rgba(255,255,255,0.6)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(px,py);ctx.stroke();
  ctx.strokeStyle='#00e5ff';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(px,cy);ctx.stroke();
  ctx.strokeStyle='#a855f7';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(px,cy);ctx.lineTo(px,py);ctx.stroke();
  ctx.beginPath();ctx.arc(px,py,7,0,6.28);ctx.fillStyle='#fff';ctx.fill();
  ctx.fillStyle='rgba(255,255,255,0.35)';ctx.font='8px monospace';ctx.textAlign='center';
  ctx.fillText('θ='+Math.round(angle%(2*Math.PI)*180/Math.PI)+'°',cx+22,cy-8);
  const sinV=Math.sin(angle),cosV=Math.cos(angle),tanV=Math.tan(angle);
  ctx.fillStyle='#00e5ff';ctx.fillText('cos='+cosV.toFixed(2),W*.68,cy+35);
  ctx.fillStyle='#a855f7';ctx.fillText('sin='+sinV.toFixed(2),W*.68,cy+50);
  ctx.fillStyle='#ffd700';ctx.fillText('tan='+Math.abs(tanV)>5?'∞':tanV.toFixed(2),W*.68,cy+65);
  const gx=W*.65,gw=W*.32,gh=80;
  const gcy=cy;
  ctx.strokeStyle='rgba(255,255,255,0.08)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(gx,gcy-gh/2);ctx.lineTo(gx+gw,gcy-gh/2);ctx.stroke();
  ctx.beginPath();ctx.moveTo(gx,gcy);ctx.lineTo(gx+gw,gcy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(gx,gcy+gh/2);ctx.lineTo(gx+gw,gcy+gh/2);ctx.stroke();
  ctx.strokeStyle='#00e5ff';ctx.lineWidth=1.5;ctx.beginPath();
  for(let x=0;x<=gw;x+=2){{const a=t*.04-3+(x/gw)*6;const y=gcy-cosV*gh/2.2;x===0?ctx.moveTo(gx+x,y):ctx.lineTo(gx+x,y);}}
  ctx.stroke();
  ctx.strokeStyle='#a855f7';ctx.lineWidth=1.5;ctx.beginPath();
  for(let x=0;x<=gw;x+=2){{const a=t*.04-3+(x/gw)*6;const y=gcy-Math.sin(a)*gh/2.2;x===0?ctx.moveTo(gx+x,y):ctx.lineTo(gx+x,y);}}
  ctx.stroke();
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'pythagoras':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">📐 PYTHAGOREAN THEOREM — a² + b² = c²</div>
<canvas id="py" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('py'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const sc=0.9+.05*Math.sin(t*.04);
  const tx=100,ty=160,tw=sc*80,th=sc*60;
  const ax=tx,ay=ty,bx=tx+tw,by=ty,cx2=tx,cy2=ty-th;
  ctx.fillStyle='rgba(100,150,255,0.15)';ctx.strokeStyle='rgba(100,150,255,0.7)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(ax,ay);ctx.lineTo(bx,by);ctx.lineTo(cx2,cy2);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.strokeStyle='rgba(255,200,100,0.3)';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(ax,ay);ctx.lineTo(ax+8,ay);ctx.lineTo(ax+8,ay-8);ctx.lineTo(ax,ay-8);ctx.closePath();ctx.stroke();
  ctx.fillStyle='rgba(255,100,100,0.25)';ctx.strokeStyle='#ef5350';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(ax,ay);ctx.lineTo(ax,ay+tw);ctx.lineTo(ax-tw,ay+tw);ctx.lineTo(ax-tw,ay);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle='#ef5350';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText('a²',ax-tw/2,ay+tw/2+4);
  ctx.fillStyle='rgba(100,255,100,0.25)';ctx.strokeStyle='#4caf50';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bx+th,by);ctx.lineTo(bx+th,by-th);ctx.lineTo(bx,by-th);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle='#4caf50';ctx.fillText('b²',bx+th/2,by-th/2+4);
  const hlen=Math.sqrt(tw*tw+th*th);const hang=Math.atan2(cy2-ay,cx2-bx);
  const px1=bx,py1=by,px2=cx2,py2=cy2;
  const nx=-(py2-py1)/hlen,ny=(px2-px1)/hlen;
  ctx.fillStyle='rgba(100,100,255,0.25)';ctx.strokeStyle='#5c8de8';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(px1,py1);ctx.lineTo(px1+nx*hlen,py1+ny*hlen);ctx.lineTo(px2+nx*hlen,py2+ny*hlen);ctx.lineTo(px2,py2);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle='#5c8de8';ctx.fillText('c²',px1+nx*hlen/2+(px2-px1)/2,py1+ny*hlen/2+(py2-py1)/2+4);
  ctx.fillStyle='rgba(255,200,100,0.9)';ctx.font='8px monospace';
  ctx.fillText('a',ax-tw-12,ay+tw/2+4);ctx.fillText('b',bx+th/2,by+14);ctx.fillText('c',bx+nx*hlen/2+(cx2-bx)/2+8,by+ny*hlen/2+(cy2-by)/2);
  ctx.fillStyle='rgba(255,255,255,0.8)';ctx.font='bold 11px monospace';
  ctx.fillText('a² + b² = c²',250,140);ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='8px monospace';
  ctx.fillText('Right angle',ax+5,ay-5);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'graph_linear':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">📊 LINEAR GRAPH — y = mx + c</div>
<canvas id="gl" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('gl'),ctx=cv.getContext('2d'),W=360,H=240,ox=60,oy=180,sx=30,sy=30;
let t=0;
const lines=[{{m:1,c:0,col:'#00e5ff'}},{{m:2,c:-1,col:'#a855f7'}},{{m:-1,c:3,col:'#ef5350'}}];
function gx(x){{return ox+x*sx;}}function gy(y){{return oy-y*sy;}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.06)';ctx.lineWidth=1;
  for(let x=-1;x<=9;x++){{ctx.beginPath();ctx.moveTo(gx(x),20);ctx.lineTo(gx(x),H-10);ctx.stroke();}}
  for(let y=-2;y<=5;y++){{ctx.beginPath();ctx.moveTo(20,gy(y));ctx.lineTo(W-10,gy(y));ctx.stroke();}}
  ctx.strokeStyle='rgba(255,255,255,0.3)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(20,oy);ctx.lineTo(W-10,oy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(ox,H-10);ctx.lineTo(ox,20);ctx.stroke();
  for(let x=-1;x<=8;x++){{ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText(x,gx(x),oy+14);}}
  for(let y=-1;y<=5;y++){{ctx.textAlign='right';ctx.fillText(y,ox-4,gy(y)+4);}}
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.textAlign='center';ctx.fillText('x',W-8,oy+4);ctx.fillText('y',ox,14);
  const drawPct=Math.min(1,(t*.015)%1+(lines.reduce((a,_,i)=>a,0)>0?0:0));
  lines.forEach((l,i)=>{{
    const dp=Math.max(0,Math.min(1,(t*.012-i*.4)));
    ctx.strokeStyle=l.col;ctx.lineWidth=2;ctx.beginPath();
    let first=true;
    for(let x=-1;x<=8;x+=.1){{
      const y=l.m*x+l.c;const px=gx(x+(1)*dp-1),py=gy(y);
      if(px>=ox-5&&px<=W-5&&py>=20&&py<=H-15){{first?ctx.moveTo(px,py):ctx.lineTo(px,py);first=false;}}
    }}
    ctx.stroke();
    ctx.fillStyle=l.col;ctx.font='8px monospace';ctx.textAlign='left';
    ctx.fillText('y='+l.m+'x'+(l.c>=0?'+'+l.c:l.c),W*.62,50+i*16);
    const intercept=gx(0),iy=gy(l.c);
    ctx.beginPath();ctx.arc(intercept,iy,4,0,6.28);ctx.fillStyle=l.col;ctx.fill();
  }});
  ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='8px monospace';ctx.textAlign='center';
  ctx.fillText('m = slope (gradient) | c = y-intercept',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'graph_quad':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">📊 QUADRATIC GRAPH — y = ax² + bx + c</div>
<canvas id="gq" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('gq'),ctx=cv.getContext('2d'),W=360,H=240,ox=W/2,oy=190,sx=35,sy=25;
let t=0;
const curves=[{{a:1,b:0,c:-3,col:'#00e5ff'}},{{a:-0.5,b:2,c:1,col:'#ef5350'}}];
function gx(x){{return ox+x*sx;}}function gy(y){{return oy-y*sy;}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.06)';ctx.lineWidth=1;
  for(let x=-4;x<=4;x++){{ctx.beginPath();ctx.moveTo(gx(x),15);ctx.lineTo(gx(x),H-10);ctx.stroke();}}
  for(let y=-2;y<=7;y++){{ctx.beginPath();ctx.moveTo(15,gy(y));ctx.lineTo(W-10,gy(y));ctx.stroke();}}
  ctx.strokeStyle='rgba(255,255,255,0.3)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(15,oy);ctx.lineTo(W-10,oy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(ox,H-10);ctx.lineTo(ox,15);ctx.stroke();
  for(let x=-4;x<=4;x++){{ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText(x,gx(x),oy+14);}}
  for(let y=0;y<=7;y++){{ctx.textAlign='right';ctx.fillText(y,ox-4,gy(y)+4);}}
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.textAlign='center';ctx.fillText('x',W-8,oy+4);ctx.fillText('y',ox+4,14);
  curves.forEach((c,i)=>{{
    const dp=Math.max(0,Math.min(1,t*.012-i*.5));
    ctx.strokeStyle=c.col;ctx.lineWidth=2;ctx.beginPath();
    let first=true,cnt=0;
    for(let x=-4;x<=4;x+=.05){{
      cnt++;if(cnt/160>dp)break;
      const y=c.a*x*x+c.b*x+c.c;const px=gx(x),py=gy(y);
      if(py>=15&&py<=H-10){{first?ctx.moveTo(px,py):ctx.lineTo(px,py);first=false;}}
    }}
    ctx.stroke();
    const vx=-c.b/(2*c.a),vy=c.a*vx*vx+c.b*vx+c.c;
    ctx.beginPath();ctx.arc(gx(vx),gy(vy),5,0,6.28);ctx.fillStyle=c.col;ctx.fill();
    ctx.fillStyle=c.col;ctx.font='8px monospace';ctx.textAlign='left';
    const lbl='y='+c.a+'x²'+(c.b>=0?'+'+c.b+'x':c.b+'x')+(c.c>=0?'+'+c.c:c.c);
    ctx.fillText(lbl,15,20+i*16);
    ctx.fillStyle=c.col+'88';ctx.font='7px monospace';ctx.fillText('Vertex('+vx.toFixed(1)+','+vy.toFixed(1)+')',gx(vx)+6,gy(vy)-6);
  }});
  ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='8px monospace';ctx.textAlign='center';
  ctx.fillText('Vertex = turning point of the parabola',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'venn':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">⭕ VENN DIAGRAM — SETS A & B</div>
<canvas id="vn" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('vn'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  const sep=30+15*Math.sin(t*.04),r=80,cx1=W/2-sep,cx2=W/2+sep,cy=H/2;
  ctx.beginPath();ctx.arc(cx1,cy,r,0,6.28);ctx.fillStyle='rgba(100,150,255,0.25)';ctx.fill();ctx.strokeStyle='#6496ff';ctx.lineWidth=2;ctx.stroke();
  ctx.beginPath();ctx.arc(cx2,cy,r,0,6.28);ctx.fillStyle='rgba(255,100,100,0.25)';ctx.fill();ctx.strokeStyle='#ef5350';ctx.lineWidth=2;ctx.stroke();
  ctx.save();ctx.beginPath();ctx.arc(cx1,cy,r,0,6.28);ctx.clip();ctx.beginPath();ctx.arc(cx2,cy,r,0,6.28);ctx.fillStyle='rgba(180,100,200,0.35)';ctx.fill();ctx.restore();
  ctx.fillStyle='#6496ff';ctx.font='bold 12px monospace';ctx.textAlign='center';ctx.fillText('A',cx1-r/2,cy+4);
  ctx.fillStyle='#ef5350';ctx.fillText('B',cx2+r/2,cy+4);
  ctx.fillStyle='rgba(180,100,200,0.9)';ctx.font='8px monospace';ctx.fillText('A∩B',W/2,cy+4);
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='9px monospace';
  ctx.fillText('Only in A',cx1-r*.6,cy-24);ctx.fillText('(A∪B)',cx1-r*.6,cy-12);
  ctx.fillText('Only in B',cx2+r*.3,cy-24);
  const elems=[['1','3','5'],['2','4'],['6','8']];
  const positions=[[cx1-r*.6,cy-8],[W/2,cy+20],[cx2+r*.3,cy-8]];
  const colors=['#6496ff','#d090f0','#ef5350'];
  elems.forEach((e,i)=>e.forEach((n,j)=>{{ctx.fillStyle=colors[i];ctx.font='9px monospace';ctx.fillText(n,positions[i][0]+(j-1)*14,positions[i][1]+20)}}));
  ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';
  ctx.fillText('A∪B = union (all elements) | A∩B = intersection (common)',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'geometry_angles':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">📐 TYPES OF ANGLES</div>
<canvas id="ga" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('ga'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
const types=[
  {{deg:35,col:'#4caf50',label:'Acute\n(< 90°)'}},
  {{deg:90,col:'#00e5ff',label:'Right\n(= 90°)'}},
  {{deg:130,col:'#ffd700',label:'Obtuse\n(90°–180°)'}},
  {{deg:200,col:'#ef5350',label:'Reflex\n(> 180°)'}},
];
function draw(){{
  ctx.clearRect(0,0,W,H);
  const cols=2,rows=2,pw=W/cols,ph=H/rows;
  types.forEach((tp,i)=>{{
    const col=i%cols,row=Math.floor(i/cols);
    const cx=col*pw+pw/2,cy=row*ph+ph*0.45,len=60;
    const deg=tp.deg+20*Math.sin(t*.04+i);
    const rad=deg*Math.PI/180;
    ctx.strokeStyle='rgba(255,255,255,0.3)';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+len,cy);ctx.stroke();
    ctx.strokeStyle=tp.col;ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+len*Math.cos(rad),cy-len*Math.sin(rad));ctx.stroke();
    const arcR=24;ctx.strokeStyle=tp.col+'99';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.arc(cx,cy,arcR,0,-rad,true);ctx.stroke();
    ctx.fillStyle=tp.col;ctx.font='bold 8px monospace';ctx.textAlign='center';
    const mid=rad/2;ctx.fillText(Math.round(deg)+'°',cx+arcR*1.4*Math.cos(-mid),cy+arcR*1.4*Math.sin(-mid)+4);
    const lines=tp.label.split('\n');
    ctx.fillStyle=tp.col;ctx.font='9px monospace';
    lines.forEach((l,j)=>ctx.fillText(l,cx,cy+ph*.4+j*13));
    if(deg===90||Math.abs(deg-90)<5){{
      ctx.strokeStyle=tp.col;ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(cx+14,cy);ctx.lineTo(cx+14,cy-14);ctx.lineTo(cx,cy-14);ctx.stroke();
    }}
  }});
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'geometry_shapes':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">🔷 TYPES OF TRIANGLES & SHAPES</div>
<canvas id="gs" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('gs'),ctx=cv.getContext('2d'),W=360,H=240;
let t=0;
const shapes=[
  {{label:'Equilateral\n(3 equal sides)',col:'#00e5ff',fn:(cx,cy,r,t)=>{{const pts=[];for(let i=0;i<3;i++){{pts.push([cx+r*Math.cos(-Math.PI/2+i*2*Math.PI/3+t*.02),cy+r*Math.sin(-Math.PI/2+i*2*Math.PI/3+t*.02)]);}}return pts;}}}},
  {{label:'Isosceles\n(2 equal sides)',col:'#a855f7',fn:(cx,cy,r,t)=>[[cx,cy-r*1.1],[cx-r*.8,cy+r*.6],[cx+r*.8,cy+r*.6]]}},
  {{label:'Scalene\n(no equal sides)',col:'#ffd700',fn:(cx,cy,r,t)=>[[cx-r*.9,cy+r*.6],[cx+r*.4,cy-r*.9],[cx+r*1,cy+r*.5]]}},
  {{label:'Right Triangle\n(one 90° angle)',col:'#ef5350',fn:(cx,cy,r,t)=>[[cx-r*.8,cy+r*.6],[cx-r*.8,cy-r*.8],[cx+r*.9,cy+r*.6]]}},
];
function draw(){{
  ctx.clearRect(0,0,W,H);
  const pw=W/2,ph=H/2;
  shapes.forEach((s,i)=>{{
    const col=i%2,row=Math.floor(i/2);
    const cx=col*pw+pw/2,cy=row*ph+ph*.42;
    const pts=s.fn(cx,cy,38,t);
    ctx.fillStyle=s.col+'22';ctx.strokeStyle=s.col;ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);
    pts.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.closePath();ctx.fill();ctx.stroke();
    const lns=s.label.split('\n');
    ctx.fillStyle=s.col;ctx.font='8px monospace';ctx.textAlign='center';
    lns.forEach((l,j)=>ctx.fillText(l,cx,cy+ph*.44+j*12));
    if(i===3){{ctx.strokeStyle=s.col+'88';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(pts[0][0]+8,pts[0][1]);ctx.lineTo(pts[0][0]+8,pts[0][1]-8);ctx.lineTo(pts[0][0],pts[0][1]-8);ctx.stroke();}}
  }});
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'demand_supply':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">📉 DEMAND & SUPPLY CURVES</div>
<canvas id="ds" width="360" height="240" style="display:block;"></canvas>
<div style="display:flex;gap:14px;font-size:11px;margin-top:4px;justify-content:center;">
  <span style="color:#ef5350">— Demand (↓ price → ↑ quantity)</span><span style="color:#4caf50">— Supply (↑ price → ↑ quantity)</span>
</div>
<script>
const cv=document.getElementById('ds'),ctx=cv.getContext('2d'),W=360,H=240,ox=50,oy=210,aw=280,ah=180;
let t=0;
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(255,255,255,0.25)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(ox,oy-ah);ctx.lineTo(ox,oy);ctx.lineTo(ox+aw,oy);ctx.stroke();
  ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='9px monospace';ctx.textAlign='center';
  ctx.fillText('Quantity',ox+aw/2,oy+18);ctx.save();ctx.rotate(-Math.PI/2);ctx.fillText('Price',-(oy-ah/2),ox-20);ctx.restore();
  const shift=20*Math.sin(t*.03);
  ctx.strokeStyle='#ef5350';ctx.lineWidth=2.5;ctx.beginPath();
  ctx.moveTo(ox+10,oy-ah+10);ctx.lineTo(ox+aw-10,oy-20);ctx.stroke();
  ctx.strokeStyle='#4caf50';ctx.lineWidth=2.5;ctx.beginPath();
  ctx.moveTo(ox+10,oy-20);ctx.lineTo(ox+aw-10,oy-ah+10);ctx.stroke();
  const eqX=ox+aw/2+shift,eqY=oy-ah/2;
  ctx.strokeStyle='rgba(255,220,50,0.5)';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(eqX,oy);ctx.lineTo(eqX,eqY);ctx.stroke();
  ctx.beginPath();ctx.moveTo(ox,eqY);ctx.lineTo(eqX,eqY);ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath();ctx.arc(eqX,eqY,8,0,6.28);ctx.fillStyle='rgba(255,220,50,0.9)';ctx.fill();
  ctx.fillStyle='rgba(255,220,50,0.9)';ctx.font='bold 9px monospace';ctx.textAlign='center';ctx.fillText('Equilibrium',eqX,eqY-14);
  ctx.fillStyle='#ef5350';ctx.font='bold 9px monospace';ctx.fillText('D',ox+12,oy-ah+22);
  ctx.fillStyle='#4caf50';ctx.fillText('S',ox+aw-20,oy-ah+22);
  ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';
  ctx.fillText('At equilibrium: quantity demanded = quantity supplied',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'circular_flow':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">💰 CIRCULAR FLOW OF INCOME</div>
<canvas id="cf" width="360" height="240" style="display:block;"></canvas>
<script>
const cv=document.getElementById('cf'),ctx=cv.getContext('2d'),W=360,H=240,cx=W/2,cy=H/2;
let t=0,dots=[];
for(let i=0;i<20;i++) dots.push({{p:i/20,lane:i%2,spd:.004+Math.random()*.002}});
function arrow(x1,y1,x2,y2,col){{ctx.strokeStyle=col;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();const a=Math.atan2(y2-y1,x2-x1);ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-8*Math.cos(a-.4),y2-8*Math.sin(a-.4));ctx.lineTo(x2-8*Math.cos(a+.4),y2-8*Math.sin(a+.4));ctx.closePath();ctx.fill();}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='rgba(100,150,255,0.2)';ctx.strokeStyle='#6496ff';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(40,cy-30,110,60,8);ctx.fill();ctx.stroke();
  ctx.fillStyle='rgba(100,200,100,0.2)';ctx.strokeStyle='#4caf50';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(W-150,cy-30,110,60,8);ctx.fill();ctx.stroke();
  ctx.fillStyle='#6496ff';ctx.font='bold 9px monospace';ctx.textAlign='center';ctx.fillText('Households',95,cy);
  ctx.fillStyle='#4caf50';ctx.fillText('Firms',W-95,cy);
  const topPath=[[150,cy-15],[W-150,cy-15]];
  const botPath=[[W-150,cy+15],[150,cy+15]];
  arrow(150,cy-35,W-150,cy-35,'rgba(255,200,50,0.8)');
  arrow(W-150,cy+35,150,cy+35,'rgba(100,200,255,0.8)');
  ctx.fillStyle='rgba(255,200,50,0.8)';ctx.font='8px monospace';ctx.fillText('Labour / Services',cx,cy-50);
  ctx.fillStyle='rgba(100,200,255,0.8)';ctx.fillText('Wages / Income',cx,cy+52);
  arrow(95,cy-30,95,cy-70,'rgba(255,150,50,0.7)');
  ctx.fillStyle='rgba(255,150,50,0.7)';ctx.fillText('Savings / Tax',70,cy-78);
  arrow(W-95,cy-30,W-95,cy-70,'rgba(200,100,255,0.7)');
  ctx.fillStyle='rgba(200,100,255,0.7)';ctx.fillText('Invest / Govt',W-130,cy-78);
  arrow(W-95,cy+30,W-95,cy+70,'rgba(150,220,150,0.7)');
  ctx.fillStyle='rgba(150,220,150,0.7)';ctx.fillText('Goods / Services',W-145,cy+85);
  arrow(95,cy+30,95,cy+70,'rgba(255,200,50,0.7)');
  ctx.fillStyle='rgba(255,200,50,0.7)';ctx.fillText('Consumer Spending',55,cy+85);
  dots.forEach(d=>{{
    d.p=(d.p+d.spd)%1;
    const px=d.lane===0?(150+(W-300)*d.p):(W-150-(W-300)*d.p);
    const py=d.lane===0?cy-35:cy+35;
    ctx.beginPath();ctx.arc(px,py,4,0,6.28);ctx.fillStyle=d.lane===0?'rgba(255,200,50,0.9)':'rgba(100,200,255,0.9)';ctx.fill();
  }});
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'atmosphere':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{background:#010208;margin:0;padding:4px 2px;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;}}</style>
</head><body>
<div style="font-size:11px;color:#40E0D0;letter-spacing:2px;font-weight:700;margin-bottom:2px;">🌍 LAYERS OF THE ATMOSPHERE</div>
<canvas id="atm" width="500" height="355" style="display:block;border-radius:8px;"></canvas>
<div style="font-size:9px;color:#6699aa;margin-top:2px;text-align:center;">Troposphere · Stratosphere · Mesosphere · Thermosphere · Exosphere</div>
<script>
const cv=document.getElementById('atm'),ctx=cv.getContext('2d'),W=500,H=355;
const cx=250,cy=430;
const eR=118,trR=160,stR=210,msR=258,thR=314,exR=366;
const stars=[];
for(let i=0;i<90;i++)stars.push({{x:Math.random()*W,y:Math.random()*H*.72,r:Math.random()*1.5+.3,tw:Math.random()*100}});
const meteors=[
  {{a:Math.PI*1.18,r:358,spd:1.3}},
  {{a:Math.PI*1.48,r:372,spd:1.0}},
  {{a:Math.PI*1.65,r:365,spd:1.5}}
];
let satAng=Math.PI*1.12,planeAng=Math.PI*1.2,t=0;
function band(ri,ro,c1,c2){{
  const grd=ctx.createLinearGradient(cx,cy-ro,cx,cy-ri);
  grd.addColorStop(0,c1);grd.addColorStop(1,c2);
  ctx.beginPath();
  ctx.arc(cx,cy,ro,Math.PI,0,false);
  if(ri>0){{ctx.arc(cx,cy,ri,0,Math.PI,true);}}
  ctx.closePath();ctx.fillStyle=grd;ctx.fill();
}}
function draw(){{
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#010208';ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{{
    const al=(0.35+0.45*Math.sin(t*.022+s.tw)).toFixed(2);
    ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,6.28);
    ctx.fillStyle='rgba(200,215,255,'+al+')';ctx.fill();
  }});
  band(exR,exR+46,'#010210','#020315');
  band(thR,exR,'#04091f','#060b2a');
  band(msR,thR,'#080f44','#0c1660');
  band(stR,msR,'#0c2a82','#1136a0');
  band(trR,stR,'#1048b8','#155ad4');
  band(eR,trR,'#1568e4','#1a7cf4');
  band(0,eR,'#145c28','#1a7434');
  const ozR=188;
  ctx.beginPath();ctx.arc(cx,cy,ozR,Math.PI,0,false);
  ctx.strokeStyle='rgba(150,255,90,.42)';ctx.lineWidth=1.6;ctx.setLineDash([5,4]);ctx.stroke();ctx.setLineDash([]);
  [eR,trR,stR,msR,thR,exR].forEach(r=>{{
    ctx.beginPath();ctx.arc(cx,cy,r,Math.PI,0,false);
    ctx.strokeStyle='rgba(70,130,255,.18)';ctx.lineWidth=.7;ctx.stroke();
  }});
  for(let i=0;i<8;i++){{
    const aA=Math.PI*(1.12+i*.095);
    const aph=(0.12+0.28*Math.sin(t*.05+i*.85)).toFixed(2);
    const x1=cx+thR*Math.cos(aA),y1=cy+thR*Math.sin(aA);
    const x2=cx+(thR+46)*Math.cos(aA+.008),y2=cy+(thR+46)*Math.sin(aA+.008);
    if(y1<H&&y1>0){{
      ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);
      ctx.strokeStyle='rgba(0,255,145,'+aph+')';ctx.lineWidth=2.8;ctx.stroke();
    }}
  }}
  const ldata=[
    {{r:(exR+exR+46)/2,nm:'EXOSPHERE',km:'700 km+',col:'#8888ff'}},
    {{r:(thR+exR)/2,nm:'THERMOSPHERE',km:'80–700 km',col:'#6688ff'}},
    {{r:(msR+thR)/2,nm:'MESOSPHERE',km:'50–80 km',col:'#55aaff'}},
    {{r:(stR+msR)/2,nm:'STRATOSPHERE',km:'12–50 km',col:'#44ccff'}},
    {{r:(trR+stR)/2,nm:'TROPOSPHERE',km:'0–12 km',col:'#88ddff'}},
  ];
  ldata.forEach(l=>{{
    const ly=cy-l.r;
    if(ly>3&&ly<H-3){{
      ctx.fillStyle=l.col;ctx.font='bold 8px sans-serif';ctx.textAlign='left';ctx.fillText(l.nm,3,ly+3);
      ctx.fillStyle=l.col+'aa';ctx.font='7px sans-serif';ctx.fillText(l.km,3,ly+12);
    }}
  }});
  const eTop=cy-eR;
  if(eTop>2&&eTop<H){{
    ctx.fillStyle='#55e888';ctx.font='bold 8px sans-serif';ctx.textAlign='center';ctx.fillText('EARTH',cx,eTop+14);
  }}
  const ozY=cy-ozR;
  if(ozY>3&&ozY<H-3){{
    ctx.fillStyle='rgba(170,255,110,.9)';ctx.font='bold 7px sans-serif';ctx.textAlign='right';ctx.fillText('OZONE LAYER',W-3,ozY+3);
  }}
  planeAng+=.0038;if(planeAng>Math.PI*1.82)planeAng=Math.PI*1.18;
  const pR=(eR+trR)/2;
  const pX=cx+pR*Math.cos(planeAng),pY=cy+pR*Math.sin(planeAng);
  if(pY<H-2&&pY>2){{
    const rot=Math.atan2(Math.cos(planeAng),-Math.sin(planeAng));
    ctx.save();ctx.translate(pX,pY);ctx.rotate(rot);
    ctx.fillStyle='#ffffff';ctx.beginPath();ctx.ellipse(0,0,10,3,0,0,6.28);ctx.fill();
    ctx.fillStyle='#cce8ff';ctx.beginPath();ctx.moveTo(-3,-2.5);ctx.lineTo(4,-2.5);ctx.lineTo(2,0);ctx.lineTo(-3,0);ctx.closePath();ctx.fill();
    ctx.fillStyle='#aaccee';ctx.beginPath();ctx.moveTo(7,-1.2);ctx.lineTo(10.5,-1.2);ctx.lineTo(9.5,0);ctx.lineTo(7,0);ctx.closePath();ctx.fill();
    ctx.restore();
  }}
  meteors.forEach(m=>{{
    m.r-=m.spd;
    if(m.r<msR-8){{m.r=exR+10+Math.random()*25;m.a=Math.PI*(1.08+Math.random()*.84);}}
    const mx=cx+m.r*Math.cos(m.a),my=cy+m.r*Math.sin(m.a);
    if(my<H&&my>0&&mx>0&&mx<W){{
      const tX=mx+20*Math.cos(m.a+.14),tY=my+20*Math.sin(m.a+.14);
      const gm=ctx.createLinearGradient(mx,my,tX,tY);
      gm.addColorStop(0,'rgba(255,185,55,.95)');gm.addColorStop(1,'rgba(255,55,0,0)');
      ctx.beginPath();ctx.moveTo(mx,my);ctx.lineTo(tX,tY);ctx.strokeStyle=gm;ctx.lineWidth=2.2;ctx.stroke();
      ctx.beginPath();ctx.arc(mx,my,2.6,0,6.28);ctx.fillStyle='#ffdd55';ctx.fill();
    }}
  }});
  satAng+=.005;
  const sR=338,sX=cx+sR*Math.cos(satAng),sY=cy+sR*Math.sin(satAng);
  if(sY<H-2&&sY>2&&sX>2&&sX<W-2){{
    ctx.save();ctx.translate(sX,sY);ctx.rotate(satAng+Math.PI/2);
    ctx.fillStyle='#c0d0f0';ctx.fillRect(-5,-2.5,10,5);
    ctx.fillStyle='#2845a8';ctx.fillRect(-13,-2,7,4);ctx.fillRect(6,-2,7,4);
    ctx.fillStyle='rgba(80,160,255,.35)';ctx.fillRect(-13,-1,20,2);
    ctx.restore();
  }}
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    elif topic == 'timeline':
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{{_flex}}}</style></head><body>
<div style="font-size:12px;color:#40E0D0;letter-spacing:2px;margin-bottom:4px;font-weight:700;">📅 HISTORICAL TIMELINE</div>
<canvas id="tl" width="360" height="200" style="display:block;"></canvas>
<div style="font-size:10px;color:#8aa;margin-top:4px;text-align:center;">Timeline shows chronological sequence of events</div>
<script>
const cv=document.getElementById('tl'),ctx=cv.getContext('2d'),W=360,H=200;
let t=0;
const events=[{{y:800,col:'#ef5350'}},{{y:1200,col:'#ffd700'}},{{y:1500,col:'#4caf50'}},{{y:1776,col:'#00e5ff'}},{{y:1900,col:'#a855f7'}},{{y:2000,col:'#ff8a65'}}];
function draw(){{
  ctx.clearRect(0,0,W,H);
  const lx=40,rx=W-40,ly=H/2;
  const grd=ctx.createLinearGradient(lx,0,rx,0);grd.addColorStop(0,'rgba(100,200,255,0.2)');grd.addColorStop(.5,'rgba(100,200,255,0.6)');grd.addColorStop(1,'rgba(100,200,255,0.2)');
  ctx.strokeStyle=grd;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(lx,ly);ctx.lineTo(rx,ly);ctx.stroke();
  ctx.fillStyle='rgba(100,200,255,0.8)';ctx.beginPath();ctx.moveTo(rx+4,ly);ctx.lineTo(rx-8,ly-6);ctx.lineTo(rx-8,ly+6);ctx.closePath();ctx.fill();
  ctx.fillStyle='rgba(255,255,255,0.4)';ctx.font='8px monospace';ctx.textAlign='left';ctx.fillText('Time →',rx+6,ly+3);
  const ymin=events[0].y,ymax=events[events.length-1].y;
  events.forEach((e,i)=>{{
    const px=lx+(rx-lx)*(e.y-ymin)/(ymax-ymin);
    const above=i%2===0;
    const pulsed=1+.1*Math.sin(t*.08+i);
    ctx.beginPath();ctx.arc(px,ly,6*pulsed,0,6.28);ctx.fillStyle=e.col;ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1.5;ctx.stroke();
    ctx.strokeStyle=e.col+'88';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(px,ly);ctx.lineTo(px,above?ly-30:ly+30);ctx.stroke();
    ctx.fillStyle=e.col;ctx.font='bold 9px monospace';ctx.textAlign='center';ctx.fillText(e.y,px,above?ly-40:ly+44);
  }});
  ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText('Chronological order: earliest on left, latest on right',W/2,H-6);
  t++;requestAnimationFrame(draw);
}}
draw();
</script></body></html>"""

    return ""


# ── Chat messages (shown in ALL modes) ───────────────────────────────────────
_msgs_list = cur_msgs()
_last_asst_content = ""
for _mi, msg in enumerate(_msgs_list):
    with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🔱"):
        if msg["role"] == "assistant" and _mi > 0:
            _prev = _msgs_list[_mi - 1]
            if _prev["role"] == "user":
                _dtopic = _detect_diagram_topic(_prev["content"])
                if _dtopic:
                    import html as _html_esc
                    _dhtml = _get_diagram_html(_dtopic)
                    _dh_map = {
                        'atom':360,'dna':370,'solar':380,'cell':340,'water':300,'wave':270,
                        'heart':330,'photosynthesis':320,'circuit':305,'eye':315,
                        'magnet':305,'mitosis':290,'moon':260,'newton':300,
                        'refraction':295,'reflection':295,'lungs':335,'digestion':345,
                        'neuron':265,'plant_structure':335,'food_chain':275,'projectile':280,
                        'circular_motion':300,'volcano':300,'earthquake':300,'rock_cycle':300,
                        'greenhouse':300,'seasons':300,'plate_tectonics':300,'river_erosion':280,
                        'trig':305,'pythagoras':305,'graph_linear':305,'graph_quad':305,
                        'venn':305,'geometry_angles':305,'geometry_shapes':305,
                        'demand_supply':305,'circular_flow':305,'timeline':260,'atmosphere':400,
                    }
                    _dh_val = _dh_map.get(_dtopic, 310)
                    _escaped = _html_esc.escape(_dhtml, quote=True)
                    st.markdown(
                        f'<iframe srcdoc="{_escaped}" width="100%" height="{_dh_val}" '
                        f'style="border:none;background:#05080f;display:block;border-radius:12px;'
                        f'margin:8px 0;" scrolling="no"></iframe>',
                        unsafe_allow_html=True
                    )
        # Strip ASCII art / text diagrams from AI response before displaying
        import re as _re_diag
        _content_show = msg["content"]
        if msg["role"] == "assistant" and _mi > 0:
            _prev2 = _msgs_list[_mi - 1]
            if _prev2["role"] == "user" and _detect_diagram_topic(_prev2["content"]):
                # Remove ALL ASCII/symbol art the AI generates (4 passes)
                # Pass 1: ^^^/~~~/||| style art (2+ consecutive visual symbols, 2+ lines)
                _content_show = _re_diag.sub(
                    r'(?:```[^\n]*\n)?(?:[ \t]*[┌┐└┘│─├┤┬┴┼╔╗╚╝║═╠╣╦╩╬+|^~*#=/\\-]{2,}[^\n]*\n){2,}(?:```\n?)?',
                    '', _content_show)
                # Pass 2: indented pyramid/volcano shapes (leading spaces + symbols)
                _content_show = _re_diag.sub(
                    r'(?:[ \t]{1,}[^a-zA-Z0-9\n\r ]{3,}[ \t]*\n){2,}',
                    '', _content_show)
                # Pass 3: +---+ box frame lines
                _content_show = _re_diag.sub(
                    r'(?:[^\n]*[+\-]{3,}[^\n]*\n)+',
                    '', _content_show)
                # Pass 4: | text | pipe box lines
                _content_show = _re_diag.sub(
                    r'(?:\|[^\n]+\|\n)+',
                    '', _content_show)
        st.markdown(_content_show, unsafe_allow_html=True)
        if msg["role"] == "assistant" and msg.get("content"):
            import json as _json_sb, re as _re_sb
            _spk = _re_sb.sub(r'```[\s\S]*?```', ' code block ', msg["content"])
            _spk = _re_sb.sub(r'!\[.*?\]\(.*?\)', '', _spk)
            _spk = _re_sb.sub(r'\[(.*?)\]\(.*?\)', r'\1', _spk)
            _spk = _re_sb.sub(r'[`*_#>\[\]|]', '', _spk)
            _spk = _re_sb.sub(r'\s+', ' ', _spk).strip()[:4500]
            _spk_payload = _json_sb.dumps(_spk)
            st.html(f"""
<style>
  body {{ margin:0; padding:0; background:transparent;
          font-family:-apple-system,Segoe UI,Roboto,sans-serif; }}
  #b {{ background:#1e3a8a; color:#fff; border:0; border-radius:6px;
        padding:1px 8px; font-size:.62rem; font-weight:500;
        cursor:pointer; opacity:.65; line-height:1.3; }}
  #b:hover {{ opacity:1; }}
  #b.on {{ background:#dc2626; }}
</style>
<button id="b">speak</button>
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
}})();
</script>
""")
    if msg["role"] == "assistant":
        _last_asst_content = msg["content"]

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

# ── Welcome cards ─────────────────────────────────────────────────────────────
if not cur_msgs():
    cols = st.columns(3)
    for i, (icon, text) in enumerate(QUICK_ACTIONS):
        with cols[i % 3]:
            if st.button(f"{icon} {text}", use_container_width=True, key=f"_qa_{i}"):
                st.session_state.quick_q = text
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
    ))

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
    mem = st.session_state.get("titan_memory", {})
    if mem:
        base += "\n\nThings you remember about the user:\n" + "\n".join(f"- {k}: {v}" for k, v in mem.items())
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

    # ── Hard math / science / JEE / NEET / reasoning → GPT-OSS 120B (strongest) ──
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
        # Strongest model — precise, deep, maximum power
        return 8192, 0.30, 0.95
    if "gpt-oss-20b" in m:
        # Fast OpenAI model — slightly warmer for fluency
        return 8192, 0.40, 0.92
    if "qwen" in m:
        # Qwen 27B — good reasoning, balanced
        return 8192, 0.50, 0.90
    if "allam" in m:
        # 7B last resort — still squeeze max quality
        return 8192, 0.60, 0.90
    # Safe default for any future model
    return 8192, 0.40, 0.92


def call_groq(messages):
    client = Groq(api_key=st.session_state.api_key)
    # Cap history at 30 messages by default to stay well under token limits
    full = _build_full(messages, trim=30)

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
        _auto = _smart_pick(messages)  # best model for this question type
        _fallback_chain = [
            _auto,                    # auto-picked for question type
            "openai/gpt-oss-120b",    # strongest always in chain
            "openai/gpt-oss-20b",     # fast fallback
            "qwen/qwen3.8-27b",       # capable 27B
            "allam-2-7b",             # last resort — always available
        ]
    # Deduplicate while preserving order
    _seen = set()
    _chain = [m for m in _fallback_chain if not (m in _seen or _seen.add(m))]
    _last_err = None
    _current_full = full
    _rate_limited = []  # models that hit rate limit — retry once after others fail
    _vision_errors = {}  # track per-model errors for vision debugging
    for m in _chain:
        try:
            _mid = m[5:] if m.startswith("groq/") else m
            _mtok, _mtemp, _mtopp = _model_cfg(_mid)
            _kwargs = {"model": _mid, "messages": _current_full, "max_tokens": _mtok}
            if not _use_vision:
                _kwargs["temperature"] = _mtemp
                _kwargs["top_p"]       = _mtopp
            r = client.chat.completions.create(**_kwargs)
            return r.choices[0].message.content
        except Exception as e:
            _last_err = e
            _es = str(e).lower()
            if _use_vision:
                _vision_errors[_mid] = str(e)[:120]
            # On 413: shrink context and retry the same model once
            if "413" in _es or "request_too_large" in _es or "request entity too large" in _es:
                try:
                    _current_full = _build_full(messages, trim=6)
                    _kwargs["messages"] = _current_full
                    _kwargs["max_tokens"] = 4096
                    r = client.chat.completions.create(**_kwargs)
                    return r.choices[0].message.content
                except Exception as e2:
                    _last_err = e2
                    _current_full = full
                    continue
            # Rate-limited: queue for one retry pass after all other models tried
            if "rate_limit" in _es or "rate limit" in _es or "429" in _es or "tokens per" in _es:
                _rate_limited.append(m)
                continue
            if any(x in _es for x in ("not found","not_found","does not exist","model_not_found",
                                       "decommission","404","context_length","unsupported",
                                       "invalid","not supported","must be a string",
                                       "multimodal","vision")):
                continue
            raise

    # Retry passes — up to 3 rounds, 5 seconds apart, trying every rate-limited model
    if _rate_limited:
        import time as _time
        for _pass in range(3):
            _time.sleep(5)
            for m in _rate_limited:
                try:
                    _mid = m[5:] if m.startswith("groq/") else m
                    _mtok, _mtemp, _mtopp = _model_cfg(_mid)
                    _kwargs = {"model": _mid, "messages": _current_full,
                               "max_tokens": _mtok, "temperature": _mtemp, "top_p": _mtopp}
                    r = client.chat.completions.create(**_kwargs)
                    return r.choices[0].message.content
                except Exception as e:
                    _last_err = e
                    continue

    # All models exhausted — show clean friendly message, never raw Groq errors
    _msg = str(_last_err).lower()
    if "rate_limit" in _msg or "429" in _msg or "tokens per" in _msg:
        raise RuntimeError("⏳ All models are busy right now. Please wait about 1 minute and ask again.")
    if _use_vision:
        raise RuntimeError("❌ Image analysis failed. Please try again or use a different image.")
    raise RuntimeError("⏳ All models are busy right now. Please wait about 1 minute and ask again.")

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
        # ── Online path: try Groq, fall back to Ollama on any failure ─────────
        if _has_internet() and st.session_state.api_key:
            try:
                return call_groq(api_msgs)
            except Exception as _groq_exc:
                _ge = str(_groq_exc).lower()
                # Vision requests never fall back to Ollama — show the real Groq error
                if st.session_state.get("pending_vision"):
                    raise
                # Only fall back to Ollama if it's a service/rate error, not a bad key
                _fallback = any(x in _ge for x in
                    ("rate_limit","429","timeout","connection","decommission",
                     "not found","503","502","500"))
                if not _fallback:
                    raise  # bad API key or invalid request — don't mask it
                # Fall through to Ollama below
        # ── Offline / Groq-failed path ─────────────────────────────────────────
        if not ollama_reachable:
            _wake_ollama()
        _om = _best_ollama_model()
        if _om:
            return call_ollama(api_msgs, ollama_model=_om)
        if ollama_reachable:
            raise RuntimeError(
                "📥 Ollama is running but has no models installed.\n"
                "In the sidebar, click 'Pull Qwen 3' or 'Pull Moondream'."
            )
        raise RuntimeError(
            "📡 No connection to Groq and Ollama is not running.\n"
            "• Check your internet and try again, OR\n"
            "• Install Ollama (https://ollama.com) for offline use."
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

# Native paperclip button INSIDE the chat box (Gemini-style attach button)
_chat_result = st.chat_input(
    "Message TITAN ULTRA...",
    accept_file=True,
    key="_chat_input_main",
)
if _chat_result:
    user_input = _chat_result.text or None
    if _chat_result.files:
        uploaded_file = _chat_result.files[0]
else:
    user_input = None

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
        else:
            file_content = uploaded_file.read().decode("utf-8", errors="replace")
    except Exception:
        file_content = f"[File: {uploaded_file.name}]"
st.session_state.pending_vision = _current_vision

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

    if not st.session_state.api_key and provider == "Groq":
        st.error("❌ Please enter your Groq API key in the sidebar first.")
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
            # Auto-trigger live weather fetch when user asks about weather
            if _is_weather_query(user_input):
                import re as _re_wq
                _m_city = _re_wq.search(
                    r'(?:weather|temperature|forecast|climate)\s+(?:in|for|of|at)\s+(.+?)(?:\?|$)',
                    user_input, _re_wq.IGNORECASE)
                st.session_state.weather_query = _m_city.group(1).strip() if _m_city else user_input
            with st.spinner("🔱 TITAN ULTRA is thinking…"):
                try:
                    _api_msgs = [{"role":m["role"],"content":m["content"]} for m in cur_msgs()]
                    answer = _do_ai_call(_api_msgs)
                    msgs = cur_msgs(); msgs.append({"role":"assistant","content":answer}); set_msgs(msgs)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""<div style='text-align:center;font-size:.6rem;color:#1a2a3a;letter-spacing:3px;padding:4px'>
🔱 TITAN ULTRA · GROQ ACCELERATED · OLLAMA OFFLINE READY · VOICE INPUT · PC CONTROL
</div>""", unsafe_allow_html=True)
