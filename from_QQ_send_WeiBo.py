#coding: utf-8
#chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep

op = Options()
op.add_argument('user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')

dr = webdriver.Chrome(chrome_options=op)

dr.get('http://www.qq.com')
today_top_link = dr.find_element_by_css_selector('#todaytop a')
content = today_top_link.text
url = today_top_link.get_attribute('href')
print content
print url

dr.get('http://www.weibo.com')
sleep(2)

dr.find_element_by_css_selector('#v6_pl_content_publishertop .W_input').send_keys(content+url)
dr.find_element_by_css_selector('#v6_pl_content_publishertop .btn_30px').click()
sleep(2)
dr.close()
