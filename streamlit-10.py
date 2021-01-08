import pandas as pd
from backtesting import Strategy
from backtesting import Backtest
import yfinance as yf
import streamlit as st

st.write("""
    Historical data of American Stocks
    """)
st.write("for Tesla Stock")
tsla = yf.Ticker("TSLA")
data2=pd.DataFrame(tsla.history(period='max'))
df=pd.DataFrame(data2,columns =['Open','High', 'Low','Close'])

df.index = pd.to_datetime(df.index)


def TurtleHigh(values, n):    
    return pd.Series(values).rolling(n).max(skipna=True)
def TurtleLow(values,n):    
    return pd.Series(values).rolling(n).min(skipna=True)

class Turtle(Strategy):
    n1 = st.slider("Select a High Number:")
    n2 = st.slider("Select a Low Number:")
    
    def init(self):
        self.High = self.I(TurtleHigh, self.data.High,self.n1)
        self.Low = self.I(TurtleLow,self.data.Low,self.n2)
        
    def next(self):
        
        if (self.data.High[-1] > self.High[-2] and self.data.High[-2] < self.High[-3] and not self.position):
            self.buy()
            
            
        elif (self.data.Low[-1] < self.Low[-2] and self.data.Low[-2] > self.Low[-3] and self.position):
            self.position.close()
            
            


bt = Backtest(df,Turtle,cash=10000,commission=.0015, exclusive_orders=True)

st.write(""" results of strategy
    """)
stats = bt.run()
st.write(stats)
st.table(stats['_trades'])
st.write(bt.plot())

st.write(""" Optimization Results
""")
stats = bt.optimize(n1=range(20,70,5),
                    n2=range(10,50,5),
                    maximize='Max. Drawdown [%]',
                    constraint = lambda param: param.n1 > param.n2)

st.write(stats)
st.write(stats._strategy)
st.table(stats['_trades'])
st.write(bt.plot())
