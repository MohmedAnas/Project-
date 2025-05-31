import pygame
import os
from game_data import load_game

class MainMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (20, 20, 20)
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 36)
        self.selected_option = 0
        self.options = ["Start Game", "Quit"]
        
        # Add "Load Game" option if save exists
        if os.path.exists('savegame.json'):
            self.options.insert(1, "Load Game")
            
        # Add "Level Select" option
        self.options.insert(1, "Level Select")
    
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
        self.levels = [
            {"name": "Level 1: Training Grounds", "difficulty": "Easy"},
            {"name": "Level 2: Forest Ambush", "difficulty": "Medium"},
            {"name": "Level 3: Mountain Pass", "difficulty": "Hard"}
        ]
    
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
        
        return "Quit"

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
                from game_data import Item
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
        
        from game_data import Ability
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

class TutorialPopup:
    def __init__(self, screen, screen_width, screen_height, tutorial_step):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tutorial_step = tutorial_step
        self.title_font = pygame.font.SysFont(None, 36)
        self.text_font = pygame.font.SysFont(None, 24)
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw tutorial panel
        panel_width = 500
        panel_height = 200
        panel_rect = pygame.Rect(
            self.screen_width // 2 - panel_width // 2,
            self.screen_height // 2 - panel_height // 2,
            panel_width,
            panel_height
        )
        pygame.draw.rect(self.screen, (50, 50, 70), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 200), panel_rect, 3)
        
        # Draw title
        title = self.title_font.render(self.tutorial_step["title"], True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 
                                panel_rect.top + 20))
        
        # Draw message (handle multi-line)
        message = self.tutorial_step["message"]
        lines = [message[i:i+60] for i in range(0, len(message), 60)]
        for i, line in enumerate(lines):
            text = self.text_font.render(line, True, (220, 220, 220))
            self.screen.blit(text, (panel_rect.left + 20, panel_rect.top + 70 + i * 25))
        
        # Draw continue instruction
        continue_text = self.text_font.render("Press SPACE to continue", True, (200, 200, 100))
        self.screen.blit(continue_text, (self.screen_width // 2 - continue_text.get_width() // 2, 
                                        panel_rect.bottom - 40))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return True
        return False
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if self.handle_event(event):
                    return True
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return False
