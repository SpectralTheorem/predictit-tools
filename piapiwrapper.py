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

# TODO email notification on failure

import requests
import string 
import pandas as pd
import time


# int -> response
# returns the web response from the PI API
def getMarketRespose(market_id):
    api_url = "https://www.predictit.org/api/marketdata/markets/"
    joined_url = api_url + str(market_id)
    
    response = requests.get(joined_url)  # fetch market data
    if("null" == response.text):
        print("Bad predictItID -- No market with that ID")
    return response


# None -> list
# returns a list of all open markets 
def getAllOpenMarketIDs():
    if(response.status_code != 200):
        print("Please wait...")
        time.sleep(3)
        print("Please try again now. If this issue persists, the API access may have changed.")

    xml_response = response.json()
    all_markets_df = pd.DataFrame.from_dict(xml_response)


    market_id_list = []  
    
    for market_index in range(len(all_markets_df)):
        # print(all_markets_df["markets"][market_index]["id"])
        market_id = all_markets_df["markets"][market_index]["id"]
        market_id_list.append(market_id)

    return market_id_list


# int -> dataframe
def getMarketDataFrame(market_id):
    response = getMarketRespose(market_id)  
    xml_response = response.json()
    
    market_df = pd.DataFrame.from_dict(xml_response)
    return market_df


# request data for entire market 
# None -> response
def getAllMarketsResponse():
    api_url = "https://www.predictit.org/api/marketdata/all/"
    response = requests.get(api_url)  # fetch market data
    if(response.status_code != 200):
        print("Please wait for API cooldown")
        
        for second in  list(range(10))[::-1]:
            time.sleep(1)
            print(second)
        print("Please try again now. If the issue persists, API access may have changed.")
        return None
    return response



# None -> list of all the open markets
def getAllMarketsList(market_data=None):
    all_markets_response = getAllMarketsResponse()
    return all_markets_response.json()["markets"]

# fetch data if there's none cached
def fetchIfNoMarketData(market_data=None):
    if market_data is None:
        print("Now fetching market data")
        market_data = getAllMarketsList()
        return market_data
    else:
        return market_data

# return list of market IDs
def getIdIndexList( market_data=None):
    market_data = fetchIfNoMarketData(market_data)
    
    id_index_list = []  # initialize empty list

    # for all markets
    for mkt_index in range(len(market_data)):
        id_index_list.append(market_data[mkt_index]["id"])  # append to list
    return id_index_list

# returns all the contracts of a particular market based on the index
# a market index of 0 is the most recent and the largest valid value is the oldest open market
def getContractsDataFrameFromIndex( mkt_index, market_data=None):
    market_data = fetchIfNoMarketData(market_data)
    
    # this references the first market in the list of all markets  ????
    market_df = pd.DataFrame.from_dict(market_data[ mkt_index ]["contracts"])
    return market_df


# using a market id, retrieve the index
def getIndexFromMarketId( mkt_id, market_data=None):
    market_data = fetchIfNoMarketData(market_data)
    
    market_index_list = getIdIndexList(market_data=market_data)
    try:
        
        return market_index_list.index(mkt_id)
    except ValueError:
        print(f"There exists no open contracts with id {mkt_id}.")
        return None
    
    
# returns all the contracts of a particular market based on ID
def getContractsDataFrame( mkt_id, market_data=None):
    market_data = fetchIfNoMarketData(market_data)
    
    # use the mkt_id to find the market index
    market_index = getIndexFromMarketId(mkt_id, market_data=market_data)
    
    return getContractsDataFrameFromIndex(market_index, market_data=market_data)


# adds the word market to a string; used to label market data for concatanation in contracts DataFrame
def concatMarketString(string):
    return "market"+string.capitalize()


# append "market" in front of each column in a dataframe if it doesn't already have the label
# df -> df
def labelMarket(market_df):
    if(market_df.columns[0][0:6] == "market"):  # if marketId is already labeled, they're every column is already labeled (hopefully)
        return market_df
    else:
        return market_df.rename(concatMarketString, axis="columns")


# Return a dataframe of all information API provides for one market
def getRawMarketInfo(mkt_id, market_data=None):
    market_data = fetchIfNoMarketData(market_data)
    
    mkt_index = getIndexFromMarketId(mkt_id, market_data=market_data)
    
    market_df = pd.DataFrame.from_dict(market_data[mkt_index])
    market_df = labelMarket(market_df)

    # contract df 
    contracts_df = getContractsDataFrame(mkt_id, market_data=market_data)
    
    # combine dfs
    return market_df.join(contracts_df)
