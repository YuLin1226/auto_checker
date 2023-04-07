#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time 
import random 
#--- parameters ----# 
ACOUNT   = "yulinchen"
PASSWORD = "Chinese10126"
ENTRY_WEBSIDE = "https://my.ntu.edu.tw/attend/ssi.aspx"
CHECKIN_HOUR = 8   # Which hour to checkin,  8:05  ~8:40
CHECKOUT_HOUR = 18 # Which hour to checkout, 18:05 ~18:40
CHECK_MINUTE = (1,15) # Which minute area to do io
SLEEP_INTERVAL = 20 # sec 
IS_GUI = True
PATH_TO_DRIVER = "/home/ryannn/auto_checker/chromedriver"

##################
####  logger   ###
##################
import logging 
# Set up logger
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger('auto_checker')
logger.setLevel(logging.DEBUG)

# Print out logging message on console
h_console = logging.StreamHandler()
h_console.setFormatter(formatter)
h_console.setLevel(logging.INFO)
logger.addHandler(h_console)

# Record logging message at logging file
h_file = logging.FileHandler("auto_checker.log")
h_file.setFormatter(formatter)
h_file.setLevel(logging.INFO)
logger.addHandler(h_file)

class Spider():
    def __init__(self):
        #---- Get uri content -------# 
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox') # Run chrome with root
        if not IS_GUI:
            self.options.add_argument('--headless') # Run chrome without GUI
        # options.add_argument("--disable-dev-shm-usage") # For err msg 
        # chrome_options.add_argument('blink-settings=imagesEnabled=false') # Dont load picture 
        # browser = webdriver.Chrome('/usr/local/share/chromedriver',chrome_options=options)

    def auto_check(self, action):
        '''
        action = "check_in"
        action = "check_out"
        '''
        logger.info("Start auto checking routine.")
        browser = webdriver.Chrome(PATH_TO_DRIVER, options=self.options)
        browser.get(ENTRY_WEBSIDE)
        logger.info("Enter entry website.")

        #---- Click login button -----# 
        browser.find_element(By.LINK_TEXT, '登入').click()
        logger.info("Click entry website login button.")

        #---- Myntu login ------# 
        user_acount = browser.find_element(By.NAME, 'user')
        user_acount.click()
        user_acount.clear()
        user_acount.send_keys(ACOUNT) # type account name 
        logger.info("Entered user account name")

        # ---- type password------#
        password = browser.find_element(By.NAME, 'pass')
        password.click()
        password.clear()
        password.send_keys(PASSWORD)  
        logger.info("Entered user password")

        #--- click login button -----# 
        login = browser.find_element(By.NAME, 'Submit')
        login.click()
        logger.info("Click submit button")

        if action == "check_in":
            # ----- click check in button -----# 
            check_in = browser.find_element(By.ID, 'btSign')
            check_in.click()
            logger.warning("CLICK CHECK IN.")
        elif action == "check_out":
            # ----- click check out button -----# 
            check_out = browser.find_element(By.ID, 'btSign2')
            check_out.click()
            logger.warning("CLICK CHECK OUT.")
        #--- close browser ---# 
        time.sleep(5)
        browser.close()
        logger.info("Close browser")
        
def check():
    spider = Spider()
    if datetime.datetime.today().weekday() == 5 and datetime.datetime.today().weekday() == 6:
        print ("Weekends, Skip check in.")
        return
    
    # Get current time
    T = datetime.datetime.now().__str__().split() #['2020-05-20', '10:14:32.086912']
    hour, minute, sec = T[1].split(':')
    hour   = int(hour)
    minute = int(minute)
    logger.info("Date : " + T[0] + ", Hour: " + str(hour) + ", Minute : " + str(minute) + ", sec : " + sec)
    try: 
        if hour > CHECKIN_HOUR+1 or hour < CHECKIN_HOUR-1:
            print("Wrong time to check in.")
            return
        checktime_at_minute = random.randint(CHECK_MINUTE[0],CHECK_MINUTE[1])
        if minute < checktime_at_minute:
            sleep_time_second = (checktime_at_minute - minute)*60
            time.sleep(sleep_time_second)
        spider.auto_check("check_in")
    except Exception as e:
        logger.error(e.__str__())


if __name__ == '__main__':
    print ("Start autochecker")
    check()
    print ("End autochecker")


