# imports
from typing import List, Tuple, Union
from random import randint
ctn = 1
ptn = 1
plays = []
# create a function to print the board
def print_board(l: List[List[str]]) -> None:
    for i in range(len(l)):
        for c in range(len(l[i])):
            print(l[i][c] + ' | ', end='')
        print("\n-----------")


# create a function to update the board
# given a board, a position and player, put the
# player's coin in the board, in the given position
def update_board(board: List, pos: Tuple, player: str) -> int:

    # if position is already taken, then print and return.
    if board[pos[0]][pos[1]] != ' ':
        print("Invalid move!")
        return False
    
    board[pos[0]][pos[1]] = player
    return True


def three_in_a_row(board: List, player = str) -> Union[Tuple, None]:
    mtlist = []
    mtlist1 = []
    mtlist2 = []
    diagonal1 = [board[0][0],board[1][1],board[2][2]]
    diagonal2 = [board[2][0],board[1][1],board[0][2]]
    for i in range(len(board)):
        if board[i].count(player) == 2:
            for c in range(len(board[i])):
                if board[i][c] == ' ':
                    return (i,c)

        mtlist += [board[i][0]]
        mtlist1 += [board[i][1]]
        mtlist2 += [board[i][2]]
    if mtlist.count(player) == 2:
        for i in range(len(mtlist)):
            if mtlist[i] == ' ':
                return (i,0)
    if mtlist1.count(player) == 2:
        for i in range(len(mtlist1)):
            if mtlist1[i] == ' ':
                return (i,1)
    if mtlist2.count(player) == 2:
        for i in range(len(mtlist2)):
            if mtlist2[i] == ' ':
                return (i,2)
    if diagonal1.count(player) == 2:
        for i in range(len(diagonal1)):
            if diagonal1[i] == ' ':
                return (i,i)
    if diagonal2.count(player) == 2:
        for i in range(len(diagonal2)):
            if diagonal2[i] == ' ':
                return (2-i,i)
    return None



# check if game over
def is_game_over(board: List[List[str]]) -> None:
    
    # check if there are 3 in a row anywhere
    for i in range(len(board)):
        if board[i].count('X') == 3:
            print("Player X won")
            return True
        if board[i].count('O') == 3:
            print("Player O won")
            return True
    
    # check if there are 3 in a coloumn anywhere
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:

            # make sure that spaces don't count
            if board[0][i] != ' ':
                print('Player',board[0][i],"won")
                return True
    
    # make sure that spaces don't count
    if board[1][1] != ' ':

        # check for diagonals
        if board[2][0] == board[1][1] == board[0][2]:
            print("Player",board[1][1],"won")
            return True
        if board[0][0] == board[1][1] == board[2][2]:
            print("Player",board[1][1],"won")
            return True
    
    # check to see if board isn't full
    for row in board:
        if row.count(' ') != 0:
            return False
    
    # else it is full and a tie
    print("It's a tie!")
    return True


# function for the computer move
def computer_move(board: List, player = str, comp = str, turn = str) -> None:
    # call in the global variables
    global ctn
    global ptn
    # put all corners into a list
    corners = [(0,0),(0,2),(2,0),(2,2)]
    
    # use three in a row function but to try to win instead
    win = three_in_a_row(board = board, player = comp)
    if win != None:
        update_board(board = board, pos = win, player = comp)
        return
    # see if player needs to be blocked
    blockpos = three_in_a_row(board = board, player = player)
    # if three_in_a_row returned a required block, update with the needed position. Else, choose a random spot to fill
    if blockpos != None:
        update_board(board = board, pos = blockpos, player = comp)
        return
    # try to use a strategy
    # create a temporary list of playermoves to bounce off of
    playermove = [(2,0),(1,0),(2,1)]
    playermove1 = [(2,2)]
    playermove2 = [(0,1),(0,2),(1,2)]
    playermove3 = [(1,1)]

    # if the player plays around the oppisite available spots, there are two possible moves
    oppspot = [(0,2),(2,0)]
    # create a variable that that will later check if it is the first try or not
    trycheck = 0
    
    # if the computer goes first and it is the first move, put a mark on a corner
    # First turn of the computer, and it is the first turn in the game.
    if turn == 'No':
        if ctn == 1:
            for i in range(len(board)):
                trycheck += (board[i].count(' '))
            if trycheck == 9:
                #update_board(board=board, pos = corners[randint(0,3)],player = comp)
                update_board(board = board, pos = (0,0), player = comp)
                return

        # if it isn't the first move of the game, check if the player placed in a spot that can be bounced off of
        elif ctn == 2:
            for i in range(len(board)):
                for c in range(len(board[i])):
                    if board[i][c] == player:
                        x = (i,c)
                        # if so, choose to opposite corner
                        if playermove.count(x) == 1:
                            if board[0][2] == ' ':
                                update_board(board = board, pos = (0,2), player = comp)
                                return
                        elif playermove1.count(x) == 1:
                            spot = randint(0,1) 
                            
                            # spot = 0 --> board[0][2]
                            
                            # spot = 1 --> board[2]
                            if board[oppspot[spot][0]][oppspot[spot][1]] == ' ':
                                update_board(board = board, pos = (oppspot[spot][0],oppspot[spot][1]), player = comp)
                                return
                        elif playermove2.count(x) == 1:
                            if board[2][0] == ' ':
                                update_board(board = board, pos = (2,0), player = comp)
                                return
                        elif playermove3.count(x) == 1:
                            if board[0][2] == ' ':
                                update_board(board = board, pos = (0,2), player = comp)
                                return
        elif ctn == 3:
            if board[2][2] == ' ':
                update_board(board = board, pos = (2,2), player = comp)
                return
            else:
                while True:
                    spot = randint(0,1)
                    if board[oppspot[spot][0]][oppspot[spot][1]] == ' ':
                        update_board(board = board, pos = (oppspot[spot][0],oppspot[spot][1]), player = comp)
                        return
                    break
        else: 
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!")

            validinputs = []

            # add the available spots to the list
            for i in range(len(board)):
                for c in range(len(board[i])):
                    if board[i][c] == ' ':
                        validinputs += [(i,c)]
        
            # select a random valid spot for the computer
            comploc = validinputs[randint(0,len(validinputs)-1)]

            # update the board with this spot
            update_board(board,comploc,comp)
    else:
        
        # create an empty list for available spots for the computer
        validinputs = []

        # add the available spots to the list
        for i in range(len(board)):
            for c in range(len(board[i])):
                if board[i][c] == ' ':
                    validinputs += [(i,c)]
        
        # select a random valid spot for the computer
        comploc = validinputs[randint(0,len(validinputs)-1)]

        # update the board with this spot
        update_board(board,comploc,comp)


def create_board() -> List:
    l = [[' ' for _ in range(3)] for _ in range(3)]
    return l


def main():
    global ctn
    global ptn
    global plays
    sym = input("What symbol do you want (X/O)? ")
    if sym == 'X':
        compsym = 'O'
    else:
        compsym = 'X'
    board = create_board()
    
    print("------ Empty Board -------")
    print_board(l = board)
    print("----------------------------")
    turn = input("Do you want to go first? ")
    if turn == 'No':
        computer_move(board = board, player = sym, comp = compsym, turn = turn)
        print("------ Computer's move -------")
        print_board(l = board)
        print("------------------------------")
        ctn+=1
    while True:

        # player's move
        player = eval(input('Where do you want to play, enter (i, j) in python index: '))
        check = update_board(board = board, pos = player, player = sym)
        if check == False:
            raise ValueError("Invalid move")
        print("------ Player's move -------")
        print_board(l = board)
        print("----------------------------")
        ptn+=1
        if is_game_over(board = board):
            break
        
        # computer's move
        computer_move(board = board, player = sym, comp = compsym, turn = turn)
        print("------ Computer's move -------")
        print_board(l = board)
        print("------------------------------")
        ctn+=1
        if is_game_over(board = board):
            break
        
# script
if __name__ == "__main__":
    main()