import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

np.set_printoptions(precision = 4, suppress=True)

def bacterial():
    bacGrowth = np.loadtxt("Avg_Growth.txt", delimiter=',', skiprows=1)
    #print(bacGrowth)
    plt.title("Average Growth vs Time")
    plt.xlabel("Time Hr")
    plt.ylabel("Average bacterial growth")
    plt.plot(bacGrowth[:,0],bacGrowth[:,1])
    plt.show()

def PredPreyPlot():
    predPray = np.loadtxt("PredPreyModelDefault.txt", delimiter=',', skiprows=1)
    #print(predPray)

    #makes first graph
    fig,plot1 = plt.subplots()
    line1, = plot1.plot(predPray[:,0], predPray[:,1], c='blue')

    #puts the second data on the same graph but on a second axis
    plot2 = plot1.twinx()
    line2, = plot2.plot(predPray[:,0], predPray[:,2], c='red')

    #title
    plt.title("Predator vs Prey Model")
    #axis labels
    plot1.set_xlabel("Time Years")
    plot1.set_ylabel("Hare Population", color='blue')
    plot2.set_ylabel("lynx Population", color='red')
    #legends
    plot1.legend((line1,line2), ('Hare','Lynx'), loc='lower right')

    plt.show()

def stonks():
    stonksData = np.loadtxt("BTC-USD_Altered.txt",delimiter=',',skiprows=1)
    #print(stonksData)
    plt.title("Open Price of BTC")
    plt.xlabel("Time days")
    plt.ylabel("Open Price")
    plt.plot(stonksData[:, 0], stonksData[:, 1])
    plt.show()
    plt.title("High price of BTC")
    plt.xlabel("Time days")
    plt.ylabel("High Price")
    plt.plot(stonksData[:, 0], stonksData[:, 2])
    plt.show()
    plt.title("Low Price of BTC")
    plt.xlabel("Time days")
    plt.ylabel("Low Price")
    plt.plot(stonksData[:, 0], stonksData[:, 3])
    plt.show()
    plt.title("Volume of BTC")
    plt.xlabel("Time days")
    plt.ylabel("Volume")
    plt.plot(stonksData[:, 0], stonksData[:, 4])
    plt.show()

    print("Stocks: I would buy BTC since you are investing in the future of currency. It is back by the people and not the government "
          "which prevents inflation since there is no way for them to make more bitcoin as there is a finite amount. You are "
          "able to track where all bitcoin. You are also anonymous while using this currency.")

def swr():
    swrData = np.genfromtxt("SWR.csv",delimiter=',')
    #print(swrData)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = swrData[0,1:]
    y = swrData[1:,0]
    z = swrData[1:,1:]

    x, y = np.meshgrid(x, y)
    surf_plot = ax.plot_surface(x,y,z, cmap='YlOrRd')
    ax.set_xlabel("Inch addition")
    ax.set_ylabel("Frequency")
    ax.set_zlabel("Power")
    fig.colorbar(surf_plot)
    plt.show()
    print("SWR: About 436MHz will be the best.")


def main():
    bacterial()
    PredPreyPlot()
    stonks()
    swr()

main()