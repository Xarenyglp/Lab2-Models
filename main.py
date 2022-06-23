
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
import visualizations

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
# Experiment 1
#functions.Model1_E1(midprices)
# Experiment 2
x,y = functions.Model1_E2(midprices)
g1 = visualizations.APT_graph(x)
g1.show()

#################################################################################################################
# Experiment 3: Martingale Process with Weighted MidPrice
# Wmidprices from metrics dataframe

functions.Model1_E3(ob_df)

#################################################################################################################
# MODEL 2 - ROLL MODEL
roll1, roll2 = functions.Model2(pd.DataFrame(midprices),ob_df)

g2 = visualizations.Model2_TS_observed(roll1)
g2.show()

g3 = visualizations.Model2_TS_Theoretical(roll1)
g3.show()

