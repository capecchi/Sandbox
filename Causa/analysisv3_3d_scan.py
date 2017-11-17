def metric_old(a,b,c,data,
           check=False,
           plot=False,
           verbose=False,
           write=False):

    import numpy as np
    import matplotlib
    import pylab as pl
    import matplotlib.pyplot as plt

    #IN-SAMPLE
    #COMPUTE EMAs, MACD, SIGNAL, and HISTOGRAMs
    dclose = np.array(data['Close'])
    dopen = np.array(data['Open'])
    ddate = np.array(data['Date'])
    dvol = np.array(data['Volume'])
    dtime = np.array(data['Time'])
    
    ema12 = [np.mean(dclose[0:a])]
    ema26 = [np.mean(dclose[0:b])]
    macd = []
    for i in np.arange(len(dclose)):
        if i >= a:
            val1 = dclose[i]*(2.0/(a+1.))+ema12[-1]*(1.-(2./(a+1.)))
            ema12.append(val1)

        if i >= b:
            val2 = dclose[i]*(2./(b+1.))+ema26[-1]*(1.-(2./(b+1.)))
            ema26.append(val2)

        if i >= b-1:
            val3 = ema12[-1] - ema26[-1]
            macd.append(val3)

        if i == b+c-2:
            #print(macd)
            signal = [np.mean(macd)]
            hist = [val3-signal[0]]
            hist_date = [ddate[i]]
            
        if i >= b+c-1:
            t1 = macd[-1]*(2./(c+1.))
            t2 = signal[-1]*(1.-(2./(c+1.)))
            signal.append(t1+t2)
            hist.append(val3-signal[-1])
            hist_date.append(ddate[i])
        #if i > b+5: stop
        
    #check against existing analysis
    if check:
        print(ema12[:5]) #ok
        print(ema26[:5]) #ok
        print(macd[:5]) #ok
        print(signal[:5]) #ok
        print(hist[:5]) #ok

    nn = len(hist)
    ema12 = ema12[len(ema12)-nn:]
    ema26 = ema26[len(ema26)-nn:]
    dclose = dclose[len(dclose)-nn:]
    dopen = dopen[len(dopen)-nn:]
    ddate = ddate[len(ddate)-nn:]
    dvol = dvol[len(dvol)-nn:]
    macd = macd[len(macd)-nn:]
    
    if plot: #plot ema12,ema26,macd,signal,histogram
        ind = np.arange(len(hist))
        print(ddate[0],ddate[-1])
        plt.figure(1)
        plt.subplot(211)
        plt.plot(ind,ema12,'r',ind,ema26,'b')

        plt.subplot(212)
        plt.plot(ind,macd,'g',ind,signal,'b')
        plt.bar(ind,hist)
        plt.show()
        
    #EVALUATE METRIC
    money_in = 0 #start with no money invested, wait for buy signal
    investment = 1.
    numsell = 0
    numbuy = 0
    buy = np.zeros(len(hist),dtype=np.int)
    sell = np.zeros(len(hist),dtype=np.int)
    for i in np.arange(len(hist)):
        if i >=0 and i < len(hist)-2: #must wait for at least second data pt

            #buy
            if hist[i-1]<0 and hist[i]>0 and money_in == 0:
                buy[i] = 1
                purchase_price = dclose[i]
                money_in = 1
                numbuy += 1

            #sell
            if money_in == 1 and dvol[i]/dvol[i-1] < .7:
                sell[i] = 1
                sell_price = dopen[i+1]
                investment = investment*sell_price/purchase_price
                money_in = 0
                numsell += 1

            #sell at 1600
            if money_in == 1 and dtime[i] == 1600:
                sell[i] = 1
                sell_price = dclose[i]
                investment = investment*sell_price/purchase_price
                money_in = 0
                numsell += 1

    if verbose:               
        print('investment return = ',investment)
        print('#sells = ',numsell)
        print('#buys = ',numbuy)
        print('between ',ddate[0],',',ddate[-1])

    if write:
        import pandas as pd
        direc = 'C:/Users/Owner/Desktop/Projects/Upwork/Causa/'
        print('buy/sell starts at row with date: ',ddate[0],dtime[0])
        print(len(hist),len(buy),len(sell),len(ddate),len(dtime))
        d = {'buy':buy, 'sell':sell}
        df = pd.DataFrame(data=d)
        df.to_csv(direc+'buy_sell',index=False)

    return investment

############################################################

def main(stock,
         check=False,
         newdata=True,
         test=False,
         write=False):

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
        newdata = False
        fsav = direc + 'test_big'
        
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
            in_inv = metric(p[0],p[1],p[2],in_data)
            in_inv_scan.append(in_inv)
            
        imax = index[ in_inv_scan == np.amax(in_inv_scan)]
        imax = imax[0]
    
        pmax = scan[imax]
        out_inv = metric(pmax[0],pmax[1],pmax[2],out_data)
        standard_in = metric(12,26,9,in_data)
        standard_out = metric(12,26,9,out_data)
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
        out_inv = f['out_inv']
        in_inv_scan = f['in_inv_scan']
        imax = f['imax']
        index = np.arange(len(scan))
        standard_in = f['standard_in']
        standard_out = f['standard_out']
        #imax = index[ in_inv_scan == np.amax(in_inv_scan) ]
        #imax = imax[0]
        print('max return of ',in_inv_scan[imax],'occurs at a,b,c = ',scan[imax])
        print('ROI on out-sample is ',out_inv)
        print('compared with an ROI for standard [12,26,9] of:')
        print(' in-sample: ',standard_in)
        print(' out-sample: ',standard_out)

    if write:
        if stock == 'jnug':
            data = pd.read_csv(direc+'Causa_JNUG.csv')
        if stock == 'jdst':
            data = pd.read_csv(direc+'Causa_JDST.csv')
        in_data = data[ data['Date'] < 20151118 ]    
        out_data = data[ data['Date'] >= 20151118 ]
        p = scan[imax]
        go = metric(p[0],p[1],p[2],data,write=True)

    xs = []
    ys = []
    zs = []
    for r in scan:
        xs.append(r[0])
        ys.append(r[1])
        zs.append(r[2])

    c = in_inv_scan/np.amax(in_inv_scan)

    if 0:
        import pylab as pl
        pl.plot(index,in_inv_scan,'b')
        pl.ylabel('ROI')
        pl.show()

    if 1:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        norm = [(d-np.min(in_inv_scan))/np.max(in_inv_scan) for d in in_inv_scan]
        ax.scatter(xs,ys,zs,cmap=cm.bwr,c=norm)
        ax.set_xlabel('a-value')
        ax.set_ylabel('b-value')
        ax.set_zlabel('c-value')

        rr = np.arange(1,79,1,dtype=np.int) #range from 1-78
        v1,v2 = np.meshgrid(rr,rr)

        Z = v1*0.
        for r in rr-1:
            for c in rr-1:
                relevant = []
                for ii in np.arange(len(scan)):
                    s = scan[ii]
                    if v1[r,c] == s[0] and v2[r,c] == s[1]:
                        relevant.append(in_inv_scan[ii])
                if len(relevant) != 0:
                    Z[r,c] = np.max(relevant)
        cset = ax.contourf(v1,v2,Z,zdir='z',offset=-1,cmap=cm.bwr)
#        cset = ax.contourf(v1,v2,Z,zdir='x',offset=-1,cmap=cm.bwr)
#        cset = ax.contourf(v1,v2,Z,zdir='y',offset=11,cmap=cm.bwr)

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

        fig = plt.figure()
        plt.subplot(121)
        plt.pcolor(v1,v2,Y,cmap=cm.bwr)
        plt.xlabel('a-value')
        plt.ylabel('c-value')
        plt.subplot(122)
        plt.pcolor(v1,v2,X,cmap=cm.bwr)
        plt.xlabel('b-value')
        plt.ylabel('c-value')
        
        plt.show()








