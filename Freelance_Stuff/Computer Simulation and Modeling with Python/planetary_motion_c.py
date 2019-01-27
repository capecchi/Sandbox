#F = GmM/r^2
#r'' = -GmM*r^(-3)*r

def orbit(beta):
    import numpy as np

    tau_days = 10.
    tau = tau_days*24.*60.*60. #convert input [days] to [seconds]
    npts = int(1000000/tau_days)
    G = 6.67e-11 #gravitational constant [m^3/kg/s^2]
    mE = 1.3e22 #pluto mass [kg]
    ecc = 0.248
    mS = 2.e30 #sun mass [kg]
    rAU = 39.26 #orbital radius [AU]
    rE = rAU*1.49e11 #pluto orbital radius [m]

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

    v0 = np.sqrt(G*mS/rE)
    E0 = 1/2.*mE*v0**2-G*mE*mS/rE
    #x0 = 2.*rE/(1+np.sqrt(1-ecc**2))
    x0 = 2.*rE/(1+np.sqrt(1+4*ecc**2/(4*(1-ecc**2)))) #start at minor radius loc
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

    #iterate method to build array
    i = 1
    while i < npts:

        if i > 0: #ignore first point
            y[i] = y[i-1]+tau*yp[i-1]
            x[i] = x[i-1]+tau*xp[i-1]
        if i > 1:
            r = np.sqrt(x[i-1]**2 + y[i-1]**2)
            theta = np.arctan2(y[i-1],x[i-1])
            fx = -G*mE*mS*r**(-(beta-1))*np.cos(theta)
            fy = -G*mE*mS*r**(-(beta-1))*np.sin(theta)
            yp[i] = yp[i-1]+tau*fy/mE
            xp[i] = xp[i-1]+tau*fx/mE
            ken = 1/2.*mE*(xp[i-1]**2 + yp[i-1]**2)
            pen = -G*mE*mS/abs(r)
            K[i] = ken
            U[i] = pen
            Etot[i] = ken+pen
        i += 1
        
    return x,y

def main():
    import matplotlib.pyplot as plt
    import numpy as np

    beta = [4.,3.5,3.1,3.01]
    for b in beta:
        xx,yy = orbit(b)
        if b == 4:
            x1 = xx
            y1 = yy
        if b == 3.5:
            x2 = xx
            y2 = yy
        if b == 3.1:
            x3 = xx
            y3 = yy
        if b == 3.01:
            x4 = xx
            y4 = yy
            
    fig = plt.figure()
    plt.suptitle('Planetary Motion')
    fig.subplots_adjust(hspace=0.5)

    plt.subplot(2,2,1)
    plt.plot(x1,y1,'b')
    plt.xlim(0.5*np.min(x1),1.5*np.max(x1))
    plt.ylabel('beat = 4.0')
    #plt.gca().set_aspect('equal', adjustable='box')


    plt.subplot(2,2,2)
    plt.plot(x2,y2,'r')
    plt.ylabel('beta = 3.5')
    #plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0.5*np.min(x2),1.5*np.max(x2))

    plt.subplot(2,2,3)
    plt.plot(x3,y3,'b')
    plt.ylabel('beat = 3.1')
    #plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0.5*np.min(x3),1.5*np.max(x3))


    plt.subplot(2,2,4)
    plt.plot(x4,y4,'r')
    plt.ylabel('beta = 3.01')
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()

    #It is evident that by raising the exponent in the denominator of the force
    #term, the gravitational attraction falls off much more rapidly and the planet
    #quickly escapes the pull of the star.
