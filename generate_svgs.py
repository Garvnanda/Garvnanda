import os

def create_svg(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated {path}")

def gen_section(num, title, dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    text_color = "#FFFFFF" if dark else "#000000"
    sub_color = "#777777" if dark else "#888888"
    line_color = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 80" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Section {num}">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="80" fill="{bg}"/>
  <line x1="48" y1="40" x2="952" y2="40" stroke="{line_color}" stroke-width="1"/>
  <rect x="48" y="24" width="220" height="32" fill="{bg}"/>
  <text fill="{text_color}" class="mono" x="56" y="45" font-size="14" font-weight="700" letter-spacing="3">{num} — {title.upper()}</text>
</svg>'''

def gen_header(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#888888" if dark else "#555555"
    dim = "#666666" if dark else "#777777"
    accent = "#AAAAAA" if dark else "#444444"
    rule = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 380" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Garv Nanda Header">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
    .title {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; font-weight: 800; }}
  </style>
  <rect width="1000" height="380" fill="{bg}"/>
  <line x1="48" y1="48" x2="952" y2="48" stroke="{rule}" stroke-width="1"/>
  <text class="mono" fill="{muted}" x="48" y="36" font-size="11" letter-spacing="3.5">PORTFOLIO — INDEX Nº 001</text>
  <text class="mono" fill="{muted}" x="952" y="36" font-size="11" letter-spacing="3.5" text-anchor="end">DELHI, IN — 28.61° N</text>

  <text fill="{bone}" class="title" x="46" y="150" font-size="64" letter-spacing="-2">Garv Nanda</text>
  <text fill="{muted}" class="mono" x="48" y="190" font-size="18" font-weight="600">ML &amp; Backend Engineer — Training models while my CPU screams for mercy.</text>

  <text fill="{dim}" class="mono" x="48" y="246" font-size="13" letter-spacing="1">focus  ▸</text>
  <text fill="{accent}" class="mono" x="128" y="246" font-size="13" letter-spacing="1">machine learning · high-throughput backends · AI safety · Web3 systems</text>
  
  <text fill="{dim}" class="mono" x="48" y="274" font-size="13" letter-spacing="1">status ▸</text>
  <text fill="{accent}" class="mono" x="128" y="274" font-size="13" letter-spacing="1">open for internships · freelance · research collaboration</text>

  <line x1="48" y1="318" x2="952" y2="318" stroke="{rule}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="48" y="350" font-size="11.5" letter-spacing="2.5">PYTHON &amp; PYTORCH</text>
  <text fill="{accent}" class="mono" x="225" y="350" font-size="11.5">·</text>
  <text fill="{muted}" class="mono" x="245" y="350" font-size="11.5" letter-spacing="2.5">FASTAPI &amp; BACKENDS</text>
  <text fill="{accent}" class="mono" x="455" y="350" font-size="11.5">·</text>
  <text fill="{muted}" class="mono" x="475" y="350" font-size="11.5" letter-spacing="2.5">AI SAFETY &amp; LLMS</text>
  <text fill="{muted}" class="mono" x="952" y="350" font-size="11.5" letter-spacing="2.5" text-anchor="end">3RD YEAR CSE @ GGSIPU</text>
</svg>'''

def gen_whoami(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#A0A0A0" if dark else "#444444"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 300" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Who Am I">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="300" fill="{bg}"/>
  <rect x="48" y="16" width="904" height="268" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  
  <text fill="{bone}" class="mono" x="80" y="56" font-size="16" font-weight="700" letter-spacing="2">ABOUT / DIAGNOSTICS</text>
  <line x1="80" y1="72" x2="920" y2="72" stroke="{border}" stroke-width="1"/>
  
  <text fill="{muted}" class="mono" x="80" y="108" font-size="13.5">▸ 3rd-year B.Tech CSE undergrad at GGSIPU specializing in Machine Learning engineering,</text>
  <text fill="{muted}" class="mono" x="98" y="132" font-size="13.5">high-throughput backend architecture, and AI safety framework design.</text>
  
  <text fill="{muted}" class="mono" x="80" y="168" font-size="13.5">▸ Passionate about building resilient, production-ready AI systems — from voice-first LLM copilots</text>
  <text fill="{muted}" class="mono" x="98" y="192" font-size="13.5">(GallaSaathi) and intelligent conversational crime DBs (Datathon-2026) to neural network auditing (SANN).</text>

  <text fill="{muted}" class="mono" x="80" y="228" font-size="13.5">▸ Core focus: PyTorch model fine-tuning (LoRA/PEFT), neural safety &amp; shortcut detection,</text>
  <text fill="{muted}" class="mono" x="98" y="252" font-size="13.5">distributed FastAPI microservices, and decentralized Web3 application backends.</text>
</svg>'''

def gen_ecosystem(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#888888" if dark else "#555555"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 360" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ecosystem System Map">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="360" fill="{bg}"/>
  
  <!-- Box 1 -->
  <rect x="48" y="20" width="436" height="150" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="72" y="52" font-size="14" font-weight="700" letter-spacing="1">01. MACHINE LEARNING &amp; LLMS</text>
  <line x1="72" y1="64" x2="460" y2="64" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="72" y="92" font-size="12">• Gemma 4 &amp; LLM Fine-Tuning (LoRA / PEFT)</text>
  <text fill="{muted}" class="mono" x="72" y="114" font-size="12">• Speech Recognition (Sarvam ASR &amp; AI4Bharat)</text>
  <text fill="{muted}" class="mono" x="72" y="136" font-size="12">• PyTorch, Scikit-Learn &amp; Embeddings</text>

  <!-- Box 2 -->
  <rect x="516" y="20" width="436" height="150" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="540" y="52" font-size="14" font-weight="700" letter-spacing="1">02. BACKEND &amp; SYSTEM DESIGN</text>
  <line x1="540" y1="64" x2="928" y2="64" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="540" y="92" font-size="12">• High-Performance FastAPI Services</text>
  <text fill="{muted}" class="mono" x="540" y="114" font-size="12">• Supabase / PostgreSQL &amp; Redis Caching</text>
  <text fill="{muted}" class="mono" x="540" y="136" font-size="12">• Containerization &amp; Zoho Catalyst Deployment</text>

  <!-- Box 3 -->
  <rect x="48" y="190" width="436" height="150" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="72" y="222" font-size="14" font-weight="700" letter-spacing="1">03. AI SAFETY &amp; NEURAL AUDITING</text>
  <line x1="72" y1="234" x2="460" y2="234" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="72" y="262" font-size="12">• Model Memorization &amp; Shortcut Detectors</text>
  <text fill="{muted}" class="mono" x="72" y="284" font-size="12">• Backdoor Poisoning &amp; Leakage Inspection</text>
  <text fill="{muted}" class="mono" x="72" y="306" font-size="12">• Explainable AI &amp; Robustness Benchmarks</text>

  <!-- Box 4 -->
  <rect x="516" y="190" width="436" height="150" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="540" y="222" font-size="14" font-weight="700" letter-spacing="1">04. WEB3 &amp; DECENTRALIZED APPS</text>
  <line x1="540" y1="234" x2="928" y2="234" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="540" y="262" font-size="12">• Smart Contract Architecture (Solidity)</text>
  <text fill="{muted}" class="mono" x="540" y="284" font-size="12">• Decentralized SocialFi Infrastructure</text>
  <text fill="{muted}" class="mono" x="540" y="306" font-size="12">• Web3 Backend Integration &amp; Node APIs</text>
</svg>'''

def gen_projects(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#888888" if dark else "#555555"
    dim = "#A0A0A0" if dark else "#666666"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    projects_data = [
        ("DATATHON-2026", "Conversational AI for KSP Crime Database (Zoho Catalyst)", "FastAPI · Gemma LLM · NetworkX · Streamlit"),
        ("DEBATEMIND", "AI-Powered Debate & Argumentation Analysis Engine", "Python · NLP · LLMs · Speech Analysis"),
        ("DEVLENS", "Developer Productivity & Codebase Telemetry Suite", "Python · AST Parser · Code Metrics"),
        ("SANN", "Self-Auditing Neural Networks — AI Safety Framework", "PyTorch · HuggingFace · Poisoning Detector"),
        ("CREATOR_X", "Decentralized SocialFi Web3 & Mobile Platform", "Solidity · Web3.js · Node.js · React Native"),
        ("GALLA-SATHI", "Voice-First AI Copilot for Kirana Shopkeepers", "TypeScript · FastAPI · Gemma 4 · Sarvam ASR")
    ]
    
    boxes = ""
    for idx, (title, desc, tech) in enumerate(projects_data):
        row = idx // 2
        col = idx % 2
        x = 48 if col == 0 else 516
        y = 20 + row * 165
        
        boxes += f'''
  <rect x="{x}" y="{y}" width="436" height="145" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="{x+24}" y="{y+36}" font-size="14" font-weight="700" letter-spacing="1">0{idx+1}. {title}</text>
  <line x1="{x+24}" y1="{y+48}" x2="{x+412}" y2="{y+48}" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="{x+24}" y="{y+76}" font-size="11.5">{desc}</text>
  <text fill="{dim}" class="mono" x="{x+24}" y="{y+108}" font-size="11" font-weight="600">TAGS: {tech}</text>'''

    return f'''<svg viewBox="0 0 1000 520" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Featured Projects">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="520" fill="{bg}"/>
  {boxes}
</svg>'''

def gen_telemetry(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#888888" if dark else "#555555"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 120" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Development Telemetry">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="120" fill="{bg}"/>
  <rect x="48" y="10" width="904" height="100" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  
  <text fill="{bone}" class="mono" x="76" y="44" font-size="15" font-weight="700" letter-spacing="2">REAL-TIME DEVELOPMENT TELEMETRY</text>
  <text fill="{muted}" class="mono" x="76" y="74" font-size="12">Live commit telemetry, repository metrics, and language breakdown synced directly from @Garvnanda</text>
</svg>'''

def gen_timeline(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#888888" if dark else "#555555"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    milestones = [
        ("2023", "Foundations — CS & Systems Engineering at GGSIPU, deep dive into Python, C++, and DSA."),
        ("2024", "ML & Backend Expansion — Developed News-Categorizer, DevLens, DebateMind, and microservice APIs."),
        ("2025", "AI Safety & LLMs — Fine-tuned Gemma 4 for GallaSaathi, created SANN auditing suite, built Creator_X."),
        ("2026", "Enterprise Datathon — Built Intelligent Conversational Crime AI for KSP Database (Zoho Catalyst).")
    ]
    
    items = ""
    for idx, (year, text) in enumerate(milestones):
        y = 36 + idx * 60
        items += f'''
  <circle cx="80" cy="{y-4}" r="5" fill="{bone}"/>
  <text fill="{bone}" class="mono" x="104" y="{y}" font-size="13" font-weight="700">{year}</text>
  <text fill="{muted}" class="mono" x="160" y="{y}" font-size="12">{text}</text>'''

    return f'''<svg viewBox="0 0 1000 280" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Development Timeline">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="280" fill="{bg}"/>
  <rect x="48" y="10" width="904" height="260" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <line x1="80" y1="36" x2="80" y2="216" stroke="{border}" stroke-width="2"/>
  {items}
</svg>'''

def gen_experience(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#888888" if dark else "#555555"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 160" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Experience">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="160" fill="{bg}"/>
  <rect x="48" y="10" width="904" height="140" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  
  <text fill="{bone}" class="mono" x="76" y="44" font-size="14" font-weight="700" letter-spacing="1">ML &amp; BACKEND SOFTWARE ENGINEER</text>
  <text fill="{muted}" class="mono" x="952" y="44" font-size="12" text-anchor="end">2024 — PRESENT</text>
  <line x1="76" y1="56" x2="924" y2="56" stroke="{border}" stroke-width="1"/>
  
  <text fill="{muted}" class="mono" x="76" y="84" font-size="12">• Architecting production machine learning models, REST APIs, and automated evaluation suites.</text>
  <text fill="{muted}" class="mono" x="76" y="108" font-size="12">• Designing voice-first LLM applications, neural safety audit tools, and high-performance backends.</text>
</svg>'''

def gen_stack(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#888888" if dark else "#555555"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 320" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Technical Stack">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="320" fill="{bg}"/>
  
  <rect x="48" y="10" width="436" height="135" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="72" y="40" font-size="13" font-weight="700" letter-spacing="1">PROGRAMMING LANGUAGES</text>
  <line x1="72" y1="50" x2="460" y2="50" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="72" y="78" font-size="12">Python · C++ · SQL · JavaScript · TypeScript · Solidity</text>

  <rect x="516" y="10" width="436" height="135" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="540" y="40" font-size="13" font-weight="700" letter-spacing="1">MACHINE LEARNING &amp; AI</text>
  <line x1="540" y1="50" x2="928" y2="50" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="540" y="78" font-size="12">PyTorch · Gemma 4 · Hugging Face · Scikit-Learn · Pandas · NetworkX</text>

  <rect x="48" y="165" width="436" height="135" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="72" y="195" font-size="13" font-weight="700" letter-spacing="1">BACKEND &amp; CLOUD INFRASTRUCTURE</text>
  <line x1="72" y1="205" x2="460" y2="205" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="72" y="233" font-size="12">FastAPI · Supabase / PostgreSQL · Redis · Docker · Uvicorn · Catalyst</text>

  <rect x="516" y="165" width="436" height="135" rx="6" fill="{card_bg}" stroke="{border}" stroke-width="1"/>
  <text fill="{bone}" class="mono" x="540" y="195" font-size="13" font-weight="700" letter-spacing="1">DEVELOPER TOOLS &amp; WORKFLOWS</text>
  <line x1="540" y1="205" x2="928" y2="205" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="540" y="233" font-size="12">Git · GitHub Actions · Linux · Jupyter · Streamlit · Vercel · VS Code</text>
</svg>'''

def gen_footer(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    muted = "#888888" if dark else "#555555"
    rule = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 80" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Footer">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="80" fill="{bg}"/>
  <line x1="48" y1="20" x2="952" y2="20" stroke="{rule}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="48" y="52" font-size="11.5" letter-spacing="2">SYSTEM STATUS: ONLINE ●</text>
  <text fill="{muted}" class="mono" x="952" y="52" font-size="11.5" letter-spacing="2" text-anchor="end">GARV NANDA © 2026</text>
</svg>'''

base_dir = "c:/Projects/Garvnanda/Garvnanda"

sections = [
    ("s01", "whoami"),
    ("s02", "system map"),
    ("s03", "projects"),
    ("s04", "telemetry"),
    ("s05", "the route"),
    ("s06", "stack")
]

for dark in [False, True]:
    folder = os.path.join(base_dir, "assets", "dark" if dark else "")
    create_svg(os.path.join(folder, "header-v1.svg"), gen_header(dark))
    create_svg(os.path.join(folder, "whoami.svg"), gen_whoami(dark))
    create_svg(os.path.join(folder, "ecosystem.svg"), gen_ecosystem(dark))
    create_svg(os.path.join(folder, "projects.svg"), gen_projects(dark))
    create_svg(os.path.join(folder, "telemetry.svg"), gen_telemetry(dark))
    create_svg(os.path.join(folder, "timeline.svg"), gen_timeline(dark))
    create_svg(os.path.join(folder, "experience.svg"), gen_experience(dark))
    create_svg(os.path.join(folder, "stack.svg"), gen_stack(dark))
    create_svg(os.path.join(folder, "footer.svg"), gen_footer(dark))
    
    for filename, title in sections:
        create_svg(os.path.join(folder, f"{filename}.svg"), gen_section(filename.upper(), title, dark))

print("All SVG assets generated successfully!")
