# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys

from pygame.locals import *

FPS = 10
SPEED_INCREMENT = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
GOLD      = ( 255, 215,  0)
BLUE      = ( 0,   0,  255)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    secondWorm = None
    secondWorm_dir = None
    secondWorm_timer = pygame.time.get_ticks()
    # Start the apple in a random place.
    apple = getRandomLocation()
    yellow_apple = None  # Initially, no yellow apple
    yellow_apple_timer = 0
    blue_apple = None
    blue_apple_timer = 0
    appleseaten = 0

    game_start_time = pygame.time.get_ticks()  # Record the start time

    global FPS
    while True:  # main game loop
        elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000
        if elapsed_time > 0 and elapsed_time % 30 == 0:  # Every 30 seconds
            FPS += SPEED_INCREMENT
            game_start_time += 30000
            # Prevent repeated increments for the same interval


        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # Move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': (wormCoords[HEAD]['y'] - 1) % CELLHEIGHT}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': (wormCoords[HEAD]['y'] + 1) % CELLHEIGHT}
        elif direction == LEFT:
            newHead = {'x': (wormCoords[HEAD]['x'] - 1) % CELLWIDTH, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': (wormCoords[HEAD]['x'] + 1) % CELLWIDTH, 'y': wormCoords[HEAD]['y']}

        # Check if the worm has hit itself
        if newHead in wormCoords:
            return  # game over

        wormCoords.insert(0, newHead)

        # Check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation() # set a new apple somewhere
            appleseaten = appleseaten + 1
        else:
            del wormCoords[-1]  # remove worm's tail segment


        if yellow_apple:
            if wormCoords[HEAD]['x'] == yellow_apple['x'] and wormCoords[HEAD]['y'] == yellow_apple['y']:
                if len(wormCoords) > 2:
                    del wormCoords[-1]  # reduce worm's length
                yellow_apple = None  # remove yellow apple
                yellow_apple_timer = 0  # reset timer
            elif yellow_apple_timer > FPS * 5:  # Yellow apple disappears after 5 seconds
                yellow_apple = None
                yellow_apple_timer = 0
            else:
                yellow_apple_timer += 1
        else:
            # Randomly spawn a yellow apple
            if random.randint(0, 100) < 2:  # 2% chance per frame
                yellow_apple = getRandomLocation()

        if blue_apple:
            if wormCoords[HEAD]['x'] == blue_apple['x'] and wormCoords[HEAD]['y'] == blue_apple['y']:
                if FPS >5:
                    FPS -=SPEED_INCREMENT  # reduce worm's length
                blue_apple = None  # remove yellow apple
                blue_apple_timer = 0  # reset timer
            elif blue_apple_timer > FPS * 5:  # Yellow apple disappears after 5 seconds
                blue_apple = None
                blue_apple_timer = 0
            else:
                blue_apple_timer += 1
        else:
            # Randomly spawn a yellow apple
            if random.randint(0, 100) < 2:  # 2% chance per frame
                blue_apple = getRandomLocation()


        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        if yellow_apple:
            drawGoldenApple(yellow_apple)
        if blue_apple:
            drawBlueApple(blue_apple)
        drawScore(appleseaten)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def getRandomLocationWithTimeDelay():
    time = 10
    while time == 0:
        return {'x': random.randint(0, CELLWIDTH), 'y': random.randint(0, CELLHEIGHT)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGoldenApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    goldenAppleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GOLD, goldenAppleRect)

def drawBlueApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    blueAppleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BLUE, blueAppleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()