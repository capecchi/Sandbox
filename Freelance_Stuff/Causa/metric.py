def main(a,b,c,data,
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
    dhigh = np.array(data['High'])
    dlow = np.array(data['Low'])
    
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
    dtime = dtime[len(dtime)-nn:]
    dhigh = dhigh[len(dhigh)-nn:]
    dlow = dlow[len(dlow)-nn:]

    
    #print(dtime[0],dtime[1],dtime[2])
    #print(dvol[0],dvol[1],dvol[2],dvol[1]/dvol[2])
    
    if plot: #plot ema12,ema26,macd,signal,histogram
        #import datetime
        import matplotlib.lines as mlines
        hr = [int(t/100)+ (t-int(t/100)*100)/60. for t in dtime]
        ind = np.arange(len(hist))
        sp = (dlow+dhigh)/2.
        sperr = dhigh-sp

        w = 4/5*(hr[1]-hr[0])
        #ind = hr
        plt.subplot(211)
        plt.plot(ind,ema12,'m',label='EMA(a)')
        plt.plot(ind,ema26,'k',label='EMA(b)')
        plt.errorbar(ind,sp,yerr=sperr,label='Stock Price')
        plt.legend()
        
        plt.subplot(212)
        plt.plot(ind,macd,'b',label='MACD')
        plt.plot(ind,signal,'r',label='EMA(c)')
        plt.bar(ind,hist,align='center',label='Histogram')
        plt.legend()
        plt.xlabel('22 Oct 2013')
        plt.show()
        
    #EVALUATE METRIC
    money_in = 0 #start with no money invested, wait for buy signal
    investment = 1.
    numsell = 0
    numbuy = 0
    buy = np.zeros(len(hist),dtype=np.int)
    sell = np.zeros(len(hist),dtype=np.int)
    for i in np.arange(len(hist)):
        if i >=1 and i < len(hist)-2: #must wait for at least second data pt

            #buy
            if hist[i-1]<0 and hist[i]>0 and money_in == 0:
                #print('i = ',i)
                #print(hist[i-1],hist[i])
                #stop
                buy[i] = 1
                purchase_price = dclose[i]
                money_in = 1
                numbuy += 1

            #sell
            elif money_in == 1 and (dvol[i]/dvol[i-1] < .7):
                sell[i] = 1
                sell_price = dopen[i+1]
                investment = investment*sell_price/purchase_price
                money_in = 0
                numsell += 1

            #sell at 1600
            elif money_in == 1 and dtime[i] == 1600:
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
        print('buy/sell starts at row with date: ',ddate[1],dtime[1])
        #print(len(hist),len(buy),len(sell),len(ddate),len(dtime))
        d = {'time':dtime,'volume':dvol,'histogram':hist,'buy':buy, 'sell':sell}
        df = pd.DataFrame(data=d)
        df.to_csv(direc+'buy_sell.csv',index=False)

    return investment
