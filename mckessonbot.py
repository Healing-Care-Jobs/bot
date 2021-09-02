from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from bs4 import BeautifulSoup
import requests as req
import json
import html
import xml.sax.saxutils as saxutils
import re
import datetime as dt

class McKesson:
    def __init__(self, api):
        self.api = api
    def textToUrl(self, text):
        lb = text.replace(" ", "-")
        lb = re.sub('[^0-9a-zA-Z-]+', '', lb)
        return lb
    def textToUrlB(self, text):
        lb = text.replace(" ", "-")
        lb = text.replace(".", "")
        lb = re.sub('[^0-9a-zA-Z-]+', '-', lb)
        return lb
    def find_job_list(self):
        url = "https://mckesson.wd3.myworkdayjobs.com/External_Careers/3/refreshFacet/318c8bb6f553100021d223d9780d30be"
        # prepare the option for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'monikerList')))
        page_html = browser.page_source
        browser.quit()
        soup = BeautifulSoup(page_html, "lxml")
        p = soup.find_all('ul')[6]
        job_list = []
        fl = "https://mckesson.wd3.myworkdayjobs.com/en-US/External_Careers/job/"
        for sp in p.find_all('li'):
            jobTitle = sp.find("div", {"class":"gwt-Label"}).get("title", "no job")
            jobMetaString = sp.find("span", {"class":"gwt-InlineLabel"})
            # print(jobMetaString)
            if jobMetaString is not None:
                metaList = jobMetaString['title'].split("|")
                jobId = metaList[0].rstrip()
                loc_str = (metaList[1].rstrip()).replace(", More...", "")
                loc_str = loc_str.strip()
                location = loc_str + ", United states"
                full_url = fl + self.textToUrl(loc_str) + "/" + self.textToUrlB(jobTitle) + "_" + jobId
                # print(full_url)
                entry = {
                    "job_id" : jobId,
                    "title" : jobTitle,
                    "full_url" : full_url,
                    "location" : location
                }
                job_list.append(entry)
        return job_list
        
    def search_jobs(self):
        links_list = []
        try:
            links_list = self.find_job_list()
        except Exception as ex :
            print(ex)
            pass
        for link in links_list:
            self.scrap_single_job(link)
        # return id_list
    def scrap_single_job(self, dataset):
        # print(dataset)
        url = dataset.get("full_url")
        job_id = dataset.get("job_id")
        title = dataset.get("title")
        location = dataset.get("location")
        organization = "McKesson"
        # print('crawling', url)
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            browser = webdriver.Chrome(chrome_options=options)
            browser.get(url)
            WebDriverWait(browser,5).until(EC.presence_of_element_located((By.ID,'wd-PageContent-vbox')))
            page_html = browser.page_source
            browser.quit()
            soup = BeautifulSoup(page_html, "lxml")
            apply_link = str(soup.find('a', {"class" : "css-144l4qt"})['href'])
            if apply_link is None:
                return "no valid job"
            description = str(soup.find('div', {"id" : "richTextArea.jobPosting.jobDescription-input"}))
            description = description.replace("section ", "sectio ")
            req_body = {
                'title':title,
                'brief': title + ' at ' + organization,
                'description': description,
                'organization': organization,
                'location': location,
                'remote':0,
                'link': apply_link,
                'source': organization,
                'logo': 'https://mckesson.wd3.myworkdayjobs.com/External_Careers/assets/logo',
                'date_posted': "2/12/2021",
                'job_link': url,
                'ext_id':job_id,
                'primary_tag':self.textToUrlB(title),
                'is_visible': True,
                'show_logo': True,
                'sticky_week':False,
                'yellow_it':False
            }
            rtn = req.post(self.api + '/jobs/add', data=req_body,verify=False)
            print(rtn.text)
            return rtn.text
        except Exception as e:
            print(e)
            print('errored out. passing ' + url)
            pass

