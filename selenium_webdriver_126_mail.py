#!/bin/python
#coding=utf-8

"""
1.test login
2.test send mail
3.test send mail with attached
4.test delete mail
5.test search mail
6.test popup recipients
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class TestLogin(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(30)
        #self.base_url = "http://www.126.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.mail_from="dxbselenium@126.com"
        self.mail_password="dxb123456"
        self.mail_to="dxbselenium@126.com"
        self.mail_topic="test126"
    
        
    def login(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.126.com/"
        driver=self.driver
        driver.maximize_window()
        driver.get(self.base_url + "")
        driver.find_element_by_id("idInput").clear()
        driver.find_element_by_id("idInput").send_keys(self.mail_from.split("@")[0])
        driver.find_element_by_id("pwdInput").clear()
        driver.find_element_by_id("pwdInput").send_keys(self.mail_password)
        driver.find_element_by_id("loginBtn").click()

    def total_received_mails(self):
        #self.login()
        driver=self.driver
        #find received box
        driver.find_element_by_css_selector("div>ul>li>div>span+span[class='nui-tree-item-text']").click()
        #find the lastest unread mail and delete the mail
        try:
            checkbox_list=driver.find_elements_by_css_selector("label.nui-chk>span.nui-chk-symbol>b")
            return len(checkbox_list)
        except Exception,e:
            print "there has no received mail" 
            return 0   
    def verify_received_mail_status(self):
        #self.login()
        driver=self.driver
        driver.find_element_by_css_selector("div>ul>li>div>span+span[class='nui-tree-item-text']").click()
        #find the lastest unread mail 
        try:       
            status_list=driver.find_elements_by_css_selector("label.nui-chk+b[title='未读']")
            first_status_list=status_list[0].get_attribute('title')
            return first_status_list         
        except Exception:
            print "there has no received mail unread"
            return u"已读" 
    def verify_received_mail_sender(self):
        #self.login()
        driver=self.driver
        #click received mail box
        driver.find_element_by_css_selector("div>ul>li>div>span+span[class='nui-tree-item-text']").click()
        #find the sender
        try:
            #find all of senders       
            sender_list=driver.find_elements_by_css_selector("div[sign='start-from']>span")
            #print sender_list
            #find the newest sender
            first_sender_list=sender_list[0].text
            return first_sender_list         
        except Exception:
            print "there has no received mail unread"
            #return u"已读" 
    def verify_received_mail_topic(self):
        #self.login()
        driver=self.driver
        #click received mail box
        driver.find_element_by_css_selector("div>ul>li>div>span+span[class='nui-tree-item-text']").click()
        #find the sender
        try:
            #find all of senders       
            topic_list=driver.find_elements_by_css_selector("div[sign='start']+div>span")
            #print sender_list
            #find the newest sender
            first_topic_list=topic_list[0].text
            return first_topic_list         
        except Exception:
            print "there has no received mail unread"
            #return u"已读" 
    
    def sendmail(self,recipients_popup="no"):
        #self.login()
        driver=self.driver
        element = WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"b.nui-ico.fn-bg.ga0")))
        element.click()
        if recipients_popup=="no":
            element = WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input.nui-editableAddr-ipt")))
            element.send_keys(self.mail_to)
        else:
            element = WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input.nui-editableAddr-ipt")))
            element.send_keys("d")
            #定位悬停的元素,点击填出的收件人
            driver.find_element_by_class_name("nui-menu-item-text").click()
            
        #switch zhuti frame
        element = WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.XPATH,"//section/header/div[2]/div[1]/div/div/input")))
        element.send_keys(self.mail_topic)
         
        #swith to text iframe
        xf = driver.find_element_by_xpath('//*[@class="APP-editor-iframe"]')
        driver.switch_to_frame(xf)
        driver.find_element_by_css_selector("body.nui-scroll").send_keys("test1261_text")
        
        #back to default content and send email
        driver.switch_to_default_content()
    def verify_mail(self):
        self.login()
        total_received_mail_nums_after=self.total_received_mails()
        #assert received a new mail
        #self.assertEqual(int(total_received_mail_nums_before),int(total_received_mail_nums_after)-1)
        #assert the status of the new received mail status as 未读
        self.assertEqual(self.verify_received_mail_status(),u'未读')
        #assert the sender of the new received mail 
        self.assertEqual(self.verify_received_mail_sender(),self.mail_from.split("@")[0])
        #assert the topic of the new received mail
        self.assertEqual(self.verify_received_mail_topic(),self.mail_topic)
        return total_received_mail_nums_after
    def non_test_126_login(self):
        self.login()
        driver=self.driver
        login_title=driver.title
        #print driver.title
        #assert title
        self.assertEqual(login_title,u"126网易免费邮--你的专业电子邮局")
        #assert username after login
        username=driver.find_element_by_id("spnUid").text
        self.assertEqual(username,self.mail_from)

    def non_test_sendmail_normal(self):
        """
        send mail normal fow
        verify received mail
        verify status mail
        verify sender mail
        """
        self.login()
        #before test,total received mails nums
        total_received_mail_nums_before=self.total_received_mails()
        #send mail
        self.sendmail()
        driver=self.driver
        #click send mail button
        driver.find_element_by_css_selector("footer.jp0 div span.nui-btn-text").click()
        
        #logout
        driver.quit()
        time.sleep(10)
        
        #after send mail,total received mails nums               
        #assert received a new mail
        total_received_mail_nums_after=self.verify_mail()
        self.assertEqual(int(total_received_mail_nums_before),int(total_received_mail_nums_after)-1)

    def non_test_sendmail_attached(self):
        self.login()
        total_received_mail_nums_before=self.total_received_mails()
        self.sendmail()  
        driver=self.driver
        #add attached
        driver.find_element_by_css_selector("div[id*='attachBrowser']>input").send_keys("/Users/dongxiaobing/Documents/test_file")
        #click send mail button
        driver.find_element_by_css_selector("footer.jp0 div span.nui-btn-text").click()
        
        driver.quit()
        time.sleep(10)
        
        #after send mail,total received mails nums               
        #assert received a new mail
        total_received_mail_nums_after=self.verify_mail()
        self.assertEqual(int(total_received_mail_nums_before),int(total_received_mail_nums_after)-1)
    
    def non_test_sendmail_recipients(self):
        """
        send mail,input a word about recipients,and then click the popup recipients
        """
        self.login()
        total_received_mail_nums_before=self.total_received_mails()
        self.sendmail("yes")
        driver=self.driver
        #add attached
        driver.find_element_by_css_selector("div[id*='attachBrowser']>input").send_keys("/Users/dongxiaobing/Documents/test_file")
        #click send mail button
        driver.find_element_by_css_selector("footer.jp0 div span.nui-btn-text").click()
        
        driver.quit()
        time.sleep(10)
        #after send mail,total received mails nums               
        #assert received a new mail
        total_received_mail_nums_after=self.verify_mail()
        self.assertEqual(int(total_received_mail_nums_before),int(total_received_mail_nums_after)-1)
        
    def non_test_delemail(self):
        self.login()
        total_received_mail_nums_before=self.total_received_mails()
        driver=self.driver
        #find recevice box
        driver.find_element_by_css_selector("div>ul>li>div>span+span[class='nui-tree-item-text']").click()
#         time.sleep(5)
        #find the lastest unread mail and delete the mail
        try:
            checkbox_list=driver.find_elements_by_css_selector("span.nui-chk-symbol>b")
            #print checkbox_list
            checkbox_list.pop().click()
            driver.find_element_by_css_selector("div#dvContentContainer>div>div+div>header>div>div+div>div>span.nui-btn-text").click()
        except Exception,e:
            #print e
            print "there has no received mail"    
            time.sleep(5) 
            
        #assert deleted a mail
        driver.quit()
        time.sleep(5)
        self.login()
        total_received_mail_nums_after=self.total_received_mails()
        self.assertEqual(int(total_received_mail_nums_before),int(total_received_mail_nums_after)+1)
    def test_search_mail(self):
        self.login()
        #first send a mail to myself, and the search action could success
        self.sendmail() 
        driver=self.driver
        #click send mail button
        driver.find_element_by_css_selector("footer.jp0 div span.nui-btn-text").click()
#         time.sleep(5)
        
        #locate to search element,and input search content,and then submit
        driver.find_element_by_css_selector("div[id*='_mail_input']>label.nui-ipt-placeholder+input").send_keys(self.mail_topic,Keys.ENTER)
        
        #locate to all_checkbox,and click
        search_result=driver.find_elements_by_css_selector("label[sign='checkbox']>span.nui-chk-symbol>b")
        self.assertTrue(len(search_result)>=1)
        
        """
        #localte to delete button;eq(3) ----the four div
        #driver.find_element_by_css_selector("div#dvContainer>div:nth(4)>header>div>div:nth(1)>div>span").click()
        driver.find_element_by_css_selector("div#dvContainer div[id*='SearchModule']>header>div>div+div>div>span.nui-btn-text").click()
        
        #need delete twice
        try:
            driver.find_element_by_css_selector("div#dvContainer div[id*='SearchModule']>header>div>div+div>div>span.nui-btn-text").click()
        except Exception:
            pass
        #after delete mail,and then check the mails deleted
        print driver.find_elements_by_css_selector("div#dvContainer div[id*='SearchModule'] .rm1")
        time.sleep(5)
        """
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: 
            return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()