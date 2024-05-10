# CSVファイルクレンジング用スクリプト
import pandas as pd

# CSVファイルを開く
df = pd.read_csv('hiragishi_4.csv', encoding='utf-8')  # 開く際のエンコーディングを指定

# 文字列を含む列の改行を削除する
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].replace('\n', '', regex=True)
    
# 新しいエンコーディングでCSVファイルを保存
df.replace({'\uff0d': '-'}, regex=True, inplace=True)
df.to_csv('hiragishi_5.csv', encoding='shift_jis', index=False)