import random

print("Welcome to the Snake and Ladder Game!\n")
players = int(input("Enter the number of players: "))
names = []

for i in range(players):
    name = input(f"Enter the name of player {i + 1}: ")
    names.append(name)

positions = [0] * players

def __rolldice():
    return random.randint(1, 6)

def __snake_or_ladder(position):
    snakes = {16: 6, 43: 26, 49: 11, 56: 34, 62: 19, 64: 6, 87: 24, 93: 43, 95: 55, 98: 48}
    ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    if position in snakes:
        print(f"Oh no! You landed on a snake at position {position}. You slide down to position {snakes[position]}.")
        return snakes[position]
    elif position in ladders:
        print(f"Yay! You landed on a ladder at position {position}. You climb up to position {ladders[position]}.")
        return ladders[position]
    else:
        return position

game_over = False

for i in range(0, 100):
    for j in range(players):
        dice_value = __rolldice()
        input(f"{names[j]}, press Enter to roll the dice...\n")

        if positions[j] == 0 and dice_value != 6:
            print(f"{names[j]} rolled a {dice_value} but cannot move until they roll a 6.")
            print(f"{names[j]} is now at position {positions[j]}\n")
        elif positions[j] + dice_value > 100:
            print(f"{names[j]} rolled a {dice_value} but cannot move beyond position 100.")
            print(f"{names[j]} is now at position {positions[j]}\n")
        else:
            positions[j] += dice_value
            positions[j] = __snake_or_ladder(positions[j])
            print(f"{names[j]} rolled a {dice_value} and is now at position {positions[j]}")

            if positions[j] == 100:
                print(f"{names[j]} wins!")
                game_over = True
                break