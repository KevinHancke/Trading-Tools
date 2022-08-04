#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta


# In[2]:


handler = TA_Handler(
    symbol="BTCUSDT",
    exchange="Binance",
    screener="Crypto",
    interval="1h",
    timeout=None
)


# In[3]:


#handler.get_analysis().summary
#handler.get_analysis().summary
#handler.get_analysis().summary
handler.get_analysis().indicators["close"]
handler.get_analysis().indicators["open"]
handler.get_analysis().indicators["high"]
handler.get_analysis().indicators["low"]


# In[14]:


#Get OHLC for current bar
print(handler.exchange +" "+ handler.symbol +" "+ handler.interval)
print("Open: "+ str(handler.get_analysis().indicators["open"]))
print("High: "+ str(handler.get_analysis().indicators["high"]))
print("Low: "+ str(handler.get_analysis().indicators["low"]))
print("Close: "+ str(handler.get_analysis().indicators["close"]))

