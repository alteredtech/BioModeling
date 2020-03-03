import numpy as np
import math

np.set_printoptions(precision = 4, suppress=True)

def Problem1():
    dt = .001
    dx = .1
    alpha = 1
    finalT = 0.1


    Uarray = np.zeros((101,12),dtype=float)
    #does the distances and time
    tempNum = 0
    for k in range(len(Uarray)-1):
        Uarray[k+1][0] = tempNum
        tempNum += .001
    tempNum = 0
    for m in range(len(Uarray[0])-1):
        Uarray[0][m+1] = tempNum
        tempNum += .1
    print(Uarray)
    #does all the data calculations
    for i in range(len(Uarray)):
        for j in range(len(Uarray[i])):
            if i==1 and j >=2:
                if j <= 6:
                    Uarray[i][j] = (2*Uarray[0][j])
                else:
                    Uarray[i][j] = (2*(1-Uarray[0][j]))
            elif (j>=2 and j<11) and i > 1:
                Uarray[i][j] = ((alpha * (Uarray[i-1,j+1]-2*Uarray[i-1,j]+Uarray[i-1,j-1])/dx**2) * dt) + Uarray[i-1,j]
                [j]

    np.savetxt('testCase1.txt', Uarray, delimiter=',', newline='\r\n', comments='',fmt=['%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f','%.4f'])

def Problem2():
    dt = .001
    dx = .1
    alpha = 1
    finalT = 0.1
    num = 1000

    Uarray = np.zeros((100, 12), dtype=float)
    # does the distances and time
    tempNum = 0
    for k in range(len(Uarray) - 1):
        Uarray[k + 1][0] = tempNum
        tempNum += .001
    tempNum = 0
    for m in range(len(Uarray[0]) - 1):
        Uarray[0][m + 1] = tempNum
        tempNum += .1

    # does all the data calculations
    for i in range(4):
        for j in range(len(Uarray[i])):
            tempNum = 0
            if i == 1 and j >= 2:
                if j <= 6:
                    Uarray[i][j] = (2 * Uarray[0][j])
                else:
                    Uarray[i][j] = (2 * (1 - Uarray[0][j]))
            elif (j >= 2 and j < 11) and i > 1:
                for n in range(1,num):
                    tempNum += analytical(n,Uarray,i,j)
                    
                print(tempNum*(8/math.pi**2))
                Uarray[i][j] = (8/math.pi**2)*tempNum
    np.savetxt('Analyticaltest1.txt', Uarray, delimiter=',', newline='\r\n', comments='',
               fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f'])

def Problem4():
    dt = .001
    dx = .1
    alpha = 1
    Uarray = np.zeros((2, 12), dtype=float)
    # does the distances and time
    tempNum = 0.001
    firstTime = True
    foundTemp = False

    #does all the data calculations
    while(not foundTemp):
        for i in range(len(Uarray)):
            Uarray[1][0] = tempNum
            for j in range(len(Uarray[i])):
                if (i==0 and j >=2) and firstTime:
                    if j <= 6:
                        Uarray[i][j] = (2*dx*(j-1))
                    else:
                        Uarray[i][j] = (2*(1-(dx*(j-1))))
                elif (j>=2 and j<11) and i == 1:
                    firstTime = False
                    Uarray[i][j] = ((alpha * (Uarray[i-1][j+1]-2*Uarray[i-1][j]+Uarray[i-1][j-1])/dx**2) * dt) + Uarray[
                        i-1][j]
        #write to file without overwriting
        with open("Problem4.txt", "a+") as file:
            if tempNum == .001:
                np.savetxt(file, Uarray, delimiter=',', newline='\r\n', comments='',
               fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f'])
            else:
                x = Uarray[1]
                np.savetxt(file, x[np.newaxis], delimiter=',', comments='',
                           fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                                '%.4f'], newline='\n')

        #puts items in second row into first
        for k in range(len(Uarray[1])):
            Uarray[0][k] = Uarray[1][k]

        #if the temp at the middle is below 5 then stop the while loop otherwise keep going
        if Uarray[0][6] <= .5:
            foundTemp = True
            x = Uarray[1]
            with open("Problem4.txt","a") as file:
                np.savetxt(file, x[np.newaxis], delimiter=',', comments='',
                       fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                            '%.4f'], newline='\n')

        else:
            tempNum += .001

def Problem5steel():
    dt = .001
    dx = .1
    alpha = ((54/(7800*.046))/10**3)
    Uarray = np.zeros((2, 12), dtype=float)
    # does the distances and time
    tempNum = 0.001
    firstTime = True
    foundTemp = False
    tick = 0


    # does all the data calculations
    while (not foundTemp):
        for i in range(len(Uarray)):
            Uarray[1][0] = tempNum
            for j in range(len(Uarray[i])):
                if (i == 0 and j >= 2) and firstTime and j<11:
                    Uarray[i][j] = 100
                elif (j >= 2 and j < 11) and i == 1:
                    firstTime = False
                    Uarray[i][j] = ((alpha * (
                                Uarray[i - 1][j + 1] - 2 * Uarray[i - 1][j] + Uarray[i - 1][j - 1]) / dx ** 2) * dt) + \
                                   Uarray[
                                       i - 1][j]
        # write to file without overwriting

        with open("Problem5steel.txt", "a+") as file:
            if tempNum == .001:
                np.savetxt(file, Uarray, delimiter=',', newline='\r\n', comments='',
                           fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                                '%.4f'])
            elif (tick*tempNum)%100==0:
                #print(tick)
                x = Uarray[1]
                np.savetxt(file, x[np.newaxis], delimiter=',', comments='',
                           fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                                '%.4f'], newline='\n')

        # puts items in second row into first
        for k in range(len(Uarray[1])):
            Uarray[0][k] = Uarray[1][k]

        # if the temp at the middle is below 5 then stop the while loop otherwise keep going
        if Uarray[0][6] <= 20:
            foundTemp = True
            with open("Problem5steel.txt", "a+") as file:
                x = Uarray[0]
                np.savetxt(file, x[np.newaxis], delimiter=',', comments='',
                               fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                                    '%.4f',
                                    '%.4f'])

        else:
            tempNum += .001
            tick += 1

def Problem5copper():
    dt = .001
    dx = .1
    alpha = ((386/(8960*.038))/10**3)
    Uarray = np.zeros((2, 12), dtype=float)
    # does the distances and time
    tempNum = 0.001
    firstTime = True
    foundTemp = False
    tick = 0


    # does all the data calculations
    while (not foundTemp):
        for i in range(len(Uarray)):
            Uarray[1][0] = tempNum
            for j in range(len(Uarray[i])):
                if (i == 0 and j >= 2) and firstTime and j<11:
                    Uarray[i][j] = 100
                elif (j >= 2 and j < 11) and i == 1:
                    firstTime = False
                    Uarray[i][j] = ((alpha * (
                                Uarray[i - 1][j + 1] - 2 * Uarray[i - 1][j] + Uarray[i - 1][j - 1]) / dx ** 2) * dt) + \
                                   Uarray[
                                       i - 1][j]

        # write to file without overwriting
        with open("Problem5copper.txt", "a+") as file:
            if tempNum == .001:
                np.savetxt(file, Uarray, delimiter=',', newline='\r\n', comments='',
                           fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                                '%.4f'])
            elif (tick*tempNum)%20==0:
                print(tick)
                x = Uarray[1]
                np.savetxt(file, x[np.newaxis], delimiter=',', comments='',
                           fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                                '%.4f'], newline='\n')

        # puts items in second row into first
        for k in range(len(Uarray[1])):
            Uarray[0][k] = Uarray[1][k]

        # if the temp at the middle is below 5 then stop the while loop otherwise keep going
        if Uarray[0][6] <= 20:
            foundTemp = True
            with open("Problem5copper.txt", "a+") as file:
                x = Uarray[0]
                np.savetxt(file, x[np.newaxis], delimiter=',', comments='',
                               fmt=['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f',
                                    '%.4f',
                                    '%.4f'])
        else:
            tempNum += .001
            tick += 1


#density of copper 8960 kg/m^3
#dt for problem 1 = 0.006
#dt for copper = 4.410999999999808
#dt for steel = 33.22300000001327


def Problem(dt,dx,FinalTime,alpha,ArrayX,ArrayY,FileName):

    Uarray = np.zeros((ArrayY,ArrayX),dtype=float)

    #does all the data calculations
    for i in range(len(Uarray)):
        for j in range(len(Uarray[i])):
            if i == 0 and j < int(len(Uarray[i])/2+1):
                Uarray[i][j] = (2*(j*dx))
            elif i == 0:
                Uarray[i][j] = (2*(1-(j*dx)))
            if (j >= 1 and j < len(Uarray[i])-1) and i > 0:
                Uarray[i][j] = equation(alpha,Uarray,i,j,dx,dt)
    Uarray = np.vstack((np.arange(0,(ArrayX)*dx,dx),Uarray))
    Uarray = np.column_stack((np.arange(0,(ArrayY+1)*dt,dt),Uarray))
    np.savetxt(FileName, Uarray, delimiter=',', newline='\r\n', comments='',fmt='%.4f')

def equation(alpha,Uarray,i,j,dx,dt):
    num = ((alpha * (Uarray[i-1][j+1]-2*Uarray[i-1][j]+Uarray[i-1][j-1])/dx**2) * dt) + Uarray[i-1][j]
    return num

def analytical(num,Uarray,i,j):
    sum = ((1/num**2)*(math.sin(.5*math.pi*num))*(math.sin(num*math.pi*Uarray[0][j]))*(math.exp((-num**2)*(math.pi**2)*(Uarray[i][0]))))
    return sum

def main():
    #Problem1()
    Problem2()
    # Problem4()
    # Problem5steel()
    # Problem5copper()
    #Problem(.001,.1,.2,1,11,21,"testFile.txt")

main()

# if j <= (len(Uarray[i])/2+1):
#                     Uarray[i][j] = (2*Uarray[0][j])
#                 else:
#                     Uarray[i][j] = (2*(1-Uarray[0][j]))
