#coding=utf-8
import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from BasePage import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class HomePage(BasePage):

    username_title_loc = (By.ID,"spnUid")
    def is_presence(self):
        WebDriverWait(self,10,0.5).until(EC.presence_of_element_located((By.ID,"spnUid")))
    def find_username_title(self): 
        return self.find_element(*self.username_title_loc).text