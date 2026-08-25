import tkinter as tk
import random
# create the main window
root = tk.Tk()
root.title("Snake and Ladder Game") 
root.geometry("600x600")
# initialize player position
player_position = 0

# from here everything is inside the window of the gui 
label = tk.Label(root, text="Welcome to the Snake and Ladder Game!")
label.pack()

# calling for the players to enter the number of players

label = tk.Label(root, text="Enter number of players (1-4):")
label.pack()

# here we create the box for the players to enter the number of players 
players_entry = tk.Entry(root)
players_entry.pack(pady=10)

colors = ["red", "blue", "green", "yellow"]

# python reads everything from top to bottom so we need to define the function before we call it in the button
# here is the start game function that will be called when the start button is pressed
name_entries = []

def start_game():
    players = int(players_entry.get())

    if players < 1 or players > 4:
        error_label = tk.Label(
            root,
            text="Please enter a valid number of players (1-4)."
        )
        error_label.pack()
        return

    for i in range(players):
        player_label = tk.Label(
            root,
            text=f"Player {i + 1} Name:"
        )
        player_label.pack()

        name_entry = tk.Entry(root)
        name_entry.pack(pady=5)

        name_entries.append(name_entry)

    continue_button = tk.Button(
        root,
        text="Continue",
        command=save_players
    )

    continue_button.pack(pady=10)


players = []

def save_players():
    names = []

    for entry in name_entries:
        name = entry.get()
        names.append(name)

    print(names)
# here is the start button that will call the start game function when pressed
start_button = tk.Button(
    root,
    text="Start Game",
    command=start_game
)

start_button.pack(pady=10)
    


# this is the label that will show the current position of the player
position_label = tk.Label(
    root,
    text="Position: 0",
    font=("Arial", 16)
)
position_label.pack(pady=10)

# this is the label that will show the value of the dice rolled
dice_label = tk.Label(
    root,
    text="You rolled: -",
    font=("Arial", 16)
)
dice_label.pack(pady=10)

# this is the function that will be called when the roll dice button is pressed
def roll_dice():
    global player_position
# the dice value is generated randomly between 1 and 6 and if the player is at position 0 and rolls a number other than 6, they cannot move forward and 
# the dice_value stores the value of the dice rolled and is displayed in the dice_label
    dice_value = random.randint(1, 6)
    if player_position == 0 and dice_value != 6:
        dice_label.config(text=f"You rolled: {dice_value}. You need to roll a 6 to start.")
        return
# the config method is used to change the text of the dice_label to show the value of the dice rolled
    dice_label.config(text=f"You rolled: {dice_value}")

    new_position = player_position + dice_value
# the player cannot move beyond position 100, so if the new position is greater than 100, the player stays in the same position and 
# the position_label is updated to show the current position
    if new_position > 100:
        new_position = player_position
        position_label.config(text=f"Position: {new_position}")
        return
# the player_position is updated to the new position and the position_label is updated to show the current position
    player_position = new_position

    snakes = {
        16: 6, 43: 26, 49: 11, 56: 34, 62: 19,
        64: 6, 87: 24, 93: 43, 95: 55, 98: 48
    }

    ladders = {
        1: 38, 4: 14, 9: 31, 21: 42, 28: 84,
        36: 44, 51: 67, 71: 91, 80: 100
    }
# check if the player has landed on a snake or a ladder and then update the player position accordingly and update the position_label 
# to show the current position and if the player has landed on a snake or a ladder
    if player_position in snakes:
        player_position = snakes[player_position]
        position_label.config(
            text=f"Position: {player_position} (Snake!)"
        )

    elif player_position in ladders:
        player_position = ladders[player_position]
        position_label.config(
            text=f"Position: {player_position} (Ladder!)"
        )

    else:
        position_label.config(
            text=f"Position: {player_position}"
        )
# if the player has reached position 100, the game is won and the roll button is disabled

    if player_position == 100:
        position_label.config(text="Congratulations! You reached 100 and won the game!")
        roll_button.config(state=tk.DISABLED)    


#button to roll the dice
roll_button = tk.Button(root, text="Roll Dice", command=roll_dice)
roll_button.pack(pady=20) 

root.mainloop()
