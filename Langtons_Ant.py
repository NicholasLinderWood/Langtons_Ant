'''This file contains three class definitions:

-------------------------------------------------------------------------------------------------------------------------------------------

    1.) Ant - The Ant class represents an ant on the grid. Ants have two attributes:

            -Orientation - A single character string ('N', 'E', 'S', 'W') indicating
                the direction the ant is facing.

            -Loc - A list of two integers storing the [row, column] location of the ant.

        Ants have three methods:

            -Turn - Makes the ant turn 90 degrees clockwise or counterclockwise depending
                on the state of the grid at its location and the given rulestring.

            -Paint - Makes the ant update the state of the square he is currently on based
                on the given rulestring.

            -Move - Moves the ant forward one square based on his location and orientation.
                Periodic boundary conditions are used to ensure the ant always stays on the grid.

-------------------------------------------------------------------------------------------------------------------------------------------

    2.) Colony - The Colony class represents the ants who live on the grid and move according
                to a given set of rules. Colonies have three attributes:

            -N - An integer which creates an NxN matrix, initially of all zeros. The location
                of the ants should have row and column locations between 0 and N-1

            -Rules - A string of 1's and 0's indicating which fully describes the rules by which
                    the ants move along the grid. (https://www.researchgate.net/publication/250803538_The_Ultimate_in_Anty-Particles)

        Colonies have two methods:

            -Add_Ant - Add an ant to the colony. Can specify the location and orientation of the ant,
                    otherwise they are randomly selected.

            -Update_Colony - Updates the colony by turning each ant, painting its square, then moving it.

-------------------------------------------------------------------------------------------------------------------------------------------

    3.) Langtons_Ant - The Langtons_Ant class will run the animation of Langtons Ant and has 2 attributes:

            -colony - A Colony object defined above

            -colors - A list of colors. There should be a number of colors in this list equal to the
                length of the rulestring given by Rules in the Colony.

-------------------------------------------------------------------------------------------------------------------------------------------

    Running this script will run the original Langton's Ant. Other example scripts will be provided that will show variants
    of Langton's Ant using multiple ants and different rules.
            

    Created By: Nicholas L. Wood, PhD
    Date Created: 03/10/2020
    Date Modified: 03/12/2020
'''
from random import randint
from matplotlib import cm as cm
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.colors import ListedColormap
import numpy as np

class Ant:

    def __init__(self, Orientation, row, column):
        '''Orientation is a single character string in 'NESW', row and column are integers
            indicating the coordinates of the ant on the grid.'''

        #Ensure the Orientation is uppercase
        Orientation = Orientation.upper()

        self.Orientation = Orientation
        self.Loc = [row, column]

    def Turn(self, Grid, Rules):
        '''Turns the Ant on the Grid according to the Rules rulestring.'''

        Orientation = self.Orientation

        #If the Ant is on a square whose state is 0 (in the rulestring), turn 90 degrees clockwise
        #If the Ant is on a square whose state is 1 (in the rulestring), turn 90 degrees counterclockwise
        TurnDicts = [{'N':'W','W':'S','S':'E','E':'N'},{'N':'E','E':'S','S':'W','W':'N'}]

        row, col = self.Loc[0], self.Loc[1]

        #Determine the state of the Grid at the Ants location (should be in [0, 1, 2, ..., len(Rules) - 1]
        State = int(Grid[row, col])

        #Determine if the state of the grid location for the Ant corresponds to a 1 or 0 in the rulestring
        RuleState = int(Rules[State])

        #Update the orientation of the Ant
        self.Orientation = TurnDicts[RuleState][Orientation]

    def Paint(self, Grid, Rules):
        '''The Ant paints his location on the grid a color according to the rulestring.
            i.e. he changes the state of the square he is on to the next state.'''

        #Get the coordinates of the ant
        row, col = self.Loc[0], self.Loc[1]

        #Increase the value of the ants location on the grid by 1
        Grid[row, col] += 1

        #If the value of the ants location is equal to the len of the rulestring,
        #set it back to zero
        if Grid[row, col] == len(Rules):
            Grid[row, col] = 0


    def Move(self, Grid):
        '''Move the ant one square forward based on his orientation.'''

        #Get the orientation of the ant
        Orientation = self.Orientation

        #Define two dictionaries. The first tells us whether it is the row or the
        #column value is changed (note that when an ant moves either the row or the column
        #changes and the other stays the same). The second tells us whether we increase or
        #decrease that value by 1
        index_dict = {'N':0,'S':0,'E':1,'W':1}
        delta_dict = {'N':1,'S':-1,'E':1,'W':-1}

        #Is it the row (0) or column (1) which is changing?
        i = index_dict[Orientation]

        #Do we increase or decrease by 1?
        delta = delta_dict[Orientation]

        #Update the location!
        self.Loc[i] += delta

        #Adjust for periodic boundary conditions
        #Determine the number of rows/columns (the grid is a square)
        N = np.size(Grid, 0)

        if self.Loc[i] < 0:
            self.Loc[i] = N - 1

        elif self.Loc[i] == N:
            self.Loc[i] = 0


class Colony:

    def __init__(self, N = 100, Rules = '10'):
        '''N is an integer indicating the NxN grid upon which the Ants live.
        Rules is a rulestring of 1's and 0's totally defining how an Ant moves.
        The grid will always initially be all zeros.

        The default Rules of '10' is the original Langtons Ant.'''

        #Define the Grid
        self.Grid = np.zeros((N, N))

        #Store the rulestring
        self.Rules = Rules

        #Create an empty list which will store the ants in the colony
        self.Ants = []

        #Store the number of times the colony has been updated
        self.iter = 0

    def Add_Ant(self, Orientation = None, row = None, col = None):
        '''Add the ant with the given orientation, row and column location. If none
            are given, then an ant with a randomly chosen orientation, row, and column
            is added.'''

        #Determine the size of the grid in case the row and column are not specified
        N = np.size(self.Grid, 0)

        if row == None:
            #Randomly chose a row
            row = randint(0, N-1)

        if  col == None:
            #Randomly chose a column
            col = randint(0, N-1)

        if Orientation == None:
            #Randomly chose an orientation
            directions = 'NESW'
            Orientation = directions[randint(0, 3)]

        #Add the ant to the list of ants
        self.Ants.append(Ant(Orientation, row, col))

    def Update_Colony(self):
        '''Do the following for each ant simultaneously (ants on the same square will each update a square):

            Turn
            Paint the Square
            Move
        '''

        self.iter += 1

        #Grab the grid and the rulestring
        Grid = self.Grid
        Rules = self.Rules

        #Turn the ants
        for ant in self.Ants:
            ant.Turn(Grid, Rules)

        #Have the ants paint the grid
        for ant in self.Ants:
            ant.Paint(Grid, Rules)

        #Have the ants move
        for ant in self.Ants:
            ant.Move(Grid)

        



class Langtons_Ant:

    def __init__(self, colony, colors):
        '''The Langton's Ant Class! This will be used for animation.'''

        #The colony on which the ants live
        self.colony = colony

        #A list of colors (in RGB format)
        #should be the same as the len of the rulestring 
        self.colors = colors

        #The number of iterations it has been running
        self.iter = 0


    def Run(self):
        '''Runs the Langton's Ant Cellular Automata'''

        plt.style.use('dark_background')

        #Generate the figure
        fig = plt.figure()
        ax = fig.add_subplot(111)

       

        #The title will report the number of iterations
        titleobj = ax.set_title(str(self.colony.iter), fontsize = 30)

        #Make the title blue in color
        plt.setp(titleobj, color = [0,0,1])

        #That layout is tight!
        plt.tight_layout()

        #We don't need no stinkin axis!       
        ax.axis('off')

        #The colormap used
        cmap = ListedColormap(self.colors)

        def func(frame):
            
            #Update the colony
            self.colony.Update_Colony()

            #Grab the updated Grid
            Grid = self.colony.Grid

            #Increase the number of iterations by 1
            self.iter += 1

            #Set the matrix data
            mat.set_data(Grid)
            ax.set_title(str(self.colony.iter), fontsize = 30)

        mat = ax.matshow(self.colony.Grid, cmap = cmap, vmin = 0, vmax = len(self.colors)-1)
        ani = animation.FuncAnimation(fig, func, interval = 10, repeat = False)

        plt.show()

    def Show(self, Rule):
        '''Return the fig object with Langtons Ant for the purposes of saving the figure'''

        plt.style.use('dark_background')

        #Generate the figure
        fig = plt.figure(figsize = (16, 9))
        ax = fig.add_subplot(111)

        #The title will display the rule
        titleobj = ax.set_title(str(Rule), fontsize = 30)

        #Make the title blue in color
        plt.setp(titleobj, color = [0,0,1])

        #That layout is tight!
        plt.tight_layout()

        #We don't need no stinkin axis!       
        ax.axis('off')

        #The colormap used
        cmap = ListedColormap(self.colors)

        mat = ax.matshow(self.colony.Grid, cmap = cmap, vmin = 0, vmax = len(self.colors)-1)

        return fig


        
    
        

if __name__ == '__main__':

    #Let's do the original Langtons Ant

    #Create a 101x101 Grid
    N = 101

    #The rules for the original Langtons Ant are coded by '10'
    Rules = '10'

    #Set 0 -> White and 1 -> Black
    colors = [[1, 1, 1], [0, 0, 0]]

    #Create the colony
    colony = Colony(N, Rules)

    #Create a single ant in the center of the Grid facing east
    #and add him to the colony
    Orientation = 'E'
    row = 50
    col = 50
    colony.Add_Ant(Orientation, row, col)

    #Create Langtons Ant
    langtons_ant = Langtons_Ant(colony, colors)

    #Run it!
    langtons_ant.Run()











        
