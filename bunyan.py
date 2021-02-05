# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---


# TODO: add notification by email feature on failure

import datetime as dt
import os
import requests
from piapiwrapper import *
from analytics import *   
import time
import pathlib


## constant
proj_path = str(pathlib.Path().absolute())
market_dir = proj_path + "/markets/"

def whatTimeIsIt():
    time_localtime = time.localtime()
    time_format = "%b %-d, %Y %-I:%M %p"
    time_result = time.strftime(time_format, time_localtime)  # print time
    print(time_result)


# If there's no csv for that market
    # make one
# If there is a csv for that market already,
    # append the data onto the opened csv 
    # and save that csv
while(True):

    ### change every minute
    try:
        my_market_data = getAllMarketsList()  # pull data from API
    except:
        print("swing and a miss for time: ", end="")
    
    whatTimeIsIt()  # print time 


    # for each market
    for mkt_id in getIdIndexList(market_data=my_market_data):   
        mkt_id = mkt_id
        csv_filename = market_dir + str(mkt_id) + ".csv"  # get absolute filename for csv

        my_market_df = getMarket(mkt_id, market_data=my_market_data)

        try:
            # if a csv exists, append data to csv
            longterm_mkt_df = pd.read_csv(csv_filename)
            longterm_mkt_df = longterm_mkt_df.append(my_market_df) # add the most recent data
            longterm_mkt_df.to_csv(path_or_buf=csv_filename, index=False)
        except FileNotFoundError:
            # create a csv for that market
            my_market_df.to_csv(path_or_buf=csv_filename, index=False)
    # end each market saving
    time.sleep(120)