#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 16:38:33 2019

@author: Erebus
"""


#Bailey McFarland
#sixth Assignment for Dr.Taylors Biological Modeling Class
#Started 2019-09-28
#Fun Fact 6: Octopuses can taste with their arms.

import numpy as np
import os
import math
np.set_printoptions(precision = 4, suppress=True)
pi = math.pi

file = open('twoRowLoop.txt', 'wb')
file.write('Two Row Loop \r\n'.encode())


def Explicit_Finite_Difference(LengthStep, TimeStep, alpha, TotalLength, TotalTime ):
    numberOfTimeSteps = int(TotalTime/TimeStep)+1
    numberOfLengthSteps = int(TotalLength/LengthStep)+1

    storageArray = np.zeros((numberOfTimeSteps,numberOfLengthSteps))
    timeTracker = []
    TimeTime = 0
    for i in range(len(storageArray)):
        for j in range(1, numberOfLengthSteps-1):
            if i == 0:
                if 0<= j and j <= 5:
                    storageArray[i,j] = 2*j*LengthStep
                elif j > 5:
                    x= LengthStep*j
                    storageArray[i,j] = 2*(1-x)
            else:
                storageArray[i,j] = (TimeStep*(alpha*((storageArray[i-1,j+1]-(2*storageArray[i-1,j])+storageArray[i-1,j-1])/(LengthStep**2))))+ storageArray[i-1,j]


    for k in range(0,21,1):
        timeTracker.append(round(TimeTime, 5))
        TimeTime += .001

    TimeandHeat = np.column_stack((timeTracker, storageArray))
    np.savetxt('IterativeRod.txt', TimeandHeat, fmt = '%1.4f', delimiter=",", comments = '', newline='\r\n')
    # print(timeTracker)
    # print(storageArray)

    # for i in range(xSteps):
        # print ("Yo")
    return storageArray

def AnalyticalSolution(LengthStep, TimeStep, alpha, TotalLength, TotalTime, TermsSummed):
    numberOfTimeSteps = int(TotalTime/TimeStep)+1
    numberOfLengthSteps = int(TotalLength/LengthStep)+1
    temporaryNumber = 0
    storageArray2 = np.zeros((numberOfTimeSteps,numberOfLengthSteps))
    timeTracker2 = []
    TimeTime = 0
    RealTimeIGuess = .001
    for i in range(len(storageArray2)):
        RealTimeIGuess += .001
        for j in range(1, numberOfLengthSteps-1):
            x= LengthStep*j
            t = i*TimeStep

            for n in range(1,TermsSummed+1):
                temporaryNumber += ((1/(n**2))*(math.sin(.5*pi*n))*(math.sin(n*pi*x)))*(math.exp((-n**2)*(pi**2)*(t)))
            storageArray2[i,j] = (8/(pi**2))*temporaryNumber
            temporaryNumber=0

    for k in range(0,21,1):
        timeTracker2.append(round(TimeTime, 5))
        TimeTime += .001

    AnalyticalTimeandHeat = np.column_stack((timeTracker2, storageArray2))
    np.savetxt('AnalyticlRod.txt', AnalyticalTimeandHeat, fmt = '%1.4f', delimiter=",", comments = '', newline='\r\n')
    # print(timeTracker)
    # print(storageArray2)

    # for i in range(xSteps):
        # print ("Yo")
    return storageArray2

def TwoRowLoop(LengthStep, TimeStep, alpha, TotalLength, TotalTime ):
    numberOfLengthSteps = int(TotalLength/LengthStep)+1
    storageArray3 = np.zeros((2,numberOfLengthSteps))
    # storageArray3[0] = [0, .2, 0.4, 0.6, 0.8, 1., 0.8, 0.6, 0.4, 0.2, 0.0]
    CountChocula = -1
    WhereIveBeen = 0
    WhereImGoing= 1
    storageArray3[0,5] = 1
    HowManySteps = 0
    while storageArray3[0, 5] >= .5:



        for j in range(1, numberOfLengthSteps-1):
            if CountChocula == -1:
                if 0 <= j and j <= 5:
                    storageArray3[WhereIveBeen,j] = 2*j*LengthStep
                    #HowManySteps+=1

                elif j > 5:
                    x= LengthStep*j
                    storageArray3[WhereIveBeen,j] = 2*(1-x)
                print(storageArray3)
                continue
                # CountChocula += 1
            # else:
            storageArray3[ WhereImGoing,j] = (TimeStep*(alpha*((storageArray3[WhereIveBeen,j+1]-(2*storageArray3[WhereIveBeen,j])+storageArray3[ WhereIveBeen,j-1])/(LengthStep**2))))+ storageArray3[WhereIveBeen,j]

        time= HowManySteps*TimeStep
        if CountChocula >= 0:
            storageArray3[WhereIveBeen] = storageArray3[WhereImGoing]
        file.write(str('{:.3f}'.format(time)).encode() + ', '.encode())
        np.savetxt(file, np.atleast_2d(storageArray3[0,:]), fmt='%.3f', delimiter=', ', newline = '\r\n')
        HowManySteps += 1
        CountChocula += 1


    print(CountChocula)

    # for i in range(xSteps):
        # print ("Yo")
    return storageArray3

#So I somehow started naming these variable like they were copper. I tried to fix the main ones but if you see a copper variable it is a simple mixup.
def Steel(LengthStep, TimeStep, alpha, TotalLength):
    numberOfLengthSteps = int(TotalLength/LengthStep)+1
    storageArray4 = np.zeros((2,numberOfLengthSteps))
    storageArray4[0] = [0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0]
    CountChocula = 0
    WhereIveBeen = 0
    WhereImGoing = 1
    HowManySteps = 0
    timetracker3 = [0]
    everyHundred=np.empty([2,11], dtype = float)

    while storageArray4[0, 5] >= 20:
        for j in range(1, numberOfLengthSteps-1):
            storageArray4[ WhereImGoing,j] = (TimeStep*(alpha*((storageArray4[WhereIveBeen,j+1]-(2*storageArray4[WhereIveBeen,j])+storageArray4[ WhereIveBeen,j-1])/(LengthStep**2))))+ storageArray4[WhereIveBeen,j]
        # if CountChocula >= 0:
        storageArray4[WhereIveBeen] = storageArray4[WhereImGoing]

        CountChocula += 1


        time= HowManySteps*TimeStep
        if HowManySteps % 1000== 0 and CountChocula > 1:
            newRow = storageArray4[WhereImGoing,:]
            everyHundred = np.vstack((everyHundred, newRow))
            #print("_______________________________________________hfhfhfhfhfhfhfh_______________")
            #print(HowManySteps)
            timetracker3.append(time)
        HowManySteps += 1

    print(CountChocula * TimeStep)
    timetracker3.append(time)

    print(everyHundred)

    initialRow = [ 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0]

    CopperEvery1000= np.column_stack((timetracker3, everyHundred))
    trimmedCopper = np.delete(CopperEvery1000, 0, axis=0)
    arraytoSave = np.vstack((initialRow, trimmedCopper))


    np.savetxt('SteeleveryHundred.txt', arraytoSave, fmt = '%1.4f', delimiter=",", comments = '', newline='\r\n')
    # for i in range(xSteps):
        # print ("Yo")
    return storageArray4

def Copper(LengthStep, TimeStep, alpha, TotalLength):
    numberOfLengthSteps = int(TotalLength/LengthStep)+1
    storageArray5 = np.zeros((2,numberOfLengthSteps))
    storageArray5[0] = [0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0]
    CountChocula = 0
    WhereIveBeen = 0
    WhereImGoing = 1
    HowManySteps = 0
    timetracker3 = [0]
    everyHundred=np.zeros([2,11], dtype = float)

    while storageArray5[0, 5] >= 20:
        for j in range(1, numberOfLengthSteps-1):
            storageArray5[ WhereImGoing,j] = (TimeStep*(alpha*((storageArray5[WhereIveBeen,j+1]-(2*storageArray5[WhereIveBeen,j])+storageArray5[ WhereIveBeen,j-1])/(LengthStep**2))))+ storageArray5[WhereIveBeen,j]
        # if CountChocula >= 0:
        storageArray5[WhereIveBeen] = storageArray5[WhereImGoing]

        CountChocula += 1


        time= HowManySteps*TimeStep
        if time % 20== 0 and CountChocula > 1:
            newRow = storageArray5[WhereImGoing,:]
            #print(everyHundred)
            if time == 20:
                everyHundred = np.delete(everyHundred,(1), axis=0)
                everyHundred = np.vstack((everyHundred, newRow))
            else:
                everyHundred = np.vstack((everyHundred, newRow))
            #print(everyHundred)
            #print("_______________________________________________hfhfhfhfhfhfhfh_______________")
            #print(HowManySteps)
            timetracker3.append(time)
        elif storageArray5[0, 5] <= 20 and CountChocula > 1:
            new2Row = storageArray5[WhereImGoing, :]
            everyHundred = np.vstack((everyHundred, new2Row))
            timetracker3.append(time)
        HowManySteps += 1

    print(CountChocula * TimeStep)
    # timetracker3.append(time)
    print(timetracker3)

    print(everyHundred)

    initialRow = [ 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0]

    everyHundred = np.delete(everyHundred, (0), axis=0)
    CopperEvery1000= np.vstack((initialRow, everyHundred))
    #trimmedCopper = np.delete(CopperEvery1000, 0, axis=0)
    arraytoSave = np.column_stack((timetracker3, CopperEvery1000))


    np.savetxt('Coppereverytwohundred.txt', arraytoSave, fmt = '%1.4f', delimiter=",", comments = '', newline='\r\n')
    # for i in range(xSteps):
        # print ("Yo")
    return storageArray5







def main():
    #test = Explicit_Finite_Difference(.1, .001, 1, 1, .02)
    # np.savetxt('TestRod.txt', test, fmt = '%8.4f', delimiter=",", comments = '', newline='\r\n', )
    test2 = AnalyticalSolution(.1, .001, 1, 1, .02, 10000)
    Test3 = TwoRowLoop(0.1, 0.001, 1, 1, 0.02)

    #alphaSteel = 0.054/(7800*0.46)
    alphaCopper = 0.386/(896*0.38)

    #Test5a = Steel(0.1, 1, alphaSteel, 1)
    Test5b = Copper(0.1, .001,alphaCopper, 1)
    #print(Test5a)


main()

