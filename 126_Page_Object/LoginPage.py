#coding=utf-8
import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from BasePage import BasePage
import HomePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class LoginPage(BasePage):
    url = ''
    username_loc = (By.ID,"idInput") 
    password_loc = (By.ID,"pwdInput") 
    submit_loc = (By.ID,"loginBtn")
    #username_title_loc = (By.ID,"spnUid")
    #Action
    def open(self):
       self._open(self.url)
    def type_username(self,username): 
        self.find_element(*self.username_loc).send_keys(username)
    def type_password(self,password): 
        self.find_element(*self.password_loc).send_keys(password)
    def submit(self): 
        self.find_element(*self.submit_loc).click()
        #WebDriverWait(self,10,0.5).until(EC.presence_of_element_located((By.ID,"spnUid")))
        return HomePage.HomePage(self)