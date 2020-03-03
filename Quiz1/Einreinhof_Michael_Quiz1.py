import math
import numpy as np 
import matplotlib.pyplot as plt

def equationN(F,N,k1,ks,S,V,dt):
    num = ((-F*N+(k1/(1+(ks/S))*N))/V)*dt
    return num

def equationS(F,Sin,S,k2,V,dt,N):
    num = ((F*Sin-F*S-k2*N)/V)*dt
    return num

def quiz():
    labels = 'time half hours, Cell con, Sub con'
    k1 = .35 #/hr
    k2 = .3 #/hr
    ks = 20 #saturation
    flowRate = .1 #lit/hr
    sin = 100 #g/lit
    volume = 10 #lit
    dt = .5
    totalTime = 100

    array = np.zeros([201,3],dtype=float)
    time = 0
    for i in range(len(array)):
        array[i,0] = time
        for j in range(len(array[0])):
            if i == 0:
                array[i,1] = 30
                array[i,2] = 20
                # print(array)
            else:
                N = array[i-1,1]
                S = array[i-1,2]
                array[i,1] = N+equationN(flowRate,N,k1,ks,S,volume,dt)
                array[i,2] = S+equationS(flowRate,sin,S,k2,volume,dt,N)
                # print(array)
        time += .5
    np.savetxt("cell.txt",array,fmt='%.4f',delimiter=',',newline='\r\n',comments='',header=labels)

def Plot():
    array = np.loadtxt("cell.txt", delimiter=',', skiprows=1)
    #print(array)

    #makes first graph
    fig,plot1 = plt.subplots()
    line1, = plot1.plot(array[:,0], array[:,1], c='blue')

    #puts the second data on the same graph but on a second axis
    plot2 = plot1.twinx()
    line2, = plot2.plot(array[:,0], array[:,2], c='red')

    #title
    plt.title("Cell vs Substrate Concentration")
    #axis labels
    plot1.set_xlabel("Time hours")
    plot1.set_ylabel("Cell Concentration g/lit", color='blue')
    plot2.set_ylabel("Substrate Constration g/lit", color='red')
    #legends
    plot1.legend((line1,line2), ('Cell','Sub'), loc='lower center')

    plt.show()

def main():

    quiz()
    Plot()

main()