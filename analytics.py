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

# +
import importlib

import requests
import string 
import pandas as pd
import time   
import datetime as dt

from apiwrapper import *

# +
# get the raw string time of a particular market's dataframe
def getRawRetrievalTime(mkt_id, market_data=None):
    market_data = fetchIfNoMarketData(market_data)
    
    return getRawMarketInfo(mkt_id, market_data=market_data)["marketTimestamp"][0]


# takes the API's formatted string and returns a datetime object
def getDateTime( time_str ):
    if( len(time_str) == 19 ):   # date and time without milliseconds 
        return dt.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
    elif( 25 <= len(time_str) <= 27): # date and time with 5 digits of milliseconds
        time_str = time_str[:-1] # cut off last millisecond
        return dt.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')  
    else:
        print(f"Unfamiliar with the time format: {time_str} with length {len(time_str)}")
        return dt.datetime.now()

# return a more comprehensible time format
def getHumanTime(time):
    if(type(time) == str):  # seems like leverage python/ duck typing, wbn
        if(len(time) <= 4):
            return "NA"
        
        time = getDateTime( time )
    return dt.datetime.strftime(time, '%b %-d, %Y %-I:%M %p')



# -

def getMarket(mkt_id, market_data=None):
    market_data = fetchIfNoMarketData(market_data)
    
    mkt_df = getRawMarketInfo(mkt_id, market_data)
    mkt_df["marketTimestamp"] = mkt_df["marketTimestamp"].apply(getHumanTime)
    mkt_df["dateEnd"] = mkt_df["dateEnd"].apply(getHumanTime)

    lesser_labels = ["marketName", "marketImage", "marketContracts",
                      "marketStatus",  "dateEnd", "displayOrder",
                      "image", "name", "status", "id" ]

    mkt_df = mkt_df.drop(labels=lesser_labels, axis=1)
    return mkt_df
