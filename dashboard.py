#Using streamlit to stream a finance dashboard of relative returns of different assets from any given point in time
#Taken and inspired from Algovibes @ https://www.youtube.com/watch?v=Km2KDo6tFpQ

import streamlit as st
import yfinance as yf
import pandas as pd

st.title('Lit Finance Dashboard')

tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD')

dropdown = st.multiselect('Pick your assets', tickers)

start = st.date_input('Start', value = pd.to_datetime('2022-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))

def relativeret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

if len(dropdown) > 0:
    #df = yf.download(dropdown, start, end)['Adj Close']
    df = relativeret(yf.download(dropdown, start, end)['Adj Close'])
    st.head['Returns of {}'.format(dropdown)]
    st.line_chart(df)