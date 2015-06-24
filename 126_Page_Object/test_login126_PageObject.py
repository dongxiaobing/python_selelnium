#!/bin/python

#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By 
from time import sleep
import LoginPage
import HomePage
import unittest

class TestLoginPageObject(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        
        self.driver = webdriver.Firefox()
        self.username = 'dxbselenium'
        self.password = 'dxb123456'
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        
    def test_user_login(self):
        login_page = LoginPage.LoginPage(self.driver)
        login_page.open()
        login_page.type_username(self.username) 
        login_page.type_password(self.password)
        homepage=login_page.submit()
        homepage.is_presence()
        username_title=homepage.find_username_title()
        self.assertIn(self.username,username_title)
        
if __name__ == "__main__":
    unittest.main()
    