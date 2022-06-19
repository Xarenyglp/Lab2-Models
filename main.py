
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Microstructure and Trading Systems - Lab 2 Models                                          -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: Xarenyglp                                                                                   -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: https://github.com/Xarenyglp/Lab2-Model                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import data as dt
import numpy as np
import functions

# Obtaining JSON file from data library (Filename: files/orderbooks_05jul21)
data_ob = dt.ob_data

# Orderbook timestamps
ob_ts = list(data_ob.keys())

# Timestamp listings
l_ts = [pd.to_datetime(i_ts) for i_ts in ob_ts]

# MODEL 1 - ASSET PRICING THEORY
# First Experiment - All midpricess in orderbook

# Metrics from Functions library
ob_df,_,_ = functions.df_metrics(data_ob)
# midpricess from metrics dataframe
midprices = ob_df["Mid Price"]

# Asset pricing model: Best estimator for future prices is current price
# Is it valid most of the time?
# e1: Martingale process for all midprices that are exactly the same as their future counterpart
e1 = [midprices[i] == midprices[i+1] for i in range(len(midprices)-1)]
# e2: Those midprices that ain't the same as their future counterparts.
e2 = [midprices[i] != midprices[i+1] for i in range(len(midprices)-1)] 

# Collecting results on dictionary
APT_dict = {"e1" : {"cantidad" : np.round(sum(e1),2), "proporcion" : np.round(sum(e1)/len(midprices)-1,2)}, 
            "e2" : {"cantidad" : np.round(sum(e2),2), "proporcion" : np.round(sum(e2)/len(midprices)-1,2)},
            "total" : np.round(len(midprices)-1,2) }

# Printing Results as DataFrame
APT_df = pd.DataFrame(APT_dict)
midprices = pd.DataFrame(midprices)
# Second Experiment (Every Minute Data)
# Separing timestamps into minutes data
dic = {} # Empty dictionary, used for storing midprices separed for every minute
for index, row in midprices.iterrows(): # Iterating over the timestamps, the rows of the midprices df
    key = str(index.hour) + ":" + str(index.minute) # New key: Hour + Minute of the timestamp (used to avoid minute repetitions)
    value = row["Mid Price"] # Value equals to the row value of the midprice at the iteration
    try: # If succesful in finding the key (extracted above) append the value
        dic[key].append(value)
    except KeyError: # If not succesful in finding the key (extracted above) create the new key, with its first value being the value at the iteration
        dic[key] = [value]

# Obtaining APT of each minute
APT_dict_min = {} # New empty dictionary
for i in list(dic): # Iterating over all the timestamps in the dic dictionary (the ones that are in the [hour:minute] format)
    e1 = sum([dic[i][i_t] == dic[i][i_t+1] for i_t in range(len(dic[i])-1)]) # Martingale process, exactly the same as previous e1
    e2 = sum([dic[i][i_t] != dic[i][i_t+1] for i_t in range(len(dic[i])-1)]) # same
    APT_dict_min[i] = ( # Appending the newly created variables to the dictionary
        {"e1" :{"cantidad" :  e1, "proporcion" : e1/(len(dic[i])-1)}, 
         "e2" :{"cantidad" :  e2, "proporcion" : e2/(len(dic[i])-1)},
         "total" : len(dic[i])-1
         }
        )

# Resuming results in a DataFrame
templiste1 = []
templiste2 = []
templisttot = []
templistp1 = []
templistp2 = []
for i in list(APT_dict_min):
    templiste1.append(APT_dict_min[i]["e1"]["cantidad"])
    templiste2.append(APT_dict_min[i]["e2"]["cantidad"])
    templisttot.append(APT_dict_min[i]["total"])
    templistp1.append(APT_dict_min[i]["e1"]["proporcion"])
    templistp2.append(APT_dict_min[i]["e2"]["proporcion"])

APT_dict_df = {"e1":templiste1,
               "e2":templiste2,
               "total":templisttot,
               "proporcion1":templistp1,
               "proporcion2":templistp2}
APT_dict_df = pd.DataFrame(data=APT_dict_df)
APT_dict_df.index = list(APT_dict_min)


# Model 2