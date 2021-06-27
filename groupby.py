import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#参考ページ
#基礎、https://it-engineer-lab.com/archives/1057
#groupby基礎、https://note.nkmk.me/python-pandas-groupby-statistics/
#groupby詳細、https://deepage.net/features/pandas-groupby.html
#groupbyグラフ、http://chachay.hatenablog.com/entry/2017/02/12/151332
#グラフ、https://own-search-and-study.xyz/2016/08/03/pandas%E3%81%AEplot%E3%81%AE%E5%85%A8%E5%BC%95%E6%95%B0%E3%82%92%E4%BD%BF%E3%81%84%E3%81%93%E3%81%AA%E3%81%99/
#グラフ分割、https://qiita.com/gaku8/items/90167693f142ebb55a7d
#グラフ分割、https://qiita.com/supersaiakujin/items/543053ca4610437112df

#CSVファイル読み込み
path = 'input/'
files = os.listdir(path) 
for i, filename in enumerate(files):
    #SHIFTJIS、3列目ロットNoを文字列として読み込み
    df_temp = pd.read_csv(path + filename,encoding='SHIFT-JIS',dtype={2: str})
    if i == 0:
        df = df_temp
    else:
        #2つ目からは追加処理
        df = df.append(df_temp)
else:
    #for文が終わったら、メモリ開放
    del df_temp

#欠損値は削除する
df = df.dropna()

#日本語ラベルだと処理に不都合があるので、アルファベットでラベルをつけなおす
df.columns = ['dt','tm','item', 'size', 't1', 't2', 't3', 't4', 't5', 't6', 'fg', 'remark']


#不要な列（remark）を削除。
df = df.drop(['remark'], axis=1)


#日付と時間を結合
df['dt'] = df['dt'] + ' ' + df['tm']
df = df.drop('tm', axis=1)

#データを確認
#df.to_csv('output/temp.csv')
#print(df.head)


#仕入れ先ごとに、品種とサイズをキーに集計。日時は初回日時、規格は平均と標準偏差を計算
grouped0 = df[df['fg']==0].groupby(['item', 'size']).agg({'dt':np.min, 't1':[np.mean, np.std], 't2':[np.mean, np.std], 't3':[np.mean, np.std], 't4':[np.mean, np.std], 't5':[np.mean, np.std], 't6':[np.mean, np.std]})
grouped1 = df[df['fg']==1].groupby(['item', 'size']).agg({'dt':np.min, 't1':[np.mean, np.std], 't2':[np.mean, np.std], 't3':[np.mean, np.std], 't4':[np.mean, np.std], 't5':[np.mean, np.std], 't6':[np.mean, np.std]})

#メモリ開放
del df

#CSV出力
grouped0.to_csv('output/0.csv')
grouped1.to_csv('output/1.csv')


#グラフ出力
cmap = plt.get_cmap('rainbow')

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
ax1.set_title('Farm0')
grouped0.plot(kind='line', ax=ax1, x=grouped0.columns[0])

ax2.set_title('Farm1')
grouped1.plot(kind='line', ax=ax2, x=grouped1.columns[0])

#plt.title('2021/05/13 09:00:00')
fig.patch.set_facecolor('white') 
plt.show()

