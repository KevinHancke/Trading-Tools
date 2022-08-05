#!/usr/bin/env python
# coding: utf-8

# In[2]:


#taken from Algovibes at https://www.youtube.com/watch?v=FpSopSupizo
import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# In[4]:


class SMAcross(Strategy):
    n1 = 50
    n2 = 100
    
    def init(self):
        close = self.data.Close
        self.sma1 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n1)
        self.sma2 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n2)
    
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


# In[5]:


df = yf.download('BTC-USD', start='2018-01-01')


# In[16]:


bt = Backtest(df, SMAcross, cash=10000, commission=0.002,
             exclusive_orders=True)


# In[17]:


output=bt.run()


# In[18]:


output


# In[13]:


#Plot your strategy visually
bt.plot()


# In[19]:


optim = bt.optimize(n1 = range(50,150,10), 
                   n2 = range(50,150,10),
                   constraint = lambda x: x.n2 - x.n1 >20,
                   maximize= 'Return [%]')
bt.plot()


# In[ ]:





# In[ ]:





# In[ ]:




