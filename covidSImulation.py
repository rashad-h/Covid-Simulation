import matplotlib.pyplot as plt
import numpy as np
import random as rdm
import math

populationNumber =  1000  #int(input("Enter the Population..."))
numDays =  100  #int(input("Enter the number of days..."))
intInfected =  5  #int(input("Number of Initial infected people..."))
numInGatherings =  4  #int(input("Number of people in gatherings..."))
primaryChanceInfect = 0.1  #int(input("Chance of infection with a one to one ineraction(In percents)..."))
chance1 = 0.1
chance2 = 0.1
percentDifferent = chance2 - chance1
precentNotice = 0.025
chanceBadC = 0.5
chanceWorse = 0.01
chanceInfectCured = 0.09
mortalRate = 0.5
qurantine = True
chanceQuarintine = 0.9
testing = False
testAccuracy = 0.9
testSize = 20


helpMe = []

population = []
helpPop = []
gathering = []
preQuarintine = []
quarantined = []
yaxis = []
xaxis = []
badConditions = []
dead = []
alives = []
listOfIdentified = []
totalDeath = 0
neverInfected = 0

class Person():

    def __init__(self, ID):
        self.ID = ID + 1

    alive = True
    corona = False
    effective = False
    badC = False
    identified = False
    isCured = False
    tillId = 3
    tillResult = 12

    def cured(self):
        self.corona = False
        self.effective = False
        self.identified = False
        self.badC = False
        self.tillId = 3
        self.tillResult = 12
        self.isCured = True
        


    #Checking if they are known as an infected person/Day passes
    def doesKnow(self):
        if self.badC and (self.tillResult > self.tillId) and self.alive:           
            if self.tillId == 0:

                if qurantine:
                    if rdm.random() < chanceQuarintine:
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
def infect(person1, person2, chanceInfect):

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
def meet(lst, difference, warning):
    for x in lst:
        for y in lst:
            if (x != y) and (x.badC == False):


                if (warning):
                    if (difference < 0):
                        if (difference > -0.5):
                        
                            infect(x, y, ((difference/ (-0.5))* percentDifferent) + chance1)



                        else:
                            infect(x, y, chance2)

                    else:
                        infect(x, y, chance1)

                else:
                    infect(x, y, primaryChanceInfect)

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





    try:
        if((float(numCororna) / float(len(population))) > precentNotice):
            warning = True

        else:
            warning = False


    except:
        warning = False

    try:
        dailyDifference = ((float(listOfIdentified[days -1]) - float(listOfIdentified[days - 2])) / float(listOfIdentified[days - 2]))

    except:
        dailyDifference = 0

    numCororna = 0
    badPeople = 0

    for x in range(numGatherings):

        for m in range(numInGatherings):

            #print(len(population))
            y = rdm.randint(0, len(population) - 1)
            j = population[y]
            population.pop(y)
            gathering.append(j)
        
        #print(x)
        
        gathering = meet(gathering, dailyDifference, warning)
        helpPop = helpPop + gathering
        gathering[:] = []

    population = population + helpPop
    helpPop[:] = []

    deads = 0

    #checks
    if testing:
        try:
            for x in range(testSize):
                y = rdm.randint(0, testSize - 1)
                if population[y].corona and not population[y].identified:
                    if rdm.random() < testAccuracy:
                        population[y].identified = True

                

        except:
            pass



    #######
    for x in population:
        x.doesKnow()
        x.doesDie()
        if not x.alive:
            helpMe.append(x)
            deads = deads + 1
        
        else:
            if x.corona:
                numCororna = numCororna + 1
                if x.badC:
                    badPeople = badPeople + 1

            

            if x.identified:
                preQuarintine.append(x)
                helpMe.append(x)

        #corona => effective
            if x.corona and (not x.effective):
                x.effective = True


    for x in helpMe:
        population.remove(x)

    helpMe[:] = []


    #######

    for x in quarantined:
        x.doesKnow()
        x.doesDie()
        if (x.alive == False):
            helpMe.append(x)
            deads = deads + 1        
        else:
            if x.corona:
                numCororna = numCororna + 1
                if x.badC:
                    badPeople = badPeople + 1

                    

            else:
                population.append(x)
                helpMe.append(x)
        
    for x in helpMe:
        quarantined.remove(x)
    
    helpMe[:] = []





    listOfIdentified.append(int(len(preQuarintine)))
    ########
    quarantined = quarantined + preQuarintine
    preQuarintine[:] = []


    ########





    #######





    ######
    #gathering data
    yaxis.append(numCororna)
    badConditions.append(badPeople)
    xaxis.append(days)
    dead.append(deads)   

    for x in dead:
        totalDeath = totalDeath + x
    
    alives.append(populationNumber - totalDeath)
    totalDeath = 0



    ######s
    #A day passes
    
    print("End of day " + str(days + 1))



for x in population:
    if x.isCured == False:
        neverInfected = neverInfected + 1


for x in dead:
    totalDeath = totalDeath + x
print(populationNumber)
print("Dead : " + str(totalDeath) +"   "+ str((float(totalDeath)/ float(populationNumber))*100) + "%")
print("Never Infected : " + str(neverInfected) +"   "+ str((float(neverInfected)/ float(populationNumber))*100) + "%")


#######
#Calculating Variance
# x = xaxis , f = badConditions


multiples = []
for x in xaxis:
    multiples.append(x * badConditions[x])

sumOfMultiples = sum(multiples)

mean = float(sumOfMultiples) / float(sum(badConditions)) 

listOfSpecial = []
for x in xaxis:
    value = ((x - mean) * (x - mean))
    listOfSpecial.append(value * badConditions[x])

variance = float(sum(listOfSpecial)) / float(sum(badConditions))


print("Variance : " + str(variance)) + "    Max : " + str(max(badConditions))

########
#plotting

plt.subplot(211)

plt.xlabel("Days")
plt.ylabel("Infected")
plt.title("Virus Spreading")
#plt.bar(xaxis, alives, width=1, color="green", label = "Alive")
plt.bar(xaxis, yaxis, width=1, color="yellow", label = "Infected")
plt.bar(xaxis, badConditions, width=1, color="orange", label = "Critical Condition")

plt.bar(xaxis, dead, width = 1, color = 'red', label = "Dead")
plt.grid(True)
plt.legend()
plt.xlim([0, numDays + 1]);

plt.subplot(212)
plt.xlabel("Days")
plt.bar(xaxis, listOfIdentified, width=1, color="gray", label = "Identified Daily")
plt.bar(xaxis, dead, width = 1, color = 'red', label = "Dead")

plt.xlim([0, numDays +1]);

plt.grid(True)
plt.legend()
plt.show()

