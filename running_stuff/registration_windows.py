import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import datetime
import matplotlib.dates as mdates
import mysql.connector
import datetime

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

"""
procedure: navigate to https://runningintheusa.com/classic/list/map/100m/all-dates
right click view page source
copy paste into notepad++ and save in Sandbox/running_stuff/data with name like 01Oct25_download.txt
because the MAP is there, this will return data for all the 100 milers in the database
*maybe not all- am I missing past years of things? not sure
"""


def update_sql_database():
    dbname = 'race_data'
    tbname = 'hundred_milers'
    direc = './data/'
    pgsrc = f'{direc}01oct25_download.txt'

    # Open database and create table if needed
    try:
        print(f'connecting to database...')
        mydb = mysql.connector.connect(host='localhost', user='silence_of_stone', password='CCg2tE69;2JH',
                                       database=dbname)
    except:
        mydb = mysql.connector.connect(host='localhost', user='silence_of_stone', password='CCg2tE69;2JH')
        print(f'database {dbname} does not exist: creating it...')
        mycursor = mydb.cursor()
        mycursor.execute(f'create database {dbname}')
        print(f'... done. connecting to database...')
        mydb = mysql.connector.connect(host='localhost', user='silence_of_stone', password='CCg2tE69;2JH',
                                       database=dbname)

    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f'''
    create table if not exists {tbname} (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    race_name VARCHAR(50), 
    city VARCHAR(50), 
    state VARCHAR(2),
    date DATE, 
    CONSTRAINT unique_race UNIQUE (race_name, city, state, date))
    ''')

    # parse through pagesource for races
    sql = f'INSERT IGNORE INTO {tbname} (race_name, city, state, date) VALUES (%s, %s, %s, %s)'
    races = []
    with open(pgsrc) as file:
        lines = file.readlines()
        for il, ll in enumerate(lines):
            if '<div id="City_' in ll:
                city, state = lines[il + 1].strip('\t').strip('<strong>').strip('\n').strip('</strong>').split(', ')
                racename = lines[il + 4].strip('\t').strip('\n')
                date = lines[il + 9].strip('\t').strip('\n')[:12]
                sqldate = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')  # convert to sql format
                races.append((racename, city, state, sqldate))
    file.close()
    mycursor.executemany(sql, races)
    mydb.commit()
    a = 1


def plot_registration_windows():
    direc = 'C:/Users/willi/PycharmProjects/Sandbox/data/'
    fn = f'{direc}100M_registrations.xlsx'
    df = pd.read_excel(fn, engine='openpyxl')
    jan1 = datetime.datetime(2025, 1, 1)
    yr = datetime.timedelta(days=365)
    j = 0
    for i in df.index:
        rd, lo, lc, ld = df['Race Date'][i], df['Registration Opens'][i], df['Registration Closes'][i], \
            df['Lottery Drawing'][i]
        while rd < jan1:  # bring into this year
            rd, lo, lc, ld = rd + yr, lo + yr, lc + yr, ld + yr
        if all([d is not pd.NaT for d in [rd, lo, lc, ld]]):
            plt.plot(rd, j, 'd', c=clrs[j % 10])
            plt.annotate(df['Race'][i], (rd, j))
            plt.plot([lo, lc], [j, j], f'v--', c=clrs[j % 10])
            plt.plot(ld, j, '^', c=clrs[j % 10])
            j += 1
        else:
            plt.plot(rd, -1, 'ks', alpha=.5)

    plt.plot(np.nan, 'kd', label='Race Date')
    plt.plot(np.nan, 'kv', label='Lottery Registration Window')
    plt.plot(np.nan, 'k^', label='Lottery Drawing')
    plt.plot(np.nan, 'ks', alpha=.5, label='Non-lottery 100s')
    plt.xlabel('Date')
    plt.legend(loc='upper left')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().yaxis.set_ticks([])
    plt.gcf().autofmt_xdate()

    plt.show()


if __name__ == '__main__':
    update_sql_database()
    # plot_registration_windows()
