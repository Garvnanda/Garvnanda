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
    if not GITHUB_TOKEN:
        return [
            "feat(ai): upgraded neural safety thresholds in SANN",
            "fix(backend): optimized FastAPI latency for Galla-Sathi",
            "chore(web3): deployed Creator_X smart contracts"
        ]
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    try:
        res = requests.get(f"https://api.github.com/users/{USERNAME}/events/public", headers=headers)
        if res.status_code == 200:
            commits = []
            for event in res.json():
                if event['type'] == 'PushEvent':
                    for commit in event['payload']['commits']:
                        msg = commit['message'].split('\\n')[0][:50]
                        commits.append(msg)
                        if len(commits) == 3:
                            return commits
        return commits if commits else ["Committed recent updates to main branch"] * 3
    except:
        return ["feat: optimized infrastructure", "fix: resolved critical bugs", "docs: updated architecture"]

def get_top_repos():
    if not GITHUB_TOKEN:
        return [
            ("Galla-Sathi", 150), ("SANN", 120), ("DevLens", 95), 
            ("DebateMind", 80), ("DATATHON-2026", 65), ("CREATOR_X", 40)
        ]
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    try:
        res = requests.get(f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=10", headers=headers)
        if res.status_code == 200:
            repos = [(r['name'], r['stargazers_count'] * 10 + r['size'] % 100) for r in res.json() if not r['fork']]
            return repos[:6]
    except:
        pass
    return [("Repo_A", 100), ("Repo_B", 80), ("Repo_C", 60), ("Repo_D", 40)]

def get_contribution_matrix():
    # Fallback random matrix that guarantees a path
    cols, rows = 52, 7
    matrix = [[0 for _ in range(rows)] for _ in range(cols)]
    
    # Generate a random path
    curr_r = 3
    for c in range(cols):
        matrix[c][curr_r] = 1 # path
        if c < cols - 1:
            moves = [0]
            if curr_r > 1: moves.append(-1)
            if curr_r < rows - 2: moves.append(1)
            curr_r += random.choice(moves)
            matrix[c][curr_r] = 1 # path
            
    # Add random noise
    for c in range(cols):
        for r in range(rows):
            if matrix[c][r] == 0 and random.random() > 0.8:
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
        except:
            pass
            
    # Ensure a guaranteed path exists by brute forcing a clear line if needed
    for c in range(cols):
        matrix[c][3] = 1
        
    return matrix

# --- SVG GENERATORS ---
def gen_terminal_svg():
    commits = get_recent_commits()
    while len(commits) < 3:
        commits.append("...")
    
    # Escape XML chars
    c1, c2, c3 = [c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for c in commits]

    return f'''<svg viewBox="0 0 1000 240" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Live Terminal">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
    .bg {{ fill: #0D1117; }}
    .card {{ fill: #161B22; stroke: #30363D; stroke-width: 1.5; }}
    .prompt {{ fill: #39D353; font-weight: bold; }}
    .text {{ fill: #C9D1D9; }}
    
    /* Typing Animation */
    .line1, .line2, .line3 {{ opacity: 0; }}
    .line1 {{ animation: type1 12s infinite; }}
    .line2 {{ animation: type2 12s infinite; }}
    .line3 {{ animation: type3 12s infinite; }}
    .cursor {{ fill: #C9D1D9; animation: blink 1s step-end infinite; }}
    
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes type1 {{
      0%, 10% {{ opacity: 0; }}
      11%, 30% {{ opacity: 1; }}
      31%, 100% {{ opacity: 0; }}
    }}
    @keyframes type2 {{
      0%, 33% {{ opacity: 0; }}
      34%, 60% {{ opacity: 1; }}
      61%, 100% {{ opacity: 0; }}
    }}
    @keyframes type3 {{
      0%, 63% {{ opacity: 0; }}
      64%, 90% {{ opacity: 1; }}
      91%, 100% {{ opacity: 0; }}
    }}
  </style>

  <rect width="1000" height="240" rx="8" class="bg"/>
  <rect x="48" y="10" width="904" height="220" rx="8" class="card"/>
  
  <!-- Terminal Header -->
  <circle cx="70" cy="28" r="5" fill="#FF5F56"/>
  <circle cx="90" cy="28" r="5" fill="#FFBD2E"/>
  <circle cx="110" cy="28" r="5" fill="#27C93F"/>
  <text fill="#8B949E" class="mono" x="500" y="32" font-size="12" text-anchor="middle">Garvnanda@system: ~/workspace</text>
  <line x1="48" y1="45" x2="952" y2="45" stroke="#30363D" stroke-width="1.5"/>

  <g font-size="16" class="mono">
    <!-- Line 1 -->
    <g class="line1">
      <text x="70" y="85" class="prompt">➜</text>
      <text x="95" y="85" class="text" font-weight="bold" fill="#58A6FF">git log --oneline -n 1</text>
      <text x="70" y="115" class="text">{c1}</text>
      <rect x="70" y="125" width="10" height="18" class="cursor"/>
    </g>
    <!-- Line 2 -->
    <g class="line2">
      <text x="70" y="85" class="prompt">➜</text>
      <text x="95" y="85" class="text" font-weight="bold" fill="#58A6FF">git log --oneline -n 1</text>
      <text x="70" y="115" class="text">{c2}</text>
      <rect x="70" y="125" width="10" height="18" class="cursor"/>
    </g>
    <!-- Line 3 -->
    <g class="line3">
      <text x="70" y="85" class="prompt">➜</text>
      <text x="95" y="85" class="text" font-weight="bold" fill="#58A6FF">git log --oneline -n 1</text>
      <text x="70" y="115" class="text">{c3}</text>
      <rect x="70" y="125" width="10" height="18" class="cursor"/>
    </g>
  </g>
</svg>'''

def gen_constellation_svg():
    repos = get_top_repos()
    
    # Orbits
    center = (500, 160)
    nodes = []
    
    # Inner orbit (first 3)
    r_inner = 80
    for i in range(min(3, len(repos))):
        angle = (i * (360/3)) * (math.pi/180)
        x = center[0] + r_inner * math.cos(angle)
        y = center[1] + r_inner * math.sin(angle)
        nodes.append((repos[i][0], x, y, 40 + (repos[i][1]%30)))

    # Outer orbit (next 3)
    r_outer = 160
    for i in range(3, len(repos)):
        angle = ((i-3) * (360/3) + 60) * (math.pi/180)
        x = center[0] + r_outer * math.cos(angle)
        y = center[1] + r_outer * math.sin(angle)
        nodes.append((repos[i][0], x, y, 30 + (repos[i][1]%20)))

    lines_svg = ""
    nodes_svg = ""
    for idx, (name, x, y, r) in enumerate(nodes):
        # Line to center
        lines_svg += f'<line x1="500" y1="160" x2="{x}" y2="{y}" stroke="rgba(88,166,255,0.3)" stroke-width="2" stroke-dasharray="4"/>'
        # Nodes
        delay = idx * 0.5
        name_esc = name.replace('&', '&amp;').replace('<', '&lt;')
        nodes_svg += f'''
        <g class="node" style="animation-delay: {delay}s; transform-origin: {x}px {y}px;">
            <circle cx="{x}" cy="{y}" r="{r/2}" fill="#0969DA" opacity="0.3" filter="blur(4px)"/>
            <circle cx="{x}" cy="{y}" r="{r/3}" fill="#58A6FF" stroke="#FFFFFF" stroke-width="1.5"/>
            <text x="{x}" y="{y+r/3+15}" fill="#C9D1D9" font-size="12" text-anchor="middle" font-weight="bold">{name_esc}</text>
        </g>
        '''

    return f'''<svg viewBox="0 0 1000 320" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ecosystem Constellation">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
    .bg {{ fill: #0D1117; }}
    .card {{ fill: #161B22; stroke: #30363D; stroke-width: 1.5; }}
    .node {{ animation: float 4s ease-in-out infinite; transition: transform 0.3s; }}
    .node:hover {{ transform: scale(1.1); cursor: pointer; }}
    @keyframes float {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-8px); }}
    }}
    .center-pulse {{ animation: pulse 3s infinite; }}
    @keyframes pulse {{
      0% {{ transform: scale(1); opacity: 0.8; }}
      50% {{ transform: scale(1.2); opacity: 0.4; }}
      100% {{ transform: scale(1); opacity: 0.8; }}
    }}
  </style>
  
  <rect width="1000" height="320" rx="8" class="bg"/>
  <rect x="48" y="10" width="904" height="300" rx="8" class="card"/>
  
  <text fill="#FFFFFF" class="mono" x="72" y="44" font-size="16" font-weight="800" letter-spacing="1">LIVE ECOSYSTEM CONSTELLATION 🌌</text>
  <line x1="72" y1="56" x2="928" y2="56" stroke="#30363D" stroke-width="1"/>

  <g>
    {lines_svg}
    <!-- Center Node (Garv) -->
    <circle cx="500" cy="160" r="30" fill="#39D353" opacity="0.2" class="center-pulse" style="transform-origin: 500px 160px;"/>
    <circle cx="500" cy="160" r="20" fill="#26A641" stroke="#FFFFFF" stroke-width="2"/>
    <text x="500" y="200" fill="#FFFFFF" class="mono" font-size="14" text-anchor="middle" font-weight="bold">@Garvnanda</text>
    
    {nodes_svg}
  </g>
</svg>'''

def gen_maze_svg():
    matrix = get_contribution_matrix()
    
    # Build grid SVG
    rects = ""
    # We put walls in one group to track hover
    walls = ""
    paths = ""
    
    for c in range(52):
        for r in range(7):
            x = 60 + c * 17
            y = 80 + r * 17
            if matrix[c][r] == 0:
                walls += f'<rect x="{x}" y="{y}" width="13" height="13" rx="2" class="wall-rect" />'
            else:
                paths += f'<rect x="{x}" y="{y}" width="13" height="13" rx="2" class="path-rect" />'
                
    return f'''<svg viewBox="0 0 1000 240" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Commit Hover Maze">
  <style>
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, monospace; }}
    .bg {{ fill: #0D1117; }}
    .card {{ fill: #161B22; stroke: #30363D; stroke-width: 1.5; }}
    
    .wall-rect {{ fill: #101217; cursor: crosshair; }}
    .path-rect {{ fill: #26A641; opacity: 0.7; cursor: crosshair; }}
    .path-rect:hover {{ opacity: 1; fill: #39D353; }}
    
    /* The core mechanics */
    .walls {{ pointer-events: auto; }}
    .walls:hover ~ .game-over {{ opacity: 1; pointer-events: auto; }}
    .goal:hover ~ .win {{ opacity: 1; pointer-events: auto; }}
    
    .game-over {{ opacity: 0; transition: opacity 0.2s; pointer-events: none; }}
    .win {{ opacity: 0; transition: opacity 0.2s; pointer-events: none; }}
  </style>
  
  <rect width="1000" height="240" rx="8" class="bg"/>
  <rect x="48" y="10" width="904" height="220" rx="8" class="card"/>
  
  <text fill="#FFFFFF" class="mono" x="72" y="44" font-size="16" font-weight="800" letter-spacing="1">HOVER MAZE: NAVIGATE THE COMMITS</text>
  <text fill="#8B949E" class="mono" x="928" y="44" font-size="12" font-weight="600" text-anchor="end">TRACE FROM LEFT TO RIGHT WITHOUT TOUCHING WALLS</text>
  <line x1="72" y1="56" x2="928" y2="56" stroke="#30363D" stroke-width="1"/>

  <text fill="#58A6FF" class="mono" x="20" y="140" font-size="12" font-weight="bold" transform="rotate(-90, 20, 140)">START ➔</text>
  <text fill="#39D353" class="mono" x="970" y="140" font-size="12" font-weight="bold" transform="rotate(90, 970, 140)">GOAL</text>

  <!-- Render paths underneath so walls are on top for hover detection -->
  <g class="paths">
    {paths}
  </g>
  
  <g class="walls">
    <!-- Huge invisible walls on top and bottom to prevent cheating -->
    <rect x="48" y="56" width="904" height="22" fill="transparent" class="wall-rect" />
    <rect x="48" y="200" width="904" height="30" fill="transparent" class="wall-rect" />
    
    {walls}
  </g>
  
  <!-- Goal node -->
  <rect x="944" y="120" width="20" height="40" fill="transparent" class="goal"/>

  <!-- Overlay Screens -->
  <g class="game-over">
    <rect x="48" y="57" width="904" height="172" rx="0" fill="rgba(255,0,0,0.9)" />
    <text x="500" y="140" fill="#FFFFFF" class="mono" font-size="32" font-weight="bold" text-anchor="middle">SYSTEM FAILURE / WALL TOUCHED</text>
    <text x="500" y="170" fill="#FFFFFF" class="mono" font-size="16" text-anchor="middle">Move mouse outside to reset.</text>
  </g>
  
  <g class="win">
    <rect x="48" y="57" width="904" height="172" rx="0" fill="rgba(38,166,65,0.9)" />
    <text x="500" y="140" fill="#FFFFFF" class="mono" font-size="32" font-weight="bold" text-anchor="middle">PAYLOAD DELIVERED / YOU WIN</text>
  </g>
</svg>'''

if __name__ == "__main__":
    assets_dir = "c:/Projects/Garvnanda/Garvnanda/assets/dynamic"
    create_svg(os.path.join(assets_dir, "terminal.svg"), gen_terminal_svg())
    create_svg(os.path.join(assets_dir, "constellation.svg"), gen_constellation_svg())
    create_svg(os.path.join(assets_dir, "maze.svg"), gen_maze_svg())
    print("Dynamic SVGs generated successfully!")
