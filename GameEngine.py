PIECE_SIZE = 50

class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.moveHistory = []
        self.whiteTurn = True  # false if black turn

    def makeMove(self, moveString):
        oldRow, oldCol, newRow, newCol = int(moveString[0]), int(moveString[1]), int(moveString[2]), int(moveString[3])
        recordMove = moveString
        recordMove += self.board[newRow][newCol]
        self.board[newRow][newCol] = self.board[oldRow][oldCol]
        self.board[oldRow][oldCol] = '--'
        self.moveHistory.append(recordMove)

    def undoMove(self):
        if self.moveHistory:
            lastMove = self.moveHistory.pop()
            oldRow, oldCol, newRow, newCol, newPiece = int(lastMove[0]), int(lastMove[1]), int(lastMove[2]), int(lastMove[3]), str(lastMove[4] + lastMove[5])
            self.board[oldRow][oldCol] = self.board[newRow][newCol]
            self.board[newRow][newCol] = newPiece


    def emptySpace(self, row, col): # helper function to return whether this space is empty
        if self.board[row][col] == '--':
            return True
        return False

    def enemySpace(self, row, col): # helper function to return whether this space has an enemy
        if self.whiteTurn and self.board[row][col][0] == 'b':
            return True
        elif not self.whiteTurn and self.board[row][col][0] == 'w':
            return True
        return False


    def findKingSpace(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                piece = self.board[row][col] # for example, '--' or 'bP'
                if self.whiteTurn and piece == "wK":
                    return str(row) + str(col)
                elif not self.whiteTurn and piece == "bK":
                    return str(row) + str(col)
        return None

    def getValidMoves(self):
        # TODO - Based on check (king under attack), which pieces can move where?
        # Remove invalid moves from list of possible moves.
        moves = self.getAllPossibleMoves()
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            kingSpace = self.findKingSpace()

            self.whiteTurn = not self.whiteTurn
            enemyMoves = self.getAllPossibleMoves()
            for m in enemyMoves:
                if m[2:4] == kingSpace:
                    moves.pop(i)
                    break

            self.whiteTurn = not self.whiteTurn
            self.undoMove()
        return moves

    def getAllPossibleMoves(self):
        # Based on turn color and piece patterns (ignoring check), which pieces can move where?
        # BONUS: code en passant and castling for extra credit points
        moves = []
        # this is what moves look like - strings of
        # starting row and column then destination row and column
        if self.whiteTurn:
            color = 'w'
        else:
            color = 'b'
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                piece = self.board[row][col] # for example, 'bN'
                if piece[0] == color: # if turn matches piece color
                    if piece[1] == 'P': # PAWN MOVES
                        self.getPawnMoves(row, col, moves)
                    elif piece[1] == 'R': #ROOK MOVES
                        self.getRookMoves(row, col, moves)
                    elif piece[1] == 'B':
                        self.getBishopMoves(row, col, moves)
                    elif piece[1] == 'Q':
                        self.getQueenMoves(row, col, moves)
                    elif piece[1] == "N":
                        self.getKnightMoves(row, col, moves)
                    elif piece[1] == "K":
                        self.getKingMoves(row, col, moves)
                    #TODO - code all other piece moves
                    # self.getKingMoves(row, col, moves)
        return moves

    def getPawnMoves(self, row, col, moves):
        # white pawns move UP the board (subtract from rows)
        if self.whiteTurn and row > 0:
            # can move 1 space forward if empty
            if self.emptySpace(row - 1, col):
                move = str(row) + str(col) + str(row - 1) + str(col) # for example, '6252'
                moves.append(move)

                if row == 6 and self.emptySpace(row - 2, col):
                    move = str(row) + str(col) + str(row - 2) + str(col)
                    moves.append(move)

            if col > 0 and self.enemySpace(row - 1, col - 1):
                move = str(row) + str(col) + str(row - 1) + str(col - 1)
                moves.append(move)
            if col < 7 and self.enemySpace(row - 1, col + 1):
                move = str(row) + str(col) + str(row - 1) + str(col + 1)
                moves.append(move)

        elif not self.whiteTurn and row < 7:
            if self.emptySpace(row + 1, col):
                move = str(row) + str(col) + str(row + 1) + str(col)
                moves.append(move)

                if row == 1 and self.emptySpace(row + 2, col):
                    move = str(row) + str(col) + str(row + 2) + str(col)
                    moves.append(move)

            if col > 0 and self.enemySpace(row + 1, col - 1):
                move = str(row) + str(col) + str(row + 1) + str(col - 1)
                moves.append(move)
            if col < 7 and self.enemySpace(row + 1, col + 1):
                move = str(row) + str(col) + str(row + 1) + str(col + 1)
                moves.append(move)


    def getRookMoves(self, row, col, moves):
        if row != 0:
            for i in range(1, row + 1):
                if self.emptySpace(row - i, col):
                    move = str(row) + str(col) + str(row - i) + str(col)
                    moves.append(move)
                elif self.enemySpace(row - i, col):
                    move = str(row) + str(col) + str(row - i) + str(col)
                    moves.append(move)
                    break
                else:
                    break

        for i in range(7 - row):
            if self.emptySpace(row + i + 1, col):
                move = str(row) + str(col) + str(row + i + 1) + str(col)
                moves.append(move)
            elif self.enemySpace(row + i + 1, col):
                move = str(row) + str(col) + str(row + i + 1) + str(col)
                moves.append(move)
                break
            else:
                break

        if col != 0:
            for j in range(1, col + 1):
                if self.emptySpace(row, col - j):
                    move = str(row) + str(col) + str(row) + str(col - j)
                    moves.append(move)
                elif self.enemySpace(row, col - j):
                    move = str(row) + str(col) + str(row) + str(col - j)
                    moves.append(move)
                    break
                else:
                    break

        for j in range(7 - col):
            if self.emptySpace(row, col + j + 1):
                move = str(row) + str(col) + str(row) + str(col + j + 1)
                moves.append(move)
            elif self.enemySpace(row, col + j + 1):
                move = str(row) + str(col) + str(row) + str(col + j + 1)
                moves.append(move)
                break
            else:
                break


    def getBishopMoves(self, row, col, moves):
        for i in range(1, row + 1):
            for j in range(1, col + 1):
                if self.emptySpace(row - i, col - j) and i == j:
                    move = str(row) + str(col) + str(row - i) + str(col - j)
                    moves.append(move)
                elif self.enemySpace(row - i, col - j) and i == j:
                    move = str(row) + str(col) + str(row + i) + str(col + j)
                    moves.append(move)
                    break

            for j in range(1, 8 - col):
                if self.emptySpace(row - i, col + j) and i == j:
                    move = str(row) + str(col) + str(row - i) + str(col + j)
                    moves.append(move)
                elif self.enemySpace(row - i, col + j) and i == j:
                    move = str(row) + str(col) + str(row + i) + str(col + j)
                    moves.append(move)
                    break


        for i in range(1, 8 - row):
            for j in range(1, col + 1):
                if self.emptySpace(row + i, col - j) and i == j:
                    move = str(row) + str(col) + str(row + i) + str(col - j)
                    moves.append(move)
                elif self.enemySpace(row + i, col - j) and i == j:
                    move = str(row) + str(col) + str(row + i) + str(col + j)
                    moves.append(move)
                    break

            for j in range(1, 8 - col):
                if self.emptySpace(row + i, col + j) and i == j:
                    move = str(row) + str(col) + str(row + i) + str(col + j)
                    moves.append(move)
                elif self.enemySpace(row + i, col + j) and i == j:
                    move = str(row) + str(col) + str(row + i) + str(col + j)
                    moves.append(move)
                    break



    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)


    def getKnightMoves(self, row, col, moves):
        for i in range(-2, 4, 4):
            for j in range(-1, 3, 2):
                if 0 <= row + i <= 7 and 0 <= col + j <= 7:
                    if self.emptySpace(row + i, col + j) or self.enemySpace(row + i, col + j):
                        move = str(row) + str(col) + str(row + i) + str(col + j)
                        moves.append(move)
                if 0 <= row + j <= 7 and 0 <= col + i <= 7:
                    if self.emptySpace(row + j, col + i) or self.enemySpace(row + j, col + i):
                        move = str(row) + str(col) + str(row + j) + str(col + i)
                        moves.append(move)

    def getKingMoves(self, row, col, moves):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i <= 7 and 0 <= col + j <= 7:
                    if self.emptySpace(row + i, col + j) or self.enemySpace(row + i, col + j):
                        move = str(row) + str(col) + str(row + i) + str(col + j)
                        moves.append(move)


    def checkPawnPromotion(self):
        for i in range(8):
            if self.board[0][i] == 'wP':
                self.board[0][i] = 'wQ'
            elif self.board[7][i] == 'bP':
                self.board[7][i] = 'bQ'