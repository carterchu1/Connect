import pygame
import random
import sys
from connect import Connect
from pygame.locals import *

FPS = 30
WINDOWHEIGHT = 500
WINDOWWIDTH = 365
BOXSIZE = 40
MARGIN = 5
BOARDSIZE = 8

#            R    G    B
BLACK    = (  0,   0,   0)
GRAY     = (100, 100, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
LIME     = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
CYAN     = (  0, 255, 255)
MAGENTA  = (255,   0, 255)
MAROON   = (128,   0,   0)
GREEN    = (  0, 128,   0)
PURPLE   = (128,   0, 128)
TEAL     = (  0, 128, 128)
NAVY     = (  0,   0, 128)
OLIVE    = (128, 128,   0)

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
OVAL = 'oval'

ALLCOLORS = [RED, LIME, BLUE, YELLOW, CYAN, MAGENTA, MAROON,
             GREEN, PURPLE, TEAL, NAVY, OLIVE]
ALLSHAPES = [DONUT, SQUARE, DIAMOND, OVAL]


def main():
    global FPSCLOCK, DISPLAYSURF, pathDict
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pathDict = {}

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Connect')

    initialBoard = Connect(BOARDSIZE, BOARDSIZE)
    initialBoard.generate()
    currentBoard = createBoard(initialBoard)

    DISPLAYSURF.fill(GRAY)

    solutionUp = False
    mouseDrag = False
    prev = [None, None]
    while True:
        mouseClick = False
        onClick = False

        DISPLAYSURF.fill(GRAY)
        drawBoard(currentBoard)
        resetButton()
        reset = pygame.Rect(35, 425, 75, 20)
        solutionButton()
        solution = pygame.Rect(135, 425, 75, 20)
        newGameButton()
        newGame = pygame.Rect(235, 425, 75, 20)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                onClick = True
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseDrag = False
                mouseClick = True

        if mouseClick and reset.collidepoint(mousex, mousey):
            currentBoard = createBoard(initialBoard)
            solutionUp = False
        elif mouseClick and solution.collidepoint(mousex, mousey):
            showSolution(initialBoard)
            pygame.display.update()
            solutionUp = True
        elif mouseClick and newGame.collidepoint(mousex, mousey):
            pathDict = {}
            initialBoard, currentBoard = newBoard()
            solutionUp = False
        else:
            x, y = getBoxAtPixel(mousex, mousey)
            if x is not None:
                if onClick and currentBoard[x][y][0]:
                    prev = [x, y]
                    mouseDrag = True
                elif mouseDrag and (x != prev[0] or y != prev[1]):
                    if checkValid(currentBoard, prev[0], prev[1], x, y):
                        for i in range(1, 4):
                            currentBoard[x][y][i] = currentBoard[prev[0]][prev[1]][i]
                        prev = [x, y]

        if not solutionUp:
            pygame.display.update()
        FPSCLOCK.tick(FPS)


def topLeftOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + MARGIN) + 5
    top = boxy * (BOXSIZE + MARGIN) + 5
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):
            left, top = topLeftOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(color, shape, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = topLeftOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, WHITE, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getColorAndShape(board, boxx, boxy):
    return board[boxx][boxy][2], board[boxx][boxy][3]


def checkValid(board, prevx, prevy, boxx, boxy):
    edges = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in edges:
        if board[boxx][boxy] is not None:
            if not board[boxx][boxy][1]:
                if prevx + dx == boxx and prevy + dy == boxy:
                    return True
    return False


def createBoard(board):
    colors = ALLCOLORS.copy()
    random.shuffle(colors)
    newBoard = [[[False, False, None, None] for i in range(BOARDSIZE)] for j in range(BOARDSIZE)]
    for r in range(BOARDSIZE):
        for c in range(BOARDSIZE):
            if board.board[r][c].endpoint:
                if board.board[r][c].path not in pathDict:
                    shape = random.randint(0, 3)
                    color = colors.pop()
                    newBoard[r][c] = [True, True, color, ALLSHAPES[shape]]
                    pathDict[board.board[r][c].path] = [color, ALLSHAPES[shape]]
                else:
                    symbol = pathDict[board.board[r][c].path]
                    newBoard[r][c] = [True, True, symbol[0], symbol[1]]
            elif board.board[r][c].path == 0:
                newBoard[r][c] = None
    return newBoard


def drawBoard(board):
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):
            left, top = topLeftOfBox(boxx, boxy)
            if board[boxx][boxy] is None:
                pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, BOXSIZE, BOXSIZE))
            elif board[boxx][boxy][2] is None or board[boxx][boxy][3] is None:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
            else:
                color, shape = getColorAndShape(board, boxx, boxy)
                drawIcon(color, shape, boxx, boxy)


def newBoard():
    initialBoard = Connect(BOARDSIZE, BOARDSIZE)
    initialBoard.generate()
    currentBoard = createBoard(initialBoard)
    return initialBoard, currentBoard


def showSolution(initialBoard):
    for boxx in range(BOARDSIZE):
        for boxy in range(BOARDSIZE):
            left, top = topLeftOfBox(boxx, boxy)
            if initialBoard.board[boxx][boxy].path == 0:
                pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, BOXSIZE, BOXSIZE))
            else:
                symbol = pathDict[initialBoard.board[boxx][boxy].path]
                color = symbol[0]
                shape = symbol[1]
                drawIcon(color, shape, boxx, boxy)


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def resetButton():
    pygame.draw.rect(DISPLAYSURF, WHITE, (35, 425, 75, 20))
    smallText = pygame.font.Font("freesansbold.ttf", 13)
    textSurf, textRect = text_objects("Reset", smallText)
    textRect.center = ((35 + (75 / 2)), (425 + (20 / 2)))
    DISPLAYSURF.blit(textSurf, textRect)


def solutionButton():
    pygame.draw.rect(DISPLAYSURF, WHITE, (135, 425, 75, 20))
    smallText = pygame.font.Font("freesansbold.ttf", 13)
    textSurf, textRect = text_objects("Solution", smallText)
    textRect.center = ((135 + (75 / 2)), (425 + (20 / 2)))
    DISPLAYSURF.blit(textSurf, textRect)


def newGameButton():
    pygame.draw.rect(DISPLAYSURF, WHITE, (235, 425, 75, 20))
    smallText = pygame.font.Font("freesansbold.ttf", 13)
    textSurf, textRect = text_objects("New Game", smallText)
    textRect.center = ((235 + (75 / 2)), (425 + (20 / 2)))
    DISPLAYSURF.blit(textSurf, textRect)


if __name__ == '__main__':
    main()
