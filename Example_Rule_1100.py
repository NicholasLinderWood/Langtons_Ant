'''A second example using my Langton's Ant code. This file will run the Langton's Ant
    with the rulestring 1100 and a single ant.

    
    Created By: Nicholas L. Wood, PhD
    Date Created: 03/12/2020
    Date Modified: 03/12/2020
'''

from Langtons_Ant import Colony, Langtons_Ant

#Create a 101x101 grid
N = 101

#Chose the rulestring
Rules = '1100'

#Select the colors: 0 -> White and 1 -> Black
colors = [[1,1,1], [0,0.33,0], [0,0.67,0], [0,1,0]]

colony = Colony(N, Rules)

#Now add some very specific ants to the colony
colony.Add_Ant('E', 50, 50)


#Create the simulation
langtons_ant = Langtons_Ant(colony, colors)

#Run the simulation
langtons_ant.Run()
