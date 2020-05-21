from selenium import webdriver
import datetime
import time 
import random 
#--- parameters ----# 
ACOUNT   = "yujia0827"
PASSWORD = "doctorso3_A"
ENTRY_WEBSIDE = "https://my.ntu.edu.tw/attend/ssi.aspx"
CHECKIN_HOUR = 8   # Which hour to checkin,  8:05  ~8:40
CHECKOUT_HOUR = 18 # Which hour to checkout, 18:05 ~18:40
CHECKIO_MINUTE = (5,40) # Which minute area to do io
SLEEP_INTERVAL = 20 # sec 
IS_GUI = False

# --- global variable ----# 
today_check_in_time =["date","hour", "minute" , "sec"]
today_check_out_time=["date","hour", "minute" , "sec"]

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
        browser = webdriver.Chrome(chrome_options=self.options)
        browser.get(ENTRY_WEBSIDE)
        logger.info("Enter entry website.")

        #---- Click login button -----# 
        browser.find_element_by_link_text('登入').click()
        logger.info("Click entry website login button.")

        #---- Myntu login ------# 
        user_acount = browser.find_element_by_name('user')
        user_acount.click()
        user_acount.clear()
        user_acount.send_keys(ACOUNT) # type account name 
        logger.info("Entered user account name")

        # ---- type password------#
        password = browser.find_element_by_name('pass')
        password.click()
        password.clear()
        password.send_keys(PASSWORD)  
        logger.info("Entered user password")

        #--- click login button -----# 
        login = browser.find_element_by_name('Submit')
        login.click()
        logger.info("Click submit button")

        if action == "check_in":
            # ----- click check in button -----# 
            check_in = browser.find_element_by_id('btSign')
            check_in.click()
            logger.warning("CLICK CHECK IN.")
        elif action == "check_out":
            # ----- click check out button -----# 
            check_out = browser.find_element_by_id('btSign2')
            check_out.click()
            logger.warning("CLICK CHECK OUT.")
        #--- close browser ---# 
        time.sleep(3)
        browser.close()
        logger.info("Close browser")
        


def cal_check_IO_time ():
    '''
    Plan when to checkin and checkout today 
    This function should only be execute once per day 
    '''
    global today_check_in_time, today_check_out_time 
    today_check_in_time[0] = datetime.datetime.now().__str__().split()[0] # '2020-05-20'
    today_check_in_time[1] = CHECKIN_HOUR
    today_check_in_time[2] = random.randint(CHECKIO_MINUTE[0],CHECKIO_MINUTE[1])
    today_check_in_time[3] = random.randint(0,60)
    logger.info("Plan to check in at : " + str(today_check_in_time))
    
    today_check_out_time[0] = datetime.datetime.now().__str__().split()[0] # '2020-05-20'
    today_check_out_time[1] = CHECKOUT_HOUR
    today_check_out_time[2] = random.randint(CHECKIO_MINUTE[0],CHECKIO_MINUTE[1])
    today_check_out_time[3] = random.randint(0,60)
    
    logger.info("Plan to check out at : " + str(today_check_out_time))

def main ():
    # global today_check_in_time, today_check_out_time
    last_checkin_date  = "" # '2020-05-20'
    last_checkout_date = "" # '2020-05-20'
    spider = Spider()
    while True:
        #----- Get current time ------# 
        T = datetime.datetime.now().__str__().split() #['2020-05-20', '10:14:32.086912']
        #----- Check if we need to plan -------# 
        # Monday is 0 and Sunday is 6.
        if datetime.datetime.today().weekday() != 5 and \
           datetime.datetime.today().weekday() != 6 and \
           today_check_in_time[0] != T[0] :  # Today haven't plan yet, And it's not SAT or SUN
                cal_check_IO_time()
        
        #----- Check we need to execute our plan right now--------# 
        (hour,minute,sec) = T[1].split(':') # Current time
        hour   = int(hour)
        minute = int(minute)
        logger.info("Date : " + T[0] + ", Hour: " + str(hour) + ", Minute : " + str(minute) + ", sec : " + sec)
        if last_checkin_date != today_check_in_time[0] and hour == today_check_in_time[1] and minute == today_check_in_time[2]:
        # if last_checkin_date != today_check_in_time[0]:
            try: 
                spider.auto_check("check_in")
            except Exception as e:
                logger.error(e.__str__())
            last_checkin_date = today_check_in_time[0]
        elif last_checkout_date != today_check_out_time[0] and hour == today_check_out_time[1] and minute == today_check_out_time[2]:
        # elif last_checkout_date != today_check_out_time[0]:
            try: 
                spider.auto_check("check_out")
            except Exception as e:
                logger.error(e.__str__())
            last_checkout_date = today_check_out_time[0]
        time.sleep(SLEEP_INTERVAL)

if __name__ == '__main__':
    main()


