import pygame
import sys
import random
from enum import Enum

# Import our modules
from unit import Unit, UnitType
from abilities import AbilityType, ItemType, Ability, Item
from levels import LevelManager
from save_load import save_game, load_game, check_save_exists
from tutorial import Tutorial, TutorialPopup
from sounds import SoundManager

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
GRID_WIDTH = 16
GRID_HEIGHT = 12
GRID_COLOR = (50, 50, 50)
BG_COLOR = (20, 20, 20)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Sound effects
def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
        
def load_sounds(self):
        # Create simple placeholder sounds
        self.sounds['move'] = self._create_beep(220, 100)  # Lower pitch, short
        self.sounds['attack'] = self._create_beep(440, 200)  # Medium pitch, medium
        self.sounds['defeat'] = self._create_beep(110, 500)  # Low pitch, long
        self.sounds['select'] = self._create_beep(660, 50)  # High pitch, very short
        self.sounds['turn'] = self._create_beep(330, 150)  # Medium-low pitch
        self.sounds['victory'] = self._create_beep(880, 400)  # High pitch, long
        self.sounds['ability'] = self._create_beep(550, 300)  # Medium-high pitch
        self.sounds['item'] = self._create_beep(660, 200)  # High pitch, medium
    
    

# Menu classes
class MainMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (20, 20, 20)
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.selected_option = 0
        self.options = ["Start Game", "Level Select", "Quit"]
        
        # Add "Load Game" option if save exists
        if check_save_exists():
            self.options.insert(2, "Load Game")
    
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Draw title
        title = self.title_font.render("Turn-Based Strategy", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.menu_font.render(option, True, color)
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 250 + i * 50))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Quit"

class LevelSelectMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (20, 20, 20)
        self.title_font = pygame.font.SysFont(None, 48)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.info_font = pygame.font.SysFont(None, 24)
        self.selected_level = 0
        
        # Get level data
        self.level_manager = LevelManager()
        self.levels = []
        for i in range(1, self.level_manager.get_level_count() + 1):
            level_data = self.level_manager.get_level_data(i)
            self.levels.append({
                "name": f"Level {i}: {level_data['name']}",
                "difficulty": "Easy" if i == 1 else "Medium" if i == 2 else "Hard"
            })
    
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Draw title
        title = self.title_font.render("Select Level", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 80))
        
        # Draw level options
        for i, level in enumerate(self.levels):
            color = (255, 255, 0) if i == self.selected_level else (255, 255, 255)
            text = self.menu_font.render(level["name"], True, color)
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 180 + i * 70))
            
            # Draw difficulty
            diff_color = (0, 255, 0) if level["difficulty"] == "Easy" else \
                        (255, 255, 0) if level["difficulty"] == "Medium" else \
                        (255, 0, 0)
            diff_text = self.info_font.render(f"Difficulty: {level['difficulty']}", True, diff_color)
            self.screen.blit(diff_text, (self.screen_width // 2 - diff_text.get_width() // 2, 210 + i * 70))
        
        # Draw instructions
        back_text = self.info_font.render("Press ESC to go back", True, (200, 200, 200))
        self.screen.blit(back_text, (self.screen_width // 2 - back_text.get_width() // 2, self.screen_height - 50))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = (self.selected_level - 1) % len(self.levels)
            elif event.key == pygame.K_DOWN:
                self.selected_level = (self.selected_level + 1) % len(self.levels)
            elif event.key == pygame.K_RETURN:
                return self.selected_level + 1  # Return level number (1-based)
            elif event.key == pygame.K_ESCAPE:
                return "Back"
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Back"

class LevelTransition:
    def __init__(self, screen, screen_width, screen_height, level_completed, next_level):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (20, 20, 20)
        self.title_font = pygame.font.SysFont(None, 48)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.info_font = pygame.font.SysFont(None, 24)
        self.level_completed = level_completed
        self.next_level = next_level
        self.timer = 0
        self.max_time = 180  # 3 seconds at 60 FPS
    
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Draw victory message
        title = self.title_font.render(f"Level {self.level_completed} Complete!", True, (255, 255, 0))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 150))
        
        # Draw next level info
        if self.next_level:
            next_text = self.menu_font.render(f"Preparing Level {self.next_level}...", True, (255, 255, 255))
            self.screen.blit(next_text, (self.screen_width // 2 - next_text.get_width() // 2, 250))
        else:
            next_text = self.menu_font.render("Congratulations! You've completed all levels!", True, (255, 255, 255))
            self.screen.blit(next_text, (self.screen_width // 2 - next_text.get_width() // 2, 250))
        
        # Draw progress bar
        progress_width = int((self.timer / self.max_time) * 400)
        pygame.draw.rect(self.screen, (100, 100, 100), (self.screen_width // 2 - 200, 350, 400, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.screen_width // 2 - 200, 350, progress_width, 20))
        
        # Draw skip instruction
        skip_text = self.info_font.render("Press SPACE to continue", True, (200, 200, 200))
        self.screen.blit(skip_text, (self.screen_width // 2 - skip_text.get_width() // 2, 400))
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running and self.timer < self.max_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return self.next_level if self.next_level else "Menu"
            
            self.timer += 1
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return self.next_level if self.next_level else "Menu"

class InventoryMenu:
    def __init__(self, screen, screen_width, screen_height, unit):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent background
        self.unit = unit
        self.title_font = pygame.font.SysFont(None, 36)
        self.item_font = pygame.font.SysFont(None, 24)
        self.selected_item = 0 if unit.inventory else -1
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw inventory panel
        panel_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 100, 300, 200)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), panel_rect, 2)
        
        # Draw title
        title = self.title_font.render(f"{self.unit.unit_type.name} Inventory", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 90))
        
        # Draw items
        if self.unit.inventory:
            for i, item_type in enumerate(self.unit.inventory):
                item_data = Item.get_item_data(item_type)
                
                # Highlight selected item
                if i == self.selected_item:
                    select_rect = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2 - 50 + i * 40, 280, 30)
                    pygame.draw.rect(self.screen, (100, 100, 100), select_rect)
                
                # Draw item name and description
                item_name = self.item_font.render(item_data["name"], True, item_data["color"])
                self.screen.blit(item_name, (self.screen_width // 2 - 130, self.screen_height // 2 - 45 + i * 40))
                
                item_desc = self.item_font.render(item_data["description"], True, (200, 200, 200))
                self.screen.blit(item_desc, (self.screen_width // 2 - 130, self.screen_height // 2 - 25 + i * 40))
        else:
            no_items = self.item_font.render("No items in inventory", True, (200, 200, 200))
            self.screen.blit(no_items, (self.screen_width // 2 - no_items.get_width() // 2, self.screen_height // 2 - 20))
        
        # Draw instructions
        instructions = self.item_font.render("Press ENTER to use item, ESC to close", True, (200, 200, 200))
        self.screen.blit(instructions, (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height // 2 + 80))
    
    def handle_event(self, event):
        if not self.unit.inventory:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Close"
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.selected_item > 0:
                    self.selected_item -= 1
            elif event.key == pygame.K_DOWN:
                if self.selected_item < len(self.unit.inventory) - 1:
                    self.selected_item += 1
            elif event.key == pygame.K_RETURN:
                return f"Use:{self.selected_item}"
            elif event.key == pygame.K_ESCAPE:
                return "Close"
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Close"

class AbilityMenu:
    def __init__(self, screen, screen_width, screen_height, unit):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent background
        self.unit = unit
        self.title_font = pygame.font.SysFont(None, 36)
        self.item_font = pygame.font.SysFont(None, 24)
        
        self.ability_data = Ability.get_ability_data(unit.ability)
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw ability panel
        panel_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 100, 300, 200)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), panel_rect, 2)
        
        # Draw title
        title = self.title_font.render(f"{self.unit.unit_type.name} Ability", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 90))
        
        # Draw ability info
        ability_name = self.item_font.render(self.ability_data["name"], True, self.ability_data["color"])
        self.screen.blit(ability_name, (self.screen_width // 2 - 130, self.screen_height // 2 - 45))
        
        ability_desc = self.item_font.render(self.ability_data["description"], True, (200, 200, 200))
        self.screen.blit(ability_desc, (self.screen_width // 2 - 130, self.screen_height // 2 - 20))
        
        cooldown_text = self.item_font.render(f"Cooldown: {self.ability_data['cooldown']} turns", True, (200, 200, 200))
        self.screen.blit(cooldown_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 5))
        
        # Draw current cooldown status
        if self.unit.ability_cooldown > 0:
            status_text = self.item_font.render(f"On cooldown: {self.unit.ability_cooldown} turns remaining", True, (255, 100, 100))
            self.screen.blit(status_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 30))
        elif self.unit.ability_used:
            status_text = self.item_font.render("Already used this turn", True, (255, 100, 100))
            self.screen.blit(status_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 30))
        else:
            status_text = self.item_font.render("Ready to use", True, (100, 255, 100))
            self.screen.blit(status_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 30))
        
        # Draw instructions
        if self.unit.ability_cooldown > 0 or self.unit.ability_used:
            instructions = self.item_font.render("Press ESC to close", True, (200, 200, 200))
        else:
            instructions = self.item_font.render("Press ENTER to use ability, ESC to close", True, (200, 200, 200))
        self.screen.blit(instructions, (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height // 2 + 80))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not self.unit.ability_cooldown > 0 and not self.unit.ability_used:
                return "Use"
            elif event.key == pygame.K_ESCAPE:
                return "Close"
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Close"
# Sound effects
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        # Create simple placeholder sounds
        self.sounds['move'] = self._create_beep(220, 100)  # Lower pitch, short
        self.sounds['attack'] = self._create_beep(440, 200)  # Medium pitch, medium
        self.sounds['defeat'] = self._create_beep(110, 500)  # Low pitch, long
        self.sounds['select'] = self._create_beep(660, 50)  # High pitch, very short
        self.sounds['turn'] = self._create_beep(330, 150)  # Medium-low pitch
        self.sounds['victory'] = self._create_beep(880, 400)  # High pitch, long
        self.sounds['ability'] = self._create_beep(550, 300)  # Medium-high pitch
        self.sounds['item'] = self._create_beep(660, 200)  # High pitch, medium
    
    

# Menu classes
class MainMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (20, 20, 20)
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.selected_option = 0
        self.options = ["Start Game", "Level Select", "Quit"]
        
        # Add "Load Game" option if save exists
        if check_save_exists():
            self.options.insert(2, "Load Game")
    
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Draw title
        title = self.title_font.render("Turn-Based Strategy", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.menu_font.render(option, True, color)
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 250 + i * 50))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Quit"

class LevelSelectMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (20, 20, 20)
        self.title_font = pygame.font.SysFont(None, 48)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.info_font = pygame.font.SysFont(None, 24)
        self.selected_level = 0
        
        # Get level data
        self.level_manager = LevelManager()
        self.levels = []
        for i in range(1, self.level_manager.get_level_count() + 1):
            level_data = self.level_manager.get_level_data(i)
            self.levels.append({
                "name": f"Level {i}: {level_data['name']}",
                "difficulty": "Easy" if i == 1 else "Medium" if i == 2 else "Hard"
            })
    
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Draw title
        title = self.title_font.render("Select Level", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 80))
        
        # Draw level options
        for i, level in enumerate(self.levels):
            color = (255, 255, 0) if i == self.selected_level else (255, 255, 255)
            text = self.menu_font.render(level["name"], True, color)
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 180 + i * 70))
            
            # Draw difficulty
            diff_color = (0, 255, 0) if level["difficulty"] == "Easy" else \
                        (255, 255, 0) if level["difficulty"] == "Medium" else \
                        (255, 0, 0)
            diff_text = self.info_font.render(f"Difficulty: {level['difficulty']}", True, diff_color)
            self.screen.blit(diff_text, (self.screen_width // 2 - diff_text.get_width() // 2, 210 + i * 70))
        
        # Draw instructions
        back_text = self.info_font.render("Press ESC to go back", True, (200, 200, 200))
        self.screen.blit(back_text, (self.screen_width // 2 - back_text.get_width() // 2, self.screen_height - 50))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = (self.selected_level - 1) % len(self.levels)
            elif event.key == pygame.K_DOWN:
                self.selected_level = (self.selected_level + 1) % len(self.levels)
            elif event.key == pygame.K_RETURN:
                return self.selected_level + 1  # Return level number (1-based)
            elif event.key == pygame.K_ESCAPE:
                return "Back"
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Back"

class LevelTransition:
    def __init__(self, screen, screen_width, screen_height, level_completed, next_level):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (20, 20, 20)
        self.title_font = pygame.font.SysFont(None, 48)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.info_font = pygame.font.SysFont(None, 24)
        self.level_completed = level_completed
        self.next_level = next_level
        self.timer = 0
        self.max_time = 180  # 3 seconds at 60 FPS
    
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Draw victory message
        title = self.title_font.render(f"Level {self.level_completed} Complete!", True, (255, 255, 0))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 150))
        
        # Draw next level info
        if self.next_level:
            next_text = self.menu_font.render(f"Preparing Level {self.next_level}...", True, (255, 255, 255))
            self.screen.blit(next_text, (self.screen_width // 2 - next_text.get_width() // 2, 250))
        else:
            next_text = self.menu_font.render("Congratulations! You've completed all levels!", True, (255, 255, 255))
            self.screen.blit(next_text, (self.screen_width // 2 - next_text.get_width() // 2, 250))
        
        # Draw progress bar
        progress_width = int((self.timer / self.max_time) * 400)
        pygame.draw.rect(self.screen, (100, 100, 100), (self.screen_width // 2 - 200, 350, 400, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.screen_width // 2 - 200, 350, progress_width, 20))
        
        # Draw skip instruction
        skip_text = self.info_font.render("Press SPACE to continue", True, (200, 200, 200))
        self.screen.blit(skip_text, (self.screen_width // 2 - skip_text.get_width() // 2, 400))
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running and self.timer < self.max_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return self.next_level if self.next_level else "Menu"
            
            self.timer += 1
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return self.next_level if self.next_level else "Menu"
class InventoryMenu:
    def __init__(self, screen, screen_width, screen_height, unit):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent background
        self.unit = unit
        self.title_font = pygame.font.SysFont(None, 36)
        self.item_font = pygame.font.SysFont(None, 24)
        self.selected_item = 0 if unit.inventory else -1
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw inventory panel
        panel_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 100, 300, 200)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), panel_rect, 2)
        
        # Draw title
        title = self.title_font.render(f"{self.unit.unit_type.name} Inventory", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 90))
        
        # Draw items
        if self.unit.inventory:
            for i, item_type in enumerate(self.unit.inventory):
                item_data = Item.get_item_data(item_type)
                
                # Highlight selected item
                if i == self.selected_item:
                    select_rect = pygame.Rect(self.screen_width // 2 - 140, self.screen_height // 2 - 50 + i * 40, 280, 30)
                    pygame.draw.rect(self.screen, (100, 100, 100), select_rect)
                
                # Draw item name and description
                item_name = self.item_font.render(item_data["name"], True, item_data["color"])
                self.screen.blit(item_name, (self.screen_width // 2 - 130, self.screen_height // 2 - 45 + i * 40))
                
                item_desc = self.item_font.render(item_data["description"], True, (200, 200, 200))
                self.screen.blit(item_desc, (self.screen_width // 2 - 130, self.screen_height // 2 - 25 + i * 40))
        else:
            no_items = self.item_font.render("No items in inventory", True, (200, 200, 200))
            self.screen.blit(no_items, (self.screen_width // 2 - no_items.get_width() // 2, self.screen_height // 2 - 20))
        
        # Draw instructions
        instructions = self.item_font.render("Press ENTER to use item, ESC to close", True, (200, 200, 200))
        self.screen.blit(instructions, (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height // 2 + 80))
    
    def handle_event(self, event):
        if not self.unit.inventory:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Close"
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.selected_item > 0:
                    self.selected_item -= 1
            elif event.key == pygame.K_DOWN:
                if self.selected_item < len(self.unit.inventory) - 1:
                    self.selected_item += 1
            elif event.key == pygame.K_RETURN:
                return f"Use:{self.selected_item}"
            elif event.key == pygame.K_ESCAPE:
                return "Close"
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Close"

class AbilityMenu:
    def __init__(self, screen, screen_width, screen_height, unit):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent background
        self.unit = unit
        self.title_font = pygame.font.SysFont(None, 36)
        self.item_font = pygame.font.SysFont(None, 24)
        
        self.ability_data = Ability.get_ability_data(unit.ability)
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw ability panel
        panel_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 100, 300, 200)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), panel_rect, 2)
        
        # Draw title
        title = self.title_font.render(f"{self.unit.unit_type.name} Ability", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 90))
        
        # Draw ability info
        ability_name = self.item_font.render(self.ability_data["name"], True, self.ability_data["color"])
        self.screen.blit(ability_name, (self.screen_width // 2 - 130, self.screen_height // 2 - 45))
        
        ability_desc = self.item_font.render(self.ability_data["description"], True, (200, 200, 200))
        self.screen.blit(ability_desc, (self.screen_width // 2 - 130, self.screen_height // 2 - 20))
        
        cooldown_text = self.item_font.render(f"Cooldown: {self.ability_data['cooldown']} turns", True, (200, 200, 200))
        self.screen.blit(cooldown_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 5))
        
        # Draw current cooldown status
        if self.unit.ability_cooldown > 0:
            status_text = self.item_font.render(f"On cooldown: {self.unit.ability_cooldown} turns remaining", True, (255, 100, 100))
            self.screen.blit(status_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 30))
        elif self.unit.ability_used:
            status_text = self.item_font.render("Already used this turn", True, (255, 100, 100))
            self.screen.blit(status_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 30))
        else:
            status_text = self.item_font.render("Ready to use", True, (100, 255, 100))
            self.screen.blit(status_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 30))
        
        # Draw instructions
        if self.unit.ability_cooldown > 0 or self.unit.ability_used:
            instructions = self.item_font.render("Press ESC to close", True, (200, 200, 200))
        else:
            instructions = self.item_font.render("Press ENTER to use ability, ESC to close", True, (200, 200, 200))
        self.screen.blit(instructions, (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height // 2 + 80))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not self.unit.ability_cooldown > 0 and not self.unit.ability_used:
                return "Use"
            elif event.key == pygame.K_ESCAPE:
                return "Close"
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                
                result = self.handle_event(event)
                if result:
                    return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "Close"
# Game class
class Game:
    def __init__(self, screen=None, sound_manager=None, level_number=1, load_saved_game=False):
        if screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Turn-Based Strategy Game")
        else:
            self.screen = screen
            
        self.clock = pygame.time.Clock()
        self.units = []
        self.obstacles = []
        self.selected_unit = None
        self.current_player = 0  # 0 for player, 1 for AI
        self.game_over = False
        self.winner = None
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.turn_count = 1
        self.ability_target_mode = False
        self.teleport_target = None
        
        # Sound manager
        if sound_manager is None:
            self.sound_manager = SoundManager()
        else:
            self.sound_manager = sound_manager
        
        # Level management
        self.level_manager = LevelManager()
        self.current_level = level_number
        self.level_manager.current_level = level_number
        
        # Tutorial system
        self.tutorial = Tutorial()
        self.show_tutorial = self.current_level == 1  # Show tutorial on first level
        self.current_tutorial = None
            
        # Load saved game or initialize new game
        if load_saved_game:
            saved_game = load_game()
            if saved_game:
                self.load_game_state(saved_game)
            else:
                self.initialize_level(level_number)
        else:
            self.initialize_level(level_number)
    
    def initialize_level(self, level_number):
        """Initialize a new level with units and obstacles"""
        self.units = []
        self.obstacles = []
        self.current_level = level_number
        self.turn_count = 1
        self.game_over = False
        self.winner = None
        
        # Get level data
        level_data = self.level_manager.get_level_data(level_number)
        
        # Create player units
        for unit_data in level_data["player_units"]:
            unit_type = UnitType[unit_data["type"]]
            self.units.append(Unit(unit_type, unit_data["x"], unit_data["y"], 0))
        
        # Create enemy units
        for unit_data in level_data["enemy_units"]:
            unit_type = UnitType[unit_data["type"]]
            self.units.append(Unit(unit_type, unit_data["x"], unit_data["y"], 1))
        
        # Set obstacles
        self.obstacles = level_data["obstacles"]
        
        # Start tutorial if needed
        if level_data.get("tutorial", False) and self.show_tutorial:
            self.current_tutorial = self.tutorial.start()
    
    def load_game_state(self, saved_game):
        """Load game state from saved data"""
        self.current_level = saved_game["current_level"]
        self.current_player = saved_game["current_player"]
        self.turn_count = saved_game["turn_count"]
        self.obstacles = saved_game["obstacles"]
        
        # Load units
        self.units = []
        for unit_data in saved_game["units"]:
            unit_type = UnitType[unit_data["unit_type"]]
            unit = Unit(unit_type, unit_data["x"], unit_data["y"], unit_data["player"])
            unit.hp = unit_data["hp"]
            unit.max_hp = unit_data["max_hp"]
            unit.attack = unit_data["attack"]
            unit.defense = unit_data["defense"]
            unit.move_range = unit_data["move_range"]
            unit.attack_range = unit_data["attack_range"]
            unit.ability = AbilityType[unit_data["ability"]]
            unit.ability_cooldown = unit_data["ability_cooldown"]
            unit.inventory = [ItemType[item] for item in unit_data["inventory"]]
            unit.active_effects = unit_data["active_effects"]
            self.units.append(unit)
    
    def save_game_state(self):
        """Save current game state"""
        game_state = {
            "current_level": self.current_level,
            "current_player": self.current_player,
            "turn_count": self.turn_count,
            "units": [unit.to_dict() for unit in self.units],
            "obstacles": self.obstacles
        }
        
        success = save_game(game_state)
        return success
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
    
    def draw_obstacles(self):
        for obstacle in self.obstacles:
            x, y = obstacle["x"], obstacle["y"]
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Different colors for different obstacle types
            if obstacle.get("type") == "tree":
                color = (0, 100, 0)  # Dark green for trees
            elif obstacle.get("type") == "rock":
                color = (100, 100, 100)  # Gray for rocks
            else:
                color = (70, 70, 70)  # Default dark gray
                
            pygame.draw.rect(self.screen, color, rect)
            
            # Draw obstacle icon
            font = pygame.font.SysFont(None, 24)
            if obstacle.get("type") == "tree":
                text = font.render("T", True, (0, 200, 0))
            elif obstacle.get("type") == "rock":
                text = font.render("R", True, (200, 200, 200))
            else:
                text = font.render("X", True, (200, 200, 200))
                
            self.screen.blit(text, (x * GRID_SIZE + GRID_SIZE // 2 - 5, y * GRID_SIZE + GRID_SIZE // 2 - 5))
    
    def draw_move_range(self):
        if self.selected_unit and not self.selected_unit.moved:
            unit = self.selected_unit
            for x in range(max(0, unit.x - unit.move_range), min(GRID_WIDTH, unit.x + unit.move_range + 1)):
                for y in range(max(0, unit.y - unit.move_range), min(GRID_HEIGHT, unit.y + unit.move_range + 1)):
                    if unit.can_move_to(x, y, self.units, self.obstacles):
                        distance = abs(unit.x - x) + abs(unit.y - y)
                        if distance <= unit.get_stat_with_effects("move_range"):
                            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                            # Use green for movement range
                            pygame.draw.rect(self.screen, (0, 200, 0, 128), rect, 2)
    
    def draw_attack_range(self):
        if self.selected_unit and not self.selected_unit.attacked:
            unit = self.selected_unit
            for target in self.units:
                if unit.can_attack(target):
                    rect = pygame.Rect(target.x * GRID_SIZE, target.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    # Use red for attack range
                    pygame.draw.rect(self.screen, (255, 0, 0, 128), rect, 3)
    
    def draw_ability_range(self):
        if self.ability_target_mode and self.selected_unit:
            unit = self.selected_unit
            ability_data = Ability.get_ability_data(unit.ability)
            
            if unit.ability == AbilityType.TELEPORT:
                # Show all valid teleport locations
                for x in range(max(0, unit.x - ability_data["range"]), min(GRID_WIDTH, unit.x + ability_data["range"] + 1)):
                    for y in range(max(0, unit.y - ability_data["range"]), min(GRID_HEIGHT, unit.y + ability_data["range"] + 1)):
                        # Check if position is valid (empty)
                        valid = True
                        for other_unit in self.units:
                            if other_unit.x == x and other_unit.y == y:
                                valid = False
                                break
                                
                        for obstacle in self.obstacles:
                            if obstacle["x"] == x and obstacle["y"] == y:
                                valid = False
                                break
                        
                        if valid:
                            distance = abs(unit.x - x) + abs(unit.y - y)
                            if distance <= ability_data["range"]:
                                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                                pygame.draw.rect(self.screen, (128, 0, 128, 128), rect, 2)  # Purple for teleport
            
            elif unit.ability == AbilityType.HEAL:
                # Show valid heal targets (self and adjacent allies)
                for target in self.units:
                    if target.player == unit.player:  # Only allies
                        distance = abs(unit.x - target.x) + abs(unit.y - target.y)
                        if distance <= ability_data["range"]:
                            rect = pygame.Rect(target.x * GRID_SIZE, target.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                            pygame.draw.rect(self.screen, (0, 255, 0, 128), rect, 2)  # Green for heal
            
            elif unit.ability == AbilityType.AREA_ATTACK:
                # Show area attack range
                for target in self.units:
                    if target.player != unit.player:  # Only enemies
                        distance = abs(unit.x - target.x) + abs(unit.y - target.y)
                        if distance <= ability_data["range"]:
                            rect = pygame.Rect(target.x * GRID_SIZE, target.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                            pygame.draw.rect(self.screen, (255, 165, 0, 128), rect, 2)  # Orange for area attack
    def draw_ui(self):
        # Draw turn indicator with background
        turn_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 40)
        pygame.draw.rect(self.screen, (40, 40, 40), turn_bg)
        
        # Draw turn indicator text with player color
        turn_color = RED if self.current_player == 0 else BLUE
        turn_text = self.font.render(f"{'Player' if self.current_player == 0 else 'AI'}'s Turn ({self.turn_count})", True, turn_color)
        self.screen.blit(turn_text, (10, 10))
        
        # Draw level indicator
        level_text = self.small_font.render(f"Level: {self.current_level}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 100, 10))
        
        # Draw selected unit info
        if self.selected_unit:
            unit = self.selected_unit
            unit_info = self.small_font.render(
                f"Type: {unit.unit_type.name} | HP: {unit.hp}/{unit.max_hp} | ATK: {unit.attack} | DEF: {unit.defense}",
                True, WHITE
            )
            self.screen.blit(unit_info, (200, 10))
            
            status = []
            if unit.moved:
                status.append("Moved")
            if unit.attacked:
                status.append("Attacked")
            if unit.ability_used:
                status.append("Ability Used")
            
            if status:
                status_text = self.small_font.render(f"Status: {', '.join(status)}", True, WHITE)
                self.screen.blit(status_text, (200, 30))
        
        # Draw end turn button
        end_turn_rect = pygame.Rect(SCREEN_WIDTH - 120, 10, 110, 30)
        pygame.draw.rect(self.screen, (100, 100, 100), end_turn_rect)
        end_turn_text = self.small_font.render("End Turn", True, WHITE)
        self.screen.blit(end_turn_text, (SCREEN_WIDTH - 110, 15))
        
        # Draw save game button
        save_game_rect = pygame.Rect(SCREEN_WIDTH - 240, 10, 110, 30)
        pygame.draw.rect(self.screen, (100, 100, 100), save_game_rect)
        save_game_text = self.small_font.render("Save Game", True, WHITE)
        self.screen.blit(save_game_text, (SCREEN_WIDTH - 230, 15))
        
        # Draw ability button if unit is selected
        if self.selected_unit and not self.selected_unit.ability_used and self.selected_unit.ability_cooldown == 0:
            ability_rect = pygame.Rect(10, SCREEN_HEIGHT - 40, 110, 30)
            pygame.draw.rect(self.screen, (100, 100, 100), ability_rect)
            ability_text = self.small_font.render("Use Ability (A)", True, WHITE)
            self.screen.blit(ability_text, (15, SCREEN_HEIGHT - 35))
        
        # Draw inventory button if unit is selected
        if self.selected_unit:
            inventory_rect = pygame.Rect(130, SCREEN_HEIGHT - 40, 110, 30)
            pygame.draw.rect(self.screen, (100, 100, 100), inventory_rect)
            inventory_text = self.small_font.render("Inventory (I)", True, WHITE)
            self.screen.blit(inventory_text, (135, SCREEN_HEIGHT - 35))
        
        # Draw game over message if applicable
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("Game Over", True, WHITE)
            winner_text = self.font.render(f"{'Player' if self.winner == 0 else 'AI'} Wins!", True, WHITE)
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 50))
    
    def handle_click(self, pos):
        if self.game_over:
            return
        
        if self.current_player != 0:  # Only handle clicks during player's turn
            return
        
        x, y = pos[0] // GRID_SIZE, pos[1] // GRID_SIZE
        
        # Check if end turn button was clicked
        end_turn_rect = pygame.Rect(SCREEN_WIDTH - 120, 10, 110, 30)
        if end_turn_rect.collidepoint(pos):
            self.sound_manager.play('turn')
            self.end_turn()
            return
            
        # Check if save game button was clicked
        save_game_rect = pygame.Rect(SCREEN_WIDTH - 240, 10, 110, 30)
        if save_game_rect.collidepoint(pos):
            self.save_game_state()
            return
        
        # Check if ability button was clicked
        if self.selected_unit and not self.selected_unit.ability_used and self.selected_unit.ability_cooldown == 0:
            ability_rect = pygame.Rect(10, SCREEN_HEIGHT - 40, 110, 30)
            if ability_rect.collidepoint(pos):
                self.toggle_ability_mode()
                return
        
        # Check if inventory button was clicked
        if self.selected_unit:
            inventory_rect = pygame.Rect(130, SCREEN_HEIGHT - 40, 110, 30)
            if inventory_rect.collidepoint(pos):
                self.open_inventory()
                return
        
        # Handle ability target selection
        if self.ability_target_mode and self.selected_unit:
            ability_data = Ability.get_ability_data(self.selected_unit.ability)
            
            if self.selected_unit.ability == AbilityType.TELEPORT:
                # Check if clicked position is valid for teleport
                valid = True
                for unit in self.units:
                    if unit.x == x and unit.y == y:
                        valid = False
                        break
                
                for obstacle in self.obstacles:
                    if obstacle["x"] == x and obstacle["y"] == y:
                        valid = False
                        break
                
                distance = abs(self.selected_unit.x - x) + abs(self.selected_unit.y - y)
                if valid and distance <= ability_data["range"]:
                    # Teleport to the selected position
                    self.selected_unit.x = x
                    self.selected_unit.y = y
                    self.selected_unit.ability_used = True
                    self.selected_unit.ability_cooldown = ability_data["cooldown"]
                    self.sound_manager.play('ability')
                    self.ability_target_mode = False
                    return
            
            elif self.selected_unit.ability == AbilityType.HEAL:
                # Check if clicked on valid heal target
                for unit in self.units:
                    if unit.x == x and unit.y == y and unit.player == self.selected_unit.player:
                        distance = abs(self.selected_unit.x - unit.x) + abs(self.selected_unit.y - unit.y)
                        if distance <= ability_data["range"]:
                            # Heal the target
                            unit.hp = min(unit.max_hp, unit.hp + 30)
                            self.selected_unit.ability_used = True
                            self.selected_unit.ability_cooldown = ability_data["cooldown"]
                            self.sound_manager.play('ability')
                            self.ability_target_mode = False
                            return
            
            elif self.selected_unit.ability == AbilityType.AREA_ATTACK:
                # Check if clicked in range for area attack
                for unit in self.units:
                    if unit.x == x and unit.y == y and unit.player != self.selected_unit.player:
                        distance = abs(self.selected_unit.x - unit.x) + abs(self.selected_unit.y - unit.y)
                        if distance <= ability_data["range"]:
                            # Perform area attack
                            for target in self.units:
                                if target.player != self.selected_unit.player:
                                    target_distance = abs(unit.x - target.x) + abs(unit.y - target.y)
                                    if target_distance <= 1:  # 1-tile radius
                                        damage = max(1, self.selected_unit.attack // 2)
                                        target.hp -= damage
                            
                            self.selected_unit.ability_used = True
                            self.selected_unit.ability_cooldown = ability_data["cooldown"]
                            self.sound_manager.play('ability')
                            self.ability_target_mode = False
                            
                            # Remove dead units
                            self.remove_dead_units()
                            return
            
            # If we get here, cancel ability mode on invalid click
            self.ability_target_mode = False
            return
        # Check if a unit was clicked
        clicked_unit = None
        for unit in self.units:
            if unit.x == x and unit.y == y:
                clicked_unit = unit
                break
        
        # If a unit is already selected
        if self.selected_unit:
            # If clicked on own unit, select it
            if clicked_unit and clicked_unit.player == 0:
                for unit in self.units:
                    unit.selected = False
                clicked_unit.selected = True
                self.selected_unit = clicked_unit
                self.sound_manager.play('select')
                
                # Trigger tutorial if needed
                if self.show_tutorial:
                    self.current_tutorial = self.tutorial.trigger_event("select_unit")
                    if self.current_tutorial:
                        self.show_tutorial_popup()
            
            # If clicked on enemy unit, try to attack
            elif clicked_unit and clicked_unit.player == 1:
                if self.selected_unit.can_attack(clicked_unit):
                    damage = self.selected_unit.attack_unit(clicked_unit)
                    self.sound_manager.play('attack')
                    print(f"Attacked for {damage} damage!")
                    
                    # Remove dead units
                    if clicked_unit.hp <= 0:
                        self.sound_manager.play('defeat')
                        self.units.remove(clicked_unit)
                        self.check_game_over()
                    
                    # Trigger tutorial if needed
                    if self.show_tutorial:
                        self.current_tutorial = self.tutorial.trigger_event("show_attack")
                        if self.current_tutorial:
                            self.show_tutorial_popup()
            
            # If clicked on empty cell, try to move
            elif self.selected_unit.can_move_to(x, y, self.units, self.obstacles):
                self.selected_unit.x = x
                self.selected_unit.y = y
                self.selected_unit.moved = True
                self.sound_manager.play('move')
                
                # Trigger tutorial if needed
                if self.show_tutorial:
                    self.current_tutorial = self.tutorial.trigger_event("show_movement")
                    if self.current_tutorial:
                        self.show_tutorial_popup()
        
        # If no unit is selected, try to select one
        elif clicked_unit and clicked_unit.player == 0:
            clicked_unit.selected = True
            self.selected_unit = clicked_unit
            self.sound_manager.play('select')
            
            # Trigger tutorial if needed
            if self.show_tutorial:
                self.current_tutorial = self.tutorial.trigger_event("select_unit")
                if self.current_tutorial:
                    self.show_tutorial_popup()
    
    def toggle_ability_mode(self):
        """Toggle ability targeting mode"""
        if not self.selected_unit or self.selected_unit.ability_used or self.selected_unit.ability_cooldown > 0:
            return
        
        self.ability_target_mode = not self.ability_target_mode
        
        # Handle abilities that don't need targeting
        if self.ability_target_mode:
            if self.selected_unit.ability == AbilityType.SHIELD:
                # Apply shield effect immediately
                self.selected_unit.active_effects.append({
                    "type": "shield",
                    "duration": 1,
                    "icon": "S",
                    "color": BLUE
                })
                self.selected_unit.ability_used = True
                ability_data = Ability.get_ability_data(self.selected_unit.ability)
                self.selected_unit.ability_cooldown = ability_data["cooldown"]
                self.sound_manager.play('ability')
                self.ability_target_mode = False
                
                # Trigger tutorial if needed
                if self.show_tutorial:
                    self.current_tutorial = self.tutorial.trigger_event("show_abilities")
                    if self.current_tutorial:
                        self.show_tutorial_popup()
            
            elif self.selected_unit.ability == AbilityType.DOUBLE_ATTACK:
                # Apply double attack effect immediately
                self.selected_unit.active_effects.append({
                    "type": "double_attack",
                    "duration": 1,
                    "uses": 1,
                    "icon": "D",
                    "color": RED
                })
                self.selected_unit.ability_used = True
                ability_data = Ability.get_ability_data(self.selected_unit.ability)
                self.selected_unit.ability_cooldown = ability_data["cooldown"]
                self.sound_manager.play('ability')
                self.ability_target_mode = False
                
                # Trigger tutorial if needed
                if self.show_tutorial:
                    self.current_tutorial = self.tutorial.trigger_event("show_abilities")
                    if self.current_tutorial:
                        self.show_tutorial_popup()
    
    def open_inventory(self):
        """Open the inventory menu for the selected unit"""
        if not self.selected_unit:
            return
        
        inventory_menu = InventoryMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.selected_unit)
        result = inventory_menu.run()
        
        if result.startswith("Use:"):
            item_index = int(result.split(":")[1])
            success, message = self.selected_unit.use_item(item_index)
            if success:
                self.sound_manager.play('item')
                print(message)
                
                # Trigger tutorial if needed
                if self.show_tutorial:
                    self.current_tutorial = self.tutorial.trigger_event("show_inventory")
                    if self.current_tutorial:
                        self.show_tutorial_popup()
    
    def show_tutorial_popup(self):
        """Show a tutorial popup"""
        if self.current_tutorial:
            popup = TutorialPopup(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.current_tutorial)
            if popup.run():
                self.current_tutorial = self.tutorial.advance()
    
    def end_turn(self):
        """End the current player's turn"""
        # Reset unit states for the next player
        for unit in self.units:
            if unit.player == self.current_player:
                unit.reset_turn()
                unit.selected = False
        
        self.selected_unit = None
        self.ability_target_mode = False
        self.current_player = 1 - self.current_player  # Switch player
        
        # Increment turn count when player's turn starts
        if self.current_player == 0:
            self.turn_count += 1
            
            # Check for enemy spawning
            level_data = self.level_manager.get_level_data(self.current_level)
            if self.turn_count % level_data["spawn_interval"] == 0:
                self.spawn_enemy(level_data["spawn_points"])
        
        # Trigger tutorial if needed
        if self.show_tutorial and self.current_player == 0:
            self.current_tutorial = self.tutorial.trigger_event("end_turn")
            if self.current_tutorial:
                self.show_tutorial_popup()
        
        # If it's AI's turn, let AI play
        if self.current_player == 1:
            self.ai_turn()
    
    def spawn_enemy(self, spawn_points):
        """Spawn a new enemy unit at one of the spawn points"""
        if not spawn_points:
            return
            
        # Choose a random spawn point
        spawn_point = random.choice(spawn_points)
        x, y = spawn_point["x"], spawn_point["y"]
        
        # Check if spawn point is occupied
        for unit in self.units:
            if unit.x == x and unit.y == y:
                return  # Spawn point is occupied
        
        # Choose a random unit type with weighted probabilities
        unit_types = [UnitType.INFANTRY, UnitType.ARCHER, UnitType.CAVALRY, UnitType.MAGE]
        weights = [0.4, 0.3, 0.2, 0.1]  # Infantry most common, mage least common
        unit_type = random.choices(unit_types, weights=weights, k=1)[0]
        
        # Create and add the new unit
        new_unit = Unit(unit_type, x, y, 1)  # player=1 for AI
        self.units.append(new_unit)
        print(f"Enemy {unit_type.name} spawned at ({x}, {y})")
    
    def remove_dead_units(self):
        """Remove units with HP <= 0"""
        self.units = [unit for unit in self.units if unit.hp > 0]
        self.check_game_over()
    
    def ai_turn(self):
        """Handle AI turn logic with optimized AI controller"""
        print("AI's turn")
        
        # Import the AI controller if not already imported
        from ai_controller import AIController
        
        # Create AI controller with difficulty based on current level
        ai_difficulty = min(3, self.current_level)  # Cap difficulty at 3
        ai = AIController(difficulty=ai_difficulty)
        
        # Get player and AI units
        ai_units = [unit for unit in self.units if unit.player == 1]
        player_units = [unit for unit in self.units if unit.player == 0]
        
        # Get AI's planned actions for all units
        actions = ai.process_turn(ai_units, player_units, self.units, self.obstacles, GRID_WIDTH, GRID_HEIGHT)
        
        # Execute the actions for each unit
        for action_data in actions:
            unit = action_data["unit"]
            unit_actions = action_data["actions"]
            
            # Process ability actions first
            if "ability" in unit_actions and not unit.ability_used and unit.ability_cooldown == 0:
                ability_action = unit_actions["ability"]
                
                if unit.ability == AbilityType.SHIELD:
                    # Apply shield effect
                    unit.active_effects.append({
                        "type": "shield",
                        "duration": 1,
                        "icon": "S",
                        "color": BLUE
                    })
                    unit.ability_used = True
                    ability_data = Ability.get_ability_data(unit.ability)
                    unit.ability_cooldown = ability_data["cooldown"]
                    self.sound_manager.play('ability')
                
                elif unit.ability == AbilityType.DOUBLE_ATTACK:
                    # Apply double attack effect
                    unit.active_effects.append({
                        "type": "double_attack",
                        "duration": 1,
                        "uses": 1,
                        "icon": "D",
                        "color": RED
                    })
                    unit.ability_used = True
                    ability_data = Ability.get_ability_data(unit.ability)
                    unit.ability_cooldown = ability_data["cooldown"]
                    self.sound_manager.play('ability')
                
                elif unit.ability == AbilityType.AREA_ATTACK and ability_action["type"] == "target":
                    target_x, target_y = ability_action["x"], ability_action["y"]
                    
                    # Perform area attack
                    for target in player_units:
                        distance = abs(target_x - target.x) + abs(target_y - target.y)
                        if distance <= 1:  # 1-tile radius
                            damage = max(1, unit.attack // 2)
                            target.hp -= damage
                    
                    unit.ability_used = True
                    ability_data = Ability.get_ability_data(unit.ability)
                    unit.ability_cooldown = ability_data["cooldown"]
                    self.sound_manager.play('ability')
                    
                    # Remove dead units
                    self.remove_dead_units()
                    if self.game_over:
                        return
                        
                elif unit.ability == AbilityType.TELEPORT and ability_action["type"] == "position":
                    # Teleport to target position
                    unit.x, unit.y = ability_action["x"], ability_action["y"]
                    unit.ability_used = True
                    ability_data = Ability.get_ability_data(unit.ability)
                    unit.ability_cooldown = ability_data["cooldown"]
                    self.sound_manager.play('ability')
            
            # Process attack actions
            if "attack" in unit_actions and not unit.attacked:
                target = unit_actions["attack"]["target"]
                if unit.can_attack(target):
                    damage = unit.attack_unit(target)
                    self.sound_manager.play('attack')
                    print(f"AI attacked for {damage} damage!")
                    
                    # Remove dead units
                    if target.hp <= 0:
                        self.sound_manager.play('defeat')
                        self.units.remove(target)
                        player_units.remove(target)
                        self.check_game_over()
                        if self.game_over:
                            return
            
            # Process movement actions
            if "move" in unit_actions and not unit.moved:
                move_x, move_y = unit_actions["move"]["x"], unit_actions["move"]["y"]
                if unit.can_move_to(move_x, move_y, self.units, self.obstacles):
                    unit.x, unit.y = move_x, move_y
                    unit.moved = True
                    self.sound_manager.play('move')
        
        # End AI turn
        self.sound_manager.play('turn')
        self.end_turn()
    
    def check_game_over(self):
        """Check if the game is over"""
        player_units = any(unit.player == 0 for unit in self.units)
        ai_units = any(unit.player == 1 for unit in self.units)
        
        if not player_units:
            self.game_over = True
            self.winner = 1  # AI wins
            self.sound_manager.play('defeat')
        elif not ai_units:
            self.game_over = True
            self.winner = 0  # Player wins
            self.sound_manager.play('victory')
            
            # Check if there's a next level
            if self.level_manager.next_level():
                # Show level transition
                transition = LevelTransition(
                    self.screen, 
                    SCREEN_WIDTH, 
                    SCREEN_HEIGHT, 
                    self.current_level, 
                    self.level_manager.current_level
                )
                result = transition.run()
                
                if isinstance(result, int):
                    # Start next level
                    self.initialize_level(result)
                    self.game_over = False
                    self.winner = None
    
    def run(self):
        """Main game loop"""
        running = True
        
        # Show initial tutorial if needed
        if self.show_tutorial and self.current_tutorial:
            self.show_tutorial_popup()
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        # Restart game
                        self.__init__(self.screen, self.sound_manager, self.current_level)
                    elif event.key == pygame.K_s:
                        # Save game with S key
                        self.save_game_state()
                    elif event.key == pygame.K_a and self.selected_unit and not self.ability_target_mode:
                        # Use ability with A key
                        self.toggle_ability_mode()
                    elif event.key == pygame.K_i and self.selected_unit:
                        # Open inventory with I key
                        self.open_inventory()
            
            # Draw everything
            self.screen.fill(BG_COLOR)
            self.draw_grid()
            self.draw_obstacles()
            
            if self.ability_target_mode:
                self.draw_ability_range()
            else:
                self.draw_move_range()
                self.draw_attack_range()
            
            for unit in self.units:
                unit.draw(self.screen)
            
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        return False  # Game ended

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Turn-Based Strategy Game")
    sound_manager = SoundManager()
    
    # Show main menu
    menu = MainMenu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    choice = menu.run()
    
    if choice == "Start Game":
        game = Game(screen, sound_manager)
        game.run()
    elif choice == "Level Select":
        level_menu = LevelSelectMenu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        level = level_menu.run()
        if isinstance(level, int):
            game = Game(screen, sound_manager, level)
            game.run()
    elif choice == "Load Game":
        game = Game(screen, sound_manager, load_saved_game=True)
        game.run()
    elif choice == "Quit":
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    main()
