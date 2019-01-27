#F = GmM/r^2
#r'' = -GmM*r^(-3)*r

def main(tau_days,beta,npts):
    import numpy as np
    import matplotlib.pyplot as plt

    tau = tau_days*24.*60.*60. #convert input [days] to [seconds]

    G = 6.67e-11 #gravitational constant [m^3/kg/s^2]
    mE = 6.e24 #earth mass [kg]
    ecc = 0.017
    mS = 2.e30 #sun mass [kg]
    rAU = 1. #orbital radius [AU]
    rE = rAU*1.49e11 #earth orbital radius [m]

    # We now use information in the table to compute initial conditions:
    # given eccentricity = e and major/minor radii of ellipse a,b:
    # then using (a+b)/2 = r and sqrt(1-b^2/a^2)=e we get:
    # r/a = (1+sqrt(1-e^2))/2.
    # Then assuming we start at the major radius location of the ellipse:
    # first we compute total energy->
    # GMm/r^2 = mv^2/r --> v = sqrt(GM/r)
    # Etot = 1/2mv^2 - GMm/r
    # Then v(a) = sqrt(2/m*(Etot-U(a))
    # where U(a) is the gravitational potential at the major radius location

#    E0 = 1/2*mE*20000.**2 #Earth orbital energy [J]
#    v0 = np.sqrt(2*E0/mE)
    v0 = np.sqrt(G*mS/rE)
    E0 = 1/2.*mE*v0**2-G*mE*mS/rE
    x0 = 2.*rE/(1+np.sqrt(1-ecc**2))
    Ux0 = -G*mE*mS/abs(x0)
    va = np.sqrt(2*(E0-Ux0)/mE)

    x = np.zeros(npts)
    y = np.zeros(npts)
    xp = np.zeros(npts)
    yp = np.zeros(npts)
    K = np.zeros(npts)
    U = np.zeros(npts)
    Etot = np.zeros(npts)

    x[0] = x0
    y[0] = 0.
    xp[:2] = 0.
    yp[:2] = va
    K[:2] = E0-Ux0
    U[:2] = Ux0
    Etot[:2] = [E0,E0]
#    print(Etot[:5])
#    stop
#    xp = np.array([0.,0.])
#    yp = np.array([v0,v0])
#    K = np.array([E0,E0])
#    U = np.array([G*mE*mS/rE,G*mE*mS/rE])
#    Etot = np.array([K+U,K+U])
    #print(x[0],rE,E0,v0)
    #stop

    #iterate method to build array
    i = 1
    while i < npts:

        if i > 0: #ignore first point
            y[i] = y[i-1]+tau*yp[i-1]
            x[i] = x[i-1]+tau*xp[i-1]
            #y = np.append(y,y[i-1]+tau*yp[i-1])
            #x = np.append(x,x[i-1]+tau*xp[i-1])
        if i > 1:
            r = np.sqrt(x[i-1]**2 + y[i-1]**2)
            theta = np.arctan2(y[i-1],x[i-1])
            fx = -G*mE*mS*r**(-(beta-1))*np.cos(theta)
            fy = -G*mE*mS*r**(-(beta-1))*np.sin(theta)
            yp[i] = yp[i-1]+tau*fy/mE
            xp[i] = xp[i-1]+tau*fx/mE
            #yp = np.append(yp,yp[i-1]+tau*fy/mE)
            #xp = np.append(xp,xp[i-1]+tau*fx/mE)
            ken = 1/2.*mE*(xp[i-1]**2 + yp[i-1]**2)
            pen = -G*mE*mS/abs(r)
            K[i] = ken
            U[i] = pen
            Etot[i] = ken+pen
            #K = np.append(K,ken)
            #U = np.append(U,pen)
            #Etot = np.append(Etot,K+U)

        i += 1
        
    tE = np.arange(len(y))*tau_days+1 #time array of npts at tau spacing

############

    fig = plt.figure()
    plt.suptitle('Earth Motion, tau = '+str(tau_days)+' days')
    fig.subplots_adjust(hspace=0.5)

    plt.subplot(2,2,1)
    plt.plot(x,y,'b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.gca().set_aspect('equal', adjustable='box')


    plt.subplot(2,2,2)
    plt.plot(xp,yp,'r')
    plt.xlabel("x'(t)")
    plt.ylabel("y'(t)")
    plt.gca().set_aspect('equal', adjustable='box')


    plt.subplot(2,1,2)
    plt.plot(tE,K,'b')
    plt.plot(tE,U,'r')
    plt.plot(tE,Etot,'k')
    plt.legend(['K','U','Etot'])
    plt.xlabel('time (days)')
    plt.ylabel('Energy (J)')

    plt.show()
