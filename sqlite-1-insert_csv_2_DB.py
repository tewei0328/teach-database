# %% [markdown]
# ## 1 - Read csv檔至dataframe
# ### (小心檔名不要多一個底線之類的, 會找不到檔案)

# %%
import pandas as pd
#df=pd.read_csv('.\data-202309\TXO202402W3\TXO18700B4_台選02C_60分鐘線.csv', encoding='big5') #小心檔名不要多一個底線之類的, 會找不到檔案
df=pd.read_csv('TXO18700B4_台選02C_60分鐘線.csv', encoding='big5') #小心檔名不要多一個底線之類的, 會找不到檔案

df.head()

# %%
df.tail()

# %%
#df.drop(df.columns[[5,6,7,8,9,10,11,12,13,14,15,16,17]], axis=1)
df.drop(df.columns[8:18], axis=1, inplace=True)
df.drop(df.columns[5:7], axis=1, inplace=True)
#df.drop(df.columns[0], axis=1, inplace=True)
df.head()

# %%
df.rename(
    columns={
        "日期時間": "date",
        "開盤": "open",
        "最高": "high",
        "最低": "low",
        "收盤": "close",
        "成交量": "volume",
    },
    inplace=True,
)

# %%
df.head()

# %%
df.to_csv('txo.csv', index = False)
#df.to_csv('txo.csv', index = False)

# %% [markdown]
# 
# 
# 
# 
# 
# 
# 

# %%
#df=pd.read_csv('.\data-202309\TXF1_1mk_2024_0120_0126.csv')
#df.head()

# %%

df=pd.read_csv('txo.csv') #小心檔名不要多一個底線之類的, 會找不到檔案
df.head()

# %% [markdown]
# ## 2- 資料整理

# %%
# 要先加時間索引, 畫出來的圖才會正確
df.index = pd.to_datetime(df["date"])
df.head()
df.close.plot()

# %%
df3=df
df3.head()

# %% [markdown]
# ### 資料整理2
# 

# %%

df3.drop(
    #columns=["date", "futures_id","contract_date", "spread", "spread_per","settlement_price","open_interest","trading_session"],
    #columns=["Date", "Time"],
    columns=["date"],
    inplace=True,
)


# %%
'''
df3.rename(
    columns={
        #"Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    },
    inplace=True,
)
'''

# %%

df3[['open','close','high','low']].plot(figsize=(10, 7))

# %%
df3.head()

# %% [markdown]
# ## 2-將DataFrame存入資料庫
# 

# %%
#stock_index='TX116700U3_W109P'
stock_index='txf1'
df=df3
df=df.reset_index() #要存入資料庫前要取消時間索引
df.head()

# %% [markdown]
# ### 設定所要存入的資料表名(股票名) 
# #### (要先開啟Mysql Workbench並連線, 否則會出錯)
# 

# %%
"""code=stock_index #'0056'

### 連線資料庫
import pymysql
import sys
#import tushare as ts
import pandas as pd
#import pandas_datareader

try:
    # 開啟資料庫連線
    #db = pymysql.connect("localhost","root","123456","pythonStock" )
    db=pymysql.connect(host="localhost",user="root",password="123456",database="pythonstock" )
except:
    print('Error when Connecting to DB.')   
    sys.exit()
cursor = db.cursor()"""
# https://github.com/tewei0328/teach-database/blob/main/mta_sqlite3_product.ipynb

#code=stock_index #'0056'

### 連線資料庫
import sqlite3
import sys
#import tushare as ts
import pandas as pd
#import pandas_datareader

conn = sqlite3.connect("aaa1.db")
c = conn.cursor()
c.execute("""CREATE TABLE txo(
date text,
open text,
high text,
low text,
close text,
volume text
)""")
conn.commit()


# %% [markdown]
# ### 建新資料表
# 

# %%

# 從網站爬取資料，並插入到對應的資料表中
'''

try:
    createSql= 'CREATE TABLE stock_' +code+' (  date varchar(255) ,open float,close float ,high float , low float,vol int(11))'
    print(createSql)
    cursor.execute(createSql)
except:
    print('Error when Creating table for:' + code)                
db.commit()
'''

# %% [markdown]
# ### 插入新的紀錄 (ver2. 防插入重複資料)

# %%
"""
cnt=0
while cnt<=len(df)-1:
    date=df.iloc[cnt]['date']
    open=df.iloc[cnt]['open']
    close=df.iloc[cnt]['close']
    high=df.iloc[cnt]['high']
    low=df.iloc[cnt]['low']
    vol=df.iloc[cnt]['volume']

    #tableName='stock_'+code
    tableName='option'
    values = [date,float(open),float(close),float(high),float(low),int(vol)]
    insertSql='insert ignore into '+tableName+' (date,open,close,high,low,vol) values (%s,%s,%s,%s,%s,%s)'
    c.execute(insertSql, values)
    cnt=cnt+1

conn.commit()   


### 資料庫離線
c.close()
conn.close()
"""

# %%
#如果資料表存在，就寫入資料，否則建立資料表
df.to_sql('option', conn, if_exists='append', index=False)

# %% [markdown]
# ## 3-讀取資料庫-並存入DataFrame
# 

# %%
#df1 = pd.read_sql("SELECT * FROM option WHERE volume>20000", conn)
df1 = pd.read_sql("SELECT * FROM option", conn)
df1.head()

# %%
df1.close.plot()

# %%
# 要先加時間索引, 畫出來的圖才會正確
df1.index = pd.to_datetime(df1["date"])
df1.close.plot()

# %%
df_5minK = df1.resample(rule='1d', closed='right').agg({
        'open': 'first', 
        'high': 'max', 
        'low': 'min', 
        'close': 'last',
        'volume': 'sum'})

# %%
df_5minK.head()

# %%
df_5minK.close.plot()


