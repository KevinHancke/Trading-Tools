#!/usr/bin/env python
# coding: utf-8

# In[241]:


#Inspired and sourced from Algovibes https://www.youtube.com/watch?v=lJlkMXxsuZk
import yfinance as yf
import pandas as pd
import numpy as np
import ta


# In[269]:


df = yf.download('BTC-USD', start='2021-01-01', interval ='1h')


# In[270]:


df['stochrsi_k'] = ta.momentum.stochrsi_k(df.Close)


# In[271]:


df['stochrsi_d'] = ta.momentum.stochrsi_d(df.Close)


# In[272]:


#8, 14, 50 EMA
for i in (5,13,21,55):
    df['EMA_'+str(i)] = ta.trend.ema_indicator(df.Close, window=i)


# In[273]:


df['atr'] = ta.volatility.average_true_range(df.High, df.Low, df.Close)


# In[274]:


df.dropna(inplace=True)


# In[275]:


#Finds the crossover using diff() function 
def checkcross(df):
    series = df['stochrsi_k'] > df['stochrsi_d']
    return series


# In[276]:


df['crossTest1'] = checkcross(df)


# In[277]:


df['crossTest2'] = checkcross(df).diff()


# In[278]:


def crossTrue(df):
    series2 = df['crossTest1'] + df['crossTest2'] >= 2
    return series2


# In[279]:


df['cross'] = crossTrue(df)


# In[280]:


df['TP'] = df.Close + (df.atr*2)


# In[281]:


df['SL'] = df.Close - (df.atr*2)


# In[282]:


#Get the BuySignal from StochCross and Triple EMA above
df['Buysignal'] = np.where((df.cross) & 
                           (df.Close > df.EMA_5) &
                           (df.EMA_5 > df.EMA_13) &
                           (df.EMA_13 > df.EMA_55), 1, 0)


# In[283]:


df.Close.iloc[10]


# In[284]:


selldates = []
outcome = []

for i in range(len(df)):
    if df.Buysignal.iloc[i]:
        k = 1
        SL = df.SL.iloc[0]
        TP = df.TP.iloc[0]
        in_position = True
        while in_position:
            looping_high = df.High.iloc[i+k]
            looping_low = df.Low.iloc[i+k]
            if looping_high >= TP:
                selldates.append(df.iloc[i+k].name)
                outcome.append('TP')
                in_position = False
            elif looping_low <= SL:
                selldates.append(df.iloc[i+k].name)
                outcome.append('SL')
                in_position = False
            k += 1


# In[285]:


df.loc[selldates, 'Sellsignal'] = 1
df.loc[selldates, 'outcome'] = outcome


# In[286]:


df.Sellsignal = df.Sellsignal.fillna(0).astype(int)


# In[287]:


mask = df[(df.Buysignal ==1) | (df.Sellsignal ==1)]


# In[288]:


mask2 = mask[(mask.Buysignal.diff() == 1) | (mask.Sellsignal.diff() == 1)]


# In[289]:


mask2


# In[290]:


mask2.outcome.value_counts()


# In[291]:


mask2.outcome.value_counts().sum()


# In[292]:


419/493


# In[ ]:




