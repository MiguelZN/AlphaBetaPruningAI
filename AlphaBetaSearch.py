from enum import Enum
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
    Maximizer state = normal triangle
    Minimizer state = upside down triangle
    Alpha = best already explored option along path to root for maximizer
    Beta = best already explored option along path to the root for minimizer
    You do a left-right traversal along the tree

    At each triangle you have variable V where V is intialized as the worst possible value for that state
    EX: if current state is maximizer (normal triangle) then V = -infinity
    EX: if current state is minimizer (upside down triangle) then V = +infinity


'''


def generateHeapOfMinMax(n_Depth: int = 1, n_RootChildrenMinimizers: int = 3, n_MinimizerChildren: int = 2,
                         n_MaximizerChildren: int = 2):
    heap = []
    rootNode = AlphaBetaNode(numberOfChildren=n_RootChildrenMinimizers, heapIndex=0,
                             minmaxtype=ALPHABETA_TYPES.MAXIMIZER)

    for i in range(0):
        ''


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

class ALPHABETA_TYPES(Enum):
    MAXIMIZER = 'maximizer'
    MINIMIZER = 'minimizer'
    TERMINAL = 'terminal'

    NEGATIVE_INFINITY = '-infinity'
    POSITIVE_INFINITY = '+infinity'

    def __str__(self):
        return self.value


class AlphaBetaEdge:
    class EDGE_DIRECTION(Enum):
        UP='up'
        DOWN='down'


        def __str__(self):
            return self.value

    def __init__(self, alpha:ALPHABETA_TYPES=ALPHABETA_TYPES.NEGATIVE_INFINITY, beta:ALPHABETA_TYPES=ALPHABETA_TYPES.POSITIVE_INFINITY, direction:EDGE_DIRECTION=None):
        self.alpha = alpha
        self.beta = beta
        self.direction =direction

    def __str__(self):
        return 'AlphaBetaEdge: Direction='+str(self.direction)+",AlphaValue="+str(self.alpha)+",BetaValue="+str(self.beta)

class AlphaBetaNode:
    def __init__(self,minmaxtype:ALPHABETA_TYPES=None, isRoot:bool=False,childrenNodes=[],parentNode=None,value:int=-1):
        self.childrenNodes = childrenNodes
        self.isRoot = isRoot
        self.minmaxtype = minmaxtype
        self.parentNode = parentNode
        self.value = value



    def __str__(self):
        return '(Node:'+str(self.minmaxtype)+",Parent:"+str(self.parentNode)+")"#",Children:"+str(self.childrenNodes)

    def __repr__(self):
        return '(Node:'+str(self.minmaxtype)+",Parent:"+str(self.parentNode)+")"



class MinMaxTree:
    def __init__(self, n_Depth: int = 1, n_RootChildrenMinimizers: int = 3, n_MinimizerChildren: int = 2,
                 n_MaximizerChildren: int = 2,listOfTerminalValues=[]):
        self.root = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.MAXIMIZER,isRoot=True)
        self.listOfTerminalValues = listOfTerminalValues
        self.currentTerminalNodeIndex = 0

        for i in range(n_RootChildrenMinimizers):
            currentMinimizerNode = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.MINIMIZER,parentNode=self.root,childrenNodes=[])
            self.root.childrenNodes.append(currentMinimizerNode)

            for k in range(n_MinimizerChildren):
                currentMaximizerNode = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.MAXIMIZER,parentNode=currentMinimizerNode,childrenNodes=[])
                currentMinimizerNode.childrenNodes.append(currentMaximizerNode)

                for j in range(n_MaximizerChildren):
                    currentTerminalValue = listOfTerminalValues[self.currentTerminalNodeIndex]
                    currentTerminalNode = AlphaBetaNode(minmaxtype=ALPHABETA_TYPES.TERMINAL, parentNode=currentMaximizerNode,
                                                         childrenNodes=None,value=currentTerminalValue)
                    currentMinimizerNode.childrenNodes.append(currentTerminalNode)
                    self.currentTerminalNodeIndex+=1



        print(self.root)

    def printNode(node):
        tmp = node

        if tmp.childrenNodes!=None:
            for child in tmp.childrenNodes:
                print(child)
                MinMaxTree.printNode(child)
        else:
            print('exit')
            return

    def printTreeFromRoot(self):
        MinMaxTree.printNode(self.root)


#terminalstates = getUserInputNumbers(12)
terminalstates = [4, 545, 32, 4, 2, 5, 75, 65, 83, 4, 3, 5]
print("Terminal states:"+str(terminalstates))


currtree = MinMaxTree(listOfTerminalValues=terminalstates)

currtree.printTreeFromRoot()
