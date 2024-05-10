# CSVファイルクレンジング用スクリプト
import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('suumo.csv')
df.drop(df.columns[[2]], axis=1)
df = df.drop(df.index[0])

df.to_csv('suumo_edit.csv')