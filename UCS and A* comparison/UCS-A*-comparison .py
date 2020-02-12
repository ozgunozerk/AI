from queue import PriorityQueue
from heapq import heappush, heappop
import time



class Node:
  def __init__(self, coordinates, goal, parent=None):
      # debug
      #if len(coordinates) == 2:
      #    self.id = str(coordinates[0][0]) + str(coordinates[0][1]) + str(coordinates[1][0] + str(coordinates[1][1]))
      #elif len(coordinates) == 1:
      #    self.id = str(coordinates[0][0]) + str(coordinates[0][1])
      # debug
      self.state = coordinates  # storing the coordinates as the state
      self.cost = 1  # cost is set to 2 for every node, since every state is cost-wise equal, and in every step we are moving a 2x1x1 block
      self.parent = parent  # setting the parent node
      self.heuristic = heuristic(coordinates, goal)  # setting the heuristic via calling the function (euclidean distance)
      if (parent == None):
          self.cost_so_far = 1
      else:
          self.cost_so_far = parent.cost_so_far + 1  # cost_so_far is the cost + previous cost of the parent node

# for constructing the path
def pathFinder(node, trialnumber, memory):
  print("Amount of Trial:", trialnumber)
  print("Amount of Memory:", memory)
  current = node
  path = [current.state]
  while current.parent != None:
      current = current.parent
      path.append(current.state)
  path.reverse()
  return path

# A*
def a_star(beginning, goal, board):
  trial_number = 0
  memorycount = 1
  fringe = []  # initialise the open list
  closed = []  # initialise the closed list
  newNode = Node(beginning, goal)  # initialize the root node
  heappush(fringe, (newNode.cost_so_far + newNode.heuristic, newNode.cost_so_far, newNode.state, newNode))  # put the starting node on the open list
  while(len(fringe) > 0):  # while open list is not empty
      memorycount += 1
      trial_number += 1
      current_node_tuple = heappop(fringe)  # assigning the lowest cost node to our current node
      current_node = current_node_tuple[3]  # since this is a tuple, node itself is in the 1st index (0th index is the cost)
      if goal_state(board, current_node.state, goal):  # if the current node is the goal
          return pathFinder(current_node, trial_number, memorycount)  # return the solution
      else:  # if not, continue searching
          new_states = successor_state(board, current_node.state)  # getting the successor states
          for i in range(len(new_states)):  # for each successor state
              memorycount += 1
              successor_node = (Node(new_states[i], goal, current_node))  # create a successor node
              fringe_node_exist = False
              closed_node_exist = False  # for checking if there exists the same state in closed list
              fringe_node_exist2 = False  # for checking if there exists the same state in fringe list with higher cost
              closed_node_exist2 = False  # for checking if there exists the same state in closed list with higher cost
              for k in range(len(fringe)):
                  memorycount += 1
                  if fringe[k][3].state == successor_node.state:
                      memorycount += 1
                      fringe_node_exist = True
                      if fringe[k][3].state == successor_node.state and fringe[k][3].cost_so_far == successor_node.cost_so_far and fringe[k][3].heuristic == successor_node.heuristic:
                          memorycount += 1
                          fringe_node_exist2 = True
                          fringe_exist2_index = k
              for m in range(len(closed)):  # for each node in closed list
                  memorycount += 1
                  if closed[m].state == successor_node.state:  # same state with the successor state exists in the closed list
                      memorycount += 1
                      closed_node_exist = True  # setting the control boolean to True
                      if (closed[m].cost_so_far + closed[m].heuristic) > (successor_node.heuristic + successor_node.cost_so_far):
                          memorycount += 1
                          closed_node_exist2 = True  # same state exists with a higher cost, setting the control boolean to True
                          closed_exist2index = m  # storing the index of that higher cost node
              if closed_node_exist == False and fringe_node_exist == False:
                  memorycount += 1
                  heappush(fringe, (successor_node.cost_so_far + successor_node.heuristic, successor_node.cost_so_far, successor_node.state, successor_node))  # adding successor node into the open list
              elif fringe_node_exist2 == True:
                  memorycount += 1
                  fringe[fringe_exist2_index] = (successor_node.cost_so_far + successor_node.heuristic, successor_node.cost_so_far, successor_node.state, successor_node)
              elif closed_node_exist2 == True:  # if successor state exists in the closed list with a higher cost
                  memorycount += 1
                  closed[closed_exist2index].cost_so_far = successor_node.cost_so_far  # updating the node in the closed list
                  closed[closed_exist2index].heuristic = successor_node.heuristic
                  closed[closed_exist2index].parent = successor_node.parent
                  heappush(fringe, (closed[closed_exist2index].cost_so_far + closed[closed_exist2index].heuristic, closed[closed_exist2index].cost_so_far, closed[closed_exist2index].state, closed[closed_exist2index]))

          closed.append(current_node)
  print(memorycount)

# UCS
def ucs(beginning, goal, board):
  memorycount = 1
  priority = []  # creating a priorityQueue for storing the nodes
  visited = []  # we should not visit the same node again in any scenario, so keeping track of them
  newNode = Node(beginning, goal)  # creating the initial node (root)
  heappush(priority, (newNode.cost_so_far, newNode.state, newNode))  # storing the root in the priorityQueue
  trial = 0
  while len(priority) > 0:  #loop to iterate through the priorityQueue
      memorycount += 1
      trial += 1
      current_node_tuple = heappop(priority)  # assigning the lowest cost node to our current node
      current_node = current_node_tuple[2]  # since this is a tuple, node itself is in the 1st index (0th index is the cost)
      if goal_state(board, current_node.state, goal):  # if current node is the goal, end the algorithm
          return pathFinder(current_node, trial, memorycount)
      else:  # if not, continue searching
          successorList = successor_state(board, current_node.state)  # get the current node's successor states and store them in a list
          for i in range(len(successorList)):  # iterate through all the successors
              memorycount += 1
              newSuccessor = Node(successorList[i], goal, current_node)  # create a newNode with that successor state (with costs and parents)
              visited_node_exist = False  # controller for checking if a successor state exist in the visited list
              priority_node_exist = False
              priority_node_exist2 = False
              for j in range(len(visited)):  # iterate through all the visited list to compare if same successor state exists
                  memorycount += 1
                  if newSuccessor.state == visited[j].state:  # if successor state exists in visited
                      memorycount += 1
                      visited_node_exist = True  # make the boolean controller True
              for k in range(len(priority)):
                  memorycount += 1
                  if priority[k][2].state == newSuccessor.state:
                      memorycount += 1
                      priority_node_exist = True
                      if priority[k][2].cost_so_far == newSuccessor.cost_so_far:
                          memorycount += 1
                          priority_node_exist2 = True
                          priority_index = k
              if visited_node_exist == False and priority_node_exist == False:
                  memorycount += 1
                  heappush(priority, (newSuccessor.cost_so_far, newSuccessor.state, newSuccessor))  # add it into the Queue
              elif priority_node_exist2 == True:
                  memorycount += 1
                  priority[priority_index] = (newSuccessor.cost_so_far, newSuccessor.state, newSuccessor)
          visited.append(current_node)  # add current node to the visited list
  print(memorycount)
# State definitions

def goal_state(board, current_state, goal):
  if len(current_state) == 1 and current_state[0][0] == goal[0][0] and current_state[0][1] == goal[0][1]:  # if block is occupying 1 space and its matching goal coordinates
      return True
  else:
      return False

def initial_state(matrix):
  block_coordinates = []  # variable for storing block coordinates
  goal_coordinates = []  # variable for storing goal coordinates
  for m in range(len(matrix)):  # iterating through the matrix rows
      for n in range(len(matrix[0])):  # iterating through the matrix columns
          if matrix[m][n] == 'S':  # where block stays are also available place
              block_coordinates.append([m,n])  # storing the coordinates of the block
              matrix[m][n] = 'O'  # so setting them as available place
  for k in range(len(matrix)):  # iterating through the matrix rows
      for l in range(len(matrix[0])):  # iterating through the matrix rows
          if matrix[k][l] == 'G':  # finding the goal coordinates
              matrix[k][l] = 'O'  # setting goal as available place
              goal_coordinates.append([k,l])
  return matrix, block_coordinates, goal_coordinates  # returning the results

def successor_state(board, current_state):
  successor_list = []

  if len(current_state) == 2:  # block is occupying 2 space

      if current_state[0][0] == current_state[1][0]:  # block is horizontal
          if board[current_state[0][0] -1][current_state[0][1]] == 'O' and (board[current_state[1][0] -1][current_state[1][1]] == 'O'):  # move up
              successor_list.append([[current_state[0][0] - 1, current_state[0][1]], [current_state[1][0] - 1, current_state[1][1]]])
          if board[current_state[0][0] + 1][current_state[0][1]] == 'O' and (board[current_state[1][0] + 1][current_state[1][1]] == 'O'):  # move down
              successor_list.append([[current_state[0][0] + 1, current_state[0][1]], [current_state[1][0] + 1, current_state[1][1]]])
          if board[current_state[0][0]][current_state[0][1] - 1] == 'O':
              successor_list.append([[current_state[0][0], current_state[0][1] - 1]])  # move left
          if board[current_state[1][0]][current_state[1][1] + 1] == 'O':
              successor_list.append([[current_state[1][0], current_state[1][1] +1]])  # move right

      elif current_state[0][1] == current_state[1][1]:  # block is vertical
          if board[current_state[0][0]][current_state[0][1] -1] == 'O' and (board[current_state[1][0]][current_state[1][1] -1] == 'O'):  # move left
              successor_list.append([[current_state[0][0], current_state[0][1] -1 ], [current_state[1][0], current_state[1][1] -1]])
          if board[current_state[0][0]][current_state[0][1] + 1] == 'O' and (board[current_state[1][0]][current_state[1][1] + 1] == 'O'):  # move right
              successor_list.append([[current_state[0][0], current_state[0][1] +1 ], [current_state[1][0], current_state[1][1] +1]])
          if board[current_state[0][0]-1][current_state[0][1]] == 'O':
              successor_list.append([[current_state[0][0]-1, current_state[0][1]]])  # move up
          if board[current_state[1][0]+1][current_state[1][1]] == 'O':
              successor_list.append([[current_state[1][0]+1, current_state[1][1]]])  # move down

  elif len(current_state) == 1:  # block stands up
      if board[current_state[0][0]][current_state[0][1] + 1] == 'O' and board[current_state[0][0]][current_state[0][1] + 2] == 'O':   # move right
          successor_list.append([[current_state[0][0], current_state[0][1] +1 ], [current_state[0][0], current_state[0][1] + 2]])
      if board[current_state[0][0]][current_state[0][1] - 2] == 'O' and board[current_state[0][0]][current_state[0][1] - 1] == 'O':  # move left
          successor_list.append([[current_state[0][0], current_state[0][1] - 2], [current_state[0][0], current_state[0][1] - 1]])
      if board[current_state[0][0] - 2][current_state[0][1]] == 'O' and board[current_state[0][0] - 1][current_state[0][1]] == 'O':  # move up
          successor_list.append([[current_state[0][0] - 2, (current_state[0][1])], [current_state[0][0] - 1, (current_state[0][1])]])
      if board[current_state[0][0] + 1][current_state[0][1]] == 'O' and board[current_state[0][0] + 2][current_state[0][1]] == 'O':  # move up
          successor_list.append([[current_state[0][0] + 1, current_state[0][1]], [current_state[0][0] + 2, current_state[0][1]]])
  return successor_list

def heuristic(block, goal):
  a = [0,0]  # starting point (block)
  if len(block) == 2: # if block is not standing up
      a[0] = (block[0][0] + block[1][0])/2.0
      a[1] = (block[0][1] + block [1][1])/2.0
  elif len(block) == 1:
      a[0] = block[0][0]
      a[1] = block[0][1]

  return (abs(a[1] - goal[0][1]) + abs(a[0] - goal[0][0])) #return the Manhattan Distance

current_state = []
board = []
matrix = []

row = int(input("Please enter matrix row amount: "))
col = int(input("Please enter matrix column amuount: "))
text = input("Enter the whole matrix as one line")
for i in range(0, row+2):
  matrix.append([])
  for j in range(0,col+2):
      matrix[i].append('X')

for i in range(1,row+1):
  for j in range(1,col+1):
      matrix[i][j] = text[(i-1)*(col) + (j-1)]


board, current_state, goal = initial_state(matrix)

start = time.clock()

solution = a_star(current_state, goal, board)

try:
    if len(solution) > 0:
        for i in range(len(solution)):
            print("Step", i+1, ": ", solution[i])
except TypeError:
  print("No solution found!")

print("Time elapsed:",time.clock() - start)