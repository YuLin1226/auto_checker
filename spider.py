'''
This is a spider sciprt that can get data from cross_website
Output : cross_data.csv
'''

import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
if __name__ == '__main__':
    def parse_table(table):
        '''
        Output : 
            (  [('國立台灣大學 機械工程學系','正取'), ('昆蟲系','備取'), .... ]  ,  ('國立台灣大學 機械工程學系','正取') )
        '''
        priority_list = [] 
        medal_ans  = None 
        rows = table.find('div').find_all('tr')
        for row in rows:
            medal, school, result = row.findChildren('td', recursive=False) # Get infomation from every column
            # isMedal = medal.find('div') is None
            #----- Get school -------# 
            try:
                school = school.find('div').find('a').contents[0] # .strip()
                school = school.replace('\n',' ') # Delete '\n' in the middle
            except IndexError:
                continue
            #----- Get result -----# 
            result = result.find_all('div')[0]
            try: 
                result  = result.contents[0].find_all('div')[0].string # Not first line 
            except AttributeError: # First line 
                result  = result.find_all('div')[0].string
            #---- Get medal --------#
            if medal_ans == None:
                medal = medal.find("img")
                if medal != None :
                    medal_ans = (school,result)
            # ---- append a priority to output  -------# 
            priority_list.append((school,result))
        return (priority_list,medal_ans)
    
    def save_student_list_unstructure(student_list_unstructure):
        '''
        Save student_list_unstructure to python file 
        '''
        file = open('student_list_unstructure.py','w')
        file.write("student_list_unstructure = " + student_list_unstructure.__str__())
        file.close()

    def parse2(response):
        print ('you are here!')
    #---- Get uri content -------# 
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless') # Run chrome without GUI
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox') # Run chrome with root
    # options.add_argument("--disable-dev-shm-usage") # For err msg 
    # chrome_options.add_argument('blink-settings=imagesEnabled=false') # Dont load picture 
    # browser = webdriver.Chrome('/usr/local/share/chromedriver',chrome_options=options)
    browser = webdriver.Chrome(chrome_options=options)

    # ------ Get URI for every department ----------# 
    browser.get("https://my.ntu.edu.tw/attend/ssi.aspx")
    # html_source = browser.page_source
    # soup = BeautifulSoup(html_source, 'html.parser')
    ans = browser.find_element_by_link_text('登入')
    Request('https://web2.cc.ntu.edu.tw/p/s/login2/p1.php',callback=parse2)
    ans.click()
    '''
    uri_list = []
    for tr in soup.find_all("tbody")[2].findChildren('tr', recursive=False): # Start from 2
        td = tr.findChildren('td', resursive=False)
        if len(td) != 5 :  # Not a legal row 
            continue
        uri_tail = td[1].find("a")['href']
        uri_list.append("https://www.com.tw/cross/" + uri_tail)
    '''
    '''
    # student_list_unstructure = []
    std_id_list = []
    std_name_list = []
    std_regist_list = []
    std_priority_list = [[], [] ,[] ,[] ,[] ,[] ,[] ,[] ,[] ,[]]
    
    for uri in uri_list: 
        # ------- For every department ---------# 
        browser.get(uri)
        soup_dep = BeautifulSoup(browser.page_source, 'html.parser')
        stud_data = soup_dep.find_all("tbody")[2].findChildren('tr', recursive=False)
        
        for tr in stud_data[3:]:
            target = tr.findChildren('td', recursive=False)
            if len(target) != 5 : # Not a legal data format 
                continue # Igorn this row 
            id, name, table = target[2:]
            #---- Get ID ------# 
            std_id = id.find('div').contents[0].strip()
            if std_id in std_id_list:
                continue
            table_result = parse_table(table)
            #             ID    ,            name           , score ,   priority list ,    regist
            # student = ( std_id  ,  name.contents[0].strip() ,   []    , table_result[0] , table_result[1])
            # student_list_unstructure.append(student)
            #------- Pandas's Dataframe -------#
            std_id_list.append(std_id)
            std_name_list.append(name.contents[0].strip())
            try: 
                std_regist_list.append(table_result[1][0]) # Only department and school is recorded.
            except TypeError: # table_result[1] ==  None
                std_regist_list.append(None)

            for i in range(len(std_priority_list)):
                try: 
                    std_priority_list[i].append(table_result[0][i][0] + " " + str(table_result[0][i][1])) # [('國立台灣大學 機械工程學系','正取'), ('昆蟲系','備取'), .... ] 
                except IndexError: 
                    std_priority_list[i].append(None)
        '''

