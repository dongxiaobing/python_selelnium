#coding=utf-8
import sys   
import urllib2
import re
import time
reload(sys)  
sys.setdefaultencoding('utf8')  
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import unittest
#import HomePage
#import SearchPage
import ConfigParser
import json
def configparse_test_data():
    """
    parse test data from configure file
    """
    conf = ConfigParser.ConfigParser()
    conf.read("testdata.conf")
    return conf.get("testdata","pub1")
    #for i in conf.items("testdata"):
    #    print i
    """
    conf = ConfigParser.ConfigParser()
    conf.read("testdata.conf")
    search_words= conf.get("testdata", loc)
    return search_words
    """
def get_suggest_elements_list(dr):
    """
    input search words
    get suggest elements list
    """
    #find suggest list elements
    search_total_num_from_suggest_list_loc=(By.CSS_SELECTOR,"ul#__suggest_keyword li span.d")
    suggest_elements_list=dr.find_elements(*search_total_num_from_suggest_list_loc)
    return suggest_elements_list
    #print suggest_element_list
    #suggest_elements_list_length=len(suggest_elements_list)
    #return suggest_elements_list_length
def get_search_content_from_suggest_list(dr):
    elements_list=dr.find_elements(By.CSS_SELECTOR,"ul#__suggest_keyword li div>div")
    search_content_list=[]
    #f=open("search_content.txt","w")
    for i in elements_list:
        content=i.get_attribute("title")
        if content:
            print "[%s]" % content,
def get_search_total_nums_from_suggest_list(dr):
        """
        get all search total nums from suggest list,and the save those info to a local file
        """
        elements_list=dr.find_elements(By.CSS_SELECTOR,"#__suggest_keyword span.d")
        elements_list_leng=len(elements_list)
     
        total_nums_list_from_suggest_list=[]
        for i in range(elements_list_leng):
            result=elements_list[i].text
            #print result
            l=[]
            for i in result:
                if i.isdigit():
                    l.append(i)
                    result_str=''.join(l)
            
            total_nums_list_from_suggest_list.append(result_str)
        return total_nums_list_from_suggest_list        
def get_searchNum_and_currentUrl_from_searchPage(dr):
    search_num_from_searchPage=dr.find_element(By.CSS_SELECTOR,".sp.total>.b").text
    CurrentUrl=dr.current_url
    return search_num_from_searchPage,CurrentUrl
def get_searchNum_from_backEnd(CurrentUrl):
    key_value=CurrentUrl.split("=")[1]
    #get backend url
    base_url="http://10.255.254.188:8390/?st=full&um=search_ranking&q="
    backend_url=base_url+key_value
    #access backend url,and then get the contens
    #print backend_url
    try:
        u=urllib2.urlopen(backend_url)
    except urllib2.URLError:
        print "backend url coule not be open"
    else:
        contents=u.read()
    finally:
        u.close()
    #get total num from xml
    pattern = re.compile(r'TotalCnt>(\d+).*TotalCnt')
    search_num_from_backEnd=pattern.findall(contents)[0] 
    return search_num_from_backEnd
def get_searchTotalNum_from_searchPage_and_backEnd(dr,suggest_elements_list,search_words):
    search_list_from_searchPage=[]
    search_list_from_backEnd=[]
    for i in range(len(suggest_elements_list)):
        dr.find_element(By.ID,"key_S").clear()
        dr.find_element(By.ID,"key_S").send_keys(search_words)
        #print "#"
        elements_list=dr.find_elements(By.CSS_SELECTOR,"#__suggest_keyword span.d")
        #search_total_num_from_suggest_list_loc=(By.CSS_SELECTOR,"ul#__suggest_keyword li span.d")
        #elements_list=dr.find_elements(search_total_num_from_suggest_list_loc)
        elements_list[i].click()
        search_num_from_searchPage,CurrentUrl=get_searchNum_and_currentUrl_from_searchPage(dr)
        #print CurrentUrl
        search_list_from_searchPage.append(search_num_from_searchPage)
        dr.back()
        dr.find_element(By.ID,"key_S").send_keys(search_words)
        #time.sleep(3)    
        search_num_from_backEnd=get_searchNum_from_backEnd(CurrentUrl)
        search_list_from_backEnd.append(search_num_from_backEnd)
    return search_list_from_searchPage,search_list_from_backEnd
def main(search_words):
    base_url = "http://www.dangdang.com"
    key_loc=(By.ID,"key_S")
    dr = webdriver.Firefox()
    dr.implicitly_wait(30)
    dr.get(base_url)
    #search_words=configparse_test_data("pub2")
    search_words=json.loads(search_words)
    #input search words
    print "#################################"
    print "搜索-------%s" % search_words
    dr.find_element(By.ID,"key_S").send_keys(search_words)
    suggest_elements_list=get_suggest_elements_list(dr)
    if len(suggest_elements_list)==0:
        print "该搜索词的建议列表为空，退出"
        dr.close()
        exit(0)  
    print "在建议列表中显示的搜索内容:"
    get_search_content_from_suggest_list(dr)
    print "\n"
    search_list_from_suggest_list=get_search_total_nums_from_suggest_list(dr)
    search_list_from_searchPage,search_list_from_backEnd=get_searchTotalNum_from_searchPage_and_backEnd(dr,suggest_elements_list,search_words)
    dr.close()
    print "在建议列表中显示的各个结果的搜索总数:"
    print search_list_from_suggest_list
    print "在搜索结果界面显示的各个结果的搜索总数:"
    print search_list_from_searchPage
    print "通过后台服务端的api查询的各个结果的搜索总数:"
    print search_list_from_backEnd
    print "#################################"

if __name__=="__main__":
    conf = ConfigParser.ConfigParser()
    conf.read("testdata.conf")
    alls=conf.items("testdata")
    #print alls
    for i in alls:
        search_words=i[1]
        main(search_words)

    
