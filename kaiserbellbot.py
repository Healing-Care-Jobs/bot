import requests as req
from bs4 import BeautifulSoup
import json
import html
import xml.sax.saxutils as saxutils
import random

class KaiserBell:
    def __init__(self, api):
        self.api = api
    def find_url(self, page):
        return 'https://www.kaiserpermanentejobs.org//search-jobs/?k=Bellevue&p=' + str(page)
    def all_pages(self):
        return [1,2,3,4,5,6]
    def rand_sticky_week(self):
        l = [True,False,False,False,False,False,True, False,False,False,False,False,False,True]
        return random.choice(l)
    def find_job_list(self, page):
        url = self.find_url(page)
        page_html = req.get(url,verify=False)
        soup = BeautifulSoup(page_html.content, "lxml")
        p = soup.find_all('ul')[18]
        # print(p)
        # exit()
        summary = []
        for li in p.findAll('li'):
            link = 'https://www.kaiserpermanentejobs.org' + li.find('a', href=True)['href']
            jobid = link.split('/')[-1]
            title = li.find('h2').text
            organization = 'kaiser permanente'
            location = li.find("span", { "class" : "job-location"}).text
            date = li.find('span', { "class": "job-date-posted"}).text
            df = {
                'jobid': jobid,
                'url': link,
                'title': title,
                'org':organization,
                'location':location,
                'posted': date
            }
            summary.append(df)
        return summary
    def search_jobs(self):
        for page in self.all_pages():
            print('current page: ', page)
            id_list = []
            try:
                id_list = self.find_job_list(page)
            except:
                print('that id did not work. no new job IDs found')
                pass
            for meta in id_list:
                self.scrap_single_job(meta['url'], meta, str(page))
        # return id_list
    def scrap_single_job(self, url, meta, page):
        print('crawling page ' + page + ' url:', url)        
        try:
            page_html = req.get(url,verify=False)
            soup = BeautifulSoup(page_html.content, "lxml")
            p = soup.find('section', {'class':'job-description'})
            pp = p.find('div', {'class':'jd-buttons'})
            link = pp.find('a', href=True)['href']
            description = p.find('div', {'class':'ats-description'})
            # print(description)
            random_val = self.rand_sticky_week()
            req_body = {
                'title':meta['title'],
                'brief': meta['title'] + ' at ' + meta['org'],
                'description': str(description),
                'organization': meta['org'],
                'location': meta['location'] + ' United States',
                'remote':0,
                'link': link,
                'source': meta['org'],
                'logo': 'https://www.mountainfamily.org/wp-content/uploads/2018/11/Kaiser-Permanent-logo.jpg',
                'date_posted': meta['posted'],
                'job_link': url,
                'ext_id':meta['jobid'],
                'primary_tag':meta['title'],
                'created_at': meta['posted'],
                'is_visible': True,
                'show_logo': True,
                'sticky_week':random_val,
                'yellow_it':random_val
            }
            rtn = req.post(self.api + '/jobs/add', data=req_body,verify=False)
            print(rtn.text)
            return rtn.text
        except:
            print('errored out. passing ' + url)
            pass

