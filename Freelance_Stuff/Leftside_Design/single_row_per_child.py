import pandas as pd
import numpy as np


def main():
    path = 'C:\\Users\\Owner\\Desktop\\Projects\\Upwork\\Leftside_Design\\'
    nonref_columns, ref_determiner, relationship_cols, lead_source_cols, phone_cols, fax_cols, email_cols = get_column_labels()

    testing = False
    if testing:
        fn = 'temp_output.csv'
        df = pd.read_excel(path + 'TOTAL FINAL_small.xlsx', header=0)
        #nonref_columns = nonref_columns[:5] #for testing only use first couple columns
        #relationship_cols = relationship_cols[:5]
        #lead_source_cols = lead_source_cols[:5]
        #df = df.iloc[:15] #use only first few rows
    else:
        fn = 'TOTAL FINAL output.csv'
        df = pd.read_excel(path + 'TOTAL FINAL.xlsx', header=0)

    #First go through and compress phone/fax/email data into 2/1/1 columns
    df['Contact Phone 1'] = ''
    df['Contact Phone 2'] = ''
    df['Contact Fax'] = ''
    df['Contact Email'] = ''
    for r in np.arange(len(df)): #go through each record
        if r >= 1243:
            a=1
        phone_numbers = np.unique(list(df[phone_cols].iloc[r].dropna()))
        phone_numbers = phone_numbers[:2]  # limit to 2 numbers
        for i, pn in enumerate(phone_numbers):
            df['Contact Phone '+str(i+1)].iloc[r] = pn
        fax_number = np.unique(list(df[fax_cols].iloc[r].dropna()))
        fax_number = fax_number[:1]  # limit to 1 fax number
        for fax in fax_number:
            df['Contact Fax'].iloc[r] = fax
        email = np.unique(list(df[email_cols].iloc[r].dropna()))
        email = email[:1]
        for em in email:
            df['Contact Email'].iloc[r] = em
        a=1

    data = {}
    for r in np.arange(len(df)): #go through each record
        if not pd.isnull(df['Child/Client Last Name'].iloc[r]): #skip empty rows
            if pd.isnull(df['Child/Client First Name'].iloc[r]):
                fname = ''
            else:
                fname = df['Child/Client First Name'].iloc[r]
            child = fname+df['Child/Client Last Name'].iloc[r]
            if child not in data.keys(): #add new record
                #print('adding entry for: ',child)
                child_data = {}
                for c in nonref_columns:
                    child_data[c] = [df[c].iloc[r]]
                relationship = {}
                lead_source = {}
                if pd.isnull(df[ref_determiner[0]].iloc[r]):  # is a lead source
                    for c in lead_source_cols:
                        lead_source[c] = [df[c].iloc[r]]
                    for c in relationship_cols:
                        relationship[c] = []
                else:  # is a relationship
                    for c in relationship_cols:
                        relationship[c] = [df[c].iloc[r]]
                    for c in lead_source_cols:
                        lead_source[c] = []
                child_data['relationship'] = relationship
                child_data['lead_source'] = lead_source
                data[child] = child_data

            else: #child record exists, add new referrer info
                if pd.isnull(df[ref_determiner[0]].iloc[r]):  # is a lead source
                    for c in lead_source_cols:
                        data[child]['lead_source'][c].append(df[c].iloc[r])  # append new relationship data
                else:  # is a relationship
                    for c in relationship_cols:
                        data[child]['relationship'][c].append(df[c].iloc[r])

    '''now have dict of all child data, convert to csv, one row per child'''
    df2 = pd.DataFrame(index=data.keys())
    for c in nonref_columns: #add columns of non-referer data
        df2[c] = [data[child][c][0] for child in data.keys()]

    '''go through relationships, adding sets of columns'''
    for i, child in enumerate(data.keys()):
        print('compiling data for: ', child, '('+str(i+1)+'/'+str(len(data.keys()))+')')
        num = 0
        for n in np.arange(min(3, len(data[child]['relationship'][relationship_cols[0]]))):  # add up to 3 relationship data
            num += 1
            for col in relationship_cols:
                col_name = col + ' (#'+str(num)+')'
                if col_name not in df2.columns:
                    df2[col_name] = ''
                df2[col_name].loc[child] = data[child]['relationship'][col][n]
        for n in np.arange(min(1, len(data[child]['lead_source'][lead_source_cols[0]]))):  # add no more than 1 lead source
            num += 1
            for col in lead_source_cols:
                col_name = col + ' (lead source)'
                if col_name not in df2.columns:
                    df2[col_name] = ''
                df2[col_name].loc[child] = data[child]['lead_source'][col][n]

    df2.to_csv(path+fn, index=False)


def get_column_labels():

    #Adding these columns to replace multiple phone/email/fax columns:
    # 'Contact Phone 1', 'Contact Phone 2', 'Contact Fax', 'Contact Email'

    child_columns = ['Program', 'General Owner', 'Child/Client First Name', 'Child/Client Last Name',
                     'Child/Cliend DOB', 'Child/Cliend Sex', 'Child/Cliend LivesWith', 'Child/Cliend School',
                     'Child/Cliend Grade', 'Lead Admitted Date', 'Lead Date of Discharge', 'Child Phone',
                     'Child Email',
                     'Child Address', 'Child Address 2', 'Child City', 'Child State', 'Child Zip',
                     'Lead Info Comments',
                     'Lead Info Assigned Program therapist', 'PARENT', 'REFERER', 'SECONDARYREFERER', 'REFEROUT',
                     'LEGALCONTACT', 'REFERRER']
    referrer_determiner = ['General tab Relationship', 'General Tab Lead Source']
    relationship_cols = ['General tab Relationship', 'Lead Info tab Referral Origin', 'Lead Info tab Origin Name',
                         'Lead Info tab Referring Therapist',
                       'Contact First Name (could be primary Contact, Parent, Referral)',
                       'Contact Last Name (could be primary Contact, Parent, Referral)',
                       'Additional Info tab MIDDLE if contact is Primary contact or Referral',
                       'Additional Info tab NICKNAME if contact is Primary contact or Referral',
                       'Contact Address', 'Contact Address 1', 'Contact City', 'Contact State',
                       'Contact Zip', 'Contact Country',
                       'Additional Info tab TITLE (if contact is primary or referral)',
                       'Additional Info tab COMPANY NAME (if contact is primary or referral)',
                       'Referral Address', 'Referral Address 2', 'Referral City', 'Referral State', 'Referral Zip',
                       'Referral Country', 'Contact Phone 1', 'Contact Phone 2',
                       'Contact Fax', 'Contact Email', 'Contact Website', 'PGROUP', 'LOCATION']
    lead_source_cols = ['General Tab Lead Source', 'Lead Info tab Referral Origin', 'Lead Info tab Origin Name',
                        'Lead Info tab Referring Therapist',
                       'Contact First Name (could be primary Contact, Parent, Referral)',
                       'Contact Last Name (could be primary Contact, Parent, Referral)',
                       'Additional Info tab MIDDLE if contact is Primary contact or Referral',
                       'Additional Info tab NICKNAME if contact is Primary contact or Referral',
                       'Contact Address', 'Contact Address 1', 'Contact City', 'Contact State',
                       'Contact Zip', 'Contact Country',
                       'Additional Info tab TITLE (if contact is primary or referral)',
                       'Additional Info tab COMPANY NAME (if contact is primary or referral)',
                       'Referral Address', 'Referral Address 2', 'Referral City', 'Referral State', 'Referral Zip',
                       'Referral Country', 'Contact Phone 1', 'Contact Phone 2', 'Contact Fax',
                       'Contact Email', 'Contact Website', 'PGROUP', 'LOCATION']

    phone_cols = ['Contact Phone (condence 4 Phone columns into 2)',
                  'Contact Phone (condence 4 Phone columns into 2).1',
                  'Contact Phone (condence 4 Phone columns into 2).2',
                  'Contact Phone (condence 4 Phone columns into 2).3']
    fax_cols = ['Contact Fax (condense 2 columns into 1)', 'Contact Fax (condense 2 columns into 1).1']
    email_cols = ['Contact Email (condense 2 columns into 1)', 'Contact Email (condense 2 columns into 1).1']

    return child_columns, referrer_determiner, relationship_cols, lead_source_cols, phone_cols, fax_cols, email_cols


if __name__ == '__main__':
    main()