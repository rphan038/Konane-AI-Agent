import random

class Node:
    def __init__(self, color, board, move = None):
        self.color = color
        self.board = self.copyListofLists(board)
        self.children = [] #holds the child nodes of this node
        self.move = move #the move that got us to this node??

    def copyListofLists(self, oldList):
        copy = []
        for item in oldList:
            copy.append(list(item))
        return copy

class Tree:
    def __init__(self, color, gameBoard):
        self.gameBoard = gameBoard# the gameBoard object we will use to access its class functions
        self.root = Node(color, gameBoard.board) #the root node of the tree
    
    def initialize(self, gameBoard, color, itr):#this function adds more layers to the tree
        parents = [self.root] #an array containing all the parent nodes we are exploring
        children = [] #an array containing all the child nodes we will explore
        depth = 0 #keeps track of the number of plys compted
        allChildren = []

        while (len(parents) > 0 and depth < itr):
            node = parents.pop(0)# gets the first node in the list
            children.extend(self.getChildren(node, 3)) #get the child nodes of the node and add them to children[]
            if (len(parents) == 0):
                parents = children #look at the next level of nodes
                allChildren = allChildren + children
                children = []
                depth += 1
        return allChildren
        
    def getChildren(self, node, itr): #gets all the child nodes of a given node
        if itr == 0:
            return []
        legalMoves = self.gameBoard.findLegalMoves(node.board, node.color)#all the legal moves the player can make at that instant
        childColor = "White" #the color of the child nodes of this node

        if node.color == "White":
            childColor = "Black"
            
        for move in legalMoves: #for every possible move by the player create a new child node
            node.children.append(Node(childColor, self.gameBoard.movePiece(node.board, move[0], move[1]), move))

        return node.children