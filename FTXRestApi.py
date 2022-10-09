#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import websocket
import json


# In[ ]:


endpoint = 'wss://ftx.com/ws/'


# In[ ]:


our_msg = json.dumps({'op': 'subscribe', 'channel':'ticker', 'market': 'ETH/USD'})


# In[ ]:


def on_open(ws):
    ws.send(our_msg)
def on_message(ws, message):
    out = json.loads(message)
    df_ = pd.DataFrame(out['data'], index=[0])
    df_.index = pd.to_datetime(df_.time, unit='s')
    print(df_['last'])
    
ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_open=on_open)
ws.run_forever()


# In[ ]:


df_ = pd.DataFrame(out['data'], index=[0])
df_.index = pd.to_datetime(df_.time, unit='s')
df_['last']


# In[10]:


base = 'https://ftx.com/api'


# In[11]:


pd.to_datetime('2021-01-01').timestamp()


# In[12]:


r = requests.get(base+'/markets/ETH/USD/candles?resolution=86400&start_time=1609459200.0')


# In[13]:


res_df = pd.DataFrame(r.json()['result'])


# In[14]:


res_df


# In[16]:


import ftx


# In[17]:


client = ftx.FtxClient()


# In[21]:


client.get_historical_data('ETH/USD', 86400, limit=500)


# In[ ]:




