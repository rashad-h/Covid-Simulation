import matplotlib.pyplot as plt
import numpy as np
import random as rdm
import math

populationNumber = int(input("Enter the Population..."))
numDays = int(input("Enter the number of days..."))
intInfected = int(input("Number of Initial infected people..."))
numInGatherings = int(input("Number of people in gatherings..."))
chanceInfect = 0.1  #int(input("Chance of infection with a one to one ineraction(In percents)..."))
chanceBadC = 0.8
chanceWorse = 0.1
chanceInfectCured = 0.1
mortalRate = 0.2
#testAccuracy = 0.7


population = []
helpPop = []
gathering = []
yaxis = []
xaxis = []
dead = 0

class Person():

    def __init__(self, ID):
        self.ID = ID + 1

    alive = True
    corona = False
    effective = False
    badC = False
    identified = False
    isCured = False
    tillId = 2
    tillResult = 12

    def cured(self):
        self.corona = False
        self.effective = False
        self.badC = False
        self.tillId = 2
        self.tillResult = 12
        self.isCured = True
        


    #Checking if they are known as an infected person/Day passes
    def doesKnow(self):
        if self.badC and (self.tillResult > self.tillId) and self.alive:           
            if self.tillId == 0:
                self.identified = True
                self.tillResult = self.tillResult - 1
            else:
                self.tillId = self.tillId - 1
                self.tillResult = self.tillResult - 1
        
        elif self.corona and not self.badC:
            self.tillResult = self.tillResult - 1

    #Checking to see what happens after the 12 days
    def doesDie(self):
        if self.tillResult == 0:
            if self.badC:
                if rdm.random() < mortalRate:
                    self.alive = False
                else:
                    self.cured()
                    
            else:
                self.cured()



#######
#Interacting with another person
def infect(person1, person2):

    if person2.effective == True:

        if (person1.corona == False):


            if (person1.isCured):

                if rdm.random() < chanceInfectCured:

                    if rdm.random() < chanceInfect:
                        person1.corona = True      
                        #Chance of having a bad infection
                        if rdm.random() < chanceBadC:
                            person1.badC = True                

            else:
                if rdm.random() < chanceInfect:
                    person1.corona = True      
                    #Chance of having a bad infection
                    if rdm.random() < chanceBadC:
                        person1.badC = True

        elif (person1.corona) and (person1.badC == False):
            if rdm.random() < chanceWorse:
                person1.badC = True

#######
#mettings in gatherings
def meet(lst):
    for x in lst:
        for y in lst:
            if (x != y) and (x.badC == False):
                infect(x, y)
    return lst

        
#######
#making a list of people

for x in range(populationNumber):
    population.append(Person(x))

#######
#rasndomly chossing infected people
for x in range(intInfected):

    z = rdm.randint(0, populationNumber - 1)
    while population[z].corona == True:
            z = rdm.randint(0, populationNumber - 1)
    population[z].corona = True


#####
#calculating number of gatherings per day

numGatherings = int(math.floor(populationNumber/numInGatherings))

#######
#Interactions happen


##############################

for days in range(numDays):

    numGatherings = int(math.floor(len(population)/numInGatherings))

    if population < numInGatherings:
        print("The whole population is dead")
        break


    numCororna = 0

    for x in range(numGatherings):

        for m in range(numInGatherings):

            #print(len(population))
            y = rdm.randint(0, len(population) - 1)
            j = population[y]
            population.pop(y)
            gathering.append(j)
        
        #print(x)
        
        gathering = meet(gathering)
        helpPop = helpPop + gathering
        gathering[:] = []

    population = population + helpPop
    helpPop[:] = []

    #######
    #Checks
    for x in population:
        x.doesKnow()
        x.doesDie()
        if not x.alive:
            population.remove(x)
            dead = dead + 1

        if x.corona:
            numCororna = numCororna + 1


        #corona => effective
        if x.corona and (not x.effective):
            x.effective = True

    ######
    #gathering data
    yaxis.append(numCororna)
    xaxis.append(days + 1)

    ######s
    #A day passes
    print("End of day " + str(days + 1))
    print("Dead : " + str(dead))

plt.xlabel("Days")
plt.ylabel("Infected")
plt.title("Virus Spreading")
plt.plot(xaxis, yaxis, 'bs')
plt.grid(True)
plt.show()


for x in population:
    print(x.isCured, x.effective)

