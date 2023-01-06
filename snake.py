import pygame
import sys
import random
from pygame import Vector2


class SNAKE:
    def __init__(self):
        self.score = 0
        self.reset()

    def new_snakeb(self):
        self.snakecc = self.snakec[:]
        self.snakecc.insert(0, self.snakecc[0]+self.direction)
        self.snakec = self.snakecc

    def move(self):
        #self.snakecc = self.snakec[:-1]
        #self.snakecc.insert(0, self.snakecc[0]+self.direction)
        #self.snakec = self.snakecc
        self.score = len(self.snakec) - 3
        pygame.display.set_caption(f"Score : {main_game.snake.score}")
        del self.snakec[-1]
        self.snakec.insert(0, self.snakec[0] + self.direction)

    def draw(self):
        for (i, j) in self.snakec:
            self.snaker = pygame.rect.Rect(i*30, j*30, 30, 30)
            pygame.draw.rect(screen, 'black', self.snaker)

    def reset(self):
        if self.score > 0:
            import os
            import datetime
            date = datetime.datetime.today()
            date = str(date)
            date = date[:19]
            if os.path.exists('Score.txt'):
                with open('Score.txt', 'a') as file:
                    file.write(f'{date}\tScore : {self.score}\n')
            else:
                with open('Score.txt', 'w') as file:
                    file.write(f'{date}\tScore : {self.score}\n')
        self.score = 0
        start_types = {1: Vector2(0, 1), 2: Vector2(
            1, 0), 3: Vector2(0, -1), 4: Vector2(-1, 0)}
        self.snakec = [Vector2(random.randint(5, 10), random.randint(5, 10))]
        self.direction = start_types[random.randint(1, 4)]
        self.new_snakeb()
        self.new_snakeb()


class FOOD:
    def __init__(self):
        self.new_random()

    def draw(self):
        foodr = pygame.rect.Rect(self.food[0]*30, self.food[1]*30, 30, 30)
        pygame.draw.rect(screen, 'green', foodr)

    def new_random(self):
        self.food = Vector2(random.randint(0, 15), random.randint(0, 15))


class MAIN:
    def __init__(self):
        self.food = FOOD()
        self.snake = SNAKE()
        self.fail = False
        self.move = False

    def game_update(self):
        self.snake.move()
        self.check_eat()
        self.check_fail()

    def game_draw(self):
        self.food.draw()
        self.snake.draw()

    def new_food(self):
        self.food.new_random()
        while (Vector2(self.food.food.x, self.food.food.y) in self.snake.snakec):
            self.food.new_random()

    def check_eat(self):  # Collision
        if self.snake.snakec[0] == self.food.food:
            self.eat = True
            self.new_food()
            self.snake.new_snakeb()

    def check_fail(self):
        for snakeb in self.snake.snakec[1:]:
            if self.snake.snakec[0] == snakeb:
                self.fail = True

        if (self.snake.snakec[0].x < 0 or self.snake.snakec[0].x > 15) or (self.snake.snakec[0].y < 0 or self.snake.snakec[0].y > 15):
            self.fail = True

        if self.fail == True:
            self.move = False
            self.snake.reset()
            self.fail = False


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption('My Game')
screen.fill('white')
food_ate = True

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 160)

main_game = MAIN()

while True:

    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            main_game.fail = True
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            main_game.move = True
            if event.key == pygame.K_UP:
                if main_game.snake.direction != Vector2(0, 1):
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction != Vector2(0, -1):
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction != Vector2(1, 0):
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction != Vector2(-1, 0):
                    main_game.snake.direction = Vector2(1, 0)

        if (event.type == SCREEN_UPDATE and main_game.move == True):
            main_game.game_update()

    screen.fill('white')
    main_game.game_draw()

    clock.tick(60)
    pygame.display.update()
