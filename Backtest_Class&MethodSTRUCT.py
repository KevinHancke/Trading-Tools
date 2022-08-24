#!/usr/bin/env python
# coding: utf-8

# In[6]:


#Taken from Algo vibes at https://www.youtube.com/watch?v=yTupVd6D9m8&t=47s
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt


# In[126]:


class Backtest:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.df = yf.download(self.symbol, start='2019-01-01')
        if self.df.empty:
            print('No data pulled')
        else:
            self.calc_indicators()
            self.generate_signals()
            self.loop_it()
            self.profit = self.calc_profit()
            self.max_dd = self.profit.min()
            self.cumul_profit = (self.profit + 1).prod() -1
            
    def calc_indicators(self):
        self.df['ma_20'] = self.df.Close.rolling(20).mean()
        self.df['vol'] = self.df.Close.rolling(20).std()
        self.df['upper_bb'] = self.df.ma_20 + (2*self.df.vol)
        self.df['lower_bb'] = self.df.ma_20 - (2*self.df.vol)
        self.df['rsi'] = ta.momentum.rsi(self.df.Close, window=6)
        self.df.dropna(inplace=True)
    
    def generate_signals(self):
        conditions = [(self.df.rsi < 30) & (self.df.Close < self.df.lower_bb),
             (self.df.rsi > 70) & (self.df.Close>self.df.upper_bb)]
        choices = ['Buy', 'Sell']
        self.df['signal'] = np.select(conditions, choices)
        self.df.signal = self.df.signal.shift()
        self.df.dropna(inplace=True)
        
    def loop_it(self):
        position = False
        buydates, selldates = [], []

        for index, row in self.df.iterrows():
            if not position and row['signal'] == 'Buy':
                position = True
                buydates.append(index)
            if position and row['signal'] == 'Sell':
                position = False
                selldates.append(index)
        self.buy_arr = self.df.loc[buydates].Open
        self.sell_arr = self.df.loc[selldates].Open
    
    def calc_profit(self):
        if self.buy_arr.index[-1] > self.sell_arr.index[-1]:
            self.buy_arr = self.buy_arr[:-1]
        else:
            return (self.sell_arr.values - self.buy_arr.values)/self.buy_arr.values
    
    def plot_chart(self):
        plt.figure(figsize=(20,10))
        plt.plot(self.df.Close)
        plt.scatter(self.buy_arr.index, self.buy_arr.values, marker='^', c='g')
        plt.scatter(self.sell_arr.index, self.sell_arr.values, marker='v', c='r')
        


# In[127]:


instance = Backtest('AAPL')


# In[132]:


instance.profit


# In[ ]:





# In[ ]:




