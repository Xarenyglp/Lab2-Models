
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Microstructure and Trading Systems - Lab 2 Models                                                       -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: Xarenyglp                                                                                   -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: https://github.com/Xarenyglp/Lab2-Model                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd 
import json


# File location inside files folder.
filename = "files/orderbooks_05jul21.json"
# Opening JSON file
orderbooks_data = json.load(open(filename))
# Selecting bitfinex data
ob_data = orderbooks_data["bitfinex"]
# Drop None Keys
ob_data = {i_key: i_value for i_key, i_value in ob_data.items() if i_value is not None}
# Convert to dataframe and rearange columns
ob_data = {i_ob: pd.DataFrame(ob_data[i_ob])[["bid_size","bid","ask","ask_size"]]
        if ob_data[i_ob] is not None else None for i_ob in list(ob_data.keys())}




