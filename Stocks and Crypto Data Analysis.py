#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# In[18]:


assets = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'DOT-USD'] #, 'BTC-USD', 'ETH-USD']


# In[19]:


df = yf.download(assets, start='2020-01-01')


# In[20]:


prices = df['Adj Close']


# In[21]:


prices


# In[22]:


returns = prices.pct_change()


# In[23]:


cum_ret = (returns + 1).cumprod() -1


# In[24]:


cum_ret.plot()


# In[25]:


returns.std()


# In[31]:


returns['BTC-USD'].plot()


# In[32]:


returns['BTC-USD'].hist(bins=50)


# In[33]:


fig,ax = plt.subplots(2,2, figsize=(10,5))
counter = 0
for i in range(2):
    for j in range(2):
        #print(returns[returns.columns[counter]])
        ax[i,j].hist(returns[returns.columns[counter]], bins=50)
        ax[i,j].set_title(returns.columns[counter])
        counter +=1
        #print(i,j)


# In[ ]:





# In[34]:


returns.corr()


# In[35]:


import seaborn as sns


# In[36]:


sns.heatmap(returns.corr())


# In[ ]:




