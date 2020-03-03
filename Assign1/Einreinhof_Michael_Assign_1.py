import math
import getpass
# problem 1
def squareNumber(num):
    print("Problem 1: " + str(num**2))
# problem 2
def getStringOfSquaredNumber(num):
    print("Problem 2: " + str(num) + '^2 = ' + str(squareNumber(num)))
# problem 3
def getUsersName():
    name = input("what is your name? ")
    print("Problem 3: Your name is " + name)
    #print('Problem 3: This account name is ' + getpass.getuser())
#problem 4
def problem4():
    alpha = -1.3345
    beta = 2.1212
    gamma = 0.9876

    print("Problem 4:")
    print("4a: " + str(alpha/(beta*gamma)))
    print("4b: " + str((5/(3*alpha))*math.pow(beta,2.35)*math.pow(math.e,(-2.0/3))))
    print("4c: " + str(math.cos(gamma/(beta+alpha))))
    print("4d: " + str(math.tan(gamma)))
    print("4e: " + str(math.atan(math.tan(gamma))))
    print("4f: " + str((abs(math.sin(gamma)-math.cos(gamma)))/3))
    print("4g: " + str(math.log(beta)))
    print("4h: " + str(math.log10(beta)))
    print("4i: " + str(math.cosh(gamma)))
    return

if __name__ == "__main__":

    squareNumber(89)
    getStringOfSquaredNumber(106)
    getUsersName()
    problem4()