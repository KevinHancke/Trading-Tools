#!/usr/bin/env python
# coding: utf-8

# In[3]:


import unicorn_binance_websocket_api
import pandas as pd


# In[4]:


ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")


# In[5]:


ubwa.create_stream(['kline_1m'], 'BTCUSDT', output='UnicornFy')


# In[6]:


buyprice = 18940
max_price = buyprice
TP = buyprice *1.001


# In[7]:


while True:
    data = ubwa.pop_stream_data_from_stream_buffer()
    if data and len(data) > 3:
        liveprice = float(data['kline']['close_price'])
        print('current liveprice: ' +str(liveprice))
        if liveprice > max_price:
            max_price = liveprice
            if max_price >= TP:
                dev_line = max_price *0.99
            try:
                print('current dev_line: ' +str(dev_line))
                if liveprice < dev_line:
                    print('Sell!')
                    break
            except:
                print('No dev_line yet')
            print('current max price: ' +str(max_price))
            print('target profit:' +str(TP))
            print('--------------------')


# In[ ]:




