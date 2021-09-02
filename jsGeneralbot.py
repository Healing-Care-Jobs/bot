from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from bs4 import BeautifulSoup
import json
import html
import xml.sax.saxutils as saxutils
import re

url = "https://mckesson.wd3.myworkdayjobs.com/en-US/External_Careers/job/DallasFort-Worth-Metro/Sr-Director-Talent-Strategy-and-Programs_JR0041405"

options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome()
browser.get(url)
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'wd-PageContent-vbox')))
page_html = browser.page_source
browser.quit()
soup = BeautifulSoup(page_html, "lxml")
description = str(soup.find('div', {"id" : "richTextArea.jobPosting.jobDescription-input"}))
apply_link = str(soup.find('a', {"class" : "css-144l4qt"})['href'])
print(apply_link)









# driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
# driver.get(url)
# sleep(10)
# innerHTML = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
# print(innerHTML)
# html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
# data = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
# print(html)