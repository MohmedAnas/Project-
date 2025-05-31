import json
import os
from enum import Enum

# Define map layouts for different levels
class MapLayouts:
    @staticmethod
    def get_level_map(level):
        """Returns map data for the specified level"""
        maps = {
            1: {
                "name": "Training Grounds",
                "grid_width": 16,
                "grid_height": 12,
                "player_units": [
                    {"type": "INFANTRY", "x": 1, "y": 3},
                    {"type": "INFANTRY", "x": 1, "y": 8},
                    {"type": "ARCHER", "x": 0, "y": 5},
                    {"type": "CAVALRY", "x": 2, "y": 6},
                    {"type": "MAGE", "x": 0, "y": 7}
                ],
                "enemy_units": [
                    {"type": "INFANTRY", "x": 14, "y": 3},
                    {"type": "INFANTRY", "x": 14, "y": 8},
                    {"type": "ARCHER", "x": 15, "y": 5},
                    {"type": "CAVALRY", "x": 13, "y": 6},
                    {"type": "MAGE", "x": 15, "y": 7}
                ],
                "spawn_points": [
                    {"x": 15, "y": 2},
                    {"x": 15, "y": 9}
                ],
                "spawn_interval": 5,  # Spawn new enemies every 5 turns
                "tutorial": True,     # Show tutorial for this level
                "obstacles": []       # No obstacles in first level
            },
            2: {
                "name": "Forest Ambush",
                "grid_width": 16,
                "grid_height": 12,
                "player_units": [
                    {"type": "INFANTRY", "x": 1, "y": 3},
                    {"type": "INFANTRY", "x": 1, "y": 8},
                    {"type": "ARCHER", "x": 0, "y": 5},
                    {"type": "CAVALRY", "x": 2, "y": 6},
                    {"type": "MAGE", "x": 0, "y": 7}
                ],
                "enemy_units": [
                    {"type": "INFANTRY", "x": 14, "y": 3},
                    {"type": "INFANTRY", "x": 14, "y": 8},
                    {"type": "ARCHER", "x": 15, "y": 5},
                    {"type": "ARCHER", "x": 15, "y": 9},
                    {"type": "CAVALRY", "x": 13, "y": 6},
                    {"type": "MAGE", "x": 15, "y": 7}
                ],
                "spawn_points": [
                    {"x": 15, "y": 2},
                    {"x": 15, "y": 10}
                ],
                "spawn_interval": 4,  # Spawn new enemies every 4 turns
                "tutorial": False,
                "obstacles": [
                    {"x": 7, "y": 3},
                    {"x": 7, "y": 4},
                    {"x": 8, "y": 4},
                    {"x": 8, "y": 5},
                    {"x": 7, "y": 8},
                    {"x": 8, "y": 8},
                    {"x": 8, "y": 9}
                ]
            },
            3: {
                "name": "Mountain Pass",
                "grid_width": 16,
                "grid_height": 12,
                "player_units": [
                    {"type": "INFANTRY", "x": 1, "y": 3},
                    {"type": "INFANTRY", "x": 1, "y": 8},
                    {"type": "ARCHER", "x": 0, "y": 5},
                    {"type": "CAVALRY", "x": 2, "y": 6},
                    {"type": "MAGE", "x": 0, "y": 7},
                    {"type": "MAGE", "x": 2, "y": 4}
                ],
                "enemy_units": [
                    {"type": "INFANTRY", "x": 14, "y": 3},
                    {"type": "INFANTRY", "x": 14, "y": 8},
                    {"type": "INFANTRY", "x": 13, "y": 5},
                    {"type": "ARCHER", "x": 15, "y": 5},
                    {"type": "ARCHER", "x": 15, "y": 9},
                    {"type": "CAVALRY", "x": 13, "y": 6},
                    {"type": "CAVALRY", "x": 14, "y": 2},
                    {"type": "MAGE", "x": 15, "y": 7}
                ],
                "spawn_points": [
                    {"x": 15, "y": 2},
                    {"x": 15, "y": 10},
                    {"x": 13, "y": 1}
                ],
                "spawn_interval": 3,  # Spawn new enemies every 3 turns
                "tutorial": False,
                "obstacles": [
                    {"x": 5, "y": 2},
                    {"x": 5, "y": 3},
                    {"x": 6, "y": 3},
                    {"x": 6, "y": 4},
                    {"x": 7, "y": 4},
                    {"x": 7, "y": 5},
                    {"x": 8, "y": 5},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 6},
                    {"x": 9, "y": 7},
                    {"x": 8, "y": 7},
                    {"x": 8, "y": 8},
                    {"x": 7, "y": 8},
                    {"x": 7, "y": 9},
                    {"x": 6, "y": 9},
                    {"x": 6, "y": 10}
                ]
            }
        }
        
        return maps.get(level, maps[1])  # Default to level 1 if level not found

# Item definitions
class ItemType(Enum):
    HEALTH_POTION = 1
    DAMAGE_BOOSTER = 2
    DEFENSE_SHIELD = 3
    RANGE_EXTENDER = 4
    MOVEMENT_BOOST = 5

class Item:
    @staticmethod
    def get_item_data(item_type):
        """Returns data for the specified item type"""
        items = {
            ItemType.HEALTH_POTION: {
                "name": "Health Potion",
                "description": "Restores 50 HP",
                "effect": {"type": "heal", "value": 50},
                "icon": "H",
                "color": (0, 255, 0)  # Green
            },
            ItemType.DAMAGE_BOOSTER: {
                "name": "Damage Booster",
                "description": "Increases attack by 15 for one turn",
                "effect": {"type": "attack_boost", "value": 15, "duration": 1},
                "icon": "D",
                "color": (255, 0, 0)  # Red
            },
            ItemType.DEFENSE_SHIELD: {
                "name": "Defense Shield",
                "description": "Increases defense by 10 for two turns",
                "effect": {"type": "defense_boost", "value": 10, "duration": 2},
                "icon": "S",
                "color": (0, 0, 255)  # Blue
            },
            ItemType.RANGE_EXTENDER: {
                "name": "Range Extender",
                "description": "Increases attack range by 1 for one turn",
                "effect": {"type": "range_boost", "value": 1, "duration": 1},
                "icon": "R",
                "color": (255, 255, 0)  # Yellow
            },
            ItemType.MOVEMENT_BOOST: {
                "name": "Movement Boost",
                "description": "Increases movement range by 2 for one turn",
                "effect": {"type": "move_boost", "value": 2, "duration": 1},
                "icon": "M",
                "color": (255, 165, 0)  # Orange
            }
        }
        
        return items.get(item_type, None)

# Special abilities
class AbilityType(Enum):
    HEAL = 1
    DOUBLE_ATTACK = 2
    SHIELD = 3
    TELEPORT = 4
    AREA_ATTACK = 5

class Ability:
    @staticmethod
    def get_ability_data(ability_type):
        """Returns data for the specified ability type"""
        abilities = {
            AbilityType.HEAL: {
                "name": "Heal",
                "description": "Restore 30 HP to self or adjacent ally",
                "range": 1,
                "cooldown": 3,
                "icon": "H",
                "color": (0, 255, 0)  # Green
            },
            AbilityType.DOUBLE_ATTACK: {
                "name": "Double Attack",
                "description": "Attack twice in one turn",
                "range": 0,  # Self only
                "cooldown": 4,
                "icon": "D",
                "color": (255, 0, 0)  # Red
            },
            AbilityType.SHIELD: {
                "name": "Shield",
                "description": "Reduce damage taken by 50% for one turn",
                "range": 0,  # Self only
                "cooldown": 3,
                "icon": "S",
                "color": (0, 0, 255)  # Blue
            },
            AbilityType.TELEPORT: {
                "name": "Teleport",
                "description": "Move to any empty tile within 5 spaces",
                "range": 5,
                "cooldown": 5,
                "icon": "T",
                "color": (128, 0, 128)  # Purple
            },
            AbilityType.AREA_ATTACK: {
                "name": "Area Attack",
                "description": "Deal damage to all enemies in a 1-tile radius",
                "range": 2,
                "cooldown": 4,
                "icon": "A",
                "color": (255, 165, 0)  # Orange
            }
        }
        
        return abilities.get(ability_type, None)

# Tutorial messages
class Tutorial:
    @staticmethod
    def get_tutorial_steps():
        """Returns a list of tutorial steps"""
        return [
            {
                "title": "Welcome to the Strategy Game!",
                "message": "This tutorial will guide you through the basics of gameplay.",
                "trigger": "start"
            },
            {
                "title": "Select a Unit",
                "message": "Click on one of your units (left side) to select it.",
                "trigger": "select_unit"
            },
            {
                "title": "Movement",
                "message": "Green outlines show where your selected unit can move. Click on a highlighted tile to move there.",
                "trigger": "show_movement"
            },
            {
                "title": "Attack",
                "message": "Red outlines show enemies you can attack. Click on an enemy to attack it.",
                "trigger": "show_attack"
            },
            {
                "title": "Special Abilities",
                "message": "Each unit has a special ability. Click the ability button or press A to use it when available.",
                "trigger": "show_abilities"
            },
            {
                "title": "Items",
                "message": "Units can carry up to 2 items. Click the inventory button or press I to view and use items.",
                "trigger": "show_inventory"
            },
            {
                "title": "End Turn",
                "message": "When you're done with all your moves, click 'End Turn' to let the AI play.",
                "trigger": "end_turn"
            }
        ]

# Save/Load functions
def save_game(game_state, filename="savegame.json"):
    """Save the game state to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(game_state, f)
    print(f"Game saved to {filename}")

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
