#!/usr/bin/env python
# coding: utf-8

# In[29]:


#Taken from and inspired by CodeTrading @ https://www.youtube.com/watch?v=NOBV08Im56Y

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta
from backtesting import Strategy
from backtesting import Backtest


# In[15]:


df = yf.download('BTC-USD', start='2022-07-25', interval="15m")


# In[16]:


df["EMA"] = ta.ema(df.Close, length=50)
df["RSI"] = ta.rsi(df.Close, length=3)
a=ta.adx(df.High, df.Low, df.Close, length=5)
df['ADX']=a['ADX_5']
df['ATR']= df.ta.atr()
#help(ta.adx)


# In[17]:


df


# In[18]:


emasignal = [0]*len(df)
backcandles = 8

for row in range(backcandles, len(df)):
    upt = 1
    dnt = 1
    for i in range(row-backcandles, row+1):
        if df.High[i]>=df.EMA[i]:
            dnt=0
        if df.Low[i]<=df.EMA[i]:
            upt=0
    if upt==1 and dnt==1:
        #print("!!!!! check trend loop !!!!")
        emasignal[row]=3
    elif upt==1:
        emasignal[row]=2
    elif dnt==1:
        emasignal[row]=1

df['EMAsignal'] = emasignal


# In[ ]:





# In[19]:


RSIADXSignal = [0] * len(df)
for row in range(0, len(df)):
    RSIADXSignal[row] = 0
    if df.EMAsignal[row]==1 and df.RSI[row]>=80 and df.ADX[row]>=30:
        RSIADXSignal[row]=1
    if df.EMAsignal[row]==2 and df.RSI[row]<=20 and df.ADX[row]>=30:
        RSIADXSignal[row]=2

df['RSIADXSignal']=RSIADXSignal


# In[20]:


#Bearish engulfing Candle defined
CandleSignal = [0] * len(df)
for row in range(1, len(df)):
    CandleSignal[row] = 0
    #if (RSIADXSignal[row]==1 or RSIADXSignal[row-1]==1) and (df.Open[row]>df.Close[row]):# and df.Close[row]<df.Close[row-1]):
    #    CandleSignal[row]=1
    #if (RSIADXSignal[row]==2 or RSIADXSignal[row-1]==2) and (df.Open[row]<df.Close[row]):# and df.Close[row]>df.Close[row-1]):
    #    CandleSignal[row]=2
    if RSIADXSignal[row-1]==1 and df.Open[row]>df.Close[row] and df.Close[row]<min(df.Close[row-1], df.Open[row-1]):
        CandleSignal[row]=1
    if RSIADXSignal[row-1]==2 and df.Open[row]<df.Close[row] and df.Close[row]>max(df.Close[row-1], df.Open[row-1]):
        CandleSignal[row]=2

df['TotSignal']=CandleSignal


# In[21]:


#
def pointpos(x):
    if x['TotSignal']==1:
        return x['High']+1e-4
    elif x['TotSignal']==2:
        return x['Low']-1e-4
    else:
        return np.nan

df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)


# In[22]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

dfpl = df[3000:4000]

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close']),
                go.Scatter(x=dfpl.index, y=dfpl.EMA, line=dict(color='red', width=1), name="EMA")])

fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                marker=dict(size=5, color="MediumPurple"),
                name="Signal")
fig.show()


# In[23]:


df.iloc[3030:3033]


# In[24]:


SLSignal = [0] * len(df)
SLbackcandles = 3
for row in range(SLbackcandles, len(df)):
    mi=1e10
    ma=-1e10
    if df.TotSignal[row]==1:
        for i in range(row-SLbackcandles, row+1):
            ma = max(ma,df.High[i])
        SLSignal[row]=ma
    if df.TotSignal[row]==2:
        for i in range(row-SLbackcandles, row+1):
            mi = min(mi,df.Low[i])
        SLSignal[row]=mi
        
df['SLSignal']=SLSignal


# In[25]:


dfpl = df[:]
def SIGNAL():
    return dfpl.TotSignal


# In[26]:


class MyStrat(Strategy):
    initsize = 0.02
    mysize = initsize
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next()
        slatr = 1.3*self.data.ATR[-1]
        TPSLRatio = 1.3

        if self.signal1==2 and len(self.trades)==0:   
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
        
        elif self.signal1==1 and len(self.trades)==0:         
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr*TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)

bt = Backtest(dfpl, MyStrat, cash=100, margin=1/50, commission=.00)
stat = bt.run()
stat


# In[27]:


bt.plot(show_legend=False)


# In[28]:


dfpl = df[:]
from backtesting import Strategy
from backtesting import Backtest

class MyStrat(Strategy):
    initsize = 0.02
    mysize = initsize
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next()
        TPSLRatio = 1

        if self.signal1==2 and len(self.trades)==0:   
            sl1 = self.data.SLSignal[-1]
            tp1 = self.data.Close[-1]+(self.data.Close[-1] - sl1)*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
        
        elif self.signal1==1 and len(self.trades)==0:         
            sl1 = self.data.SLSignal[-1]
            tp1 = self.data.Close[-1]-(sl1 - self.data.Close[-1])*TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)

bt = Backtest(dfpl, MyStrat, cash=100, margin=1/50, commission=.00)
stat = bt.run()
stat


# In[ ]:




