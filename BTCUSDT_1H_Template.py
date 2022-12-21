#!/usr/bin/env python
# coding: utf-8

# In[190]:


import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime


# In[191]:


df = pd.read_csv("Binance_BTCUSDT_NEW.csv")


# In[192]:


df.columns


# In[193]:


df


# In[194]:


#Slicing and cleaning DF
df = df.iloc[:,:6]
df.columns=['Date','Open', 'High', 'Low', 'Close', 'Volume']
df=df[df['Volume']!=0]
df.reset_index(drop=True, inplace=True)


# In[10]:


#Generating Technical Indicators Columns
df["EMA200"] = ta.ema(df.Close, length=200)
df['ATR']= df.ta.atr()
df['RSI'] = ta.rsi(df.Close, length=10)
df['RSI200'] = df['RSI'].ewm(span=200).mean()


# In[11]:


#Generating Signals
df["Shifted_Open"] = df.Open.shift(-1)
df["Shifted_RSI"] = df.RSI.shift(1)
df["Shifted_RSI200"] = df.RSI200.shift(1)
df["Open_Signal"] = (df.Shifted_RSI < df.Shifted_RSI200) & (df.RSI > df.RSI200)


# In[195]:


#New strat
df['RSI'] = ta.rsi(df.Close, length=10)
df['RSI50MA'] = df['RSI'].ewm(span=50).mean()
df["Shifted_Open"] = df.Open.shift(-1)


# In[196]:


#NEW SIGNALS
df['RSI_Crossover'] = (df.RSI > df.RSI50MA)


# In[197]:


df['Buy'] = (df.RSI_Crossover) & (df.RSI_Crossover.shift(1) == False)


# In[198]:


df


# In[199]:


df.dropna(inplace=True)


# In[200]:


df


# In[201]:


def strategy(data, sl, tp):
   
   in_position = False
   buydates, selldates = [],[]
   buyprices, sellprices = [],[]

   for index, row in data.iterrows():
       if not in_position and row.Buy == True:
           buyprice = row.Shifted_Open
           buydates.append(index)
           buyprices.append(buyprice)
           in_position = True
       if in_position:
           if row.Low < buyprice * sl:
               sellprice = buyprice * sl
               sellprices.append(sellprice)
               selldates.append(index)
               in_position = False
           elif row.High > buyprice * tp:
               sellprice = buyprice * tp
               sellprices.append(sellprice)
               selldates.append(index)
               in_position = False
   profits = pd.Series([(sell-buy)/buy for sell, buy in zip(sellprices,buyprices)])
   print((profits + 1).prod())


# In[202]:


strategy(df,0.99,1.03)


# In[203]:


sl_range = 1 - np.arange(0.01,0.06,0.005)
tp_range = 1 + np.arange(0.01,0.06,0.005)


# In[204]:


for sl in sl_range:
    for tp in tp_range:
        print("stop loss: " +str(sl), "target profit: " + str(tp))
        strategy(df, sl, tp)


# In[ ]:




