# Jason Rudinsky
# October 2, 2025
# CAI 5005 - Intro to AI - Project 1 - Part 3

# This is a program that will simulate the 2 player game using minimax and later alpha-beta pruning. 
# The program will allow for the user to play against a minimax agent (with or without alpha beta pruning), 
# the playing against another random agent, and the ability for the program to go up against it's own minimiax 
# agent (ergo, two minimax agents going against each other)

# 10/2/2025 - Original Version
# 10/3/2025 @ 2:48 PM - Added in the fun methods for trying to compute the available directions that the user is able to go for their turn.
    # Also tried to start the process for determining when to go a certain direction and when a person is able to pick up resources or
    # deposit resources at the base.
# 10/4/2025 @ 10:31 AM - Added in a method to help with the easiness of computing what the coordinates of a user will be after the move is made. 
    # Also added in the functions for the mini-max traversal. As far as I know the only thing that doesn't work correctly is for the heurisitic 
    # to determine the values of the mini-max nodes.


import sys                                                                                                          # Imports the sys libraries
from copy import deepcopy                                                                                           # Imports the deepcopy method
from random import choice                                                                                           # Imports the choice method from the random library



class Node:                                                                                                         # Class BLock
    
    def __init__(self, coordinate, base, baseCoor, pack):                                                           # Initializer method
        self.__coordinate = coordinate                                                                              # Sets the value of self.__coordinate
        self.__baseCoor = baseCoor                                                                                  # Sets the value of self.__baseCoor
        self.__baseStats = deepcopy(base)                                                                           # Sets the value of self.__baseStats
        self.__backpack = deepcopy(pack)                                                                            # Sets the value of self.__backpack
            
    def getCoordinates(self):                                                                                       # GETTER METHOD
        return self.__coordinate                                                                                    # Returns self.__coordinate

    def getIndividualCoor(self):                                                                                    # GETTER METHOD
        return self.__coordinate[0], self.__coordinate[1]                                                           # Returns the x, y coordinates 

    def getBaseCoor(self):                                                                                          # GETTER METHOD
        return self.__baseCoor                                                                                      # Returns self.__baseCoor
    
    def getBase(self):                                                                                              # GETTER METHOD
        return deepcopy(self.__baseStats)                                                                           # Returns a copy of self.__baseStats
        
    def getPack(self):                                                                                              # GETTER METHOD
        return deepcopy(self.__backpack)                                                                            # Returns a copy of self.__backpack
        
    def __str__(self):                                                                                              # Str method
        
        return f"At {self.__coordinate} with the following items in the pack: \n\t{self.__backpack}\n\tAt base {self.__baseCoor}: {self.__baseStats} \n"
    
    


# This is just a data validation method to make sure that the name of the graph entered ends in .txt; 
# If it doesn't then i will just return the value passed in + ".txt"
def endsInTxt(fileName: str) -> str:                                                                                # Method Block
    
    return fileName if fileName.endswith(".txt") else fileName + ".txt"                                             # Returns the str to the user



# This is just a method that will be used to auto-generate the name of the output file if that is not specified 
# when the commands are entered in to the command line prompt
def outputGenerator(inputName: str):                                                                                # Method Block
    
    seperation = inputName.split(".txt")                                                                            # Defines separation
    return seperation[0] + "-output.txt"                                                                            # Returns the value to the user


# This is the method that will be used to start the solving of the path 
# to take for the maze in the input graph that is passed to the user
def makeGraph(argv: list(str())) -> list(list(str())):                                                              # Method Block
                                                                                                                    
                                                                                                                    # VARIABLE DEFINITIONS
    myFile = open(argv[0], "r")                                                                                     # Attempts to open the file in read mode
    fileInfo = myFile.readlines()                                                                                   # Obtains the information from the fiel
    row, col = fileInfo[0].split()                                                                                  # Sets the value of row and col
    graph = list()                                                                                                  # Initializes the value of graph
    
    myFile.close()                                                                                                  # Closes the file
    
    row = int(row)                                                                                                  # Converts row to an integer
    col = int(col)                                                                                                  # Converts col to an integer
    graph = [["" for i in range(row)] for j in range(col)]                                                          # Initially fills the value of graph
    
    fileInfo = fileInfo[1:]                                                                                         # Prunes the first row from fileInfo
    
    for i in range(row):                                                                                            # For Loop
        line = fileInfo[i].split()                                                                                  # Sets the value of line    
        for j in range(col):                                                                                        # Nested For Loop
            graph[i][j] = line[j]                                                                                   # Updates the value of graph at the index of i and j

    return graph                                                                                                    # Returns the filled graph to the user
    
    
    
# This is the method that will check to make sure that the coordinate 
# we are trying to go to is within the bounds of the table
def validCoordinates(row: int, column: int, graph) -> bool:                                                         # Method Block
    
    #print(f"Testing ({row}, {column})")
    if row < 0 or row >= len(graph):                                                                                # The value of row is not in bounds of the graph
        return False                                                                                                # Returns false to the user
    elif column < 0 or column >= len(graph[0]):                                                                     # The value of column is not in bounds of the graph
        return False                                                                                                # Returns false to the user
    
    return True                                                                                                     # Returns true to the user
        
    
        
# This is a helper method that will be used to display the contents of the grid.
# It will only be used as a helper method that will be useless once a certain stage in the program is reached.
def printList(table, playerA = None, playerB = None):
    
    for row in range(len(table)):                                                                                   # For Loop
        for col in range(len(table[row])):                                                                          # Nested For Loop
            
            if playerA != None:                                                                                     # Passing in an object
                if playerA.getCoordinates() == (row, col):
                    print(f"\033[94m{table[row][col]:^5s}", end = "")                                               # Prints out to the user
                elif playerB.getCoordinates() == (row, col):
                    print(f"\033[91m{table[row][col]:^5s}", end = "")                                               # Prints out to the user
                else:
                    print(f"\033[0m{table[row][col]:^5s}", end = "")                                                # Prints out to the user
            else:
                print(f"\033[0m{table[row][col]:^5s}", end = "")                                                    # Prints out to the user
        
        print("\033[0m")                                                                                            # Prints a blank line to the user
    
    if playerA != None:                                                                                             # Additional information about the players
        
        print(f"Player A\'s at coordinates {playerA.getCoordinates()}\n\tbase: {playerA.getBase()}\n\tbackpack: {playerA.getPack()}")
        print(f"Player B\'s at coordinates {playerB.getCoordinates()}\n\tbase: {playerB.getBase()}\n\tbackpack: {playerB.getPack()}")


# This is the method that will be used to return the euclidean heuristic value.
# I have not decided whether or not to choose this or manhattan for the heuristic
# so both will be included until I make a decision

# I can use the math.dist formula for the euclidean distance
def manhattanHeuristic(currentState, terminalState):                                                                # Method Block
   
                                                                                                                    # VARIABLE DEFINITIONS
   curXYPosition = currentState                                                                                     # Defines a variable to look at the values in the tuple currentState
   terminationXYPosition = terminalState                                                                            # Defines a variable to look at the values in the tuple terminalState
   
   # Manhattan = |x1 - x2| + |y1 - y2|
   return abs(curXYPosition[0] - terminationXYPosition[0]) + abs(curXYPosition[1] - terminationXYPosition[1])       # Returns the manhattan distance to the user



# This is the method that will be used to help with the playing of the game. 
# It will be where the initial starting of the game will commence. 
# It will also fill the values of the locations of the resources on the map.
def playTheGame(graph, onePlayer = True, randomState = False, minimax = True, alphaBeta = False):                   # Method Block
    
                                                                                                                    # VARIABLE DEFINITIONS
    turn = "A"                                                                                                      # Sets the value of turn
    playerA = Node((0, 0), list(), (0, 0), list())                                                                  # Creates the default position for playerA
    playerB = Node((len(graph) - 1, len(graph[0]) - 1), list(), (len(graph) - 1, len(graph[0]) - 1), list())        # Creates the default position for playerB
    
    resourceCoordinates = []                                                                                        # Defines resourceCoordinates
    nextMove = []
    
    for i in range(len(graph)):                                                                                     # For Loop
        for j in range(len(graph[i])):                                                                              # Nested For Loop
            
            if graph[i][j][-1] in ['S', 'I', 'C']:                                                                  # If the coordinate has a resource, then add it to the list
                resourceCoordinates.append((i, j))                                                                  # Appends to resourceCoordinates
                
                
    openingMove = (playerA, playerB, deepcopy(resourceCoordinates), turn)                                                     # Defines openingMove
    nextMove.append(openingMove)                                                                                    # Appends the openingMove to the list
                
    while not gameOver(playerA, playerB, resourceCoordinates):                                                      # As long as the coordinates are not all delivered 
        
        playerA, playerB, resources, whoseTurn = nextMove.pop()                                                     # Pops the information from the list
        
        printList(graph, playerA, playerB)                                                                          # Debug print statement
        
        # Even if the turn isn't one player, or it's not player A then we will go to the computer
        if onePlayer and whoseTurn == "A":                                                                          # If statement
            
            LCV = 0                                                                                                 # Sets the value of LCV
            
            directions = ['N', 'S', 'E', 'W']                                                                       # Sets the value of directions
            
            while LCV < len(directions):                                                                            # While Loop
                
                if not availableDirection(graph, playerA.getCoordinates()[0], playerA.getCoordinates()[1], directions[LCV], playerB):
                    directions.pop(LCV)                                                                             # Removes the direction from the list
                else:                                                                                               # We can go this direction
                    LCV += 1                                                                                        # Adds to the value of LCV
                    
            userInput = input(f"Of the list of options to choose from, please enter the direction you want to go: {directions} ").upper()
            
            while userInput.upper() not in directions:                                                              # While Loop
                print("You chose an option not available as a direction")                                           # Prints out to the user
                userInput = input(f"From the options: {directions}, please choose again. ").upper()                 # Taking input from the user    
        
        else:
            
            # For now this is for when the agent has been created. 
            # The random state agent will be a greedy algorithm
            # As of right now it will be a completely random movement agent
            if randomState:                                                                                         # We are doing the randomState machine for the baseline
                LCV = 0                                                                                             # Sets the value of LCV
            
                directions = ['N', 'S', 'E', 'W']                                                                   # Sets the value of directions
                
                while LCV < len(directions):                                                                        # While Loop
                    
                    if not availableDirection(graph, playerB.getCoordinates()[0], playerB.getCoordinates()[1], directions[LCV], playerA):
                        directions.pop(LCV)                                                                         # Removes the direction from the list
                    else:                                                                                           # We can go this direction
                        LCV += 1                                                                                    # Adds to the value of LCV
                
                userInput = choice(directions)                                                                      # Sets the value of userInput
            
            elif minimax:
                
                userInput = maxValue(playerA, playerB, deepcopy(resourceCoordinates), resourceCoordinates, whoseTurn, 0, graph)
                print("Hello!!!!!", userInput)
            #break
        
        
        # This player making the move is player A
        if whoseTurn == "A":                                                                                        # It's player A who is moving
            
            x, y = playerA.getIndividualCoor()                                                                      # Sets the value of x and y
            x, y = updatedCoordinates(x, y, userInput)                                                              # Call to method updatedCoordinates
            
            newPack = playerA.getPack()                                                                             # Copies the information into the newPack
            newBase = playerA.getBase()                                                                             # Copies the information into newBase            
            
            if (x, y) in resources and len(playerA.getPack()) < 2:                                                  # We found a resource and have space to claim it
                
                newPack.append(graph[x][y][-1])                                                                     # Appends to the newPack
                resources.remove((x, y))                                                                            # Removes the tuple from resources                
                    
                graph[x][y] = graph[x][y][:-1] + "E"                                                                # Picks up the resource
            
            elif (x, y) == playerA.getBaseCoor():                                                                   # We arrived back at the base
                
                newBase += newPack                                                                                  # Adds the contents of the pack to the base
                newPack = list()                                                                                    # Creates an empty list for the pack
            
            
            newPlayerA = Node((x, y), newBase, playerA.getBaseCoor(), newPack)                                      # Creates an object of the Node classd
            nextMove.append((newPlayerA, playerB, resources, "B"))                                                    # Appends to the list                        
            
            
        else:
            
            x, y = playerB.getIndividualCoor()                                                                      # Sets the value of x and y
            
            x, y = updatedCoordinates(x, y, userInput)                                                              # Call to method updatedCoordinates
            
            newPack = playerB.getPack()                                                                             # Copies the information into the newPack
            newBase = playerB.getBase()                                                                             # Copies the information into newBase            
            
            if (x, y) in resources and len(playerB.getPack()) < 2:                                                  # We found a resource and have space to claim it
                
                newPack.append(graph[x][y][-1])                                                                     # Appends to the newPack
                resources.remove((x, y))                                                                            # Removes the tuple from resources                
                    
                graph[x][y] = graph[x][y][:-1] + "E"                                                                # Picks up the resource
            
            elif (x, y) == playerB.getBaseCoor():                                                                   # We arrived back at the base
                
                newBase += newPack                                                                                  # Adds the contents of the pack to the base
                newPack = list()                                                                                    # Creates an empty list for the pack
            
            
            newPlayerB = Node((x, y), newBase, playerB.getBaseCoor(), newPack)                                      # Creates an object of the Node classd
            nextMove.append((playerA, newPlayerB, resources, "A"))                                                  # Appends to the list                        
            
        
                
                #playerA, playerB, resources, whoseTurn = nextMove.pop()                                                     # Pops the information from the list

        
        # if we are doing a game with the computer making the turn we want to have
            # either the random state, minimax, alpha beta pruning agent
        # compute which direction to go and then take that action.
    else:
        
        if len(playerA.getBase()) > len(playerB.getBase()):                                                         # Player A collected the most amount of resources
            print("Player A wins!")                                                                                 # Prints out to the user
            
        elif len(playerA.getBase()) < len(playerB.getBase()):                                                       # Player B collected the most amount of resources
            print("Player B Wins")                                                                                  # Prints out to the user
        
        else:                                                                                                       # Both players collected the same amount of resources
            print("It\'s a Tie")                                                                                    # Prints out to the user
        
        
        
# This is the method that will be used to determine whether or not the user can go in a specific direction
def availableDirection(graph, xCoor, yCoor, direction, playerB):                                                    # Method Block
    
    
    
    xCoor, yCoor = updatedCoordinates(xCoor, yCoor, direction)                                                      # Call to method updatedCoordinates
    
    if xCoor < 0 or xCoor >= len(graph):                                                                            # If the x-coordinate is beyond the bounds of the graph
        return False                                                                                                # Returns false to the user
    
    if yCoor < 0 or yCoor >= len(graph[0]):                                                                         # If the y-coordinate is beyond the bounds of the graph
        return False                                                                                                # Returns false to the user
    
    if (xCoor, yCoor) == playerB.getCoordinates():                                                                  # If the player will collide with the other player
        return False                                                                                                # Returns false to the user
    
    return True                                                                                                     # Returns true to the user
    
         

# This is the method that will be used to determine if the game is over
def gameOver(playerA, playerB, resourceCoordinates):                                                                # Method BLock
    
    return len(playerA.getBase()) + len(playerB.getBase()) == len(resourceCoordinates)                              # Returns the bool value to the user



# This is a helper method that will just assist in the computation of the new coordinate that the player will be moving to.
# It will take in the x and y coordinates, along with the direction and will return the updated x and y values to the user.
def updatedCoordinates(xCoor, yCoor, stepTaken):                                                                    # Method Block
    
    match stepTaken:                                                                                                # Match case
        
        case "E":                                                                                                   # In the case of East
            yCoor += 1                                                                                              # Adds to the value of 

        case "S":                                                                                                   # In the case of South
            xCoor += 1                                                                                              # Adds to the value of xCoor
        
        case "W":                                                                                                   # In the case of West
            yCoor -= 1                                                                                              # Subtracts from the value of yCoor
            
        case "N":                                                                                                   # In the case of North
            xCoor -=1                                                                                               # Subtracts from the value of xCoor
            
        case _:                                                                                                     # Default case
            raise Exception("Unknown direction entered")                                                            # Raises the error to the user
    
    
    return xCoor, yCoor                                                                                             # Returns the updated values to the user
    
    

# This is the method that will be used to help with determining the value of minimax. This will be the max function of the mini-max algorithm.
def maxValue(playerA, playerB, availableResources, resourceCoordinates, whoseTurn, depth, graph):                   # Method Block
    
    # For now the heuristic function will be the backpack + base resources - (opponents backpack + resources)
    if gameOver(playerA, playerB, resourceCoordinates) or depth == 3:                                               # If statement
        return len(playerA.getBase()) + len(playerA.getPack()) - len(playerB.getBase()) + len(playerB.getPack())    # Returns the value to the user
    
    maxVal = float("-inf")                                                                                          # Sets the value of maxVal
    direction = ""                                                                                                  # Sets the value of direction
    
    newGraph = deepcopy(graph)                                                                                      # Copies the contents into a new graph
    
    possibleSteps = ["N", "E", "S", "W"]                                                                            # Sets the value of possibleSteps
    
    for step in possibleSteps:                                                                                      # For each of the successors
        
                                                                                                                    #  It's player A's turn
        print(f"{depth}: ", end = "")
        print("\t" * depth, end = "")
        print(f"Going {step}")
        
        if whoseTurn == "A" and availableDirection(newGraph, playerA.getCoordinates()[0], playerA.getCoordinates()[1], step, playerB):
            
            x, y = playerA.getIndividualCoor()                                                                      # Sets the value of x and y
            
            x, y = updatedCoordinates(x, y, step)                                                                   # Call to method updatedCoordinates
            
            newPack = playerA.getPack()                                                                             # Copies the information into the newPack
            newBase = playerA.getBase()                                                                             # Copies the information into newBase            
            
            if (x, y) in availableResources and len(playerA.getPack()) < 2:                                         # We found a resource and have space to claim it
                
                newPack.append(newGraph[x][y][-1])                                                                  # Appends to the newPack
                availableResources.remove((x, y))                                                                   # Removes the tuple from resources                
                    
                newGraph[x][y] = newGraph[x][y][:-1] + "E"                                                          # Picks up the resource
            
            elif (x, y) == playerA.getBaseCoor():                                                                   # We arrived back at the base
                
                newBase += newPack                                                                                  # Adds the contents of the pack to the base
                newPack = list()                                                                                    # Creates an empty list for the pack
            
            
            newPlayerA = Node((x, y), newBase, playerA.getBaseCoor(), newPack)                                      # Creates an object of the Node classd
            
            tempVal = minValue(newPlayerA, playerB, availableResources, resourceCoordinates, "B", depth + 1, newGraph)
            
           
            if maxVal < tempVal:
                maxVal = tempVal
                direction = step
                
                 
            
        elif whoseTurn == "B" and availableDirection(newGraph, playerB.getCoordinates()[0], playerB.getCoordinates()[1], step, playerA):                                                                                                       # It's player B's turn
            
            x, y = playerB.getIndividualCoor()                                                                      # Sets the value of x and y
            
            x, y = updatedCoordinates(x, y, step)                                                                   # Call to method updatedCoordinates
            
            newPack = playerB.getPack()                                                                             # Copies the information into the newPack
            newBase = playerB.getBase()                                                                             # Copies the information into newBase            
            
            if (x, y) in availableResources and len(playerB.getPack()) < 2:                                         # We found a resource and have space to claim it
                
                newPack.append(newGraph[x][y][-1])                                                                  # Appends to the newPack
                
                availableResources.remove((x, y))                                                                   # Removes the tuple from resources                
                    
                newGraph[x][y] = newGraph[x][y][:-1] + "E"                                                          # Picks up the resource
                
            elif (x, y) == playerB.getBaseCoor():                                                                   # We arrived back at the base
                
                newBase += newPack                                                                                  # Adds the contents of the pack to the base
                newPack = list()                                                                                    # Creates an empty list for the pack
            
            
            newPlayerB = Node((x, y), newBase, playerB.getBaseCoor(), newPack)                                      # Creates an object of the Node classd
            
            tempVal = minValue(playerA, newPlayerB, availableResources, resourceCoordinates, "A", depth + 1, newGraph)
            
            if maxVal < tempVal:
                maxVal = tempVal
                direction = step
    
    return direction if depth == 0 else maxVal                                                                      # Returns the value to the user
    





# This is the method that will be used to help with determining the value of minimax. This will be the min function of the mini-max algorithm.
def minValue(playerA, playerB, availableResources, resourceCoordinates, whoseTurn, depth, graph):                   # Method Block 
    # For now the heuristic function will be the backpack + base resources - (opponents backpack + resources)
    if gameOver(playerA, playerB, resourceCoordinates) or depth == 3:                                               # If statement
        return len(playerA.getBase()) + len(playerA.getPack()) - len(playerB.getBase()) + len(playerB.getPack())    # Returns the value to the user
    
    minVal = float("inf")                                                                                           # Sets the value of minVal
    direction = ""                                                                                                  # Sets the value of direction
    
    newGraph = deepcopy(graph)                                                                                      # Copies the contents into a new graph
    
    possibleSteps = ["N", "E", "S", "W"]                                                                            # Sets the value of possibleSteps
    
    for step in possibleSteps:                                                                                      # For each of the successors
        
                                                                                                                    #  It's player A's turn
        print(f"{depth}: ", end = "")
        print("\t" * depth, end = "")
        print(f"Going {step}")
        
        if whoseTurn == "A" and availableDirection(newGraph, playerA.getCoordinates()[0], playerA.getCoordinates()[1], step, playerB):
            
            x, y = playerA.getIndividualCoor()                                                                      # Sets the value of x and y
            x, y = updatedCoordinates(x, y, step)                                                                   # Call to method updatedCoordinates
            
            newPack = playerA.getPack()                                                                             # Copies the information into the newPack
            newBase = playerA.getBase()                                                                             # Copies the information into newBase            
            
            if (x, y) in availableResources and len(playerA.getPack()) < 2:                                         # We found a resource and have space to claim it
                
                newPack.append(newGraph[x][y][-1])                                                                  # Appends to the newPack
                availableResources.remove((x, y))                                                                   # Removes the tuple from resources                
                    
                newGraph[x][y] = newGraph[x][y][:-1] + "E"                                                          # Picks up the resource
            
            elif (x, y) == playerA.getBaseCoor():                                                                   # We arrived back at the base
                
                newBase += newPack                                                                                  # Adds the contents of the pack to the base
                newPack = list()                                                                                    # Creates an empty list for the pack
            
            
            newPlayerA = Node((x, y), newBase, playerA.getBaseCoor(), newPack)                                      # Creates an object of the Node classd
            
            tempVal = maxValue(newPlayerA, playerB, availableResources, resourceCoordinates, "B", depth + 1, newGraph)
            
            
            if minVal > tempVal:
                minVal = tempVal
                direction = step
                print("What")
                
            
        elif whoseTurn == "B" and availableDirection(newGraph, playerB.getCoordinates()[0], playerB.getCoordinates()[1], step, playerA):                                                                                                       # It's player B's turn
        
            x, y = playerB.getIndividualCoor()                                                                      # Sets the value of x and y
            
            x, y = updatedCoordinates(x, y, step)                                                                   # Call to method updatedCoordinates
            
            newPack = playerB.getPack()                                                                             # Copies the information into the newPack
            newBase = playerB.getBase()                                                                             # Copies the information into newBase            
            
            if (x, y) in availableResources and len(playerB.getPack()) < 2:                                         # We found a resource and have space to claim it
                
                newPack.append(newGraph[x][y][-1])                                                                  # Appends to the newPack
                availableResources.remove((x, y))                                                                   # Removes the tuple from resources                
                    
                newGraph[x][y] = newGraph[x][y][:-1] + "E"                                                          # Picks up the resource
            
            elif (x, y) == playerB.getBaseCoor():                                                                   # We arrived back at the base
                
                newBase += newPack                                                                                  # Adds the contents of the pack to the base
                newPack = list()                                                                                    # Creates an empty list for the pack
            
            
            newPlayerB = Node((x, y), newBase, playerB.getBaseCoor(), newPack)                                      # Creates an object of the Node classd
            
            tempVal = maxValue(playerA, newPlayerB, availableResources, resourceCoordinates, "A", depth + 1, newGraph)
            
            if minVal > tempVal:
                minVal = tempVal
                direction = step
            
    
    return direction if depth == 0 else minVal                                                                      # Returns the value to the user



def main():
   
                                                                                                                    # VARIABLE DEFINITION
    LCV = 0                                                                                                         # Defines LCV
    arguments = sys.argv                                                                                            # Obtains the system arguments from the user 
   
    arguments = arguments[1:]                                                                                       # There should be at least two arguments passed in
   
    if len(arguments) < 1:                                                                                          # If an inappropriate number of arguments is entered
        raise Exception("Too few arguments entered! \nValid commands: \
                        \n\t\'python resourceAcquisitionGame.py {name of input graph}\' \
                        \n\t\'python resourceAcquisitionGame.py {name of input graph} {name of output graph}\'\n")  # Error message raised to the user
    elif len(arguments) > 2:                                                                                        # Too many arguments entered
        raise Exception("Too many arguments entered! \nValid commands: \
                        \n\t\'python resourceAcquisitionGame.py {name of input graph}\' \
                        \n\t\'python resourceAcquisitionGame.py {name of input graph} {name of output graph}\'\n")  # Error message raised to the user
    
    while LCV < len(arguments):                                                                                     # While Loop
        
        arguments[LCV] = endsInTxt(arguments[LCV])                                                                  # Updates the value of arguments at the index of LCV
        
        LCV += 1                                                                                                    # Updates the value of LCV
    
    if len(arguments) == 1:                                                                                         # If the user didn't specify an output file
        arguments.append(outputGenerator(arguments[0]))                                                             # Adds the output file name to the arguments
    
    graph = makeGraph(arguments)                                                                                    # Call to method makeGraph
    
    playTheGame(graph)                                                                                              # Call to method playTheGame
    #printList(graph)                                                                                                # Debug print statement
    
    
    


if __name__ == "__main__":
   
    try:
        main()
    except Exception as e:
       print(f"Error!: {e}")
    finally:
       print("The program is now done")
