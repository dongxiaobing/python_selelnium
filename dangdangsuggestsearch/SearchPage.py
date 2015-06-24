#coding=utf-8
#import BasePage
import sys   
reload(sys)  
sys.setdefaultencoding('utf8')   
from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import urllib2
class SearchPage(BasePage):
    total_num_loc=(By.CSS_SELECTOR,".sp.total>.b")
    def is_presence(self):
        WebDriverWait(self,10,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".sp.total>.b")))
    def find_total_num_frontend(self):
        return self.find_element(*self.total_num_loc).text
        #return total_num
    def find_total_num_backend(self):
        #get current url
        current_url=self.driver.get_current_url()
        #get key value
        #print "############"
        #print current_url
        key_value=current_url.split("=")[-1]
        base_url="http://10.255.254.188:8390/?st=full&um=search_ranking&q="
        full_url=base_url+key_value
        #print "#############"
        #print full_url
        u=urllib2.urlopen(full_url)
        contents=u.read()
        u.close()
        pattern = re.compile(r'TotalCnt>(\d+).*TotalCnt')
        return pattern.findall(contents)[0]   
                   
        
        
