import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import datetime
import warnings
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
warnings.filterwarnings('ignore')

def calculated_df(df):
    df['Date'] = df.index
    df['Day_Perc_Change'] = df['Adj Close'].pct_change()*100
    df.dropna(inplace= True)
    df['Trend']= np.zeros(df['Day_Perc_Change'].count())
    df['Trend']= df['Day_Perc_Change'].apply(lambda x:trend(x))
    return df

def last_8_years_price_plot(df):
    df['Adj Close'].plot()
    plt.xlabel('Date')
    plt.ylabel('Adj Close Price')



def trend(x):
    if x > -0.5 and x <= 0.5:
        return 'Slight or No change'
    elif x > 0.5 and x <= 1:
        return 'Slight Positive'
    elif x > -1 and x <= -0.5:
        return 'Slight Negative'
    elif x > 1 and x <= 3:
        return 'Positive'
    elif x > -3 and x <= -1:
        return 'Negative'
    elif x > 3 and x <= 7:
        return 'Among top gainers'
    elif x > -7 and x <= -3:
        return 'Among top losers'
    elif x > 7:
        return 'Bull run'
    elif x <= -7:
        return 'Bear drop'
    
def trend_pie_chart(df):
    pie_label = sorted([i for i in calculated_df(df).loc[:, 'Trend'].unique()])
    plt.pie(calculated_df(df)['Trend'].value_counts(), labels = pie_label, autopct = '%1.1f%%', radius = 1)
    plt.show()



def generate_buy_sell_signals(condition_buy, condition_sell, dataframe, strategy):
    last_signal = None
    indicators = []
    buy = []
    sell = []
    for i in range(0, len(dataframe)):
        # if buy condition is true and last signal was not Buy
        if condition_buy(i, dataframe) and last_signal != 'Buy':
            last_signal = 'Buy'
            indicators.append(last_signal)
            buy.append(dataframe['Close'].iloc[i])
            sell.append(np.nan)
        # if sell condition is true and last signal was Buy
        elif condition_sell(i, dataframe)  and last_signal == 'Buy':
            last_signal = 'Sell'
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(dataframe['Close'].iloc[i])
        else:
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(np.nan)

    dataframe[f"{strategy}_Last_Signal"] = np.array(last_signal)
    dataframe[f"{strategy}_Indicator"] = np.array(indicators)
    dataframe[f"{strategy}_Buy"] = np.array(buy)
    dataframe[f"{strategy}_Sell"] = np.array(sell)




def sma_plot(df):
        # create 50 days simple moving average column
    df['50_SMA'] = df['Close'].rolling(window = 50, min_periods = 1).mean()
    # create 200 days simple moving average column
    df['200_SMA'] = df['Close'].rolling(window = 200, min_periods = 1).mean()
    # display first few rows
    df['Signal'] = 0.0
    df['Signal'] = np.where(df['50_SMA'] > df['200_SMA'], 1.0, 0.0)
    df['Position'] = df['Signal'].diff()
    # plot close price, short-term and long-term moving averages 
    df['Close'].plot(color = 'k', label= 'Close Price') 
    df['50_SMA'].plot(color = 'b',label = '50-day SMA') 
    df['200_SMA'].plot(color = 'g', label = '200-day SMA')
    # plot 'buy' signals
    plt.plot(df[df['Position'] == 1].index, df['50_SMA'][df['Position'] == 1], '^', markersize = 15, color = 'g', label = 'buy')
    # plot 'sell' signals
    plt.plot(df[df['Position'] == -1].index, df['200_SMA'][df['Position'] == -1], 'v', markersize = 15, color = 'r', label = 'sell')
    plt.ylabel('Price in Rupees', fontsize = 15 )
    plt.xlabel('Date', fontsize = 15 )
    plt.title('SMA Crossover', fontsize = 20)
    plt.legend()
    plt.show()

def ema_plot(df):
    # Create 50 days exponential moving average column
    df['50_EMA'] = df['Close'].ewm(span = 50, adjust = False).mean()
    # Create 200 days exponential moving average column
    df['200_EMA'] = df['Close'].ewm(span = 200, adjust = False).mean()
    # create a new column 'Signal' such that if 50-day EMA is greater   # than 200-day EMA then set Signal as 1 else 0
    df['Signal'] = 0.0  
    df['Signal'] = np.where(df['50_EMA'] > df['200_EMA'], 1.0, 0.0)
    # create a new column 'Position' which is a day-to-day difference of # the 'Signal' column
    df['Position'] = df['Signal'].diff()
    # plot close price, short-term and long-term moving averages 
    df['Close'].plot(color = 'k', lw = 1, label = 'Close Price')  
    df['50_EMA'].plot(color = 'b', lw = 1, label = '50-day EMA') 
    df['200_EMA'].plot(color = 'g', lw = 1, label = '200-day EMA')
    # plot 'buy' and 'sell' signals
    plt.plot(df[df['Position'] == 1].index, df['50_EMA'][df['Position'] == 1], '^', markersize = 15, color = 'g', label = 'buy')
    plt.plot(df[df['Position'] == -1].index, df['200_EMA'][df['Position'] == -1], 'v', markersize = 15, color = 'r', label = 'sell')
    plt.ylabel('Price in Rupees', fontsize = 15 )
    plt.xlabel('Date', fontsize = 15 )
    plt.title('EMA Crossover', fontsize = 20)
    plt.legend()
    plt.show()

