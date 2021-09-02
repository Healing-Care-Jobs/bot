import requests as req
from bs4 import BeautifulSoup
import json
import html
import xml.sax.saxutils as saxutils
import random

class MorinaTx:
    def __init__(self, api):
        self.api = api
    def find_url(self):
        return 'https://careers.molinahealthcare.com/search-jobs/?alt=3&alp=6252001-5815135alt=3&alp=6252001-5332921alt=3&alp=6252001-4736286alt=3&alp=6252001-5332921alt=3&alp=6252001-4736286alt=3&alp=6252001-5332921alt=3&alp=6252001-5332921alt=3&alp=6252001-4736286'
    def rand_sticky_week(self):
        l = [True,False,False,False,False,False,True, False,False,False,False,False,False,True]
        return random.choice(l)
    def find_job_list(self):
        url = self.find_url()
        page_html = req.get(url,verify=False)
        soup = BeautifulSoup(page_html.content, "lxml")
        p = soup.find_all('ul')[11]
        summary = []
        for li in p.findAll('li'):
            link = 'https://careers.molinahealthcare.com' + li.find('a', href=True)['href']
            jobid = link.split('/')[-1]
            title = li.find('h2').text
            organization = li.find("span", { "class" : "job-location"}).text
            lc = li.findAll("span")[1]
            foo = str(lc.find_next("b"))
            foo = foo.replace('<b>', '')
            location = foo.replace('</b>', '')
            if 'Enter number to jump' in location:
                location = 'Long Beach, California'
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
        id_list = []
        try:
            id_list = self.find_job_list()
        except:
            print('that id did not work. no new job IDs found')
            pass
        for id in id_list:
            self.scrap_single_job(id['url'], id)
        # return id_list
    def scrap_single_job(self, url, meta):
        print('crawling', url)        
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
                'logo': 'https://media.glassdoor.com/sql/15828/molina-healthcare-squarelogo-1483641096661.png',
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

