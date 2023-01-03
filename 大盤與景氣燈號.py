# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:54:53 2023

@author: Wistronits
"""

import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_datareader import data
# 需要用此套建載入yahoo的API，否則無法取得資訊
import yfinance as yf
yf.pdr_override()

#--- 抓取大盤的股價變動
# 先設定要爬的時間
start = datetime.datetime.strptime('20010101',"%Y%m%d")
end = datetime.datetime.strptime('20221231',"%Y%m%d")
# 取得全台灣所有的股票，每天的交易資訊
df_stock = data.get_data_yahoo('^TWII', start, end)
# 整理出日期欄位，計算指數的月平均線
df_stock['日期'] = df_stock.index
df_stock['年月'] = df_stock['日期'].dt.strftime('%Y-%m')
M_index = df_stock[['年月','Close']].groupby('年月').mean()
M_index['日期'] =  pd.to_datetime(M_index.index)
#--- 引入國家景氣燈號資料
monitoring_indicator = pd.read_excel('精氣燈號.xls')
monitoring_indicator.columns = ['日期','景氣對策信號(燈號)','景氣對策信號(分)']
monitoring_indicator['日期'] = pd.to_datetime(monitoring_indicator['日期'])
#--- 開始繪製「大盤與景氣燈號關係曲線」
fig, ax1 = plt.subplots()
plt.title('大盤與景氣燈號關係曲線')
plt.xlabel('日期')
ax2 = ax1.twinx()

ax1.set_ylabel('台灣指數', color='#5d82bb')
ax1.plot( 
    M_index['日期'], 
    M_index['Close'], 
    color='#5d82bb', 
    alpha=0.5)
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2.set_ylabel('景氣燈號', color='#bb965d')
ax2.plot( 
    monitoring_indicator['日期'], 
    monitoring_indicator['景氣對策信號(分)'], 
    color='#bb965d', 
    alpha=0.5)
ax2.tick_params(axis='y', labelcolor='black')


fig.tight_layout()
plt.show()
