import numpy as np

np.set_printoptions(precision = 4, suppress=True)

def Problem1():
    labels = 'ml_base , pH_buffer'
    sensorData = np.loadtxt('mV_Sensor.txt', delimiter=',')
    # print(sensorData)
    #copys array to make a numpy array from the sensor data
    newSensorData = np.array(sensorData)
    for i in range(len(sensorData)):
        newSensorData[i][0] = newSensorData[i][0]*1000
    for i in range(len(sensorData[1])):
        newSensorData[i][1] = newSensorData[i][1]/290
    np.savetxt('pH_Sensor.txt', newSensorData, fmt=['%d','%.3f'], delimiter=',', newline='\r\n', header= labels, comments='')

def Problem2():
    labels = 'time in hours, average'
    growthData = np.loadtxt('Bacterial_Growth.txt', delimiter=',')
    
    #making an empty array
    newArr = np.empty([len(growthData),2])
    for i in range(len(growthData)):
        x = 0
        for j in range(1,len(growthData[i])):
            x += growthData[i][j]
        newArr[i][1] = (x/4)
        newArr[i][0] = i

    np.savetxt("Avg_Growth.txt", newArr, fmt=['%d','%.3f'], delimiter=',',comments='',header=labels,newline='\r\n')

def PredPrey(n0,p0,K,H,R,s,a,b,step,inc,fileName):
    #all variables
    labels = 'quarter years, hare pop, lynx pop'
    model = Create2DArr(step,3)
    x = 0
    for j in range(step):
        model[j][0] = x
        # if time is zero it sets the initial population
        if j == 0:
            model[0][1] = n0
            model[0][2] = p0
        # all the modeling calculations
        else:
            N = model[j-1][1]
            P = model[j-1][2]
            model[j][1] = (N + PreyEq(N,R,K,a,b,P)*inc)
            model[j][2] = (P + PredEq(P,s,H,N)*inc)
        x += .25
    np.savetxt(fileName,model,fmt=['%.2f','%.4f','%.4f'],comments='',header= labels,delimiter=',', newline='\r\n')

def PredPreyDrought(n0,p0,K,H,R,s,a,b,step,inc,fileName):
    #all variables
    labels = 'quarter years, hare pop, lynx pop'

    model = Create2DArr(step,3)
    x = 0
    for j in range(step):
        model[j][0] = x
        #if time is zero it sets the initial population
        if j == 0:
            model[0][1] = n0
            model[0][2] = p0
        #if the year quarter is 100 which equals 25 years it makes the hare pop equal 2000
        elif j == 100:
            model[j][1] = 2000
        #all the modeling calculations
        else:
            N = model[j-1][1]
            P = model[j-1][2]
            model[j][1] = (N + PreyEq(N,R,K,a,b,P)*inc)
            model[j][2] = (P + PredEq(P,s,H,N)*inc)
        x += .25
    np.savetxt(fileName,model,fmt=['%.2f','%.4f','%.4f'],comments='',header= labels,delimiter=',', newline='\r\n')

def PreyEq(N,r,k,A,B,P):
    #do the prey calculation
    return N*(r*(1-(N/k))-((A*N)/(N**2+B**2))*P)

def PredEq(P,S,h,N):
    #do the pred calculation
    return P*(S*(1-((h*P)/N)))

def Create2DArr(row,col):
    #purpose in life is to create arrays for me
    array = np.empty([row,col])
    return array

def main():
    Problem1()
    Problem2()
    #N0=1000, P0=100, k=10000, h=10, r=.9, S=.3, A=5, B=1000, step=400, inc=.25, filename= PredPreyModel.txt
    PredPrey(1000, 100, 10000, 10, .9, .3, 5, 1000, 401, .25,"PredPreyModelDefault2.txt")
    PredPrey(1000, 100, 10000, 10, .9, .3, 2, 1000, 401, .25, "PredPreyModelA_2.txt")
    PredPrey(1000, 100, 10000, 10, .9, .3, 4, 1000, 401, .25, "PredPreyModelA_4.txt")
    PredPrey(1000, 100, 10000, 10, .9, .3, 6, 1000, 401, .25, "PredPreyModelA_6.txt")
    PredPrey(1000, 100, 10000, 10, .9, .3, 8, 1000, 401, .25, "PredPreyModelA_8.txt")
    PredPreyDrought(1000, 100, 10000, 10, .9, .3, 5, 1000, 401, .25, "PredPreyModelDrought.txt")

main()




