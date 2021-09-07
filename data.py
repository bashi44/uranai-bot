# モジュールインポート
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import urllib.request as req
import time
import json

# seleniumをあらゆる環境で起動させるchromeオプション
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--headless')

# google chrome を起動
driver = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(3)

# 対象のページにアクセス
url = 'https://cocoloni.me/unsei'
driver.get(url)
response = req.urlopen(url)
soup = BeautifulSoup(response, "html.parser")
time.sleep(3)

# さらに読み込みをクリック
element = driver.find_element_by_id('ajax_next')
element.click()

# 星座の名前を取得
signs = {}
for i in range(1, 13):
  lists = []
  #星座名
  obj1 = {}
  name = soup.select(f'#rank-{i} > dt')
  obj1['name'] = name[0].contents[1]
  lists.append(obj1)
  #ランキング
  obj2 = {}
  rank = soup.select(f'#rank-{i} > dt > span')
  obj2['rank'] = rank[0].text
  lists.append(obj2)
  #メッセージ
  obj3 = {}
  message = soup.select(f'#rank-{i} > dd > *')
  if i == 1 or i == 2:
      obj3['message'] = message[0].contents[0].text
  else:
      obj3['message'] = message[1].text
  lists.append(obj3)
  signs[obj1['name']] = lists

time.sleep(3)

# jsonファイルに書き込み
with open('/Applications/MAMP/htdocs/uranai_bot/save.json', 'w', encoding='utf-8') as save:
    json.dump(signs, save, indent=2, ensure_ascii = False)