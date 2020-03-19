# colorful-platform

## Instructions

1. Find out your local ip adress (192.168.X.X). On linux use `ip adress`, on windows use `ifconfig`.
2. Paste your ip adress in the `ip_adress` variables in the top of the files `projectse/Server.py` and `projectse/game_manager.py`
3. Open a terminal and change directory to `projectse` and run `python3 Server.py`
4. Open another terminal and run `python3 project_se.py`

You can now play the game

## How to play

Use the arrow keys to move around and press enter to select or place a stone. You can at any time press escape to exit the game.

## Modes

### Single

In single you play against another human player on your computer

### Tournament

In tournament you are 3-8 players and you can have AI's playing against you. You will play against everyone and the winner is announced at the end

## Known bugs

- Placeing a stone in the top left corner when playing against an AI causes the game to crash on the first turn
