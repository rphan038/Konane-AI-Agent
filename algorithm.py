import random
import sys
from tree import Tree

class Algorithm:
    def __init__(self, gameBoard):
        self.branchFactor = 0
        self.num = 0
        self.depth = 0
        self.evaluations = 0
        self.cuts = 0
        self.gb = gameBoard
        self.tree = Tree("Black", self.gb)
    
    # Selects random moves
    def randomMoves(self, moveSet):
        rand = random.randint(0, len(moveSet) - 1)
        return moveSet[rand]

    def copyListofLists(self, oldList):
        copy = []
        for item in oldList:
            copy.append(list(item))
        return copy

    # State is the current state being evaluated, turn is who's turn it is and itr is the depth at which the alg goes
    def minimaxDecision(self, state, turn, itr):
        # Using parallel array idea
        actions = []
        utilityValues = []
        t = Tree(turn, self.gb)
        t.initialize(self.gb, turn, itr + 1)
        root = t.root

        possibleMoves = self.gb.findLegalMoves(state, turn)
        self.branchFactor += len(possibleMoves)
        self.num += 1
        for i in range(len(possibleMoves)):
            a = possibleMoves[i]
            newState = self.gb.movePiece(self.copyListofLists(state), a[0], a[1])
            actions.append(a)
            if turn == 'Black':
                utilityValues.append(self.maxValue('White', root, self.copyListofLists(newState), itr - 1))
            elif turn == 'White':
                utilityValues.append(self.minValue('Black', root, self.copyListofLists(newState), itr - 1))
        if turn == 'White':
            return actions[utilityValues.index(min(utilityValues))]
        return actions[utilityValues.index(max(utilityValues))]

    def minValue(self, turn, childStates, state, itr):
        if itr == 0:
            currColor = ''
            self.evaluations += 1
            for node in childStates.children:
                if node.board == state:
                    currColor = node.color
                    break
            return self.gb.findUtility(state, currColor)
        v = sys.maxint
        possibleMoves = self.gb.findLegalMoves(state, turn)
        self.branchFactor += len(possibleMoves)
        self.num += 1
        if turn == 'Black':
            turn = 'White'
        elif turn == 'White':
            turn = 'Black'
        for i in range(len(possibleMoves)):
            a = possibleMoves[i]
            newState = self.gb.movePiece(self.copyListofLists(state), a[0], a[1])
            v = min(v, self.maxValue(turn, childStates, self.copyListofLists(newState), itr - 1))
        return v

    def maxValue(self, turn, childStates, state, itr):
        if itr == 0:
            currColor = ''
            self.evaluations += 1
            for node in childStates.children:
                if node.board == state:
                    currColor = node.color
                    break
            return self.gb.findUtility(state, currColor)
        v = (-1 * sys.maxint) + 1
        possibleMoves = self.gb.findLegalMoves(state, turn)
        self.branchFactor += len(possibleMoves)
        self.num += 1
        if turn == 'Black':
            turn = 'White'
        elif turn == 'White':
            turn = 'Black'
        for i in range(len(possibleMoves)):
            a = possibleMoves[i]
            newState = self.gb.movePiece(self.copyListofLists(state), a[0], a[1])
            v = max(v, self.minValue(turn,childStates, self.copyListofLists(newState), itr - 1))
        return v

    def miniMaxAB(self, color, itr):#performs minmax with alpha bet pruning
        t = Tree(color, self.gb) #creates the tree our algorithms will run on
        t.initialize(self.gb, color, 3)
        values = [] #stores all the evaluated values we get from our minimax algorithm
        root = t.root #the root of the tree
        self.branchFactor += len(root.children)
        self.num += 1

        if color =="Black":
            for child in root.children: values.append (self.minValueAB(child, (-1 * sys.maxint) + 1, sys.maxint, itr - 1))
            return root.children[values.index(max(values))].move
        if color == "White":
            for child in root.children: values.append (self.maxValueAB(child, (-1 * sys.maxint) + 1, sys.maxint, itr - 1))
            return root.children[values.index(min(values))].move                                                                     
    
    def maxValueAB(self, node, alpha, beta, itr):
        if len(node.children) == 0: #terminal test
            self.evaluations += 1
            return self.gb.findUtility(node.board, node.color)
        self.num += 1
        v = (-1 * sys.maxint) + 1
        for child in node.children:
            v = max(v, self.minValueAB(child, alpha, beta, itr - 1))
            if v >= beta: 
                self.cuts += len(node.children) - (node.children.index(child)+1)#add number of cuts
                self.branchFactor += node.children.index(child)+1 #add to branching factor
                return v
            alpha = max(alpha, v)
        self.branchFactor += len(node.children)
        return v

    def minValueAB(self, node, alpha, beta, itr):
        if len(node.children) == 0: #terminal test
            self.evaluations += 1
            return self.gb.findUtility(node.board, node.color)
        self.num += 1
        v = sys.maxint
        for child in node.children:
            v = min(v, self.maxValueAB(child, alpha, beta, itr - 1))
            if v <= alpha: 
                self.cuts += len(node.children) - (node.children.index(child)+1) #add number of cuts
                self.branchFactor += node.children.index(child) #add to branching factor
                return v
            beta = min(beta, v)
        self.branchFactor += len(node.children)
        return v