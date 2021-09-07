#
#  main.py
#  Description: This is a snake game created by team New Bee. The snake will move by key WASD and goal is to eat
#               apples appeared at a random location. If snake has eaten an apple, the score will plus one and the top
#               score will be recorded in a txt file named topScore.txt. If snake eats itself or hit the boundary of
#               the window, game over.
#  Created by: Richard Yang
#  Created On: Nov 25, 2019
#  Last Modified: Dec 3, 2019
#  Known Limitations: If press WASD these four keys rapidly at the same time, snake will bite itself.
####################################################################################################################
import random
import pygame
import sys
from pygame.locals import *
from pygame import mixer


def game_start_info():
    """When this function is called, it will keep showing a page says Snake Game. It will only return if key pressed"""
    ziti = pygame.font.Font('OpenSans-Bold.ttf', 120)
    zitisurf = ziti.render('Snake Game', True, blue)
    while True:
        biaoti = zitisurf.get_rect()
        biaoti.center = (Window_Width / 2, Window_Height / 2)
        display.blit(zitisurf, biaoti)
        keypress_info()
        if is_key_pressed():
            pygame.event.get()
            return
        pygame.display.update()
        snake_speedCLOCK.tick(snake_speed)


def game_ends_info():
    """When this function is called, it will keep showing a page says Game Over. It will only return if key pressed"""
    gameOver = pygame.font.Font('OpenSans-Bold.ttf', 120)
    gameWord = gameOver.render('Game', True, White)
    overWord = gameOver.render('Over!', True, White)
    gameWordRect = gameWord.get_rect()
    overWordRect = overWord.get_rect()
    gameWordRect.midtop = (Window_Width / 2, 150)
    overWordRect.midtop = (Window_Width / 2, gameWordRect.height + 50 + 80)

    display.blit(gameWord, gameWordRect)
    display.blit(overWord, overWordRect)
    keypress_info()
    pygame.display.update()
    pygame.time.wait(500)
    is_key_pressed()
    while True:
        if is_key_pressed():
            pygame.event.get()
            return


def draw_head(snake_positions):
    """(list)
    This function will only draw the snake head and cover it above the snake body."""
    snake_head_Section_Rect = pygame.Rect(snake_positions[HEAD]['x'] * cells_size, snake_positions[HEAD]['y'] * cells_size, cells_size, cells_size)
    pygame.draw.rect(display, Yellow, snake_head_Section_Rect)
    before_eat_snake_body = pygame.Rect(snake_positions[HEAD]['x'] * cells_size + 4, snake_positions[HEAD]['y'] * cells_size + 4, cells_size - 8, cells_size - 8)
    pygame.draw.rect(display, Orange, before_eat_snake_body)


def draw_snake(snake_positions):
    """(list)
    This function will draw the entire snake, include head and body. The colour has two layers"""
    for coord in snake_positions:
        x = coord['x'] * cells_size
        y = coord['y'] * cells_size
        after_eat_snake_body = pygame.Rect(x, y, cells_size, cells_size)
        pygame.draw.rect(display, DARKGreen, after_eat_snake_body)
        before_eat_snake_body = pygame.Rect(x + 8, y + 8, cells_size - 14, cells_size - 14)
        pygame.draw.rect(display, Green, before_eat_snake_body)


def snake_movement():
    """This function decides the movement of the snake in regards to the key WASD. It will also change global variables
    direction and head_update"""
    global direction, head_update
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_a) and direction != D:
                direction = A
            elif (event.key == K_d) and direction != A:
                direction = D
            elif (event.key == K_w) and direction != S:
                direction = W
            elif (event.key == K_s) and direction != W:
                direction = S
            elif event.key == K_ESCAPE:
                terminate()
    # add a segment in its direction and therefore form a new head:
    if direction == W:
        head_update = {'x': snake_positions[HEAD]['x'], 'y': snake_positions[HEAD]['y'] - 1}
    elif direction == A:
        head_update = {'x': snake_positions[HEAD]['x'] - 1, 'y': snake_positions[HEAD]['y']}
    elif direction == S:
        head_update = {'x': snake_positions[HEAD]['x'], 'y': snake_positions[HEAD]['y'] + 1}
    elif direction == D:
        head_update = {'x': snake_positions[HEAD]['x'] + 1, 'y': snake_positions[HEAD]['y']}


def eat_apple():
    """This function is to check whether snake has eaten an apple. If yes, create an new apple, if no, pop the tail of
    snake."""
    global apple
    if snake_positions[HEAD]['x'] == apple['x'] and snake_positions[HEAD]['y'] == apple['y']:
        # if snake has eaten an apple, create a new one with random location
        apple = {'x': random.randint(0, cells_w - 1), 'y': random.randint(0, cells_h - 1)}  # a new apple
    else:
        # snake is keep growing, so that if it doesn't eat an apple, it need to be 1 cell short every time
        snake_positions.pop()


def is_game_over():
    """This function will return True if the Snake has hit itself or the edge"""
    if snake_positions[HEAD]['x'] == -1 or snake_positions[HEAD]['x'] == cells_w or snake_positions[HEAD]['y'] == -1 or \
            snake_positions[HEAD]['y'] == cells_h:
        return True
    for snakeBody in snake_positions[1:]:
        if snakeBody['x'] == snake_positions[HEAD]['x'] and snakeBody['y'] == snake_positions[HEAD]['y']:
            return True


def draw_apple(apple_positions):
    """(dict)
    This function will draw an apple in regards to the parameter which should be a dictionary with random value of x & y"""
    x = apple_positions['x'] * cells_size
    y = apple_positions['y'] * cells_size
    apple_rect = pygame.Rect(x, y, cells_size, cells_size)
    pygame.draw.rect(display, Red, apple_rect)


def keypress_info():
    """this function is used to show the message on the bottom of the page. It is designed to appear on the beginning of
    the game and on the end of the game"""
    pressKeySurf = small_font.render('Press any key', True, White)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Window_Width - 630, Window_Height - 30)
    display.blit(pressKeySurf, pressKeyRect)


def draw_score(score):
    """(int)
    This function will print the current score and the score from topScore.txt
    the number inside the topScore.txt will always be the biggest number"""
    scoreSurf = small_font.render('Score: %d' % score, True, White)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 140, 10)
    display.blit(scoreSurf, scoreRect)

    topScoreFile = open("topScore.txt", 'r')
    textScore = topScoreFile.readline()
    topScoreFile.close()
    textScore = int(textScore)

    # obtain the top score
    if textScore >= score:
        topScore = textScore
    else:
        topScore = score
        topScoreFile_write = open('topScore.txt', 'w')
        topScore = str(topScore)
        topScoreFile_write.write(topScore)
        topScoreFile_write.close()

    scoreSurf2 = small_font.render('Top Score: %s' % topScore, True, White)
    scoreRect2 = scoreSurf.get_rect()
    scoreRect2.topleft = (Window_Width - 140, 40)
    display.blit(scoreSurf2, scoreRect2)


def is_key_pressed():
    """This function will call terminate() and end the whole program if Esc key is pressed
    And if other key is pressed, it will clear the queue"""
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyup_event = pygame.event.get(KEYUP)
    if len(keyup_event) == 0:
        return None
    if keyup_event[0].key == K_ESCAPE:
        terminate()
    return keyup_event[0].key


def terminate():
    """end the game by using sys.exit()"""
    pygame.quit()
    sys.exit()


def initial_program():
    """This function initialize a lot of global variables and will only be called once"""
    global snake_speedCLOCK, display, small_font, W, S, A, D, snake_speed, HEAD, Window_Height, Window_Width
    global cells_size, cells_w, cells_h, White, Black, Green, Red, DARKGreen, Yellow, Orange, blue

    pygame.init()
    mixer.music.load('Yiruma - River Flows in You.flac')    # load background music
    mixer.music.play(-1)

    W = 'up'
    S = 'down'  # keyboard keys
    A = 'left'
    D = 'right'

    snake_speed = 8     # change the speed here
    HEAD = 0

    # Note that window width and height have to be the multiple of cells_size, in this case, is 20
    Window_Width = 1100
    Window_Height = 700
    cells_size = 20
    cells_w = int(Window_Width / cells_size)  # Cell's Width
    cells_h = int(Window_Height / cells_size)  # Cell's Height

    White = (255, 255, 255)
    Black = (0, 0, 0)  # background color change here
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    DARKGreen = (0, 140, 0)
    Yellow = (255, 165, 0)
    Orange = (255, 255, 0)
    blue = (0, 0, 255)

    snake_speedCLOCK = pygame.time.Clock()
    display = pygame.display.set_mode((Window_Width, Window_Height))
    small_font = pygame.font.Font('OpenSans-Bold.ttf', 20)
    pygame.display.set_caption('Snake')
    initial_top_file = open("topScore.txt", "w")  # initial topScore.txt 's text to 0
    initial_top_file.write('0')
    initial_top_file.close()


def initial_snake():
    """This function initialize the postion of snake at the beginning of the game"""
    global initial_x, initial_y, snake_positions, direction, apple
    # initial position
    initial_x = 20
    initial_y = 20
    snake_positions = []
    initial_snake_length = 4
    initial_loop = 0
    # this loop sets the initial length for snake
    while initial_loop < initial_snake_length:
        snake_positions.append({'x': initial_x, 'y': initial_y})
        initial_x -= 1
        initial_loop += 1
    direction = D
    apple = {'x': random.randint(0, cells_w - 1), 'y': random.randint(0, cells_h - 1)}


def main():
    """This is the main function. This function will initialize the whole program by initial_program() and
    game_start_info(), then it will have an always true while loop to run the game. If the snake dead, it will go to
    game_ends_info() and will continue the while loop if a key is pressed."""
    initial_program()
    game_start_info()
    while True:
        initial_snake()

        # game runs here
        while True:
            snake_movement()
            eat_apple()
            if is_game_over():
                break   # and then shows the game end information
            display.fill(Black)       # background colour
            snake_positions.insert(0, head_update)
            draw_snake(snake_positions)
            draw_head(snake_positions)
            draw_apple(apple)
            draw_score(len(snake_positions) - 4)    # initial length of the snake is 4
            pygame.display.update()
            snake_speedCLOCK.tick(snake_speed)

        game_ends_info()


main()
