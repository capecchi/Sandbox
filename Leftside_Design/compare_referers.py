import pandas as pd
import numpy as np


def main():
    path = 'C:\\Users\\Owner\\Desktop\\Projects\\Upwork\\Leftside_Design\\'
    #solstice = pd.read_excel(path+'Solstice RTC.xlsx', header=7)
    solstice = pd.read_csv(path+'Solstice RTC.csv', header=7)
    master = pd.read_excel(path + 'FINAL MASTER REFERRAL DATABASE.xlsx')
    records = np.arange(len(solstice['CID']))
    fname = solstice['RFNAME']
    lname = solstice['RLNAME']
    RTCnames = []

    for r in records:
        referer = solstice['REFERER'].iloc[r] #1/0 referer relationship column
        if referer: #ensure relationship=referer
            if pd.isnull(fname.iloc[r]):
                referer_name = ''
            else:
                referer_name = fname.iloc[r]
            if pd.isnull(lname.iloc[r]):
                referer_name += ''
            elif len(referer_name) > 0:
                referer_name += ' ' + lname.iloc[r]
            else:
                referer_name += lname.iloc[r]
            referer_name = " ".join(referer_name.split())  # remove double spaces
            if 'Rianoshek' in referer_name:
                a=1
            if len(referer_name) > 0:
                RTCnames.append(referer_name)

    RTCnames = np.unique(RTCnames)  # drop repeated names from list

    #test = pd.DataFrame(data={'RTCNames': RTCnames})
    #test.to_csv(path+'test.csv')

    database_fullnames = master['FullName'].dropna()
    master_names = []
    for r in np.arange(len(database_fullnames)):
        fullname = database_fullnames.iloc[r]
        fullname = " ".join(fullname.split())  # remove double spaces
        if len(fullname) > 0:
            master_names.append(fullname)
    master_names = np.unique(master_names)  # drop repeated names from list

    #COMPARE
    in_database = []
    not_in_database = []
    for name in RTCnames:
        if name in master_names:
            in_database.append(name)
        else:
            not_in_database.append(name)

    id = []
    for name in in_database:
        #name = name.decode('utf-8')
        id.append(name)
    nid = []
    for name in not_in_database:
        #name = name.decode('utf-8')
        nid.append(name)
    while len(id) < len(nid):
        id.append('')
    while len(nid) < len(id):
        nid.append('')

    results = pd.DataFrame(columns=['Not In Master', 'In Master'])
    results['Not In Master'] = nid
    results['In Master'] = id
    results.to_csv(path+'results.csv', index=False)
    a=1

if __name__ == '__main__':
    main()