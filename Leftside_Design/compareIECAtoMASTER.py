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

def main():
    path = 'C:\\Users\\Owner\\Documents\\GitHub\\Sandbox\\Leftside_Design\\'
    ieca = pd.read_excel(path + 'IECA Full Database.xlsx')
    master = pd.read_excel(path + 'FINAL MASTER REFERRAL DATABASE_edited Nov 9.xlsx')
    master['Name'].fillna(value=' ')

    '''
    Note for me: gonna need to add a lot of cases so I can avoid things like "Dr" or "LCSW" or "Drs. Ashley and Paul"
    '''

    ieca_fname = ieca['Name'].values  # Has middle initials
    ieca_fname = [name.split(' ')[0] for name in ieca_fname]
    ieca_fname = [name.split(',')[0] for name in ieca_fname]
    ieca_lname = ieca['Last Name'].values
    ieca_lname = [name.split(' ')[0] for name in ieca_lname]
    ieca_lname = [name.split(',')[0] for name in ieca_lname]
    for i in ieca.index:  # check to make sure first and last name are in full name
        err_message = str(ieca_fname[i])+', '+str(ieca_lname[i])+', does not match record '+\
                      str(ieca['Full Name'].iloc[i])+' at index '+str(ieca.index[i])
        assert ieca_fname[i].lower() in ieca['Full Name'].iloc[i].lower(), err_message
        assert ieca_lname[i].lower() in ieca['Full Name'].iloc[i].lower(), err_message

    master_fname = master['Name'].values  # No middle initial
    master_fname = [name.split(' ')[0] for name in master_fname]
    master_fname = [name.split(',')[0] for name in master_fname]
    master_lname = master['LastName'].values
    master_lname = [name.split(' ')[0] for name in master_lname]
    master_lname = [name.split(',')[0] for name in master_lname]
    for i in master.index:  # check to make sure first and last name are in full name
        if i == 120:
            a=1
        err_message = str(master_fname[i])+', '+str(master_lname[i])+', does not match record '+\
                      str(master['FullName'].iloc[i])+' at index '+str(master.index[i])
        assert master_fname[i].lower() in master['FullName'].iloc[i].lower(), err_message
        assert master_lname[i].lower() in master['FullName'].iloc[i].lower(), err_message

    a=1


if __name__ == '__main__':
    main()