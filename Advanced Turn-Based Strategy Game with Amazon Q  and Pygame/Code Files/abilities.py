from enum import Enum

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
