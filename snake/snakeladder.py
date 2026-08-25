import tkinter as tk
import random

# create the main window
root = tk.Tk()

root.title("Snake and Ladder Game")
root.geometry("600x600")




# create the list of colors that will be assigned to the players
colors = ["red", "blue", "green", "yellow"]

# create an empty list where we will store the player name entry boxes
name_entries = []

# create an empty list where we will store the player information
players = []

# initialize the current player
current_player = 0

# ---------------------------------------------------------
# START FRAME
# ---------------------------------------------------------

# create a frame for the starting part of the game
start_frame = tk.Frame(root)

start_frame.pack(pady=20)


# from here everything is inside the starting frame of the gui
label = tk.Label(
    start_frame,
    text="Welcome to the Snake and Ladder Game!"
)

label.pack()


# calling for the players to enter the number of players
label = tk.Label(
    start_frame,
    text="Enter number of players (1-4):"
)

label.pack(pady=10)


# here we create the box for the players to enter the number of players
players_entry = tk.Entry(start_frame)

players_entry.pack(pady=10)


# ---------------------------------------------------------
# NAME FRAME
# ---------------------------------------------------------

# create a frame where the players will enter their names
name_frame = tk.Frame(root)

# we are not packing the name frame yet because
# we only want it to appear after the Start Game button is pressed


# ---------------------------------------------------------
# GAME FRAME
# ---------------------------------------------------------

# create a frame where the actual game will be displayed
game_frame = tk.Frame(root)

# we are not packing the game frame yet because
# the actual game should only appear after the players have entered their names


# ---------------------------------------------------------
# SAVE PLAYERS FUNCTION
# ---------------------------------------------------------

# this function will be called when the Continue button is pressed
def save_players():

    global players

    # clear the players list before adding the player information
    players = []



    # go through every name entry box and get the name entered by the player
    for i, entry in enumerate(name_entries):

        name = entry.get()

        player = {
            "name": name,
            "position": 0,
            "color": colors[i]
        }

        players.append(player)

    print(players)

      # show the first player's name because they will get the first turn
    current_player_label.config(
        text=f"Current Player: {players[0]['name']}"
    )

    # after the players have been created,
    # hide the name frame because we no longer need it
    name_frame.pack_forget()

    # show the game frame because the players are ready and the game can start
    game_frame.pack(pady=20)


# ---------------------------------------------------------
# START GAME FUNCTION
# ---------------------------------------------------------

# this function will be called when the Start Game button is pressed
def start_game():

    players_number = int(players_entry.get())

    # check if the number of players is between 1 and 4
    if players_number < 1 or players_number > 4:

        error_label = tk.Label(
            start_frame,
            text="Please enter a valid number of players (1-4)."
        )

        error_label.pack()

        return

    # hide the starting frame because we now want the players to enter their names
    start_frame.pack_forget()

    # show the name frame
    name_frame.pack(pady=20)

    # create a name entry box for every player
    for i in range(players_number):

        player_label = tk.Label(
            name_frame,
            text=f"Player {i + 1} Name:"
        )

        player_label.pack()

        # create the box where the player will enter their name
        name_entry = tk.Entry(name_frame)

        name_entry.pack(pady=5)

        # store the entry box in the name_entries list
        name_entries.append(name_entry)

    # create the Continue button after all the name entry boxes
    # have been created
    continue_button = tk.Button(
        name_frame,
        text="Continue",
        command=save_players
    )

    continue_button.pack(pady=10)


# ---------------------------------------------------------
# START GAME BUTTON
# ---------------------------------------------------------

# here is the Start Game button that will call the start_game function
# when it is pressed
start_button = tk.Button(
    start_frame,
    text="Start Game",
    command=start_game
)

start_button.pack(pady=10)


# ---------------------------------------------------------
# GAME UI
# ---------------------------------------------------------

# this is the label that will show the current position of the player
position_label = tk.Label(
    game_frame,
    text="Position: 0",
    font=("Arial", 16)
)

position_label.pack(pady=10)

# this is the label that will show whose turn it is
current_player_label = tk.Label(
    game_frame,
    text = "Current Player: -",
    font = ("Arial", 16)
)

current_player_label.pack(pady=10)

# this is the label that will show the value of the dice rolled
dice_label = tk.Label(
    game_frame,
    text="You rolled: -",
    font=("Arial", 16)
)

dice_label.pack(pady=10)

# ---------------------------------------------------------
# ROLL DICE FUNCTION
# ---------------------------------------------------------

# this is the function that will be called when the Roll Dice button is pressed

def roll_dice():

    global current_player

    # get the player whose turn it currently is
    player = players[current_player]

    # the dice value is generated randomly between 1 and 6
    dice_value = random.randint(1, 6)

    # get the current position of the player
    current_position = player["position"]

    # if the player is at position 0 and rolls a number other than 6,
    # they cannot start the game
    if current_position == 0 and dice_value != 6:

        dice_label.config(
            text=f"{player['name']} rolled {dice_value}. You need to roll a 6 to start."
        )

        # move to the next player
        current_player = (current_player + 1) % len(players)

        current_player_label.config(
            text=f"Current Player: {players[current_player]['name']}"
        )

        return

    # show the dice value
    dice_label.config(
        text=f"{player['name']} rolled: {dice_value}"
    )

    # calculate the new position
    new_position = current_position + dice_value

    # the player cannot move beyond position 100
    if new_position > 100:

        position_label.config(
            text=f"{player['name']} stays at position {current_position}"
        )

        # move to the next player
        current_player = (current_player + 1) % len(players)

        current_player_label.config(
            text=f"Current Player: {players[current_player]['name']}"
        )

        return

    # update the player's position
    player["position"] = new_position

    # create the snakes
    snakes = {
        16: 6,
        43: 26,
        49: 11,
        56: 34,
        62: 19,
        64: 6,
        87: 24,
        93: 43,
        95: 55,
        98: 48
    }

    # create the ladders
    ladders = {
        1: 38,
        4: 14,
        9: 31,
        21: 42,
        28: 84,
        36: 44,
        51: 67,
        71: 91,
        80: 100
    }

    # check if the player has landed on a snake
    if player["position"] in snakes:

        player["position"] = snakes[player["position"]]

        position_label.config(
            text=f"{player['name']} is at position {player['position']} (Snake!)"
        )

    # check if the player has landed on a ladder
    elif player["position"] in ladders:

        player["position"] = ladders[player["position"]]

        position_label.config(
            text=f"{player['name']} is at position {player['position']} (Ladder!)"
        )

    else:

        position_label.config(
            text=f"{player['name']} is at position {player['position']}"
        )

    # check if the player has reached position 100
    if player["position"] == 100:

        position_label.config(
            text=f"🎉 {player['name']} won the game! 🎉"
        )

        roll_button.config(
            state=tk.DISABLED
        )

        return

    # move to the next player
    current_player = (current_player + 1) % len(players)

    # update the current player label
    current_player_label.config(
        text=f"Current Player: {players[current_player]['name']}"
    )

# ---------------------------------------------------------
# ROLL DICE BUTTON
# ---------------------------------------------------------

# button to roll the dice
roll_button = tk.Button(
    game_frame,
    text="Roll Dice",
    command=roll_dice
)

roll_button.pack(pady=20)


# start the Tkinter event loop
root.mainloop()