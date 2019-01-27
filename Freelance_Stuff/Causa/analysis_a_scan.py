def metric_old(a,b,c,data,
           check=False,
           plot=False,
           verbose=False):

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
    for i in np.arange(len(hist)):
        if i >=0 and i < len(hist)-2: #must wait for at least second data pt

            #buy
            if hist[i-1]<0 and hist[i]>0 and money_in == 0:
                purchase_price = dclose[i]
                money_in = 1
                numbuy += 1

            #sell
            if money_in == 1 and dvol[i]/dvol[i-1] < .7:
                sell_price = dopen[i+1]
                investment = investment*sell_price/purchase_price
                money_in = 0
                numsell += 1
    if verbose:               
        print('investment return = ',investment)
        print('#sells = ',numsell)
        print('#buys = ',numbuy)
        print('between ',ddate[0],',',ddate[-1])

    return investment

############################################################

def main(check=False):

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import matplotlib.patches as mpatches

    direc = 'C:/Users/Owner/Desktop/Projects/Upwork/Causa/'
    jnug = pd.read_csv(direc+'Causa_JNUG.csv')
    jdst = pd.read_csv(direc+'Causa_JDST.csv')

    #in-sample 18Nov2013-18Nov2015
    #out-sample 18Nov2015-

    in_data = jnug[ jnug['Date'] < 20151118 ]

    if check: #set start to match existing analysis
        in_data = jnug[ jnug['Date'] > 20131021 ]

    out_data = jnug[ jnug['Date'] >= 20151118 ]

    a_scan = np.arange(25)+1 #array from 1 to 25
    index = np.arange(len(a_scan))
    in_inv_scan = []
    out_inv_scan = []
    for a in a_scan:
        in_inv = metric_old(a,26,9,in_data)
        in_inv_scan.append(in_inv)
        out_inv = metric_old(a,26,9,out_data)
        out_inv_scan.append(out_inv)

    imax = index[ in_inv_scan == np.amax(in_inv_scan)]
    imax = imax[0]
    omax = index[ out_inv_scan == np.amax(out_inv_scan)]
    omax = omax[0]
    
    print('max return of ',in_inv_scan[imax],'occurs at a=',a_scan[imax])
    print('resulting in an out-sample ROI of ',out_inv_scan[imax])
    print('max return of ',out_inv_scan[omax],'occurs at a=',a_scan[omax])


    red_patch = mpatches.Patch(color='red', label='out-sample data')
    blue_patch = mpatches.Patch(color='blue', label='in-sample data')

    import matplotlib
    matplotlib.rcParams.update({'font.size': 15})
    plt.plot(a_scan,in_inv_scan,'k',a_scan,in_inv_scan,'bs')
    plt.plot(a_scan[imax],in_inv_scan[imax],'gs')
    plt.plot(a_scan,out_inv_scan,'k',a_scan,out_inv_scan,'rs')
    plt.plot(a_scan[omax],out_inv_scan[omax],'gs')
    plt.legend(handles=[blue_patch,red_patch])
    #plt.legend(handles=[red_patch])
    plt.xlabel('a-value')
    plt.ylabel('ROI')
    plt.show()







