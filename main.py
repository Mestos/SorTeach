import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

Branco = (255, 255, 255)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
pygame.display.set_caption("SorTeach.exe")


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):

        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player:
    def __init__(self, score=0, lives=3, current_level=0):
        self.score = score
        self.lives = lives
        self.current_level = current_level


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = study_mode(screen)

        if game_state == GameState.MODE:
            player.current_level = 0
            game_state = study_mode(screen)

        if game_state == GameState.NEXT_LEVELH:
            if player.current_level < 10:
                player.current_level += 1
            else:
                player.current_level = player.current_level - 9
            game_state = play_levelh(screen, player)

        if game_state == GameState.NEXT_LEVELT:
            if player.current_level < 10:
                player.current_level += 1
            else:
                player.current_level = player.current_level - 9
            game_state = play_levelt(screen, player)

        if game_state == GameState.NEXT_LEVELQ:
            if player.current_level < 10:
                player.current_level += 1
            else:
                player.current_level = player.current_level - 9
            game_state = play_levelq(screen, player)

        if game_state == GameState.PLAYT:
            game_state = level_type(screen, player)

        if game_state == GameState.PLAYH:
            game_state = level_type(screen, player)

        if game_state == GameState.PLAYQ:
            game_state = level_type(screen, player)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    name_btn = UIElement(
        center_position=(400, 150),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=AMARELO,
        text="SorTeach",
    )
    start_btn = UIElement(
        center_position=(400, 300),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Iniciar",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 350),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Sair",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(name_btn,start_btn, quit_btn)
    return game_loop(screen, buttons)


def play_levelt(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Modo de ensino",
        action=GameState.MODE,
    )
    playlevelt_btn = UIElement(
        center_position=(400, 200),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Iniciar Nivel",
        action=GameState.PLAYT,
    )
    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Proximo Nivel ({player.current_level})",
        action=GameState.NEXT_LEVELT,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn, playlevelt_btn)
    return game_loop(screen, buttons)


def play_levelh(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Modo de ensino",
        action=GameState.MODE,
    )
    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Proximo Nivel ({player.current_level})",
        action=GameState.NEXT_LEVELH,
    )
    playlevel_btn = UIElement(
        center_position=(400, 200),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Iniciar Nivel",
        action=GameState.PLAYH,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn, playlevel_btn)
    return game_loop(screen, buttons)


def play_levelq(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Modo de ensino",
        action=GameState.MODE,
    )
    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Proximo Nivel ({player.current_level})",
        action=GameState.NEXT_LEVELQ,
    )
    playlevel_btn = UIElement(
        center_position=(400, 200),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Iniciar Nivel",
        action=GameState.PLAYQ,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn, playlevel_btn)
    return game_loop(screen, buttons)


def study_mode(screen):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Voltar para o menu",
        action=GameState.TITLE,
    )
    heapsort_btn = UIElement(
        center_position=(400, 350),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Heapsort",
        action=GameState.NEXT_LEVELH,
    )
    quicksort_btn = UIElement(
        center_position=(400, 250),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Quicksort",
        action=GameState.NEXT_LEVELQ,
    )

    tutorial_btn = UIElement(
        center_position=(400, 150),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Tutorial",
        action=GameState.NEXT_LEVELT,
    )

    buttons = RenderUpdates(return_btn, heapsort_btn, quicksort_btn, tutorial_btn)
    return game_loop(screen, buttons)


def level_type(screen, player):
    if player.current_level <= 5:
        name_btn = UIElement(
            center_position=(400, 50),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERDE,
            text="Facil",
        )
    elif player.current_level <= 8:
        name_btn = UIElement(
            center_position=(400, 50),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=AMARELO,
            text="Medio",
        )
    else:
        name_btn = UIElement(
            center_position=(400, 50),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Dificil",
        )
    buttons = RenderUpdates(name_btn)
    return game_loop(screen, buttons)



def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.QUIT:
                exit()
        screen.fill(PRETO)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    MODE = 2
    PLAYT = 3
    PLAYH = 4
    PLAYQ = 5
    NEXT_LEVELT = 6
    NEXT_LEVELH = 7
    NEXT_LEVELQ = 8


if __name__ == "__main__":
    main()
