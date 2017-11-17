def main(check=False,
         plot=False):
    import pandas as pd
    import numpy as np
    import matplotlib
    import pylab as pl
    import matplotlib.pyplot as plt

    direc = 'C:/Users/Owner/Desktop/Projects/Upwork/Causa/'
    jnug = pd.read_csv(direc+'Causa_JNUG.csv')
    jdst = pd.read_csv(direc+'Causa_JDST.csv')

    #in-sample 18Nov2013-18Nov2015
    #out-sample 18Nov2015-

    in_data = jnug[ jnug['Date'] < 20151118 ]

    if check: #set start to match existing analysis
        in_data = jnug[ jnug['Date'] > 20131021 ]

    if plot: #select small timeframe to view data
        in_data = jnug[ jnug['Date'] < 20131118 ]
        
    out_data = jnug[ jnug['Date'] >= 20151118 ]
    
    #IN-SAMPLE
    #COMPUTE EMAs, MACD, SIGNAL, and HISTOGRAMs
    in_close = np.array(in_data['Close'])
    in_open = np.array(in_data['Open'])
    in_date = np.array(in_data['Date'])
    in_vol = np.array(in_data['Volume'])
    
    a = 12
    b = 26
    c = 9
    ema12 = [np.mean(in_close[0:a])]
    ema26 = [np.mean(in_close[0:b])]
    macd = []
    for i in np.arange(len(in_close)):
        if i >= a:
            val1 = in_close[i]*(2.0/(a+1.))+ema12[-1]*(1.-(2./(a+1.)))
            ema12.append(val1)

        if i >= b:
            val2 = in_close[i]*(2./(b+1.))+ema26[-1]*(1.-(2./(b+1.)))
            ema26.append(val2)

        if i >= b-1:
            val3 = ema12[-1] - ema26[-1]
            macd.append(val3)

        if i == b+c-2:
            #print(macd)
            signal = [np.mean(macd)]
            hist = [val3-signal[0]]
            hist_date = [in_date[i]]
            
        if i >= b+c-1:
            t1 = macd[-1]*(2./(c+1.))
            t2 = signal[-1]*(1.-(2./(c+1.)))
            signal.append(t1+t2)
            hist.append(val3-signal[-1])
            hist_date.append(in_date[i])
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
    in_close = in_close[len(in_close)-nn:]
    in_open = in_open[len(in_open)-nn:]
    in_date = in_date[len(in_date)-nn:]
    in_vol = in_vol[len(in_vol)-nn:]
    macd = macd[len(macd)-nn:]
    
    if plot:
        ind = np.arange(len(hist))
        print(in_date[0],in_date[-1])
        plt.figure(1)
        plt.subplot(211)
        plt.plot(ind,ema12,'r',ind,ema26,'b')

        plt.subplot(212)
        plt.plot(ind,macd,'g',ind,signal,'b')
        plt.bar(ind,hist)
        plt.show()

        #plt.bar(ind,hist)
        #plt.show()
#        pl.plot(ind,ema12,'r')
#        pl.plot(ind,ema26,'b')
#        pl.show()
#        pl.plot(ind,macd,'g')
#        pl.plot(ind,signal)
 #       plt.show()
        
    #EVALUATE METRIC
    money_in = 0 #start with no money invested, wait for buy signal
    investment = 1.
    numsell = 0
    numbuy = 0
    for i in np.arange(len(hist)):
        if i >=0 and i < len(hist)-2: #must wait for at least second data pt

            #buy
            if hist[i-1]<0 and hist[i]>0 and money_in == 0:
                purchase_price = in_close[i]
                money_in = 1
                numbuy += 1

            #sell
            if money_in == 1 and in_vol[i]/in_vol[i-1] < .7:
                sell_price = in_open[i+1]
                investment = investment*sell_price/purchase_price
                money_in = 0
                numsell += 1
                
    print('investment return = ',investment)
    print('#sells = ',numsell)
    print('#buys = ',numbuy)
    print('between ',in_date[0],',',in_date[-1])




    
    stop
