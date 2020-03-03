#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:40:25 2019

@author: lindseybach7
"""

import numpy as np 

#~~~~~~~~~~~~~~~~~~~~~~~     Problem 1     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

#~~~~~~~~~~~~~~~~~~~~~~~     Problem 2     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

#~~~~~~~~~~~~~~~~~~~~~~~     Problem 3    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	


#~~~~~~~~~~~~~~~~~~~~~~~     Problem 4     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

#design a cooling tunnel for a chocolate enrobing system at the M&M Mars 
#plant in Hackettstown, NJ to cool Snickers candy bars from 33°C to 15°C in the tunnel.  
#The tunnel operates at 5°C.  The warmest point of the Snickers candy bar can be no warmer than 15 °C.
file = open('Snickers.txt', 'wb')
file.write('Snickers\r\n'.encode())



#---------- Initialize Array ----------

#snickers bar dimmensions 33x15x10 (mm)
snickers= np.full([2,11,16],33,float) #initialize array w/ proper dimensions and fill with 33 thoroughout 



#-----------  variables  --------------

Rho = 800 #kg/m^3 
Cp= 2.4*1000 #kJ/kg*K 
K= 0.4 #W/m*K thermal conductivity 
h= 100 #W/M^2K convective rate 

dx= .001 #m 
dy= .001 #m 

dz= .001
dt = 0.01 #seconds
alpha = K/(Rho*Cp)

#temperatures 
temperature = 15 
tunnel_temperature = 5 
Ta = tunnel_temperature 

#create Area and Volume variables to input in equations 
A= dx*dz
V= dx*dy*dz

#area and volume of corners 
A_corners = A/2
V_corners = V/4

#other Area variables 
A_full = A 
V_half = V/2

A_half = A/2
V_full = dx*dy*dz

#set i equal to 1 so that my i-1 is "0" 
i = 1


#--------------   set up txt file   --------------
 
file.write(str('{:.3f}'.format(0)).encode() + '\n'.encode())
np.savetxt(file, np.atleast_2d(snickers[1, :]), fmt='%.3f', delimiter=',', newline='\r\n')
file.write('\n'.encode())

counter = 0 

#--------------  while loop w/ dbl for loop and all 9 equations   -----------------

while snickers [1,10,8] >= temperature:
    counter += 1
    time = counter*dt 
    for j in range (11): #rows
        for k in range (16):#need to add 1 to each for loop range #columns
            if j == 0:
                if k==0: 
                    #top left corner equation! 
                    snickers [i,j,k] = ((A_corners*h)/Rho*Cp*V_corners)*(Ta-snickers[i-1,j,k]*(dt))
                    + ((A_corners*h)/(Rho*Cp*V_corners))*((Ta- snickers[i-1,j,k])*(dt))
                    + ((A_corners*alpha)/(V_corners)) * ((snickers[i-1,j+1,k] - snickers[i-1,j,k])*(dt/dx))
                    + ((A_corners*alpha)/(V_corners)) * ((snickers[i-1,j,k+1] - snickers[i-1,j,k])*(dt/dx))
                    + (snickers[i-1,j,k]) #account for previous step
                elif k==15:
                     #top right corner equation 
                    snickers [i,j,k] = ((A_corners*alpha)/V_corners) * ((snickers[i-1,j-1,k] - snickers[i-1,j,k])*(dt/dx)) 
                    + (((A_corners*h)/(Rho*Cp*V_corners)) * ((Ta- snickers[i-1,j,k])*dt))  
                    + (((A_corners*h)/(Rho*Cp*V_corners)) * ((Ta- snickers[i-1,j,k])*dt)) 
                    + ((A_corners*alpha)/V_corners) * ((snickers[i-1,j,k-1] - snickers[i-1,j,k])*(dt/dx)) 
                    + (snickers[i-1,j,k])
                else:
                    #top side equation 
                    snickers[i,j,k] = ((A_full*h)/(Rho*Cp*V_full))*((Ta-snickers[i-1,j,k])*(dt))
                    + ((A_half*alpha)/V_half) * ((snickers[i-1,j,k+1] - snickers[i-1,j,k]) *(dt/dx)) 
                    + ((A_half*alpha)/V_half) * ((snickers[i-1,j,k-1] - snickers[i-1,j,k]) *(dt/dx)) 
                    + ((A_full*alpha)/V_half) * ((snickers[i-1,j+1,k] - snickers[i-1,j,k]) *(dt/dx)) 
                    + (snickers[i-1,j,k])      
            elif j == 10:
                #print("in j == 10")
                if k ==0:
                    #bottom left corner equation 
                    snickers [i,j,k] = ((A_corners*h)/(Rho*Cp*V_corners)) * ((Ta -snickers[i-1,j,k])*(dt)) 
                    + ((A_corners*alpha)/V_corners)*((snickers[i-1,j-1,k] - snickers[i-1,j,k])*(dt/dx)) 
                    + ((A_corners*alpha)/V_corners)*((snickers[i-1,j,k+1] - snickers[i-1,j,k])*(dt/dx)) 
                    + (0) 
                    + (snickers[i-1,j,k])
                elif k==15: 
                    #bottom right corner equation! 
                    snickers [i,j,k] = ((A_corners*alpha)/V_corners)* ((snickers[i-1,j-1,k] - snickers[i-1,j,k])*(dt/dx)) 
                    + (((A_corners*h)/(Rho*Cp*V_corners)) * ((Ta-snickers[i-1,j,k])*dt)) 
                    + ((A_corners*alpha)/V_corners)* ((snickers[i-1,j,k-1] - snickers[i-1,j,k])*(dt/dx)) 
                    + (0) 
                    + (snickers[i-1,j,k])
                else: 
                    #bottom side equation 
                    #print("bottom side equation")
                    snickers[i,j,k] = (((A_full*alpha)/V_half) * ((snickers[i-1,j-1,k] - snickers[i-1,j,k]) *(dt/dx))
                    + ((A_half*alpha)/V_half) * ((snickers[i-1,j,k+1] - snickers[i-1,j,k]) *(dt/dx)) 
                    + ((A_half*alpha)/V_half) * ((snickers[i-1,j,k-1] - snickers[i-1,j,k]) *(dt/dx)) 
                    + (0)) 
                    + (snickers[i-1,j,k])    
            else: 
                if k==0: 
                    #left side equation! 
                    snickers[i,j,k] = ((A_full*h)/(Rho*Cp*V_full))*(Ta-snickers[i-1,j,k]*(dt))
                    + ((A_full*alpha)/V_half) * ((snickers[i-1,j,k+1] - snickers[i-1,j,k]) *(dt/dx)) 
                    + ((A_half*alpha)/V_half) * ((snickers[i-1,j-1,k] - snickers[i-1,j,k]) *(dt/dx)) 
                    + ((A_half*alpha)/V_half) * ((snickers[i-1,j+1,k] - snickers[i-1,j,k]) *(dt/dx)) 
                    + (snickers[i-1,j,k])
                if k==15: 
                    #print("right side equations")
                    #right side equation 
                    snickers [i,j,k] = ((A_half*alpha)/V_half) * ((snickers[i-1,j,k-1] - snickers[i-1,j,k])*(dt/dx))
                    + ((A_full*h)/(Rho*Cp*V_half)) * ((Ta-snickers[i-1,j,k])*dt) 
                    + ((A_half*alpha)/V_half) * ((snickers[i-1,j-1,k] - snickers[i-1,j,k]) *(dt/dx)) 
                    + ((A_full*alpha)/V_half) * ((snickers[i-1,j+1,k] - snickers[i-1,j,k]) *(dt/dx)) 
                    + (snickers[i-1,j,k])  
                else: 
                    #middle equation 
                    snickers[i,j,k] = ((A_full*alpha)/V_full) * ((snickers[i-1,j,k-1] - snickers[i-1,j,k]) *(dt/dx))
                    + ((A_full*alpha)/V_full) * ((snickers[i-1,j+1,k] - snickers[i-1,j,k]) *(dt/dx))
                    + ((A_full*alpha)/V_full) * ((snickers[i-1,j-1,k] - snickers[i-1,j,k]) *(dt/dx))
                    + ((A_full*alpha)/V_full) * ((snickers[i-1,j,k+1] - snickers[i-1,j,k]) *(dt/dx))
                    + (snickers[i-1,j,k])
                    

    snickers[0]= snickers[1]
    print(counter)
    
    
     
    if time == 50 or time == 100 or time == 150 or round(time,1) >= 199: 
        file.write(str('{:.3f}'.format(time)).encode() + '\n'.encode())
        np.savetxt(file, np.atleast_2d(snickers[1,:]), fmt='%.3f', delimiter=', ', newline = '\r\n')
                    
        
    

    #file.write(str('{:.3f}'.format(time)).encode() + '\n'.encode())
    #np.savetxt(file, np.atleast_2d(snickers[1, :]), fmt='%.3f', delimiter=', ', newline = '\r\n') # IS THIS RIGHT?? !
                    
file.close() 
            