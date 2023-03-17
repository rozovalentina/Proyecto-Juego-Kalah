import sys
import copy

class Node:
    def __init__(self, heuristic, table, next, holeMoved):
        self.heuristic = heuristic
        self.table = table
        self.next = next
        self.holeMoved = holeMoved


def startTable():
    table = [[4 for i in range(6)] for j in range(2)]
    return table

def clearMemory(table):
    for i in range(2):
        del table[i]
    del table

def clearTable(table):
    for i in range(2):
        for j in range(6):
            table[i][j] = 0

def printTable(table, southPoints, northPoints):
    print("\t\tNorth AI Points====>", northPoints)
    for i in range(-1, 2):
        for j in range(6):
            if i == -1:
                print("\033[0;31;40m", "\t", j, "\033[0;0;40m", end="")
            else:
                print("\t", table[i][j], end="")
        print("")
    print("\t\tSouth Player Points====>", southPoints)
  
def movement(table, isAI, hole, points):
    anotherMove = False
    ballsLeft = table[1][hole]
    limit = 5
    startIn = hole + 1
    lastMoveHole = [-1, -1]
    
    if isAI:
        limit = 0
        ballsLeft = table[0][hole]
        table[0][hole] = 0
        startIn = hole - 1
    else:
        table[1][hole] = 0
        
    while ballsLeft > 0:
        if isAI:
            if limit == 5:
                for i in range(limit+1):
                    if ballsLeft > 0:
                        table[1][i] += 1
                        ballsLeft -= 1
                lastMoveHole = [-1, -1]
                limit = 0
            else:
                for i in range(startIn, limit-1, -1):
                    if ballsLeft > 0:
                        table[0][i] += 1
                        ballsLeft -= 1
                        lastMoveHole = [0, i]
                if ballsLeft > 0:
                    points += 1
                    if ballsLeft == 1 and lastMoveHole[1] == 0:
                        anotherMove = True
                    ballsLeft -= 1
                limit = 5
                startIn = 5
        else:
            if limit == 5:
                for i in range(startIn, limit+1):
                    if ballsLeft > 0:
                        table[1][i] += 1
                        ballsLeft -= 1
                        lastMoveHole = [1, i]
                if ballsLeft > 0:
                    points += 1
                    if ballsLeft == 1 and lastMoveHole[1] == 5:
                        anotherMove = True
                    ballsLeft -= 1
                limit = 0
                startIn = 0
            else:
                for i in range(5, limit-1, -1):
                    if ballsLeft > 0:
                        table[0][i] += 1
                        ballsLeft -= 1
                lastMoveHole = [-1, -1]
                limit = 5
                
    if lastMoveHole[0] != -1 and lastMoveHole[1] != -1 and table[lastMoveHole[0]][lastMoveHole[1]] == 1:
        if lastMoveHole[0] == 0:
            points += table[lastMoveHole[0]][lastMoveHole[1]] + table[1][lastMoveHole[1]]
            table[lastMoveHole[0]][lastMoveHole[1]] = 0
            table[1][lastMoveHole[1]] = 0
        else:
            points += table[lastMoveHole[0]][lastMoveHole[1]] + table[0][lastMoveHole[1]]
            table[lastMoveHole[0]][lastMoveHole[1]] = 0
            table[0][lastMoveHole[1]] = 0
    
    #it returns if the player has another movement
    return anotherMove
def checkTable(table, pointsIa, pointsPlayer):
    iaHasMovements = False
    playerHasMovements = False
    keepPlaying = False
    iaSidePoints = 0
    playerSidePoints = 0
    
    for i in range(6):
        if table[0][i] != 0:
            iaSidePoints += table[0][i]
            iaHasMovements = True
        if table[1][i] != 0:
            playerSidePoints += table[1][i]
            playerHasMovements = True
    
    if iaHasMovements and playerHasMovements:
        keepPlaying = True
    else:
        if iaHasMovements:
            pointsIa += iaSidePoints
        if playerHasMovements:
            pointsPlayer += playerSidePoints
    
    return keepPlaying

def clearTable(table):
    for i in range(6):
        table[0][i] = 0
        table[1][i] = 0

# I will count the number of movement that the adversary has at that instant
# and the number of movements that the actual player can give to the adversary
def heuristicTable(table, ai):
    movements = 0
    giveMovement = False
    oneMoveMore = False
    if ai:
        for i in range(6):
            # adversary movement
            if table[1][i] != 0:
                movements += 1
            # last movement get one more movement
            if table[1][i] - (5 - i) == 1:
                oneMoveMore = True
            # ai can give a move
            if table[0][i] - (i + 1) > 0:
                giveMovement = True
    else:
        for i in range(6):
            # AI Movements
            if table[0][i] != 0:
                movements += 1
            # last movement get one more movement
            if table[0][i] - i == 1:
                oneMoveMore = True
            # player can give a move
            if table[1][i] - (i + 1) > 0:
                giveMovement = True
    if giveMovement:
        movements += 1
    if oneMoveMore:
        movements += 1
    return movements

def copyTable(table):
    newTable = [[0]*6 for i in range(2)]
    for i in range(2):
        for j in range(6):
            newTable[i][j] = table[i][j]
    return newTable

def createTree(table):
    print("IA Jugando")
    root = Node(table)
    points = 0
    minimum = sys.maxsize
    maximum = -sys.maxsize
    holeSelected = None

    # creating possible movements of the AI
    for i in range(6):
        nextMoveTable = copy.deepcopy(table)
        movement(nextMoveTable, False, i, points)
        son = Node(nextMoveTable, holeMoved=i)
        root.next.append(son)

    # creating possible movements for the player
    for son in root.next:
        son.next = []
        for j in range(6):
            nextMoveTable = copy.deepcopy(son.table)
            movement(nextMoveTable, True, j, points)
            grandSon = Node(nextMoveTable, holeMoved=j)
            grandSon.heuristic = heuristicTable(grandSon.table, True)
            son.next.append(grandSon)

    # give heuristic to the son
    for son in root.next:
        for grandSon in son.next:
            if grandSon.heuristic < minimum:
                minimum = grandSon.heuristic
        son.heuristic = minimum
        minimum = sys.maxsize

    # give heuristic to the decision to take
    while True:
        for son in root.next:
            if son.heuristic > maximum:
                maximum = son.heuristic
                holeSelected = son.holeMoved
        root.heuristic = maximum
        if table[0][holeSelected] == 0:
            root.next[holeSelected].heuristic = 0
            maximum = -sys.maxsize
        else:
            break

    return holeSelected

if __name__ == '__main__':
    main()
