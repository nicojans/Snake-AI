import numpy as np
import math
import pygame


class Game:

    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    SIZE = 50
    FONT = 'comicsans'

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._score = 0
        self._snake = None
        self._food = None

    def reset(self):
        self._score = 0
        self._generate_snake()
        self._generate_food()

    def move(self, direction):
        new_head = list(self._snake[0])
        if direction == 0:
            new_head[1] -= 1
        elif direction == 1:
            new_head[0] += 1
        elif direction == 2:
            new_head[1] += 1
        elif direction == 3:
            new_head[0] -= 1

        if self._is_dead(new_head):
            return False

        self._snake.insert(0, new_head)
        if new_head != self._food:
            self._snake.pop()
        else:
            if len(self._snake) == self._width * self._height:
                return False
            else:
                self._generate_food()
                self._score += 1
        return True

    def state(self):
        x = self._snake[0][0]
        y = self._snake[0][1]
        # distance from food
        food_x = self._food[0] - x
        food_y = self._food[1] - y
        state = [food_x if food_x > 0 else 25, food_y if food_y > 0 else 25]
        state += [food_x if food_x < 0 else 25, food_y if food_y < 0 else 25]
        # available space
        state += [self._space_available([x + 1, y])]
        state += [self._space_available([x, y - 1])]
        state += [self._space_available([x - 1, y])]
        state += [self._space_available([x, y + 1])]

        return np.array(state)

    def play_new_game(self, speed, ai_next_movement=None):
        self.reset()
        game_width = self._width * self.SIZE
        game_height = self._height * self.SIZE
        pygame.init()
        screen = pygame.display.set_mode((game_width, game_height))
        counter = 0
        direction = 1
        done = False
        alive = True

        clock = pygame.time.Clock()
        font_score = pygame.font.SysFont(self.FONT, 20)
        font_game_over = pygame.font.SysFont(self.FONT, 50)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset()
                    alive = True
                    direction = 1

            if ai_next_movement is None:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP]:
                    direction = 0
                if pressed[pygame.K_RIGHT]:
                    direction = 1
                if pressed[pygame.K_DOWN]:
                    direction = 2
                if pressed[pygame.K_LEFT]:
                    direction = 3
            else:
                direction = ai_next_movement(self.state())

            counter += 1
            if counter == speed:
                alive = self.move(direction)
                counter = 0

            screen.fill((0, 0, 0))
            if alive:
                for elem in self._snake:
                    rect = pygame.Rect(elem[0] * self.SIZE, elem[1] * self.SIZE, self.SIZE, self.SIZE)
                    pygame.draw.rect(screen, self.BLUE, rect)
                rect = pygame.Rect(self._food[0] * self.SIZE, self._food[1] * self.SIZE, self.SIZE, self.SIZE)
                pygame.draw.rect(screen, self.RED, rect)
                text = font_score.render(str(self._score), True, self.WHITE)
                screen.blit(text, (game_width - text.get_width(), 15))
            else:
                text1 = font_game_over.render('GAME OVER', True, self.WHITE)
                text2 = font_game_over.render('Score: ' + str(self._score), True, self.WHITE)
                screen.blit(text1, ((game_width - text1.get_width()) / 2, (game_height - text1.get_height()) / 2 - 25))
                screen.blit(text2, ((game_width - text2.get_width()) / 2, (game_height - text2.get_height()) / 2 + 25))

            pygame.display.flip()

            clock.tick(60)

    def _generate_snake(self):
        self._snake = [[4, 4], [4, 3], [4, 2]]

    def _generate_food(self):
        self._food = None
        while self._food is None:
            new_food = [np.random.randint(0, self._width), np.random.randint(0, self._height)]
            self._food = new_food if not self._is_snake(new_food) else None

    def _is_dead(self, block):
        return self._out_of_bound(block) or self._is_snake(block)

    def _is_snake(self, block):
        for e in self._snake:
            if e == block:
                return True
        return False

    def _out_of_bound(self, block):
        return block[0] < 0 or block[1] < 0 or block[0] >= self._width or block[1] >= self._height

    def _space_available(self, block):
        blocks = [[]]
        self._adjoined_blocks(block, blocks)
        return math.log(len(blocks), 10)

    def _adjoined_blocks(self, block, blocks):
        for b in blocks:
            if b == block:
                return
        if not self._is_dead(block):
            blocks.insert(0, block)
            self._adjoined_blocks([block[0] + 1, block[1]], blocks)
            self._adjoined_blocks([block[0] - 1, block[1]], blocks)
            self._adjoined_blocks([block[0], block[1] + 1], blocks)
            self._adjoined_blocks([block[0], block[1] - 1], blocks)

    @property
    def score(self):
        return self._score
