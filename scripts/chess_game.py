import os
import sys
import json
import random
import re
import xml.etree.ElementTree as ET

try:
    import chess
except ImportError:
    os.system("pip install python-chess")
    import chess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(BASE_DIR, "data", "chess_state.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DARK_ASSETS_DIR = os.path.join(BASE_DIR, "assets", "dark")
README_PATH = os.path.join(BASE_DIR, "README.md")
REPO_URL = "https://github.com/Garvnanda/Garvnanda"

PIECE_SYMBOLS = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900
}

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "fen": chess.STARTING_FEN,
        "status": "in_progress",
        "move_history": [],
        "last_move": None,
        "last_player": "System",
        "turn_count": 1,
        "winner": None,
        "repo_count": 6
    }

def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def evaluate_board(board):
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
        
    score = 0
    for square, piece in board.piece_map().items():
        val = PIECE_VALUES.get(piece.piece_type, 0)
        if piece.color == chess.WHITE:
            score += val
        else:
            score -= val
    return score

def get_best_ai_move(board):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
        
    best_move = None
    best_score = 99999 # Black wants to minimize score
    
    for move in legal_moves:
        board.push(move)
        score = evaluate_board(board)
        board.pop()
        
        if score < best_score:
            best_score = score
            best_move = move
            
    return best_move if best_move else random.choice(legal_moves)

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
    print(f"Generated valid Minimalist Chess SVG: {path}")

def gen_board_svg(board, last_move_uci=None, last_player="System"):
    sq_size = 50
    board_x, board_y = 50, 60
    
    board_rects = ""
    pieces_svg = ""
    
    last_from = None
    last_to = None
    if last_move_uci and len(last_move_uci) >= 4:
        try:
            m = chess.Move.from_uci(last_move_uci.split(' ')[0])
            last_from = m.from_square
            last_to = m.to_square
        except:
            pass

    for rank in range(7, -1, -1):
        for file in range(8):
            sq = chess.square(file, rank)
            px = board_x + file * sq_size
            py = board_y + (7 - rank) * sq_size
            
            is_light = (rank + file) % 2 != 0
            color = "#21262D" if is_light else "#111418"
            
            if sq in (last_from, last_to):
                color = "#1F402B" if is_light else "#142E1E"
                
            board_rects += f'<rect x="{px}" y="{py}" width="{sq_size}" height="{sq_size}" fill="{color}"/>'
            
            if rank == 0:
                file_name = chr(ord('a') + file)
                board_rects += f'<text x="{px + sq_size - 6}" y="{py + sq_size - 4}" fill="#484F58" class="mono" font-size="10">{file_name}</text>'
            if file == 0:
                rank_name = str(rank + 1)
                board_rects += f'<text x="{px + 4}" y="{py + 14}" fill="#484F58" class="mono" font-size="10">{rank_name}</text>'

            piece = board.piece_at(sq)
            if piece:
                sym = PIECE_SYMBOLS.get(piece.symbol(), '')
                p_color = "#FFFFFF" if piece.color == chess.WHITE else "#58A6FF"
                pieces_svg += f'<text x="{px + sq_size/2}" y="{py + sq_size/2 + 13}" fill="{p_color}" font-size="34" text-anchor="middle">{sym}</text>'

    status_str = "YOUR TURN (WHITE)"
    status_col = "#39D353"
    if board.is_checkmate():
        status_str = "CHECKMATE!"
        status_col = "#FF5F56"
    elif board.is_check():
        status_str = "CHECK!"
        status_col = "#FFBD2E"

    return f'''<svg viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Garv Profile Chess Board">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .bg {{ fill: #000000; }}
    .card {{ fill: #111111; stroke: #30363D; stroke-width: 1.5; }}
  </style>

  <rect width="500" height="500" class="bg"/>
  <rect x="20" y="20" width="460" height="460" rx="8" class="card"/>

  <text fill="#FFFFFF" class="mono" x="50" y="45" font-size="13" font-weight="800">Garv AI (Black) ♟  vs  You (White) ♙</text>
  <text fill="{status_col}" class="mono" x="450" y="45" font-size="12" font-weight="800" text-anchor="end">{status_str}</text>

  <g>
    <rect x="{board_x - 2}" y="{board_y - 2}" width="404" height="404" fill="#161B22" stroke="#30363D" stroke-width="2" rx="4"/>
    {board_rects}
    {pieces_svg}
  </g>
</svg>'''

def update_readme(board, state):
    if not os.path.exists(README_PATH):
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    legal_moves = list(board.legal_moves)
    left_badges = []
    right_badges = []

    if not board.is_game_over():
        for i, m in enumerate(legal_moves[:12]):
            uci = m.uci()
            move_fmt = f"{uci[:2]} ➔ {uci[2:]}"
            badge_url = f"https://img.shields.io/badge/PLAY-{uci[:2]}--{uci[2:]}-0d1117?style=for-the-badge&amp;logo=github&amp;logoColor=39D353"
            issue_url = f"{REPO_URL}/issues/new?title=chess%7C{uci}&amp;body=Click+Submit+new+issue+to+play+move+{uci}"
            badge_link = f'<a href="{issue_url}"><img src="{badge_url}" alt="Play {move_fmt}"/></a>'
            
            if i % 2 == 0:
                left_badges.append(badge_link)
            else:
                right_badges.append(badge_link)

    left_html = "<br/><br/>".join(left_badges) if left_badges else "<i>No moves</i>"
    right_html = "<br/><br/>".join(right_badges) if right_badges else "<i>No moves</i>"

    # Absolute raw URLs with timestamp cache-buster to completely bypass GitHub camo caching
    import time
    v = int(time.time())
    raw_base = "https://raw.githubusercontent.com/Garvnanda/Garvnanda/main"
    
    chess_section = f'''<!-- CHESS_START -->
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/s07.svg"/><img src="assets/s07.svg" alt="07 — CHESS ARENA"/></picture>

<div align="center">

<p align="center">
  <b>Click any move badge below to play against Garv's AI Bot</b><br/>
  <font color="#8B949E">AI responds automatically in ~10s • Board resets automatically on new repository creation</font>
</p>

<table border="0">
<tr>
<td align="center" valign="middle">
{left_html}
</td>
<td align="center" valign="middle" width="520">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{raw_base}/assets/dark/chess_board.svg?v={v}"/>
    <img src="{raw_base}/assets/chess_board.svg?v={v}" alt="GitHub Profile Chess Game" width="480"/>
  </picture>
</td>
<td align="center" valign="middle">
{right_html}
</td>
</tr>
</table>

</div>
<!-- CHESS_END -->'''

    if "<!-- CHESS_START -->" in content and "<!-- CHESS_END -->" in content:
        start_idx = content.find("<!-- CHESS_START -->")
        end_idx = content.find("<!-- CHESS_END -->") + len("<!-- CHESS_END -->")
        new_content = content[:start_idx] + chess_section + content[end_idx:]
    else:
        if "<picture><source media=\"(prefers-color-scheme: dark)\" srcset=\"assets/dark/s05.svg\"/>" in content:
            pos = content.find("<picture><source media=\"(prefers-color-scheme: dark)\" srcset=\"assets/dark/s05.svg\"/>")
            new_content = content[:pos] + chess_section + "\n\n<br/>\n\n" + content[pos:]
        else:
            new_content = content + "\n\n" + chess_section

    new_content = new_content.replace('<!-- COMMIT HOVER MAZE GAME -->\n<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/dynamic/maze.svg"/><img src="assets/dynamic/maze.svg" alt="Commit Hover Maze Game"/></picture>', '')

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated README.md with live Chess game arena and cache-busting!")

def main():
    state = load_state()
    board = chess.Board(state["fen"])
    
    if len(sys.argv) >= 2:
        raw_input = sys.argv[1].strip()
        player_name = sys.argv[2] if len(sys.argv) >= 3 else "Anonymous"
        
        match = re.search(r'([a-h][1-8][a-h][1-8]|reset)', raw_input, re.IGNORECASE)
        if match:
            move_input = match.group(1).lower()
            if move_input == "reset":
                state = {
                    "fen": chess.STARTING_FEN,
                    "status": "in_progress",
                    "move_history": [],
                    "last_move": "Reset Game",
                    "last_player": player_name,
                    "turn_count": 1,
                    "winner": None,
                    "repo_count": state.get("repo_count", 6)
                }
                board = chess.Board()
            else:
                try:
                    user_move = chess.Move.from_uci(move_input)
                    if user_move in board.legal_moves:
                        board.push(user_move)
                        state["move_history"].append(move_input)
                        state["last_move"] = move_input
                        state["last_player"] = player_name
                        
                        if not board.is_game_over():
                            ai_move = get_best_ai_move(board)
                            if ai_move:
                                board.push(ai_move)
                                state["move_history"].append(ai_move.uci())
                                state["last_move"] = f"{move_input} (You) ➔ {ai_move.uci()} (AI)"
                        
                        state["fen"] = board.fen()
                        state["turn_count"] += 1
                    else:
                        print(f"Illegal move attempted: {move_input}")
                except Exception as e:
                    print(f"Error processing move {move_input}: {e}")
        else:
            print(f"No valid UCI move found in input string: {raw_input}")

    svg_content = gen_board_svg(board, state.get("last_move"), state.get("last_player"))
    create_svg(os.path.join(ASSETS_DIR, "chess_board.svg"), svg_content)
    create_svg(os.path.join(DARK_ASSETS_DIR, "chess_board.svg"), svg_content)

    save_state(state)
    update_readme(board, state)

if __name__ == "__main__":
    main()
