import math
import numpy as np

np.set_printoptions(precision = 4, suppress=True)

#equation for x to solve the finite solution 
def equationX(z,i,j,Uarray,alpha,dx,dt):
    num = ((alpha * (Uarray[z][i][j+1] - 2 * Uarray[z][i][j] + Uarray[z][i][j-1]) / (dx ** 2)) * dt)
    return num

#equation for y to solve the finite solution 
def equationY(z,i,j,Uarray,alpha,dy,dt):
    num = ((alpha * (Uarray[z][i+1][j] - 2 * Uarray[z][i][j] + Uarray[z][i-1][j]) / (dy ** 2)) * dt)
    return num

#equation for z to solve the finite solution 
def equationZ(z,i,j,Uarray,alpha,dz,dt):
    num = ((alpha * (Uarray[z+1][i][j] - 2 * Uarray[z][i][j] + Uarray[z-1][i][j]) / (dz ** 2)) * dt)
    return num

def findTime(Uarray,topBottomValue,sideValue,valueToFind,centerX,centerY,alpha,dx,dy,dt):
    temp = np.copy(Uarray)
    for k in range(len(temp[0])):
        for m in range(len(temp[0,1])):
            if k == 0 or k == len(temp[0])-1:
                temp[0,k,m] = topBottomValue
            elif m == 0 or m == len(temp[0,1])-1:
                temp[0,k,m] = sideValue
    time = 0
    temp[1] = np.copy(temp[0])

    while(temp[0][centerY][centerX] < valueToFind):
    
        for i in range(1,len(temp[0])-1):
            for j in range(1,len(temp[0,i])-1):
                temp[1][i][j] = (equationX(0,i,j,temp,alpha,dx,dt) + equationY(0,i,j,temp,alpha,dy,dt)) + temp[0][i][j]
        temp[0] = np.copy(temp[1])
        time += 1
        print(time)
        if temp[0][centerY][centerX] > valueToFind:
            num = time*dt
    return num

def Equilibrium(Array,centerX,centerY,centerZ,alpha,dx,dy,dz,dt,Divisor):
    FirstArray = np.copy(Array)
    NewArray = np.copy(FirstArray)
    movingAverage = []
    temp = 0
    found = False
    while(not found):
        for h in range(1,len(FirstArray)-1):
            for i in range(1,len(FirstArray[0])-1):
                for j in range(1,len(FirstArray[0,i])-1):
                        FirstArray[h][i][j] = (equationX(h,i,j,NewArray,alpha,dx,dt) + equationY(h,i,j,NewArray,alpha,dy,dt)+ equationZ(h,i,j,NewArray,alpha,dz,dt)) + NewArray[h][i][j]
        NewArray = np.copy(FirstArray)
        if len(movingAverage) < Divisor:
            movingAverage.append(FirstArray[centerZ,centerY,centerX])
            #print(movingAverage)
        else:
            for i in range(0,Divisor):
                temp += movingAverage[i]
                #print(round(temp/Divisor,2))
            temp = temp/Divisor
            print(temp)
            if round(temp,2) == round(FirstArray[centerZ,centerY,centerX],2):
                found = True
                return round(temp,2)
            else:
                movingAverage.pop(0)
                temp = 0

def ProblemPlate(header,dx,dy,dt,alpha,ArrayX,ArrayY,topBottomValue,sideValue,valueToFind,FileName):
    #creates two arrays
    Uarray = np.zeros([2,ArrayY,ArrayX], dtype= float)
    #alpha = 0.283*(10**-4) #diffusion
    centerX = int(ArrayX/2)
    centerY = int(ArrayY/2)
    File = open(FileName,'wb')
    File.write(str(header).encode())

    #setting outside boundaries 
    for k in range(len(Uarray[0])):
        for m in range(len(Uarray[0,1])):
            if k == 0 or k == len(Uarray[0])-1:
                Uarray[0,k,m] = topBottomValue
            elif m == 0 or m == len(Uarray[0,1])-1:
                Uarray[0,k,m] = sideValue

    time = 0
    Uarray[1] = np.copy(Uarray[0])
    File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
    np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')

    magicNumber = findTime(Uarray,topBottomValue,sideValue,valueToFind,centerX,centerY,alpha,dx,dy,dt)

    #keep going until the center value is met
    while(Uarray[0][centerY][centerX] < valueToFind):

        for i in range(1,len(Uarray[0])-1):
            for j in range(1,len(Uarray[0,i])-1):
                Uarray[1][i][j] = (equationX(0,i,j,Uarray,alpha,dx,dt) + equationY(0,i,j,Uarray,alpha,dy,dt)) + Uarray[0][i][j]
        Uarray[0] = np.copy(Uarray[1])
        time += 1

        #print the plate at 25%, 50%, 75%, 100%
        if round((time*dt),2)%25 == 0:
            File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
            np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')

        elif round(time*dt,2) >= magicNumber:
            File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
            np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')
    File.close()

def CubeCross(header,dx,dy,dz,dt,alpha,sideValue,bottomValue,centerValue,ArrayX,ArrayY,ArrayZ,valueToFind,FileName):
    Uarray = np.zeros([ArrayZ,ArrayY,ArrayX], dtype= float)
    NewArray = np.zeros([ArrayZ, ArrayY, ArrayX], dtype=float)
    #alpha = (54/(7800*(.46*10**3)))
    centerX = int(ArrayX/2)
    centerY = int(ArrayY/2)
    centerZ = int(ArrayZ/2)

    for l in range(len(Uarray)):
        for k in range(len(Uarray[0])):
            for m in range(len(Uarray[0,1])):
                if (k == 0 or k == len(Uarray[0])-1) and (l>0 and l<len(Uarray[0])-1):
                    Uarray[l,k,m] = sideValue
                elif (m == 0 or m == len(Uarray[0,0])-1) and (l>0 and l<len(Uarray[0])-1):
                    Uarray[l,k,m] = sideValue
                elif l == 0:
                    Uarray[l,k,m] = bottomValue
                elif l == len(Uarray[0])-1:
                    Uarray[l,k,m] = sideValue
                else:
                    Uarray[l,k,m] = centerValue

    time = 0
    NewArray = np.copy(Uarray)
    while(Uarray[centerZ,centerY,centerX]<valueToFind):
        for h in range(1,len(Uarray)-1):
            for i in range(1,len(Uarray[0])-1):
                for j in range(1,len(Uarray[0,i])-1):
                        Uarray[h][i][j] = (equationX(h,i,j,NewArray,alpha,dx,dt) + equationY(h,i,j,NewArray,alpha,dy,dt)+ equationZ(h,i,j,NewArray,alpha,dz,dt)) + NewArray[h][i][j]

        NewArray = np.copy(Uarray)
        time +=1
        if Uarray[centerZ,centerY,centerX] > valueToFind:
            temp = np.copy(Uarray[:,:,centerX])
            temp = np.vstack((temp,Uarray[:,centerY,:]))
            np.savetxt(FileName, temp, fmt='%.4f', delimiter=",", comments='', newline='\r\n', header=header)

def CubeCenterColumn(header,FileName,dx,dy,dz,dt,alpha,sideValue,bottomValue,centerValue,ArrayX,ArrayY,ArrayZ,Modulus,Divisor,Difference):
    Uarray = np.zeros([ArrayZ,ArrayY,ArrayX], dtype= float)
    NewArray = np.zeros([ArrayZ, ArrayY, ArrayX], dtype=float)
    temp = np.arange(0,ArrayZ+1,dtype=float)
    File = open(FileName,'wb')
    File.write(str(header+'\n').encode())
    #alpha = (54/(7800*(.46*10**3)))
    centerX = int(ArrayX/2)
    centerY = int(ArrayY/2)
    centerZ = int(ArrayZ/2)

    for l in range(len(Uarray)):
        for k in range(len(Uarray[0])):
            for m in range(len(Uarray[0,0])):
                if (k == 0 or k == len(Uarray[0])-1) and (l>0 and l<len(Uarray[0])-1):
                    Uarray[l,k,m] = sideValue
                elif (m == 0 or m == len(Uarray[0,0])-1) and (l>0 and l<len(Uarray[0])-1):
                    Uarray[l,k,m] = sideValue
                elif l == 0:
                    Uarray[l,k,m] = bottomValue
                elif l == len(Uarray[0])-1:
                    Uarray[l,k,m] = sideValue
                else:
                    Uarray[l,k,m] = centerValue

    time = 0
    NewArray = np.copy(Uarray)

    magicNumber = round(Equilibrium(Uarray,centerX,centerY,centerZ,alpha,dx,dy,dz,dt,Divisor),1)

    while(Uarray[centerZ,centerY,centerX] < magicNumber-Difference):
        for h in range(1,len(Uarray)-1):
            for i in range(1,len(Uarray[0])-1):
                for j in range(1,len(Uarray[0,i])-1):
                        Uarray[h][i][j] = (equationX(h,i,j,NewArray,alpha,dx,dt) + equationY(h,i,j,NewArray,alpha,dy,dt)+ equationZ(h,i,j,NewArray,alpha,dz,dt)) + NewArray[h][i][j]

        NewArray = np.copy(Uarray)
        time +=1

        if time%Modulus==0:
            File.write(str('Time:, {:.1f}'.format(time)+', ').encode())
            temp = np.copy(Uarray[:,centerY,centerX]).reshape(1,ArrayX)
            np.savetxt(File, temp, fmt='%.4f', delimiter=",", comments='')

        if Uarray[centerZ][centerY][centerX] > magicNumber-Difference:
            File.write(str('Time:, {:.1f}'.format(time)+', ').encode())
            temp = np.copy(Uarray[:,centerY,centerX]).reshape(1,ArrayX)
            np.savetxt(File, temp, fmt='%.4f', delimiter=",", comments='')
            File.close()

def main():
    #ProblemPlate("problem 1",.01,.01,.1,0.283*(10**-4),21,11,20,20,19,"NewProblem1.txt")
    CubeCenterColumn('Cube Center','CenterColumn.txt',.01,.01,.01,1,(54/(7800*(.46*10**3))),40,150,20,21,21,21,50,30,.1)
main()