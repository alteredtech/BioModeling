import math
import numpy as np 


def ProblemFinite(dt=.001,dx=.1,FinalTime=.1,alpha=1,ArrayX=1,FileName="finite.txt"):
    ArrayY=int(FinalTime/dt)

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

def ProblemAnalytical(dt=.001,dx=.1,FinalTime=.1,alpha=1,ArrayX=11,num=1000,FileName="analytical.txt"):
    ArrayY=int(FinalTime/dt)
    Uarray = np.zeros((ArrayY, ArrayX), dtype=float)

    # does all the data calculations
    for i in range(len(Uarray)):
        tempNum = 0
        for j in range(len(Uarray[i])):
            if i == 0 and j < int(len(Uarray[i])/2+1):
                Uarray[i][j] = (2*(j*dx))
            elif i == 0:
                Uarray[i][j] = (2*(1-(j*dx)))
            if (j >= 1 and j < len(Uarray[i])-1) and i > 0:
                for n in range(1,num):
                    tempNum += analytical(n,Uarray,i,j)

                Uarray[i][j] = (8/math.pi**2)*tempNum

    Uarray = np.vstack((np.arange(0,(ArrayX)*dx,dx),Uarray))
    Uarray = np.column_stack((np.arange(0,(ArrayY+1)*dt,dt),Uarray))
    np.savetxt(FileName, Uarray, delimiter=',', newline='\r\n', comments='',fmt='%.4f')

def Problem4(dt,dx,alpha,getToValue,ArrayX,FileName):
    Uarray = np.zeros((2, ArrayX), dtype=float)
    tempNum = dt
    firstTime = True
    File = open(FileName,'wb')
    center = ArrayX/2+1

    #does all the data calculations
    while(Uarray[0][center] <= getToValue):
        for i in range(len(Uarray)):
            Uarray[1][0] = tempNum
            for j in range(len(Uarray[i])):
                if (i == 0 and j < int(len(Uarray[i])/2+1)) and firstTime:
                    Uarray[i][j] = (2*(j*dx))
                elif i == 0:
                    Uarray[i][j] = (2*(1-(j*dx)))
                if (j >= 1 and j < len(Uarray[i])-1) and i == 1:
                    firstTime = False
                    Uarray[i][j] = equation(alpha,Uarray,i,j,dx,dt)
        #write to file without overwriting

        #puts items in second row into first
        for k in range(len(Uarray[1])):
            if k == 0:
                np.savetxt(FileName, Uarray[0][np.newaxis], delimiter=',', comments='',fmt='%.4f', newline='\n')
            else:
                if Uarray[0][center] <= getToValue:
                    np.savetxt(FileName, Uarray[0][np.newaxis], delimiter=',', comments='',fmt='%.4f', newline='\n')
                else:
                    Uarray[0][k] = Uarray[1][k]
        tempNum += dt

def ProblemAlloy(dt,dx,alpha,getToValue,modValue,ArrayX,FileName):
    #alpha = ((54/(7800*.046))/10**3)
    Uarray = np.zeros((2, ArrayX), dtype=float)
    # does the distances and time
    tempNum = dt
    center = ArrayX/2+1
    firstTime = True
    tick = 0

    # does all the data calculation
    while(Uarray[0][center] <= getToValue):
        for i in range(len(Uarray)):
            for j in range(len(Uarray[i])):
                if (i == 0 and j < int(len(Uarray[i])/2+1)) and firstTime:
                    Uarray[i][j] = (2*(j*dx))
                elif i == 0:
                    Uarray[i][j] = (2*(1-(j*dx)))
                if (j >= 1 and j < len(Uarray[i])-1) and i == 1:
                    if firstTime:
                        np.savetxt(FileName, Uarray[0][np.newaxis], delimiter=',', comments='',fmt='%.4f', newline='\n')
                    firstTime = False
                    Uarray[i][j] = equation(alpha,Uarray,i,j,dx,dt)

        #puts items in second row into first and saves
        for k in range(len(Uarray[1])):
            if k % modValue == 0:
                np.savetxt(FileName, Uarray[0][np.newaxis], delimiter=',', comments='',fmt='%.4f', newline='\n')
            else:
                if Uarray[0][center] <= getToValue:
                    np.savetxt(FileName, Uarray[0][np.newaxis], delimiter=',', comments='',fmt='%.4f', newline='\n')
                else:
                    Uarray[0][k] = Uarray[1][k]
        tempNum += dt
        tick += 1

def equation(alpha,Uarray,i,j,dx,dt):
    return ((alpha * (Uarray[i-1][j+1]-2*Uarray[i-1][j]+Uarray[i-1][j-1])/dx**2) * dt) + Uarray[i-1][j]
    
def analytical(num,Uarray,i,j):
    return ((1/num**2)*(math.sin(.5*math.pi*num))*(math.sin(num*math.pi*Uarray[0][j]))*(math.exp((-num**2)*(math.pi**2)*(Uarray[i][0]))))

ProblemFinite()
ProblemAnalytical()