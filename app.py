import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.widgets import RangeSlider
import seaborn as sns
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM, GRU
from sklearn.preprocessing import MinMaxScaler
import datetime
# import pickle
import streamlit as st
from PIL import Image
import model_building as m
import technical_analysis as t
import correlation_analysis as c
import mpld3
import streamlit.components.v1 as components
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import  BollingerBands




img = Image.open('image.png')


st.set_page_config(
    page_title="Algo-Trading-WebApp",
    page_icon="image.png",
    layout="wide",
    initial_sidebar_state="expanded",
       
)


######################
# Page Title
######################

image = Image.open('stock.jpg')

st.image(image, use_column_width=True)




with st.sidebar:
    
    st.markdown("# Equity Analysis & Forecasting")
    user_input = st.selectbox(
    'Please select the Equity for forecasting and technical analysis ',
    ('TATASTEEL.NS','ADANIENT.NS','RELIANCE.NS','INFY.NS'))
    # user_input = st.text_input('Enter Stock Name', "ADANIENT.NS")
    st.markdown("### Choose Date for your anaylsis")
    date_from = st.date_input("From",datetime.date(2015, 1, 1))
    date_to = st.date_input("To",datetime.date(2023, 1, 1))
    options = st.multiselect(
        'Select equity for diversification analysis(select minimum Stocks/Equity)',
        ['TATASTEEL.NS','ADANIENT.NS','RELIANCE.NS','INFY.NS'],
        ['TATASTEEL.NS']
    )
    # st.write('You selected:', options[0])
    btn = st.button('Submit') 

#adding a button
if btn:
    df = yf.download(user_input, start=date_from, end=date_to)
    plotdf, future_predicted_values =m.create_model(df)
    st.subheader('Raw Data')
    st.write(df.describe())

    
    st.markdown("### Original vs predicted close price with Rangeslider")
    fig = go.Figure()
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], name="stock_open"))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name="stock_close"))
    fig = px.line(plotdf,x=plotdf['Date'], y=[plotdf['original_close'],plotdf['train_predicted_close'], plotdf['test_predicted_close']],labels={'value':'Stock price','Date': 'Date'})
    fig.update_layout(title_text=' original close price vs predicted close price',font_size=10, font_color='white',legend_title_text='Close Price',title_x = 0.5, width = 1200, height = 800,xaxis_rangeslider_visible=True)
    fig.add_shape(       
            type="rect",
            xref="paper",
            yref="paper",
            x0=0,
            y0=0,
            x1=1.0,
            y1=1.0,
            line=dict(
                color="white",
                 width=1,
             )
         )
   # fig.update_la(title_text=' original close price vs predicted close price', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    
  
   

    st.markdown("<h2 style='text-align: center; color: black;'>Next 30 days forecast </h2>", unsafe_allow_html=True)
    list_of_days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7","Day 8", "Day 9", "Day 10", "Day 11" ,"Day 12","Day 13",
                   "Day 14","Day 15","Day 16","Day 17","Day 18","Day 19","Day 20","Day 21","Day 22","Day 23","Day 24","Day 25","Day 26",
                    "Day 27","Day 28","Day 29","Day 30"]
     

    for i,j in zip(st.tabs(list_of_days),range(30)):
        with i:
            st.write(future_predicted_values.iloc[j:j+1])
           
  
   
    st.markdown("### Adj Close Price")
    fig= plt.figure(figsize=(20,10))
    t.last_8_years_price_plot(df)
    st.pyplot(fig)

    st.markdown("### Trend Analysis")
    fig= plt.figure(figsize=(20,10))
    t.trend_pie_chart(df)
    st.pyplot(fig)

   


    st.markdown("## Technical Analysis")

    st.markdown("### SMA Indicator")
   
    fig= plt.figure(figsize=(20,10))
    t.sma_plot(df)
    st.pyplot(fig)
    
    st.write(" ***:blue[Strategy:]:***")
    st.write(":red[Sell  Signal:] When the 50-day SMA crosses below the 200-day SMA.")
    st.write(":green[Buy Signal:] When the 50-day SMA crosses above the 200-day SMA.")

    st.markdown("### EMA Indicator")
   
    fig= plt.figure(figsize=(20,10))
    t.ema_plot(df)
    st.pyplot(fig)
    st.write(" ***:blue[Strategy:]:***")
    st.write(":red[Sell  Signal:] When the 50-day EMA crosses below the 200-day EMA.")
    st.write(":green[Buy Signal:] When the 50-day EMA crosses above the 200-day EMA.")
   
    st.markdown("### Diversified Portfolio Analysis")
    combined_df = yf.download(options, start=date_from, end=date_to)['Adj Close']
    combined_df = combined_df.round(2)
    
    fig= plt.figure(figsize=(20,10))
    c.corr_plot(combined_df)
    st.pyplot(fig)

    st.write(" ***:blue[Strategy:]:*** All the stocks which do not show significant correlation can be included in a portfolio.")
    
    
else:
    st.write('Please click on the submit to get the analysis') #displayed when the button is unclicked
    
    
    
   

    
        
