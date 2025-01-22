ServerSpy is a powerful and easy-to-use tool for scanning and analyzing Minecraft servers. It helps you quickly identify active players, display their roles (Friend/Admin), and retrieve essential server information.
Project was written for my russian friend, thats why software's language is russian, but it is not hard to translate them. Just I'm too lazy to add english support
Programm may scan the server forever, if any player would join or leave, it's kinda buggy, it is not final version of software, but just to know.
There is a limitation that does not let you know nicknames of players, if there are more that 35 players. Because you would wait forever until it gets all players nicknames. Its more like beta version of programm, where it may be unstable.

## Features:
- Fetch a list of players on the server with their roles (Friend/Admin).
- Display key server information:
  - Core version
  - Protocol version
  - Maximum player count
- Add or remove players to/from Friend and Admin lists.
- Save and load player data using a JSON file.
- Simple CLI interface with a user-friendly menu.

## Requirements:
- Python 3.7+
- mcstatus library

## Installation:
1. Ensure Python (version 3.7+) is installed on your system.
2. Install dependencies:
   ```bash
   pip install mcstatus

## Usage:
Launch the script:
python scanBest.py
Follow the menu instructions.

Adding a player to a list:
Enter the player's nickname: Player123
Which list to add them to? (f - Friends, a - Admins): f
Player123 has been added to the Friends list.
