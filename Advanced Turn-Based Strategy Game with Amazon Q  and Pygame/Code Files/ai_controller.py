import random
from enum import Enum
import math
from abilities import AbilityType, Ability

class AIStrategy(Enum):
    AGGRESSIVE = 1    # Focus on attacking player units
    DEFENSIVE = 2     # Focus on protecting own units
    BALANCED = 3      # Balance between attack and defense
    ABILITY_FOCUSED = 4  # Prioritize using abilities

class AIController:
    def __init__(self, difficulty=1):
        """
        Initialize the AI controller with a difficulty level
        difficulty: 1 (Easy), 2 (Medium), 3 (Hard)
        """
        self.difficulty = difficulty
        # Set strategy based on difficulty
        if difficulty == 1:
            self.strategy = AIStrategy.BALANCED
        elif difficulty == 2:
            self.strategy = random.choice([AIStrategy.AGGRESSIVE, AIStrategy.DEFENSIVE])
        else:
            self.strategy = random.choice([AIStrategy.AGGRESSIVE, AIStrategy.DEFENSIVE, AIStrategy.ABILITY_FOCUSED])
        
        # AI decision weights (adjusted by difficulty)
        self.weights = {
            "attack_low_hp": 0.8 + (difficulty * 0.1),  # Prefer attacking low HP units
            "attack_high_threat": 0.6 + (difficulty * 0.15),  # Prefer attacking high threat units
            "use_ability": 0.5 + (difficulty * 0.2),  # Chance to use ability when available
            "move_to_attack": 0.7 + (difficulty * 0.1),  # Prefer moving to attack position
            "move_to_safety": 0.4 + (difficulty * 0.15),  # Prefer moving to safer positions
            "target_selection": 0.5 + (difficulty * 0.2),  # Sophistication in target selection
            "group_cohesion": 0.3 + (difficulty * 0.2)  # Tendency to keep units together
        }
        
        # Cache for pathfinding and threat calculations
        self.path_cache = {}
        self.threat_cache = {}
        
    def reset_caches(self):
        """Reset the caches when the game state changes significantly"""
        self.path_cache = {}
        self.threat_cache = {}
    
    def calculate_unit_threat(self, unit):
        """Calculate how threatening a unit is based on its stats and abilities"""
        # Cache check
        cache_key = f"{unit.unit_type.name}_{unit.hp}_{unit.attack}_{unit.ability_cooldown}"
        if cache_key in self.threat_cache:
            return self.threat_cache[cache_key]
            
        # Base threat is attack power
        threat = unit.attack * 1.0
        
        # Adjust for HP (lower HP means less threat)
        hp_factor = unit.hp / unit.max_hp
        threat *= (0.5 + (0.5 * hp_factor))
        
        # Adjust for range (higher range means more threat)
        threat *= (1.0 + (unit.attack_range * 0.2))
        
        # Adjust for mobility (higher mobility means more threat)
        threat *= (1.0 + (unit.move_range * 0.1))
        
        # Adjust for ability availability
        if unit.ability_cooldown == 0 and not unit.ability_used:
            # Different abilities have different threat levels
            if unit.ability == AbilityType.AREA_ATTACK:
                threat *= 1.5  # Area attack is very threatening
            elif unit.ability == AbilityType.DOUBLE_ATTACK:
                threat *= 1.4  # Double attack is quite threatening
            elif unit.ability == AbilityType.TELEPORT:
                threat *= 1.3  # Teleport adds mobility threat
            else:
                threat *= 1.2  # Other abilities are moderately threatening
        
        # Cache the result
        self.threat_cache[cache_key] = threat
        return threat
    
    def find_best_move(self, unit, units, obstacles, grid_width, grid_height):
        """Find the best move for a unit based on the current game state"""
        player_units = [u for u in units if u.player == 0]
        ai_units = [u for u in units if u.player == 1]
        
        # If no player units, no need to move
        if not player_units:
            return None
            
        # Get all possible moves
        possible_moves = []
        for dx in range(-unit.move_range, unit.move_range + 1):
            for dy in range(-unit.move_range, unit.move_range + 1):
                if abs(dx) + abs(dy) <= unit.move_range:
                    new_x, new_y = unit.x + dx, unit.y + dy
                    if self.is_valid_position(new_x, new_y, units, obstacles, grid_width, grid_height):
                        possible_moves.append((new_x, new_y))
        
        if not possible_moves:
            return None
            
        # Score each move
        scored_moves = []
        for move_x, move_y in possible_moves:
            score = self.evaluate_move(unit, move_x, move_y, player_units, ai_units, obstacles, grid_width, grid_height)
            scored_moves.append((move_x, move_y, score))
        
        # Sort by score (highest first)
        scored_moves.sort(key=lambda x: x[2], reverse=True)
        
        # Add some randomness based on difficulty
        # On easy, might not always pick the best move
        if self.difficulty == 1 and random.random() < 0.3:
            # Pick from top 3 moves if available
            top_n = min(3, len(scored_moves))
            return scored_moves[random.randint(0, top_n-1)][:2]
        
        # Return best move
        return scored_moves[0][:2] if scored_moves else None
    
    def is_valid_position(self, x, y, units, obstacles, grid_width, grid_height):
        """Check if a position is valid for movement"""
        # Check grid boundaries
        if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
            return False
            
        # Check for units
        for unit in units:
            if unit.x == x and unit.y == y:
                return False
                
        # Check for obstacles
        for obstacle in obstacles:
            if obstacle["x"] == x and obstacle["y"] == y:
                return False
                
        return True
    
    def evaluate_move(self, unit, move_x, move_y, player_units, ai_units, obstacles, grid_width, grid_height):
        """Evaluate a potential move and return a score"""
        score = 0
        
        # Calculate distance to closest player unit
        min_distance_to_player = float('inf')
        closest_player_unit = None
        for player_unit in player_units:
            distance = abs(move_x - player_unit.x) + abs(move_y - player_unit.y)
            if distance < min_distance_to_player:
                min_distance_to_player = distance
                closest_player_unit = player_unit
        
        # Calculate distance to closest AI unit
        min_distance_to_ally = float('inf')
        for ai_unit in ai_units:
            if ai_unit != unit:
                distance = abs(move_x - ai_unit.x) + abs(move_y - ai_unit.y)
                min_distance_to_ally = min(min_distance_to_ally, distance)
        
        # Adjust score based on strategy
        if self.strategy == AIStrategy.AGGRESSIVE:
            # Prefer positions closer to player units
            score -= min_distance_to_player * 10
            
            # But not too close to other AI units (avoid clustering)
            if min_distance_to_ally < 2:
                score -= 20
                
        elif self.strategy == AIStrategy.DEFENSIVE:
            # Prefer positions that are not too close to player units
            if min_distance_to_player < unit.attack_range:
                score += 30  # Good attack position
            else:
                score -= (min_distance_to_player - unit.attack_range) * 5
                
            # Prefer positions closer to other AI units
            if min_distance_to_ally > 0:  # Not on top of another unit
                score += max(0, (5 - min_distance_to_ally) * 10)
                
        elif self.strategy == AIStrategy.BALANCED:
            # Balance between attack and defense
            if min_distance_to_player <= unit.attack_range:
                score += 40  # Good attack position
            else:
                score -= (min_distance_to_player - unit.attack_range) * 3
                
            # Moderate grouping with allies
            if 1 <= min_distance_to_ally <= 3:
                score += 15
                
        elif self.strategy == AIStrategy.ABILITY_FOCUSED:
            # Position for optimal ability use
            if unit.ability == AbilityType.AREA_ATTACK:
                # Count how many player units would be in area attack range
                targets_in_range = 0
                for player_unit in player_units:
                    distance = abs(move_x - player_unit.x) + abs(move_y - player_unit.y)
                    if distance <= Ability.get_ability_data(unit.ability)["range"]:
                        targets_in_range += 1
                        
                        # Count nearby player units for each target
                        for other_player_unit in player_units:
                            if player_unit != other_player_unit:
                                other_distance = abs(player_unit.x - other_player_unit.x) + abs(player_unit.y - other_player_unit.y)
                                if other_distance <= 1:  # 1-tile radius
                                    targets_in_range += 0.5  # Count as half a target
                
                score += targets_in_range * 25
            else:
                # For other abilities, use balanced approach
                if min_distance_to_player <= unit.attack_range:
                    score += 40
                else:
                    score -= (min_distance_to_player - unit.attack_range) * 3
        
        # Consider safety - avoid positions where multiple player units could attack
        threat_level = 0
        for player_unit in player_units:
            attack_distance = abs(move_x - player_unit.x) + abs(move_y - player_unit.y)
            if attack_distance <= player_unit.attack_range:
                threat_level += self.calculate_unit_threat(player_unit)
        
        # Higher difficulty AIs are better at avoiding danger
        score -= threat_level * (0.5 + (self.difficulty * 0.25))
        
        # Consider terrain and positioning
        # Prefer positions that are not easily surrounded
        surrounded_count = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            check_x, check_y = move_x + dx, move_y + dy
            if not self.is_valid_position(check_x, check_y, [], obstacles, grid_width, grid_height):
                surrounded_count += 1
        
        # Being surrounded is bad, but having some cover is good
        if surrounded_count >= 3:
            score -= 30  # Too surrounded
        elif surrounded_count >= 1:
            score += 10  # Some cover is good
            
        # Add a small random factor to avoid predictability
        score += random.uniform(-5, 5)
        
        return score
    
    def find_best_attack_target(self, unit, units):
        """Find the best target for an attack"""
        player_units = [u for u in units if u.player == 0]
        attackable_units = [u for u in player_units if unit.can_attack(u)]
        
        if not attackable_units:
            return None
            
        # Score each potential target
        scored_targets = []
        for target in attackable_units:
            score = self.evaluate_attack_target(unit, target)
            scored_targets.append((target, score))
            
        # Sort by score (highest first)
        scored_targets.sort(key=lambda x: x[1], reverse=True)
        
        # Add some randomness based on difficulty
        if self.difficulty == 1 and random.random() < 0.3 and len(scored_targets) > 1:
            # Pick from top 2 targets if available
            top_n = min(2, len(scored_targets))
            return scored_targets[random.randint(0, top_n-1)][0]
            
        # Return best target
        return scored_targets[0][0] if scored_targets else None
    
    def evaluate_attack_target(self, attacker, target):
        """Evaluate a potential attack target and return a score"""
        score = 0
        
        # Base score - prefer low HP targets that can be killed
        estimated_damage = max(1, attacker.attack - target.defense // 2)
        
        # Check for shield effect
        for effect in target.active_effects:
            if effect["type"] == "shield":
                estimated_damage = int(estimated_damage * 0.5)  # 50% damage reduction
                break
                
        # Killing a unit is highly valuable
        if target.hp <= estimated_damage:
            score += 100
        else:
            # Otherwise, prefer units with lower HP
            hp_percentage = target.hp / target.max_hp
            score += 50 * (1 - hp_percentage)
            
        # Consider target threat level
        target_threat = self.calculate_unit_threat(target)
        score += target_threat * self.weights["attack_high_threat"]
        
        # Consider target type
        if target.unit_type.name == "MAGE":
            score += 20  # Mages are high priority targets
        elif target.unit_type.name == "ARCHER":
            score += 15  # Archers are also priority targets
        elif target.unit_type.name == "CAVALRY":
            score += 10  # Cavalry are medium priority
            
        # Consider if target has used its turn already
        if target.moved and target.attacked:
            score -= 10  # Less valuable to attack units that have already acted
            
        # Add a small random factor
        score += random.uniform(-5, 5)
        
        return score
    
    def should_use_ability(self, unit, units, obstacles, grid_width, grid_height):
        """Decide if the unit should use its ability"""
        if unit.ability_used or unit.ability_cooldown > 0:
            return False
            
        # Base chance from weights
        base_chance = self.weights["use_ability"]
        
        # Adjust based on ability type and situation
        player_units = [u for u in units if u.player == 0]
        ai_units = [u for u in units if u.player == 1]
        
        if unit.ability == AbilityType.SHIELD:
            # Use shield if under threat
            threat_level = 0
            for player_unit in player_units:
                distance = abs(unit.x - player_unit.x) + abs(unit.y - player_unit.y)
                if distance <= player_unit.attack_range + player_unit.move_range:
                    threat_level += self.calculate_unit_threat(player_unit)
                    
            # More likely to use shield when threatened
            return random.random() < (base_chance * (0.5 + min(1.5, threat_level / 50)))
            
        elif unit.ability == AbilityType.DOUBLE_ATTACK:
            # Use double attack if there are good targets
            attackable_units = [u for u in player_units if unit.can_attack(u)]
            if attackable_units:
                # More likely to use if there are multiple targets or high value targets
                if len(attackable_units) > 1:
                    return random.random() < (base_chance * 1.3)
                else:
                    target = attackable_units[0]
                    target_value = self.evaluate_attack_target(unit, target) / 50  # Normalize
                    return random.random() < (base_chance * (0.7 + target_value))
            return False
            
        elif unit.ability == AbilityType.AREA_ATTACK:
            # Count how many targets would be hit by area attack
            ability_data = Ability.get_ability_data(unit.ability)
            best_target_count = 0
            
            for player_unit in player_units:
                distance = abs(unit.x - player_unit.x) + abs(unit.y - player_unit.y)
                if distance <= ability_data["range"]:
                    # Count targets in area
                    targets_in_area = 0
                    for potential_target in player_units:
                        area_distance = abs(player_unit.x - potential_target.x) + abs(player_unit.y - potential_target.y)
                        if area_distance <= 1:  # 1-tile radius
                            targets_in_area += 1
                    
                    best_target_count = max(best_target_count, targets_in_area)
            
            # Use area attack if it would hit multiple targets
            if best_target_count >= 2:
                return random.random() < (base_chance * (0.5 + (best_target_count * 0.25)))
            return False
            
        elif unit.ability == AbilityType.TELEPORT:
            # Use teleport to reach strategic positions
            ability_data = Ability.get_ability_data(unit.ability)
            
            # Find best teleport destination
            best_score = -float('inf')
            for dx in range(-ability_data["range"], ability_data["range"] + 1):
                for dy in range(-ability_data["range"], ability_data["range"] + 1):
                    if abs(dx) + abs(dy) <= ability_data["range"]:
                        new_x, new_y = unit.x + dx, unit.y + dy
                        if self.is_valid_position(new_x, new_y, units, obstacles, grid_width, grid_height):
                            score = self.evaluate_move(unit, new_x, new_y, player_units, ai_units, obstacles, grid_width, grid_height)
                            best_score = max(best_score, score)
            
            # Use teleport if there's a significantly better position
            current_score = self.evaluate_move(unit, unit.x, unit.y, player_units, ai_units, obstacles, grid_width, grid_height)
            if best_score > current_score + 30:
                return random.random() < base_chance * 1.5
            return False
            
        # Default case
        return random.random() < base_chance
    
    def use_ability(self, unit, units, obstacles, grid_width, grid_height):
        """Use the unit's ability in the most effective way"""
        if unit.ability_used or unit.ability_cooldown > 0:
            return None
            
        player_units = [u for u in units if u.player == 0]
        ai_units = [u for u in units if u.player == 1]
        ability_data = Ability.get_ability_data(unit.ability)
        
        if unit.ability == AbilityType.SHIELD or unit.ability == AbilityType.DOUBLE_ATTACK:
            # These abilities are used on self
            return {"type": "self"}
            
        elif unit.ability == AbilityType.AREA_ATTACK:
            # Find best target for area attack
            best_target = None
            max_targets = 0
            
            for player_unit in player_units:
                distance = abs(unit.x - player_unit.x) + abs(unit.y - player_unit.y)
                if distance <= ability_data["range"]:
                    # Count targets in area
                    targets_in_area = 0
                    for potential_target in player_units:
                        area_distance = abs(player_unit.x - potential_target.x) + abs(player_unit.y - potential_target.y)
                        if area_distance <= 1:  # 1-tile radius
                            targets_in_area += 1
                    
                    if targets_in_area > max_targets:
                        max_targets = targets_in_area
                        best_target = player_unit
            
            if best_target:
                return {"type": "target", "x": best_target.x, "y": best_target.y}
            return None
            
        elif unit.ability == AbilityType.TELEPORT:
            # Find best teleport destination
            best_pos = None
            best_score = -float('inf')
            
            for dx in range(-ability_data["range"], ability_data["range"] + 1):
                for dy in range(-ability_data["range"], ability_data["range"] + 1):
                    if abs(dx) + abs(dy) <= ability_data["range"]:
                        new_x, new_y = unit.x + dx, unit.y + dy
                        if self.is_valid_position(new_x, new_y, units, obstacles, grid_width, grid_height):
                            score = self.evaluate_move(unit, new_x, new_y, player_units, ai_units, obstacles, grid_width, grid_height)
                            if score > best_score:
                                best_score = score
                                best_pos = (new_x, new_y)
            
            if best_pos:
                return {"type": "position", "x": best_pos[0], "y": best_pos[1]}
            return None
            
        return None
    
    def process_turn(self, ai_units, player_units, all_units, obstacles, grid_width, grid_height):
        """Process the entire AI turn and return the actions to take"""
        # Reset caches at the start of turn
        self.reset_caches()
        
        actions = []
        
        # Process each AI unit
        for unit in ai_units:
            unit_actions = {}
            
            # First, check if we should use ability
            if self.should_use_ability(unit, all_units, obstacles, grid_width, grid_height):
                ability_action = self.use_ability(unit, all_units, obstacles, grid_width, grid_height)
                if ability_action:
                    unit_actions["ability"] = ability_action
            
            # Next, check if we can attack
            attack_target = self.find_best_attack_target(unit, all_units)
            if attack_target:
                unit_actions["attack"] = {"target": attack_target}
            
            # Finally, check if we should move
            if not unit.moved:
                best_move = self.find_best_move(unit, all_units, obstacles, grid_width, grid_height)
                if best_move:
                    unit_actions["move"] = {"x": best_move[0], "y": best_move[1]}
            
            actions.append({"unit": unit, "actions": unit_actions})
        
        return actions
