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

def Problem1():
    header = 'Problem 1'
    #creates two arrays
    Uarray = np.zeros([2,11,21], dtype= float)
    StackedArray = np.zeros([1,11, 21], dtype=float)
    dx = .01 #meter
    dy = .01 #meter
    dt = .1 #day
    alpha = 0.283*(10**-4) #diffusion
    File = open('2DArray.txt','wb')
    File.write(str(header).encode())

    #setting outside boundaries 
    for k in range(len(Uarray[0])):
        for m in range(len(Uarray[0,1])):
            if k == 0 or k == 10:
                Uarray[0,k,m] = 20
                StackedArray[0,k,m] = 20
            elif m == 0 or m == 20:
                Uarray[0,k,m] = 20
                StackedArray[0,k, m] = 20

    time = 0
    Uarray[1] = np.copy(Uarray[0])
    File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
    np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')

    #keep going until the center value is met
    while(Uarray[0][5][10] < 19):

        for i in range(1,len(Uarray[0])-1):
            for j in range(1,len(Uarray[0,i])-1):
                Uarray[1][i][j] = (equationX(0,i,j,Uarray,alpha,dx,dt) + equationY(0,i,j,Uarray,alpha,dy,dt)) + Uarray[0][i][j]
        Uarray[0] = np.copy(Uarray[1])
        time += 1

        #print the plate at 25%, 50%, 75%, 100%
        if round((time*dt),3)%25 == 0:
            File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
            np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')

        elif round(time*dt,2) >= 99.9:
            File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
            np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')
    File.close()
    
def Problem2():
    header = 'Problem 2'
    #creates two arrays
    Uarray = np.zeros([2,11,11], dtype= float)
    File = open('2DArrayP2.txt','wb')
    File.write(str(header).encode())
    dx = .02 #meter
    dy = .01 #meter
    dt = .1 #day
    alpha = 0.283*(10**-4) #diffusion

    #setting outside boundaries 
    for k in range(len(Uarray[0])):
        for m in range(len(Uarray[0,1])):
            if k == 0 or k == 10:
                Uarray[0,k,m] = 20
            elif m == 0 or m == 10:
                Uarray[0,k,m] = 20

    time = 0
    Uarray[1] = np.copy(Uarray[0])
    File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
    np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')

    #keep going until the center value is met
    while(Uarray[0][5][5] < 19):

        for i in range(1,len(Uarray[0])-1):
            for j in range(1,len(Uarray[0,i])-1):
                Uarray[1][i][j] = (equationX(0,i,j,Uarray,alpha,dx,dt) + equationY(0,i,j,Uarray,alpha,dy,dt)) + Uarray[0][i][j]
        Uarray[0] = np.copy(Uarray[1])
        time += 1

        if round(time*dt, 3)%25 == 0:
            File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
            np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')
            
        elif round(time*dt, 3) >= 99.8:
            File.write(str('\nTime: {:.1f}'.format(time*dt)+'\n').encode())
            np.savetxt(File, Uarray[0], fmt='%.4f', delimiter=",", comments='', newline='\r\n')
    File.close()
        
def Problem3():
    header = 'Problem 3'
    Uarray = np.zeros([21,21,21], dtype= float)
    NewArray = np.zeros([21, 21, 21], dtype=float)
    dx = .01 #meter
    dy = .01 #meter
    dz = .01 #meter
    dt = 1 #second
    alpha = (54/(7800*(.46*10**3)))

    for l in range(len(Uarray)):
        for k in range(len(Uarray[0])):
            for m in range(len(Uarray[0,1])):
                if (k == 0 or k == 20) and (l>0 and l<20):
                    Uarray[l,k,m] = 40
                elif (m == 0 or m == 20) and (l>0 and l<20):
                    Uarray[l,k,m] = 40
                elif l == 0:
                    Uarray[l,k,m] = 150
                elif l == 20:
                    Uarray[l,k,m] = 40
                else:
                    Uarray[l,k,m] = 20

    time = 0
    NewArray = np.copy(Uarray)
    while(Uarray[10,10,10]<35):
        for h in range(1,len(Uarray)-1):
            for i in range(1,len(Uarray[0])-1):
                for j in range(1,len(Uarray[0,i])-1):
                        Uarray[h][i][j] = (equationX(h,i,j,NewArray,alpha,dx,dt) + equationY(h,i,j,NewArray,alpha,dy,dt)+ equationZ(h,i,j,NewArray,alpha,dz,dt)) + NewArray[h][i][j]

        NewArray = np.copy(Uarray)
        time +=1
        if Uarray[10][10][10] > 35:
            temp = np.copy(Uarray[:,:,10])
            temp = np.vstack((temp,Uarray[:,10,:]))
            np.savetxt('3DArrayP3Cross.txt', temp, fmt='%.4f', delimiter=",", comments='', newline='\r\n',
                       header=header)

def Problem3a():
    header = 'Problem 3a\n'
    Uarray = np.zeros([21,21,21], dtype= float)
    NewArray = np.zeros([21, 21, 21], dtype=float)
    temp = np.arange(0,22,dtype=float)
    File = open('3DArrayColumn.txt','wb')
    File.write(str(header).encode())
    dx = .01 #meter
    dy = .01 #meter
    dz = .01 #meter
    dt = 1 #second
    alpha = (54/(7800*(.46*10**3)))

    for l in range(len(Uarray)):
        for k in range(len(Uarray[0])):
            for m in range(len(Uarray[0,1])):
                if (k == 0 or k == 20) and (l>0 and l<20):
                    Uarray[l,k,m] = 40
                elif (m == 0 or m == 20) and (l>0 and l<20):
                    Uarray[l,k,m] = 40
                elif l == 0:
                    Uarray[l,k,m] = 150
                elif l == 20:
                    Uarray[l,k,m] = 40
                else:
                    Uarray[l,k,m] = 20

    time = 0
    NewArray = np.copy(Uarray)

    while(Uarray[10,10,10]<58.2):
        for h in range(1,len(Uarray)-1):
            for i in range(1,len(Uarray[0])-1):
                for j in range(1,len(Uarray[0,i])-1):
                        Uarray[h][i][j] = (equationX(h,i,j,NewArray,alpha,dx,dt) + equationY(h,i,j,NewArray,alpha,dy,dt)+ equationZ(h,i,j,NewArray,alpha,dz,dt)) + NewArray[h][i][j]

        NewArray = np.copy(Uarray)
        time +=1

        if time%50==0:
            File.write(str('Time:, {:.1f}'.format(time)+', ').encode())
            temp = np.copy(Uarray[:,10,10]).reshape(1,21)
            np.savetxt(File, temp, fmt='%.4f', delimiter=",", comments='')

        if Uarray[10][10][10] > 58.2:
            File.write(str('Time:, {:.1f}'.format(time)+', ').encode())
            temp = np.copy(Uarray[:,10,10]).reshape(1,21)
            np.savetxt(File, temp, fmt='%.4f', delimiter=",", comments='')
            File.close()
        print(Uarray[10][10][10])

#Problem1()
#Problem2()
# Problem3()
#Problem3a()