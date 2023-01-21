from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import pathlib
from lxml import etree
import time
import pandas as pd


class GooglePlay:
    def __init__(self):
        pass

    def save_to_mongo(self, data, db_name, db_collection,
                      connection_string: str = 'mongodb://localhost:27017/'):
        cluster = MongoClient(
            connection_string
        )
        db = cluster[db_name]

        collection = db[db_collection]
        if type(data) == list:
            collection.insert_many(data)
        elif type(data) == dict:
            collection.insert_one(data)
        else:
            raise ValueError('mongodb has received a non-dict and non-list object.')
        collection.find_one()

    def get_url(self, keyword: str) -> bool:
        options = webdriver.ChromeOptions()
        # options.headless = True
        options.add_experimental_option('detach', True)
        options.add_argument("--log-level=3")
        options.add_argument("user-data-dir=selenium")
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        script_directory = pathlib.Path().absolute()
        # chrome_options = Options()
        # chrome_options.add_experimental_option("detach", True)

        options.add_argument(fr"user-data-dir={script_directory}\\userdata")
        options.add_experimental_option(
            "prefs",
            {"profile.default_content_setting_values.notifications": 1}
        )
        # options.headless = True
        s = Service('./chromedriver.exe')
        print(1)
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        print(2)
        # options.headless = False
        wait = WebDriverWait(driver, 10)

        driver.get(f"https://play.google.com/store/search?q={keyword}&c=apps")
        print(3)
        sleep(1)

        try:
            print(4)

            sleep(0.5)

            sectionElement = driver.find_element(By.CSS_SELECTOR,
                                                 "div[class='fUEl2e']")
            soup = BeautifulSoup(sectionElement.get_attribute('innerHTML'), "html.parser")
            backlinks = soup.findAll('a', href=True)
            hrefs = [f"https://play.google.com{a['href']}" for a in backlinks]
            output = {}
            for vpn_detail_page in hrefs:
                try:
                    driver.get(vpn_detail_page)
                    app_name_element = driver.find_element(By.CSS_SELECTOR, "div[class='wkMJlb YWi3ub']")

                    soup_metadata = BeautifulSoup(app_name_element.get_attribute('innerHTML'), "html.parser")
                    support_info_element = driver.find_element(By.CSS_SELECTOR, "div[class='vfQhrf BxIr0d']")

                    soup = BeautifulSoup(support_info_element.get_attribute('innerHTML'), "html.parser")
                    title = soup.find_all('div', {"class": "xFVDSb"})
                    address = soup.find_all('div', {"class": "pSEeg"})
                    try:
                        app_name = soup_metadata.find('div', {"class": "Il7kR"}).text
                    except:
                        app_name = soup_metadata.find('div', {"class": "qxNhq"}).text

                    try:
                        rate = soup_metadata.find('div', {'class': 'TT9eCd'}).text
                    except:
                        rate = 'None'

                    try:
                        downloads_tag = soup_metadata.findAll('div', {'class': 'ClM7O'})
                        if rate == 'None':
                            downloads = downloads_tag[0].text
                        else:
                            downloads = downloads_tag[1].text

                    except:
                        downloads = 'None'
                    usk = soup_metadata.find('span', {'itemprop': 'contentRating'}).text
                    result = {}
                    result['_id'] = app_name
                    for i in range(len(title)):
                        result[title[i].text] = address[i].text
                    print(result)
                    result['rate'] = rate
                    result['downloads'] = downloads
                    result['usk'] = usk
                    result['keyword'] = keyword

                    # output[app_name] = result
                    # output['keyword'] = keyword

                except Exception as e:
                    raise e

                try:
                    self.save_to_mongo(result, 'tapsel', 'vpn', 'mongodb://localhost:27017')

                except Exception as e:
                    print(e)

            # df = pd.DataFrame(dataframe)
            # df.to_csv(f"./{keyword}_{time.time()}.csv")

        except Exception as e:
            print(e)
            pass


gp = GooglePlay()
# try:
#     gp.get_url('vpn 2022')
# except:
#     pass

# try:
#     gp.get_url('تحریم شکن')
# except:
#     pass
# try:
#     gp.get_url('فیلتر شکن قوی')
# except:
#     pass
# try:
#     gp.get_url('وی پی ان')
# except:
#     pass
# try:
#     gp.get_url('proxy')
# except:
#     pass

# try:
#     gp.get_url('فیلتر شکن')
# except:
#     pass
#
# try:
#     gp.get_url('best vpn')
# except:
#     pass

# try:
#     gp.get_url('vpn master')
# except:
#     pass

# try:
#     gp.get_url('proxy vpn')
# except:
#     pass
#
# try:
#     gp.get_url('proxy 2022')
# except:
#     pass

# try:
#     gp.get_url('vpn pro')
# except:
#     pass

# try:
#     gp.get_url('expressvpn')
# except:
#     pass
#
# try:
#     gp.get_url('hotspot vpn')
# except:
#     pass

# try:
#     gp.get_url('psiphon')
# except:
#     pass
# try:
#     gp.get_url('سایفون')
# except:
#     pass
#
#
