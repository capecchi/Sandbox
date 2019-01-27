#patch to add standard [12,26,9] evaluations

def main():
    import metric
    import numpy as np
    import pandas as pd

    direc = 'C:/Users/Owner/Desktop/Projects/Upwork/Causa/'

    stocks = ['jnug','jdst']
    stocks = ['jdst']
    for stock in stocks:
        if stock == 'jnug':
            data = pd.read_csv(direc+'Causa_JNUG.csv')
        if stock == 'jdst':
            data = pd.read_csv(direc+'Causa_JDST.csv')

        in_data = data[ data['Date'] < 20151118 ]    
        out_data = data[ data['Date'] >= 20151118 ]

        fsav = direc+stock+'_analysis'

        f = np.load(fsav+'.npz')
        scan = f['scan']
        out_inv = f['out_inv']
        in_inv_scan = f['in_inv_scan']
        imax = f['imax']
        index = np.arange(len(scan))
        standard_in = metric.main(12, 26, 9, in_data)
        standard_out = metric.main(12, 26, 9, out_data)

        print('FOR ',stock,' STOCK::')
        print('max return of ',in_inv_scan[imax],'occurs at a,b,c = ',scan[imax])
        print('ROI on out-sample is ',out_inv)
        print('compared with an ROI for standard [12,26,9] of:')
        print(' in-sample: ',standard_in)
        print(' out-sample: ',standard_out)

        np.savez(fsav,scan=scan,in_inv_scan=in_inv_scan,out_inv=out_inv,imax=imax,
                 standard_in=standard_in,standard_out=standard_out)
