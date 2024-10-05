from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.window import WindowTypes
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import logging
from datetime import datetime
import random
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import threading
import socket
from bs4 import BeautifulSoup
import json
import pandas as pd


CHROME_DRIVER_PATH = "./chromedriver.exe"
TARGET_WEBSITE_URL = "https://www.tiktok.com"

PAGE_SCROLL_DOWN_LIMIT = 50

FOLLOWER_LIMIT = 1000
LIKE_LIMIT = 100



USER_AGENTS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4564.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4084.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.62 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4896.52 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-N970U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.60 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G781U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4564.47 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; LM-G900N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.39 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 3a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi K20 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G986U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.38 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; LG-G820) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.59 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-J600F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.82 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G930U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G970U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A705F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G980U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; LG-Q730) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4084.89 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; LM-G710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.58 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4896.60 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4896.65 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4896.65 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4896.69 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4896.70 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4896.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4896.72 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4896.74 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4896.75 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4896.76 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4896.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4896.78 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4896.79 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4896.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4896.81 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4896.82 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4896.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4896.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4896.86 Mobile Safari/537.36",
]


class ScraperLogger:
    """
    This class creates loggs of all movements for scraper.

    Attributes:
    _filename contains a string name of the file where loggs are stored.
    _filemode contains a string value indicated the above file's accessibility
    _format contains concatenated string of time, seconds, name, level and message for every actions
    _dateformat contains string of date format for tracks loggs of each actions
    """

    def __init__(self):
        self._logger_name = "puresounds"
        self._filename = "web_traffic_logging.log"
        self._filemode = "a"
        self._format = "%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"
        self._dateformat = "%d-%b-%y %H:%M:%S"
        self.setup_logfile()

    def setup_logfile(self):
        """
        Initialize logging config
        """
        logging.basicConfig(
            filename=self._filename,
            filemode=self._filemode,
            format=self._format,
            datefmt=self._dateformat,
            level=logging.INFO,
        )


class WebTraffic:
    def __init__(self) -> None:
        self.browser_options = ChromeOptions()
        self.browser_options.headless = False
        self.browser_options.add_argument("--log-level=1")
        self.browser_options.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 1 
        })
        self.service = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = None
        self.run_driver()
        self.is_messenger_logged_in = False

    def run_driver(self, user_agent=None) -> None:
        """
        A method which initialize the selenium driver.
        """
        if user_agent:
            self.browser_options.add_argument(f"user-agent={user_agent}")
        self.driver = Chrome(service=self.service, options=self.browser_options)
        self.driver.maximize_window()

    def wait_till_locator(
        self, by_what, by_value, load_time=120, soup_driver=None
    ) -> None:
        """
        A method which helps to check a specific web element of page
        is existed or not within a load duration time.
        """
        try:
            element = EC.presence_of_element_located((by_what, by_value))
            if soup_driver:
                WebDriverWait(soup_driver, load_time).until(element)
            else:
                WebDriverWait(self.driver, load_time).until(element)
            logging.info("Locator loading is found properly")
            return True
        except TimeoutException:
            logging.debug("Locator loading is not found properly")
            return False

    def accept_cokkies(self) -> None:
        """
        A method which accepts puresounds cookies.
        """
        if self.wait_till_locator(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'):
            logging.info("Finding accept cokkies button")
            accept_button = self.driver.find_element(
                By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'
            )
            logging.info("click on accept cokkies")
            accept_button.click()
        else:
            logging.warning("accept_all_cookies not loaded")

    def get_custom_user_agent(self) -> str:
        """
        Returns a random user agent string.
        """
        return random.choice(USER_AGENTS_LIST)

    def go_next_tab(self) -> None:
        """
        A method whichs move current tab to immediate next tab
        """
        total_tabs = len(self.driver.window_handles)
        if total_tabs > 1:
            self.driver.switch_to.window(self.driver.window_handles[total_tabs - 1])
        else:
            logging.info("There are less than 1 tabs!")


    def read_json_file(self, file_name) -> None:
        data = []
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
            return data
        except:
            logging.info(f"{file_name} file is not found!")

    def write_json_file(self, file_name, data) -> None:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def page_scroll_down(self):
        limit = PAGE_SCROLL_DOWN_LIMIT
        while limit > 0:
            print(f"scrolling down and {limit} times left")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(10)
            limit -= 1

    def move_tag_page(self, hash_code):
        if self.wait_till_locator(By.TAG_NAME, "canvas"):
            print("Search video elements are loaded")
            # example: href="/tag/wanderlust"
            target_hash_tag_link_elements = self.driver.find_element(By.XPATH, f'//a[@href="/tag/{hash_code}"]')
            time.sleep(2)
            target_hash_tag_link_elements.click()
        else:
            logging.warning("Search posts are not loaded yet.")

    def get_video_id_from_tiktok_video_url(self, url):
        left_part = url.split('video/')
        return left_part[1]

    def get_username_from_tiktok_video_url(self, url):
        left_part = url.split('/@')
        right_part = left_part[1].split('/video')
        return right_part[0]

    def get_post_data_from_list(self, post_element):
        video_box = post_element.find("div", {"data-e2e": 'challenge-item'})
        if video_box:
            video_link_element =  video_box.find("a") # first anchor tag has video url
            author_username = self.get_username_from_tiktok_video_url(video_link_element['href'])
            video_id = self.get_video_id_from_tiktok_video_url(video_link_element['href'])
            # Description below the video card
            description_box = video_box.find_next_sibling('div').find("a")
            if description_box is None:
                return None
            video_caption = description_box['title']

            data = {
                "video_url": video_link_element["href"],
                "video_caption": video_caption,
                "author_username": author_username
            }
            return data
        return None

    def get_tag_posts(self, link_data):
        if self.wait_till_locator(By.TAG_NAME, "video"):
            page_data = self.driver.page_source
            page_soup = BeautifulSoup(page_data, features="html.parser")
            post_element_wrapper = page_soup.find("div", {"data-e2e": "challenge-item-list"})
            post_element_list = post_element_wrapper.find_all("div")
            for element in post_element_list:
                post_data = self.get_post_data_from_list(element)
                if post_data:
                    link_data.append(post_data)
        else: 
            logging.warning("Tag posts are not loaded yet.")

    def get_user_data(self):
        page_data = self.driver.page_source
        soup = BeautifulSoup(page_data, 'html.parser')
        follower_element = soup.find_all("span", {'data-e2e':"followers-count"})
        print('====================PENDING=================')

    def get_user_profile_information(self, link_data):
        
        for data in link_data:
            username = data['author_username']
            user_profile_link = TARGET_WEBSITE_URL+f"/@{username}"
            self.driver.get(user_profile_link)
            time.sleep(4)
            self.get_user_data()


    def store_data_csv_format(self, link_data):
        core_df = pd.DataFrame(
            columns=[
                'id',
                "username",
                "video_url",
                "video_caption",
                "follower_count",
                "like_count",
                "followers",
                "likes",
            ]
        )
        index_no = 0
        for data in link_data:
            parent_row = {
                "id": index_no+1,
                "username": data['author_username'],
                "video_url": data['video_url'],
                "video_caption": data['video_caption'],
                "follower_count": 0,
                "like_count": 0,
                "followers": 0,
                "likes": 0,
            }
            core_df.loc[index_no] = parent_row
            index_no+=1            
            core_df.to_csv("hashtag_data.csv", index=False)


    def run_through_hashcode(self, hash_code) -> None:
        starttime = datetime.now()

        self.driver.get(f"{TARGET_WEBSITE_URL}/tag/{hash_code}")
        time.sleep(5)
        link_data = []

        time.sleep(30)
        self.page_scroll_down()
        self.get_tag_posts(link_data)
        # self.get_user_profile_information(link_data) 
        self.store_data_csv_format(link_data)
        
        endtime = datetime.now()
        logging.info(f"Start time: {starttime}")
        logging.info(f"End time: {endtime}")
        logging.info(f"Total Duration: {endtime - starttime}")
        time.sleep(5)
        custom_user_agent = self.get_custom_user_agent()
        self.run_driver(user_agent=custom_user_agent)
        user_agent = self.driver.execute_script("return navigator.userAgent;")
        logging.info(user_agent)
        time.sleep(10)


def run_scraper(hash_code):
    web_traffic = WebTraffic()
    web_traffic.run_through_hashcode(hash_code)

def is_internet_connected():
    try:
        s = socket.create_connection(("1.1.1.1", 80))
        logging.info("Internet connection is available!")
        return True
    except OSError:
        logging.info("There is no internet connection!")
    return False

def categories_scraper_threads():
    t0 = threading.Thread(target=run_scraper, args=(0,))

    t0.start()
   

    t0.join()

if __name__ == "__main__":
    scraper_logger = ScraperLogger()
    hash_code_list = ['traveltok',]
    run_scraper(hash_code_list[0])
