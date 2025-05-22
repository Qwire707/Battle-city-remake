import pygame
import os
pygame.init()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED_COLOR = (255, 0, 0)
BRICK_RED = (178, 34, 34)
WHITE_COLOR = (255, 0, 0)
GRAY = (70, 70, 7)
FPS = 60

PATH = os.path.dirname(__file__) + os.path.sep



####

#class map

#class tank

#class enemy tank

class Level:
    def __init__(self, level_number: int):
        pass

    def load_map(self, level_number: int):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("Courier New", 72, bold=True)
        self.button_font = pygame.font.SysFont("Courier New", 36, bold=True)
        self.button_width = 240
        self.button_height = 60
        self.button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            SCREEN_HEIGHT // 2 - self.button_height // 4,
            self.button_width,
            self.button_height
        )

    def draw_title(self):
        title_text = "BATTLE CITY REMAKE"
        title_surface = self.title_font.render(title_text, True, BRICK_RED)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_surface, title_rect)

    def draw_button(self):
        pygame.draw.rect(self.screen, GRAY, self.button_rect)
        pygame.draw.rect(self.screen, WHITE_COLOR, self.button_rect, 3)

        text_surface = self.button_font.render("PLAY GAME", True, WHITE_COLOR)
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                return "start_game"
        return None


class LevelSelectMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("Courier New", 60, bold=True)
        self.button_font = pygame.font.SysFont("Courier New", 28, bold=True)
        self.level_buttons = []
        self.menu_button = pygame.Rect(20, 20, 120, 50)

        for i in range(3):
            rect = pygame.Rect(150 + i * 200, 250, 150, 150)
            self.level_buttons.append((i + 1, rect))

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("SELECT LEVEL", True, BRICK_RED)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)

        for level_number, rect in self.level_buttons:
            pygame.draw.rect(self.screen, GRAY, rect)
            pygame.draw.rect(self.screen, WHITE_COLOR, rect, 3)
            text_surface = self.button_font.render(f"Level {level_number}", True, WHITE_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, BRICK_RED, self.menu_button)
        pygame.draw.rect(self.screen, WHITE_COLOR, self.menu_button, 3)
        menu_text = self.button_font.render("MENU", True, WHITE_COLOR)
        menu_text_rect = menu_text.get_rect(center=self.menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.collidepoint(event.pos):
                return "back_to_main"

            for level_number, rect in self.level_buttons:
                if rect.collidepoint(event.pos):
                    return f"start_level_{level_number}"
        return None

# Ініціалізація вікна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()


in_main_menu = True
in_level_select_menu = False
current_level = None
menu = MainMenu(screen)
level_select_menu = LevelSelectMenu(screen)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_main_menu:
            result = menu.handle_event(event)
            if result == "start_game":
                in_main_menu = False
                in_level_select_menu = True

        elif in_level_select_menu:
            result = level_select_menu.handle_event(event)
            if result == "back_to_main":
                in_level_select_menu = False
                in_main_menu = True
            elif result and result.startswith("start_level_"):
                level_number = int(result.split("_")[-1])
                current_level = Level(level_number)
                in_level_select_menu = False

    if in_main_menu:
        screen.fill((0, 0, 0))
        menu.draw_title()
        menu.draw_button()
    elif in_level_select_menu:
        level_select_menu.draw()
    else:
        screen.fill((0, 0, 0))
        if current_level:
            current_level.update()
            current_level.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
