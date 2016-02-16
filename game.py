'''
Ricky Su
28714101
CSC242
'''

import random

# global variables
cpu = '' 
user = ''

class state():
    def __init__(self, parent, utility, terminal, board, nextTurn):
        self.parent = parent # parent state
        self.utility = utility # -1, 0, or 1, depending on the utility return
        self.terminal = terminal # boolean whether terminal state or not
        self.board = list(board) # the list representing this state
        self.nextTurn = nextTurn # 'X' or 'O' next to go on board
        self.children = [] # list of children states


def printInitial():
    # print initial board
    for index, i in enumerate([1,2,3,4,5,6,7,8,9]):
        print(str(i), end = '\n') if (index+1) % 3 == 0 \
                      else print(str(i), end = "|")
    print()

    
def printBoard(tempBoard):
    # prints given board in the tic-tac-toe format
    # replaces numbers with blanks for user
    boardWithBlanks = [" " if isinstance(x, int) else x for x in tempBoard]
    for index, i in enumerate(boardWithBlanks):
        print(str(i), end = '\n') if (index+1) % 3 == 0 \
                      else print(str(i), end = "|")
    print()


def checkTerminalUtility(board, cpu, user):
    # checks utility at terminal nodes
    # also used to check for wins
    # returns 1 if cpu win
    # returns -1 if user win
    # returns 0 if draw
    ########################################
    # horizontal wins
    for i in [0, 3, 6]:
        if board[i] == board[i+1] == board [i+2] == cpu:
            return 1
        elif board[i] == board[i+1] == board [i+2] == user:
            return -1
    # vertical wins
    for i in [0, 1, 2]:
        if board[i] == board[i+3] == board [i+6] == cpu:
            return 1
        elif board[i] == board[i+3] == board [i+6] == user:
            return -1
    # diagonal right win
    if board[0] == board[4] == board[8] == cpu:
        return 1
    if board[0] == board[4] == board[8] == user:
        return -1
    # diagonal left win
    if board[2] == board[4] == board[6] == cpu:
        return 1
    if board[2] == board[4] == board[6] == user:
        return -1
    return -2 # not terminal


def generateFrontier(tempState, turn): # parameters (a state, who's turn)
    # returns list of frontier of states
    # creates frontier by iterating through the parameter state
    # if the element found is a number, replace it with either 'X' or 'O'
    frontier = []
    tempBoard = tempState.board
    nextTurn = ""
    if turn == 'X':
        nextTurn = 'O'
    else:
        nextTurn = 'X'
    if any(isinstance(x, int) for x in tempBoard):
        # check if there is an integer on the board, otherwise skip
        for index, position in enumerate(tempBoard):
            # iterate through board
            currentBoard = list(tempBoard) # make copy of initial board
            if isinstance(position, int):
                # checks for integer values, which means blank space
                currentBoard[index] = turn # changes board with next letter
                if checkTerminalUtility(currentBoard, cpu, user) == -2:
                    # check for terminal state 
                    newState = state(tempState, 0, False, currentBoard, nextTurn)
                else:
                    # terminal state
                    utility = getUtility(currentBoard) # get utility of terminal
                    newState = state(tempState, utility, True, currentBoard, None)
                    relateUtility(newState) # bring utility from child to parent
                frontier.append(newState)
        tempState.children = frontier # add children
    return frontier


def relateUtility(tempState):
    # parameter is terminal state
    # bring utility up from terminal state by adding utility to parent utility
    if tempState.parent == None:
        return
    (tempState.parent).utility += tempState.utility
    relateUtility(tempState.parent)
    
    
def getUtility(tempBoard):
    # returns utility of given board
    global cpu, user
    utility = checkTerminalUtility(tempBoard, cpu, user)
    return utility


def do(temp):
    # must be in format [[<__main__.state object at 0x103edb128>]]
    # where the thing inside is the state containing initial board
    # generates all possibilities and combinations
    # returns a list, every element is a list of the next frontier, starting
    # with the initial state at the top
    for index, tempList in enumerate(temp):
# [[state],[state,state,state]]
        stateFrontiers = []     # list of frontiers of each state in tempList
        for tempState in tempList:
            turn = tempState.nextTurn
            if tempState.terminal == False:
                frontier = generateFrontier(tempState, turn)
                tempState.children = frontier   # add children
                temp.append(frontier)
    return temp


def create(tempBoard, nextTurn):
    # creates a state of the current board, and puts it into the format
    # that is parsed into the list of the state-space
    r = state(None, 0, False, tempBoard, nextTurn)
    e = []
    e.append(r)
    total = []
    total.append(e)
    return do(total)


def getTurnDecision(tempBoard):
    # returns cpu turn, and board
    # change board if user goes first
    # chooses global user and cpu as 'X' or 'O'
    global cpu, user
    cpuFirst = False
    print("\'X\' goes first and \'O\' goes second.")
    while True:
        decision = input("Would you like be \'X\' or \'O\'?: ")
        if decision.lower() == 'x':
            user = 'X'
            cpu = 'O'
            while True:
                space = int(input("Please enter where you would like to start."))
                if space > 0 and space < 10:
                    break;
                print("Please enter a valid answer!")
            tempBoard[space-1] = user
            break
        elif decision.lower() == 'o':
            user = 'O'
            cpu = 'X'
            cpuFirst = True
            break
        else:
            print("Please enter a valid answer!")
            continue
    return cpuFirst, tempBoard


def getCpuTurn(tempStateSpace):
    # returns new board with cpu's move
    utilities = []                      # utilities of all children
    currentState = tempStateSpace[0][0]
    for child in currentState.children: # go over children for utilities
        utilities.append(child.utility)
    m = max(utilities)                  # choose best utility from children
    indeces = [i for i, j in enumerate(utilities) if j == m]
    # indices of max utilities
    index = 0 # index of max
    if len(indeces) > 1:
        # more than one max index, choose one at random
        index = random.choice(indeces)
    else:
        index = indeces[0]
    newBoard = currentState.children[index].board # pick board from best child
    return newBoard

def getUserTurn(board):
    while True:
        try:
            place = int(input("Please input a number(1-9) \
corresponding to the board indicating where you would like to play: "))
            if place not in board:
                raise ValueError()
            break
        except ValueError:
            print("Oops! That was not a valid number. Try again...")
    return place


def full(board):
    if not any(isinstance(x, int) for x in board):
            return True
    return False


def regularTTT():
    global cpu, user
    board = [1,2,3,4,5,6,7,8,9]
    printInitial()
    cpuFirst, board = getTurnDecision(board) # ask user to go first or second
    while True:
        ###### BEGIN CPU TURN ######
        if cpuFirst: # solely for the cpu to take middle spot
            board[4] = cpu
            printBoard(board)
            cpuFirst = False
        else:
            stateSpace = create(board, cpu)             # create state space
            board = getCpuTurn(stateSpace)              # put new turn on board
            printBoard(board)                           # print board
            if checkTerminalUtility(board, cpu, user) == 1:
                print("I win!")
                print("Let's play again!")
                regularTTT()
                break
        if full(board):
            print("The game is a draw!")
            print("Let's play again!")
            regularTTT()
            break
        ###### END CPU TURN ######
        ###### BEGIN USER TURN ######
        place = getUserTurn(board)                        # get user's move
        board[place-1] = user                             # place move on board
        printBoard(board)                                 # print board
        if checkTerminalUtility(board, cpu, user) == -1:  # check win
            print("You win!")
            print("Let's play again!")
            regularTTT()
            break
        ###### END USER TURN  ######
        # check if any blank spaces left/draw
        if full(board):
            print("The game is a draw!")
            print("Let's play again!")
            regularTTT()
            break

# SEPARATE REGULAR AND SUPER TTT #
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# SEPARATE REGULAR AND SUPER TTT #
    
def printInitial9board():
    temp = [[1,2,3],[4,5,6],[7,8,9]]
    count = 0
    for l in range(3):
        for k in range(3):
            for i in range(3):
                for j in temp[count]:
                    print(j, end = '|') if j % 3 != 0 else print(j, end = '')
                print("\t", end = '')
            print()
            count += 1
        print()
        count = 0

        
def print9board(boards):
    count3 = 0
    for l in range(3):
        count = 0
        count2 = 0
        for k in range(3):
            for i in range(3):
                for j in range(3): # 1123
                    if (j+1) % 3 == 0:
                        if isinstance(boards[i + (count3 * 3)]\
                                      [j + (count2 * 3)], int):
                            print(' ', end = '')
                        else:
                            print(boards[i + (count3 * 3)][j + (count2 * 3)], \
                              end = '')
                    else:
                        if isinstance(boards[i + (count3 * 3)]\
                                      [j + (count2 * 3)], int):
                            print(' ', end = '|')
                        else:
                            print(boards[i + (count3 * 3)][j + (count2 * 3)], \
                              end = '|')
                count += 1
                print("\t", end = '')
                if count % 3 == 0:
                    print()
                    count = 0
                    count2 += 1 # second line
        print()
        count3 += 1

def generateBoards9():
    board1 = [1,2,3,4,5,6,7,8,9]
    board2 = [1,2,3,4,5,6,7,8,9]
    board3 = [1,2,3,4,5,6,7,8,9]
    board4 = [1,2,3,4,5,6,7,8,9]
    board5 = [1,2,3,4,5,6,7,8,9]
    board6 = [1,2,3,4,5,6,7,8,9]
    board7 = [1,2,3,4,5,6,7,8,9]
    board8 = [1,2,3,4,5,6,7,8,9]
    board9 = [1,2,3,4,5,6,7,8,9]

    boards = []
    boards.append(board1)
    boards.append(board2)
    boards.append(board3)
    boards.append(board4)
    boards.append(board5)
    boards.append(board6)
    boards.append(board7)
    boards.append(board8)
    boards.append(board9)

    return boards


def boardDecision9():
    while True:
        try:
            changedIndex = int(input("Please enter which board \
you would like to play on (1-9): "))
            if changedIndex < 1 or changedIndex > 9:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid answer!")
    while True:
        try:
            space = int(input("Please enter where you would \
like to play on that board (1-9): "))
            if space < 1 or space > 9:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid answer!")
    return changedIndex, space


def getTurnDecision9(tempBoards):
    # returns cpu turn, and board
    # change board if user goes first
    # chooses global user and cpu as 'X' or 'O'
    global cpu, user
    changedIndex = space = 0
    print("\'X\' goes first and \'O\' goes second.")
    while True:
        decision = input("Would you like to be \'X\' or \'O\'?: ")
        if decision.lower() == 'x':
            user = 'X'
            cpu = 'O'
            # user picks board and position
            changedIndex, space = boardDecision9()
            tempBoards[changedIndex - 1][space-1] = user
            break
        elif decision.lower() == 'o':
            user = 'O'
            cpu = 'X'
            break
        else:
            print("Please enter a valid answer!")
            continue
    return changedIndex, tempBoards


def getCpuTurn9(tempStateSpace):
    # returns new board with cpu's move
    utilities = []                      # utilities of all children
    currentState = tempStateSpace[0][0]
    for child in currentState.children: # go over children for utilities
        utilities.append(child.utility)
    m = max(utilities)                  # choose best utility from children
    indeces = [i for i, j in enumerate(utilities) if j == m]
    # indices of max utilities
    index = 0 # index of max
    if len(indeces) > 1:
        # more than one max index, choose one at random
        index = random.choice(indeces)
    else:
        index = indeces[0]
    newBoard = currentState.children[index].board # pick board from best child
    ### find the index that was changed ###
    changedIndex = 0
    for index in range(9):
        if currentState.board[index] != newBoard[index]:
            changedIndex = index
            break
    return changedIndex + 1, newBoard


def getCpuTurnUtility9(tempStateSpace):
    # returns new board with cpu's move and max utility
    utilities = []                      # utilities of all children
    currentState = tempStateSpace[0][0]
    for child in currentState.children: # go over children for utilities
        utilities.append(child.utility)
    m = max(utilities)                  # choose best utility from children
    indeces = [i for i, j in enumerate(utilities) if j == m]
    # indices of max utilities
    index = 0 # index of max
    if len(indeces) > 1:
        # more than one max index, choose one at random
        index = random.choice(indeces)
    else:
        index = indeces[0]
    newBoard = currentState.children[index].board # pick board from best child
    ### find the index that was changed ###
    changedIndex = 0
    for index in range(9):
        if currentState.board[index] != newBoard[index]:
            changedIndex = index
            break
    return m, changedIndex + 1, newBoard


def getUserTurn9(board, index):
    print("You can play on board #%d" % index)
    printBoard(board)
    while True:
        try:
            place = int(input("Please input a number(1-9) \
corresponding to the board indicating where you would like to play: "))
            if place not in board:
                raise ValueError()
            break
        except ValueError:
            print("Oops! That was not a valid number. Try again...")
    return place


def cpuMoveFull(boards):
    # full board, rechoose board and position
    # do statespace for each board and find the best utility
    # out of all boards
    utilities = []
    statespaces = []
    changedIndeces = []
    for board in boards:
        statespace = create(board, cpu)
        utility, changedIndex, newBoard = getCpuTurnUtility9(statespace)
        utilities.append(utility)
        statespaces.append(statespace)
        changedIndeces.append(changedindex)
    m = max(utilities)
    indeces = [i for i, j in enumerate(utilities) if j == m]
    # indices of max utilities
    index = 0 # index of max
    if len(indeces) > 1:
        # more than one max index, choose one at random
        index = random.choice(indeces)
    else:
        index = indeces[0]
    return index, changedIndex, newBoard


def empty(board):
    if board == [1,2,3,4,5,6,7,8,9]:
        return True
    return False

def superTTT():
    global cpu, user
    boards = generateBoards9() # generate all 9 boards
 #   printInitial9board()
    changedIndex, boards = getTurnDecision9(boards)
    # ask user to go first or second, and get which board moved at
    while True:
        if changedIndex == 0: # cpu goes first
            boards[4][4] = cpu
            changedIndex = 5
            print("I played on board 5 at position 5")
            # default first move, take middle spot on middle board
        else: # user went first
            if full(boards[changedIndex-1]):
                # when the board is full, do statespace on all boards and pick
                # the best one
                index, changedIndex, newBoard = cpuMoveFull 
                boards[index] = newBoard
                print("I played on board %d at position %d" % (index, changedIndex))
                changedindex = index
            elif empty(boards[changedIndex-1]):
                # board is empty, pick the middle spot to save time
                boards[changedIndex-1][4] = cpu
                print("I played on board %d at position 5" % changedIndex)
                changedIndex = 5
            else:
                stateSpace = create(boards[changedIndex-1], cpu) # create statespace
                newIndex, newBoard = getCpuTurn9(stateSpace)
                print("I played on board %d at position %d" % (changedIndex, newIndex))
                # get the space that was changed, and new board  
                boards[changedIndex-1] = newBoard # change board
                changedIndex = newIndex
        print9board(boards)                           # print board
        if checkTerminalUtility(boards[changedIndex-1], cpu, user) == 1:
            # check win
            print("I win!")
            print("Let's play again!")
            superTTT()
            break
        ###### END CPU TURN ######
        ###### BEGIN USER TURN ######
        if full(boards[changedIndex-1]):
            # board is full
            changedIndex, space = boardDecision9()
            boards[changedIndex-1][space-1] = user
        else:
            place = getUserTurn9(boards[changedIndex-1], changedIndex)
            # get user's move
            boards[changedIndex-1][place-1] = user
            # place move on board
        if checkTerminalUtility(boards[changedIndex-1], cpu, user) == -1:
            # check win
            printBoard(boards[changedIndex-1])
            print("You win!")
            print("Let's play again!")
            superTTT()
            break
        ###### END USER TURN  ######
        changedIndex = place


print("Would you like to play regular or super tic-tac-toe?")
while True:
    choice = input("Please enter \'r\' for regular or \'s\' for super: ")
    if not choice.lower() == 'r' and not choice.lower() == 's':
        print("Please enter a valid option")
        continue
    if choice == 'r':
        regularTTT()
    else:
        superTTT()
