#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd


# In[3]:


r = requests.get('https://ftx.com/api/markets')


# In[6]:


df = pd.DataFrame(r.json()['result'])


# In[8]:


df.index = df.name


# In[14]:


spot_df = df[df.type == 'spot']


# In[17]:


spot_df = spot_df[spot_df.tokenizedEquity.isna()]


# In[19]:


spot_df = spot_df[spot_df.isEtfMarket == False]


# In[21]:


spot_df = spot_df[spot_df.quoteCurrency == 'USD']


# In[25]:


spot_df.change24h.sort_values(ascending=False)


# In[29]:


spot_df.change1h.sort_values(ascending=True).head(10).plot(kind='bar')


# In[ ]:


#TASK to complete:
#what are the realtime movements?
# a set of cryptos variable caps
#compare in realtime which one of them is moving the fastest
# you should create a websocket stream of multiple coins and --> keep track of their performance

