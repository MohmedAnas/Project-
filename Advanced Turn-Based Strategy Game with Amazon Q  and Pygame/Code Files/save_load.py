import json
import os

def save_game(game_state, filename="savegame.json"):
    """Save the game state to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(game_state, f)
        print(f"Game saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game(filename="savegame.json"):
    """Load the game state from a JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    return None

def check_save_exists(filename="savegame.json"):
    """Check if a save file exists"""
    return os.path.exists(filename)
