#coding=utf-8
import sys   
reload(sys)  
sys.setdefaultencoding('utf8')  
from selenium import webdriver
from selenium.webdriver.common.by import By 
from time import sleep
import unittest
import HomePage
import SearchPage
import ConfigParser
import json
class TestLoginPageObject(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        #self.base_url = "http://www.dangdang.com/"
        self.verificationErrors = []
        self.accept_next_alert = True  
        #self.key=u"数据"  
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
    def configparse(self,loc):
        conf = ConfigParser.ConfigParser()
        conf.read("testdata.conf")
        search_key = conf.get("testdata", loc)
        return search_key
    def get_suggest_list(self,key):
        dr=self.driver
        home_page = HomePage.HomePage(dr)
        home_page.open()    
        home_page.type_search_key(key)
        
        #suggest list
        suggest_element_list=home_page.find_suggest_list()
        #print suggest_element_list
        suggest_element_list_length=len(suggest_element_list)
        #print suggest_element_list_length
        #sleep(5)
        return suggest_element_list_length  
    def non_test_pub1(self):
        """
        搜索“数据”,弹出的建议列表应该是11个
        """
        #get search data from configure file tetstdata.conf
        #pub1 数据
        key=self.configparse("pub1")
        key=json.loads(key)
        suggest_element_list_length=self.get_suggest_list(key)
        #搜索建议的列表长度应该是11
        self.assertEqual(int(suggest_element_list_length),11)
    
    def non_test_pub2(self):
        """
        搜索“英语”，弹出的建议列表应该是11个
        """
        #get search data from configure file tetstdata.conf
        #pub2 英语
        key=self.configparse("pub2")
        key=json.loads(key)
        suggest_element_list_length=self.get_suggest_list(key)
        #搜索建议的列表长度应该是11
        self.assertEqual(int(suggest_element_list_length),11)
    def non_test_special_character(self):
        """
        搜索特殊字符，弹出的建议列表为空
        """
        #get search data from configure file tetstdata.conf
        #pub3 @
        key=self.configparse("pub3")
        key=json.loads(key)
        suggest_element_list_length=self.get_suggest_list(key)
        #搜索建议的列表长度应该是11
        self.assertEqual(int(suggest_element_list_length),0)
    def get_total_num(self):
        key=self.configparse("pub1")
        key=json.loads(key)
        dr=self.driver
        home_page = HomePage.HomePage(dr)
        home_page.open()
        home_page.type_search_key(key)
        home_page.find_total_num_text()
    def click_suggest_num(self,num):
        key=self.configparse("pub1")
        key=json.loads(key)
        dr=self.driver
        home_page = HomePage.HomePage(dr)
        home_page.open()
        home_page.type_search_key(key)
        return home_page.click_suggest_list(num)
    def test_compare_first_total_nums(self):
        self.get_total_num()
        f=open("total_num.txt","r")
        total_num_suggestlist=f.readline()
        f.close()
        l=[]
        total_num_suggestlist=total_num_suggestlist[3:7]
        
        #建议列表中显示的搜索总数
        print "sugget list total num"
        print total_num_suggestlist
        sp=self.click_suggest_num(0)
        sp.is_presence()
        #前端显示的搜索总数
        print "frontend total num"
        total_num_frontend=sp.find_total_num_frontend()
        print total_num_frontend
        #后台显示的搜索总数
        sleep(5)
        print "backend total num"
        total_num_backend=sp.find_total_num_backend()
        print total_num_backend
        sleep(5)
        
        
        
        
        #print home_page.find_total_num()  
if __name__ == "__main__":
    unittest.main()
    