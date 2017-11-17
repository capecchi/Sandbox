#metric moved to its own file
def main(stock,
         check=False,
         newdata=False,
         test=False,
         write=False,
         trendplot=False,
         scanplot=True,
         newplotdata=False):

    import metric
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import matplotlib.patches as mpatches
    import time
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm


    direc = 'C:/Users/Owner/Desktop/Projects/Upwork/Causa/'
    fsav = direc+stock+'_analysis'

    if test:
        newdata = Falsef
        fsav = direc + 'test'

    if trendplot:
        data = pd.read_csv(direc+'Causa_JNUG.csv')
        data1 = data[ data['Date'] == 20131023]
        data2 = data[ data['Date'] == 20131024]

        data = pd.concat([data1,data2])
        met = metric.main(12,26,9,data,plot=True)
        scanplot=False
                
    if newdata:
        t1 = time.time()
        if stock == 'jnug':
            data = pd.read_csv(direc+'Causa_JNUG.csv')
        if stock == 'jdst':
            data = pd.read_csv(direc+'Causa_JDST.csv')
    
        #in-sample 18Nov2013-18Nov2015
        #out-sample 18Nov2015-
    
        in_data = data[ data['Date'] < 20151118 ]
    
        if check: #set start to match existing analysis
            in_data = data[ data['Date'] > 20131021 ]
    
        out_data = data[ data['Date'] >= 20151118 ]
    
        scan = []
        for b in np.arange(78)+1: #array from 1-78
            a = 1
            c = 1
            while a < b:
                while c <= a:
                    scan.append([a,b,c])
                    c += 1
                a += 1
                c = 1
        index = np.arange(len(scan))
        in_inv_scan = []
        out_inv_scan = []
        l=1
        for p in scan:
            print(l,'/',len(scan))
            l += 1
            in_inv = metric.main(p[0],p[1],p[2],in_data)
            in_inv_scan.append(in_inv)
            
        imax = index[ in_inv_scan == np.amax(in_inv_scan)]
        imax = imax[0]
    
        pmax = scan[imax]
        out_inv = metric.main(pmax[0],pmax[1],pmax[2],out_data)
        standard_in = metric.main(12,26,9,in_data)
        standard_out = metric.main(12,26,9,out_data)
        print('computation done in ',time.time()-t1,' seconds')
        print('max return of ',in_inv_scan[imax],'occurs at a,b,c = ',scan[imax])
        print('ROI on out-sample is ',out_inv)
        print(' ')
        print('compared with an ROI for standard [12,26,9] of:')
        print(' in-sample: ',standard_in)
        print(' out-sample: ',standard_out)

        np.savez(fsav,scan=scan,in_inv_scan=in_inv_scan,out_inv=out_inv,imax=imax,
                 standard_in=standard_in,standard_out=standard_out)
    #end of newdata
    else:
        f = np.load(fsav+'.npz')
        scan = f['scan']
        print(len(scan))
        out_inv = f['out_inv']
        in_inv_scan = f['in_inv_scan']
        index = np.arange(len(scan))
        if test:
            imax = index[ in_inv_scan == np.amax(in_inv_scan) ]
            imax = imax[0]
        else:
            imax = f['imax']
            standard_in = f['standard_in']
            standard_out = f['standard_out']
            print('compared with an ROI for standard [12,26,9] of:')
            print(' in-sample: ',standard_in)
            print(' out-sample: ',standard_out)
        print('max return of ',in_inv_scan[imax],'occurs at a,b,c = ',scan[imax])
        print('ROI on out-sample is ',out_inv)

    if write:
        if stock == 'jnug':
            data = pd.read_csv(direc+'Causa_JNUG.csv')
        if stock == 'jdst':
            data = pd.read_csv(direc+'Causa_JDST.csv')
        in_data = data[ data['Date'] < 20151118 ]    
        out_data = data[ data['Date'] >= 20151118 ]
        p = scan[imax]
        go = metric.main(p[0],p[1],p[2],data,write=True)

#---PLOT DATA---------------------
    if newplotdata:

        c = in_inv_scan/np.amax(in_inv_scan)


        print('normalizing')
        norm = [(d-np.min(in_inv_scan))/np.max(in_inv_scan) for d in in_inv_scan]

        npts = 79
        if test: npts = 11
        rr = np.arange(1,npts,1,dtype=np.int) #range from 1-78
        print('making mesh grid')
        v1,v2 = np.meshgrid(rr,rr)

        Z = v1*0.
        print('flattening to 2D')
        for r in rr-1:
            for c in rr-1:
                relevant = []
                for ii in np.arange(len(scan)):
                    s = scan[ii]
                    if v1[r,c] == s[0] and v2[r,c] == s[1]:
                        relevant.append(in_inv_scan[ii])
                if len(relevant) != 0:
                    Z[r,c] = np.max(relevant)

        Y = v1*0.
        for r in rr-1:
            for c in rr-1:
                relevant = []
                for ii in np.arange(len(scan)):
                    s = scan[ii]
                    if v1[r,c] == s[0] and v2[r,c] == s[2]:
                        relevant.append(in_inv_scan[ii])
                if len(relevant) != 0:
                    Y[r,c] = np.max(relevant)
                    
        X = v1*0.
        for r in rr-1:
            for c in rr-1:
                relevant = []
                for ii in np.arange(len(scan)):
                    s = scan[ii]
                    if v1[r,c] == s[1] and v2[r,c] == s[2]:
                        relevant.append(in_inv_scan[ii])
                if len(relevant) != 0:
                    X[r,c] = np.max(relevant)
        np.savez(direc+stock+'_plotdata',X=X,Y=Y,Z=Z,norm=norm,v1=v1,v2=v2)

#-----PLOTTING------------------
    if 0:
        import pylab as pl
        pl.plot(index,in_inv_scan,'b')
        pl.ylabel('ROI')
        pl.show()

    if scanplot:
        f = np.load(direc+stock+'_plotdata.npz')
        X = f['X']
        Y = f['Y']
        Z = f['Z']
        norm = f['norm']
        v1 = f['v1']
        v2 = f['v2']
        
        xs = []
        ys = []
        zs = []
        for r in scan:
            xs.append(r[0])
            ys.append(r[1])
            zs.append(r[2])

        import matplotlib
        matplotlib.rcParams.update({'font.size': 15})
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        print('making scatter plot')
        ax.scatter(xs,ys,zs,cmap=cm.bwr,c=norm,s=1)
        ax.set_xlabel('a-value')
        ax.set_ylabel('b-value')
        ax.set_zlabel('c-value')
        print('making contour plot')
        cset = ax.contourf(v1,v2,Z,zdir='z',offset=-10,cmap=cm.bwr)

        fig = plt.figure()
        plt.subplot(121)
        plt.pcolor(v1,v2,Y,cmap=cm.bwr)
        plt.xlabel('a-value')
        plt.ylabel('c-value')
        plt.subplot(122)
        plt.pcolor(v1,v2,X,cmap=cm.bwr)
        plt.xlabel('b-value')
        plt.ylabel('c-value')

        print('done')
        plt.show()








