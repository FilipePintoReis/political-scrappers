import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import os

def ret_html():
    driver = webdriver.Chrome()
    driver.get('https://www.psd.pt/atualidade-agenda/')
    python_list_button = driver.find_elements_by_class_name("mec-load-more-button")

    while True:
        
        for x in range(0, len(python_list_button)):
            if python_list_button[x].get_attribute("class") == "mec-load-more-button mec-util-hidden": python_list_button.pop(x)
        
        if len(python_list_button) == 0: break
        
        if(python_list_button[0].get_attribute("class") != "mec-load-more-button mec-util-loading"):
            python_list_button[0].click()

        time.sleep(5)
        python_list_button = driver.find_elements_by_class_name("mec-load-more-button")
        
    to_be_ret = driver.find_element_by_id('ajax-content-wrap').get_attribute('innerHTML')
    driver.close()
    return to_be_ret