#!/usr/bin/env python
# coding: utf-8

# In[1]:


#    Author:    Vamsi Varanasi
#    Date:      08-APRIL-2020

#importing stuff we need
from random import randint
from termcolor import colored
from colorama import init

#global options
VERBOSE = False                    #Set to true to get logs of internal working to stdout
COMPUTER_NAME = "Mr. Komputer"     #Set to whatever name you want the computer to be called by
MARKUP = True                      #Markup = True for coloured output, False for plain output


# In[2]:


def clear_output():
    print("\n"*50)


# In[3]:


def display_board(board,markdown=False):

    if not markdown:    
        print(" "*3+board[0]+" | "+board[1]+" | "+board[2])
        print(" "*3+"-"*9)
        print(" "*3+board[3]+" | "+board[4]+" | "+board[5])
        print(" "*3+"-"*9)
        print(" "*3+board[6]+" | "+board[7]+" | "+board[8])
    
    else:
        convertedBoard = ["" for i in range(9)]
        for position in range(9):
            if board[position]==" ":
                convertedBoard[position]=colored(str(position),'white')
            elif board[position]=="X":
                convertedBoard[position]=colored(board[position],'red')
            elif board[position]=="O":
                convertedBoard[position]=colored(board[position],'cyan')
            
        coloredSeparator=colored(" | ",'white')
        
        print(" "*3+convertedBoard[0]+coloredSeparator+convertedBoard[1]+coloredSeparator+convertedBoard[2])
        print(colored(" "*3+"-"*9,'white'))
        print(" "*3+convertedBoard[3]+coloredSeparator+convertedBoard[4]+coloredSeparator+convertedBoard[5])
        print(colored(" "*3+"-"*9,'white'))
        print(" "*3+convertedBoard[6]+coloredSeparator+convertedBoard[7]+coloredSeparator+convertedBoard[8])
    
    return 0


# In[4]:


def place_marker(board, marker, position):
    board[position]=marker
    return 0


# In[5]:


def win_check(board):
    for i in range(0,7,3):
        if board[i]==board[i+1]==board[i+2]:
            return board[i]
    
    for i in range(0,3):
        if board[i]==board[i+3]==board[i+6]:
            return board[i]
    
    if board[0]==board[4]==board[8]:
        return board[4]
    if board[2]==board[4]==board[6]:
        return board[4]
    
    return "NoWin"


# In[6]:


def space_check(board, position):
    return board[position] != "X" and board[position] != "O"


# In[7]:


def full_board_check(board):
    return not " " in board


# In[8]:


def player_action(board,marker,playerName,verbose=False):
    filledSpacePicked = False
    
    print("To pick a position, enter the position number from the positions shown below:\n")
    display_board(board,True)
    
    while True:
        if filledSpacePicked:
            filledSpacePicked = False
            position = int(input(playerName+", that spot is already taken. Please pick a new position\n"))
        else:
            position = int(input(playerName+", please pick a position\n"))

        if board[position] != "X" and board[position] != "O":
            place_marker(board,marker,position)
            return True
        else:
            filledSpacePicked = True


# In[9]:


def computer_action_meta_v1(localBoard,localMarker,verbose=False):
    '''
    Evaluates a given tic tac toe board for opportunities
    
    Inputs:
    localBoard = a list of string values representing the tic tac toe board
    localMarker = marker for which opportunities should be evaluated, i.e. where is the best place to put this marker?
    Use verbose = pass True to get internal actions logged to std out via print() commands
    
    Return:
    Returns a positive integer where there is an opportunity to place the localMarker, if an opportunity is found
    Returns -1 if no opportunity is found
    '''
    
    #default value of position is -1 which indicates no opportunity found
    position = -1
    
    #checking rows first
    for i in range(0,7,3):
        #consider only rows that have space
        if localBoard[i]==" " or localBoard[i+1]==" " or localBoard[i+2]==" ":
            #score the row, higher the score, higher the opportunity
            score = int(localBoard[i]==localMarker)+int(localBoard[i+1]==localMarker)+int(localBoard[i+2]==localMarker)
            if verbose:
                print("For row of "+str(i)+" score is "+str(score))
            #if the player is on the verge of winning, pick that position
            if score > 1:
                position = localBoard[i:i+3].index(' ') + i
                if verbose:
                    print("Opportunity to put marker in "+str(position))
                return position
                
    #checking columns
    for i in range(0,3):
        #consider only columns that have space
        if localBoard[i]=="" or localBoard[i+3]==" " or localBoard[i+6]==" ":
            #score the column, higher the score, higher the opportunity
            score = int(localBoard[i]==localMarker)+int(localBoard[i+3]==localMarker)+int(localBoard[i+6]==localMarker)
            if verbose:
                print("For column of "+str(i)+" score is "+str(score))
            #if the player is on the verge of winning, pick that position
            if score > 1:
                if localBoard[i]==" ":
                    position = i
                elif localBoard[i+3]==" ":
                    position = i+3
                else:
                    position = i+6
                if verbose:
                    print("Opportunity to put marker in "+str(position))
                return position
                
    
    #checking diagonals similarly
    #diagonal 1
    if localBoard[0]==" " or localBoard[4]==" " or localBoard[8]==" ":
        score = int(localBoard[0]==localMarker)+int(localBoard[4]==localMarker)+int(localBoard[8]==localMarker)
        if verbose:
                print("For D1(0-4-8) of "+str(i)+" score is "+str(score))
        if score > 1:
            if localBoard[0]==" ":
                position = 0
            elif localBoard[4]==" ":
                position = 4
            else:
                position = 8
            if verbose:
                print("Opportunity to put marker in "+str(position))
            return position
        
    
    #diagonal 2
    if localBoard[2]==" " or localBoard[4]==" " or localBoard[6]==" ":
        score = int(localBoard[2]==localMarker)+int(localBoard[4]==localMarker)+int(localBoard[6]==localMarker)
        if verbose:
                print("For D2(2-4-6) of "+str(i)+" score is "+str(score))
        if score > 1:
            if localBoard[2]==" ":
                position = 2
            elif localBoard[4]==" ":
                position = 4
            else:
                position = 6
            if verbose:
                print("Opportunity to put marker in "+str(position))
            return position
    
    #send a negative number if nothing works
    if verbose:
        print("No opportunity found")
    return position


# In[10]:


def computer_action_v3(board,ownMarker,opponentMarker,playerName="Computer",verbose=False):
    #Get the center cell if possible
    if board[4]==" ":
        #Center is empty, put marker in 4
        if verbose:
            print("Found the center cell to be empty placing the marker in 4")
        place_marker(board,ownMarker,4)
        return True
    
    #Block opponent's markers first
    if verbose:
        print("Evaluating opponent's markers:")
    position = computer_action_meta_v1(board,opponentMarker,verbose)
    if position >= 0:
        if verbose:
            print("Found opponent opportunity in position "+str(position)+" blocking it")
        place_marker(board,ownMarker,position)
        return True
    else:
        if verbose:
            print("No opportunity found for opponent")
    
    if verbose:
        print("\nEvaluating OWN markers:")
    #If the opponent doesn't have an opportunity, pick a line with higher number of own markers
    position = computer_action_meta_v1(board,ownMarker,verbose)
    if position >= 0:
        if verbose:
            print("Found OWN opportunity in position "+str(position)+" taking it")
        place_marker(board,ownMarker,position)
        return True
    else:
        if verbose:
            print("No opportunity found for OWN")
    
    #If all else fails pick a random empty cell
    #make sure there is an empty spot on the board
    if full_board_check(board):
        #board is full
        if verbose:
            print("\nBoard is full")
        return False
    else:
        position = randint(0,8)
        while not space_check(board,position):
            position = randint(0,8)
        if verbose:
            print("\nLast resort - picking random cell at "+str(position))
        place_marker(board,ownMarker,position)
        return True
    
    return False #just to be safe


# In[11]:


def tic_tac_toe():
    runLoop = True
    gameInProgress = True
    playBoard = [" " for i in range(9)]
    player1Turn = True
    filledSpacePicked = False
    
    player1Name = "Player 1"
    player1Name = "Player 2"

    while runLoop:
        mode = ""
        while mode.lower() != "p" and mode.lower()!= "c":
            if not VERBOSE:
                clear_output()
            print('Welcome to Tic Tac Toe!\n')
            mode = input('Type P for playing against another player and C to play against computer\n')

        if mode.lower() == "p":
            player1Name = input('Enter name for player 1: ')
            player2Name = input('Enter name for player 2: ')
            
            print("Coin toss will decide who plays first.")
            coinToss = ""
            while coinToss.lower()!="h" and coinToss.lower()!="t":
                coinToss = input(player1Name+", type H to pick heads and T to pick tails: ")
            temp = randint(0,1)
            if temp==0:
                player1Turn = coinToss.lower() == 'h'
            else:
                player1Turn = coinToss.lower() == 't'
                
            if player1Turn:
                print(player1Name+" wins the toss\n")
            else:
                print(player2Name+" wins the toss\n")
                
            input("Press any key to continue. ")
            
            while gameInProgress:
                if player1Turn:
                    if not VERBOSE:
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+player2Name+":O\n")
                    player_action(playBoard,"X",player1Name)
                    if win_check(playBoard)=="X":
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+player2Name+":O\n")
                        display_board(playBoard,True)
                        print(player1Name+" wins!\n")
                        gameInProgress = False
                        runLoop = False
                    if full_board_check(playBoard):
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+player2Name+":O\n")
                        display_board(playBoard,True)
                        print("Board is full. No one wins.\n")
                        gameInProgress = False
                        runLoop = False
                    player1Turn = False

                else:
                    if not VERBOSE:
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+player2Name+":O\n")
                    player_action(playBoard,"O",player2Name)
                    if win_check(playBoard)=="O":
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+player2Name+":O\n")
                        display_board(playBoard,True)
                        print(player2Name+" wins!\n")
                        gameInProgress = False
                        runLoop = False
                    if full_board_check(playBoard):
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+player2Name+":O\n")
                        display_board(playBoard,True)
                        print("Board is full. No one wins.\n")
                        gameInProgress = False
                        runLoop = False
                    player1Turn = True

        elif mode.lower() == "c":
            player1Name = input('Enter your name: ')
            print("Coin toss will decide who plays first.")
            coinToss = ""
            while coinToss.lower()!="h" and coinToss.lower()!="t":
                coinToss = input("Type H to pick heads and T to pick tails: ")
            temp = randint(0,1)
            if temp==0:
                player1Turn = coinToss.lower() == 'h'
            else:
                player1Turn = coinToss.lower() == 't'
                
            if player1Turn:
                print(player1Name+" wins the toss\n")
            else:
                print(COMPUTER_NAME+" wins the toss\n")
                
            input("Press any key to continue. ")
                
            while gameInProgress:
                if player1Turn:
                    if not VERBOSE:
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print(COMPUTER_NAME+' accepts your challenge!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+COMPUTER_NAME+":O\n")
                    player_action(playBoard,"X",player1Name)
                    if win_check(playBoard)=="X":
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print(COMPUTER_NAME+' accepts your challenge!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+COMPUTER_NAME+":O\n")
                        display_board(playBoard,True)
                        print(player1Name+" wins... "+COMPUTER_NAME+" will have his revenge!\n")
                        gameInProgress = False
                        runLoop = False
                    if full_board_check(playBoard):
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print(COMPUTER_NAME+' accepts your challenge!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+COMPUTER_NAME+":O\n")
                        display_board(playBoard,True)
                        print("Board is full. No one wins. "+COMPUTER_NAME+" will fight you another day!\n")
                        gameInProgress = False
                        runLoop = False
                    player1Turn = False
                else:
                    if not VERBOSE:
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print(COMPUTER_NAME+' accepts your challenge!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+COMPUTER_NAME+":O\n")
                    computer_action_v3(playBoard,"O","X",COMPUTER_NAME,VERBOSE)
                    if win_check(playBoard)=="O":
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print(COMPUTER_NAME+' accepts your challenge!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+COMPUTER_NAME+":O\n")
                        display_board(playBoard,True)
                        print(COMPUTER_NAME+" wins! Next, on to world domination!!\n")
                        gameInProgress = False
                        runLoop = False
                    if full_board_check(playBoard):
                        clear_output()
                        print('Welcome to Tic Tac Toe!\n')
                        print(COMPUTER_NAME+' accepts your challenge!\n')
                        print("Marker for "+player1Name+": X\tMarker for "+COMPUTER_NAME+":O\n")
                        display_board(playBoard,True)
                        print("Board is full. No one wins. "+COMPUTER_NAME+" will fight you another day!\n")
                        gameInProgress = False
                        runLoop = False
                    player1Turn = True
        else:
            runLoop=False

    else:
        print("\nThank you for playing!")


# In[12]:
if __name__ == "__main__"
    init()
    tic_tac_toe()
