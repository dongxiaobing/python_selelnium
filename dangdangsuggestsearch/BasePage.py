#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
class BasePage(object):
    #url="http://www.dangdang.com"
    login_url = 'http://www.dangdang.com'
    def __init__(self, selenium_driver,base_url=login_url, parent=None): 
        self.base_url = base_url
        self.driver = selenium_driver
        self.timeout = 30
        self.parent = parent
        self.tabs = {}
    def _open(self,url):
        url = self.base_url+url
        self.driver.get(url)
        #assert self.on_page(),'Did not land on %s' % url
    def find_element(self,*loc):
        return self.driver.find_element(*loc)
    def find_elements(self,*loc):
        return self.driver.find_elements(*loc)

    def open(self):
        self._open(self.url)
    def script(self,src):
        return self.driver.execute_script(src)
    def send_keys(self,loc,value, clear_first=True, click_first=True): 
        try:
            loc = getattr(self, '_%s' % loc)
            if click_first:
                self.find_element(*loc).click() 
            if clear_first:
                self.find_element(*loc).clear() 
            self.find_element(*loc).send_keys(value)
        except AttributeError:
            print '%s page does not have "%s" locator' %(self,loc)
    def get_current_url(self):
        return self.driver.current_url
      