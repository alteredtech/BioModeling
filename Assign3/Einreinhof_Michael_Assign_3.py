import math
import numpy

def genPrimeList():
    print("____Problem 1____\n")

    #generates a prime list
    primeList = [x for x in range(2,10001) if all(x%y != 0 for y in range(2,x))]
    print("amount of prime numbers " + str(len(primeList)))

    #gets the list, finds the length of list and iterates from end back 10
    print("Last 10 prime numbers: ")
    print(*primeList[:-11:-1], sep = "\n")

def genFactList():
    print("\n\n\n____Problem 2____\n")
    #generates a list of factorial numbers
    factlist = [factorial(num) for num in range(1,101)]

    lastFactList = []
    #generating a list of the last 10 of the previous list factorials
    for x in range(1,10):
        #takes them off and adds them to the new list
        lastFactList.append(factlist.pop())

    for i in range(0,9):
        print("\nnumber {} of factorial 1-100: ".format(i+1) + str(factlist[i]))
        print("number {} of the new factorial list: ".format(i+1) + str(format(lastFactList[i],"5.2E")))

def printMatrix():
    print("\n\n\n____Problem 3____\n")
    #making the matrix
    matrix = [[1,4,7],[2,5,8],[3,6,9]]
    #iterates through the matrix
    for i in range(len(matrix)):
        print()
        for j in range(len(matrix[i])):
            if j != (len(matrix[i])-1):
                print(str(matrix[j][i]).rjust(2), end=", ")
            else:
                print(str(matrix[j][i]).rjust(2), end=" ")

def np():
    print("\n\n\n____Problem 4____")
    #creates an array with all zeros
    arr = numpy.zeros([21,3], dtype=object)
    x = 0
    #adding x to the array index and increasing x
    for i in range(0,21):
        arr[i,0] = x
        x = x+1
    #takes the array index to the left and multiples its value by 3
    for j in range(0,21):
        arr[j,1] = arr[j,0] * 3
    #takes the array element to the left and up one, multiples it by 2
    for k in range(1,21):
            arr[k,2] = 2 * arr[k-1,1]
    #interates through the array
    for m in range(len(arr)):
        print()
        for n in range(len(arr[m])):
            if n != (len(arr[m])-1):
                print(str(arr[m][n]).rjust(3), end=", ")
            else:
                print(str(arr[m][n]).rjust(3), end=" ")

def factorial(num):
    #uses recursion to get factorials
    if num == 1:
        return num
    else:
        return num * factorial(num - 1)

def main():
    genPrimeList()
    genFactList()
    printMatrix()
    np()

main()