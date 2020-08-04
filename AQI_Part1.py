# Taking data from https://en.tutiempo.net/ which is 3rd party url and free

import os
import time
import requests
import sys

def retrieve_html():
    for year in range(2013,2019): # Taking 5 years data for delhi/palam city
        for month in range(1,13):
            # print(month)
            if (month<10): # taking condition becuz to put 0 in url
                url= 'https://en.tutiempo.net/climate/0{}-{}/ws-421810.html'.format(month, year) # formatting has been done to fetch data %i, %i from url. e.g--> https://en.tutiempo.net/climate/01-2013/ws-421810.html
            else:
                url = 'https://en.tutiempo.net/climate/{}-{}/ws-421810.html'.format(month, year)
            # print(month)
            texts= requests.get(url) # fetching data from url
            text_utf= texts.text.encode('utf=8') # some tags in HTMl to fix it by using utf-8

            if not os.path.exists(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\HTML_data\{}'.format(year)): # if this path does not exist then create
                os.makedirs(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\HTML_data\{}'.format(year))
            with open(r'C:\Users\egoeshu\Desktop\testingdoc\AQI_ML\data\HTML_data\{}\{}.html'.format(year, month), 'wb') as output: # store data in every month.html file
                output.write(text_utf)

        sys.stdout.flush()


if __name__== '__main__': # starting line in python
    start_time= time.time()
    retrieve_html()
    stop_time= time.time()
    print(f'Total time taken is {stop_time- start_time}') # o/p Total time taken is 102.63164043426514