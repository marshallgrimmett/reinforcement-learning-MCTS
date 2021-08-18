import time
import numpy as np
import sys

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.wins = 0
        self.visits = 0
        self.parent = parent
        self.children = []

class Monte_Carlo_Tree():
    def __init__(self, state):
        self.root = Node(state, None)
        self.curr = self.root
        self.turn = True
        self.currTurn = True

    # main function for the Monte Carlo Tree Search 
    def monte_carlo_tree_search(self, state):
        root = Node(state, None)
        
        # seconds = time.time()
        # while (time.time() - seconds) < 1:                 # computational power?
        for i in range(100):
            # print(i)
            self.turn = True

            # selection
            leaf = root
            while True:
                # print(leaf.state)
                bestUcb = None
                bestNode = leaf
                for child in leaf.children:
                    if child.visits != 0:
                        ucb = child.wins/child.visits + 1*np.sqrt(np.log(child.parent.visits)/child.visits)
                    else:
                        ucb = 1
                    if bestUcb == None:
                        bestUcb = ucb
                        bestNode = child
                    if ucb >= bestUcb:
                        bestUcb = ucb
                        bestNode = child
                leaf = bestNode
                if leaf.children:
                    self.turn = not self.turn
                else:
                    break

            # expansion
            if leaf.visits != 0:
                if self.gameOver(leaf.state) == -1:
                    self.createChildren(leaf)
                    leaf = np.random.choice(leaf.children)
                    self.turn = not self.turn
            
            # rollout
            tempNode = Node(leaf.state, None)
            turn = self.turn
            while self.gameOver(tempNode.state) < 0:
                if not tempNode.children:
                    self.createChildren(tempNode)
                tempNode = np.random.choice(tempNode.children)
                turn = not turn
            if self.gameOver(tempNode.state) == 0:
                simulationResult = 0.5
            elif turn:
                simulationResult = 0
            else:
                simulationResult = 1
        
            # backpropogate
            self.backpropagate(leaf, simulationResult)

        self.printInfo(root)
        return self.best_child(root)

    # find all possible moves and add them as children to node
    def createChildren(self, node):
        for idx, move in np.ndenumerate(node.state):
            if move == 0:
                newState = np.copy(node.state)
                if self.turn:
                    newState[idx] = 2
                else:
                    newState[idx] = 1
                newNode = Node(newState, node)
                node.children.append(newNode)
        return
    
    # function for backpropagation
    def backpropagate(self, node, result):
        node.wins += result
        node.visits += 1
        if not node.parent:
            return
        self.backpropagate(node.parent, 1-result)

    # function for selecting the best child
    # node with highest number of visits
    def best_child(self, node):
        most_visits = 0
        best = None
        for child in node.children:
            if best == None:
                best = child
            if not ((child.visits == 0) or (best.visits == 0)):
                if (child.wins / child.visits) > (best.wins / best.visits):
                    best = child
            # if child.visits > most_visits:
            #     most_visits = child.visits
            #     best = child
        return best
    
    # function to determine if game has ended.
    # -1 if game has not ended.
    # 0 if game ended in cats.
    # 1 if game ended with a winner.
    def gameOver(self, state):
        victory = False

        for row in state:
            if (0 not in row) and (row[0] == row[1]) and (row[0] == row[2]):
                victory = True
                break
        for col in state.T:
            if (0 not in col) and (col[0] == col[1]) and (col[0] == col[2]):
                victory = True
                break
        if (0 not in [state[0,0], state[1,1], state[2,2]]) and (state[0,0] == state[1,1]) and (state[0,0] == state[2,2]):
                victory = True
        if (0 not in [state[0,2], state[1,1], state[2,0]]) and (state[0,2] == state[1,1]) and (state[0,2] == state[2,0]):
                victory = True

        if (not victory) and (0 not in state):
            return 0

        if victory == True:
            return 1
        else:
            return -1

    def printInfo(self, root):
        print('#############################################')
        print(root.state)
        print(root.wins)
        print(root.visits)
        print()
        level = root.children
        totNodes = 0
        treeSizeMb = 0
        for i in range(9):
            nextLevel = []
            totVisits = 0
            levelStr = ''
            for node in level:
                totNodes += 1
                treeSizeMb += sys.getsizeof(node)
                levelStr += ' ' + str(node.wins) + '/' + str(node.visits)
                totVisits += node.visits
                for child in node.children:
                    nextLevel.append(child)
            print('#### ' + str(totVisits) + ' #############################################')
            print(levelStr)
            level = nextLevel.copy()
        print('#############################################')
        print(totNodes)
        print(treeSizeMb)

#########################################################################################

def gameOver(state, playerOne):
    victory = False

    for row in state:
        if (0 not in row) and (row[0] == row[1]) and (row[0] == row[2]):
            victory = True
            break
    for col in state.T:
        if (0 not in col) and (col[0] == col[1]) and (col[0] == col[2]):
            victory = True
            break
    if (0 not in [state[0,0], state[1,1], state[2,2]]) and (state[0,0] == state[1,1]) and (state[0,0] == state[2,2]):
            victory = True
    if (0 not in [state[0,2], state[1,1], state[2,0]]) and (state[0,2] == state[1,1]) and (state[0,2] == state[2,0]):
            victory = True

    if (not victory) and (0 not in state):
        print('Cats Game.')
        return True
    if victory and playerOne:
        print(state)
        print('Tic Tac Toe!')
        print('Player 1 Wins.')
        return True
    elif victory and not playerOne:
        print(state)
        print('Tic Tac Toe!')
        print('Player 2 Wins.')
        return True
    
    return False

def humanVsAi():
    state = np.array([[0,0,0],[0,0,0],[0,0,0]])
    mcts = Monte_Carlo_Tree(state)
    i = 0
    while True:

        if gameOver(state, False):
            break

        while True:
            print(state)
            print('Make your move.')

            while True:
                print('Enter row:')
                try:
                    row = int(input())
                    if row in [0,1,2]:
                        break
                except:
                    print('Please enter 0, 1, or 2 representing the row.')

            while True:
                print('Enter column:')
                try:
                    col = int(input())
                    if col in [0,1,2]:
                        break
                except:
                    print('Please enter 0, 1, or 2 representing the column.')

            if state[row, col] == 0:
                state[row, col] = 1
                break
            else:
                print('Square already taken. Try another.')

        if gameOver(state, True):
            break

        state = np.copy(mcts.monte_carlo_tree_search(np.copy(state)).state)

    return mcts

#########################################################################################
if __name__ == "__main__":
    # state = np.array([[0,0,0],[0,0,0],[0,0,0]])
    # state = np.array([[1, 2, 0],
    #                   [0, 1, 0],
    #                   [2, 0, 1]])
    # mcts = Monte_Carlo_Tree(state)
    # bestMove = mcts.monte_carlo_tree_search(state)

    # print('best move')
    # print(bestMove.state)

    mcts = humanVsAi()


