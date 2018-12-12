# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 18:27:12 2018

@author: FISH LIN
"""

import pandas_datareader.data as web
import datetime
#import matplotlib.pyplot as plt


"""
下面是...各項平均值 和 股價與20週均線的走勢圖
"""

#start=datetime.datetime(2017,12,1)
end=datetime.date.today()
passyear=datetime.timedelta(days=365*3)
#passyear=datetime.timedelta(days=365*5)
start=end-passyear

company=["1477.TW"]
#company=["1477.TW","1303.TW"]
stockfind=web.DataReader(company,"yahoo",start,end)

print(round(stockfind.mean(),2))

stockfind["100d"]=round(stockfind["Adj Close"].rolling(window=100).mean(),2)
stockfind.dropna(inplace=True)

print(stockfind["Adj Close"].plot(color="black"))
print(stockfind["100d"].plot(color="orange",legend="100d"))


"""
下面是...近半年的成交量圖
"""

end=datetime.date.today()
passyear=datetime.timedelta(days=365/2)
start=end-passyear

company=["1477.TW"]
stockfind=web.DataReader(company,"yahoo",start,end)

print(stockfind["Volume"].plot())
#print(stockfind["Volume"].hist())

