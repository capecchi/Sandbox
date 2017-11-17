import pandas as pd
import numpy as np


def main():
    path = 'C:\\Users\\Owner\\Desktop\\Projects\\Upwork\\Leftside_Design\\'
    df = pd.read_excel(path+'Solstice RTC_Temp.xlsx', header=0)
    #df = pd.read_excel(path+'Solstice RTC Nov 11-FINAL.xlsx', header=0)

    # referer columns: missing 'RNICKNAME'
    ref_columns = ['RELATIONSHIP','RFNAME','RLNAME','RMNAME','RADDR1','RADDR2','RCITY1','RSTATE1',
                   'RZIP1','RCOUNTRY1','RTITLE','REMPLOYER','RADDR21','RADDR22','RCITY2','RSTATE2','RZIP2','RCOUNTRY2',
                   'RHPHONE','RMPHONE','RWPHONE1','RWPHONE2','RFAX1','RFAX2','REMAIL1','REMAIL2','RURL']
    cols = df.columns
    nonref_columns = [c for c in cols if c not in ref_columns]

    testing = False
    if testing:
        nonref_columns = nonref_columns[:2] #for testing only use first couple columns
        ref_columns = ref_columns[:3]

    data = {}
    for r in np.arange(len(df)): #go through each record
        if not pd.isnull(df['FNAME'].iloc[r]): #skip empty rows
            child = df['FNAME'].iloc[r]+df['LNAME'].iloc[r]
            if child not in data.keys(): #add new record
                #print('adding entry for: ',child)
                child_data = {}
                for c in df.columns:
                    child_data[c] = [df[c].iloc[r]]
                data[child] = child_data
            else: #child record exists, add new referer info
                for c in ref_columns:
                    data[child][c].append(df[c].iloc[r]) #append new relationship data

    '''now have dict of all child data, convert to csv, one row per child'''
    df2 = pd.DataFrame(index=data.keys())
    for c in nonref_columns: #add columns of non-referer data
        df2[c] = [data[child][c][0] for child in data.keys()]

    '''go through referers, adding sets of columns'''
    max_records = max([len(data[child][ref_columns[0]]) for child in data.keys()])

    for i, child in enumerate(data.keys()):
        print('compiling data for: ',child, '('+str(i+1)+'/'+str(len(data.keys()))+')')
        refs = list(data[child][ref_columns[0]])
        num_refs = len(refs)
        index_arr = list(np.arange(num_refs))
        ordered_index = []
        add_referers = True
        while add_referers:
            if 'Mother' in refs:
                indx = refs.index('Mother')
                ordered_index.append(index_arr[indx])
                refs.remove('Mother')
                index_arr.remove(index_arr[indx])
            if 'Father' in refs:
                indx = refs.index('Father')
                ordered_index.append(index_arr[indx])
                refs.remove('Father')
                index_arr.remove(index_arr[indx])
            if len(refs) > 0:
                ordered_index.append(index_arr[0])
                refs.remove(refs[0])
                index_arr.remove(index_arr[0])
            else:
                add_referers = False
            if len(ordered_index) >= 3:
                add_referers = False

        ordered_index = ordered_index[:3]  # limit to 3 referers

        #for n in np.arange(num_refs):
        for i, n in enumerate(ordered_index):
            for ref_col in ref_columns:
                col_name = ref_col + ' (#'+str(i+1)+')'
                if col_name not in df2.columns:
                    df2[col_name] = ''
                df2[col_name].loc[child] = data[child][ref_col][n]

    df2.to_csv(path+'temp_output.csv', index=False)


if __name__ == '__main__':
    main()