import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import numpy as np



st.title("MARKET LAB")
ticker=None
data=None


###INPUTS block###
with st.sidebar:
    st.title("Settings")
    ticker = st.text_input("Enter any asset...")

    Period = st.selectbox(
        "Time Period",
        ["1d","1mo","3mo","6mo","1y","5y","max"]
    )

    Interval = st.selectbox(
        "Interval",
        ["1m", "2m", "5m", "15m", "30m", "1h", "1d"]
    )

    load = st.button("Load Chart")
    chart = st.radio(
        "Chart type",
        ["Candlesticks","Line"]
    )
    
    
###CHART generation

if load:  

    
    data = yf.download(
        ticker,
        period=Period,
        interval=Interval,
        progress=False,
        auto_adjust=False
        )

    


    
    if data.empty: 
        st.error("Ticker not found!")
    elif chart is "Candlesticks":


        # This block of code checks if data is a dataframe with multiple levels and
        # in case selects only the columns from the first level (the one with prices),
        # this yield a linear 1D array that can be used by the go.Candlestick function
        if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
            data.columns = data.columns.get_level_values(0)
            
        fig = go.Figure()


        fig.add_trace(go.Candlestick(
            x = data.index,
            open = data['Open'],
            close = data['Close'],
            high = data['High'],
            low = data['Low'],
        ))


        fig.update_layout(
            title = f"{ticker} CHART",
            dragmode="zoom",
            xaxis_rangeslider_visible=False,
            height=600
        )

        
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
            "scrollZoom": True,
            "displayModeBar": True
            }
        )



        
    elif chart is "Line":
        
        # To plot a line chart we can directly use streamlit library
        Date = data.index.tolist()
        Close = np.array(data['Close'])
        Open = np.array(data['Open'])
        Avg = (Open + Close)/2   # To plot the price we compute the average between each opening and closure

        df = pd.DataFrame(data=Avg,index=Date,columns=["Prices"])
    
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Prices"],
            mode="lines",
            name="Price"
            )
        )

        fig.update_layout(
            title = f"{ticker} CHART",
            dragmode="zoom",
            xaxis_rangeslider_visible=False,
            height=600
        )

        
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
            "scrollZoom": True,
            "displayModeBar": True
            }
        )

        
       
        
        
        
    
    
