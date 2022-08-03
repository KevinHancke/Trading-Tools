#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tradingview_ta import TA_Handler, Interval, Exchange


# In[2]:


output = TA_Handler(
    symbol="BTCUSDT",
    screener="Crypto",
    exchange="Binance",
    interval=Interval.INTERVAL_1_MINUTE,
    # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
)
#print(output.get_analysis().summary)


# In[5]:


output.get_analysis().summary


# In[6]:


output.get_analysis().indicators


# In[7]:


symbols = ['ETHUSDT', 'SOLUSDT', 'DOTUSDT', 'MATICUSDT', 'SUSHIUSDT']


# In[8]:


for symbol in symbols:
    output = TA_Handler(
    symbol=symbol,
    screener="Crypto",
    exchange="Binance",
    interval=Interval.INTERVAL_1_MINUTE)
    print('Symbol: ' +symbol)
    print(output.get_analysis().summary)


# In[ ]:




