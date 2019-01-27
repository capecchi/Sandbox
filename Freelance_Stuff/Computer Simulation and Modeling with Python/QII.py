#Assuming a source-free region, the electrostatic potential V satisfies the equation:
#del^2V = 0 (Laplacian of V = 0)
#Dropping higher order terms this gives
#Vi,j = (Vi+1,j + Vi-1,j + Vi,j-1 + Vi,j+1)/4

def div0( a, b, val ):
    import numpy as np
    #ignore / 0, div0( [-1, 0, 1], 0 ) -> [val,val,val]
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide( a, b )
        c[ ~ np.isfinite( c )] = val  # -inf inf NaN
    return c

def initial_conditions(part):
    import numpy as np

    if part == 1:
        V = np.ones([11,16])*2.*.7 #set all values to 70% of boundary value
        V[0,:] = 2. #set boundary conditions
        V[:,0] = 2.
        V[10,:] = 2.
        V[:,15] = 2.

    if part == 2:
        V = np.ones([11,16])*2.
        V[1:10,1:15]=0.
        V[5,7:9] = 5. #Assuming these two are the "central sites"?
    if part == 3:
        #Assuming we start with interior sites as in part 2?
        V = np.ones([11,16])*2.
        V[1:10,1:15]=0.
        V[5,7:9] = 5.
        V[0,:] = 2.
        V[10,:] = 2.
        V[:,0] = 1. #Assuming corner values get assigned value = 1.
        V[:,15] = 1.
    if part == 4:
        #Assuming we start with interior sites as in part 2?
        V = np.ones([11,16])*2.
        V[1:10,1:15]=0.
        V[5,7:9] = 5.
        V[0,:] = 2.
        V[10,:] = 2.
        V[:,0] = 2.
        V[:,15] = 0. #Assuming this is the "fourth" side        

    return V   

def main(part):
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.arange(11) #0-10
    y = np.arange(16) #0-15
    V = initial_conditions(part)
    #print(V)
    #stop
    tolerance = 0.01 #set tolerance to 1%
    change = 1.
    iterations = 0
    while change > tolerance: #Assuming this is correct convergence criteria
        iterations += 1
        newV = initial_conditions(part)
        for i in x:
            for j in y:
                if i != 0 and i != 10 and j != 0 and j != 15:
                    #interior value, compute average of neighbor pts
                    newV.itemset((i,j),(V[i-1,j]+V[i+1,j]+V[i,j-1]+V[i,j+1])/4.)
        change = np.max(div0(abs(newV-V),V,0))
        print('change=',change)
        V = newV
    
############

    if 1:
        plt.figure()
        CS = plt.contour(x,y,np.transpose(V))
        plt.clabel(CS,inline=1,fontsize=10)
        plt.title('Jacobi Method, part ' +str(part)+' : '+str(iterations)+' iterations')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
