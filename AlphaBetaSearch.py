from enum import Enum
import math
'''
Miguel Zavala
4/13/20
CISC481-Intro To AI
Dr.Rahmat
Homework 2: Alpha-Beta Search

Alpha-Beta Search: It is simply an improved Minimax algorithm where it prunes unwanted subtrees/leaves in order
to improve search time

Description
In this programming homework, you will work on the same alpha-beta search problem that we
have solved in the class. There was also a youtube link for you to watch the complete solution.
The tree structure is fixed and is shown in the figure below. You need to write a program that
receives 12 numbers separated by space from the user. The 12 input numbers will correspond
to the 12 terminal nodes of the tree from left to right. Your program should print the index of
the terminal states that will be pruned using the alpha-beta search algorithm. The indexes are
fixed and are shown in the figure below (0 to 11). As an example case, if the middle red triangle
should be pruned completely, your program must print: “4 5 6 7” referring to the four terminal
nodes below that node.

Notes: (by Miguel Zavala)
    Maximizer state = normal triangle = alpha will be changed
    Minimizer state = upside down triangle = beta will be changed
    You do a left-right traversal along the tree
    
    AlphaBeta has two variables: (These are passed down node to child to child and then passed up to parent, left to right of tree) 
    Alpha = contains highest max value currently found, initialized with worst value = -infinity
    Beta = contains lowest min value currently found, initialized with worst value = +infinity

    At each triangle you have variable V where V is intialized as the worst possible value for that state
    EX: if current state is maximizer (normal triangle) then V = -infinity
    EX: if current state is minimizer (upside down triangle) then V = +infinity
    
    PRUNING:
    -you only prune when alpha>=beta value, then don't check the other side


'''
POSITIVE_INFINITY = float('inf')
NEGATIVE_INFINITY = float('-inf')



#Method to get the terminal states input from user
#Returns a list of integers
def getUserInputNumbers(n:int=12)->[int]:
    listOfNumbers = []
    i=1
    while i<=n:
        print(str(i)+")Enter number:")
        curr_input = input()
        if(curr_input.isdigit()==False):
            i=i-1
            print('This is not a valid number, retry')
            continue
        else:
            listOfNumbers.append(int(curr_input))

        i+=1

    #print("These are your input values:"+str(listOfNumbers))
    return listOfNumbers

#Method to get the terminal states input from user
#Returns a list of integers
def getUserInputNumbers2(n:int=12)->[int]:
    print("Enter 12 numbers separated by a (space) EX: 5 3 5 4 3 5 1 etc")
    stringinput = input()
    listOfStrings = stringinput.split(" ")

    listOfNumbers = []
    for s in listOfStrings:
        if(s.isdigit()):
            listOfNumbers.append(int(s))

    return listOfNumbers

#Enumeration type for alpha beta constants such 'Maximizer','Minimizer', and 'Terminal'
class ALPHABETA_TYPES(Enum):
    MAXIMIZER = 'maximizer'
    MINIMIZER = 'minimizer'
    TERMINAL = 'terminal'

    def __str__(self):
        return self.value


class AlphaBetaNode:
    def __init__(self,minmaxtype:ALPHABETA_TYPES=None, isRoot:bool=False,childrenNodes=[],parentNode=None,terminalValue:int=-1, isRightMostChild=False):
        self.childrenNodes = childrenNodes
        self.isRoot = isRoot
        self.minmaxtype = minmaxtype
        self.parentNode = parentNode

        if(self.minmaxtype==ALPHABETA_TYPES.TERMINAL):
            self.terminalValue = terminalValue


    def __str__(self):
        if(self.isRoot):
            return '(Node:' + str(self.minmaxtype) + "[ROOT])"
        if(self.minmaxtype==ALPHABETA_TYPES.TERMINAL):
            return '(Node:'+str(self.minmaxtype)+ ",Value:"+str(self.terminalValue)+",Parent:"+str(self.parentNode)+")"

        return '(Node:'+str(self.minmaxtype)+",Parent:"+str(self.parentNode)+")"#",Children:"+str(self.childrenNodes)

    def __repr__(self):
        return '(Node:'+str(self.minmaxtype)+",Parent:"+str(self.parentNode)+")"



class MinMaxTree:
    def __init__(self, n_Depth: int = 1, n_RootChildrenMinimizers: int = 3, n_MinimizerChildren: int = 2,
                 n_MaximizerChildren: int = 2,listOfTerminalValues=[]):
        self.root = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.MAXIMIZER,isRoot=True)

        self.listOfTerminalValues = listOfTerminalValues
        self.currentTerminalNodeIndex = 0

        self.remainingNodes = []
        self.prunedNodes = []
        self.prunedIndexes = []

        #Creates the Min Max Tree
        for i in range(n_RootChildrenMinimizers):
            currentMinimizerNode = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.MINIMIZER,parentNode=self.root,childrenNodes=[])
            self.root.childrenNodes.append(currentMinimizerNode)

            for k in range(n_MinimizerChildren):
                currentMaximizerNode = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.MAXIMIZER,parentNode=currentMinimizerNode,childrenNodes=[])
                currentMinimizerNode.childrenNodes.append(currentMaximizerNode)

                for j in range(n_MaximizerChildren):
                    if(self.currentTerminalNodeIndex>=len(listOfTerminalValues)):
                        return
                    else:
                        currentTerminalValue = listOfTerminalValues[self.currentTerminalNodeIndex]
                        currentTerminalNode = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.TERMINAL, parentNode=currentMaximizerNode,
                                                             childrenNodes=None,terminalValue=currentTerminalValue)
                        currentTerminalNode.terminalNodeIndex = self.currentTerminalNodeIndex
                        currentMaximizerNode.childrenNodes.append(currentTerminalNode)
                        self.currentTerminalNodeIndex+=1

    def printNode(node):
        tmp = node
        if(tmp.isRoot):
            print("ROOT:"+str(tmp.minmaxtype))
        elif(tmp.minmaxtype==ALPHABETA_TYPES.TERMINAL):
            print(str(tmp.minmaxtype)+", value:"+str(tmp.terminalValue))
        else:
            print(tmp.minmaxtype)
        if tmp.childrenNodes!=None:
            for child in tmp.childrenNodes:
                MinMaxTree.printNode(child)
        else:
            print('exit')
            return

    def printTreeFromRoot(self):
        MinMaxTree.printNode(self.root)

    #Compares the remaining nodes with the initial given terminal values and finds
    #out which terminal values were pruned
    def findPrunesIndexes(self):
        k=0
        for i in range(len(self.listOfTerminalValues)):
            currTerminalValue = self.listOfTerminalValues[i]

            try:
                currLeftOverNode = self.remainingNodes[k]
                if(currLeftOverNode==currTerminalValue):
                    ''
                    #print("Found corresponding node, Good")
                else:
                    #print("Did not find corresponding node")
                    self.prunedNodes.append(currTerminalValue)
                    self.prunedIndexes.append(i)
                    continue
            except:
                self.prunedNodes.append(currTerminalValue)
                self.prunedIndexes.append(i)

            k+=1

    #Recurses through the alpha beta min max tree and applies alpha beta pruning
    #Returns a dictionary containing information about the min max tree such as 'value', 'remainingNodes', 'prunedNodes' and 'prunedIndexes'
    def alphaBetaRecursion(self,node, alpha, beta):
        # Base Case:
        if (node.minmaxtype == ALPHABETA_TYPES.TERMINAL):
            # print("ENTERED")
            #print("CURRENT TERMINAL NODE:" + str(node.terminalValue))
            self.remainingNodes.append(node.terminalValue)
            #print("LEFT OVER NODES" + str(self.remainingNodes))
            return node.terminalValue
        elif (node.minmaxtype == ALPHABETA_TYPES.MAXIMIZER):
            totalsum = 0

            terminalValues = []
            for child in node.childrenNodes:
                # Gets each child's values
                currentvalue = self.alphaBetaRecursion(child, alpha, beta)

                # Terminal Parent Maximizers:
                # Gets the terminal node values:
                if (isinstance(currentvalue, int)):
                    terminalValues.append(currentvalue)
                    #print("TERMINAL VALUES:" + str(terminalValues))
                    # print(node)
                    # print(currentvalue)
                    alpha = max(alpha, currentvalue)  # Sets alpha to the biggest found value
                    # print("NEW ALPHA:" + str(alpha))
                    totalsum += currentvalue
                    # print(totalsum)

                    if (alpha >= beta):
                        #print("ALPHA IS GREATER OR EQUAL TO BETA")
                        break

                else:
                    ''
                    # print("ELSE")
                    #print(node)

                #print(terminalValues)

            if (node.isRoot):
                self.findPrunesIndexes()
                return {
                    'value': alpha,
                    'remainingNodes': self.remainingNodes,
                    'prunedNodes':self.prunedNodes,
                    'prunedIndexes':self.prunedIndexes
                }
            else:
                return alpha


        elif (node.minmaxtype == ALPHABETA_TYPES.MINIMIZER):
            maximizerBetaValues = []
            for child in node.childrenNodes:
                currentvalue = self.alphaBetaRecursion(child, alpha,
                                                  beta)  # should return None because no minimizer node is parent of a terminal node
                maximizerBetaValues.append(currentvalue)

                if (isinstance(currentvalue, int)):
                    maximizerBeta = currentvalue
                    beta = min(maximizerBeta, beta)

                    if (alpha >= beta):
                        #print("ALPHA IS GREATER OR EQUAL TO BETA")
                        break

                else:
                    ''
                    #print("MINIMIZER GOT:" + str(currentvalue))
                    #print('MAXIMIZER BETA VALUES:' + str(maximizerBetaValues))

            return beta






terminalstates = [4,6,7,9,1,2,0,1,8,1,9,2] #fixed variable to test alpha beta without inputting numbers
terminalstates = getUserInputNumbers2(12) #Gets user input for terminal values
print("Given terminal states:"+str(terminalstates))


currtree = MinMaxTree(n_RootChildrenMinimizers=30,listOfTerminalValues=terminalstates)

#currtree.printTreeFromRoot()
#MinMaxTree.printNode(currtree.root)


print("Thus after performing AlphaBeta Pruning with min max, we get:")
results = currtree.alphaBetaRecursion(currtree.root,NEGATIVE_INFINITY,POSITIVE_INFINITY)
print(results)
print("The pruned indexes are:"+str(results['prunedIndexes']))