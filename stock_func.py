from pandas_datareader import data as pdr
import datetime
import yfinance as yf 
import numpy as np
import pandas as pd

class DaySeries:
    
    def __init__(self, ticker, start, end):
        
        self.ticker = ticker
        self.start = start
        self.end = end
        """
        start = "2023-1-1" #@param {type:"string"}
        end = datetime.date.today()
        ticker = "AAPL" #@param [""] {allow-input: true}
        """
        # データ取得をdrからyfinanceへ変更。2021.7.4
        yf.pdr_override() # <== that's all it takes :-)
        # download dataframe
        self.df = pdr.get_data_yahoo(ticker, start, end)
    
    """
    def df(self):
        df = self.df
        return df
    """
    
    def open_mean(self):
        mean = self.df["Open"].mean()
        return mean
    
    def close_mean(self):
        mean = self.df["Close"].mean()
        return mean
    
    def adj_colse_mean(self):
        mean = self.df["Adj Close"].mean()
        return mean
    
    def high_mean(self):
        mean = self.df["High"].mean()
        return mean
    
    def low_mean(self):
        mean = self.df["Low"].mean()
        return mean
    
    def volume_mean(self):
        mean = self.df["Volume"].mean()
        return mean
    
    def close_std(self):
        std = self.df["Close"].std()
        return std
    
    def adj_close_std(self):
        std = self.df["Adj Close"].std()
        return std
    
    def high_std(self):
        std = self.df["High"].std()
        return std
    
    def low_std(self):
        std = self.df["Low"].std()
        return std
    
    def close_std(self):
        std = self.df["close"].std()
        return std
    
    def plot(self, md=10):
        from matplotlib import pyplot as plt
        
        df = self.df
        
        price = df['Adj Close']
        date = df.index
        
        df[str(md)+'mean'] = price.rolling(window=int(md)).mean()
        
        plt.figure(figsize=(30, 15))
        plt.subplot(3,1,1)

        plt.title(self.ticker, fontsize=18)
        plt.ylabel('Price', fontsize=18)

        plt.plot(date, price, label='Adj Close', color='#99b898')
        plt.plot(date, df[str(md)+'mean'], label=str(md)+'days mean', color='#e84a5f')
        plt.legend(fontsize=18)

        plt.subplot(3,1,2)
        plt.ylabel('Volume', fontsize=18)
        plt.bar(date, df['Volume'], label='Volume', color='gray')
        plt.legend(fontsize=18)
    
        plt.subplot(3,1,3)
        plt.plot(date, price, label='Adj Close', color='r')
        plt.plot(date, df['High'], label='High', color='b')
        plt.plot(date, df['Low'], label='Low', color='b')
        plt.ylabel('Price', fontsize=18)
        plt.xlabel('Date', fontsize=18)
        plt.legend(fontsize=18)
        plt.plot()
        plt.show()
        
    def cross_point(self, md=10):
        df = self.df
        
        if len(df) < md + 1:
            print("The length of data is required more than " + str(md + 1) + ".")
            return
        
        else:
            price = df['Adj Close']
            date = df.index
            means = price.rolling(window=int(md)).mean()
            up = []
            down = []
            for i in range(md, len(means)-1):
                
                if price[i] <= means[i] and price[i+1] > means[i+1]:
                    up.append(i)
                elif price[i] >= means[i] and price[i+1] < means[i+1]:
                    down.append(i)
           
            return (up, down, md)
    
    def peak_rate(self, md=10, key="Adj Close"):
        up, down, md = self.cross_point(md)
        df = self.df
        up_rates = []
        durations = []
        cross = []
        peak = []
        if up[0] > down[0]:   
            for i in range(len(up)):
                
                date = df.index[up[i]:down[i+1]]
                ac = df[key][up[i]:down[i+1]]
                pre = ac[0]
                max_value = ac.max()
                idxmax = ac.idxmax()

                up_rate = 100 * (max_value - pre) / pre
                duration = idxmax - date[0]
                up_rates.append(up_rate)
                durations.append(duration)
                cross.append(date[0])
                peak.append(idxmax)
                    
        else:
            for i in range(len(up)):
                date = df.index[up[i]:down[i]]
                ac = df[key][up[i]:down[i]]
                pre = ac[0]
                max_value = ac.max()
                idxmax = ac.idxmax()

                up_rate = 100 * (max_value - pre) / pre
                duration = idxmax - date[0]
                up_rates.append(up_rate)
                durations.append(duration)
                cross.append(date[0])
                peak.append(idxmax)
                
        df2 = pd.DataFrame({
            "up_rate": up_rates,
            "cross_date": cross,
            "peak_date": peak,
            "duration": durations})
        
        return (df2, md)
   
    def peak_rate_down(self, md=10, key="Adj Close"):
            up, down, md = self.cross_point(md)
            df = self.df
            down_rates = []
            durations = []
            cross = []
            peak = []
            if up[0] > down[0]:   
                for i in range(len(down)):

                    date = df.index[down[i]:up[i+1]]
                    ac = df[key][down[i]:up[i+1]]
                    pre = ac[0]
                    min_value = ac.min()
                    idxmax = ac.idxmin()

                    down_rate = 100 * (pre - min_value) / pre
                    duration = idxmin - date[0]
                    down_rates.append(down_rate)
                    durations.append(duration)
                    cross.append(date[0])
                    peak.append(idxmax)

            else:
                for i in range(len(up)):
                    date = df.index[down[i]:up[i]]
                    ac = df[key][down[i]:up[i]]
                    pre = ac[0]
                    min_value = ac.min()
                    idxmin = ac.idxmin()

                    down_rate = 100 * (min_value - pre) / pre
                    duration = idxmin - date[0]
                    down_rates.append(down_rate)
                    durations.append(duration)
                    cross.append(date[0])
                    peak.append(idxmin)

            df2 = pd.DataFrame({
                "down_rate": down_rates,
                "cross_date": cross,
                "peak_date": peak,
                "duration": durations})

            return (df2, md)
    
    def floor_dif(self, df=None, key=None):
        if df is None:
            df = self.df
        if key is None:
            key = "Adj Close"
        x = df[key]
        array = []
        for i in range(1, len(x)):
            array.append(x[i]-x[i-1])
        df2 = pd.DataFrame({"floor_dif": array}, index=df.index[1:])
        return df2
    
    def ndim_floor_dif(self, n, df=None, key=None):
        if df is None:
            df = self.df
        if key is None:
            key = "Adj Close"
        x = df[key]
        
        if type(n) is not int:
            print('The type of "n" must be int.')
            return
        elif len(df) < n + 1:
            print('The length of array is smaller than or equal to n')
            return
        else:
            df2 = self.floor_dif(df=df, key=key)
            for i in range(n-1):
                df2 = self.floor_dif(df=df2, key=df2.columns[0])
            return df2
