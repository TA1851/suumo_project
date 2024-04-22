import bs4 as bs
import time
import urllib.request
import pandas as pd

source = urllib.request.urlopen('https://suumo.jp/jj/chintai/kensaku/FR301FB036/?ar=010&bs=040&ra=001&ek=00790&ts=2&et=10&cn=5').read()
#全てのhtmlタグを取得する
soup = bs.BeautifulSoup(source,'html.parser')
#bodys = soup.find_all('label')
#bodys = soup.find_all('select')
#bodys = soup.find_all('a')
bodys = soup.find_all('tr')
#bodys = soup.find_all('option')
# for tags in bodys:
#     print(tags.prettify())

# <tr>タグからすべての行を取得
rows = soup.find_all('tr')

# 行データをリストに整形
data = []
for row in rows:
    cols = row.find_all('td')  # <td> タグを探す
    cols = [ele.text.strip() for ele in cols]  # テキストデータを取得し、前後の空白を削除
    data.append(cols)  # リストに行データを追加

# DataFrameを作成
df = pd.DataFrame(data)
# CSVに書き出し。最初の行が空白列なら、それを除外
#df.to_csv('suumo.csv', index=False, header=True, encoding='Shift_JIS')  # header=False はここでは列名が不要な場合
df.to_csv('suumo.csv', index=False, header=True)  # header=False はここでは列名が不要な場合
