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

class MonteCarloTree():
    def __init__(self, state):
        self.root = Node(state, None)
        self.curr = self.root
        self.turn = True
 
    # main function for the Monte Carlo Tree Search 
    def monteCarloTreeSearch(self, state):
        if not np.array_equal(state, self.root.state):
            if np.array_equal(state, self.curr.state):
                return self.curr
            else:
                for child in self.curr.children:
                    if np.array_equal(state, child.state):
                        self.curr = child

        # seconds = time.time()
        # while (time.time() - seconds) < 1:                 # computational power?
        for i in range(1000):
            print(i)
            print('s1')
            leaf = self.traverse(self.curr)
            print('s2')
            simulationResult = self.rollout(leaf)
            print('s3')
            self.backpropagate(leaf, simulationResult)
            print('s4')

        self.curr = self.bestChild(self.curr)
        return self.curr

    # function for node traversal
    def traverse(self, node):
        self.turn = True

        # selection
        while node.children:
            bestUcb = 0
            bestNode = node
            for child in node.children:
                if child.visits != 0:
                    ucb = child.wins/child.visits + 2*np.sqrt(np.log(child.parent.visits)/child.visits)
                else:
                    ucb = 1
                if ucb >= bestUcb:
                    bestUcb = ucb
                    bestNode = child
            node = bestNode
            if node.children:
                self.turn = not self.turn

        # expansion
        if not node.children:
            if node.visits == 0:
                return node
            else:
                # game over
                if self.gameOver(node.state) > -1:
                    return node
                
                self.createChildren(node)

                # Randomly choose a child for rollout
                node = np.random.choice(node.children)
                self.turn = not self.turn
                return node
    
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

    # function for the result of the simulation
    def rollout(self, node):
        tempNode = Node(node.state, None)
        turn = self.turn

        while self.gameOver(tempNode.state) < 0:
            # print(tempNode.state)
            # print()
            if not tempNode.children:
                self.createChildren(tempNode)
            tempNode = self.rolloutPolicy(tempNode)
            turn = not turn

        # print(tempNode.state)
        # print()

        if self.gameOver(tempNode.state) == 0:
            return 0
        elif self.turn:
            return -1
        else:
            return 1

    # function for randomly selecting a child node
    def rolloutPolicy(self, node):
        return np.random.choice(node.children)
    
    # function for backpropagation
    def backpropagate(self, node, result):
        node.wins += result
        node.visits += 1
        if not node.parent:
            return
        self.backpropagate(node.parent, -result)

    # function for selecting the best child
    # node with highest number of visits
    def bestChild(self, node):
        mostVisits = 0
        best = None
        for child in node.children:
            if child.visits > mostVisits:
                mostVisits = child.visits
                best = child
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
    mcts = MonteCarloTree(state)
    while True:
        state = np.copy(mcts.monteCarloTreeSearch(np.copy(state)).state)

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

    return mcts

#########################################################################################
if __name__ == "__main__":
    # state = np.array([[0,0,0],[0,0,0],[0,0,0]])
    # mcts = MonteCarloTree(state)
    # bestMove = mcts.monteCarloTreeSearch(state)

    # print('best move')
    # print(bestMove.state)

    mcts = humanVsAi()
    
    # print('#############################################')
    # print(mcts.root.state)
    # print(mcts.root.wins)
    # print(mcts.root.visits)
    # print()
    # level = mcts.root.children
    # totNodes = 0
    # treeSizeMb = 0
    # for i in range(9):
    #     nextLevel = []
    #     totVisits = 0
    #     levelStr = ''
    #     for node in level:
    #         totNodes += 1
    #         treeSizeMb += sys.getsizeof(node)
    #         levelStr += ' ' + str(node.wins) + '/' + str(node.visits)
    #         totVisits += node.visits
    #         for child in node.children:
    #             nextLevel.append(child)
    #     print('#### ' + str(totVisits) + ' #############################################')
    #     print(levelStr)
    #     level = nextLevel.copy()
    # print('#############################################')
    # print(totNodes)
    # print(treeSizeMb)

