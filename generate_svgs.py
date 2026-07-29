import os
import xml.etree.ElementTree as ET

def create_svg(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    clean_content = content.strip()
    # Validate XML
    try:
        ET.fromstring(clean_content)
    except ET.ParseError as e:
        print(f"XML ERROR in {path}: {e}")
        raise e
    with open(path, "w", encoding="utf-8") as f:
        f.write(clean_content)
    print(f"Generated valid SVG: {path}")

def gen_section(num, title, dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    text_color = "#FFFFFF" if dark else "#000000"
    line_color = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 90" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Section {num}">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="90" fill="{bg}"/>
  <line x1="48" y1="45" x2="952" y2="45" stroke="{line_color}" stroke-width="1.5"/>
  <rect x="48" y="25" width="280" height="40" fill="{bg}"/>
  <text fill="{text_color}" class="mono" x="56" y="51" font-size="18" font-weight="800" letter-spacing="3.5">{num} — {title.upper()}</text>
</svg>'''

def gen_header(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#999999" if dark else "#444444"
    dim = "#777777" if dark else "#666666"
    accent = "#BBBBBB" if dark else "#333333"
    rule = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 420" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Garv Nanda Header">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
    .title {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; font-weight: 900; }}
  </style>
  <rect width="1000" height="420" fill="{bg}"/>
  <line x1="48" y1="50" x2="952" y2="50" stroke="{rule}" stroke-width="1.5"/>
  <text class="mono" fill="{muted}" x="48" y="38" font-size="13" font-weight="700" letter-spacing="3.5">PORTFOLIO — INDEX Nº 001</text>
  <text class="mono" fill="{muted}" x="952" y="38" font-size="13" font-weight="700" letter-spacing="3.5" text-anchor="end">DELHI, IN — 28.61° N</text>

  <text fill="{bone}" class="title" x="46" y="160" font-size="72" letter-spacing="-2">Garv Nanda</text>
  <text fill="{muted}" class="mono" x="48" y="206" font-size="22" font-weight="700">ML &amp; Backend Engineer — Training models while my CPU screams for mercy.</text>

  <text fill="{dim}" class="mono" x="48" y="268" font-size="15" font-weight="700" letter-spacing="1">focus  ▸</text>
  <text fill="{accent}" class="mono" x="140" y="268" font-size="15" font-weight="600" letter-spacing="0.5">machine learning · high-throughput backends · AI safety · Web3 systems</text>
  
  <text fill="{dim}" class="mono" x="48" y="300" font-size="15" font-weight="700" letter-spacing="1">status ▸</text>
  <text fill="{accent}" class="mono" x="140" y="300" font-size="15" font-weight="600" letter-spacing="0.5">open for internships · freelance · research collaboration</text>

  <line x1="48" y1="350" x2="952" y2="350" stroke="{rule}" stroke-width="1.5"/>
  <text fill="{muted}" class="mono" x="48" y="386" font-size="13" font-weight="700" letter-spacing="2.5">PYTHON &amp; PYTORCH</text>
  <text fill="{accent}" class="mono" x="240" y="386" font-size="14">·</text>
  <text fill="{muted}" class="mono" x="260" y="386" font-size="13" font-weight="700" letter-spacing="2.5">FASTAPI &amp; BACKENDS</text>
  <text fill="{accent}" class="mono" x="490" y="386" font-size="14">·</text>
  <text fill="{muted}" class="mono" x="510" y="386" font-size="13" font-weight="700" letter-spacing="2.5">AI SAFETY &amp; LLMS</text>
  <text fill="{muted}" class="mono" x="952" y="386" font-size="13" font-weight="700" letter-spacing="2.5" text-anchor="end">3RD YEAR CSE @ GGSIPU</text>
</svg>'''

def gen_whoami(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#BBBBBB" if dark else "#333333"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 320" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Who Am I">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="320" fill="{bg}"/>
  <rect x="48" y="16" width="904" height="288" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  
  <text fill="{bone}" class="mono" x="80" y="60" font-size="18" font-weight="800" letter-spacing="2">ABOUT / SYSTEM DIAGNOSTICS</text>
  <line x1="80" y1="76" x2="920" y2="76" stroke="{border}" stroke-width="1"/>
  
  <text fill="{muted}" class="mono" x="80" y="116" font-size="15" font-weight="500">▸ 3rd-year B.Tech CSE undergrad at GGSIPU specializing in Machine Learning engineering,</text>
  <text fill="{muted}" class="mono" x="100" y="142" font-size="15" font-weight="500">high-throughput backend architecture, and AI safety framework design.</text>
  
  <text fill="{muted}" class="mono" x="80" y="182" font-size="15" font-weight="500">▸ Building resilient, production AI systems — from voice-first LLM copilots (GallaSaathi)</text>
  <text fill="{muted}" class="mono" x="100" y="208" font-size="15" font-weight="500">and conversational crime AI (Datathon 2026) to neural network auditing suites (SANN).</text>

  <text fill="{muted}" class="mono" x="80" y="248" font-size="15" font-weight="500">▸ Core expertise: PyTorch model fine-tuning (LoRA/PEFT), neural safety &amp; shortcut detection,</text>
  <text fill="{muted}" class="mono" x="100" y="274" font-size="15" font-weight="500">distributed FastAPI microservices, and decentralized Web3 application backends.</text>
</svg>'''

def gen_ecosystem(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#AAAAAA" if dark else "#444444"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 420" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ecosystem System Map">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="420" fill="{bg}"/>
  
  <!-- Box 1 -->
  <rect x="48" y="20" width="436" height="175" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="72" y="56" font-size="16" font-weight="800" letter-spacing="1">01. MACHINE LEARNING &amp; LLMS</text>
  <line x1="72" y1="70" x2="460" y2="70" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="72" y="102" font-size="14" font-weight="500">• Gemma 4 &amp; LLM Fine-Tuning (LoRA / PEFT)</text>
  <text fill="{muted}" class="mono" x="72" y="128" font-size="14" font-weight="500">• Speech Recognition (Sarvam ASR &amp; AI4Bharat)</text>
  <text fill="{muted}" class="mono" x="72" y="154" font-size="14" font-weight="500">• PyTorch, Scikit-Learn &amp; Embeddings</text>

  <!-- Box 2 -->
  <rect x="516" y="20" width="436" height="175" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="540" y="56" font-size="16" font-weight="800" letter-spacing="1">02. BACKEND &amp; SYSTEM DESIGN</text>
  <line x1="540" y1="70" x2="928" y2="70" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="540" y="102" font-size="14" font-weight="500">• High-Performance FastAPI Microservices</text>
  <text fill="{muted}" class="mono" x="540" y="128" font-size="14" font-weight="500">• Supabase / PostgreSQL &amp; Redis Caching</text>
  <text fill="{muted}" class="mono" x="540" y="154" font-size="14" font-weight="500">• Containerization &amp; Zoho Catalyst Deployment</text>

  <!-- Box 3 -->
  <rect x="48" y="220" width="436" height="175" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="72" y="256" font-size="16" font-weight="800" letter-spacing="1">03. AI SAFETY &amp; NEURAL AUDITING</text>
  <line x1="72" y1="270" x2="460" y2="270" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="72" y="302" font-size="14" font-weight="500">• Model Memorization &amp; Shortcut Detectors</text>
  <text fill="{muted}" class="mono" x="72" y="328" font-size="14" font-weight="500">• Backdoor Poisoning &amp; Leakage Inspection</text>
  <text fill="{muted}" class="mono" x="72" y="354" font-size="14" font-weight="500">• Explainable AI &amp; Robustness Benchmarks</text>

  <!-- Box 4 -->
  <rect x="516" y="220" width="436" height="175" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="540" y="256" font-size="16" font-weight="800" letter-spacing="1">04. WEB3 &amp; DECENTRALIZED APPS</text>
  <line x1="540" y1="270" x2="928" y2="270" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="540" y="302" font-size="14" font-weight="500">• Smart Contract Architecture (Solidity)</text>
  <text fill="{muted}" class="mono" x="540" y="328" font-size="14" font-weight="500">• Decentralized SocialFi Infrastructure</text>
  <text fill="{muted}" class="mono" x="540" y="354" font-size="14" font-weight="500">• Web3 Backend Integration &amp; Node APIs</text>
</svg>'''

def gen_projects(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#AAAAAA" if dark else "#444444"
    dim = "#888888" if dark else "#666666"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    projects_data = [
        ("DATATHON-2026", "Conversational AI for KSP Crime DB (Zoho Catalyst)", "FastAPI · Gemma LLM · NetworkX · Streamlit"),
        ("DEBATEMIND", "AI Debate &amp; Argumentation Analysis Engine", "Python · NLP · LLMs · Speech Analysis"),
        ("DEVLENS", "Developer Productivity &amp; Code Telemetry Suite", "Python · AST Parser · Static Analysis"),
        ("SANN", "Self-Auditing Neural Networks — AI Safety Suite", "PyTorch · HuggingFace · Poisoning Detector"),
        ("CREATOR_X", "Decentralized SocialFi Web3 &amp; Mobile Platform", "Solidity · Web3.js · Node.js · React Native"),
        ("GALLA-SATHI", "Voice-First AI Copilot for Kirana Shopkeepers", "TypeScript · FastAPI · Gemma 4 · Sarvam ASR")
    ]
    
    boxes = ""
    for idx, (title, desc, tech) in enumerate(projects_data):
        row = idx // 2
        col = idx % 2
        x = 48 if col == 0 else 516
        y = 20 + row * 200
        
        boxes += f'''
  <rect x="{x}" y="{y}" width="436" height="180" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="{x+24}" y="{y+42}" font-size="17" font-weight="800" letter-spacing="1">0{idx+1}. {title}</text>
  <line x1="{x+24}" y1="{y+56}" x2="{x+412}" y2="{y+56}" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="{x+24}" y="{y+92}" font-size="14" font-weight="500">{desc}</text>
  <text fill="{dim}" class="mono" x="{x+24}" y="{y+136}" font-size="13" font-weight="700">TAGS: {tech}</text>'''

    return f'''<svg viewBox="0 0 1000 640" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Featured Projects">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="640" fill="{bg}"/>
  {boxes}
</svg>'''

def gen_telemetry(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#AAAAAA" if dark else "#444444"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 130" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Development Telemetry">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="130" fill="{bg}"/>
  <rect x="48" y="10" width="904" height="110" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  
  <text fill="{bone}" class="mono" x="76" y="48" font-size="18" font-weight="800" letter-spacing="2">REAL-TIME DEVELOPMENT TELEMETRY</text>
  <text fill="{muted}" class="mono" x="76" y="82" font-size="14" font-weight="500">Live commit telemetry, repository metrics, and language breakdown synced directly from @Garvnanda</text>
</svg>'''

def gen_timeline(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#AAAAAA" if dark else "#444444"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    milestones = [
        ("2023", "Foundations — CS &amp; Systems Engineering at GGSIPU, mastering Python, C++, and DSA."),
        ("2024", "ML &amp; Backend Expansion — Developed News-Categorizer, DevLens, DebateMind, and microservices."),
        ("2025", "AI Safety &amp; LLMs — Fine-tuned Gemma 4 for GallaSaathi, built SANN audit suite &amp; Creator_X."),
        ("2026", "Enterprise Datathon — Built Intelligent Conversational Crime AI for KSP DB on Zoho Catalyst.")
    ]
    
    items = ""
    for idx, (year, text) in enumerate(milestones):
        y = 44 + idx * 68
        items += f'''
  <circle cx="80" cy="{y-5}" r="6" fill="{bone}"/>
  <text fill="{bone}" class="mono" x="108" y="{y}" font-size="15" font-weight="800">{year}</text>
  <text fill="{muted}" class="mono" x="170" y="{y}" font-size="14" font-weight="500">{text}</text>'''

    return f'''<svg viewBox="0 0 1000 320" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Development Timeline">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="320" fill="{bg}"/>
  <rect x="48" y="10" width="904" height="300" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <line x1="80" y1="44" x2="80" y2="248" stroke="{border}" stroke-width="2.5"/>
  {items}
</svg>'''

def gen_experience(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#AAAAAA" if dark else "#444444"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 180" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Experience">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="180" fill="{bg}"/>
  <rect x="48" y="10" width="904" height="160" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  
  <text fill="{bone}" class="mono" x="76" y="48" font-size="17" font-weight="800" letter-spacing="1">ML &amp; BACKEND SOFTWARE ENGINEER</text>
  <text fill="{muted}" class="mono" x="924" y="48" font-size="14" font-weight="700" text-anchor="end">2024 — PRESENT</text>
  <line x1="76" y1="64" x2="924" y2="64" stroke="{border}" stroke-width="1"/>
  
  <text fill="{muted}" class="mono" x="76" y="98" font-size="14" font-weight="500">• Architecting production machine learning models, REST APIs, and automated evaluation suites.</text>
  <text fill="{muted}" class="mono" x="76" y="126" font-size="14" font-weight="500">• Designing voice-first LLM applications, neural safety audit tools, and high-performance backends.</text>
</svg>'''

def gen_stack(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    bone = "#FFFFFF" if dark else "#000000"
    muted = "#BBBBBB" if dark else "#333333"
    card_bg = "#111111" if dark else "#F8F9FA"
    border = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 480" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Technical Stack">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="480" fill="{bg}"/>
  
  <!-- Row 1: Languages -->
  <rect x="48" y="10" width="904" height="100" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="76" y="42" font-size="16" font-weight="800" letter-spacing="1">PROGRAMMING LANGUAGES</text>
  <line x1="76" y1="52" x2="924" y2="52" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="76" y="80" font-size="14.5" font-weight="600">Python  ·  C++  ·  SQL  ·  JavaScript  ·  TypeScript  ·  Solidity</text>

  <!-- Row 2: ML & AI -->
  <rect x="48" y="125" width="904" height="100" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="76" y="157" font-size="16" font-weight="800" letter-spacing="1">MACHINE LEARNING &amp; AI</text>
  <line x1="76" y1="167" x2="924" y2="167" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="76" y="195" font-size="14.5" font-weight="600">PyTorch  ·  Gemma 4  ·  Hugging Face  ·  Scikit-Learn  ·  Pandas  ·  NetworkX  ·  OpenCV</text>

  <!-- Row 3: Backend & Infrastructure -->
  <rect x="48" y="240" width="904" height="100" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="76" y="272" font-size="16" font-weight="800" letter-spacing="1">BACKEND &amp; CLOUD INFRASTRUCTURE</text>
  <line x1="76" y1="282" x2="924" y2="282" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="76" y="310" font-size="14.5" font-weight="600">FastAPI  ·  Supabase / PostgreSQL  ·  Redis  ·  Docker  ·  Uvicorn  ·  Zoho Catalyst</text>

  <!-- Row 4: Tools -->
  <rect x="48" y="355" width="904" height="100" rx="8" fill="{card_bg}" stroke="{border}" stroke-width="1.5"/>
  <text fill="{bone}" class="mono" x="76" y="387" font-size="16" font-weight="800" letter-spacing="1">DEVELOPER TOOLS &amp; WORKFLOWS</text>
  <line x1="76" y1="397" x2="924" y2="397" stroke="{border}" stroke-width="1"/>
  <text fill="{muted}" class="mono" x="76" y="425" font-size="14.5" font-weight="600">Git  ·  GitHub Actions  ·  Linux  ·  Jupyter  ·  Streamlit  ·  Vercel  ·  VS Code</text>
</svg>'''

def gen_footer(dark=False):
    bg = "#000000" if dark else "#FFFFFF"
    muted = "#AAAAAA" if dark else "#444444"
    rule = "#30363D" if dark else "#E1E4E8"
    
    return f'''<svg viewBox="0 0 1000 90" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Footer">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
  </style>
  <rect width="1000" height="90" fill="{bg}"/>
  <line x1="48" y1="25" x2="952" y2="25" stroke="{rule}" stroke-width="1.5"/>
  <text fill="{muted}" class="mono" x="48" y="60" font-size="13" font-weight="700" letter-spacing="2.5">SYSTEM STATUS: ONLINE ●</text>
  <text fill="{muted}" class="mono" x="952" y="60" font-size="13" font-weight="700" letter-spacing="2.5" text-anchor="end">GARV NANDA © 2026</text>
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

print("All SVG assets regenerated and XML validated successfully!")
