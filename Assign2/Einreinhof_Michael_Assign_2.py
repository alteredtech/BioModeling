def ifElse(x,y,z):
    if(x<y):
        x = x*2
        if(x>z):
            z=z*5
        else:
            z=(z*1.0)/2
    else:
        y=y*3
    return x,y,z

def whileLoop(x):
    while(x <= 107):
        x = x * 3.0
        print(x)
    while (x > 5):
        x = (x*1.0) / 5
        print(x)
    return x

def getFactorial():
    for num in range(1, 11):
        fac = 1
        for i in range(1, num + 1):
            fac = fac * i
        print(str(num) + " factorial is " + str(fac))

def findPrime():
    for p in range(2, 11):
        for i in range(2, p):
            if p % i == 0:
                print(str(p) + " is not prime")
                break
        else:
            print (str(p) + " is prime")

if __name__ == "__main__":
    print("problem 1a: x=3, x=12, x=1 " + str(ifElse(3,12,1)))
    print("problem 1b: x=6, x=5, x=2 " + str(ifElse(6,5,2)))
    print("problem 2: while loop ")
    str(whileLoop(7))
    print("problem 3: factorial values ranging from 1 - 10 ")
    str(getFactorial())
    print("problem 4: prime numbers ranging from 2-10 ")
    str(findPrime())
