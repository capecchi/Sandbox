
def main():
    import numpy as np
    from scipy.stats import binom
    from scipy.stats import binom_test
    import matplotlib.pyplot as plt

    n = 5312
    p = .228
    k = int(n*.241)
    print('k=',k)
    x = np.arange(binom.ppf(.001,n,p)
                  ,binom.ppf(.999,n,p))
    prob = binom.cdf(x,n,p) #compute cumulative probability distribution
    dist = binom.pmf(x,n,p)
    dist = dist/np.max(dist) #normalize

    print('at 22.8% we expect ',p*n)
    ii = np.where(x == k-1) #find index of highest cdf below k
    pval = 1-prob[ii] #find pval
    print('pval = ',pval)

    fig, ax = plt.subplots(1,1)
    ax.plot(x,dist,'b')
    ax.plot(x,prob,'r')
    plt.show()
