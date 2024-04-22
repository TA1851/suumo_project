import time
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    # WebDriverのセットアップ
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # ウェブページを開く
    driver.get('https://suumo.jp/jj/chintai/kensaku/FR301FB036/?ar=010&bs=040&ra=001&ek=00790&ts=2&et=10&cn=5')
    return driver

def select_dropdown_option(driver, dropdown_name, option_text):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, dropdown_name))).click()
    dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, dropdown_name)))
    dropdown.find_element(By.XPATH, f"//option[. = '{option_text}']").click()

def click_button(driver, button_text):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, button_text))).click()

def extract_data(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')
    data = [[cell.text.strip() for cell in row.find_all('td')] for row in rows]
    return pd.DataFrame(data)

def save_data_to_csv(df, filename):
    if not df.empty:
        df.to_csv(filename, index=False, header=True)
    else:
        print("No data to save.")

#関数を呼び出して実行（Browserの起動）
driver = setup_driver()
select_dropdown_option(driver, "et", "1分～5分")
time.sleep(5) 
click_button(driver, "相場情報を更新する")
time.sleep(10)
df = extract_data(driver)
save_data_to_csv(df, 'suumo_1.csv')

select_dropdown_option(driver, "et", "5分～10分")
time.sleep(5)
click_button(driver, "相場情報を更新する")
time.sleep(10)
df = extract_data(driver)
save_data_to_csv(df, 'suumo_2.csv')

driver.quit()