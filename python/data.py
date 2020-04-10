
import pandas as pd
import pandas_datareader as web
import datetime



class Data():
    
    def __init__(self, symbol, from_str, to_str, variable):
        self.symbol = symbol
        self.from_str = from_str
        self.to_str = to_str
        self.variable = variable
        

    @staticmethod
    def parse_dates(from_str, to_str):
        from_dt = datetime.datetime.strptime(from_str, '%Y-%m-%d')
        if len(to_str) > 1:
            to_dt = datetime.datetime.strptime(to_str, '%Y-%m-%d')
        else:
            to_dt = datetime.datetime.now()
        return from_dt, to_dt
    

    @staticmethod
    def query_yahoo(symbol, from_dt, to_dt, variable):
        dtf = web.DataReader(name=symbol, data_source="yahoo", 
                             start=from_dt, end=to_dt, 
                             retry_count=10)
        return dtf[variable]
    
    
    def get_data(self):
        #rolling_mean = self.ts.rolling(window=window).mean()
        #rolling_std = self.ts.rolling(window=window).std()
        from_dt, to_dt = parse_dates(self.from_str, self.to_str)
        self.ts = query_yahoo(self.symbol, from_dt, to_dt, self.variable)
