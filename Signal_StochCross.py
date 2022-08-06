#!/usr/bin/env python
# coding: utf-8

# In[62]:


#Inspired and sourced from Algovibes https://www.youtube.com/watch?v=lJlkMXxsuZk
import yfinance as yf
import pandas as pd
import numpy as np
import ta


# In[63]:


df = yf.download('BTC-USD', start='2021-01-01', interval ='1h')


# In[64]:


df['stochrsi_k'] = ta.momentum.stochrsi_k(df.Close)


# In[65]:


df['stochrsi_d'] = ta.momentum.stochrsi_d(df.Close)


# In[66]:


#8, 14, 50 EMA
for i in (5,13,21,55):
    df['EMA_'+str(i)] = ta.trend.ema_indicator(df.Close, window=i)


# In[67]:


df['atr'] = ta.volatility.average_true_range(df.High, df.Low, df.Close)


# In[68]:


#df.dropna(inplace=True)


# In[74]:


#Finds the crossover using diff() function 
def checkcross(df):
    series = df['stochrsi_k'] > df['stochrsi_d']
    return series


# In[96]:


df['crossTest1'] = checkcross(df)


# In[97]:


df['crossTest2'] = checkcross(df).diff()


# In[98]:


def crossTrue(df):
    series2 = df['crossTest1'] + df['crossTest2'] >= 2
    return series2


# In[99]:


df['cross'] = crossTrue(df)


# In[100]:


df.head(50)


# In[ ]:




