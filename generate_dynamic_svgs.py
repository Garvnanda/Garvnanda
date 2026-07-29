import os
import math
import random
import requests
import xml.etree.ElementTree as ET

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "Garvnanda"

def create_svg(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    clean_content = content.strip()
    try:
        ET.fromstring(clean_content)
    except ET.ParseError as e:
        print(f"XML ERROR in {path}: {e}")
        raise e
    with open(path, "w", encoding="utf-8") as f:
        f.write(clean_content)
    print(f"Generated valid SVG: {path}")

# --- DATA FETCHING ---
def get_recent_commits():
    default_commits = [
        ("Galla-Sathi", "a8f3b92", "feat: voice overlay & ASR dispatcher pipeline optimization"),
        ("SANN", "4c11e02", "fix: neural poisoning defense evaluation threshold"),
        ("DebateMind", "99f6e64", "refactor: argument graph NLP transformer model")
    ]
    if not GITHUB_TOKEN:
        return default_commits
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    try:
        res = requests.get(f"https://api.github.com/users/{USERNAME}/events/public", headers=headers)
        if res.status_code == 200:
            commits = []
            for event in res.json():
                if event['type'] == 'PushEvent':
                    repo_name = event['repo']['name'].split('/')[-1]
                    for commit in event['payload']['commits']:
                        sha = commit['sha'][:7]
                        msg = commit['message'].split('\n')[0][:55]
                        commits.append((repo_name, sha, msg))
                        if len(commits) == 3:
                            return commits
            if commits:
                return commits
    except Exception as e:
        print(f"Commit fetch fallback: {e}")
    return default_commits

def get_top_repos():
    default_repos = [
        ("Galla-Sathi", 150), ("SANN", 120), ("DevLens", 95), 
        ("DebateMind", 80), ("DATATHON-2026", 65), ("CREATOR_X", 40)
    ]
    if not GITHUB_TOKEN:
        return default_repos
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    try:
        res = requests.get(f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=10", headers=headers)
        if res.status_code == 200:
            repos = [(r['name'], r['stargazers_count'] * 10 + r['size'] % 100) for r in res.json() if not r['fork']]
            if len(repos) >= 4:
                return repos[:6]
    except Exception as e:
        print(f"Repo fetch fallback: {e}")
    return default_repos

def get_contribution_matrix():
    cols, rows = 52, 7
    matrix = [[0 for _ in range(rows)] for _ in range(cols)]
    
    # Generate path fallback
    curr_r = 3
    for c in range(cols):
        matrix[c][curr_r] = 1
        if c < cols - 1:
            moves = [0]
            if curr_r > 1: moves.append(-1)
            if curr_r < rows - 2: moves.append(1)
            curr_r += random.choice(moves)
            matrix[c][curr_r] = 1
            
    # Add noise
    for c in range(cols):
        for r in range(rows):
            if matrix[c][r] == 0 and random.random() > 0.75:
                matrix[c][r] = 1
                
    if GITHUB_TOKEN:
        query = """
        query($login: String!) {
            user(login: $login) {
                contributionsCollection {
                    contributionCalendar {
                        weeks { contributionDays { contributionCount } }
                    }
                }
            }
        }
        """
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
        try:
            res = requests.post("https://api.github.com/graphql", json={"query": query, "variables": {"login": USERNAME}}, headers=headers)
            if res.status_code == 200:
                weeks = res.json()['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
                for c, week in enumerate(weeks[-52:]):
                    for r, day in enumerate(week['contributionDays']):
                        if day['contributionCount'] > 0:
                            matrix[c][r] = 1
        except Exception as e:
            print(f"GraphQL fallback: {e}")
            
    # Ensure clear line
    for c in range(cols):
        matrix[c][3] = 1
        
    return matrix

# --- SVG GENERATORS matching exact #000000 / #111111 design system ---

def gen_terminal_svg():
    commits = get_recent_commits()
    while len(commits) < 3:
        commits.append(("System", "0000000", "chore: automated telemetry synchronization"))
    
    formatted_commits = []
    for repo, sha, msg in commits:
        repo_esc = repo.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        sha_esc = sha.replace('&', '&amp;').replace('<', '&lt;')
        msg_esc = msg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        formatted_commits.append((repo_esc, sha_esc, msg_esc))

    c1, c2, c3 = formatted_commits

    return f'''<svg viewBox="0 0 1000 420" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Live Hacker Terminal">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .bg {{ fill: #000000; }}
    .card {{ fill: #111111; stroke: #30363D; stroke-width: 1.5; }}
    
    .cyan {{ fill: #58A6FF; }}
    .green {{ fill: #39D353; }}
    .purple {{ fill: #BC8CFF; }}
    .yellow {{ fill: #E3B341; }}
    .gray {{ fill: #8B949E; }}
    .white {{ fill: #FFFFFF; }}
    .dim {{ fill: #484F58; }}
    
    .cursor {{ fill: #39D353; animation: blink 1s step-end infinite; }}
    .pulse-dot {{ animation: pulse 2s ease-in-out infinite; }}

    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.9); }}
    }}
    
    .tab-active {{ fill: #1C2128; stroke: #58A6FF; stroke-width: 1; }}
    .tab-inactive {{ fill: #111111; stroke: #30363D; stroke-width: 1; opacity: 0.7; }}
  </style>

  <!-- Black outer canvas matching Garv design system -->
  <rect width="1000" height="420" class="bg"/>
  
  <!-- Outer Card Frame aligned with x=48 width=904 -->
  <rect x="48" y="20" width="904" height="380" rx="8" class="card"/>
  
  <!-- Window Header Bar -->
  <circle cx="72" cy="42" r="5.5" fill="#FF5F56"/>
  <circle cx="92" cy="42" r="5.5" fill="#FFBD2E"/>
  <circle cx="112" cy="42" r="5.5" fill="#27C93F"/>
  
  <!-- Navigation Tabs -->
  <rect x="140" y="28" width="160" height="26" rx="4" class="tab-active"/>
  <text x="220" y="45" fill="#58A6FF" class="mono" font-size="12" text-anchor="middle" font-weight="800">⚡ system_status.sh</text>
  
  <rect x="310" y="28" width="140" height="26" rx="4" class="tab-inactive"/>
  <text x="380" y="45" fill="#8B949E" class="mono" font-size="12" text-anchor="middle" font-weight="600">📊 git_stream.log</text>

  <rect x="460" y="28" width="140" height="26" rx="4" class="tab-inactive"/>
  <text x="530" y="45" fill="#8B949E" class="mono" font-size="12" text-anchor="middle" font-weight="600">🧠 ml_core.py</text>
  
  <text fill="#484F58" class="mono" x="928" y="45" font-size="11" text-anchor="end">garvnanda@developer-station</text>
  <line x1="48" y1="62" x2="952" y2="62" stroke="#30363D" stroke-width="1.5"/>

  <!-- NEOFETCH / SYSTEM STATS PANEL -->
  <g class="mono" font-size="13">
    <!-- Left ASCII Art Badge -->
    <g font-size="11" font-weight="900">
      <text x="72" y="92" fill="#58A6FF">█▀▀ █▀█ █▀█ █ █ █ █▄ █ █▀█ █▀ me</text>
      <text x="72" y="108" fill="#39D353">█▄█ █▀█ █▀▄ ▀▄▀ █ █ █ ▀█ █▀█ █▄</text>
      <text x="72" y="124" fill="#BC8CFF">==============================</text>
    </g>

    <!-- System Metadata Grid -->
    <text x="360" y="92" class="purple" font-weight="800">USER:</text>
    <text x="430" y="92" class="white" font-weight="600">Garv Nanda (@Garvnanda)</text>

    <text x="360" y="112" class="purple" font-weight="800">ROLE:</text>
    <text x="430" y="112" class="yellow" font-weight="600">ML Architect &amp; Backend Engineer</text>

    <text x="360" y="132" class="purple" font-weight="800">CORE:</text>
    <text x="430" y="132" class="green" font-weight="600">Python • PyTorch • FastAPI • C++ • TypeScript</text>

    <text x="740" y="92" class="cyan" font-weight="800">STATUS:</text>
    <circle cx="815" cy="88" r="4.5" fill="#39D353" class="pulse-dot"/>
    <text x="828" y="92" class="green" font-weight="800">ONLINE</text>

    <text x="740" y="112" class="cyan" font-weight="800">SHELL:</text>
    <text x="815" y="112" class="gray" font-weight="600">zsh 5.9 (x86_64)</text>

    <text x="740" y="132" class="cyan" font-weight="800">UPTIME:</text>
    <text x="815" y="132" class="white" font-weight="600">99.9% (Active Commits)</text>
  </g>

  <line x1="72" y1="152" x2="928" y2="152" stroke="#21262D" stroke-width="1" stroke-dasharray="4"/>

  <!-- RECENT LIVE GIT LOG FEED -->
  <g class="mono" font-size="13">
    <!-- Command Prompt -->
    <text x="72" y="184" class="green" font-weight="800">➜</text>
    <text x="92" y="184" class="cyan" font-weight="800">~/workspace</text>
    <text x="195" y="184" class="white" font-weight="800">git log --oneline --graph -n 3</text>

    <!-- Commit 1 -->
    <text x="72" y="218" class="purple">*</text>
    <text x="88" y="218" class="yellow" font-weight="800">{c1[1]}</text>
    <rect x="155" y="204" width="110" height="20" rx="4" fill="#161B22" stroke="#30363D"/>
    <text x="210" y="218" class="cyan" font-size="11" font-weight="800" text-anchor="middle">[{c1[0]}]</text>
    <text x="275" y="218" class="white" font-weight="500">{c1[2]}</text>

    <!-- Commit 2 -->
    <text x="72" y="250" class="purple">*</text>
    <text x="88" y="250" class="yellow" font-weight="800">{c2[1]}</text>
    <rect x="155" y="236" width="110" height="20" rx="4" fill="#161B22" stroke="#30363D"/>
    <text x="210" y="250" class="cyan" font-size="11" font-weight="800" text-anchor="middle">[{c2[0]}]</text>
    <text x="275" y="250" class="white" font-weight="500">{c2[2]}</text>

    <!-- Commit 3 -->
    <text x="72" y="282" class="purple">*</text>
    <text x="88" y="282" class="yellow" font-weight="800">{c3[1]}</text>
    <rect x="155" y="268" width="110" height="20" rx="4" fill="#161B22" stroke="#30363D"/>
    <text x="210" y="282" class="cyan" font-size="11" font-weight="800" text-anchor="middle">[{c3[0]}]</text>
    <text x="275" y="282" class="white" font-weight="500">{c3[2]}</text>
  </g>

  <line x1="72" y1="305" x2="928" y2="305" stroke="#21262D" stroke-width="1"/>

  <!-- ACTIVE INPUT PROMPT LINE -->
  <g class="mono" font-size="13">
    <text x="72" y="334" class="green" font-weight="800">➜</text>
    <text x="92" y="334" class="purple" font-weight="800">garvnanda@system:~$</text>
    <text x="260" y="334" class="white" font-weight="800">./run_pipeline.sh --watch --live-telemetry</text>
    <rect x="650" y="321" width="9" height="17" class="cursor"/>
  </g>

  <!-- BOTTOM TERMINAL FOOTER BAR -->
  <rect x="48" y="360" width="904" height="40" rx="0" fill="#0D1117"/>
  <rect x="48" y="360" width="904" height="1" fill="#30363D"/>
  <g class="mono" font-size="11">
    <text x="72" y="384" class="green" font-weight="800">NORMAL</text>
    <text x="140" y="384" class="gray" font-weight="600">main*</text>
    <text x="190" y="384" class="dim">|</text>
    <text x="205" y="384" class="cyan" font-weight="600">utf-8</text>
    <text x="250" y="384" class="dim">|</text>
    <text x="265" y="384" class="yellow" font-weight="600">python 3.10.12</text>
    <text x="370" y="384" class="dim">|</text>
    <text x="385" y="384" class="purple" font-weight="600">latency: 12ms</text>
    
    <text x="928" y="384" class="gray" font-weight="600" text-anchor="end">100%  420:1</text>
  </g>
</svg>'''

def gen_constellation_svg():
    repos = get_top_repos()
    
    # Center coordinates inside viewBox 0 0 1000 420
    # Card is x=48 y=20 width=904 height=380
    center_x, center_y = 500, 210
    nodes = []
    
    # Inner Orbit (3 repos) - Radius 95px
    r_inner = 95
    for i in range(min(3, len(repos))):
        angle = (i * (360/3) - 90) * (math.pi/180) # -90° starts at top
        x = center_x + r_inner * math.cos(angle)
        y = center_y + r_inner * math.sin(angle)
        nodes.append((repos[i][0], x, y))

    # Outer Orbit (3 repos) - Radius 150px
    r_outer = 150
    for i in range(3, len(repos)):
        angle = ((i-3) * (360/3) + 30) * (math.pi/180) # Offset for constellation symmetry
        x = center_x + r_outer * math.cos(angle)
        y = center_y + r_outer * math.sin(angle)
        nodes.append((repos[i][0], x, y))

    lines_svg = ""
    nodes_svg = ""
    for idx, (name, x, y) in enumerate(nodes):
        # Dashed constellation connection line to center
        lines_svg += f'<line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" stroke="#30363D" stroke-width="1.5" stroke-dasharray="4 4"/>'
        
        delay = idx * 0.4
        name_esc = name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Calculate text badge offset (badge below node dot)
        badge_w = len(name) * 8 + 24
        badge_x = x - badge_w / 2
        badge_y = y + 16
        
        nodes_svg += f'''
        <g class="node-group" style="animation-delay: {delay}s; transform-origin: {x}px {y}px;">
            <!-- Outer Glow Aura -->
            <circle cx="{x}" cy="{y}" r="18" fill="#58A6FF" opacity="0.15" filter="blur(4px)"/>
            <!-- Main Node Dot -->
            <circle cx="{x}" cy="{y}" r="9" fill="#1F6FEB" stroke="#58A6FF" stroke-width="2"/>
            <circle cx="{x}" cy="{y}" r="3" fill="#FFFFFF"/>
            
            <!-- Repository Text Badge Box (prevents text clipping and background overlap) -->
            <rect x="{badge_x}" y="{badge_y}" width="{badge_w}" height="24" rx="4" fill="#161B22" stroke="#30363D" stroke-width="1"/>
            <text x="{x}" y="{badge_y + 16}" fill="#FFFFFF" class="mono" font-size="12" font-weight="800" text-anchor="middle">{name_esc}</text>
        </g>
        '''

    return f'''<svg viewBox="0 0 1000 420" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ecosystem Constellation">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .bg {{ fill: #000000; }}
    .card {{ fill: #111111; stroke: #30363D; stroke-width: 1.5; }}
    
    .node-group {{ animation: float 4s ease-in-out infinite; transition: transform 0.3s; }}
    .node-group:hover {{ transform: scale(1.12); cursor: pointer; }}
    
    @keyframes float {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-6px); }}
    }}
    
    .center-pulse {{ animation: pulse 3s infinite; transform-origin: {center_x}px {center_y}px; }}
    @keyframes pulse {{
      0% {{ transform: scale(1); opacity: 0.5; }}
      50% {{ transform: scale(1.35); opacity: 0.15; }}
      100% {{ transform: scale(1); opacity: 0.5; }}
    }}
  </style>
  
  <!-- Black canvas matching Garv design system -->
  <rect width="1000" height="420" class="bg"/>
  
  <!-- Outer Card Frame aligned with x=48 width=904 -->
  <rect x="48" y="20" width="904" height="380" rx="8" class="card"/>
  
  <!-- Header Title -->
  <text fill="#FFFFFF" class="mono" x="72" y="56" font-size="16" font-weight="800" letter-spacing="1">LIVE ECOSYSTEM CONSTELLATION 🌌</text>
  <text fill="#8B949E" class="mono" x="928" y="56" font-size="12" font-weight="600" text-anchor="end">REAL-TIME REPOSITORY GRAPH</text>
  <line x1="72" y1="70" x2="928" y2="70" stroke="#30363D" stroke-width="1"/>

  <!-- Orbits & Connections -->
  <g>
    <!-- Orbit Guide Circles -->
    <circle cx="{center_x}" cy="{center_y}" r="95" stroke="#21262D" stroke-width="1" stroke-dasharray="3 3" fill="none"/>
    <circle cx="{center_x}" cy="{center_y}" r="150" stroke="#21262D" stroke-width="1" stroke-dasharray="3 3" fill="none"/>

    {lines_svg}

    <!-- Center Node (Garv Nanda) -->
    <circle cx="{center_x}" cy="{center_y}" r="40" fill="#39D353" class="center-pulse"/>
    <circle cx="{center_x}" cy="{center_y}" r="22" fill="#238636" stroke="#FFFFFF" stroke-width="2.5"/>
    
    <!-- Center Label Badge -->
    <rect x="{center_x - 65}" y="{center_y + 30}" width="130" height="26" rx="4" fill="#0D1117" stroke="#238636" stroke-width="1.5"/>
    <text x="{center_x}" y="{center_y + 47}" fill="#39D353" class="mono" font-size="13" text-anchor="middle" font-weight="800">@Garvnanda</text>
    
    {nodes_svg}
  </g>
</svg>'''

def gen_maze_svg():
    matrix = get_contribution_matrix()
    
    walls = ""
    paths = ""
    
    for c in range(52):
        for r in range(7):
            x = 72 + c * 16.2
            y = 88 + r * 16.5
            if matrix[c][r] == 0:
                walls += f'<rect x="{x}" y="{y}" width="12.5" height="12.5" rx="2" class="wall-rect" />'
            else:
                paths += f'<rect x="{x}" y="{y}" width="12.5" height="12.5" rx="2" class="path-rect" />'
                
    return f'''<svg viewBox="0 0 1000 240" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Commit Hover Maze">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .bg {{ fill: #000000; }}
    .card {{ fill: #111111; stroke: #30363D; stroke-width: 1.5; }}
    
    .wall-rect {{ fill: #161B22; cursor: crosshair; }}
    .path-rect {{ fill: #238636; opacity: 0.85; cursor: crosshair; }}
    .path-rect:hover {{ opacity: 1; fill: #39D353; stroke: #FFFFFF; stroke-width: 1; }}
    
    .walls {{ pointer-events: auto; }}
    .walls:hover ~ .game-over {{ opacity: 1; pointer-events: auto; }}
    .goal:hover ~ .win {{ opacity: 1; pointer-events: auto; }}
    
    .game-over {{ opacity: 0; transition: opacity 0.2s; pointer-events: none; }}
    .win {{ opacity: 0; transition: opacity 0.2s; pointer-events: none; }}
  </style>
  
  <!-- Black canvas matching Garv design system -->
  <rect width="1000" height="240" class="bg"/>
  
  <!-- Outer Card Frame aligned with x=48 width=904 -->
  <rect x="48" y="16" width="904" height="208" rx="8" class="card"/>
  
  <text fill="#FFFFFF" class="mono" x="72" y="44" font-size="16" font-weight="800" letter-spacing="1">HOVER MAZE: NAVIGATE THE COMMITS 🕹️</text>
  <text fill="#8B949E" class="mono" x="928" y="44" font-size="12" font-weight="600" text-anchor="end">TRACE FROM LEFT TO RIGHT WITHOUT TOUCHING WALLS</text>
  <line x1="72" y1="56" x2="928" y2="56" stroke="#30363D" stroke-width="1"/>

  <text fill="#58A6FF" class="mono" x="22" y="140" font-size="11" font-weight="800" transform="rotate(-90, 22, 140)">START ➔</text>
  <text fill="#39D353" class="mono" x="978" y="140" font-size="11" font-weight="800" transform="rotate(90, 978, 140)">GOAL</text>

  <g class="paths">
    {paths}
  </g>
  
  <g class="walls">
    <rect x="48" y="56" width="904" height="26" fill="transparent" class="wall-rect" />
    <rect x="48" y="203" width="904" height="21" fill="transparent" class="wall-rect" />
    {walls}
  </g>
  
  <rect x="918" y="125" width="30" height="35" fill="transparent" class="goal"/>

  <g class="game-over">
    <rect x="48" y="57" width="904" height="166" fill="rgba(218, 54, 51, 0.95)" />
    <text x="500" y="130" fill="#FFFFFF" class="mono" font-size="28" font-weight="900" text-anchor="middle">⚠️ SYSTEM FAILURE / WALL TOUCHED ⚠️</text>
    <text x="500" y="165" fill="#FFFFFF" class="mono" font-size="14" font-weight="600" text-anchor="middle">Move cursor outside the window frame to reset system.</text>
  </g>
  
  <g class="win">
    <rect x="48" y="57" width="904" height="166" fill="rgba(35, 134, 54, 0.95)" />
    <text x="500" y="130" fill="#FFFFFF" class="mono" font-size="28" font-weight="900" text-anchor="middle">🎉 PAYLOAD DELIVERED / YOU WIN! 🎉</text>
    <text x="500" y="165" fill="#FFFFFF" class="mono" font-size="14" font-weight="600" text-anchor="middle">Garv Nanda's repository core successfully unlocked.</text>
  </g>
</svg>'''

if __name__ == "__main__":
    assets_dir = "c:/Projects/Garvnanda/Garvnanda/assets/dynamic"
    dark_dir = "c:/Projects/Garvnanda/Garvnanda/assets/dark/dynamic"
    
    term_svg = gen_terminal_svg()
    const_svg = gen_constellation_svg()
    maze_svg = gen_maze_svg()
    
    create_svg(os.path.join(assets_dir, "terminal.svg"), term_svg)
    create_svg(os.path.join(assets_dir, "constellation.svg"), const_svg)
    create_svg(os.path.join(assets_dir, "maze.svg"), maze_svg)
    
    create_svg(os.path.join(dark_dir, "terminal.svg"), term_svg)
    create_svg(os.path.join(dark_dir, "constellation.svg"), const_svg)
    create_svg(os.path.join(dark_dir, "maze.svg"), maze_svg)
    
    print("All dynamic SVGs re-aligned 100% to Garv's design system!")
