import yfinance as yf
import pandas as pd
import requests as req
import os
import sqlite3 as sq
from io import StringIO

# Initialize the stock database
def stocks_update():

        # TODO: Pull the stock data from the database daily
        # Link to iShares Russell 2000 ETF CSV, seeks to track the investment results of an index composed of small-capitalization U.S. equities.
        url = "https://www.ishares.com/us/products/239710/ishares-russell-2000-etf/1467271812596.ajax?fileType=csv&fileName=IWM_holdings&dataType=fund"

        data = req.get(url).content # Get the data from the url
        result = str(data, 'utf-8') # Convert the data to a string
        data = StringIO(result)     # Convert the string to a StringIO object

        df = pd.DataFrame(data)     # Convert the StringIO object to a DataFrame
        df = df[0][9:]              # Remove the first 9 rows
        df = df.to_frame()          # Convert the series to a DataFrame
        df2 = df[0].str.split('","', expand=True).copy() 
        df2.columns = df[0][9].split(",") 
        df2 = df2.dropna(axis=0, subset = ['Market Value'], how = "any") # Drop rows with NaN values in the Market Value column
        df2["Ticker"] = df2["Ticker"].str.replace('"','')                # Remove the " from the Ticker column
        tickers = df2["Ticker"].tolist()                                 # Convert the Ticker column to a list

        # Get the stock data from Yahoo Finance, comments are from the yfinance documentation
        data = yf.download(  
                
                tickers = tickers, # list of tickers

                # use "period" instead of start/end
                # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                # (optional, default is '1mo')
                period = "5y",

                # fetch data by interval (including intraday if period < 60 days)
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                # (optional, default is '1d')
                interval = "1d",

                # group by ticker (to access via data['SPY'])
                # (optional, default is 'column')
                group_by = 'column',

                # adjust all OHLC automatically
                # (optional, default is False)
                auto_adjust = True,

                # download pre/post regular market hours data
                # (optional, default is False)
                prepost = True,

                # use threads for mass downloading? (True/False/Integer)
                # (optional, default is True)
                threads = True,

                # proxy URL scheme use use when downloading?
                # (optional, default is None)
                proxy = None
            )

        # Data is in a wide format, need to convert to long format to store in the MySQL database

        data2 = data.unstack(level=-1) # Unstack the data
        data2 = data2.reset_index()    # Reset the index
        data2 = data2.pivot(index = ["level_1","Date"], columns = ["level_0"], values = 0) # Pivot the data
        data2 = data2.reset_index()   # Reset the index
        data2 = data2.rename(columns = {"level_1": "Ticker"}) # Rename the level_1 column to Ticker


        db = "database"               # Database name
        table_name = "stock_database" # Table name for the stock data
        conn = sq.connect('{}.sqlite'.format(db)) # Connect to the database
        data2.to_sql(table_name, conn, if_exists='replace', index=False) # Write the stock data to the database
        df2.to_sql("stock_infos",conn, if_exists='replace', index=False) # Write the stock infos to the database

        conn.close() # Close the connection

if __name__ == '__main__':
        stocks_update() # Run the stocks_update function