    #d2x/dt2 + kdx/dt + x^3 = Bcos(t)
    #ASSUME x(0) = x'(0) = 1 ??

def main(k,B,tau,npts,log=False):
    import scipy.integrate as integrate
    import numpy as np
    import matplotlib.pyplot as plt

    #npts = 5
    #tau = 1
    #B = 1
    #k = 0
    index = np.arange(npts)
    t = np.arange(npts)*tau +1 #time array of npts at tau spacing
    x = np.ones(npts)
    xp = np.ones(npts)
    
    for i in index:
        if i > 0: #ignore first pt
            x[i] = x[i-1]+tau*xp[i-1]
        if i > 1:
            xp[i] = xp[i-1]+tau*(B*np.cos(t[i])-x[i-1]**3-k*xp[i-1])

    print(x)
    if log:
        plt.semilogy(t,x,'b')
        plt.semilogy(t,xp,'r')
    else:
        plt.plot(t,x,'b')
        plt.plot(t,xp,'r')
    plt.title('k='+str(k)+', B='+str(B)+', tau='+str(tau)+', npts='+str(npts))
    plt.legend(['x(t)',"x'(t)"])
    plt.xlabel('time')
    plt.show()
