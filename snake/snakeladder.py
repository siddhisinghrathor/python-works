import tkinter as tk
from tkinter import colorchooser, font as tkfont
import random
import math

# ===========================================================
# THEME / PALETTE
# ===========================================================

BG_DARK = "#1b1f2a"
BG_PANEL = "#242a38"
BG_CARD = "#2d3446"
ACCENT = "#7c5cff"
ACCENT_LIGHT = "#a48cff"
TEXT_PRIMARY = "#f4f2ff"
TEXT_MUTED = "#9aa0b4"
BOARD_LIGHT = "#f7f3ff"
BOARD_DARK = "#e4defa"
SNAKE_COLOR = "#ff5d73"
LADDER_COLOR = "#38d996"
GOLD = "#ffcb52"

DEFAULT_COLORS = ["#ff5d73", "#4fa3ff", "#38d996", "#ffcb52"]

FONT_FAMILY = "Segoe UI"


def font(size, weight="normal"):
    return (FONT_FAMILY, size, weight)


# ===========================================================
# ROOT WINDOW
# ===========================================================

root = tk.Tk()
root.title("Snake & Ladder")
root.geometry("1050x800")
root.configure(bg=BG_DARK)
root.resizable(False, False)

players = []
position_labels = []
name_entries = []
color_buttons = []
current_player = 0
box_size = 52
board_origin = 20

snakes = {
    16: 6, 43: 26, 49: 11, 56: 34, 62: 19,
    64: 6, 87: 24, 93: 43, 95: 55, 98: 48
}

ladders = {
    1: 38, 4: 14, 9: 31, 21: 42, 28: 84,
    36: 44, 51: 67, 71: 91, 80: 100
}


# ===========================================================
# ROUNDED BUTTON HELPER (canvas-based, since ttk styling is limited)
# ===========================================================

def make_button(parent, text, command, bg=ACCENT, fg="white", width=18, pady=12, font_size=12):
    btn = tk.Label(
        parent, text=text, bg=bg, fg=fg,
        font=font(font_size, "bold"), width=width, pady=pady,
        cursor="hand2"
    )
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.config(bg=_lighten(bg)))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def _lighten(hex_color, factor=1.15):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (min(255, int(c * factor)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


# ===========================================================
# FRAMES
# ===========================================================

start_frame = tk.Frame(root, bg=BG_DARK)
start_frame.pack(expand=True, fill="both")

name_frame = tk.Frame(root, bg=BG_DARK)

game_frame = tk.Frame(root, bg=BG_DARK)


# ===========================================================
# START SCREEN
# ===========================================================

start_card = tk.Frame(start_frame, bg=BG_PANEL, padx=50, pady=40)
start_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    start_card, text="  SNAKE & LADDER  ",
    bg=BG_PANEL, fg=TEXT_PRIMARY, font=font(26, "bold")
).pack(pady=(0, 6))

tk.Label(
    start_card, text="A classic race to the top",
    bg=BG_PANEL, fg=TEXT_MUTED, font=font(12)
).pack(pady=(0, 25))

tk.Label(
    start_card, text="Number of players (1-4)",
    bg=BG_PANEL, fg=TEXT_PRIMARY, font=font(12, "bold")
).pack()

players_entry = tk.Entry(
    start_card, font=font(14), justify="center", width=10,
    bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
    relief="flat", highlightthickness=2, highlightbackground=BG_CARD,
    highlightcolor=ACCENT
)
players_entry.pack(pady=(8, 6), ipady=6)

start_error_label = tk.Label(
    start_card, text="", bg=BG_PANEL, fg=SNAKE_COLOR, font=font(10)
)
start_error_label.pack(pady=(0, 10))

start_button = make_button(start_card, "Start Game", lambda: start_game())
start_button.pack(pady=(15, 0))


# ===========================================================
# NAME + COLOR SCREEN
# ===========================================================

name_card = tk.Frame(name_frame, bg=BG_PANEL, padx=45, pady=35)
name_card.pack(expand=True)

tk.Label(
    name_card, text="Set Up Players",
    bg=BG_PANEL, fg=TEXT_PRIMARY, font=font(20, "bold")
).pack(pady=(0, 20))

name_fields_frame = tk.Frame(name_card, bg=BG_PANEL)
name_fields_frame.pack()

name_error_label = tk.Label(
    name_card, text="", bg=BG_PANEL, fg=SNAKE_COLOR, font=font(10)
)

continue_button_holder = tk.Frame(name_card, bg=BG_PANEL)


def pick_color(index):
    chosen = colorchooser.askcolor(
        color=color_buttons[index]["value"],
        title="Choose your token color"
    )
    if chosen[1]:
        color_buttons[index]["value"] = chosen[1]
        color_buttons[index]["swatch"].config(bg=chosen[1])


def build_name_fields(count):
    for widget in name_fields_frame.winfo_children():
        widget.destroy()
    name_entries.clear()
    color_buttons.clear()

    for i in range(count):
        row = tk.Frame(name_fields_frame, bg=BG_PANEL)
        row.pack(pady=8, fill="x")

        tk.Label(
            row, text=f"Player {i + 1}", bg=BG_PANEL, fg=TEXT_MUTED,
            font=font(11), width=9, anchor="w"
        ).pack(side="left")

        entry = tk.Entry(
            row, font=font(12), width=16, bg=BG_CARD, fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY, relief="flat",
            highlightthickness=2, highlightbackground=BG_CARD, highlightcolor=ACCENT
        )
        entry.insert(0, f"Player {i + 1}")
        entry.pack(side="left", padx=10, ipady=5)
        name_entries.append(entry)

        default_color = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
        swatch = tk.Label(
            row, bg=default_color, width=3, height=1,
            relief="flat", cursor="hand2",
            highlightthickness=2, highlightbackground="white"
        )
        swatch.pack(side="left", padx=4)
        entry_data = {"value": default_color, "swatch": swatch}
        color_buttons.append(entry_data)
        swatch.bind("<Button-1>", lambda e, idx=i: pick_color(idx))

        tk.Label(
            row, text="pick color", bg=BG_PANEL, fg=TEXT_MUTED, font=font(9)
        ).pack(side="left", padx=(4, 0))


# ===========================================================
# GAME SCREEN LAYOUT
# ===========================================================

game_wrapper = tk.Frame(game_frame, bg=BG_DARK)
game_wrapper.pack(expand=True, fill="both", padx=20, pady=15)

board_panel = tk.Frame(game_wrapper, bg=BG_PANEL, padx=15, pady=15)
board_panel.pack(side="left")

board_canvas = tk.Canvas(
    board_panel,
    width=box_size * 10 + board_origin * 2,
    height=box_size * 10 + board_origin * 2,
    bg=BOARD_LIGHT, highlightthickness=0
)
board_canvas.pack()

side_panel = tk.Frame(game_wrapper, bg=BG_DARK, padx=20)
side_panel.pack(side="left", fill="y")

tk.Label(
    side_panel, text="🐍  SNAKE & LADDER",
    bg=BG_DARK, fg=TEXT_PRIMARY, font=font(18, "bold")
).pack(anchor="w", pady=(0, 20))

current_player_card = tk.Frame(side_panel, bg=BG_PANEL, padx=18, pady=14)
current_player_card.pack(fill="x", pady=(0, 12))

tk.Label(
    current_player_card, text="CURRENT TURN", bg=BG_PANEL, fg=TEXT_MUTED,
    font=font(9, "bold")
).pack(anchor="w")

current_player_label = tk.Label(
    current_player_card, text="-", bg=BG_PANEL, fg=TEXT_PRIMARY, font=font(16, "bold")
)
current_player_label.pack(anchor="w", pady=(4, 0))

# dice display
dice_card = tk.Frame(side_panel, bg=BG_PANEL, padx=18, pady=16)
dice_card.pack(fill="x", pady=(0, 12))

dice_canvas = tk.Canvas(dice_card, width=70, height=70, bg=BG_PANEL, highlightthickness=0)
dice_canvas.pack()

dice_label = tk.Label(
    dice_card, text="Roll to begin", bg=BG_PANEL, fg=TEXT_MUTED, font=font(11)
)
dice_label.pack(pady=(8, 0))

roll_button = make_button(side_panel, "🎲  Roll Dice", lambda: roll_dice(), width=16)
roll_button.pack(fill="x", pady=(4, 16))

tk.Label(
    side_panel, text="PLAYERS", bg=BG_DARK, fg=TEXT_MUTED, font=font(9, "bold")
).pack(anchor="w", pady=(0, 6))

players_position_frame = tk.Frame(side_panel, bg=BG_DARK)
players_position_frame.pack(fill="x")


def draw_die_face(value):
    dice_canvas.delete("all")
    dice_canvas.create_rectangle(4, 4, 66, 66, fill="white", outline=ACCENT, width=2)
    pip_positions = {
        1: [(35, 35)],
        2: [(20, 20), (50, 50)],
        3: [(20, 20), (35, 35), (50, 50)],
        4: [(20, 20), (50, 20), (20, 50), (50, 50)],
        5: [(20, 20), (50, 20), (35, 35), (20, 50), (50, 50)],
        6: [(20, 18), (50, 18), (20, 35), (50, 35), (20, 52), (50, 52)],
    }
    for x, y in pip_positions.get(value, []):
        dice_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=BG_DARK, outline="")


draw_die_face(0)


# ===========================================================
# BOARD GEOMETRY
# ===========================================================

def get_coordinates(position):
    zero_position = position - 1
    row = zero_position // 10
    column = zero_position % 10
    if row % 2 != 0:
        column = 9 - column
    x = board_origin + column * box_size + box_size / 2
    y = board_origin + (9 - row) * box_size + box_size / 2
    return x, y


def draw_board():
    for position in range(1, 101):
        zero_position = position - 1
        row = zero_position // 10
        column = zero_position % 10
        if row % 2 != 0:
            column = 9 - column

        x1 = board_origin + column * box_size
        y1 = board_origin + (9 - row) * box_size
        x2 = x1 + box_size
        y2 = y1 + box_size

        shade = BOARD_LIGHT if (row + column) % 2 == 0 else BOARD_DARK

        board_canvas.create_rectangle(
            x1, y1, x2, y2, fill=shade, outline="#d8d2f0", width=1
        )

        text_color = GOLD if position == 100 else "#8b83b0"
        board_canvas.create_text(
            x1 + 8, y1 + 10,
            text=str(position), font=font(8, "bold"), fill=text_color, anchor="w"
        )


def draw_snakes():
    for start, end in snakes.items():
        sx, sy = get_coordinates(start)
        ex, ey = get_coordinates(end)
        board_canvas.create_line(
            sx, sy, ex, ey, fill=SNAKE_COLOR, width=7,
            capstyle="round", smooth=True
        )
        board_canvas.create_oval(
            sx - 7, sy - 7, sx + 7, sy + 7, fill=SNAKE_COLOR, outline=""
        )
        board_canvas.create_text(sx, sy, text="🐍", font=font(10))


def draw_ladders():
    for start, end in ladders.items():
        sx, sy = get_coordinates(start)
        ex, ey = get_coordinates(end)
        # draw two rails + rungs for a ladder look
        dx, dy = ex - sx, ey - sy
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length, dx / length
        offset = 5
        board_canvas.create_line(
            sx + nx * offset, sy + ny * offset, ex + nx * offset, ey + ny * offset,
            fill=LADDER_COLOR, width=3, capstyle="round"
        )
        board_canvas.create_line(
            sx - nx * offset, sy - ny * offset, ex - nx * offset, ey - ny * offset,
            fill=LADDER_COLOR, width=3, capstyle="round"
        )
        steps = 5
        for i in range(steps + 1):
            t = i / steps
            rx = sx + dx * t
            ry = sy + dy * t
            board_canvas.create_line(
                rx + nx * offset, ry + ny * offset, rx - nx * offset, ry - ny * offset,
                fill=LADDER_COLOR, width=2
            )


def draw_players():
    for i, player in enumerate(players):
        if player["position"] == 0:
            if player["token"] is not None:
                board_canvas.delete(player["token"])
                board_canvas.delete(player["token_text"])
                player["token"] = None
                player["token_text"] = None
            continue

        x, y = get_coordinates(player["position"])
        offset_x = (i % 2) * 12 - 6
        offset_y = (i // 2) * 12 - 6

        if player["token"] is None:
            player["token"] = board_canvas.create_oval(
                x - 11 + offset_x, y - 11 + offset_y,
                x + 11 + offset_x, y + 11 + offset_y,
                fill=player["color"], outline="white", width=2
            )
            player["token_text"] = board_canvas.create_text(
                x + offset_x, y + offset_y,
                text=player["name"][0].upper(),
                fill="white", font=font(9, "bold")
            )
        else:
            board_canvas.coords(
                player["token"],
                x - 11 + offset_x, y - 11 + offset_y,
                x + 11 + offset_x, y + 11 + offset_y
            )
            board_canvas.coords(player["token_text"], x + offset_x, y + offset_y)

        board_canvas.tag_raise(player["token"])
        board_canvas.tag_raise(player["token_text"])


# ===========================================================
# SMOOTH TOKEN ANIMATION (eased slide between two squares)
# ===========================================================

def ease_in_out(t):
    return t * t * (3 - 2 * t)


def animate_slide(player, from_pos, to_pos, on_done, duration=180, steps=10):
    """Smoothly slide a token's pixel position from from_pos to to_pos."""
    fx, fy = get_coordinates(from_pos)
    tx, ty = get_coordinates(to_pos)

    idx = players.index(player)
    offset_x = (idx % 2) * 12 - 6
    offset_y = (idx // 2) * 12 - 6

    def step(i=0):
        t = ease_in_out(i / steps)
        x = fx + (tx - fx) * t
        y = fy + (ty - fy) * t

        if player["token"] is None:
            player["token"] = board_canvas.create_oval(
                x - 11, y - 11, x + 11, y + 11,
                fill=player["color"], outline="white", width=2
            )
            player["token_text"] = board_canvas.create_text(
                x, y, text=player["name"][0].upper(), fill="white", font=font(9, "bold")
            )
        else:
            board_canvas.coords(
                player["token"],
                x - 11 + offset_x, y - 11 + offset_y,
                x + 11 + offset_x, y + 11 + offset_y
            )
            board_canvas.coords(player["token_text"], x + offset_x, y + offset_y)

        board_canvas.tag_raise(player["token"])
        board_canvas.tag_raise(player["token_text"])

        if i < steps:
            root.after(duration // steps, lambda: step(i + 1))
        else:
            on_done()

    step()


def animate_dice_roll(final_value, on_done, rolls=10):
    def step(i=0):
        if i < rolls:
            draw_die_face(random.randint(1, 6))
            root.after(60, lambda: step(i + 1))
        else:
            draw_die_face(final_value)
            on_done()
    step()


# ===========================================================
# PLAYER SETUP
# ===========================================================

def save_players():
    global players, current_player

    for entry in name_entries:
        if not entry.get().strip():
            name_error_label.config(text="Please fill in every player's name.")
            name_error_label.pack(pady=(10, 0))
            return

    players = []
    position_labels.clear()
    current_player = 0

    for i, entry in enumerate(name_entries):
        players.append({
            "name": entry.get().strip(),
            "position": 0,
            "color": color_buttons[i]["value"],
            "token": None,
            "token_text": None
        })

    for widget in players_position_frame.winfo_children():
        widget.destroy()

    for player in players:
        row = tk.Frame(players_position_frame, bg=BG_PANEL, padx=12, pady=8)
        row.pack(fill="x", pady=4)

        dot = tk.Canvas(row, width=14, height=14, bg=BG_PANEL, highlightthickness=0)
        dot.create_oval(2, 2, 12, 12, fill=player["color"], outline="")
        dot.pack(side="left", padx=(0, 8))

        label = tk.Label(
            row, text=f"{player['name']} — Start",
            bg=BG_PANEL, fg=TEXT_PRIMARY, font=font(11, "bold"), anchor="w"
        )
        label.pack(side="left", fill="x", expand=True)

        position_labels.append(label)

    current_player_label.config(text=players[0]["name"])

    name_frame.pack_forget()
    game_frame.pack(expand=True, fill="both")

    draw_board()
    draw_snakes()
    draw_ladders()
    draw_players()


def start_game():
    try:
        n = int(players_entry.get())
    except ValueError:
        start_error_label.config(text="Please enter a number between 1 and 4.")
        return

    if n < 1 or n > 4:
        start_error_label.config(text="Please enter a valid number of players (1-4).")
        return

    start_error_label.config(text="")
    start_frame.pack_forget()
    name_frame.pack(expand=True, fill="both")

    build_name_fields(n)
    continue_button_holder.pack(pady=(20, 0))
    for widget in continue_button_holder.winfo_children():
        widget.destroy()
    cont_btn = make_button(continue_button_holder, "Continue", save_players)
    cont_btn.pack()


# ===========================================================
# GAMEPLAY LOGIC
# ===========================================================

def update_position_label(player):
    idx = players.index(player)
    text = f"{player['name']} — {'Start' if player['position'] == 0 else player['position']}"
    if player["position"] == 100:
        text = f"🏆 {player['name']} — WINNER!"
    position_labels[idx].config(text=text)


def move_step():
    try:
        if player["position"] >= target_position:
            on_finished()
            return
        start = player["position"]
        end = start + 1
        player["position"] = end
        update_position_label(player)
        animate_slide(player, start, end, move_step, duration=140, steps=6)
    except Exception as e:
        import traceback; traceback.print_exc()

    move_step()


def finish_move(player):
    global current_player

    def after_snake_or_ladder():
        update_position_label(player)

        if player["position"] == 100:
            dice_label.config(text=f"🏆 {player['name']} wins the game!")
            roll_button.config(state=tk.DISABLED)
            return

        current_player = (current_player + 1) % len(players)
        current_player_label.config(text=players[current_player]["name"])
        roll_button.config(state=tk.NORMAL)

    if player["position"] in snakes:
        target = snakes[player["position"]]
        dice_label.config(text=f"🐍 {player['name']} slid down a snake!")
        animate_slide(player, player["position"], target, lambda: (
            player.__setitem__("position", target), after_snake_or_ladder()
        ), duration=350, steps=14)

    elif player["position"] in ladders:
        target = ladders[player["position"]]
        dice_label.config(text=f"🪜 {player['name']} climbed a ladder!")
        animate_slide(player, player["position"], target, lambda: (
            player.__setitem__("position", target), after_snake_or_ladder()
        ), duration=350, steps=14)

    else:
        after_snake_or_ladder()


def roll_dice():
    global current_player

    player = players[current_player]
    dice_value = random.randint(1, 6)
    current_position = player["position"]

    roll_button.config(state=tk.DISABLED)

    def after_roll_animation():
        if current_position == 0 and dice_value != 6:
            dice_label.config(text=f"{player['name']} rolled {dice_value} — need a 6 to start!")
            current_player_advance()
            return

        new_position = current_position + dice_value

        if new_position > 100:
            dice_label.config(text=f"{player['name']} rolled {dice_value} — overshoots 100!")
            current_player_advance()
            return

        dice_label.config(text=f"{player['name']} rolled {dice_value}")
        animate_token_path(player, new_position, lambda: finish_move(player))

    animate_dice_roll(dice_value, after_roll_animation)


def current_player_advance():
    global current_player
    current_player = (current_player + 1) % len(players)
    current_player_label.config(text=players[current_player]["name"])
    roll_button.config(state=tk.NORMAL)


# ===========================================================
# MAIN LOOP
# ===========================================================

root.mainloop()