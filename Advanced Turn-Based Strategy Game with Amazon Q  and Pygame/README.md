# Enhanced Turn-Based Strategy Game

A grid-based turn-based strategy game built with Python and Pygame featuring multiple unit types, special abilities, items, and multiple levels.

## Advanced Features

- Grid-based battlefield with obstacles
- Multiple unit types with different abilities:
  - Infantry: Balanced units with Shield ability
  - Archers: Ranged units with Double Attack ability
  - Cavalry: Fast units with Teleport ability
  - Mages: Powerful units with Area Attack ability
- Turn-based combat system
- AI opponents with increasing difficulty
- Multiple levels with different layouts
- Special abilities for each unit type
- Inventory system with usable items
- Enemy spawn system
- In-game tutorials
- Save/Load game functionality
- Main menu system

## Project Structure

- `strategy_game.py`: Main game file
- `unit.py`: Unit class and unit types
- `abilities.py`: Abilities and items definitions
- `levels.py`: Level management and map layouts
- `save_load.py`: Game saving and loading functionality
- `tutorial.py`: Tutorial system
- `sounds.py`: Sound management
- `ai_controller.py`: Advanced AI with multiple strategies and difficulty levels

## How to Run in VS Code

1. Make sure you have Python and Pygame installed:
   ```
   pip install pygame
   ```

2. Open the project folder in VS Code:
   - Launch VS Code
   - Go to File > Open Folder
   - Select the folder containing the game files

3. Set up the Python environment:
   - Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)
   - Type "Python: Select Interpreter" and select your Python installation

4. Run the game:
   - Open `strategy_game.py` in the editor
   - Click the "Run" button (green triangle) in the top-right corner
   - Alternatively, right-click in the editor and select "Run Python File in Terminal"
   - You can also press F5 to run with the debugger

5. Debug the game (optional):
   - Set breakpoints by clicking in the margin next to line numbers
   - Press F5 to start debugging
   - Use the debug toolbar to step through code, inspect variables, etc.

## How to Play

1. From the main menu, select "Start Game", "Level Select", or "Load Game"
2. Click on your units (left side of the screen) to select them
3. Move your units by clicking on valid tiles within the green movement range
4. Attack enemy units by clicking on them when they're within your attack range (red outline)
5. Use special abilities by pressing 'A' when a unit is selected
6. Access a unit's inventory by pressing 'I' when a unit is selected
7. End your turn when you're done by clicking the "End Turn" button
8. Save your game progress by clicking the "Save Game" button or pressing S
9. Defeat all enemy units to win and advance to the next level!

## Controls

- Left-click: Select units, move units, attack enemies
- A key: Use selected unit's special ability
- I key: Open selected unit's inventory
- S key: Save the current game state
- R key: Restart the game (when game is over)
- Arrow keys: Navigate menu options
- Enter: Select menu option
- Escape: Go back in menus

## Special Abilities

- Shield (Infantry): Reduce damage taken by 50% for one turn
- Double Attack (Archer): Attack twice in one turn
- Teleport (Cavalry): Move to any empty tile within 5 spaces
- Area Attack (Mage): Deal damage to all enemies in a 1-tile radius

## Items

- Health Potion: Restores 50 HP
- Damage Booster: Increases attack by 15 for one turn
- Defense Shield: Increases defense by 10 for two turns
- Range Extender: Increases attack range by 1 for one turn
- Movement Boost: Increases movement range by 2 for one turn

## AI Difficulty

The game features an advanced AI system with multiple difficulty levels:
- Level 1: Easy - Balanced strategy with some randomness
- Level 2: Medium - More aggressive or defensive strategies
- Level 3: Hard - Advanced strategies with ability focus and better target selection

## Troubleshooting

If you encounter any issues running the game:

1. Make sure Pygame is installed correctly:
   ```
   pip install --upgrade pygame
   ```

2. Check for Python version compatibility (Python 3.6+ recommended)

3. If you see import errors, ensure all the game files are in the same directory

4. For graphics issues, update your graphics drivers and ensure your system meets the minimum requirements for Pygame

5. If the game crashes, check the terminal output for error messages
