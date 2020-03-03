import math
import numpy as np

np.set_printoptions(precision = 4, suppress=True)

def eqCenter(Array,fo,j,k,ambientTemp):
    return (1-4*fo)*Array[0,j,k]+fo*(Array[0,j-1,k]+Array[0,j+1,k]+Array[0,j,k-1]+Array[0,j,k+1])

def eqLSide(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-2*bi*fo)*Array[0,j,k]+2*fo*(Array[0,j,k+1]+.5*(Array[0,j-1,k]+Array[0,j+1,k])+bi*ambientTemp)

def eqRSide(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-2*bi*fo)*Array[0,j,k]+2*fo*(Array[0,j,k-1]+.5*(Array[0,j-1,k]+Array[0,j+1,k])+bi*ambientTemp)

def eqTSide(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-2*bi*fo)*Array[0,j,k]+2*fo*(Array[0,j+1,k]+.5*(Array[0,j,k+1]+Array[0,j,k-1])+bi*ambientTemp)

def eqLCorner(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-4*bi*fo)*Array[0,j,k]+2*fo*(Array[0,j,k+1]+Array[0,j+1,k]+2*bi*ambientTemp)

def eqRCorner(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-4*bi*fo)*Array[0,j,k]+2*fo*(Array[0,j+1,k]+Array[0,j,k-1]+2*bi*ambientTemp)

def eqLBCorner(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-2*bi*fo)*Array[0,j,k]+2*fo*(Array[0,j-1,k]+Array[0,j,k+1]+bi*ambientTemp)

def eqRBCorner(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-2*bi*fo)*Array[0,j,k]+2*fo*(Array[0,j-1,k]+Array[0,j,k-1]+bi*ambientTemp)

def eqBSide(Array,fo,bi,j,k,ambientTemp):
    return (1-4*fo-2*bi*0*fo)*Array[0,j,k]+2*fo*(Array[0,j-1,k]+.5*(Array[0,j,k-1]+Array[0,j,k+1])+0*bi*ambientTemp)

def findTime(array,internalTempFind,fo,bi,ambientTemp,searchSlotX,searchSlotY,searchSlotZ,dt):
    temp = np.copy(array)
    time = 0

    while(round(temp[searchSlotZ,searchSlotY,searchSlotX],8) >= internalTempFind):
        for j in range(len(temp[0])): #row
            for k in range(len(temp[0,1])): #column
                #top half side
                if (0 < k < len(temp[0,0])-1) and j==0:
                    temp[1,j,k] = eqTSide(temp,fo,bi,j,k,ambientTemp)
                #bottom half side
                elif (0 < k < len(temp[0,0])-1) and j==len(temp[0])-1:
                    temp[1,j,k] = eqBSide(temp,fo,bi,j,k,ambientTemp)
                #left half side
                elif (0 < j < len(temp[0])-1) and k==0:
                    temp[1,j,k] = eqLSide(temp,fo,bi,j,k,ambientTemp)
                #left top corner
                elif j==0 and k==0:
                    temp[1,j,k] = eqLCorner(temp,fo,bi,j,k,ambientTemp)
                #right top corner
                elif j==0 and k==len(temp[0,0])-1:
                    temp[1,j,k] = eqRCorner(temp,fo,bi,j,k,ambientTemp)
                #right half side
                elif k == len(temp[0,0])-1 and (0<j<len(temp[0])-1):
                    temp[1,j,k] = eqRSide(temp,fo,bi,j,k,ambientTemp)
                #bottom left corner
                elif j == len(temp[0])-1 and k == 0:
                    temp[1,j,k] = eqLBCorner(temp,fo,bi,j,k,ambientTemp)
                #bottom right corner
                elif j == len(temp[0])-1 and k == len(temp[0,0])-1:
                    temp[1,j,k] = eqRBCorner(temp,fo,bi,j,k,ambientTemp)
                #center
                else:
                    temp[1,j,k]= eqCenter(temp,fo,j,k,ambientTemp)
        temp[0] = np.copy(temp[1])
        time += 1
        # print(time)
        if temp[searchSlotZ,searchSlotY,searchSlotX] > internalTempFind:
            num = time
    return num

def Snickers(fileName,startInternalTemp = 33,internalTempFind = 15,ambientTemp = 5,dt = 0.01,dx = 1/1000,dy = 1/1000,convRate = 100,thermCond = 0.4,heatCap = 2400,rho = 800,ArrayX=16,ArrayY=11,ArrayZ=2,searchSlotX=8,searchSlotY=10,searchSlotZ=0):
    fo = ((thermCond/(rho*heatCap))*dt)/dx**2
    bi = (convRate*dx)/thermCond
    File = open(fileName,'wb')
    File.write(str("Problem 8\n").encode())

    snickerBlock = np.full([ArrayZ,ArrayY,ArrayX],startInternalTemp,dtype=float)
    
    doneTime = findTime(snickerBlock,internalTempFind,fo,bi,ambientTemp,searchSlotX,searchSlotY,searchSlotZ,dt)
    time = 0
    print("calm down Dylan, it essentially runs twice to get the time it takes to get to the value then does it again")
    while(round(snickerBlock[searchSlotZ,searchSlotY,searchSlotX],8) >= internalTempFind):
        for j in range(len(snickerBlock[0])): #row
            for k in range(len(snickerBlock[0,0])): #column
                #top half side
                if (0 < k < len(snickerBlock[0,0])-1) and j==0:
                    snickerBlock[1,j,k] = eqTSide(snickerBlock,fo,bi,j,k,ambientTemp)
                #bottom half side
                elif (0 < k < len(snickerBlock[0,0])-1) and j==len(snickerBlock[0])-1:
                    snickerBlock[1,j,k] = eqBSide(snickerBlock,fo,bi,j,k,ambientTemp)
                #left half side
                elif (0 < j < len(snickerBlock[0])-1) and k==0:
                    snickerBlock[1,j,k] = eqLSide(snickerBlock,fo,bi,j,k,ambientTemp)
                #left top corner
                elif j==0 and k==0:
                    snickerBlock[1,j,k] = eqLCorner(snickerBlock,fo,bi,j,k,ambientTemp)
                #right top corner
                elif j==0 and k==len(snickerBlock[0,0])-1:
                    snickerBlock[1,j,k] = eqRCorner(snickerBlock,fo,bi,j,k,ambientTemp)
                #right half side
                elif k == len(snickerBlock[0,0])-1 and (0<j<len(snickerBlock[0])-1):
                    snickerBlock[1,j,k] = eqRSide(snickerBlock,fo,bi,j,k,ambientTemp)
                #bottom left corner
                elif j == len(snickerBlock[0])-1 and k == 0:
                    snickerBlock[1,j,k] = eqLBCorner(snickerBlock,fo,bi,j,k,ambientTemp)
                #bottom right corner
                elif j == len(snickerBlock[0])-1 and k == len(snickerBlock[0,0])-1:
                    snickerBlock[1,j,k] = eqRBCorner(snickerBlock,fo,bi,j,k,ambientTemp)
                #center
                else:
                    snickerBlock[1,j,k]= eqCenter(snickerBlock,fo,j,k,ambientTemp)
        snickerBlock[0] = np.copy(snickerBlock[1])
        time += 1
        
        if (time == int(doneTime*.25)) or (time == int(doneTime*.5)) or (time == int(doneTime*.75)):
            File.write(str('\nTime: {:.1f}'.format((time*dt))+'\n').encode())
            np.savetxt(File, snickerBlock[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')
            
        elif snickerBlock[searchSlotZ,searchSlotY,searchSlotX] < internalTempFind:
            File.write(str('\nTime: {:.1f}'.format((time*dt))+'\n').encode())
            np.savetxt(File, snickerBlock[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')
    
    File.close()


Snickers("snickers.txt")