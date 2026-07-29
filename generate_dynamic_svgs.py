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

    return f'''<svg viewBox="0 0 1000 240" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Live Hacker Terminal">
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

  <!-- Black canvas matching Garv design system -->
  <rect width="1000" height="240" class="bg"/>
  
  <!-- Outer Card Frame aligned with x=48 width=904 -->
  <rect x="48" y="20" width="904" height="200" rx="8" class="card"/>
  
  <!-- Window Header Bar -->
  <circle cx="72" cy="42" r="5.5" fill="#FF5F56"/>
  <circle cx="92" cy="42" r="5.5" fill="#FFBD2E"/>
  <circle cx="112" cy="42" r="5.5" fill="#27C93F"/>
  <text fill="#8B949E" class="mono" x="500" y="46" font-size="12" text-anchor="middle" font-weight="600">Garvnanda@system: ~/workspace</text>
  <line x1="48" y1="62" x2="952" y2="62" stroke="#30363D" stroke-width="1.5"/>

  <!-- RECENT LIVE GIT LOG FEED -->
  <g class="mono" font-size="13">
    <!-- Command Prompt -->
    <text x="72" y="92" class="green" font-weight="800">➜</text>
    <text x="92" y="92" class="cyan" font-weight="800">~/workspace</text>
    <text x="195" y="92" class="white" font-weight="800">git log --oneline --graph -n 3</text>

    <!-- Commit 1 -->
    <text x="72" y="122" class="purple" font-weight="800">*</text>
    <text x="88" y="122" class="yellow" font-weight="800">{c1[1]}</text>
    <text x="160" y="122" class="cyan" font-weight="800">[{c1[0]}]</text>
    <text x="270" y="122" class="white" font-weight="500">{c1[2]}</text>

    <!-- Commit 2 -->
    <text x="72" y="148" class="purple" font-weight="800">*</text>
    <text x="88" y="148" class="yellow" font-weight="800">{c2[1]}</text>
    <text x="160" y="148" class="cyan" font-weight="800">[{c2[0]}]</text>
    <text x="270" y="148" class="white" font-weight="500">{c2[2]}</text>

    <!-- Commit 3 -->
    <text x="72" y="174" class="purple" font-weight="800">*</text>
    <text x="88" y="174" class="yellow" font-weight="800">{c3[1]}</text>
    <text x="160" y="174" class="cyan" font-weight="800">[{c3[0]}]</text>
    <text x="270" y="174" class="white" font-weight="500">{c3[2]}</text>

    <!-- Active Prompt Line -->
    <text x="72" y="202" class="green" font-weight="800">➜</text>
    <text x="92" y="202" class="purple" font-weight="800">garvnanda@system:~$</text>
    <rect x="255" y="189" width="9" height="16" class="cursor"/>
  </g>
</svg>'''

def gen_constellation_svg():
    repos = get_top_repos()
    
    # 6 Top Repos mapped to Tree Fruit Nodes
    repo_names = [r[0] for r in repos]
    while len(repo_names) < 6:
        repo_names.append(f"Repo_{len(repo_names)+1}")
        
    r1, r2, r3, r4, r5, r6 = [r.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for r in repo_names[:6]]

    return f'''<svg viewBox="0 0 1000 440" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ecosystem Tree">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .bg {{ fill: #000000; }}
    .card {{ fill: #111111; stroke: #30363D; stroke-width: 1.5; }}
    
    .trunk {{ stroke: #FFFFFF; stroke-width: 3.5; stroke-linecap: round; stroke-linejoin: round; }}
    .branch-y {{ stroke: #E3B341; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
    
    .fruit-pink {{ fill: #111111; stroke: #FF5F56; stroke-width: 3.5; }}
    .fruit-green {{ fill: #111111; stroke: #39D353; stroke-width: 3.5; }}
    .fruit-blue {{ fill: #111111; stroke: #58A6FF; stroke-width: 3.5; }}
    
    .fruit-group {{ animation: float 4s ease-in-out infinite; transition: transform 0.3s; }}
    .fruit-group:hover {{ transform: scale(1.12); cursor: pointer; }}
    
    @keyframes float {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-5px); }}
    }}
  </style>
  
  <!-- Transparent / Black outer canvas -->
  <rect width="1000" height="440" class="bg"/>
  <rect x="48" y="20" width="904" height="400" rx="8" class="card"/>
  
  <!-- Header Title -->
  <text fill="#FFFFFF" class="mono" x="72" y="56" font-size="16" font-weight="800" letter-spacing="1">LIVE ECOSYSTEM TREE 🌳</text>
  <text fill="#8B949E" class="mono" x="928" y="56" font-size="12" font-weight="600" text-anchor="end">REAL-TIME REPOSITORY BRANCHES</text>
  <line x1="72" y1="70" x2="928" y2="70" stroke="#30363D" stroke-width="1"/>

  <g>
    <!-- ROOT BASE LINE -->
    <path d="M 360 380 Q 500 380 500 340 Q 500 380 640 380" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.4"/>

    <!-- TRUNK LINES (PARALLEL CIRCUIT TRUNKS) -->
    <line x1="492" y1="360" x2="492" y2="200" class="trunk"/>
    <line x1="500" y1="360" x2="500" y2="160" class="trunk"/>
    <line x1="508" y1="360" x2="508" y2="200" class="trunk"/>

    <!-- BRANCHES LEFT -->
    <!-- Low Left Branch -->
    <path d="M 492 310 L 380 310 L 300 260 L 230 260" class="branch-y"/>
    
    <!-- Mid Left Branch -->
    <path d="M 492 250 L 400 200 L 320 200 L 260 160" class="branch-y"/>
    
    <!-- High Left Branch -->
    <path d="M 500 180 L 430 120 L 340 120 L 300 95" class="branch-y"/>

    <!-- BRANCHES RIGHT -->
    <!-- Low Right Branch -->
    <path d="M 508 310 L 620 310 L 700 260 L 770 260" class="branch-y"/>
    
    <!-- Mid Right Branch -->
    <path d="M 508 250 L 600 200 L 680 200 L 740 160" class="branch-y"/>
    
    <!-- High Right Branch -->
    <path d="M 500 180 L 570 120 L 660 120 L 700 95" class="branch-y"/>

    <!-- TOP CENTER TRUNK FRUIT -->
    <path d="M 500 160 L 500 90" class="branch-y"/>

    <!-- FRUIT NODES & BADGES -->
    
    <!-- Top Center Core Node -->
    <g class="fruit-group" style="transform-origin: 500px 90px;">
      <circle cx="500" cy="90" r="15" class="fruit-green"/>
      <rect x="430" y="55" width="140" height="22" rx="4" fill="#161B22" stroke="#39D353" stroke-width="1"/>
      <text x="500" y="70" fill="#39D353" class="mono" font-size="12" font-weight="800" text-anchor="middle">@Garvnanda Core</text>
    </g>

    <!-- Node 1: High Left -->
    <g class="fruit-group" style="transform-origin: 300px 95px;">
      <circle cx="300" cy="95" r="14" class="fruit-pink"/>
      <rect x="180" y="83" width="100" height="24" rx="4" fill="#161B22" stroke="#30363D" stroke-width="1"/>
      <text x="230" y="99" fill="#FFFFFF" class="mono" font-size="11" font-weight="800" text-anchor="middle">{r1}</text>
    </g>

    <!-- Node 2: High Right -->
    <g class="fruit-group" style="transform-origin: 700px 95px;">
      <circle cx="700" cy="95" r="14" class="fruit-blue"/>
      <rect x="720" y="83" width="100" height="24" rx="4" fill="#161B22" stroke="#30363D" stroke-width="1"/>
      <text x="770" y="99" fill="#FFFFFF" class="mono" font-size="11" font-weight="800" text-anchor="middle">{r2}</text>
    </g>

    <!-- Node 3: Mid Left -->
    <g class="fruit-group" style="transform-origin: 260px 160px;">
      <circle cx="260" cy="160" r="14" class="fruit-blue"/>
      <rect x="140" y="148" width="100" height="24" rx="4" fill="#161B22" stroke="#30363D" stroke-width="1"/>
      <text x="190" y="164" fill="#FFFFFF" class="mono" font-size="11" font-weight="800" text-anchor="middle">{r3}</text>
    </g>

    <!-- Node 4: Mid Right -->
    <g class="fruit-group" style="transform-origin: 740px 160px;">
      <circle cx="740" cy="160" r="14" class="fruit-pink"/>
      <rect x="760" y="148" width="100" height="24" rx="4" fill="#161B22" stroke="#30363D" stroke-width="1"/>
      <text x="810" y="164" fill="#FFFFFF" class="mono" font-size="11" font-weight="800" text-anchor="middle">{r4}</text>
    </g>

    <!-- Node 5: Low Left -->
    <g class="fruit-group" style="transform-origin: 230px 260px;">
      <circle cx="230" cy="260" r="14" class="fruit-green"/>
      <rect x="110" y="248" width="105" height="24" rx="4" fill="#161B22" stroke="#30363D" stroke-width="1"/>
      <text x="162" y="264" fill="#FFFFFF" class="mono" font-size="11" font-weight="800" text-anchor="middle">{r5}</text>
    </g>

    <!-- Node 6: Low Right -->
    <g class="fruit-group" style="transform-origin: 770px 260px;">
      <circle cx="770" cy="260" r="14" class="fruit-green"/>
      <rect x="790" y="248" width="105" height="24" rx="4" fill="#161B22" stroke="#30363D" stroke-width="1"/>
      <text x="842" y="264" fill="#FFFFFF" class="mono" font-size="11" font-weight="800" text-anchor="middle">{r6}</text>
    </g>
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
