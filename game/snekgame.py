import pygame
import sys
import random
import os

pygame.init()

screenWidth = 400
screenHeight = 400
gridSize = 20
gridWidth = screenWidth // gridSize
gridHeight = screenHeight // gridSize
fps = 10 

window = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

bg = (20, 20, 30)
grid = (35, 35, 50)
snakeHead = (80, 220, 120)
snakeBody = (40, 170, 90)
snakeTail = (30, 130, 70)
food = (230, 70, 70)
text = (240, 240, 240)

black = (0, 0, 0)
white = (255, 255, 255)

font = pygame.font.SysFont(None, 28)
bigFont = pygame.font.SysFont(None, 60)

imgsFolder = os.path.join(os.path.dirname(__file__), "imgs")

def loadImage(fileName):
    image = pygame.image.load(os.path.join(imgsFolder, fileName)).convert_alpha()
    return pygame.transform.scale(image, (gridSize, gridSize))

appleImg = loadImage("appel.png")
headImg = loadImage("Sprite-0001.png")
bodyImg = loadImage("Sprite-0002.png")
tailImg = loadImage("Sprite-0003.png")

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

pygame.display.set_caption("Snek")

def randomFood(snake):
    while True:
        spot = (random.randint(0, gridWidth -1), random.randint(0, gridHeight - 1))
        if spot not in snake:
            return spot

def resetGame():
    global snake, direction, nextDirection, foodPos, score, gameOver, started
    middleX = gridWidth // 2
    middleY = gridHeight // 2
    snake = [(middleX, middleY), (middleX - 1, middleY), (middleX - 2, middleY)]
    direction = right
    nextDirection = right
    foodPos = randomFood(snake)
    score = 0
    gameOver = False
    started = False

resetGame()

def drawSquare(color, pos):
    x, y = pos
    pygame.draw.rect(window, color, (x * gridSize + 1, y * gridSize + 1, gridSize - 2, gridSize -2), border_radius = 4)

def drawImage(image, pos, angle = 0):
    rotated = pygame.transform.rotate(image, angle - 90)
    window.blit(rotated, (pos[0] * gridSize, pos[1] * gridSize))

def getAngle(fromPos, toPos):
    dx = toPos[0] - fromPos[0]
    dy = toPos [1] - fromPos[1]
    if dx == 1:
        return 0
    if dx == -1:
        return 180
    if dy == -1:
        return 90
    return 270

def drawGrid():
    for x in range(0, screenWidth, gridSize):
        pygame.draw.line(window, grid, (x, 0), (x, screenHeight))

    for y in range(0, screenHeight, gridSize):
        pygame.draw.line(window, grid, (0, y), (screenWidth, y))

def moveSnake():
    global direction, foodPos, score, gameOver

    direction = nextDirection
    headX, headY, = snake[0]
    newHead = (headX + direction[0], headY + direction[1])

    if not (0 <= newHead[0] < gridWidth and 0 <= newHead[1] < gridHeight):
        gameOver = True
        return

    if newHead in snake[:-1]:
        gameOver = True
        return

    snake.insert(0, newHead)

    if newHead == foodPos:
        score += 1
        foodPos = randomFood(snake)
    else:
        snake.pop()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            started = True

            if gameOver and event.key == pygame.K_SPACE:
                resetGame()

            if event.key in (pygame.K_UP, pygame.K_w) and direction != down:
                nextDirection = up
            elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != up:
                nextDirection = down
            elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != right:
                nextDirection = left
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != left:
                nextDirection = right

    if started and not gameOver:
        moveSnake()

    window.fill(bg)
    drawGrid()
    drawImage(appleImg, foodPos, 90)

    for i, piece in enumerate(snake):
        if i == 0:
            drawImage(headImg, piece, getAngle(snake[1], snake[0]))
        elif i == len(snake) - 1:
            drawImage(bodyImg, piece, getAngle(piece, snake[i - 1]))
        else:
            drawImage(bodyImg, piece, getAngle(piece, snake[i - 1]))

    window.blit(font.render(f"Score: {score}", True, text), (8, 6))
    if gameOver:
        msg = bigFont.render("Game Over", True, white)
        sub = font.render("Press Space to restart", True, text)
        window.blit(msg, msg.get_rect(center=(screenWidth // 2, screenHeight // 2 - 20)))
        window.blit(sub, sub.get_rect(center=(screenWidth // 2, screenHeight // 2 + 25)))
    if not started:
        hint = font.render("Press an arrow key to start", True, text)
        window.blit(hint, hint.get_rect(center=(screenWidth // 2, screenHeight // 2)))

    pygame.display.flip()

    clock.tick(fps)




