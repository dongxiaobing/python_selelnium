#coding=utf-8
import sys   
from selenium.webdriver.support.wait import WebDriverWait

reload(sys)  
sys.setdefaultencoding('utf8')  
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import unittest
import ConfigParser
import json
class TestSearchOptimize(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://search.dangdang.com"
        self.verificationErrors = []
        self.accept_next_alert = True  
        #self.key=u"数据"  
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
    def get_search_data(self,data):
        conf = ConfigParser.ConfigParser()
        conf.read("testdata.conf")
        test_data=conf.items(data)
        return test_data
    def element_is_present_all_products(self,dr):
        try:
            WebDriverWait(dr, 2).until(lambda dr : dr.find_element_by_css_selector(".now[dd_name='全部商品']"))
        except NoSuchElementException:
            return False
        except TimeoutException:      
            if str(dr.find_element_by_css_selector(".search_null_ts").text).find("看看输入的文字是否有误")>0:       
                return "No result"
            else:
                return False
        else:
            return True
    def element_is_present_english(self,dr):
        try:
            WebDriverWait(dr, 2).until(lambda dr : dr.find_element_by_css_selector("li[dd_name='英语考试必备']"))
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False
        else:
            return True
    def element_is_present_account(self,dr):
        try:
            WebDriverWait(dr, 2).until(lambda dr : dr.find_element_by_css_selector("li[dd_name='注册会计师必备']"))
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False
        else:
            return True
    def assert_elements_english(self,dr,test_data):
        element_flag_all=self.element_is_present_all_products(dr)
        if element_flag_all=="No result":
            print "the test data %s has no search result" % test_data
            self.assertTrue(element_flag_all=="No result")
        elif element_flag_all=="True":
            self.assertTrue(element_flag_all)
            element_flag_english=self.element_is_present_english(dr)
            self.assertTrue(element_flag_english)
        else:
            pass
    def assert_elements_account(self,dr,test_data):
        element_flag_all=self.element_is_present_all_products(dr)
        if element_flag_all=="No result":
            print "the test data '%s' has no search result!!!!!!!!!!!!!!!!!!!!!!!!!" % test_data
            self.assertTrue(element_flag_all=="No result")
        elif element_flag_all=="True":
            self.assertTrue(element_flag_all)
            element_flag_account=self.element_is_present_account(dr)
            self.assertTrue(element_flag_account)
        else:
            pass
    def input_test_data(self,dr,test_data):
        dr.get(self.base_url)
        dr.find_element_by_id("key_S").clear()
        dr.find_element_by_id("key_S").send_keys(test_data)
        dr.find_element_by_id("key_S").send_keys(Keys.ENTER)
    def test_001_englist_search(self):
        """
               英语考试必备
        """       
        print "###################test englist#######################"
        test_data=self.get_search_data("English")
        n=1
        for i in test_data:
            #print i[1]
            test_data=i[1]
            test_data=json.loads(test_data)
            dr=self.driver
            print "This is the '%s' test,the test data is %s " % (n,test_data)
            self.input_test_data(dr,test_data)
            self.assert_elements_english(dr,test_data)
            print "The %s test pass!" % n
            dr.back()
            n+=1
    def test_002_account_search(self):
        """
                注册会计师必备
        """
        print "###################test account#######################"
        test_data=self.get_search_data("Account")
        n=1
        for i in test_data:
            #print i[1]
            test_data=i[1]
            test_data=json.loads(test_data)
            dr=self.driver
            print "This is the '%s' test,the test data is %s " % (n,test_data)
            self.input_test_data(dr,test_data)
            self.assert_elements_account(dr,test_data)
            print "The %s test pass!" % n
            dr.back()
            n+=1
if __name__ == "__main__":
    unittest.main()