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
    def __init__(self, current_level=0):
        self.current_level = current_level


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = GameState.NEXT_LEVEL

        if game_state == GameState.NEXT_LEVEL:
            if player.current_level < 6:
                player.current_level += 1

            else:
                player.current_level = player.current_level - 5
            game_state = play_level(screen, player)

        if game_state == GameState.PLAY:
            game_state = level_type(screen, player)

        if game_state == GameState.COMPLETE:
            game_state = complete(screen)

        if game_state == GameState.FAILED:
            game_state = fail(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen):
    name_btn = UIElement(
        center_position=(590, 150),
        font_size=50,
        bg_rgb=PRETO,
        text_rgb=AMARELO,
        text="SorTeach",
    )
    start_btn = UIElement(
        center_position=(590, 300),
        font_size=40,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Iniciar",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(590, 400),
        font_size=40,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Sair",
        action=GameState.QUIT,
    )
    buttons = RenderUpdates(name_btn, start_btn, quit_btn)
    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(100, 550),
        font_size=40,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Menu",
        action=GameState.TITLE,
    )
    playlevelt_btn = UIElement(
        center_position=(600, 200),
        font_size=50,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Iniciar Nivel",
        action=GameState.PLAY,
    )
    nextlevel_btn = UIElement(
        center_position=(600, 450),
        font_size=30,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text=f"Proximo Nivel ({player.current_level})",
        action=GameState.NEXT_LEVEL,
    )
    buttons = RenderUpdates(return_btn, nextlevel_btn, playlevelt_btn)
    return game_loop(screen, buttons)


def level_type(screen, player):
    if player.current_level <= 3:
        name_btn = UIElement(
            center_position=(600, 50),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERDE,
            text="Facil",
        )
    elif player.current_level <= 5:
        name_btn = UIElement(
            center_position=(600, 50),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=AMARELO,
            text="Medio",
        )
    else:
        name_btn = UIElement(
            center_position=(600, 50),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Dificil",
        )
    if player.current_level == 1:
        yes_btn = UIElement(
            center_position=(200, 410),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERDE,
            text="Sim",
            action=GameState.COMPLETE
        )
        question_btn = UIElement(
            center_position=(600, 300),
            font_size=27,
            bg_rgb=PRETO,
            text_rgb=Branco,
            text="Uma árvore binária possui no máximo 2 nós filhos de outro nó?",
        )
        no_btn = UIElement(
            center_position=(800, 400),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Nao",
            action=GameState.FAILED
        )
    if player.current_level == 3:
        no_btn = UIElement(
            center_position=(820, 450),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Nao",
            action=GameState.COMPLETE
        )
        yes_btn = UIElement(
            center_position=(400, 450),
            font_size=50,
            bg_rgb=PRETO,
            text_rgb=VERDE,
            text="Sim",
            action=GameState.FAILED
        )
        question_btn = UIElement(
            center_position=(600, 200),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=Branco,
            text="Este vetor representa uma Heap?",
        )
        heap_btn = UIElement(
            center_position=(600, 300),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=Branco,
            text="[20 35 18 64 7 12 43 25 50]",
        )
    if player.current_level == 4:
        question_btn = UIElement(
            center_position=(600, 200),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=Branco,
            text="Qual dos vetores abaixo representa uma Heap?",
        )
        op1_btn = UIElement(
            center_position=(220, 250),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 1: [1 0 3 4 9 6]",
            action=GameState.FAILED
        )
        op2_btn = UIElement(
            center_position=(290, 300),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 2: [30 7 18 4 64 9 3 24]",
            action=GameState.FAILED
        )
        op3_btn = UIElement(
            center_position=(340, 350),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 3: [64 50 43 35 7 12 18 25 20]",
            action=GameState.COMPLETE
        )
        op4_btn = UIElement(
            center_position=(195, 400),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 4: [20 2 30 4]",
            action=GameState.FAILED
        )
    if player.current_level == 6:
        question_btn = UIElement(
            center_position=(600, 200),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=Branco,
            text="Qual a complexidade de construção de uma Heap?",
        )
        op1_btn = UIElement(
            center_position=(300, 250),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 1: O(n)",
            action=GameState.COMPLETE
        )
        op2_btn = UIElement(
            center_position=(335, 300),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 2: O(log n)",
            action=GameState.FAILED
        )
        op3_btn = UIElement(
            center_position=(350, 350),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 3: O(n*log n)",
            action=GameState.FAILED
        )
    if player.current_level == 2:
        question_btn = UIElement(
            center_position=(600, 200),
            font_size=23,
            bg_rgb=PRETO,
            text_rgb=Branco,
            text="Seja V[i] um elemento na posição i. Em uma Heap, V[i] > V[2i] e V[i] > V[2i + 1]",
        )
        t_btn = UIElement(
            center_position=(820, 450),
            font_size=40,
            bg_rgb=PRETO,
            text_rgb=VERDE,
            text="Verdadeiro",
            action=GameState.COMPLETE
        )
        fake_btn = UIElement(
            center_position=(350, 450),
            font_size=40,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Falso",
            action=GameState.FAILED
        )
    if player.current_level == 5:
        question_btn = UIElement(
            center_position=(600, 200),
            font_size=23,
            bg_rgb=PRETO,
            text_rgb=Branco,
            text="Dada a Heap H: [95 60 78 39 28 66 70]. Mudando a prioridade de 66 para 98, H fica:",
        )
        op3_btn = UIElement(
            center_position=(340, 350),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 3: [95 60 78 98 39 28 70]",
            action=GameState.FAILED
        )
        op2_btn = UIElement(
            center_position=(340, 300),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 2: [98 60 95 39 28 78 70]",
            action=GameState.COMPLETE
        )
        op1_btn = UIElement(
            center_position=(340, 250),
            font_size=30,
            bg_rgb=PRETO,
            text_rgb=VERMELHO,
            text="Opçao 1: [98 95 60 39 28 78 70]",
            action=GameState.FAILED
        )

    if player.current_level == 3:
        buttons = RenderUpdates(name_btn, yes_btn, question_btn, no_btn, heap_btn)
    elif player.current_level == 1:
        buttons = RenderUpdates(name_btn, yes_btn, question_btn, no_btn)
    elif player.current_level == 4:
        buttons = RenderUpdates(name_btn, question_btn, op1_btn, op2_btn, op3_btn, op4_btn)
    elif player.current_level == 6:
        buttons = RenderUpdates(name_btn, question_btn, op1_btn, op2_btn, op3_btn)
    elif player.current_level == 2:
        buttons = RenderUpdates(name_btn, question_btn, t_btn, fake_btn)
    elif player.current_level == 5:
        buttons = RenderUpdates(name_btn, question_btn, op1_btn, op2_btn, op3_btn)
    return game_loop(screen, buttons)


def complete(screen):
    name_btn = UIElement(
        center_position=(600, 200),
        font_size=100,
        bg_rgb=PRETO,
        text_rgb=AMARELO,
        text="Parabens",
    )
    back_btn = UIElement(
        center_position=(100, 550),
        font_size=40,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Voltar",
        action=GameState.NEWGAME
    )
    buttons = RenderUpdates(name_btn, back_btn)
    return game_loop(screen, buttons)


def fail(screen):
    name_btn = UIElement(
        center_position=(600, 200),
        font_size=100,
        bg_rgb=PRETO,
        text_rgb=AMARELO,
        text="Errou",
    )
    back_btn = UIElement(
        center_position=(100, 550),
        font_size=40,
        bg_rgb=PRETO,
        text_rgb=Branco,
        text="Voltar",
        action=GameState.NEWGAME
    )
    buttons = RenderUpdates(name_btn, back_btn)
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
    PLAY = 2
    NEXT_LEVEL = 3
    COMPLETE = 4
    FAILED = 5


if __name__ == "__main__":
    main()