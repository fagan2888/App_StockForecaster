
import pandas as pd
import pandas_datareader as web
import datetime
import plotly.express as px



class Data():
    
    def __init__(self, symbol, variable, from_str, to_str):
        self.symbol = symbol
        self.variable = variable
        self.from_str = from_str
        self.to_str = to_str
        

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
        self.from_dt, self.to_dt = self.parse_dates(self.from_str, self.to_str)
        self.ts = self.query_yahoo(self.symbol, self.from_dt, self.to_dt, self.variable)


    def plot_data(self):
        self.to_str = "today" if self.to_str == "" else self.to_str
        fig = px.line(self.ts.reset_index(), x="Date", y=self.variable, 
                      title=self.symbol+" "+self.variable+": from "+self.from_str+ " to "+self.to_str)
        fig.update_xaxes(rangeslider_visible=True)
        return fig