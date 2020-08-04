# Scrapping HTML data for fetching independent variable

from AQI_Part2 import avg_data_year # importing function from AQI_part2.py file
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv

# for i in range(2013,2014):
#     a= avg_data_year(i)
#     print(len(a))

def meta_data(year, month):

    file_html= open(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\HTML_data\{}\{}.html'.format(year, month), 'rb') # reading each html file
    plain_text= file_html.read()

    temp_data= []
    final_data= []

    soup= BeautifulSoup(plain_text, 'lxml') # giving error for lxml so downloaded it 'lxml'
    for table in soup.find_all('table', {'class': 'medias mensuales numspan'}): # on table tag, we have to find this class
        for tbody in table: # inside the above class, there tbody tag
            for tr in tbody: # inside tbody tag, there are tr tags
                # for td in tr:
                #     a= td.get_text()
                #     temp_data.append(a)
                a= tr.get_text() # fetching text from each 'tr' tags
                temp_data.append(a) # each iteration give one row
    # print(len(temp_data)) #496
    rows= len(temp_data)/15 # dividing by 15 becuz total 15 columns to find out the rows. present in website eg. https://en.tutiempo.net/climate/ws-421810.html
    # print(rows) # 33.06. why we divide by 15 becuz all data are in list so we need to separate each by 15 so converting into rows

    for times in range(round(rows)):
        newtemp_data= []
        for i in range(15):
            newtemp_data.append(temp_data[0]) # giving only 0th index in each iteration till 14th index
            temp_data.pop(0) # then removing 0th index value in each iteration from temp_data object
        final_data.append(newtemp_data)

    # print(final_data) # it will contain list of lists i.e rows
    # print(len(final_data)) # 33 only for Januray 2013 data
    length= len(final_data)

    final_data.pop(length-1) # dropping the last row bcuz not important one
    final_data.pop(0) # delete this as well bcuz this row contains column name
    # print(final_data)

    for a in range(len(final_data)): # Removing that index value which we dont want or deleting not important feature values
    #     # print(final_data[a])
        final_data[a].pop(0) # day if we do popping then index value will be changed so change accordingly
        final_data[a].pop(5) # PP bcuz containing all 0 values
        final_data[a].pop(8) # VG
        final_data[a].pop(8) # RA
        final_data[a].pop(8) # SN
        final_data[a].pop(8) # TS
        final_data[a].pop(8)  # FG
    # print(len(final_data[0]))
    return final_data

def data_combine(year, cs):  # Data will be combined
    for a in pd.read_csv('Data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist



if __name__ == "__main__":

    if not os.path.exists(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\Real-Data'): # making new directory real-data if not exists
        os.makedirs(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\Real-Data')

    for year in range(2013, 2017):
        final_data = []
        with open(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\Real-Data\real_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel') # dialect means styling looks like excel
            wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5']) # writing first row i.e column name
        for month in range(1, 13): # total months 1 to 12
            temp = meta_data(year, month) # fetching the independent variables rows from above function
            final_data = final_data + temp # saving all in one list of each year
        # print(len(final_data)) #365 for Januray month
        # print(f'length of independent in {year} is {len(final_data)}')

        pm_target_data= avg_data_year(year) # calling function from AQI_part2.py fileand storing target rows
        # print(len(pm_target_data)) # 365
        # print(pm_target_data)
        # print(f'length of target in {year} is {len(pm_target_data)}')

        for i in range(len(final_data)): # This is used to insert target variable rows in final_data list
        #     # final[i].insert(0, i + 1)
            final_data[i].insert(8, pm_target_data[i]) # adding data at last index i.e 8 (PM2.5)
        print(final_data)

        with open(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\Real-Data\real_' + str(year) + '.csv',  'a') as csvfile: # Writing above data to csv file
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                wr.writerow(row)
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-": # if row containing blank or '-' then dont write to file
                        flag = 1
                if flag != 1:
                    wr.writerow(row)

    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)

    total = data_2013 + data_2014 + data_2015 + data_2016

    with open('Data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)

df = pd.read_csv(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\Real-Data\Real_Combine.csv')
