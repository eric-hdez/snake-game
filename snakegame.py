from dataclasses import dataclass
from node import Node
from snake import Snake
import random
import pygame
import sys

pygame.init()  # init pygames module

# Game Defines  ------------------------------------------------------------------------------------

@dataclass
class Text:
    FONT = pygame.font.Font(None, 30)
    START_TEXT = "Press 'SPACE' to start"
    SCORE_TEXT = "Length: "
    END_TEXT = "Press 'SPACE' to play again"


@dataclass
class Dimension:
    WIDTH = 840
    HEIGHT = 660


@dataclass
class Color:
    BLACK = (0, 0, 0)
    GREEN = (52, 222, 0)
    RED = (255, 0, 0)
    BLUE = (177, 156, 217)
    WHITE = (246, 246, 246)


@dataclass
class Direction:
    UP = (0, -20)
    DOWN = (0, 20)
    LEFT =  (-20, 0)
    RIGHT = (20, 0)
    NONE =  (0, 0)
    

# Game Functions -----------------------------------------------------------------------------------


# function that initializes the screen of the game
#
def init_screen() -> pygame.display:
    flags = pygame.RESIZABLE | pygame.SCALED
    pygame.display.set_caption("Classic Snake")
    logo = pygame.image.load("images/snake_logo.png")
    pygame.display.set_icon(logo)

    new_screen = pygame.display.set_mode([Dimension.WIDTH, Dimension.HEIGHT], flags)
    new_screen.fill(Color.BLACK)

    return new_screen


# function that loads the sprites and sprite_list of game
#
def load_sprites() -> tuple:
    snake = Snake(Color.GREEN, random.randint(1, 39) * 20, random.randint(1, 29) * 20)
    apple = Node(Color.RED, random.randint(1, 39) * 20, random.randint(1, 29) * 20)

    if apple.x == snake.head.x and apple.y == snake.head.y:
        apple.rect.x = random.randint(1, 39) * 20
        apple.rect.y = random.randint(1, 29) * 20

    new_sprites_list = pygame.sprite.Group()
    new_sprites_list.add(snake.head)
    new_sprites_list.add(apple)

    return snake, apple, new_sprites_list


# function that deploys the borders of the main game
#
def draw_borders(screen: pygame.display) -> None:
    for i in range(20, Dimension.WIDTH, 20):
        pygame.draw.rect(screen, Color.BLACK, [i, 0, 1, Dimension.HEIGHT])
    for i in range(20, Dimension.HEIGHT - 20, 20):
        pygame.draw.rect(screen, Color.BLACK, [0, i, Dimension.WIDTH, 1])

    pygame.draw.rect(screen, Color.WHITE, [0, 0, Dimension.WIDTH, 20])
    pygame.draw.rect(screen, Color.WHITE, [0, Dimension.HEIGHT - 40, Dimension.WIDTH, 40])
    pygame.draw.rect(screen, Color.WHITE, [0, 0, 20, Dimension.HEIGHT])
    pygame.draw.rect(screen, Color.WHITE, [Dimension.WIDTH - 20, 0, 20, Dimension.HEIGHT])



# function that renders text onto the game screen
#
def render_text(text: str, pos: tuple, color: tuple) -> tuple:
    surface = Text.FONT.render(text, True, color)
    rect = surface.get_rect(center=pos)

    return surface, rect


# function that initiates the start sequence of the game screen
#
def start_screen(screen: pygame.display) -> None:
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False

        screen.fill(Color.BLACK)
        draw_borders(screen)
        pygame.draw.rect(screen, Color.WHITE, [420 - 120, 330 - 30, 240, 60], 5)

        score_surface, score_rect = render_text(Text.SCORE_TEXT, (760, 640), Color.BLACK)
        start_surface, start_rect = render_text(Text.START_TEXT, (420, 330), Color.WHITE)

        screen.blit(score_surface, score_rect)
        screen.blit(start_surface, start_rect)
        pygame.display.update()


# function that contains the main logic of the game, returns the final score
#
def run_snake_game(screen: pygame.display) -> int:
    snake, apple, sprites_list = load_sprites()
    direction = Direction.NONE # current direction that the snake is headed in
    running = True  # boolean determines if the game is over or not

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord("a"):
                    if snake.length > 1  and direction == Direction.RIGHT:
                        break
                    direction = Direction.LEFT

                if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    if snake.length > 1  and direction == Direction.LEFT:
                        break
                    direction = Direction.RIGHT

                if event.key == pygame.K_UP or event.key == ord("w"):
                    if snake.length > 1 and direction == Direction.DOWN:
                        break
                    direction = Direction.UP

                if event.key == pygame.K_DOWN or event.key == ord("s"):
                    if snake.length > 1 and direction == Direction.UP:
                        break
                    direction = Direction.DOWN

        # movement of the snake along the grid
        snake.move(direction)

        # handle the snake going out of bounds
        if snake.out_of_bounds((20, 820), (20, 620)):
            running = False

        # handle the collision of the snake head and snake body
        for sprite in sprites_list:
            if sprite in [snake.head, apple]:
                continue
            if snake.head.rect.colliderect(sprite.rect):
                running = False

        # handle the collision of the snake and the apple
        if snake.head.rect.colliderect(apple.rect):
            snake.grow(snake.head.x, snake.head.y)
            for node in snake:
                sprites_list.add(node)

            # get the position that an apple should not spawn in
            apple_bad_position = [[sprite.x, sprite.y] for sprite in sprites_list]
            while [apple.x, apple.y] in apple_bad_position:
                apple.rect.x = random.randint(1, 39) * 20
                apple.rect.y = random.randint(1, 29) * 20

        # grab the score for the next refresh
        score = str(snake.length)
        score_surface, score_rect = render_text(Text.SCORE_TEXT + score, (760, 640), Color.BLACK)

        # refreshing sprites, drawing borders
        screen.fill(Color.BLACK)
        sprites_list.update()
        sprites_list.draw(screen)
        draw_borders(screen)

        # updating the screen
        screen.blit(score_surface, score_rect)
        pygame.display.update()
        pygame.time.Clock().tick(11)

    return snake.length  # return the final score


# function that initiates the end sequence of the end screen
#
def end_screen(screen: pygame.display, score: int) -> None:
    replay = False

    while not replay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    replay = True

        screen.fill(Color.BLACK)
        draw_borders(screen)
        pygame.draw.rect(screen, Color.WHITE, [420 - 150, 330 - 30, 300, 60], 5)

        end_score_text = Text.SCORE_TEXT + str(score)
        score_surface, score_rect = render_text(end_score_text, (760, 640), Color.BLACK)
        end_surface, end_rect = render_text(Text.END_TEXT, (420, 330), Color.WHITE)

        screen.blit(score_surface, score_rect)
        screen.blit(end_surface, end_rect)
        pygame.display.update()

# Runner -------------------------------------------------------------------------------------------

def main() -> None:
    screen = init_screen()

    while True:
        start_screen(screen)
        score = run_snake_game(screen)
        end_screen(screen, score)


if __name__ == "__main__":
    main()

pygame.quit()  # un-init pygame module
