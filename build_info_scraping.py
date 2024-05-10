import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #取得したいURLを指定
    driver.get('https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=010&bs=040&ra=001&rn=4060&ek=406033250&cb=0.0&ct=9999999&mb=0&mt=80&md=07&ts=1&et=9999999&cn=30&co=1&tc=0400901&tc=0401102&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04&pc=50')
    # windowサイズはPyautoguiで取得
    driver.set_window_size(1920, 1080)
    return driver

def extract_data(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # CSSセレクタを指定してデータを取得
    build_names = [item.text.strip() for item in soup.select('.cassetteitem_content-title')]
    build_addresses = [item.text.strip() for item in soup.select('.cassetteitem_detail-col1')]
    build_ages = [item.text.strip() for item in soup.select('.cassetteitem_detail-col3')]
    build_prices = [item.text.strip() for item in soup.select('.cassetteitem_other-emphasis.ui-text--bold')]

    # データの長さを確認し、最短の長さに合わせる
    min_length = min(len(build_names), len(build_addresses), len(build_ages), len(build_prices))
    data = {
        'Buken': build_names[:min_length],
        'Address': build_addresses[:min_length],
        'Age': build_ages[:min_length],
        'Price': build_prices[:min_length]
    }
    return pd.DataFrame(data)

# 現在のぺージのUIをクリックする関数
def click_button(driver, button_text):
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.ID, "js-tabmenu2-pcChange")))
    button.click()
    select = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[. = '50件']")))
    select.click()
    next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pagination pagination_set-nav")))
    next_button.click()
# 次のページに遷移するためのUIをクリックする関数
def click_button(driver, button_text):
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pagination-parts")))
    next_button.click()
# データをCSVに保存する関数    
def save_data_to_csv(df, filename):
    if not df.empty:
        df.to_csv(filename, index=False)
    else:
        print("No data to save.")
        
# Browserを開く
driver = setup_driver()
time.sleep(10)
# 表示建物数を50に変更
click_button(driver, '50件')
time.sleep(3)
# スクレイピングしたデータをDFに格納してCSVに保存
df = extract_data(driver)
save_data_to_csv(df, 'hiragishi_3.csv')
time.sleep(5)

# 次のページに移動
click_button(driver, '次へ')
time.sleep(5)
# スクレイピングしたデータをDFに格納してCSVに保存
df = extract_data(driver)
save_data_to_csv(df, 'hiragishi_4.csv')
time.sleep(3)
driver.quit()