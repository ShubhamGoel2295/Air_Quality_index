# Fetching the dependent feature 'PM2.5' from excel sheets and these sheets have been fetched from mapweather.com which 3 party URL and paid one..

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def avg_data_year(year):
    temp_i= 0
    average=[]
    dd= pd.read_csv(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\AQI\aqi{}.csv'.format(year))
    # print(dd.tail())
    # print(dd[dd['Date']=='31/1/2013'])
    # print(dd['Date'].unique())
    # print(len(dd['Date'].unique()))
    # print(len(dd))
    # print(len(dd)/365)
    for rows in pd.read_csv(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\AQI\aqi{}.csv'.format(year), chunksize=24): # chunkszie becuz 24 rows needs to average for 1 day
        # print(rows)
        add_var=0
        avg= 0.0
        data=[]
        df= pd.DataFrame(data=rows)
        # print(df)
        for index, row in df.iterrows():
            data.append(row['PM2.5'])
        # print(data)
        for i in data:
            if type(i) is float or type(i) is int:
                add_var= add_var+i
            elif type(i) is str:
                if i!='NoData' and i!= 'PwrFail' and i!= '---' and i!= 'InVld':
                    temp= float(i)
                    add_var= add_var+temp
        avg= add_var/24
        temp_i= temp_i +1

        average.append(avg)

    if len(average)== 364: # Some o/p is showing total 364 instead if 365 becuz 31st dec data is missing so filling it with '-'
        average.insert(364, '-')

    if year%4 == 0: # if leap year then fill 29th feb with '-' as data is missing
        average.insert(59, '-') # starting from 0 to 29th feb
    return average

if __name__== '__main__':

    list_2013 = avg_data_year(2014)
    # list_2014 = avg_data_year(2014)
    # list_2015 = avg_data_year(2015)
    # list_2016= avg_data_year(2016)
    # list_2017= avg_data_year(2017)
    # list_2018= avg_data_year(2018)

    # for i in [list_2013, list_2014, list_2015, list_2016, list_2017, list_2018]:
    #     print(f'length are {len(i)}')
