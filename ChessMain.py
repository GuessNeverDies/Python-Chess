import pygame as p
import GameEngine as g

def setup():
    global screen, clock, s, images
    p.init()  # initialize all pygame stuff
    screen = p.display.set_mode((g.PIECE_SIZE * 8, g.PIECE_SIZE * 8))  # create display object
    clock = p.time.Clock()  # create time object
    s = g.GameState()
    images = loadImages()

def main():
    global screen, clock, s
    setup()  # call the setup function that we defined above
    done = False
    firstClick = True
    x1 = y1 = None
    while not done:  # loop continues until done = True
        screen.fill('black')
        for event in p.event.get():  # iterate through event queue
            if event.type == p.QUIT:  # if we click the red X to close the window
                done = True  # end loop
            elif event.type == p.MOUSEBUTTONDOWN:
                if firstClick:
                    x1, y1 = p.mouse.get_pos()
                    x1, y1 = x1 // g.PIECE_SIZE, y1 // g.PIECE_SIZE
                    print("Click destination.")
                else:
                    x2, y2 = p.mouse.get_pos()
                    x2, y2 = x2 // g.PIECE_SIZE, y2 // g.PIECE_SIZE
                    if (x1 != x2 or y1 != y2) and not s.emptySpace(y1, x1):
                        moveString = str(y1) + str(x1) + str(y2) + str(x2)
                        if moveString in s.getValidMoves():
                            s.makeMove(moveString)
                            s.whiteTurn = not s.whiteTurn
                    print("Choose a piece to move.")

                    print('white turn?', s.whiteTurn)
                firstClick = not firstClick
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    s.undoMove()
                    firstClick = not firstClick
                    s.whiteTurn = not s.whiteTurn

        s.checkPawnPromotion()
        drawBoard()
        if not firstClick and x1 is not None and y1 is not None:
            p.draw.rect(screen, 'green', (x1 * g.PIECE_SIZE, y1 * g.PIECE_SIZE, g.PIECE_SIZE, g.PIECE_SIZE))
        elif x1 is not None and y1 is not None:
            drawBoard()
        drawPieces()

        p.display.flip()  # update the screen
        clock.tick(20)  # FPS of screen updating
    p.quit()  # close display window (and all pygame stuff) after ending loop

# TODO - create a 8 by 8 checkerboard pattern of rectangles (squares)
def drawBoard():
    side = g.PIECE_SIZE
    for i in range(8):
        for j in range(8):
            if (i+j) % 2 == 0:
                p.draw.rect(screen, 'seashell', (i * side, j * side, side, side))
            else:
                p.draw.rect(screen, 'gray40', (i * side, j * side, side, side))
    # TODO - add 63 more rectangles. USE A LOOP!

# DONE - this function loads and resizes all of the images
def loadImages():
    imageDictionary = {}
    names = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK',
             'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for name in names:
        img = p.image.load('Images/' + name + '.png')
        img = p.transform.scale(img, (g.PIECE_SIZE, g.PIECE_SIZE))
        imageDictionary[name] = img
    return imageDictionary

# TODO - use s.board to find which pieces appear where.
# Blit ALL images in the correct locations as the pieces move.
def drawPieces():
    for i in range(8):
        for j in range(8):
            if s.board[i][j] != '--':
                screen.blit(images[s.board[i][j]], (j * g.PIECE_SIZE, i * g.PIECE_SIZE))




# python script to run the main function
if __name__ == "__main__":
    main()
