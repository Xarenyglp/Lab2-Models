
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Microstructure and Trading Systems - Lab 2 Models                                                        -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: Xarenyglp                                                                                   -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: https://github.com/Xarenyglp/Lab2-Model                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import plotly.express as px
import plotly.io as pio
import pandas as pd
import functions as ft
import data as dt

def Model1_Prices_Comparison(data: pd.DataFrame = None,filename: str = None):
    """
    Model 1 Graphical Hypothesis Evaluation
    This function displays a graph on which the prices and the future prices are
    overlapped, in order for us to test the Model 1 hypothesis, which is:
    "The best estimator for the future price is the current price"

    Parameters
    ----------
    data (DataFrame) : 

    Returns
    -------
    None
    
    """

    midpricesshift = data.iloc[1:]
    df = pd.DataFrame({
        "Mid Price" : data,
        "Mid Price t_1" : midpricesshift
    })
    fig = px.line(df)
    pio.write_image(fig,"files/"+filename+".png")
    fig.show()
def Model1_graph_results_t1(data: pd.DataFrame = None,filename: str = None) -> True:
    """
    Experiment 1 Graphical Results Type 1
    Returns Bar plot for the number of succesful predictions and unsuccesful 
    for the first experiment of the model

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    None
    """
    fig = px.bar(data, x="amount")
    pio.write_image(fig,"files/"+filename+".png")
    fig.show()
    

def Model1_graph_results_t2(data: pd.DataFrame = None,filename: str = None) -> True:
    """
    Experiment 1 Graphical Results Type 2
    Returns Histogram

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    None
    """
    fig = px.histogram(data,x="ratio1")
    pio.write_image(fig,"files/"+filename+".png")
    fig.show()

def Model1_graph_results_t3(data: pd.DataFrame = None,filename : str = None) -> True:
    """
    Experiment 1 Graphical Results
    Returns Bar plot

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    None
    """
    fig = px.bar(data.drop(columns=["Total trades"]))
    pio.write_image(fig,"files/"+filename+".png")
    fig.show()
    
def Model2_graph_results(data: pd.DataFrame = None,filename: str = None) -> True:
    """
    Function Description here
    Plots Line plot comparing actual spread vs calculated spread and histogram showing
    the distribution of the spread.

    Parameters
    ----------
    data (DataFrame) : Parameter Description

    Returns
    -------
    None

    """
    fig1 = px.line(data,y=data.columns[0:2])
    pio.write_image(fig1,"files/"+filename+"1"+".png")
    fig2 = px.histogram(data,x="Spread (OB)")
    pio.write_image(fig2,"files/"+filename+"2"+".png")
    fig1.show()
    fig2.show()