#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime


# In[2]:


df = pd.read_csv("Binance_BTCUSDT_NEW.csv")


# In[3]:


df.columns


# In[4]:


df


# In[5]:


#Slicing and cleaning DF
df = df.iloc[:,:6]
df.columns=['Date','Open', 'High', 'Low', 'Close', 'Volume']
df=df[df['Volume']!=0]
df.reset_index(drop=True, inplace=True)


# In[6]:


#New strat
df['RSI'] = ta.rsi(df.Close, length=10)
df["Shifted_Open"] = df.Open.shift(-1)


# In[7]:


#NEW SIGNALS
df['RSI_Overbought'] = (df.RSI > 80)
df['RSI_Oversold'] = (df.RSI < 20)


# In[8]:


df['Buy_Signal'] = (df.RSI_Oversold) & (df.RSI_Oversold.shift(1) == False)
df['Sell_Signal'] = (df.RSI_Overbought) & (df.RSI_Overbought.shift(1) == False)


# In[9]:


df.head(50)


# In[10]:


df.dropna(inplace=True)


# In[11]:


df


# In[77]:


def strategy(data, sl, tp):
   
   in_position = False
   buydates, selldates = [],[]
   buyprices, sellprices = [],[]

   for index, row in data.iterrows():
       if not in_position and row.Buy_Signal == True:
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
   profits_df = pd.DataFrame(profits)
   print("profit/loss: " + str(round(((profits+1).prod()*100),3)),"%")
   print("number of trades: " + str(len(sellprices)))
   print("culmulative profit/loss: " + str(round((sum(profits)*100),3)),"%")
   print("winrate: " + str(round(((sum(profits_df[0]>0)/len(sellprices))*100))),"%")
   print("---------------------------")
   print(" ")


# In[78]:


strategy(df,0.99,1.03)


# In[79]:


sl_range = 1 - np.arange(0.01,0.06,0.01)
tp_range = 1 + np.arange(0.01,0.06,0.01)


# In[80]:


for sl in sl_range:
    for tp in tp_range:
        print("stop loss: " +str(100-(sl*100)),"%  " "target profit: " + str((tp*100)-100),"%")
        strategy(df, sl, tp)

