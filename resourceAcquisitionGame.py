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

import sys
from copy import deepcopy

class Node:
    
    def __init__(self, coordinate, base, baseCoor, pack):
        self.__coordinate = coordinate
        self.__baseCoor = baseCoor
        self.__baseStats = deepcopy(base)
        self.__backpack = deepcopy(pack)
        
    def getCoordinates(self):
        return self.__coordinate

    def getIndividualCoor(self):
        return self.__coordinate[0], self.__coordinate[1]

    def getBaseCoor(self):
        return self.__baseCoor
    
    def getBase(self):
        return deepcopy(self.__baseStats)
        
    def getPack(self):
        return deepcopy(self.__backpack)
        
        
    def __str__(self):
        
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
def playTheGame(graph, onePlayer = True):                                                                                             # Method Block
    
                                                                                                                    # VARIABLE DEFINITIONS
    turn = "A"                                                                                                      # Sets the value of turn
    playerA = Node((0, 0), (0, 0), list(), list())                                                                  # Creates the default position for playerA
    playerB = Node((len(graph) - 1, len(graph[0]) - 1), (len(graph) - 1, len(graph[0]) - 1), list(), list())        # Creates the default position for playerB
    
    resourceCoordinates = []                                                                                        # Defines resourceCoordinates
    nextMove = []
    
    for i in range(len(graph)):                                                                                     # For Loop
        for j in range(len(graph[i])):                                                                              # Nested For Loop
            
            if graph[i][j][-1] in ['S', 'I', 'C']:                                                                  # If the coordinate has a resource, then add it to the list
                resourceCoordinates.append((i, j))                                                                  # Appends to resourceCoordinates
                
                
    openingMove = (playerA, playerB, resourceCoordinates, turn)                                                     # Defines openingMove
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
            
            pass
            
            
            #break
        
        
        # This player making the move is player A
        if whoseTurn == "A":                                                                                        # It's player A who is moving
            
            x, y = playerA.getIndividualCoor()                                                                      # Sets the value of x and y
            
            match userInput:                                                                                        # Match case
                
                case "E":                                                                                           # In the case of East
                    y += 1                                                                                          # Adds to the value of y

                case "S":                                                                                           # In the case of South
                    x += 1                                                                                          # Adds to the value of x
                
                case "W":                                                                                           # In the case of West
                    y -= 1                                                                                          # Subtracts from the value of y
                    
                case "N":                                                                                           # In the case of North
                    x -=1                                                                                           # Subtracts from the value of x
                
            if (x, y) in resources and len(playerA.getPack()) < 2:                                                  # We found a resource and have space to claim it
                newPack = playerA.getPack()                                                                         # Copies the information into the newPack
                newBase = playerA.getBase()                                                                         # Copies the information into newBase
                newPack.append(graph[x][y][-1])                                                                     # Appends to the newPack
                
                graph[x][y] = graph[x][y][:-1] + "E"                                                                # Picks up the resource
            
            elif (x, y) == playerA.getBaseCoor():                                                                   # We arrived back at the base
                
                newPack = playerA.getPack()                                                                         # Copies the information into the newPack
                newBase = playerA.getBase()                                                                         # Copies the information into newBase
                
                newBase += newPack                                                                                  # Adds the contents of the pack to the base
                newPack = list()                                                                                    # Creates an empty list for the pack
                
            
            
            
            
        else:
            
            break
        
                
                #playerA, playerB, resources, whoseTurn = nextMove.pop()                                                     # Pops the information from the list

        
        # if we are doing a game with the computer making the turn we want to have
            # either the random state, minimax, alpha beta pruning agent
        # compute which direction to go and then take that action.
        
        
        
        
        
# This is the method that will be used to determine whether or not the user can go in a specific direction
def availableDirection(graph, xCoor, yCoor, direction, playerB):                                                             # Method Block
     
    match direction:                                                                                                # Match case
        
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
