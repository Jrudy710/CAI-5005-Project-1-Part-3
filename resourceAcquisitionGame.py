class Node:
    
    def __init__(self, coordinate, resourcesLeft, base, pack, steps):
        self.__coordinate = coordinate
        self.__baseStats = deepcopy(base)
        self.__backpack = deepcopy(pack)
        self.__directions = steps
        self.__leftToCollect = deepcopy(resourcesLeft)
        
    def getCoordinates(self):
        return self.__coordinate

    def getBase(self):
        return deepcopy(self.__baseStats)
        
    def getPack(self):
        return self.__backpack
        
    def getDirections(self):
        return self.__directions

    def addDirections(self, extraStep):
        self.__directions += extraStep

    def getAvailableResources(self):
        return self.__leftToCollect

    def emptyPack(self):
        
        self.addDirections("DEPOSITING-RESOURCES-AT-BASE-")
        for i in self.__backpack:
            self.addDirections(f"{i}-")
            self.__baseStats[i] += 1
        self.addDirections(f" ")
        
        self.__backpack = []
        
    def allResourcesDelivered(self):
        
        for resource in self.__baseStats.keys():
            if self.__baseStats[resource] != endGame[resource]:
                return False
            
        return True
        
    
    def __str__(self):
        
        return f"At {self.__coordinate} with the following items in the pack: \n\t{self.__backpack}\n\tAt base: {self.__baseStats} \n\tthis many resources left to go: {self.__leftToCollect}\n\tsteps taken: {self.__directions}"
    

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

    #printList(graph)                                                                                                # Debug print statement
    return graph                                                                                                    # Returns the filled graph to the user
    
    
    
       
       
# This will be the method that will be used to determine the path cost up to that point. 
# It will be passed the sequence of steps taken to get to a point and then the program will 
# return the integer value obtained, which will be a combination of the heuristic values at 
# each index/step taken and the sum will be returned to the user.
def pathCostDetermination(steps, graph) -> int:
    
                                                                                                                    # VARIABLE DEFINITIONS
    row = 0                                                                                                         # Defines row
    column = 0                                                                                                      # Defines column
    pathCost = 0                                                                                                    # Defines pathCost
    
    steps = steps.split()                                                                                           # Redefines steps
    #print(steps)
    for i in steps:                                                                                                 # Loops through the steps
        rowInc = colInc = 0                                                                                         # Defines rowInc and colInc
        
        match i:                                                                                                    # Match case
            case 'N':                                                                                               # Case of going north
                rowInc = -1                                                                                         # Sets the value of rowInc
            case 'E':                                                                                               # Case of going east
                colInc = 1                                                                                          # Sets the value of colInc
            case 'S':                                                                                               # Case of going south
                rowInc = 1                                                                                          # Sets the value of rowInc
            case 'W':                                                                                               # Case of going west
                colInc = -1                                                                                         # Sets the value of colInc
            case _:                                                                                                 # Default statement
                continue                                                                                            # Continues on to the next iteration
        
        row += rowInc                                                                                               # Adds to the value of row
        column += colInc                                                                                            # Adds to the value of column
        
        pathCost += determineHeuristicTraversal(graph[row][column])                                                 # Adds to the value of pathCost
    return pathCost                                                                                                 # Returns pathCost to the user
        
    
  
# This is the method that will be used to return the heuristic value, steps taken given the terrain of a given coordinate
# base = 1
# grassland = 1
# hills = 2
# swamp = 3
# mountain = 4
def determineHeuristicTraversal(value: str()):
    
    match value[0]:
        case 'B':
            return 1
        case 'G':
            return 1
        case 'H':
            return 2
        case 'S':
            return 3
        case 'M':
            return 4
        case _:
            raise Exception("Unknown terrain on the map")
    
    
    
    
# The following function is a helper method that will return the last element 
# in a given tuple that is passed in to theFrontier
def lastElem(elem):
    return elem[-1]
    
    
    
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
def printList(table):
    
    for row in table:                                                                                               # For Loop
        for col in row:                                                                                             # Nested For Loop
            print(f"{col:^5s}", end = "")                                                                           # Prints out to the user
        print()                                                                                                     # Prints a blank line to the user
    


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
    
    #print(arguments)                                                                                                # Debug print statement
    graph = makeGraph(arguments)                                                                                    # Call to method makeGraph
    findThePath(arguments, graph)                                                                                   # Call to method findThePath
        
    


if __name__ == "__main__":
   
    try:
        main()
    except Exception as e:
       print(f"Error!: {e}")
    finally:
       print("The program is now done")
