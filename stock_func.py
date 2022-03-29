import os
import pandas_datareader as data
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date as dt
from dateutil.relativedelta import relativedelta as rdelta
import argparse
#%matplotlib inline
# pd.core.common.is_list_like = pd.api.types.is_list_like

'''
def parse_args():
    
    parser = argparse.ArgumentParser(description='Plot or analyze stock price')
    parser.add_argument('--name', default='N225', help='name of brand, and it is used as path too.', type=str)
    parser.add_argument('--site', default='yahoo', help='Web scraping (Where the data comes from)', type=str)
    parser.add_argument('--code', default='^N225', help='code of the brand')
    parser.add_argument('--te',default=dt.today().isoformat(), help='End date', type=str)
    parser.add_argument('--ts', default=(dt.today()+rdelta(months=-1)).isoformat(), help='Start date', type=str)
    parser.add_argument('--showfig', default=False, help='Whether figures are shown or not(default=False).', type=bool)
    parser.add_argument('--savefig', default=True, help='Whether figures are saved or not(default=True).', type=bool)
    parser.add_argument('--path', default='pictures', help='path where figures save')
    parser.add_argument('--md', default=10, help='How many days are averaged', type=int)
    
    return parser.parse_args()
'''

class Stock:
    
    name = input("name of brand: ")
    #name of brand, and it is used as path too.
    if name == "":
        name = "N225"

    site = input("Web site: ")
    #Web scraping (Where the data comes from)
    if site == "":
        site = "yahoo"
    
    code = input("code: ")
    #code of the brand
    if code == "":
        code = "^N225"
    
    ts = input("Start date: ")
    #default is a month ago from today.
    if ts == "":
        ts = (dt.today()+rdelta(months=-1)).isoformat()
        
    te = input("End date: ")
    #default is today.
    if te == "":
        te = dt.today().isoformat()
        
    savefig = input("If save figures or not, T or F. (default=F): ")
    if savefig == "T":
        savefig = True
    else:
        savefig = False
        
    showfig = input("If show figures or not, T or F. (default=T): ")
    if showfig == "F":
        showfig = False
    else:
        showfig = True
        
    path = "pictures"
        
    df = data.DataReader(code, site, ts, te)
    #scriping data
    
    def graph(self):
        
        df = self.df
        
        md = input("Mean days (int, default=10): ")
        #How many days are averaged.
        if md == "":
            md = 10
        price = df['Adj Close']
        date = df.index
        price = price
        date = date
        
        df[str(md)+'mean'] = price.rolling(window=int(md)).mean()
        
        plt.figure(figsize=(30, 15))
        plt.subplot(3,1,1)

        plt.title(self.name, fontsize=18)
        plt.xlabel('date', fontsize=18)
        plt.ylabel('price', fontsize=18)

        plt.plot(date, price, label='Adj Close', color='#99b898')
        plt.plot(date, df[str(md)+'mean'], label=str(md)+'day mean', color='#e84a5f')
        plt.legend(fontsize=18)

        plt.subplot(3,1,2)
        plt.bar(date, df['Volume'], label='Volume', color='gray')
        plt.legend(fontsize=18)
    
        plt.subplot(3,1,3)
        plt.plot(date, price, label=['Adj Close'], color='r')
        plt.plot(date, df['High'], label='High', color='b')
        plt.plot(date, df['Low'], label='Low', color='b')
        plt.legend(fontsize=18)
        plt.plot()
        if self.savefig == True:
            os.makedirs(self.path + "/" + self.name, exist_ok = True)
            plt.savefig(self.path + '/'  + self.name + "/" + '.png')
        if self.showfig == True:
            plt.show()
    
    def diff(self):
    
        df = self.df
        tren = [0]
        raise_rate = [0]
        widt = []

        date = df.index
    
        for i in range(len(df["Adj Close"])-1):
            x = df["Adj Close"][i+1] - df["Adj Close"][i]
            rate = 100 * x / df["Adj Close"][i+1]
            tren.append(x)
            raise_rate.append(rate)
        
        for i in range(len(df["High"])):
            y = df["High"][i] - df["Low"][i]
            widt.append(y)
                                            
        df["trend"] = tren
        df["width"] = widt
        df["raise rate"] = raise_rate
        
        width_mean = df["width"].mean() 
        width_max = df["width"].max()
        width_min = df["width"].min()
        
        trend_mean = df["trend"].mean()
        trend_max = df["trend"].max()
        trend_min = df["trend"].min()
        
        raise_rate_mean = df["raise rate"].mean()
        raise_rate_max = df["raise rate"].max()
        raise_rate_min = df["raise rate"].min()
            
        plt.figure(figsize=(30,15))
        plt.subplot(2,1,1)
        plt.bar(date, df["raise rate"], label='raise rate comparing with each previous day [%]', color='b')
        plt.title("raise rate comparing with each previous day [%]", fontsize=18)
        plt.xlabel("date", fontsize=18)
        plt.ylabel("[%]", fontsize=18)
        plt.legend(fontsize=18)
                   
        plt.subplot(2,1,2)
        plt.bar(date, df["width"], 
                label='Daily difference between the highest price and the lowest one [yen]', color='b')
        plt.title("Daily difference between the highest price and the lowest one [yen]")
        plt.xlabel("date", fontsize=18)
        plt.ylabel("[yen]", fontsize=18)
        plt.legend(fontsize=18)
        
        if self.showfig == True:
            plt.show()
        if self.savefig == True:
            plt.savefig(self.path + '/' + self.name + '/' + '-raise_rate' + '.png')
    
def main():
    x = Stock()
    x.graph()
    x.diff()
        
if __name__ == '__main__':
    main()
