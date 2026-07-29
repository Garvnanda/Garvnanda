import os
import sys
import json
import random
import xml.etree.ElementTree as ET

try:
    import chess
except ImportError:
    os.system("pip install python-chess")
    import chess

STATE_PATH = "c:/Projects/Garvnanda/Garvnanda/data/chess_state.json"
ASSETS_DIR = "c:/Projects/Garvnanda/Garvnanda/assets"
DARK_ASSETS_DIR = "c:/Projects/Garvnanda/Garvnanda/assets/dark"
README_PATH = "c:/Projects/Garvnanda/Garvnanda/README.md"
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
        "winner": None
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
    print(f"Generated valid Chess SVG: {path}")

def gen_board_svg(board, last_move_uci=None, last_player="System"):
    # 8x8 Board geometry
    sq_size = 50
    board_x, board_y = 72, 70
    
    board_rects = ""
    pieces_svg = ""
    highlights = ""
    
    last_from = None
    last_to = None
    if last_move_uci and len(last_move_uci) >= 4:
        try:
            m = chess.Move.from_uci(last_move_uci)
            last_from = m.from_square
            last_to = m.to_square
        except:
            pass

    # Draw Squares & Pieces
    for rank in range(7, -1, -1):
        for file in range(8):
            sq = chess.square(file, rank)
            px = board_x + file * sq_size
            py = board_y + (7 - rank) * sq_size
            
            is_light = (rank + file) % 2 != 0
            color = "#252B33" if is_light else "#111418"
            
            # Highlight last move
            if sq in (last_from, last_to):
                color = "#1F402B" if is_light else "#142E1E"
                
            board_rects += f'<rect x="{px}" y="{py}" width="{sq_size}" height="{sq_size}" fill="{color}"/>'
            
            # File/Rank Labels
            if rank == 0:
                file_name = chr(ord('a') + file)
                board_rects += f'<text x="{px + sq_size - 6}" y="{py + sq_size - 4}" fill="#484F58" class="mono" font-size="10">{file_name}</text>'
            if file == 0:
                rank_name = str(rank + 1)
                board_rects += f'<text x="{px + 4}" y="{py + 14}" fill="#484F58" class="mono" font-size="10">{rank_name}</text>'

            # Piece
            piece = board.piece_at(sq)
            if piece:
                sym = PIECE_SYMBOLS.get(piece.symbol(), '')
                p_color = "#FFFFFF" if piece.color == chess.WHITE else "#58A6FF"
                pieces_svg += f'<text x="{px + sq_size/2}" y="{py + sq_size/2 + 13}" fill="{p_color}" font-size="34" text-anchor="middle">{sym}</text>'

    # Game Status Message
    status_msg = "YOUR TURN (WHITE)"
    status_color = "#39D353"
    if board.is_checkmate():
        status_msg = "CHECKMATE!"
        status_color = "#FF5F56"
    elif board.is_check():
        status_msg = "CHECK!"
        status_color = "#FFBD2E"
    elif board.is_stalemate():
        status_msg = "STALEMATE"
        status_color = "#8B949E"

    eval_score = evaluate_board(board)
    eval_str = f"+{eval_score/10:.1f}" if eval_score >= 0 else f"{eval_score/10:.1f}"

    return f'''<svg viewBox="0 0 1000 520" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Garv Profile Chess Arena">
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
  </style>

  <rect width="1000" height="520" class="bg"/>
  <rect x="48" y="20" width="904" height="480" rx="8" class="card"/>

  <!-- Header -->
  <text fill="#FFFFFF" class="mono" x="72" y="52" font-size="16" font-weight="800" letter-spacing="1">CHESS ARENA: PLAYER (WHITE) VS GARV AI (BLACK) ♟️</text>
  <text fill="#8B949E" class="mono" x="928" y="52" font-size="12" font-weight="600" text-anchor="end">TURN-BASED GITHUB ACTION</text>
  <line x1="72" y1="62" x2="928" y2="62" stroke="#30363D" stroke-width="1"/>

  <!-- 8x8 Chess Board -->
  <g>
    <rect x="{board_x - 2}" y="{board_y - 2}" width="404" height="404" fill="#161B22" stroke="#30363D" stroke-width="2" rx="4"/>
    {board_rects}
    {pieces_svg}
  </g>

  <!-- Right Telemetry Panel (x=500) -->
  <g class="mono">
    <!-- Status Box -->
    <rect x="500" y="80" width="428" height="70" rx="6" fill="#161B22" stroke="#30363D" stroke-width="1"/>
    <text x="520" y="105" fill="#8B949E" font-size="12" font-weight="600">GAME STATUS</text>
    <text x="520" y="132" fill="{status_color}" font-size="20" font-weight="900">{status_msg}</text>
    
    <!-- Evaluator -->
    <rect x="810" y="95" width="100" height="40" rx="4" fill="#0D1117" stroke="#30363D"/>
    <text x="860" y="112" fill="#8B949E" font-size="10" text-anchor="middle">EVAL SCORE</text>
    <text x="860" y="128" fill="#58A6FF" font-size="14" font-weight="800" text-anchor="middle">{eval_str}</text>

    <!-- Telemetry Box -->
    <rect x="500" y="165" width="428" height="155" rx="6" fill="#161B22" stroke="#30363D" stroke-width="1"/>
    <text x="520" y="192" class="purple" font-size="13" font-weight="800">LAST ACTIVITY:</text>
    <text x="520" y="215" class="white" font-size="13" font-weight="600">Player: @{last_player}</text>
    <text x="520" y="238" class="yellow" font-size="13" font-weight="600">Last Move: {last_move_uci if last_move_uci else "Game Initialized"}</text>

    <text x="520" y="275" class="cyan" font-size="13" font-weight="800">PIECE LEGEND:</text>
    <text x="520" y="298" fill="#FFFFFF" font-size="16"> White (You): ♙ ♘ ♗ ♖ ♕ ♔</text>
    <text x="730" y="298" fill="#58A6FF" font-size="16"> Black (AI): ♟ ♞ ♝ ♜ ♛ ♚</text>

    <!-- Instructions -->
    <rect x="500" y="335" width="428" height="135" rx="6" fill="#0D1117" stroke="#238636" stroke-width="1.5"/>
    <text x="520" y="362" fill="#39D353" font-size="14" font-weight="800">HOW TO PLAY:</text>
    <text x="520" y="388" fill="#C9D1D9" font-size="12">1. Scroll down to the LEGAL MOVES grid below.</text>
    <text x="520" y="410" fill="#C9D1D9" font-size="12">2. Click any move link (e.g. ▶ Play e2➔e4).</text>
    <text x="520" y="432" fill="#C9D1D9" font-size="12">3. Click "Submit new issue" on GitHub.</text>
    <text x="520" y="454" fill="#39D353" font-size="12" font-weight="bold">Garv's AI Bot will execute White &amp; Black counter in ~10s!</text>
  </g>
</svg>'''

def update_readme(board, state):
    if not os.path.exists(README_PATH):
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate Legal Moves Table
    legal_moves = list(board.legal_moves)
    moves_html = ""
    
    if board.is_game_over():
        reason = "Checkmate!" if board.is_checkmate() else "Draw!"
        moves_html = f"### 🏆 GAME OVER — {reason}\n\n[ **🔄 Click Here to Reset & Play Again** ]({REPO_URL}/issues/new?title=chess%7Creset&body=Click+Submit+New+Issue+to+reset+the+board)\n"
    else:
        moves_html = "### ♟️ AVAILABLE LEGAL MOVES (CLICK TO PLAY)\n\n"
        moves_html += "| Move | Click to Play | Move | Click to Play |\n"
        moves_html += "| --- | --- | --- | --- |\n"
        
        # Display top legal moves in 2 columns
        move_pairs = []
        for i in range(0, min(24, len(legal_moves)), 2):
            m1 = legal_moves[i]
            m2 = legal_moves[i+1] if i+1 < len(legal_moves) else None
            
            u1 = m1.uci()
            l1 = f"[ ▶ Play {u1[:2]} ➔ {u1[2:]} ]({REPO_URL}/issues/new?title=chess%7C{u1}&body=Click+Submit+new+issue+to+play+move+{u1})"
            
            if m2:
                u2 = m2.uci()
                l2 = f"[ ▶ Play {u2[:2]} ➔ {u2[2:]} ]({REPO_URL}/issues/new?title=chess%7C{u2}&body=Click+Submit+new+issue+to+play+move+{u2})"
                move_pairs.append(f"| **{u1}** | {l1} | **{u2}** | {l2} |")
            else:
                move_pairs.append(f"| **{u1}** | {l1} | - | - |")
                
        moves_html += "\n".join(move_pairs) + "\n\n"
        moves_html += f"[ **🔄 Reset Chess Game** ]({REPO_URL}/issues/new?title=chess%7Creset&body=Click+Submit+New+Issue+to+reset+the+board)\n"

    chess_section = f'''<!-- CHESS_START -->
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/s07.svg"/><img src="assets/s07.svg" alt="07 — CHESS ARENA"/></picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/dark/chess_board.svg"/>
  <img src="assets/chess_board.svg" alt="GitHub Profile Chess Game"/>
</picture>

<br/><br/>

<div align="center">

{moves_html}

</div>
<!-- CHESS_END -->'''

    # Replace or append CHESS section
    if "<!-- CHESS_START -->" in content and "<!-- CHESS_END -->" in content:
        start_idx = content.find("<!-- CHESS_START -->")
        end_idx = content.find("<!-- CHESS_END -->") + len("<!-- CHESS_END -->")
        new_content = content[:start_idx] + chess_section + content[end_idx:]
    else:
        # Insert before section 05 — THE ROUTE or footer
        if "<picture><source media=\"(prefers-color-scheme: dark)\" srcset=\"assets/dark/s05.svg\"/>" in content:
            pos = content.find("<picture><source media=\"(prefers-color-scheme: dark)\" srcset=\"assets/dark/s05.svg\"/>")
            new_content = content[:pos] + chess_section + "\n\n<br/>\n\n" + content[pos:]
        else:
            new_content = content + "\n\n" + chess_section

    # Remove old hover maze section if present
    new_content = new_content.replace('<!-- COMMIT HOVER MAZE GAME -->\n<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/dynamic/maze.svg"/><img src="assets/dynamic/maze.svg" alt="Commit Hover Maze Game"/></picture>', '')

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated README.md with live Chess game arena!")

def main():
    state = load_state()
    board = chess.Board(state["fen"])
    
    # Process move if passed via CLI: python chess_game.py "e2e4" "Username"
    if len(sys.argv) >= 2:
        move_input = sys.argv[1].strip().lower()
        player_name = sys.argv[2] if len(sys.argv) >= 3 else "Anonymous"
        
        if move_input == "reset":
            state = {
                "fen": chess.STARTING_FEN,
                "status": "in_progress",
                "move_history": [],
                "last_move": "Reset Game",
                "last_player": player_name,
                "turn_count": 1,
                "winner": None
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
                    
                    # AI Counter-move if game not over
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

    # Generate Board SVG
    svg_content = gen_board_svg(board, state.get("last_move"), state.get("last_player"))
    create_svg(os.path.join(ASSETS_DIR, "chess_board.svg"), svg_content)
    create_svg(os.path.join(DARK_ASSETS_DIR, "chess_board.svg"), svg_content)

    # Save State & Update README
    save_state(state)
    update_readme(board, state)

if __name__ == "__main__":
    main()
