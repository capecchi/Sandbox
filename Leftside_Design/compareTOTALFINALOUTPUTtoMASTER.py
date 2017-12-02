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
    tfo = pd.read_csv(path + 'TOTAL FINAL output.csv', encoding='utf-8')
    tfo_relevant_columns = [tfo.columns[i] for i in np.arange(len(tfo.columns)) if 'lead source' in tfo.columns[i]]
    tfo_relevant_columns.insert(0, 'Program')
    tfo = tfo[tfo_relevant_columns]

    '''We start by filling in missing values and combining some columns for transfer later'''
    fname_col = 'Contact First Name (could be primary Contact, Parent, Referral) (lead source)'
    lname_col = 'Contact Last Name (could be primary Contact, Parent, Referral) (lead source)'
    tfo[fname_col].fillna(value='', inplace=True)
    tfo[lname_col].fillna(value='', inplace=True)
    tfo['FullName'] = tfo[fname_col]+' '+tfo[lname_col]
    tfo['FullName'] = [fullname.strip() for fullname in tfo['FullName'].values]
    tfo['Contact Address (lead source)'].fillna(value='', inplace=True)
    tfo['Contact Address 1 (lead source)'].fillna(value='', inplace=True)
    tfo['Contact Address (combined)'] = tfo['Contact Address (lead source)'] + ' ' + tfo['Contact Address 1 (lead source)']
    tfo['Referral Address (lead source)'].fillna(value='', inplace=True)
    tfo['Referral Address 2 (lead source)'].fillna(value='', inplace=True)
    tfo['ALT Address'] = tfo['Referral Address (lead source)'] + ' ' + tfo['Referral Address 2 (lead source)']

#    master = pd.read_excel(path + 'FINAL MASTER REFERRAL DATABASE_edited Nov 9.xlsx')
    master = pd.read_csv(path + 'IECA_MASTER_output.csv')  # use output from IECA comparison
    master['Name'].fillna(value='', inplace=True)
    master['LastName'].fillna(value='', inplace=True)

    things_to_remove = ['Dr.', 'Drs.', 'LCSW']

    tfo_fname = tfo[fname_col].values
    tfo_lname = tfo[lname_col].values
    master_fname = master['Name'].values  # No middle initial
    master_lname = master['LastName'].values

    for thing in things_to_remove:
        tfo_fname = [name.replace(thing, '').strip() for name in tfo_fname]
        tfo_lname = [name.replace(thing, '').strip() for name in tfo_lname]
        master_fname = [name.replace(thing, '').strip() for name in master_fname]
        master_lname = [name.replace(thing, '').strip() for name in master_lname]

    tfo_fname = [name.split(' ')[0] for name in tfo_fname]
    tfo_fname = [name.split(',')[0] for name in tfo_fname]
    tfo_lname = [name.split(' ')[0] for name in tfo_lname]
    tfo_lname = [name.split(',')[0] for name in tfo_lname]

    master_fname = [name.split(' ')[0] for name in master_fname]
    master_fname = [name.split(',')[0] for name in master_fname]
    master_lname = [name.split(' ')[0] for name in master_lname]
    master_lname = [name.split(',')[0] for name in master_lname]

    for i in master.index:  # check to make sure first and last name are in full name
        err_message = str(master_fname[i])+', '+str(master_lname[i])+', does not match record '+\
                      str(master['FullName'].iloc[i])+' at index '+str(master.index[i])
        assert master_fname[i].lower() in master['FullName'].iloc[i].lower(), err_message
        assert master_lname[i].lower() in master['FullName'].iloc[i].lower(), err_message

    remove = ['Previous', 'Employee', 'Other', 'Current']
    tfo_names = tfo['FullName'].values
    tfo_names = [name for name in tfo_names if len(name) > 1]  # remove any blank entries
    for r in remove:  # remove entries like "Previous"
        tfo_names = [name for name in tfo_names if r not in name]
    tfo_names = list(np.unique([n.strip() for n in tfo_names]))  # remove whitespace and keep only unique names
    master_names = [master_fname[i] + ' ' + master_lname[i] for i in np.arange(len(master_fname))]

    num_names = 0
    newname_dict = {}
    for iname in tfo_names:
        if iname not in master_names:

            tfo_data_for_newname = tfo[tfo['FullName'] == iname]
            if len(tfo_data_for_newname) > 1:  # multiple rows exist for this person
                tfo_data_for_newname = smoosh_df(tfo_data_for_newname)  # compress rows keeping longest string value

            num_names += 1
            col_dict = get_tfo2master_dict()
            newname_dict[num_names] = {}
            for col in col_dict:
                value = tfo_data_for_newname[col_dict[col]].values[0]
                newname_dict[num_names].update({col: value})

    newname_df = pd.DataFrame.from_dict(data=newname_dict, orient='index')

    master_out = master.append(newname_df, ignore_index=True)
    master_out = master_out[master.columns]  # reorder columns to original layout
    master_out.to_csv(path+'tfo2master.csv', index=False)
    print(str(num_names)+' names added to Master Database')
    print('Check for: '+iname)
    a=1


def smoosh_df(df):

    nrows = len(df)
    for col in df.columns:
        for i, ind in enumerate(df.index):
            if i == 0:
                ind0 = ind
                a=1
            else:
                if len(str(df.loc[ind, col])) > len(str(df.loc[ind0, col])):
                    df.set_value(ind0, col, df.loc[ind, col])
                    #print('changed to: '+df.loc[ind, col])
    df = df.loc[[ind0]]
    return df

def get_tfo2master_dict():

    dict = {'PROGRAM NAME': 'Program',
    'FullName': 'FullName',
    'Name': 'Contact First Name (could be primary Contact, Parent, Referral) (lead source)',
    'LastName': 'Contact Last Name (could be primary Contact, Parent, Referral) (lead source)',
    'General Tab Title': 'General Tab Lead Source (lead source)',
    'Additional Info tab TITLE': 'Additional Info tab TITLE (if contact is primary or referral) (lead source)',
    'BusinessName': 'Additional Info tab COMPANY NAME (if contact is primary or referral) (lead source)',
    'Address': 'Contact Address (combined)',
    'City': 'Contact City (lead source)',
    'State': 'Contact State (lead source)',
    'Zip': 'Contact Zip (lead source)',
    'Country': 'Contact Country (lead source)',
    'BusinessPhone': 'Contact Phone 1 (lead source)',
    'Fax': 'Contact Fax (lead source)',
    'Email': 'Contact Email (lead source)',
    'Website': 'Contact Website (lead source)',
    'ALT Address': 'ALT Address',
    'ALT City': 'Referral City (lead source)',
    'ALT State': 'Referral State (lead source)',
    'ALT Zip': 'Referral Zip (lead source)',
    'ALT Country': 'Referral Country (lead source)',
    'ALT BusinessPhone': 'Contact Phone 2 (lead source)'}

    return dict


if __name__ == '__main__':
    main(verbose=True)











'''
MASTER Columns:
'PROGRAM NAME': 'Program'
--'FullName': 'Contact First Name (could be primary Contact, Parent, Referral) (lead source)' + 'Contact Last Name (could be primary Contact, Parent, Referral) (lead source)'
'Name': 'Contact First Name (could be primary Contact, Parent, Referral) (lead source)'
--'LastName': 'Contact Last Name (could be primary Contact, Parent, Referral) (lead source)'
'General Tab Title': 'General Tab Lead Source (lead source)'
'Additional Info tab TITLE': 'Additional Info tab TITLE (if contact is primary or referral) (lead source)'
'Business Title': 
'BusinessName': 'Additional Info tab COMPANY NAME (if contact is primary or referral) (lead source)'
--'Address': 'Contact Address (lead source)'+'Contact Address 1 (lead source)'
'City': 'Contact City (lead source)' 
'State': 'Contact State (lead source)' 
'Zip': 'Contact Zip (lead source)'
'Country': 'Contact Country (lead source)'
'BusinessPhone': 'Contact Phone 1 (lead source)'
'Cell Phone': 
'Fax': 'Contact Fax (lead source)'
'Email': 'Contact Email (lead source)'
'Website': 'Contact Website (lead source)'
'Lead Source': 
'Iteration1': 
'file_name': 
'AccountId': 
'ALT BusinessName': 
'ALT Address': 'Referral Address (lead source)'+'Referral Address 2 (lead source)'
'ALT City': 'Referral City (lead source)'
'ALT State': 'Referral State (lead source)'
'ALT Zip': 'Referral Zip (lead source)'
'ALT Country': 'Referral Country (lead source)'
'ALT BusinessPhone': 'Contact Phone 2 (lead source)'
'ALT Cell Phone': 
'ALT Fax': 
'ALT Email': 
'''
'''
TOTAL FINAL output (unused lead source columns)
Lead Info tab Referral Origin (lead source)
Lead Info tab Origin Name (lead source)
Lead Info tab Referring Therapist (lead source)
Additional Info tab MIDDLE if contact is Primary contact or Referral (lead source)
Additional Info tab NICKNAME if contact is Primary contact or Referral (lead source)
PGROUP (lead source)
LOCATION (lead source)
'''