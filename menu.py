import pygame
from settings import *

class SlidePanel:
    def __init__(self):
        self.font_large = pygame.font.SysFont("Courier New", 36, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 28)
        self.pause_btn = pygame.Rect(GAME_WIDTH + 40, 100, 120, 40)

    def draw(self, surface, paused, player_tank):
        pygame.draw.rect(surface, (30, 30, 30), (GAME_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(surface, WHITE_COLOR, (GAME_WIDTH, 0), (GAME_WIDTH, SCREEN_HEIGHT), 2)

        pygame.draw.rect(surface, GRAY, self.pause_btn)
        pygame.draw.rect(surface, WHITE_COLOR, self.pause_btn, 2)
        label = "RESUME" if paused else "PAUSE"
        pause_txt = self.font_small.render(label, True, WHITE_COLOR)
        surface.blit(pause_txt, pause_txt.get_rect(center=self.pause_btn.center))

        lives_txt = self.font_small.render(f"Lives: {player_tank.lives}", True, WHITE_COLOR)

        surface.blit(lives_txt, (GAME_WIDTH + 30, 190))

    def handle_event(self, event, paused):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_btn.collidepoint(event.pos):
                paused = not paused
        return paused

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

class EndGameScreen:
    def __init__(self, window, result_text, score):
        self.window = window
        self.result_text = result_text
        self.score = score
        self.font = pygame.font.SysFont("Courier New", 50, bold=True)
        self.button_font = pygame.font.SysFont("Courier New", 36)
        self.buttons = {
            "retry": pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50, 100, 50),
            "exit": pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 50, 100, 50)
        }

    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((30, 30, 30))
        self.window.blit(overlay, (0, 0))

        result_surf = self.font.render(self.result_text, True, WHITE_COLOR)
        score_surf = self.button_font.render(f"Score: {self.score}", True, WHITE_COLOR)

        self.window.blit(result_surf, result_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
        self.window.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))

        for name, rect in self.buttons.items():
            pygame.draw.rect(self.window, (100, 100, 100), rect)
            pygame.draw.rect(self.window, WHITE_COLOR, rect, 3)
            text = self.button_font.render("Retry" if name == "retry" else "Exit", True, WHITE_COLOR)
            self.window.blit(text, text.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.buttons["retry"].collidepoint(pos):
                return "retry"
            elif self.buttons["exit"].collidepoint(pos):
                return "exit"
        return None