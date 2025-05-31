import pygame
from enum import Enum
import random
from abilities import ItemType, AbilityType, Item, Ability

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Unit types
class UnitType(Enum):
    INFANTRY = 1
    ARCHER = 2
    CAVALRY = 3
    MAGE = 4

class Unit:
    def __init__(self, unit_type, x, y, player, grid_size=50):
        self.unit_type = unit_type
        self.x = x
        self.y = y
        self.player = player  # 0 for player, 1 for AI
        self.selected = False
        self.moved = False
        self.attacked = False
        self.ability_used = False
        self.grid_size = grid_size
        self.inventory = []  # Max 2 items
        self.active_effects = []  # List of active effects/buffs
        self.ability_cooldown = 0
        
        # Set unit stats based on type
        if unit_type == UnitType.INFANTRY:
            self.max_hp = 100
            self.hp = 100
            self.attack = 20
            self.defense = 10
            self.move_range = 3
            self.attack_range = 1
            self.color = RED if player == 0 else BLUE
            self.ability = AbilityType.SHIELD
        elif unit_type == UnitType.ARCHER:
            self.max_hp = 70
            self.hp = 70
            self.attack = 15
            self.defense = 5
            self.move_range = 2
            self.attack_range = 3
            self.color = GREEN if player == 0 else YELLOW
            self.ability = AbilityType.DOUBLE_ATTACK
        elif unit_type == UnitType.CAVALRY:
            self.max_hp = 90
            self.hp = 90
            self.attack = 25
            self.defense = 8
            self.move_range = 5
            self.attack_range = 1
            self.color = YELLOW if player == 0 else GREEN
            self.ability = AbilityType.TELEPORT
        elif unit_type == UnitType.MAGE:
            self.max_hp = 60
            self.hp = 60
            self.attack = 30
            self.defense = 3
            self.move_range = 2
            self.attack_range = 2
            self.color = PURPLE if player == 0 else WHITE
            self.ability = AbilityType.AREA_ATTACK
            
        # Give starting items to player units
        if player == 0:
            if unit_type == UnitType.INFANTRY:
                self.add_item(ItemType.DEFENSE_SHIELD)
            elif unit_type == UnitType.ARCHER:
                self.add_item(ItemType.RANGE_EXTENDER)
            elif unit_type == UnitType.CAVALRY:
                self.add_item(ItemType.MOVEMENT_BOOST)
            elif unit_type == UnitType.MAGE:
                self.add_item(ItemType.DAMAGE_BOOSTER)
                
            # All player units get a health potion
            self.add_item(ItemType.HEALTH_POTION)
    
    def draw(self, screen):
        # Draw unit on the grid
        rect = pygame.Rect(self.x * self.grid_size, self.y * self.grid_size, self.grid_size, self.grid_size)
        pygame.draw.rect(screen, self.color, rect)
        
        # Draw border if selected
        if self.selected:
            pygame.draw.rect(screen, WHITE, rect, 3)
        
        # Draw health bar with background
        # Background (red)
        health_bg_rect = pygame.Rect(self.x * self.grid_size, self.y * self.grid_size - 8, self.grid_size, 5)
        pygame.draw.rect(screen, RED, health_bg_rect)
        
        # Foreground (green) - scales with health percentage
        health_width = int((self.hp / self.max_hp) * self.grid_size)
        health_rect = pygame.Rect(self.x * self.grid_size, self.y * self.grid_size - 8, health_width, 5)
        pygame.draw.rect(screen, GREEN, health_rect)
        
        # Draw unit type indicator
        font = pygame.font.SysFont(None, 20)
        if self.unit_type == UnitType.INFANTRY:
            text = font.render("I", True, WHITE)
        elif self.unit_type == UnitType.ARCHER:
            text = font.render("A", True, WHITE)
        elif self.unit_type == UnitType.CAVALRY:
            text = font.render("C", True, WHITE)
        elif self.unit_type == UnitType.MAGE:
            text = font.render("M", True, WHITE)
        
        screen.blit(text, (self.x * self.grid_size + self.grid_size // 2 - 5, self.y * self.grid_size + self.grid_size // 2 - 5))
        
        # Draw active effects indicators
        if self.active_effects:
            effect_font = pygame.font.SysFont(None, 16)
            for i, effect in enumerate(self.active_effects):
                effect_text = effect_font.render(effect["icon"], True, effect["color"])
                screen.blit(effect_text, (self.x * self.grid_size + 5 + (i * 10), self.y * self.grid_size + 5))
        
        # Draw ability cooldown if applicable
        if self.ability_cooldown > 0:
            cooldown_text = font.render(str(self.ability_cooldown), True, WHITE)
            pygame.draw.circle(screen, GRAY, 
                              (self.x * self.grid_size + self.grid_size - 10, 
                               self.y * self.grid_size + 10), 8)
            screen.blit(cooldown_text, (self.x * self.grid_size + self.grid_size - 13, 
                                       self.y * self.grid_size + 5))
    
    def can_move_to(self, x, y, units, obstacles):
        # Check if the position is within move range
        distance = abs(self.x - x) + abs(self.y - y)
        
        # Get actual move range including any active effects
        actual_move_range = self.get_stat_with_effects("move_range")
        
        if distance > actual_move_range or self.moved:
            return False
        
        # Check if the position is occupied by a unit
        for unit in units:
            if unit.x == x and unit.y == y:
                return False
        
        # Check if the position is blocked by an obstacle
        for obstacle in obstacles:
            if obstacle["x"] == x and obstacle["y"] == y:
                return False
        
        # Check if the position is within grid bounds
        if x < 0 or x >= 16 or y < 0 or y >= 12:  # Using default grid size
            return False
        
        return True
    
    def can_attack(self, target):
        # Check if the target is within attack range
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        
        # Get actual attack range including any active effects
        actual_attack_range = self.get_stat_with_effects("attack_range")
        
        if distance > actual_attack_range or self.attacked:
            return False
        
        # Check if the target is an enemy
        if self.player == target.player:
            return False
        
        return True
    
    def attack_unit(self, target):
        # Get actual attack value including any active effects
        actual_attack = self.get_stat_with_effects("attack")
        
        # Calculate damage based on attack and defense
        damage = max(1, actual_attack - target.get_stat_with_effects("defense") // 2)
        
        # Apply damage reduction if target has shield effect
        for effect in target.active_effects:
            if effect["type"] == "shield":
                damage = int(damage * 0.5)  # 50% damage reduction
                break
        
        target.hp -= damage
        self.attacked = True
        
        # If double attack is active, don't mark as attacked yet
        for effect in self.active_effects:
            if effect["type"] == "double_attack" and effect["uses"] > 0:
                self.attacked = False
                effect["uses"] -= 1
                if effect["uses"] <= 0:
                    self.active_effects.remove(effect)
                break
        
        return damage
    
    def use_ability(self, target_x=None, target_y=None, units=None):
        """Use the unit's special ability"""
        if self.ability_used or self.ability_cooldown > 0:
            return False, "Ability on cooldown"
        
        ability_data = Ability.get_ability_data(self.ability)
        result = False
        message = ""
        
        if self.ability == AbilityType.HEAL:
            # Heal self or adjacent ally
            if target_x is not None and target_y is not None and units is not None:
                # Find target unit
                target_unit = None
                for unit in units:
                    if unit.x == target_x and unit.y == target_y:
                        target_unit = unit
                        break
                
                if target_unit and target_unit.player == self.player:
                    # Check if target is in range
                    distance = abs(self.x - target_x) + abs(self.y - target_y)
                    if distance <= ability_data["range"]:
                        target_unit.hp = min(target_unit.max_hp, target_unit.hp + 30)
                        result = True
                        message = f"Healed {target_unit.unit_type.name} for 30 HP"
                    else:
                        message = "Target out of range"
                else:
                    message = "Invalid target"
            else:
                # Heal self
                self.hp = min(self.max_hp, self.hp + 30)
                result = True
                message = "Healed self for 30 HP"
                
        elif self.ability == AbilityType.DOUBLE_ATTACK:
            # Allow attacking twice
            self.active_effects.append({
                "type": "double_attack",
                "duration": 1,
                "uses": 1,
                "icon": "D",
                "color": RED
            })
            result = True
            message = "Double Attack activated"
            
        elif self.ability == AbilityType.SHIELD:
            # Reduce damage taken
            self.active_effects.append({
                "type": "shield",
                "duration": 1,
                "icon": "S",
                "color": BLUE
            })
            result = True
            message = "Shield activated"
            
        elif self.ability == AbilityType.TELEPORT:
            # Teleport to target location
            if target_x is not None and target_y is not None and units is not None:
                # Check if target location is valid
                can_teleport = True
                for unit in units:
                    if unit.x == target_x and unit.y == target_y:
                        can_teleport = False
                        break
                
                # Check if target is in range
                distance = abs(self.x - target_x) + abs(self.y - target_y)
                if distance <= ability_data["range"] and can_teleport:
                    self.x = target_x
                    self.y = target_y
                    result = True
                    message = "Teleported successfully"
                else:
                    message = "Invalid teleport location"
            else:
                message = "No target specified"
                
        elif self.ability == AbilityType.AREA_ATTACK:
            # Attack all enemies in a 1-tile radius
            if units is not None:
                targets_hit = 0
                for unit in units:
                    if unit.player != self.player:
                        distance = abs(self.x - unit.x) + abs(self.y - unit.y)
                        if distance <= ability_data["range"]:
                            damage = max(1, self.attack // 2)  # Area attack does half damage
                            unit.hp -= damage
                            targets_hit += 1
                
                if targets_hit > 0:
                    result = True
                    message = f"Area attack hit {targets_hit} enemies"
                else:
                    message = "No targets in range"
            else:
                message = "No units specified"
        
        if result:
            self.ability_used = True
            self.ability_cooldown = ability_data["cooldown"]
        
        return result, message
    
    def use_item(self, item_index):
        """Use an item from the unit's inventory"""
        if item_index < 0 or item_index >= len(self.inventory):
            return False, "Invalid item index"
        
        item_type = self.inventory[item_index]
        item_data = Item.get_item_data(item_type)
        
        if not item_data:
            return False, "Invalid item"
        
        effect = item_data["effect"]
        result = False
        message = ""
        
        if effect["type"] == "heal":
            # Heal the unit
            self.hp = min(self.max_hp, self.hp + effect["value"])
            result = True
            message = f"Healed for {effect['value']} HP"
            
        elif effect["type"] == "attack_boost":
            # Add attack boost effect
            self.active_effects.append({
                "type": "attack_boost",
                "value": effect["value"],
                "duration": effect["duration"],
                "icon": "D",
                "color": RED
            })
            result = True
            message = f"Attack increased by {effect['value']} for {effect['duration']} turn(s)"
            
        elif effect["type"] == "defense_boost":
            # Add defense boost effect
            self.active_effects.append({
                "type": "defense_boost",
                "value": effect["value"],
                "duration": effect["duration"],
                "icon": "S",
                "color": BLUE
            })
            result = True
            message = f"Defense increased by {effect['value']} for {effect['duration']} turn(s)"
            
        elif effect["type"] == "range_boost":
            # Add range boost effect
            self.active_effects.append({
                "type": "range_boost",
                "value": effect["value"],
                "duration": effect["duration"],
                "icon": "R",
                "color": YELLOW
            })
            result = True
            message = f"Attack range increased by {effect['value']} for {effect['duration']} turn(s)"
            
        elif effect["type"] == "move_boost":
            # Add movement boost effect
            self.active_effects.append({
                "type": "move_boost",
                "value": effect["value"],
                "duration": effect["duration"],
                "icon": "M",
                "color": ORANGE
            })
            result = True
            message = f"Movement range increased by {effect['value']} for {effect['duration']} turn(s)"
        
        if result:
            # Remove the item from inventory
            self.inventory.pop(item_index)
        
        return result, message
    
    def add_item(self, item_type):
        """Add an item to the unit's inventory if there's space"""
        if len(self.inventory) < 2:
            self.inventory.append(item_type)
            return True
        return False
    
    def get_stat_with_effects(self, stat_name):
        """Get a stat value including any active effects"""
        base_value = getattr(self, stat_name, 0)
        bonus = 0
        
        for effect in self.active_effects:
            if effect["type"] == f"{stat_name}_boost" and "value" in effect:
                bonus += effect["value"]
        
        return base_value + bonus
    
    def update_effects(self):
        """Update active effects at the end of turn"""
        # Decrease cooldown
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1
        
        # Update effect durations
        for effect in list(self.active_effects):
            if "duration" in effect:
                effect["duration"] -= 1
                if effect["duration"] <= 0:
                    self.active_effects.remove(effect)
    
    def reset_turn(self):
        """Reset unit state for a new turn"""
        self.moved = False
        self.attacked = False
        self.ability_used = False
        self.update_effects()
    
    def to_dict(self):
        """Convert unit to dictionary for saving"""
        return {
            "unit_type": self.unit_type.name,
            "x": self.x,
            "y": self.y,
            "player": self.player,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "move_range": self.move_range,
            "attack_range": self.attack_range,
            "ability": self.ability.name,
            "ability_cooldown": self.ability_cooldown,
            "inventory": [item.name for item in self.inventory],
            "active_effects": self.active_effects
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a unit from dictionary data"""
        unit_type = UnitType[data["unit_type"]]
        unit = cls(unit_type, data["x"], data["y"], data["player"])
        
        # Restore stats
        unit.hp = data["hp"]
        unit.max_hp = data["max_hp"]
        unit.attack = data["attack"]
        unit.defense = data["defense"]
        unit.move_range = data["move_range"]
        unit.attack_range = data["attack_range"]
        
        # Restore ability and cooldown
        unit.ability = AbilityType[data["ability"]]
        unit.ability_cooldown = data["ability_cooldown"]
        
        # Restore inventory
        unit.inventory = [ItemType[item] for item in data["inventory"]]
        
        # Restore active effects
        unit.active_effects = data["active_effects"]
        
        return unit
