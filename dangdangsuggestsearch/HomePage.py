#coding=utf-8
#import BasePage
import sys   
#reload(sys)  
sys.setdefaultencoding('utf8')   
from BasePage import BasePage
from selenium.webdriver.common.by import By
import json
import os
import SearchPage
import time
class HomePage(BasePage):
    url = ''
    username_loc = (By.ID,"idInput") 
    password_loc = (By.ID,"pwdInput") 
    submit_loc = (By.ID,"loginBtn")
    key_loc=(By.ID,"key_S")
    suggest_loc=(By.CSS_SELECTOR,"div[id^='key_']")
    total_num_loc=(By.CSS_SELECTOR,"ul#__suggest_keyword li span.d")#ul#__suggest_keyword li#li_3 span.d
    #Action
    def open(self):
        self._open(self.url)
    def type_search_key(self,key):
        self.find_element(*self.key_loc).send_keys(key)
    def find_total_num_elements(self):
        return self.find_elements(*self.total_num_loc)
    def click_suggest_list(self,num):
        element_list=self.find_elements(*self.total_num_loc)
        element_list[num].click()
        time.sleep(5)
        return SearchPage.SearchPage(self)
    def find_total_num_text(self):
        element_list=self.find_total_num_elements()
        l=[]
        #os.system("rm -rf total_num.txt")
        f=open("total_num.txt","wb")
        for i in element_list:
            #print i.text
            f.write(i.text)
            f.write("\n")
        f.close()   
    def find_suggest_list(self):
        try:
            find_result=self.find_elements(*self.suggest_loc)
        except Exception,e:
            print e
            return None
        else:
            return find_result
    def type_username(self,username): 
        self.find_element(*self.username_loc).send_keys(username)
    def type_password(self,password): 
        self.find_element(*self.password_loc).send_keys(password)
    def submit(self): 
        self.find_element(*self.submit_loc).click()
    def get_current_url(self):
        return self.driver.current_url