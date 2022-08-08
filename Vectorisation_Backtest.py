#!/usr/bin/env python
# coding: utf-8

# In[374]:


# Taken from and inspired by AlgoVibes @ https://www.youtube.com/watch?v=nAfnAuvRpqE
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import matplotlib.pyplot as plt


# In[375]:


def indicators(df):
    df['SMA_200'] = ta.trend.sma_indicator(df.Close, window=200)
    df['stoch'] = ta.momentum.stoch(df.High,df.Low,df.Close, window=10)
    df.dropna(inplace=True)


# In[376]:


df = yf.download('TSLA', start='2020-01-01')


# In[377]:


df['Buy'] = (df.Close > df.SMA_200) & (df.stoch < 20)


# In[378]:


df['buyprice'] = np.where(df.Buy, df.Close * 0.97, np.nan)


# In[379]:


df.buyprice = df.buyprice.ffill()


# In[380]:


df['sellprice'] = df.Open.shift(-1)


# In[381]:


for i in range (1,11):
    df['shifted_Low_'+str(i)] = df.Low.shift(-i)
    df['shifted_Close_'+str(i)] = df.Close.shift(-i)
colnames_low = ['shifted_Low_'+str(i) for i in range(1,11)]
colnames_close = ['shifted_Close_'+str(i) for i in range(1,11)]


# In[382]:


raw_signals = df[df.Buy]


# In[383]:


checkbuys = raw_signals[colnames_low].le(raw_signals.buyprice, axis=0)


# In[384]:


checkbuys_sum = checkbuys.cumsum(axis=1) == 1


# In[385]:


filter_buys = checkbuys.astype(int)[checkbuys_sum]


# In[386]:


raw_trades = filter_buys.T.idxmax()


# In[387]:


extract_buys_raw = raw_trades.str.split('_').str[-1]


# In[388]:


extract_buys = extract_buys_raw.fillna(10)


# In[389]:


buydates = [df.loc[i:].index[int(e)] for i,e in zip(extract_buys.index,extract_buys.values)]


# In[390]:


buy_df = df.loc[buydates]


# In[391]:


df_ = pd.DataFrame(extract_buys_raw, columns = ['NaN-check'])


# In[392]:


df_['buydates'] = buydates


# In[393]:


df_


# In[394]:


checksells = buy_df[colnames_close].gt(buy_df.buyprice, axis=0)


# In[395]:


checksells[colnames_close[-1]] = True


# In[396]:


checksells_sum = checksells.cumsum(axis=1) == 1


# In[397]:


filter_sells = checksells.astype(int)[checksells_sum]


# In[398]:


raw_sells = filter_sells.T.idxmax()


# In[399]:


extract_sells = raw_sells.str.split('_').str[-1].astype(int)


# In[400]:


selldates = [df.loc[i:].index[e] for i,e in zip(extract_sells.index, extract_sells.values)]


# In[401]:


df_['selldates'] = selldates


# In[402]:


df_.loc[df_['NaN-check'].isna(), 'selldates'] = df_.loc[df_['NaN-check'].isna()].buydates


# In[403]:


trades_ = df_[df_.index > df_.selldates.shift(1)]


# In[404]:


real_trades = df_[:1].append(trades_)


# In[405]:


real_trades_executed = real_trades.dropna()


# In[406]:


real_trades_executed


# In[407]:


buys = df.loc[real_trades_executed.buydates].buyprice
sells = df.loc[real_trades_executed.selldates].sellprice


# In[408]:


profit = (sells.values - buys.values) / buys.values


# In[409]:


profit


# In[410]:


(profit + 1).cumprod()


# In[411]:


plt.plot(df.Low)
plt.plot(df.SMA_200)
plt.scatter(buys.index, buys.values, marker='^', c='g')
plt.scatter(sells.index, sells.values, marker='v', c='r')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




