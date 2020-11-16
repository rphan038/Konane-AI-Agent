import random
from algorithm import Algorithm
#Encapsulated everything into a class so that all of the methods can be referred to in other files
class GameBoard:
    def __init__(self):
        self.board = [ #this is our game board
            ['', '', '', '', '', '', '', '', ''],
            ['','B','W','B','W','B','W','B','W'],
            ['','W','B','W','B','W','B','W','B'],
            ['','B','W','B','W','B','W','B','W'],
            ['','W','B','W','B','W','B','W','B'],
            ['','B','W','B','W','B','W','B','W'],
            ['','W','B','W','B','W','B','W','B'],
            ['','B','W','B','W','B','W','B','W'],
            ['','W','B','W','B','W','B','W','B']
            ]
        self.firstMove = True #keeps track of whether we are on one of the first two moves of the game
        self.whiteFirstmove = [] #keeps track of all possible first moves for the white player 
        self.alg = Algorithm(self)

    def draw(self, board): #this function draws the game on the screen
        for i in range(1 , 9):
            print (board [i][1:9])

    def movePiece(self, Gboard, start, end): #this function moves a piece on the self.
        #gets two tuples start(x1,y1) and end (x2,y2) for where the piece starts and ends its move
        board = []#this will hold a copy of our gameboard
        for x in Gboard:#copy gboard so we don't alter the original
            board.append(list(x))
        piece = board[start[0]][start[1]] #get the piece
        
        if end == 0:#this is how you remove a piece directly, set end = 0
            board[start[0]][start[1]] = ' ' #remove the piece from the start location
            return board
        elif (start[0] != end[0]): #if the movment was vertical
            if end[0] > start[0]:
                for c in range (start[0], end[0] + 1):#remove all pieces in between the start and end location
                    board[c][end[1]] = ' '
            elif end[0] < start[0]:
                for c in range (start[0], end[0] - 1, -1):#remove all pieces in between the start and end location
                    board[c][end[1]] = ' '
        elif (start[1] != end[1]): #if the movment was horizontal
            if end[1] > start[1]:
                for c in range (start[1],end[1] + 1):#remove all pieces in between the start and end location
                    board[end[0]][c] = ' '
            elif end[1] < start[1]:
                for c in range (start[1],end[1] - 1, -1):#remove all pieces in between the start and end location
                    board[end[0]][c] = ' '
                
        board[end[0]][end[1]] = piece #place the piece at the end location
        return board

    #This method goes through every single location on the board and depending on who's turn it is, checks to see if there are valid moves
    def findLegalMoves(self, board, playerColor):
        moveSet = [] #List of two pairs of locations [[(start1X, start1Y), (end1X, end1Y)], [(start2X, start2Y), (end2X, end2Y)]]
        player = "B" #the color of the currernt player
        other = "W" #the color of the other player
        if playerColor == "White": #if the current player is white
            player = "W"
            other = "B"

        for i in range(1, 9):
            for k in range(1,9):
                if (board[i][k] != player):continue# if the particular piece we are looking at is not the same color as the current player, we go to the next piece
                #check up
                a = i# a variable we will use for the inner loops so we dont interfere with the outer loop
                while (a > 1 and board [a-1][k] == other and board [a-2][k] == ' '):
                    moveSet.append([(i,k),(a-2,k)])
                    a = a-2
                #check down
                a = i
                while (a < 7 and board [a+1][k] == other and board [a+2][k] == ' '):
                    moveSet.append([(i,k),(a+2,k)])
                    a = a + 2    
                #check left
                a = k
                while (a > 1 and board [i][a-1] == other and board [i][a-2] == ' '):
                    moveSet.append([(i,k),(i,a-2)])
                    a = a-2
                #check right
                a = k
                while (a < 7 and board [i][a+1] == other and board [i][a+2] == ' '):
                    moveSet.append([(i,k),(i,a+2)])
                    a = a + 2            
        return moveSet

    # Finds the utility of a board. The utility we defined is the number of legal moves a player has
    def findUtility(self, board, player):
        numOfMoves = len(self.findLegalMoves(board, 'Black')) - len(self.findLegalMoves(board, 'White'))
        return numOfMoves

    # Used only during game play to make random moves
    def moveRandomly(self, moveSet):
        rand = random.randint(0, len(moveSet) - 1)
        return moveSet[rand]

    def verify(self, board, stringMove, turn):#helps format and verify user input
        #first convert the move from a string
        start = stringMove.split()[0]#the string of the start location f the move
        end = stringMove.split()[1]#the string of the end location f the move
        start = (int(start.split(",")[0]),int(start.split(",")[1]))#set the start of the move in the correct format
        if len(end.split(",")) != 2:#if there is only one entry in the end
            end = int (end)
        else:
            end = (int(end.split(",")[0]),int(end.split(",")[1]))
        move = [start,end] #forms our formatted move
        
        if self.firstMove:
            if turn == "White" and move in self.whiteFirstmove:#if the move is a valid first move
                self.firstMove = False #after this we have done the first two moves
                return move
            if turn == "Black" and move in [[(8,8),0],[(1,1),0],[(4,4),0],[(5,5),0]]:
                moverow, movecol = move[0][0], move[0][1]#the row and column of the piece we are removing
                if moverow < 8: self.whiteFirstmove.append([(moverow+1,movecol),0])#here we populate the list of possible first moves for white
                if moverow > 1: self.whiteFirstmove.append([(moverow-1,movecol),0])
                if movecol < 8: self.whiteFirstmove.append([(moverow,movecol+1),0])
                if movecol > 1: self.whiteFirstmove.append([(moverow,movecol-1),0])
                return move
            return None
        if move in self.findLegalMoves(self.board, turn): return move
        return None


    def run(self): #the main method of the game   

        black = None # this variable keeps track of who is playing black
        white = None # this variable keeps track of who is playing white
        turn = 'Black' #this variable keeps track of whose turn it is
        
        while black == None and white == None: #this loops until players enter a valid value and pick to play either black or white
            val = raw_input ("Enter B to play Black and W to play White: ")
            if val == 'B' or val == 'b':
                black = 'Player'    #black is the player
                white = 'AI'        #white is the ai
            elif val == 'W' or val == 'w': 
                black = 'AI'        #black is the ai
                white = 'Player'    #white is the player
            else:
                black = 'AI'
                white = 'AI'

        wf = False
        while turn != 'End': #this is the main loop of the game
            move = None # this variable keeps track of the players move
            self.draw(self.board)
            # Each iteration, find all moves a player can make
            allMoves = self.findLegalMoves(self.board, turn)
            if (not self.firstMove) : print(turn + " move set " + str(allMoves))

            if allMoves == [] and self.firstMove != True:
                if turn == 'Black':
                    print("White has won")
                else:
                    print("Black has won")
                print("The number of static evaluations: " + str(self.alg.evaluations))
                print("Average branching factor: " + str(self.alg.branchFactor / self.alg.num))
                print("The number of cuts is: " + str(self.alg.cuts))
                return
            if (turn == 'Black' and black == 'AI') or (turn == 'White' and white == 'AI'): #if it is the AI's turn
                #move = some algorithm's return.
                #Here we can just pass turn (as board is already a global variable), and get the best move for that color on that board 
                #if move cant be made, end game (turn = 'End')
                #print ('AI has moved ... ')
                if (self.firstMove):
                    if (turn == "Black"):
                        posMoves = [[(8,8),0],[(1,1),0],[(4,4),0],[(5,5),0]]#blacks possible first move
                        move = random.choice(posMoves)#pick from the possible moves
                        moverow, movecol = move[0][0], move[0][1]#the row and column of the piece we are removing
                        if moverow < 8: self.whiteFirstmove.append([(moverow+1,movecol),0])#here we populate the list of possible first moves for white
                        if moverow > 1: self.whiteFirstmove.append([(moverow-1,movecol),0])
                        if movecol < 8: self.whiteFirstmove.append([(moverow,movecol+1),0])
                        if movecol > 1: self.whiteFirstmove.append([(moverow,movecol-1),0])
                    if (turn == "White"):
                        move = random.choice(self.whiteFirstmove)
                        self.firstMove = False

                if move == None:
                    # move = self.alg.minimaxDecision(self.board, turn, 3)
                    move = self.alg.miniMaxAB(turn, 4)
                print ("AI moved " + str(move))
                self.board = self.movePiece(self.board, move[0], move[1])
                if turn == 'Black':
                    turn = 'White'
                else:
                    turn = 'Black'
            else: #if it is the humans turn
                # Computer AI plays against Computer random
                # if wf == False:
                #     if self.firstMove == True and turn == 'Black':
                #         firstBlackMove = [[(8,8),0],[(1,1),0],[(4,4),0],[(5,5),0]]
                #         move = random.choice(firstBlackMove)
                #         moverow, movecol = move[0][0], move[0][1]#the row and column of the piece we are removing
                #         if moverow < 8: self.whiteFirstmove.append([(moverow+1,movecol),0])#here we populate the list of possible first moves for white
                #         if moverow > 1: self.whiteFirstmove.append([(moverow-1,movecol),0])
                #         if movecol < 8: self.whiteFirstmove.append([(moverow,movecol+1),0])
                #         if movecol > 1: self.whiteFirstmove.append([(moverow,movecol-1),0])
                #     else:
                #         move = random.choice(self.whiteFirstmove)
                #         wf = True
                #         self.firstMove = False
                # else:
                #     move = random.choice(allMoves)

                # Tournament human playing
                if self.firstMove and turn == "Black":print(turn + " move set " + str([[(8,8),0],[(1,1),0],[(4,4),0],[(5,5),0]])) #print the possible moves
                elif self.firstMove and turn == "White":print(turn + " move set " + str(self.whiteFirstmove))#print the possible moves
                while move == None:
                    move = raw_input ("Enter a valid move: ") #use format x1,y1 x2,y2 or x1,y1 0
                    move = self.verify(self.board, move, turn)

                print(turn + " Move " + str(move))
                self.board = self.movePiece(self.board, move[0], move[1])
                if turn == 'Black':
                    turn = 'White'
                else:
                    turn = 'Black'
                
    # Getter method for the game board
    def getGameboard(self):
        return self.board

        
gb = GameBoard()
gb.run()
