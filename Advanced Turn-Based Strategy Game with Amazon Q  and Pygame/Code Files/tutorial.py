import pygame

class Tutorial:
    def __init__(self):
        self.steps = [
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
        self.current_step = 0
    
    def start(self):
        """Start the tutorial from the beginning"""
        self.current_step = 0
        return self.steps[self.current_step]
    
    def advance(self):
        """Advance to the next tutorial step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            return self.steps[self.current_step]
        return None
    
    def trigger_event(self, event_name):
        """Trigger a tutorial step based on an event"""
        for i, step in enumerate(self.steps):
            if step["trigger"] == event_name and i > self.current_step:
                self.current_step = i
                return step
        return None

class TutorialPopup:
    def __init__(self, screen, screen_width, screen_height, tutorial_step):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tutorial_step = tutorial_step
        self.title_font = pygame.font.SysFont(None, 36)
        self.message_font = pygame.font.SysFont(None, 24)
    
    def draw(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw tutorial panel
        panel_rect = pygame.Rect(self.screen_width // 2 - 200, self.screen_height // 2 - 100, 400, 200)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), panel_rect, 2)
        
        # Draw title
        title = self.title_font.render(self.tutorial_step["title"], True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 2 - 80))
        
        # Draw message (word wrap)
        message = self.tutorial_step["message"]
        words = message.split()
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            if self.message_font.size(test_line)[0] < 380:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        
        for i, line in enumerate(lines):
            text = self.message_font.render(line, True, (200, 200, 200))
            self.screen.blit(text, (self.screen_width // 2 - 180, self.screen_height // 2 - 40 + i * 25))
        
        # Draw continue button
        button_rect = pygame.Rect(self.screen_width // 2 - 60, self.screen_height // 2 + 60, 120, 30)
        pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
        
        button_text = self.message_font.render("Continue", True, (255, 255, 255))
        self.screen.blit(button_text, (self.screen_width // 2 - button_text.get_width() // 2, self.screen_height // 2 + 65))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                button_rect = pygame.Rect(self.screen_width // 2 - 60, self.screen_height // 2 + 60, 120, 30)
                if button_rect.collidepoint(event.pos):
                    return True
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return True
        return False
    
    def run(self):
        """Run the tutorial popup and return True when dismissed"""
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
