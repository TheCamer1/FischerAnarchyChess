import random
from itertools import count

darkSquares = [
    22, 24, 26, 28,
    31, 33, 35, 37,
    42, 44, 46, 48,
    51, 53, 55, 57,
    62, 64, 66, 68,
    71, 73, 75, 77,
    82, 84, 86, 88,
    91, 93, 95, 97
]
lightSquares = [x - 1 for x in darkSquares]
exclusions = [x for x in range(20)] + \
    [x for x in range(100,120)] + \
    [x for x in range(20,91,10)] + \
    [x for x in range(29,100,10)]

board = list(
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' ........\n'  #  20 - 29
    ' ........\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' ........\n'  #  80 - 89
    ' ........\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
)
whitePieces = "PPPPPPPPRNBQKBNR"
blackPieces = "pppppppprnbqkbnr"

N, E, S, W = -10, 1, 10, -1
whiteDirections = {
    'P': (N+W, N+E),
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}
blackDirections = {
    'p': (S+W, S+E),
    'n': whiteDirections['N'],
    'b': whiteDirections['B'],
    'r': whiteDirections['R'],
    'q': whiteDirections['Q'],
    'k': whiteDirections['K'],
}

def getRandomPosition(start, end, exclusions):
    return random.choice(list(set([x for x in range(start, end)]) - set(exclusions)));

def printBoard(board):
    rows = []
    for i in range(2,10):
        row = ""
        for j in range(1,9):
            character = board[10*i + j]
            if character.isspace():
                continue
            row += ' ' + character
        print(row)
        rows.append(row)
    fen = ""
    for row in rows:
        blankSpaces = 0
        for character in row:
            if character.isspace():
                continue
            if character != ".":
                if blankSpaces != 0:
                    fen += str(blankSpaces)
                    blankSpaces = 0
                fen += character
                continue
            blankSpaces += 1
        if blankSpaces != 0:
            fen += str(blankSpaces)
        fen += '/'
    print(fen + " w - - 0 1")

def setPieces(board, pieces):
    bishopExclusions = None
    for piece in pieces:
        if piece == 'K' or piece == 'k':
            continue
        position = 0
        if piece == 'p' or piece == 'P':
            position = getRandomPosition(31, 89, exclusions)
        else:
            position = getRandomPosition(21, 99, exclusions)

        if piece == 'b' or piece == 'B':
            if bishopExclusions == None:
                if position in darkSquares:
                    bishopExclusions = darkSquares
                if position in lightSquares:
                    bishopExclusions = lightSquares
            else:
                position = getRandomPosition(21, 99, bishopExclusions + exclusions)
        board[position] = piece
        exclusions.append(position)

def setKing(board, king, enemyDirections):
    attackedSquares = []
    for piece in enemyDirections.keys():
        for position in [i for i, x in enumerate(board) if x == piece]:
            for direction in enemyDirections[piece]:
                for newPosition in count(position+direction, direction):
                    square = board[newPosition]
                    if square != '.':
                        break
                    attackedSquares.append(newPosition)
                    if piece in 'PNKpnk':
                        break
    kingPosition = getRandomPosition(21, 99, exclusions + attackedSquares)
    board[kingPosition] = king
    exclusions.append(kingPosition)

setPieces(board, whitePieces)
setPieces(board, blackPieces)
setKing(board, 'K', blackDirections)
setKing(board, 'k', whiteDirections)
            
printBoard(board)
