#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unicorn_binance_websocket_api
import pandas as pd
import numpy as np


# In[2]:


ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")


# In[3]:


ubwa.create_stream(['kline_1m'], 'BTCUSDT', output='UnicornFy')


# In[4]:


buyprice = 18620
benchmark = buyprice


# In[5]:


while True:
    data = ubwa.pop_stream_data_from_stream_buffer()
    if data and len(data) > 3:
        liveprice = float(data['kline']['close_price'])
        print(liveprice)
        if liveprice > benchmark:
            benchmark = liveprice
        print('current benchmark: ' +str(benchmark))
        TSL = benchmark * 0.98
        if liveprice < TSL:
            print('Sell!')
        print('current trailing stop loss: ' +str(TSL))
        print('--------------------------------------')


# In[ ]:




