import numpy as np
import math

np.set_printoptions(precision = 4, suppress=True)
pi = math.pi

def Copper(LengthStep, TimeStep, alpha, TotalLength):
    numberOfLengthSteps = int(TotalLength/LengthStep)+1
    storageArray5 = np.zeros((2,numberOfLengthSteps))
    storageArray5[0] = [0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0]
    CountChocula = 0
    WhereIveBeen = 0
    WhereImGoing = 1
    HowManySteps = 0
    timetracker3 = [0]
    everyHundred=np.empty([2,11], dtype = float)

    while storageArray5[0, 5] >= 20:
        for j in range(1, numberOfLengthSteps-1):
            storageArray5[ WhereImGoing,j] = (TimeStep*(alpha*((storageArray5[WhereIveBeen,j+1]-(2*storageArray5[WhereIveBeen,j])+storageArray5[ WhereIveBeen,j-1])/(LengthStep**2))))+ storageArray5[WhereIveBeen,j]
        # if CountChocula >= 0:
        storageArray5[WhereIveBeen] = storageArray5[WhereImGoing]

        CountChocula += 1


        time= HowManySteps*TimeStep
        if time % 20== 0 and CountChocula > 1:
            newRow = storageArray5[WhereImGoing,:]
            print(everyHundred)
            everyHundred = np.vstack((everyHundred, newRow))
            print(everyHundred)
            #print("_______________________________________________hfhfhfhfhfhfhfh_______________")
            #print(HowManySteps)
            timetracker3.append(time)
        HowManySteps += 1

    print(CountChocula * TimeStep)
    timetracker3.append(time)

    print(everyHundred)

    initialRow = [ 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0]

    CopperEvery1000= np.column_stack((timetracker3, everyHundred))
    arraytoSave = np.vstack((initialRow, CopperEvery1000))


    np.savetxt('Coppereverytwohundred.txt', arraytoSave, fmt = '%1.4f', delimiter=",", comments = '', newline='\r\n')
    # for i in range(xSteps):
        # print ("Yo")
    return storageArray5

def main():
    alphaCopper = 0.386 / (8960 * 0.38)
    Test5b = Copper(0.1, .001, alphaCopper, 1)

main()