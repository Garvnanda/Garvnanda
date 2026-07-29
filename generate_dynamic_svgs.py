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
        ("Galla-Sathi", "a8f3b92", "feat(voice): ASR dispatcher & real-time audio pipeline"),
        ("SANN", "4c11e02", "fix(ai-safety): neural poisoning defense evaluation threshold"),
        ("DebateMind", "99f6e64", "refactor(nlp): argument graph transformer model weights")
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
    
    curr_r = 3
    for c in range(cols):
        matrix[c][curr_r] = 1
        if c < cols - 1:
            moves = [0]
            if curr_r > 1: moves.append(-1)
            if curr_r < rows - 2: moves.append(1)
            curr_r += random.choice(moves)
            matrix[c][curr_r] = 1
            
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
            
    for c in range(cols):
        matrix[c][3] = 1
        
    return matrix

# --- CLEAN, SLEEK TERMINAL GENERATOR ---
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

    return f'''<svg viewBox="0 0 1000 270" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Live Developer Terminal">
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
    
    .cursor {{ fill: #39D353; animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
  </style>

  <!-- Pitch Black outer background matching Garv design system -->
  <rect width="1000" height="270" class="bg"/>
  
  <!-- Sleek Outer Card Frame -->
  <rect x="48" y="20" width="904" height="230" rx="8" class="card"/>
  
  <!-- Terminal Window Header -->
  <circle cx="72" cy="42" r="5.5" fill="#FF5F56"/>
  <circle cx="92" cy="42" r="5.5" fill="#FFBD2E"/>
  <circle cx="112" cy="42" r="5.5" fill="#27C93F"/>
  <text fill="#8B949E" class="mono" x="500" y="46" font-size="12" font-weight="600" text-anchor="middle">garvnanda@developer-station: ~/workspace</text>
  <line x1="48" y1="62" x2="952" y2="62" stroke="#30363D" stroke-width="1.5"/>

  <!-- CLEAN TERMINAL CONTENT -->
  <g class="mono" font-size="13">
    <!-- Command Prompt 1 -->
    <text x="72" y="94" class="green" font-weight="800">➜</text>
    <text x="92" y="94" class="purple" font-weight="800">garvnanda@system:~$</text>
    <text x="250" y="94" class="white" font-weight="700">git log --oneline -n 3</text>

    <!-- Commit Line 1 -->
    <text x="92" y="125" class="yellow" font-weight="800">{c1[1]}</text>
    <text x="162" y="125" class="cyan" font-weight="800">[{c1[0]}]</text>
    <text x="280" y="125" class="white" font-weight="500">{c1[2]}</text>

    <!-- Commit Line 2 -->
    <text x="92" y="152" class="yellow" font-weight="800">{c2[1]}</text>
    <text x="162" y="152" class="cyan" font-weight="800">[{c2[0]}]</text>
    <text x="280" y="152" class="white" font-weight="500">{c2[2]}</text>

    <!-- Commit Line 3 -->
    <text x="92" y="179" class="yellow" font-weight="800">{c3[1]}</text>
    <text x="162" y="179" class="cyan" font-weight="800">[{c3[0]}]</text>
    <text x="280" y="179" class="white" font-weight="500">{c3[2]}</text>

    <!-- Active Command Prompt with Cursor -->
    <text x="72" y="215" class="green" font-weight="800">➜</text>
    <text x="92" y="215" class="purple" font-weight="800">garvnanda@system:~$</text>
    <text x="250" y="215" class="white" font-weight="700">python -m ml_core.deploy --live-telemetry</text>
    <rect x="585" y="202" width="9" height="17" class="cursor"/>
  </g>
</svg>'''

def gen_constellation_svg():
    repos = get_top_repos()
    center_x, center_y = 500, 210
    nodes = []
    
    r_inner = 95
    for i in range(min(3, len(repos))):
        angle = (i * (360/3) - 90) * (math.pi/180)
        x = center_x + r_inner * math.cos(angle)
        y = center_y + r_inner * math.sin(angle)
        nodes.append((repos[i][0], x, y))

    r_outer = 150
    for i in range(3, len(repos)):
        angle = ((i-3) * (360/3) + 30) * (math.pi/180)
        x = center_x + r_outer * math.cos(angle)
        y = center_y + r_outer * math.sin(angle)
        nodes.append((repos[i][0], x, y))

    lines_svg = ""
    nodes_svg = ""
    for idx, (name, x, y) in enumerate(nodes):
        lines_svg += f'<line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" stroke="#30363D" stroke-width="1.5" stroke-dasharray="4 4"/>'
        delay = idx * 0.4
        name_esc = name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        badge_w = len(name) * 8 + 24
        badge_x = x - badge_w / 2
        badge_y = y + 16
        
        nodes_svg += f'''
        <g class="node-group" style="animation-delay: {delay}s; transform-origin: {x}px {y}px;">
            <circle cx="{x}" cy="{y}" r="18" fill="#58A6FF" opacity="0.15" filter="blur(4px)"/>
            <circle cx="{x}" cy="{y}" r="9" fill="#1F6FEB" stroke="#58A6FF" stroke-width="2"/>
            <circle cx="{x}" cy="{y}" r="3" fill="#FFFFFF"/>
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

  <rect width="1000" height="420" class="bg"/>
  <rect x="48" y="20" width="904" height="380" rx="8" class="card"/>
  
  <text fill="#FFFFFF" class="mono" x="72" y="56" font-size="16" font-weight="800" letter-spacing="1">LIVE ECOSYSTEM CONSTELLATION 🌌</text>
  <text fill="#8B949E" class="mono" x="928" y="56" font-size="12" font-weight="600" text-anchor="end">REAL-TIME REPOSITORY GRAPH</text>
  <line x1="72" y1="70" x2="928" y2="70" stroke="#30363D" stroke-width="1"/>

  <g>
    <circle cx="{center_x}" cy="{center_y}" r="95" stroke="#21262D" stroke-width="1" stroke-dasharray="3 3" fill="none"/>
    <circle cx="{center_x}" cy="{center_y}" r="150" stroke="#21262D" stroke-width="1" stroke-dasharray="3 3" fill="none"/>

    {lines_svg}

    <circle cx="{center_x}" cy="{center_y}" r="40" fill="#39D353" class="center-pulse"/>
    <circle cx="{center_x}" cy="{center_y}" r="22" fill="#238636" stroke="#FFFFFF" stroke-width="2.5"/>
    <rect x="{center_x - 65}" y="{center_y + 30}" width="130" height="26" rx="4" fill="#0D1117" stroke="#238636" stroke-width="1.5"/>
    <text x="{center_x}" y="{center_y + 47}" fill="#39D353" class="mono" font-size="13" text-anchor="middle" font-weight="800">@Garvnanda</text>
    
    {nodes_svg}
  </g>
</svg>'''

if __name__ == "__main__":
    assets_dir = "c:/Projects/Garvnanda/Garvnanda/assets/dynamic"
    dark_dir = "c:/Projects/Garvnanda/Garvnanda/assets/dark/dynamic"
    
    term_svg = gen_terminal_svg()
    const_svg = gen_constellation_svg()
    
    create_svg(os.path.join(assets_dir, "terminal.svg"), term_svg)
    create_svg(os.path.join(assets_dir, "constellation.svg"), const_svg)
    
    create_svg(os.path.join(dark_dir, "terminal.svg"), term_svg)
    create_svg(os.path.join(dark_dir, "constellation.svg"), const_svg)
    
    print("Clean terminal & constellation SVGs generated!")
