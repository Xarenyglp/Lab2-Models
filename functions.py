
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Microstructure and Trading Systems - Lab 2 Models                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: Xarenyglp                                                                                   -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: https://github.com/Xarenyglp/Lab2-Model                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import numpy as np
import pandas as pd


def df_metrics(data_ob: dict = None):
    """
    OrderBook df_metrics
    Obtains the 11 df_metrics necessary for microstructure analysis of an Orderbook.
    The df_metrics returned are:
    -1. Median of time between trades
    -2. Spread of price
    -3. Midprice of given timestamp
    -4. Number of price levels
    -5. Bid Volume
    -6. Ask Volume
    -7.Total Volume
    -8. Volume Imbalance
    -9. Ask Weighted Midprice
    -10. Bid Weighted Midprice
    -11. Volume-Weighted-Average Price

    All df_metrics, with the exception of df_metrics 1 and 4 (Median time between trades and Number of 
    Price Levels) are returned within a DataFrame, with the value of each metric corresponding to 
    its timestamp.
    
    Parameters
    ----------
    data_ob (dict) : Dictonary containing the OrderBook

    Returns
    -------
    df_df_metrics : DataFrame containing the df_metrics obtained from the OrderBook
    m1 : Median of time between trades
    m4 : Number of price levels in the OrderBook
    


    """
    ob_ts = list(data_ob.keys())
    l_ts = [pd.to_datetime(i_ts) for i_ts in ob_ts]
    # Median timedelta
    m1 = np.median([l_ts[n_ts+1]-l_ts[n_ts] for n_ts in range(len(l_ts)-1)]).total_seconds()*1000
    # Spread
    m2 = [data_ob[ob_ts[i]]["ask"][0]- data_ob[ob_ts[i]]["bid"][0] for i in range(len(ob_ts))]
    # MidPrice
    m3 = [(data_ob[ob_ts[i]]["ask"][0]+ data_ob[ob_ts[i]]["bid"][0])*0.5 for i in range(len(ob_ts))]  
    # Price Levels
    m4 = [data_ob[i_ts].shape[0] for i_ts in ob_ts]   
    # Bid Volume
    m5 = [np.round(data_ob[i_ts]["bid_size"].sum(), 6) for i_ts in ob_ts]  
    # Ask Volume
    m6 = [np.round(data_ob[i_ts]["ask_size"].sum(), 6) for i_ts in ob_ts] 
    # Total Volume
    m7 = [np.round(data_ob[i_ts]['bid_size'].sum() + data_ob[i_ts]['ask_size'].sum() , 6) for i_ts in ob_ts]  
    # Orderbook Imbalance
    m8 = [m5[i_ts]/m7[i_ts] for i_ts in range(len(ob_ts))]
    #  Weighted-Midprice (Ask): ((Bid_Volume/ Bid_Volume + Ask Volume )) * ((bid_price[0] + ask_price[0])/2)
    m9 = [m8[i_ts]*m3[i_ts] for i_ts in range(len(ob_ts))]
    # Weighted-MidPrice (Bid): ((Ask_Volume/ Bid_Volume + Ask Volume )*Bid_Price) + ((Bid_Volume/ Bid_Volume + Ask Volume )*Ask_Price)
    m10 = [ (m6[i_ts]/(m5[i_ts] + m6[i_ts]) * data_ob[ob_ts[i_ts]]['bid'][0]) + (m8[i_ts]*(data_ob[ob_ts[i_ts]]['ask'][0])) for i_ts in range(len(ob_ts)) ]
    Bids_ToB = [data_ob[ob_ts[i]]['bid'][0] for i in range(len(ob_ts))]
    Asks_ToB = [data_ob[ob_ts[i]]['ask'][0] for i in range(len(ob_ts))]
    # VWAP (Volume-Weighted-Average Price)
    m11 = [np.round((Bids_ToB[i]*m5[i] + Asks_ToB[i]*m6[i]) / (m5[i]+m6[i]),6) for i in range(len(ob_ts))]

    df_metrics = pd.DataFrame({
        "Spread" : m2,
        "Mid Price" : m3,
        "Bid Volume" : m5,
        "Ask Volume" : m6,
        "Total Volume" : m7 ,
        "OrderBook Imbalance" : m8,
        "Weighted MidPrice (Ask)" : m9,
        "Weighted MidPrice (Bid)": m10,
        "Volume Weighted Average Price" : m11
        
    })
    df_metrics.index = l_ts
    return df_metrics, m1, m4# Returns df_metrics dataframe, median of trades and no. of priceLevels
