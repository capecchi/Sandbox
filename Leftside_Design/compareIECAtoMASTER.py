import pandas as pd
import numpy as np
import glob

'''
1) Take the IECA database and match it against REFERRAL database. Any name from IECA database that is in REFERRAL 
database please place "Ed Con" in the General Tab Title column. 

2) Then from your Total Final Output file, please add in any name missing from the REFERRAL database into the 
REFERRAL database. Unfortunately file info isn't in same order. Please bring over all relevant referral info from 
Total Final Output file (e.g. address, etc). Place General Tab Lead Source (lead source) into the General Tab Title 
column on REFERRAL database.
'''

def main(verbose=False):
    path = 'C:\\Users\\Owner\\Documents\\GitHub\\Sandbox\\Leftside_Design\\'
    ieca = pd.read_excel(path + 'IECA Full Database.xlsx')
    master = pd.read_excel(path + 'FINAL MASTER REFERRAL DATABASE_edited Nov 9.xlsx')
    master['Name'].fillna(value='', inplace=True)
    master['LastName'].fillna(value='', inplace=True)

    things_to_remove = ['Dr.', 'Drs.', 'LCSW']

    ieca_fname = ieca['Name'].values  # Has middle initials
    ieca_lname = ieca['Last Name'].values
    master_fname = master['Name'].values  # No middle initial
    master_lname = master['LastName'].values

    for thing in things_to_remove:
        ieca_fname = [name.replace(thing, '').strip() for name in ieca_fname]
        ieca_lname = [name.replace(thing, '').strip() for name in ieca_lname]
        master_fname = [name.replace(thing, '').strip() for name in master_fname]
        master_lname = [name.replace(thing, '').strip() for name in master_lname]

    ieca_fname = [name.split(' ')[0] for name in ieca_fname]
    ieca_fname = [name.split(',')[0] for name in ieca_fname]
    ieca_lname = [name.split(' ')[0] for name in ieca_lname]
    ieca_lname = [name.split(',')[0] for name in ieca_lname]

    master_fname = [name.split(' ')[0] for name in master_fname]
    master_fname = [name.split(',')[0] for name in master_fname]
    master_lname = [name.split(' ')[0] for name in master_lname]
    master_lname = [name.split(',')[0] for name in master_lname]

    for i in ieca.index:  # check to make sure first and last name are in full name
        err_message = str(ieca_fname[i])+', '+str(ieca_lname[i])+', does not match record '+\
                      str(ieca['Full Name'].iloc[i])+' at index '+str(ieca.index[i])
        assert ieca_fname[i].lower() in ieca['Full Name'].iloc[i].lower(), err_message
        assert ieca_lname[i].lower() in ieca['Full Name'].iloc[i].lower(), err_message

    for i in master.index:  # check to make sure first and last name are in full name
        err_message = str(master_fname[i])+', '+str(master_lname[i])+', does not match record '+\
                      str(master['FullName'].iloc[i])+' at index '+str(master.index[i])
        assert master_fname[i].lower() in master['FullName'].iloc[i].lower(), err_message
        assert master_lname[i].lower() in master['FullName'].iloc[i].lower(), err_message

    ieca_names = [ieca_fname[i] + ieca_lname[i] for i in np.arange(len(ieca_fname))]
    master_names = [master_fname[i] + master_lname[i] for i in np.arange(len(master_fname))]

    num_names = 0
    for iname in ieca_names:
        if iname in master_names:
            num_names += 1
            ind = master_names.index(iname)
            master['General Tab Title'].iloc[ind] = 'Ed Con'
            if verbose:
                print(iname)

    print(str(num_names)+' names labeled "Ed Con" in Master Database')
    master.to_csv(path+'IECA_MASTER_output.csv')


if __name__ == '__main__':
    main(verbose=False)