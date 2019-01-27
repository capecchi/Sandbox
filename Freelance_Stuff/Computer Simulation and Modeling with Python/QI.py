#F = GmM/r^2-kv^2
#y'' = -GmM*y^(-2) + k*(y')^2

def main(tau):
    import numpy as np
    import matplotlib.pyplot as plt

    k = 2.e-4 #air resistance constant [kg/m]
    m1 = 2. #falling mass [kg]
    rE = 6371000. #mean earth radius [m]
    G = 6.67408e-11 #gravitational constant [m^3/kg/s^2]
    mE = 5.972e24 #earth mass [kg]
    
    #a) Euler method
    y = np.array([rE+5000.]) #height + earth radius
    yp = np.array([0.,0.]) #y'[0] = 0 (initially at rest)

    i = 1
    while y[-1] >= rE:
        if i > 0: #ignore first pt
            y = np.append(y,y[i-1]+tau*yp[i-1])
        if i > 1:
            yp = np.append(yp,yp[i-1]+tau*(-G*m1*mE*y[i-1]**(-2) + k*yp[i-1]**2))
        i += 1
    tE = np.arange(len(y))*tau+1 #time array of npts at tau spacing
    hE = y-rE
    aE = yp
    
    #b) Euler-Richardson method
    y = np.array([rE+5000.]) #height + earth radius
    yp = np.array([0.]) #y'[0] = 0 (initially at rest)
    #ypp = np.array([-9.8]) #initial acceleration -9.8m/s^2

    i = 1
    while y[-1] >= rE:
        ypp = -G*m1*mE*y[i-1]**(-2)+k*yp[i-1]**2
        ymid = y[i-1] + tau/2.*yp[i-1]
        ypmid = yp[i-1] + tau/2.*ypp
        yppmid = -G*m1*mE*ymid**(-2)+k*ypmid**2

        if i > 0: #ignore first pt
            y = np.append(y,y[i-1]+tau*ypmid)
            yp = np.append(yp,yp[i-1]+tau*yppmid)
        i += 1
    tER = np.arange(len(y))*tau+1 #time array of npts at tau spacing
    hER = y-rE
    aER = yp

############


    plt.plot(tE,hE,'b')
    plt.plot(tE,aE,'b.')
    plt.plot(tER,hER,'r')
    plt.plot(tER,aER,'r.')
    plt.title('tau='+str(tau)+'s')
    plt.legend(['y(t) Euler',"y'(t)",'y(t) Euler-Richardson',"y'(t)"])
    plt.xlabel('time')
    plt.show()
