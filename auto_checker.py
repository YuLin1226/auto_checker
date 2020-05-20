from selenium import webdriver
import datetime
import time 
import random 
#--- parameters ----# 
ACOUNT   = "yujia0827"
PASSWORD = "doctorso3_A"
ENTRY_WEBSIDE = "https://my.ntu.edu.tw/attend/ssi.aspx"
CHECKIN_HOUR = "11" # Which hour to checkin
CHECKOUT_HOUR = "18" # Which hour to checkout 
CHECKIO_MINUTE = (15,45) # Which minute area to do io
SLEEP_INTERVAL = 30 # sec 

# --- global variable ----# 
today_check_in_time =["date","hour", "minute" , "sec"]
today_check_out_time=["date","hour", "minute" , "sec"]

class Spider():
    def __init__(self):
        #---- Get uri content -------# 
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-extensions')
        # options.add_argument('--headless') # Run chrome without GUI
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox') # Run chrome with root
        # options.add_argument("--disable-dev-shm-usage") # For err msg 
        # chrome_options.add_argument('blink-settings=imagesEnabled=false') # Dont load picture 
        # browser = webdriver.Chrome('/usr/local/share/chromedriver',chrome_options=options)

    def auto_check_in(self):
        browser = webdriver.Chrome(chrome_options=self.options)
        browser.get(ENTRY_WEBSIDE)
    
        browser.find_element_by_link_text('登入').click()
        
        #---- Myntu login ------# 
        user_acount = browser.find_element_by_name('user')
        user_acount.click()
        user_acount.clear()
        user_acount.send_keys(ACOUNT) # type account name 

        # ---- type password------#
        password = browser.find_element_by_name('pass')
        password.click()
        password.clear()
        password.send_keys(PASSWORD)  

        #--- click login button -----# 
        login = browser.find_element_by_name('Submit')
        login.click()
        
        # ----- click check in button -----# 
        check_in = browser.find_element_by_id('btSign')
        check_in.click()
        
        #--- close browser ---# 
        time.sleep(3)
        browser.close()
    
    def auto_check_out(self):
        browser = webdriver.Chrome(chrome_options=self.options)
        browser.get(ENTRY_WEBSIDE)
    
        browser.find_element_by_link_text('登入').click()
        
        #---- Myntu login ------# 
        user_acount = browser.find_element_by_name('user')
        user_acount.click()
        user_acount.clear()
        user_acount.send_keys(ACOUNT) # type account name 

        # ---- type password------#
        password = browser.find_element_by_name('pass')
        password.click()
        password.clear()
        password.send_keys(PASSWORD)  

        #--- click login button -----# 
        login = browser.find_element_by_name('Submit')
        login.click()
        
        # ----- click check in button -----# 
        check_out = browser.find_element_by_id('btSign2')
        check_out.click()

        #--- close browser ---# 
        time.sleep(3)
        browser.close()



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
    print ("Plan to check in at : " + str(today_check_in_time))
    
    today_check_out_time[0] = datetime.datetime.now().__str__().split()[0] # '2020-05-20'
    today_check_out_time[1] = CHECKOUT_HOUR
    today_check_out_time[2] = random.randint(CHECKIO_MINUTE[0],CHECKIO_MINUTE[1])
    today_check_out_time[3] = random.randint(0,60)
    print ("Plan to check out at : " + str(today_check_out_time))

def main ():
    # global today_check_in_time, today_check_out_time
    last_checkin_date  = "2020-05-19"
    last_checkout_date = "2020-05-19"
    spider = Spider()
    while True:
        T = datetime.datetime.now().__str__().split() #['2020-05-20', '10:14:32.086912']

        # ----- Do we plan today checkI/O time already ? ------#  
        if today_check_in_time[0] == T[0]: # Yes, plan before
            print ("Today plan before")
            pass 
        else: # No, plan one now
            cal_check_IO_time()

        (hour,minute,sec) = T[1].split(':') # Current time
        # check if now is the today today_check_in_time  
        # if last_checkin_date != today_check_in_time[0] and hour == today_check_in_time[1] and minute == today_check_in_time[2]: # TODO 
        if last_checkin_date != today_check_in_time[0]:
            print ("Check In !!!" + str(T))
            spider.auto_check_in()
            last_checkin_date = today_check_in_time[0]
        # elif last_checkout_date != today_check_out_time[0] and hour == today_check_out_time[1] and minute == today_check_out_time[2]: # TODO 
        elif last_checkout_date != today_check_out_time[0]:
            print ("Check out!"  + str(T))
            spider.auto_check_out()
            last_checkout_date = today_check_out_time[0]
        time.sleep(SLEEP_INTERVAL)

if __name__ == '__main__':
    main()


