
def main():
    import numpy as np
    from scipy.stats import binom
    from scipy.stats import binom_test
    import matplotlib.pyplot as plt

    k = 1953
    n = 5982
    p = .338
    x = np.arange(binom.ppf(.001,n,p)
                  ,binom.ppf(.999,n,p))
    prob = binom.cdf(x,n,p)
    dist = binom.pmf(x,n,p)
    dist = dist/np.max(dist)
    pval = binom_test(k,n,p)
    print(pval)

    print('at 33.8% we expect ',p*n)
    ii = np.where(x == k)
    print(prob[ii])

    i2 = np.where(prob > .05)
    i2 = np.min(i2)
    print(prob[i2-1:i2+1],x[i2-1:i2+1])
    fig, ax = plt.subplots(1,1)
    ax.plot(x,dist,'b')
    ax.plot(x,prob,'r')
    plt.show()
    
    n = 598
    k = 192
    p = .338
                        
