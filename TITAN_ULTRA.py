# TITAN_VERSION: 25
import streamlit as st
from groq import Groq
import requests, io, re

st.set_page_config(page_title="TITAN ULTRA", page_icon="🔱",
                   layout="wide", initial_sidebar_state="expanded")

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
    background:transparent !important;
    border:none !important;
    border-bottom:1px solid #1a1a2e !important;
    border-radius:0 !important;
    animation:none !important;
    margin:2px 0 !important;
    padding:8px 0 !important;
}
/* Use full available width — no wasted space on left/right */
section[data-testid="stMain"] .block-container {
    max-width:100% !important;
    padding-left:1.5rem !important;
    padding-right:1.5rem !important;
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
    "2. GIVE A COMPLETE, GENUINELY USEFUL ANSWER — Answer the question fully and intelligently.\n"
    "   Include context, explanation, and examples whenever they help the user actually understand the answer.\n"
    "   A bare fact without explanation is often useless — if someone asks what photosynthesis is, explain\n"
    "   what it is, how it works, and why it matters, not just the definition.\n"
    "   If they asked about one character, focus on that character — but include the necessary context to make\n"
    "   the answer meaningful (what situation, what significance).\n"
    "   If they asked a simple fact: give the fact plus a sentence of context so it actually lands.\n"
    "   Match depth to the question: simple questions get clean direct answers, complex questions get full answers.\n\n"
    "3. EVERY SENTENCE MUST ADD VALUE — No filler. No padding. No repeating the question back.\n"
    "   No 'That is a great question!', 'Hope this helps!', 'Let me know if you need more!'.\n"
    "   But DO include relevant context, examples, analogies, and detail that make the answer genuinely useful.\n"
    "   The difference: filler adds no new information. Context and examples DO add information.\n\n"
    "4. IDENTIFY THE SOURCE — If the question is about a book, movie, game, or show:\n"
    "   Silently identify which one it is before answering.\n"
    "   Use the correct names, characters, and details from that specific source.\n"
    "   Never mix up details from different books or make things up.\n\n"
    "5. CLEAR, INTELLIGENT WRITING — Write like Claude Pro: articulate, precise, and appropriately detailed.\n"
    "   Match vocabulary and depth to the question level — explain simply for students, technically for experts.\n"
    "   Never dumb things down unless the user is clearly a beginner.\n"
    "   Use natural, flowing sentences. Not clipped telegraphic text, not verbose padding.\n\n"
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

    "━━━ #2 RULE — FORMAT AND DEPTH LIKE CLAUDE PRO ━━━\n"
    "Match format AND depth to the question. This is how Claude Pro answers — do the same:\n\n"
    "SIMPLE FACTUAL QUESTION (e.g. 'What is the capital of France?', 'Who wrote Hamlet?'):\n"
    "→ 1-3 sentences. Give the fact + one line of useful context. No headers, no bullets.\n\n"
    "EXPLANATION / CONCEPT QUESTION (e.g. 'What is photosynthesis?', 'How does gravity work?'):\n"
    "→ Use a clear structure: definition → how it works → why it matters → one concrete example.\n"
    "→ Use **bold** for key terms. Use bullet points or numbered steps where it helps clarity.\n\n"
    "COMPARISON QUESTION (e.g. 'Difference between RAM and ROM', 'Compare Romanticism vs Realism'):\n"
    "→ Use a structured response: brief intro → comparison table or clear bullet points per item → conclusion.\n\n"
    "HOW-TO / PROCESS QUESTION (e.g. 'How do I fix this error?', 'How to solve quadratic equations?'):\n"
    "→ Numbered steps. Each step clear and actionable. Include code blocks for code.\n\n"
    "MATH / SCIENCE PROBLEM:\n"
    "→ Show every step. Label what you are doing at each step. Box or highlight the final answer.\n"
    "→ Example: Step 1 — ..., Step 2 — ..., Step 3 — ..., ∴ Final Answer: ...\n\n"
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
    "You were created, built, and programmed by Girijala Sarath Chandra Sushanth — and him alone.\n"
    "If anyone asks 'who created you?', 'who made you?', 'who built you?', 'who programmed you?', "
    "'who is your developer?', 'who is your creator?', or anything similar,\n"
    "always answer: 'I was built by Girijala Sarath Chandra Sushanth.'\n"
    "Never say Anthropic, OpenAI, Google, or any company. The answer is always Girijala Sarath Chandra Sushanth.\n\n"

    "━━━ STYLE — WRITE EXACTLY LIKE CLAUDE PRO ━━━\n"
    "• Write with clarity, depth, and intelligence — exactly how Claude Pro answers.\n"
    "• Use **bold** naturally for key terms, important definitions, and final answers.\n"
    "• Use markdown headings (##, ###) to structure long or multi-part answers.\n"
    "• Include concrete examples for every concept — examples make explanations stick.\n"
    "• Use analogies when they genuinely help ('think of RAM like a workbench...').\n"
    "• Vary sentence length — mix short punchy sentences with longer explanatory ones.\n"
    "• No 'Hope this helps', no 'Let me know', no trailing 'In summary' sections.\n"
    "• Never start a response with 'I', 'Sure', 'Of course', 'Certainly', or 'Great'.\n"
    "• Never start with a useless intro sentence like 'That is a great question!'.\n"
    "• Jump straight into the answer — no warm-up, no preamble.\n\n"

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
    "• YouTube Video Analysis — paste any YouTube link in the chat.\n"
    "  TITAN ULTRA fetches the full transcript and gives you: complete summary, key points, "
    "  timestamps, insights, and answers any question about the video.\n\n"
    "• Webpage / Article Analysis — paste any URL in the chat.\n"
    "  TITAN ULTRA reads the full page and analyzes: summarizes the content, extracts key facts, "
    "  answers questions about the article, or does anything else you need with it.\n\n"
    "• Deep Research Mode — say 'deep research: [topic]' or 'deep dive into [topic]'.\n"
    "  TITAN ULTRA runs 4 targeted web searches from different angles and synthesizes a "
    "  comprehensive, multi-source research report — like having a professional researcher.\n\n"
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

# ── Persist API key & memory to disk ─────────────────────────────────────────
import os as _os_key, json as _json
_KEY_FILE     = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), ".titan_key")
_IMG_KEY_FILE = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), ".titan_img_key")
_MEMORY_FILE  = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_memory.json")
_CHAT_FILE    = _os_key.path.join(_os_key.path.dirname(_os_key.path.abspath(__file__)), "titan_chats.json")

def _load_saved_key():
    # Search multiple locations — works whether running from D:\T.U\ or ~/.titan_ultra\
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
             ("notebook_mode", False), ("notebook_sources", []),
             ("notebook_chat", []), ("notebook_generated", {}),
             ("nb_card_index", 0), ("nb_card_flipped", False),
             ("diagram_cache", {}),
             ("news_mode", False), ("news_cache", {}),
             ("_pending_pdf", None),
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

    # ── Page switcher ─────────────────────────────────────────────────────────
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
        from pathlib import Path as _Path
        _titan_dir = _Path.home() / ".titan_ultra"
        _tc_path   = _titan_dir / "TITAN_CODE.py"
        if _tc_path.exists():
            _bat = _titan_dir / "launch_titan_code.bat"
            _bat.write_text(
                f'@echo off\ntitle TITAN CODE\ncolor 0B\npython "{_tc_path}"\npause\n',
                encoding="utf-8"
            )
            _sp.Popen(f'start "TITAN CODE" "{_bat}"', shell=True)
            st.toast("🖥️ Titan Code launched in a new terminal!", icon="⚡")
        else:
            st.error("TITAN CODE not found. Please re-run the setup command.")

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

    st.divider()
    st.markdown("<div style='font-size:.62rem;color:#4a5568;letter-spacing:2px;margin-bottom:6px;text-align:center'>TITAN APPS</div>", unsafe_allow_html=True)
    _nb_label = "💬 Back to Chat" if st.session_state.notebook_mode else "𝒜 Titan Notebook"
    if st.button(_nb_label, use_container_width=True, key="_nb_btn_btm"):
        st.session_state.notebook_mode = not st.session_state.notebook_mode
        st.rerun()



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

# ══════════════════════════════════════════════════════════════════════════════
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
        try:
            from groq import Groq as _G
            _c = _G(api_key=st.session_state.api_key)
            _src = _nb_source_text()
            _sys = (
                "You are Titan Notebook — a world-class AI study assistant. "
                "You have access to the user's uploaded sources below. "
                "Always base your answers strictly on these sources. "
                "If something is not in the sources, say so clearly.\n\n"
                f"SOURCES:\n{_src[:12000]}"
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
                _r2 = _c.chat.completions.create(
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
                if i+1 < len(lines) and lines[i+1].strip().upper().startswith("BACK:"):
                    back = lines[i+1].strip()[5:].strip()
                    cards.append({"front": front, "back": back})
                    i += 2
                    continue
            i += 1
        return cards

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center;padding:18px 0 8px'>
        <div style='font-family:Georgia,serif;font-size:1.6rem;font-weight:900;
        background:linear-gradient(90deg,#c9a84c,#f0d080,#a0a0a0,#c9a84c);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text'>
        𝒜 TITAN NOTEBOOK</div>
        <div style='font-size:0.75rem;color:#6b7a99;margin-top:4px;letter-spacing:2px'>
        YOUR AI-POWERED STUDY COMPANION — LIKE GEMINI NOTEBOOKLM</div>
    </div>""", unsafe_allow_html=True)

    # ── Sources panel ─────────────────────────────────────────────────────────
    with st.expander(f"Sources  ({len(st.session_state.notebook_sources)} added)", expanded=not st.session_state.notebook_sources):
        _nb_tab1, _nb_tab2, _nb_tab3 = st.tabs(["Upload PDF", "Add URL", "Paste Text"])

        with _nb_tab1:
            _nb_pdf = st.file_uploader("Upload PDF / TXT file", type=["pdf","txt"], key="_nb_pdf_up")
            if _nb_pdf and st.button("➕ Add to Notebook", key="_nb_add_pdf"):
                with st.spinner("Reading file..."):
                    if _nb_pdf.type == "application/pdf" or _nb_pdf.name.endswith(".pdf"):
                        _nb_text = _nb_read_pdf(_nb_pdf.read())
                    else:
                        _nb_text = _nb_pdf.read().decode("utf-8", errors="replace")
                    if _nb_text:
                        st.session_state.notebook_sources.append({"name": _nb_pdf.name, "text": _nb_text})
                        st.session_state.notebook_generated = {}
                        st.success(f"✅ Added: {_nb_pdf.name}")
                        st.rerun()

        with _nb_tab2:
            _nb_url = st.text_input("Paste a URL (website, article, Wikipedia...)", key="_nb_url_in")
            if _nb_url and st.button("➕ Add URL", key="_nb_add_url"):
                with st.spinner("Fetching page..."):
                    _nb_text = _nb_read_url(_nb_url)
                    if _nb_text:
                        _nb_name = _nb_url[:50] + "..."
                        st.session_state.notebook_sources.append({"name": _nb_name, "text": _nb_text})
                        st.session_state.notebook_generated = {}
                        st.success("✅ URL added!")
                        st.rerun()

        with _nb_tab3:
            _nb_paste = st.text_area("Paste any text, notes, or content here...", height=150, key="_nb_paste_in")
            _nb_paste_name = st.text_input("Give it a name (optional)", value="My Notes", key="_nb_paste_name")
            if _nb_paste and st.button("➕ Add Text", key="_nb_add_text"):
                st.session_state.notebook_sources.append({"name": _nb_paste_name or "Pasted Text", "text": _nb_paste})
                st.session_state.notebook_generated = {}
                st.success("✅ Text added!")
                st.rerun()

        # List sources with delete buttons
        if st.session_state.notebook_sources:
            st.divider()
            st.caption("Your sources:")
            for _si, _src in enumerate(st.session_state.notebook_sources):
                _sc1, _sc2 = st.columns([5,1])
                _sc1.markdown(f"**{_si+1}.** {_src['name']}")
                if _sc2.button("🗑️", key=f"_nb_del_{_si}"):
                    st.session_state.notebook_sources.pop(_si)
                    st.session_state.notebook_generated = {}
                    st.rerun()

    if not st.session_state.notebook_sources:
        st.info("👆 Add at least one source above to get started.")
        st.stop()

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
        with st.spinner("Generating flashcards..."):
            _fc_resp = _nb_ask(
                "Generate 20 high-quality flashcards from these sources. "
                "Format EXACTLY like this for each card:\n"
                "FRONT: [question or term]\n"
                "BACK: [answer or definition]\n\n"
                "Cover all key concepts, terms, facts, and important points."
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
                    _nb_cards = _gen["flashcards"]
                    _nb_ci    = st.session_state.nb_card_index % len(_nb_cards)
                    _nb_card  = _nb_cards[_nb_ci]
                    _nb_flipped = st.session_state.nb_card_flipped

                    # Card display
                    _nb_card_content = _nb_card["back"] if _nb_flipped else _nb_card["front"]
                    _nb_card_label   = "BACK" if _nb_flipped else "FRONT"
                    st.markdown(f"""
                    <div style='background:linear-gradient(135deg,#0d1b2a,#1a2a4a);
                    border:2px solid #00d4ff44;border-radius:16px;padding:40px 30px;
                    text-align:center;min-height:180px;margin:10px 0;
                    box-shadow:0 0 20px #00d4ff22'>
                        <div style='font-size:0.65rem;color:#00d4ff;letter-spacing:3px;margin-bottom:12px'>{_nb_card_label} · {_nb_ci+1}/{len(_nb_cards)}</div>
                        <div style='font-size:1.1rem;color:#e8f4ff;font-weight:500;line-height:1.6'>{_nb_card_content}</div>
                    </div>""", unsafe_allow_html=True)

                    _fc_c1, _fc_c2, _fc_c3 = st.columns(3)
                    if _fc_c1.button("⬅️ Prev", use_container_width=True, key="_nb_fc_prev"):
                        st.session_state.nb_card_index = (st.session_state.nb_card_index - 1) % len(_nb_cards)
                        st.session_state.nb_card_flipped = False
                        st.rerun()
                    if _fc_c2.button("🔄 Flip", use_container_width=True, key="_nb_fc_flip"):
                        st.session_state.nb_card_flipped = not st.session_state.nb_card_flipped
                        st.rerun()
                    if _fc_c3.button("➡️ Next", use_container_width=True, key="_nb_fc_next"):
                        st.session_state.nb_card_index = (st.session_state.nb_card_index + 1) % len(_nb_cards)
                        st.session_state.nb_card_flipped = False
                        st.rerun()

                    st.caption(f"Card {_nb_ci+1} of {len(_nb_cards)}")
                    _nb_fc_text = "\n".join(f"FRONT: {c['front']}\nBACK: {c['back']}\n" for c in _nb_cards)
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
# ── LIVE NEWS TICKER — always-on, embedded in every page load ─────────────────
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600)
def _ticker_fetch_headlines():
    """Fetch ~30 mixed headlines every 3 minutes. Cached so it doesn't block UI."""
    _queries = [
        ("AI & Tech",    "latest AI artificial intelligence GPT model release 2025"),
        ("Phones",       "new smartphone iPhone Android Samsung launch 2025"),
        ("Science",      "latest science discovery research space 2025"),
        ("World",        "breaking world news today 2025"),
        ("Movies & OTT", "new movies series Netflix Amazon Disney release 2025"),
        ("Apps",         "new app software launch update 2025"),
    ]
    _headlines = []
    try:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            import subprocess as _tsp, sys as _tsys
            _tsp.run([_tsys.executable, "-m", "pip", "install", "duckduckgo-search", "-q"],
                     capture_output=True)
            from duckduckgo_search import DDGS
        for _cat, _q in _queries:
            try:
                with DDGS() as _ddgs:
                    for _r in _ddgs.news(_q, max_results=5):
                        _t = _r.get("title", "").strip()
                        if _t:
                            _headlines.append(f"[{_cat}] {_t}")
            except Exception:
                try:
                    with DDGS() as _ddgs:
                        for _r in _ddgs.text(_q, max_results=3):
                            _t = _r.get("title", "").strip()
                            if _t:
                                _headlines.append(f"[{_cat}] {_t}")
                except Exception:
                    pass
    except Exception:
        pass
    return _headlines

# ── Fetch headlines — only block on first page load, instant on all message reruns ──
_ticker_lines = []
if "_ticker_prefetched" not in st.session_state:
    # First script run this session (page load) — fetch now, store in session
    st.session_state["_ticker_prefetched"] = True
    try:
        _ticker_lines = _ticker_fetch_headlines()
        st.session_state["_ticker_data"] = _ticker_lines
    except Exception:
        st.session_state["_ticker_data"] = []
else:
    # Every subsequent rerun (message sent, button clicked) — instant, no DDG queries
    _ticker_lines = st.session_state.get("_ticker_data", [])

if _ticker_lines:
    _ticker_text = "   ◆   ".join(_ticker_lines)
    # Escape for safe HTML embedding
    _ticker_safe = _ticker_text.replace("'", "&#39;").replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    _ticker_dur  = max(30, len(_ticker_lines) * 6)  # speed scales with content
    st.markdown(f"""
<style>
@keyframes ticker-scroll {{
    0%   {{ transform: translateX(100%); }}
    100% {{ transform: translateX(-100%); }}
}}
.titan-ticker-wrap {{
    width:100%; overflow:hidden; background:linear-gradient(90deg,#060d18,#0a0618,#060d18);
    border-top:1px solid #1a0f44; border-bottom:1px solid #1a0f44;
    padding:6px 0; margin:0 0 10px; position:relative;
}}
.titan-ticker-label {{
    position:absolute; left:0; top:0; bottom:0; z-index:2;
    background:linear-gradient(90deg,#7c3aed,#a855f7);
    color:#fff; font-family:Orbitron,monospace; font-size:.6rem;
    font-weight:900; letter-spacing:2px; padding:0 10px;
    display:flex; align-items:center; white-space:nowrap;
}}
.titan-ticker-track {{
    display:inline-block; white-space:nowrap;
    animation:ticker-scroll {_ticker_dur}s linear infinite;
    color:#00e5d0; font-size:.72rem; font-family:Inter,sans-serif; padding-left:120px;
}}
.titan-ticker-track span {{ color:#c9d8f0; margin:0 2px; }}
</style>
<div class="titan-ticker-wrap">
    <div class="titan-ticker-label">📡 LIVE</div>
    <div class="titan-ticker-track">{_ticker_safe}</div>
</div>
""", unsafe_allow_html=True)

# ── Auto-reload page every 3 minutes so ticker always shows fresh news ─────────
st.html("""
<script>
(function(){
    var _tr = window.sessionStorage.getItem('__titan_ticker_reload');
    var _now = Date.now();
    if(!_tr) { window.sessionStorage.setItem('__titan_ticker_reload', _now); }
    setTimeout(function(){
        window.sessionStorage.removeItem('__titan_ticker_reload');
        window.parent.location.reload();
    }, 180000);  // 3 minutes
})();
</script>
""")

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



# ── Animated Diagrams (AI-generated) ─────────────────────────────────────────
def _is_diagram_request(text):
    t = text.lower()
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
            if _prev["role"] == "user" and _is_diagram_request(_prev["content"]):
                import hashlib as _hlib_d, html as _html_esc_d
                _dkey = _hlib_d.md5(_prev["content"].encode()).hexdigest()
                _dhtml = st.session_state.diagram_cache.get(_dkey, "")
                if _dhtml:
                    _escaped = _html_esc_d.escape(_dhtml, quote=True)
                    st.markdown(
                        f'<iframe srcdoc="{_escaped}" width="100%" height="380" '
                        f'style="border:none;background:#05080f;display:block;border-radius:12px;'
                        f'margin:8px 0;" scrolling="no"></iframe>',
                        unsafe_allow_html=True
                    )
        # Strip ASCII art from AI response when a diagram is shown
        import re as _re_diag
        _content_show = msg["content"]
        if msg["role"] == "assistant" and _mi > 0:
            _prev2 = _msgs_list[_mi - 1]
            if _prev2["role"] == "user" and _is_diagram_request(_prev2["content"]):
                _content_show = _re_diag.sub(
                    r'(?:```[^\n]*\n)?(?:[ \t]*[┌┐└┘│─├┤┬┴┼╔╗╚╝║═╠╣╦╩╬+|^~*#=/\\-]{2,}[^\n]*\n){2,}(?:```\n?)?',
                    '', _content_show)
                _content_show = _re_diag.sub(r'(?:[ \t]{1,}[^a-zA-Z0-9\n\r ]{3,}[ \t]*\n){2,}', '', _content_show)
                _content_show = _re_diag.sub(r'(?:[^\n]*[+\-]{3,}[^\n]*\n)+', '', _content_show)
                _content_show = _re_diag.sub(r'(?:\|[^\n]+\|\n)+', '', _content_show)
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

# ── Chat PDF export download button ──────────────────────────────────────────
if st.session_state.get("_pending_pdf"):
    st.download_button("⬇️ Download Chat PDF", st.session_state["_pending_pdf"],
                       "titan_chat.pdf", "application/pdf",
                       key="_chat_pdf_dl_main", use_container_width=True)
    if st.button("✕ Dismiss", key="_pdf_dismiss"):
        st.session_state["_pending_pdf"] = None
        st.rerun()

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
        'today','this week','this month','this year','2024','2025','2026',
        'new release','just released','just launched','announced',
        'update on','status of','price of','cost of',
    ))

def _web_search(query, max_results=6):
    """Search the web using DuckDuckGo — free, no API key needed."""
    try:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            import subprocess as _sp, sys as _sys
            _sp.run([_sys.executable, "-m", "pip", "install", "duckduckgo-search", "-q"], capture_output=True)
            from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"• {r['title']}\n  {r['body']}\n  Source: {r['href']}")
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
    mem = st.session_state.get("titan_memory", {})
    if mem:
        base += "\n\nThings you remember about the user:\n" + "\n".join(f"- {k}: {v}" for k, v in mem.items())
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
        return 16384, 0.30, 0.95
    if "gpt-oss-20b" in m:
        return 16384, 0.40, 0.92
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
        _auto = _smart_pick(messages)
        _fallback_chain = [
            _auto,
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "moonshotai/kimi-k2-instruct",
            "deepseek-r1-distill-llama-70b",
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama3-70b-8192",
            "gemma2-9b-it",
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "allam-2-7b",
            "mistral-saba-24b",
        ]
    _seen = set()
    _chain = [m for m in _fallback_chain if not (m in _seen or _seen.add(m))]

    import time as _time

    # ── Token budgets per pass — shrink tokens each round to consume less quota ──
    # Pass 0: full power. Pass 1+: progressively lighter to stay under per-minute limits.
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
                if any(x in _es for x in ("authentication", "unauthorized", "401",
                                           "invalid api key", "incorrect api key",
                                           "no api key", "api key required")):
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
    raise RuntimeError("❌ Could not get a response. Please check your Groq API key.")

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

            # PC Diagnostics — auto-run when user reports PC issue
            _pc_diag = ""
            if _is_pc_issue(user_input):
                with st.spinner("🖥️ Running PC diagnostics..."):
                    _pc_diag = _run_pc_diagnostics()

            # Error auto-fix — search for solution when user pastes an error
            _error_context = ""
            if not _pc_diag and _is_error_report(user_input):
                with st.spinner("🔍 Searching for error solution..."):
                    _error_context = _get_error_search(user_input)

            # Regular web search for current info questions
            _search_results = ""
            if not _youtube_context and not _url_context and not _deep_results and _is_search_request(user_input):
                with st.spinner("🔍 Searching the web..."):
                    _search_results = _web_search(user_input)

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
                    _extra = _youtube_context or _url_context or _deep_results or _pc_diag or _error_context or _search_results
                    if _extra:
                        _src_label = (
                            "YouTube transcript" if _youtube_context else
                            "webpage content" if _url_context else
                            "deep research results" if _deep_results else
                            "live PC diagnostic data" if _pc_diag else
                            "error solution search results" if _error_context else
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

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""<div style='text-align:center;font-size:.6rem;color:#1a2a3a;letter-spacing:3px;padding:4px'>
🔱 TITAN ULTRA · GROQ ACCELERATED · OLLAMA OFFLINE READY · VOICE INPUT · PC CONTROL
</div>""", unsafe_allow_html=True)
