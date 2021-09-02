import requests as req
from bs4 import BeautifulSoup
import json
import html
import xml.sax.saxutils as saxutils
import random
import re
import datetime as dt

class HeadSpace:
    def __init__(self, api):
        self.api = api
    def find_url(self):
        return
    def find_job_list(self):
        url = "https://jobs.lever.co/headspace/?"
        page_html = req.get(url,verify=False)
        soup = BeautifulSoup(page_html.content, "lxml")
        p = soup.find_all('div', {"class":"postings-group"})
        job_list = []
        for group in p:
            jobs = group.find_all('div', {"class":"posting"})
            for job in jobs:
                job_id_meta = job.find_all('a', attrs={'href': re.compile("^https://")})
                job_id_meta = job_id_meta[1]
                job_id = job_id_meta.get('href')
                job_list.append(job_id)
        return job_list
    def search_jobs(self):
        links_list = []
        try:
            links_list = self.find_job_list()
        except:
            print('that id did not work. no new job IDs found')
            pass
        for link in links_list:
            self.scrap_single_job(link)
        # return id_list
    def scrap_single_job(self, url):
        print('crawling', url)        
        try:
            page_html = req.get(url,verify=False)
            soup = BeautifulSoup(page_html.content, "lxml")
            p = soup.find('div', {"class":"posting-page"})
            head = p.find('div', {"class":"posting-headline"})
            job_id = url.split("/")[-1]
            organization = "Headspace"
            location = head.find('div', {"class":"sort-by-time"}).text
            location = location.replace("/", "")
            primary_tag = head.find('div', {"class":"sort-by-team"}).text
            primary_tag = primary_tag.replace("/", "")
            apply_link = p.find('a', {"class":"postings-btn"}, href=True).get('href')
            title = head.find('h2').text
            description_meta = p.find_all('div', {"class":"page-centered"})
            description = ""
            for section in description_meta[:-1]:
                description += str(section)
            description = description.replace("section ", "sectio ")
            req_body = {
                'title':title,
                'brief': title + ' at ' + organization,
                'description': description,
                'organization': organization,
                'location': location + ' United States',
                'remote':0,
                'link': apply_link,
                'source': organization,
                'logo': 'https://lever-client-logos.s3.us-west-2.amazonaws.com/46b59e6c-a01f-4c71-b402-e56beebee07c-1598992123604.png',
                'job_link': url,
                'ext_id':job_id,
                'primary_tag':primary_tag,
                'is_visible': True,
                'show_logo': True,
                'sticky_week':False,
                'yellow_it':False
            }
            rtn = req.post(self.api + '/jobs/add', data=req_body,verify=False)
            print(rtn.text)
            # exit()
            return rtn.text
        except Exception as e:
            print(e)
            print('errored out. passing ' + url)
            pass

