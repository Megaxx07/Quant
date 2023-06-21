
import  pandas_datareader.data as web
import numpy as np
import yfinance as yf
import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
yf.pdr_override()


# import data
def getData(stocks, start, end):
  stockData = web.get_data_yahoo(stocks,start=start,end=end)
  stockData = stockData['Close']
  returns = stockData.pct_change()
  meanReturns = returns.mean()
  # covMatrix = returns.cov()
  return returns, meanReturns

#Portfolio Performance
def portfolioperfomance(meanReturns, Time): #Time for time step to evaluate the VaR time step
  returns = np.sum(meanReturns)*Time
  return returns


stocks = input('Enter a stock code: ')

# define the time span
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days = 800)


returns, meanReturns = getData(stocks, start = startDate, end = endDate)
returns = returns.dropna()


def historicalVaR(returns, alpha = 5):
   """
   Read in a pandas dataframe of returns / a pandas series of returns
   Output the percentile of the distribution st the given alpha confidence level
   """
   if isinstance(returns, pd.Series): # What is isinstance?
     return np.percentile(returns, alpha)

   #A passed user-defined-function will be passed a Series for evaluation
   elif isinstance(returns, pd.DataFrame):
     return returns.aggregate(historicalVaR, alpha=5)

   else:
     raise TypeError("Expected returns to be dataframe or series")

def historicalCVaR(returns, alpha = 5):
   """
   Read in a pandas dataframe of returns / a pandas series of returns
   Output the CVaR fro dataframe / series
   """
   if isinstance(returns, pd.Series):
     belowVaR = returns <= historicalVaR(returns, alpha =alpha)
     return returns[belowVaR].mean()

   #A passed user-defined-function will be passed a Series for evaluation
   elif isinstance(returns, pd.DataFrame):
     return returns.aggregate(historicalCVaR, alpha=5) #Aggregate funtion?

   else:
     raise TypeError("Expected returns to be dataframe or series")


Time = int(input('Enter a time period: '))
InitialInvestment = int(input("Enter your capital: "))


VaR = -historicalVaR(returns, alpha=5)*np.sqrt(Time)
CVaR = -historicalCVaR(returns, alpha=5)*np.sqrt(Time)
pRet = portfolioperfomance(meanReturns, Time)


print('Expected Return:       ', round(InitialInvestment*pRet, 2))
print('Value at Risk 95th CI:       ', round(InitialInvestment*VaR, 2))
print('Conditional VaR 95th CI:       ', round(InitialInvestment*CVaR, 2))
