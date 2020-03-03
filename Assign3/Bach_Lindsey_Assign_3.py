#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:34:39 2019

@author: lindseybach7
"""
#Bach_Lindsey_Assign_3

import numpy as np 

#Problem 1 

#partA--- generate a list that contains all the prime numbers from 1 to 10,000 using list comprehension

def isNumberPrime(n):#function from Assignment 2
    if n>1: #number has to be greater than 1 to be prime 
        for x in range(2,n): #for loop starting with value 2 as prime
            if (n % x)== 0: #check divisibility with mod function 
                return False 
        else:
            return True 
    else: 
        return False

def Problem1():
    listComp = [x for x in range(1,10000) if isNumberPrime(x)]
    print(listComp)

#partB--- output the total number of prime numbers there are in the list created in part a 
    print(len(listComp))

#partC--- output the last 10 numbers of the list of prime numbers to the console, each separated by new line 
    #print(listComp[-10:])
    print(*listComp[-10:], sep = "\n")



#Problem 2 

#partA--- generate a list of factorials using numbers from 1-100 using list comprehension 
def Factorial(n):
    factorial=1 #initialize as 1
    if n<0:
        return None
    elif n==0:
        return 1 
    else: 
        while(n>0): 
            factorial= factorial*n 
            n=n-1 
    return(factorial)
    
def Problem2():
    listComp2 = [Factorial(x) for x in range(1,101)]#use 101 beccause of the iterator in python 
    print(listComp2)

#partB--- remove last 10 numbers from the list of factorials and add them to new list 
    newList= []
    
    #utilize for loop and combine append and pop to remove last 10 numbers from factorial list and add to new list 
    for x in range(10):
        (newList.append(listComp2.pop()))
        print(newList[x])
  
#partC--- output first 10 numbers from each of 2 lists generated in parts a and b to console. each number separated by new line 
    #** make it easy to tell which numbers belong to each list by including header line 
    print("listComp2", *listComp2[:10], sep = "\n")
    print("newList", *newList[:10], sep = "\n")
    


#Problem 3 

#partA--- create the matrix shown in problem statement 

def Problem3(): 
    
#NOT supposed to use numpy for this part??? !    
#utilize nested forloops and numpy to create 3x3 matrix 
    #import numpy as np
    #iterateOverArray= np.zeros([3,3])
    #x=1 
    #for i in range(3):
        #for j in range(3):
            #iterateOverArray[i,j]=x 
            #x=x+1
   # print(iterateOverArray, end = ' ') #NOT SURE IF THIS IS RIGHT??! 
    

#partB--- output numbers of matrix to console in a format that looks like prob statement (use nested forloops)
    #FIX THIS SHIT LINDSEY- YOU NEED COMMAS GIRL!!! 
    
    #(Hint: you can separate the values printed using the keyword "end" in the 
    #print function like "print(object, end = ' ')"This will make it so the print
    #statement will not go to the next line.
   
    matrix3 = np.zeros([3,3], int)#get rid of decimals
    x=1
    for i in range(3):
       for j in range(3):
           matrix3 [i][j]= x
           x = x+1 
           
    for i in range(3):
        print()#blank line
        for j in range(3):
            if (j != 2):
                print(str(matrix3[i][j]).rjust(4), end = ', ') #utilize rjust to separate values nicely
            else: 
                print(str(matrix3[i][j]).rjust(4), end = '')





#Problem 4 

#partA--- Develop code to generate a matrix that is 21 x 3 in size using numpy.	
def Problem4():
    matrix= []
    
    #partB--- Set all the top row’s values equal to 0.
    matrix= np.zeros([21,3], int)#get rid of decimals
    
    #partC--- In the first column, set the numbers equal to the values 1-20, 1 being the second value and 20 being the last 
    for i in range(1,21):
        for j in range(1):
            matrix[i][0]= i 
            #partD--- In the second column, set the numbers equal to the number to the left of it multiplied by 3
        matrix[i][1]= matrix[i][0]*3
            #partE--- In the third column, set the values equal to the number 2 multiplied by the value of the cell 
            #in the position 1 to the left and 1 above it.   
        matrix[i][2]= matrix[i-1][1]*2
    
    #partF--- Finally output the array to the console so it looks like a 2D array with distinct rows and 
    #columns (use nested for loops). 
    #make another forloop to iterate and print out values and commas 
    for i in range(21):
        print()#blank line
        for j in range(3):
            if matrix[j][2]:
                print(str(matrix[i][j]).rjust(4), end = ' ') #utilize rjust to separate values nicely 
            else: 
                print(str(matrix[i][j]).rjust(4), end = ',')


def main():
    Problem4()

main()

        
    
  


  




    
    
    

    
    




















#Reorganize code/prob 1a...etc and check what needs to be printed! 
    
    
    