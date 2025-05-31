class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.max_levels = 3
        
    def get_level_count(self):
        """Returns the total number of available levels"""
        return self.max_levels
        
    def get_level_data(self, level_number):
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
                    {"x": 7, "y": 3, "type": "tree"},
                    {"x": 7, "y": 4, "type": "tree"},
                    {"x": 8, "y": 4, "type": "tree"},
                    {"x": 8, "y": 5, "type": "tree"},
                    {"x": 7, "y": 8, "type": "rock"},
                    {"x": 8, "y": 8, "type": "rock"},
                    {"x": 8, "y": 9, "type": "rock"}
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
                    {"x": 5, "y": 2, "type": "rock"},
                    {"x": 5, "y": 3, "type": "rock"},
                    {"x": 6, "y": 3, "type": "rock"},
                    {"x": 6, "y": 4, "type": "rock"},
                    {"x": 7, "y": 4, "type": "tree"},
                    {"x": 7, "y": 5, "type": "tree"},
                    {"x": 8, "y": 5, "type": "tree"},
                    {"x": 8, "y": 6, "type": "tree"},
                    {"x": 9, "y": 6, "type": "rock"},
                    {"x": 9, "y": 7, "type": "rock"},
                    {"x": 8, "y": 7, "type": "rock"},
                    {"x": 8, "y": 8, "type": "tree"},
                    {"x": 7, "y": 8, "type": "tree"},
                    {"x": 7, "y": 9, "type": "tree"},
                    {"x": 6, "y": 9, "type": "rock"},
                    {"x": 6, "y": 10, "type": "rock"}
                ]
            }
        }
        
        return maps.get(level_number, maps[1])  # Default to level 1 if level not found
    
    def next_level(self):
        """Advance to the next level if available"""
        if self.current_level < self.max_levels:
            self.current_level += 1
            return True
        return False
