import random # To randomize the probability of a tree spawning instead of a pond
import matplotlib.pyplot as plt # For plotting our grid of colors
import matplotlib.colors as colors # To map colors onto our grid
import time # To sleep the program to keep final image up longer

# Generate the forest based on tree density, returns the generated forest and the breadth and length of the forest
def GenerateForest(sizeX, sizeY, treeDensity):
    treeCount = 0 # Counts number of trees in the forest to see if density is reached
    forestArea = sizeX * sizeY # Get the area of the forest
    numberOfTrees = int(forestArea * treeDensity) # Get number of trees needed to reach the required forest density

    generatedForest = [[0]*sizeX for i in range(sizeY)] # Create an empty 2D array with the forest's specified dimensions

    # Set up a loop to keep spawning trees randomly until the required tree density has been met
    while (treeCount < numberOfTrees):
        # Loop through a 2D array(list) of elements to spawn either a tree or a pond randomly
        # We start with y axis first since it's the rows of the 2D array
        # Then, we do a for loop within this to loop through the columns of the 2D array representing the forest
        for y in range(sizeY):
            for x in range(sizeX):
                if (random.random() <= treeDensity):  # Note that the random determinant is based on the tree density required (e.g. 0.2 chance of spawning a tree)
                    # If randomnized number between 0-1 falls within the tree density range, we spawn a tree. If not, we spawn a pond.
                    # We set the element of the 2D array by calling the coordinates [row][column] aka [y][x]
                    generatedForest[y][x] = 1 # We use 1 for tree, 0 for pond
                    treeCount += 1
                    
                    # If we exceed the number of trees then we stop spawning (since tree density has been met)
                    if (treeCount >= numberOfTrees):
                        break
    
    # Returns the forest 2D array along with its length and breadth for further use
    # Note that we return an array (list). So to manipulate this, we need to call blah[0] for the 2D array, blah[1] for sizeX etc.
    return([generatedForest, sizeX, sizeY]) 

# This function displays the forest by reading the 2D array and generating a grid of colored squares
# 0 maps to pond (blue), 1 maps to tree (green), 2 maps to spreadable fires (red), 3 maps to ashes (black), 4 maps to newly spread fires (red) (see below comments for more info)
def DisplayForest(forestToDisplay):

    # Clear any previous plots
    plt.clf()

    # Create a color map that maps array values to colors (0: water, 1: tree, 2: fire, 3: ash)
    colorMap = colors.ListedColormap(["royalblue", "green", "red", "black"])
    # Set the bounds of the color map to make it discrete values instead of a gradient
    bounds = [0, 1, 2, 3, 4] # Aka 0 = royalblue, 1 = green and so on. 4 is just an arbitrary filler number.
    norm = colors.BoundaryNorm(bounds, colorMap.N)

    # Create a plot using the 2D forest array as a base and map it to the color map with normalized bounds
    plt.imshow(forestToDisplay[0], cmap = colorMap, norm = norm)
    plt.axis('off') #Remove the axes of the plotted graph so only colored squares are displayed
    plt.pause(0.05) # Delay between each redraw of the image (basically delay between refreshing the display)

# Start forest fire
def StartForestFire(forestToBurn):
    #Start the fire in the middle
    middleX = forestToBurn[1] // 2
    middleY = forestToBurn[2] // 2
    forestToBurn[0][middleY][middleX] = 2 # Set fire to be the value 2, start in middle of 2D array

    burning = True # While fire is still burning, keep looping to start new fires

    # Create a 2D array of same size to store which forest tiles started new fires
    # False = Did not start new fire this loop, True = Started a new fire this loop
    # When all tiles did not start new fires, the loop can end (stop attempting to spread forest fires)
    newFireCheck = [[False]*forestToBurn[1] for i in range(forestToBurn[2])]

    # Start burning algorithm
    while burning:
        # We check each tile in the forest for each loop, loop through the rows, then loop through the columns
        # Recall that forestToBurn[1] = sizeX and forestToBurn[2] = sizeY
        # And recall that sizeY = number of rows, and sizeX = number of columns
        for row in range(0, forestToBurn[2]):
            for column in range(0, forestToBurn[1]):

                newFire = False # First, we assume this tile did not start a new fire this loop

                # If this tile was a fire started in the previous loop, in this loop, it attempts to spread new fires
                if (forestToBurn[0][row][column] == 2):

                    # Check up down left right to see if there's a tree. If it's a tree, spread new fire to it
                    # If the fire on this tile was spread to this tile by another tile on this turn, do NOT spread this fire during this loop iteration
                    # We use 4 for new fire on this turn, only for fires AFTER us. We ignore fires BEFORE us because they will be dealt with on the next loop. 
                    # New fires DO NOT spread on this turn. Only OLD fires (from the previous loop) will spread.

                    # Check up
                    if (row-1 >= 0): # Check if index in range (within the forest area bounds)
                        if (forestToBurn[0][row-1][column] == 1):
                            forestToBurn[0][row-1][column] = 2
                            newFire = True # If we spread a fire, we record that this tile spread a new fire this loop
                            # This means that we cannot end the fire spreading loop yet since we need to check again for new fire spreading possibilities

                    # Check right
                    if (column+1 < forestToBurn[1]): #Check if index in range
                        if (forestToBurn[0][row][column+1] == 1):
                            forestToBurn[0][row][column+1] = 4
                            newFire = True

                    # Check down
                    if (row+1 < forestToBurn[2]): #Check if index in range
                        if (forestToBurn[0][row+1][column] == 1):
                            forestToBurn[0][row+1][column] = 4
                            newFire = True

                    # Check left
                    if (column-1 >= 0): #Check if index in range
                        if (forestToBurn[0][row][column-1] == 1):
                            forestToBurn[0][row][column-1] = 2
                            newFire = True

                    # Since this tile was burning the last turn, this turn, make it ashes
                    forestToBurn[0][row][column] = 3

                # If this fire is a new fire, aka another tile spread to this tile on this loop iteration
                # We change it to a normal fire so the loop after this iteration recognizes it as a spreadable fire
                # This also ensures that we display the tile on fire as red
                elif (forestToBurn[0][row][column] == 4): 
                    forestToBurn[0][row][column] = 2

                # We now store whether this tile spread a new fire on this loop iteration in our fireCheck array.
                # We will store FALSE if this tile did NOT spread a new fire this turn.
                # We will store TRUE if this tile spread a new fire this turn.
                # When ALL tiles stored FALSE, that means there are no more trees that we can spread fires to, and the program ends.
                newFireCheck[row][column] = newFire
        
        # If no tiles started a new fire this loop, no more fire spread. Stop loop.
        if not any(True in col for col in newFireCheck): 
            burning = False

        DisplayForest(forestToBurn) # Displays the forest fire spread as each loop completes

    time.sleep(5) # Keeps the final burnt forest image up for 5 seconds
    return(forestToBurn) # Returns the burnt forest (we don't actually need this)

# ================== MAIN PROGRAM ===================== #

# Generate the forest
forest = GenerateForest(100, 95, 0.7)
StartForestFire(forest)

