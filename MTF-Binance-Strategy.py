#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance import Client
client = Client()


# In[2]:


def getdata (symbol, interval, start):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, start))
    frame = frame[[0,1,2,3,4,5,8]]
    frame.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume','Number of trades']
    frame.Date = pd.to_datetime(frame.Date, unit='ms')
    frame.set_index('Date', inplace=True)
    frame = frame.astype(float)
    return frame


# In[11]:


daily = getdata('ETHUSDT', '1d', '2022-01-01')


# In[12]:


hourly = getdata('ETHUSDT', '1h', '2022-01-01')


# In[19]:


def calc_MA(df):
    df['SMA_50'] = df.Close.rolling(50).mean()


# In[20]:


calc_MA(daily)
calc_MA(hourly)


# In[24]:


daily['Buy'] = daily.Close > daily.SMA_50
daily['Sell'] = daily.Close < daily.SMA_50
hourly['Buy'] = hourly.Close > hourly.SMA_50
hourly['Sell'] = hourly.Close < hourly.SMA_50


# In[26]:


daily.Buy = daily.Buy.shift().fillna(False)
daily.Sell = daily.Sell.shift().fillna(False)
hourly.Buy = hourly.Buy.shift().fillna(False)
hourly.Sell = hourly.Sell.shift().fillna(False)


# In[28]:


position = False
buydates, selldates = [],[]

for index_daily, row_daily in daily.iterrows():
    if not position and row_daily['Buy']:
        for index_hourly, row_hourly in hourly[index_daily:][1:25].iterrows():
            if not position and row_hourly['Buy']:
                position = True
                buydates.append(index_hourly)
    if position and row_daily['Sell']:
        for index_hourly, row_hourly in hourly[index_daily:][1:25].iterrows():
            if position and row_hourly['Sell']:
                position = False
                selldates.append(index_hourly)
    


# In[39]:


buydates


# In[30]:


selldates


# In[36]:


plt.figure(figsize=(30,15))
plt.plot(hourly.Close)
plt.scatter(hourly.loc[buydates].index,hourly.loc[buydates].Close, marker="^", c="g", s=200)
plt.scatter(hourly.loc[selldates].index,hourly.loc[selldates].Close, marker="v", c="r", s=200)


# In[40]:


buy_arr = hourly.loc[buydates].Open
sell_arr = hourly.loc[selldates].Open


# In[41]:


buy_arr = buy_arr[:len(sell_arr)]


# In[42]:


buy_arr


# In[43]:


sell_arr


# In[44]:


profit = (sell_arr.values - buy_arr.values)/buy_arr.values


# In[45]:


profit


# In[46]:


profit.mean()


# In[47]:


(profit +1).prod()-1


# In[ ]:




