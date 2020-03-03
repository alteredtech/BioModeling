import numpy as np 
import math
np.set_printoptions(precision = 4, suppress=True)

def problem1():
    A0 = np.array([[1,2,3,4],
                   [2,4,5,6],
                   [7,8,5,-2],
                   [4,1,2,3]])

    B0 = np.array([[5],
                   [8],
                   [1],
                   [5]])

    Y0 = np.linalg.solve(A0,B0)

    print(Y0)

def problem2():
    matrixA = np.array([[0,-1,.24,0,0,.25],
                        [-2,0,.49,2,1,.31],
                        [0,-3,1.77,0,2,1.55],
                        [0,0,1,1,0,1],
                        [0,0,1,0,0,0],
                        [0,0,0,0,0,1]])
    matrixB = np.array([[0],
                        [6],
                        [12],
                        [6],
                        [3.46],
                        [.785]])
    matrixC = np.linalg.solve(matrixA,matrixB)

    print(matrixC)

def equationRight(array,i,j,dx,dt):
    return (dt/dx**2)*(array[i-1,j+1])+(2-2*(dt/dx**2))*array[i-1,j]+(dt/dx**2)*array[i-1,j-1]

def equationLeft(array,i,j,dx,dt):
    return -(dt/dx**2)*(array[i,j+1])+(2+2*(dt/dx**2))*array[i,j]-(dt/dx**2)*array[i,j-1]

def finite(alpha,Uarray,i,j,dx,dt):
    return ((alpha * (Uarray[i-1,j+1]-2*Uarray[i-1,j]+Uarray[i-1,j-1])/dx**2) * dt) + Uarray[i-1,j]

def analytical(num,Uarray,i,j):
    return ((1/num**2)*(math.sin(.5*math.pi*num))*(math.sin(num*math.pi*Uarray[0][j]))*(math.exp((-num**2)*(math.pi**2)*(Uarray[i][0]))))

def implicit(sizeArr=11,finalTime=.1,dt=1/1000,printTime=.02,dx=.1,leftCE=-.1,centerCE=2.2,rightCE=-.1,FileName="Implicit.txt"):
    count = 0
    timeList = []
    sizeArrY = int((finalTime/dt))+1
    storageMatrix = np.zeros([sizeArrY,sizeArr],dtype = float)
    matrixA = np.zeros([sizeArr,sizeArr],dtype = float)

    for i in range(sizeArr-1):
        if i == 0:
            matrixA[0,0] = 1
            matrixA[sizeArr-1,sizeArr-1] = 1
        else:
            matrixA[i,i-1] = -(dt/dx**2)
            matrixA[i,i] = (2+2*(dt/dx**2))
            matrixA[i,i+1] = -(dt/dx**2)

    
    for j in range(len(storageMatrix[0])):
        if j < int(len(storageMatrix[0])/2+1):
            storageMatrix[0,j] = (2*(j*dx))
        else:
            storageMatrix[0,j] = (2*(1-(j*dx)))
    tempMatrix = np.copy(storageMatrix)
    
    
    for i in range(1,sizeArrY):
        timeList.append(count*dt)
        matrixC = np.zeros([sizeArr],dtype=float)
        for j in range(1,sizeArr-1):
            matrixC[j] = equationRight(storageMatrix,i,j,dx,dt)
        matrixC = np.reshape(matrixC,(-1,1))
        matrixD = np.linalg.solve(matrixA,matrixC)
        matrixD = matrixD.flatten()
        storageMatrix[i] = np.copy(matrixD)
        count += 1
        
    timeList.append(count*dt)
    timeList = np.reshape(timeList,(-1))
    storageMatrix = np.column_stack((timeList,storageMatrix))
    np.savetxt(FileName,storageMatrix,fmt='%.4f',delimiter=',',newline='\r\n',comments='',header='implicit')
    print(storageMatrix[:int(printTime/dt)+1])

def problemFinite(dt=.001,dx=.1,FinalTime=.1,alpha=1,ArrayX=11,FileName="Finite.txt"):
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
                Uarray[i][j] = finite(alpha,Uarray,i,j,dx,dt)
    Uarray = np.vstack((np.arange(0,(ArrayX)*dx,dx),Uarray))
    Uarray = np.column_stack((np.arange(0,(ArrayY+1)*dt,dt),Uarray))
    np.savetxt(FileName, Uarray, delimiter=',', newline='\r\n', comments='',fmt='%.4f')

def problemAnalytical(dt=.001,dx=.1,FinalTime=.1,alpha=1,ArrayX=12,num=1000,FileName="Analytical.txt"):
    ArrayY=int(FinalTime/dt)+1
    Uarray = np.zeros((ArrayY, ArrayX), dtype=float)

    tempNum = 0
    for k in range(len(Uarray) - 1):
        Uarray[k + 1][0] = tempNum
        tempNum += .001
    tempNum = 0
    for m in range(len(Uarray[0]) - 1):
        Uarray[0][m + 1] = tempNum
        tempNum += .1

    # does all the data calculations
    for i in range(len(Uarray)):
        for j in range(len(Uarray[i])):
            tempNum = 0
            if i == 1 and j >= 2:
                if j <= int(len(Uarray[0])/2):
                    Uarray[i][j] = (2 * Uarray[0][j])
                else:
                    Uarray[i][j] = (2 * (1 - Uarray[0][j]))
            elif (j >= 2 and j < len(Uarray[0])-1) and i > 1:
                for n in range(1,num):
                    tempNum += analytical(n,Uarray,i,j)
                Uarray[i][j] = (8/math.pi**2)*tempNum
    np.savetxt(FileName, Uarray, delimiter=',', newline='\r\n', comments='',fmt='%.4f')

# problem1()
# problem2()
implicit()
# problemFinite()
# problemAnalytical()