
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


def Model1_E1(midprices: pd.Series = None):
    """
    Model 1: Asset Pricing Theory - Experiment 1
    This function evaluates the martingale process as explained in the commentaries
    in order for it to find whether the APT hypothesis is valid for the MidPrices 
    observed in the orderbook.

    Parameters
    ----------
    midprices (pd-Series) : Series containing the midprices and the timestamp of the 
    orderbook on which midprices ocurred.

    Returns
    -------
    APT_df : DataFrame containing the results of the APT evaluation over the midprices



    """




    # Asset pricing model: Best estimator for future prices is current price
    # Is it valid most of the time?
    # e1: Martingale process for all midprices that are exactly the same as their future counterpart
    e1 = [midprices[i] == midprices[i+1] for i in range(len(midprices)-1)]
    # e2: Those midprices that ain't the same as their future counterparts.
    e2 = [midprices[i] != midprices[i+1] for i in range(len(midprices)-1)] 

    # Collecting results on dictionary
    APT_dict = {"e1" : {"amount" : np.round(sum(e1),2), "ratio" : np.round(sum(e1)/len(midprices)-1,2)}, 
                "e2" : {"amount" : np.round(sum(e2),2), "ratio" : np.round(sum(e2)/len(midprices)-1,2)},
                "total" : np.round(len(midprices)-1,2) }

    # Printing Results as DataFrame
    APT_df = pd.DataFrame(APT_dict).T
    return APT_df
    
    
def Model1_E2(midprices: pd.Series = None):
    """
    Model 1 Experiment 2: Asset Pricing Theory Hypothesis using minute-segmented data
    This function tests the APT Hypothesis on a minute-segmented data of the provided 
    midprices.

    Parameters
    ----------
    midprices (Series) : Series containing both the midprices and its timestamps

    Returns
    -------
    APT_dict_df (DataFrame) : DataFrame containing the result of the Model 1
    Hypothesis for each timestamp
    APT_results_df (DataFrame) : DataFrame containing the mean of the results of 
    the previous returned DataFrame, in order for us to check the whole 
    results of the Model 1 Hypothesis on the minute segmented data.



    """ 
    
    
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
            {"e1" :{"amount" :  e1, "ratio" : e1/(len(dic[i])-1)}, 
            "e2" :{"amount" :  e2, "ratio" : e2/(len(dic[i])-1)},
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
        templiste1.append(APT_dict_min[i]["e1"]["amount"])
        templiste2.append(APT_dict_min[i]["e2"]["amount"])
        templisttot.append(APT_dict_min[i]["total"])
        templistp1.append(APT_dict_min[i]["e1"]["ratio"])
        templistp2.append(APT_dict_min[i]["e2"]["ratio"])

    APT_dict_df = {"e1":templiste1,
                "e2":templiste2,
                "total":templisttot,
                "ratio1":templistp1,
                "ratio2":templistp2}
    APT_dict_df = pd.DataFrame(data=APT_dict_df)
    APT_dict_df.index = list(APT_dict_min)

    # Totals, table
    APT_results_df = pd.DataFrame(data = {
        "Total trades" : np.array(APT_dict_df["total"]).sum()+60,
        "E1 Ratio Mean" : np.array(APT_dict_df["ratio1"]).mean(),
        "E2 Ratio Mean" : np.array(APT_dict_df["ratio2"]).mean()
    }, index = range(1))
    return APT_dict_df,APT_results_df






def Model1_E3(ob_df: pd.DataFrame = None):
    """
    Model 1 Experiment 3: Asset Pricing Theory over Volme-Weighted-Mid Prices
    both for the entire data, and minute segmented data.

    Parameters
    ----------
    ob_df (Dataframe) : OrderBook DataFrame containing the VWMP and the timestamps

    Returns
    -------
    WAPT_df (DataFrame) : DataFrame containing the results of the APT evaluation over the VWMP
    WAPT_dict_df (DataFrame) : DataFrame containing the result of the Model 1
    Hypothesis for each timestamp
    WAPT_results_df (DataFrame) : DataFrame containing the mean of the results of 
    the previous returned DataFrame, in order for us to check the whole 
    results of the Model 1 Hypothesis on the minute segmented data.
    """


    Wmidprices = ob_df["Weighted MidPrice (Ask)"]

    # Asset pricing model: Best estimator for future prices is current price
    # Is it valid most of the time?
    # e1: Martingale process for all midprices that are exactly the same as their future counterpart
    e1 = [Wmidprices[i] == Wmidprices[i+1] for i in range(len(Wmidprices)-1)]
    # e2: Those midprices that ain't the same as their future counterparts.
    e2 = [Wmidprices[i] != Wmidprices[i+1] for i in range(len(Wmidprices)-1)] 

    # Collecting results on dictionary
    WAPT_dict = {"e1" : {"amount" : np.round(sum(e1),2), "ratio" : np.round(sum(e1)/(len(Wmidprices)-1),2)}, 
                "e2" : {"amount" : np.round(sum(e2),2), "ratio" : np.round(sum(e2)/(len(Wmidprices)-1),2)},
                "total" : np.round(len(Wmidprices)-1,2) }

    # Printing Results as DataFrame
    WAPT_df = pd.DataFrame(WAPT_dict).T
    Wmidprices = pd.DataFrame(Wmidprices)
    # Second Experiment (Every Minute Data)
    # Separing timestamps into minutes data
    dic = {} # Empty dictionary, used for storing midprices separed for every minute
    for index, row in Wmidprices.iterrows(): # Iterating over the timestamps, the rows of the midprices df
        key = str(index.hour) + ":" + str(index.minute) # New key: Hour + Minute of the timestamp (used to avoid minute repetitions)
        value = row["Weighted MidPrice (Ask)"] # Value equals to the row value of the midprice at the iteration
        try: # If succesful in finding the key (extracted above) append the value
            dic[key].append(value)
        except KeyError: # If not succesful in finding the key (extracted above) create the new key, with its first value being the value at the iteration
            dic[key] = [value]

    # Obtaining APT of each minute
    WAPT_dict_min = {} # New empty dictionary
    for i in list(dic): # Iterating over all the timestamps in the dic dictionary (the ones that are in the [hour:minute] format)
        e1 = sum([dic[i][i_t] == dic[i][i_t+1] for i_t in range(len(dic[i])-1)]) # Martingale process, exactly the same as previous e1
        e2 = sum([dic[i][i_t] != dic[i][i_t+1] for i_t in range(len(dic[i])-1)]) # same
        WAPT_dict_min[i] = ( # Appending the newly created variables to the dictionary
            {"e1" :{"amount" :  e1, "ratio" : e1/(len(dic[i])-1)}, 
            "e2" :{"amount" :  e2, "ratio" : e2/(len(dic[i])-1)},
            "total" : len(dic[i])-1
            }
            )

    # Resuming results in a DataFrame
    templiste1 = []
    templiste2 = []
    templisttot = []
    templistp1 = []
    templistp2 = []
    for i in list(WAPT_dict_min):
        templiste1.append(WAPT_dict_min[i]["e1"]["amount"])
        templiste2.append(WAPT_dict_min[i]["e2"]["amount"])
        templisttot.append(WAPT_dict_min[i]["total"])
        templistp1.append(WAPT_dict_min[i]["e1"]["ratio"])
        templistp2.append(WAPT_dict_min[i]["e2"]["ratio"])

    WAPT_dict_df = {"e1":templiste1,
                "e2":templiste2,
                "total":templisttot,
                "ratio1":templistp1,
                "ratio2":templistp2}
    WAPT_dict_df = pd.DataFrame(data=WAPT_dict_df)
    WAPT_dict_df.index = list(WAPT_dict_min)

    # Totals, table
    WAPT_results_df = pd.DataFrame(data = {
        "Total trades" : np.array(WAPT_dict_df["total"]).sum()+60,
        "E1 Ratio Mean" : np.array(WAPT_dict_df["ratio1"]).mean(),
        "E2 Ratio Mean" : np.array(WAPT_dict_df["ratio2"]).mean()
    }, index = range(1))
    return WAPT_df,WAPT_dict_df,WAPT_results_df


def Model2(midprices: pd.DataFrame = None, ob_df: pd.DataFrame = None):
    """
    Model 2: Roll model
    This states that the best estimator for the OrderBook Spread can be obtained
    through the autocovariance of the price differences vs the previous price differences.
    In order to test this Hypothesis, the midprices are provided as the prices,
    as well as the orderbook spread in order for us to find what the actual spread was vs.
    what the estimated Spread was.

    Parameters
    ----------
    midprices (pd.DataFrame) : DataFrame containing the midprices
    ob_df (DataFrame) : Dataframe containing the spread of the orderbooks.

    Returns
    -------
    roll_df (DataFrame) : DataFrame containing the results of the spread and prices estimators
    for all timestamps
    roll_df_stats (DataFrame) : Spread Metrics (Mean, Variance) and its comparison in order to
    check whether the hypothesis was correct or not.

    """



    # Model 2
    # Roll Model
    # This Model Uses the price change covariance to deduce the spread of the OrderBook
    # In order for us to find such Spread, first we need the price changes of the Mid Price

    dP_t = midprices["Mid Price"].diff(1) # Present price changes
    dP_t_1 = midprices["Mid Price"].shift(1).diff(1) # 1 instant in time shifted mid prices
    # We now need to find this prices Covariance
    cov = pd.DataFrame({
        "dP_t" : dP_t, "dP_t_1" : dP_t_1
    }).cov().iloc[1,0]
    # Constant C is Sqrt(-cov)
    C = np.sqrt(-cov)
    # Spread is Supossed to be 2*C
    CalcSpread = 2*C

    # Comparing with the obtained spread in the orderbook

    roll_df = pd.DataFrame(
        data = {
            "Spread (OB)" : ob_df["Spread"],
            "Calculated Spread" : CalcSpread,
            "Bid" : midprices["Mid Price"] - ob_df["Spread"],
            "Ask" : midprices["Mid Price"] + ob_df["Spread"],
            "Calc Bid": midprices["Mid Price"] - CalcSpread,
            "Calc Ask" : midprices["Mid Price"] + CalcSpread            
        }, index = midprices.index
    )

    # Modelling spread as a Random Variable and comparing it to the results obtained in Roll
    roll_df_stats = pd.DataFrame({
        "Spread Mean" : roll_df["Spread (OB)"].mean(),
        "Spread Variance" : roll_df["Spread (OB)"].var(),
        "Calculated Spread" : roll_df["Calculated Spread"][0]
    },index = range(1))
    roll_df_stats["Spread Difference"] = roll_df_stats["Spread Mean"] - roll_df_stats["Calculated Spread"]
    return roll_df,roll_df_stats

