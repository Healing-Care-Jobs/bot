import requests as req
from bs4 import BeautifulSoup
import json
import html
import xml.sax.saxutils as saxutils
import random

class CignaJobs:
    def __init__(self, api):
        self.api = api
    def find_from(self):
        endpoint = self.api + '/jobs/cigna/from'
        res = req.get(endpoint,verify=False)
        return json.loads(res.text)['cigna_from']
    def rand_sticky_week(self):
        l = [False,False,False,False,False,True, False,False,False,False,False,False]
        return random.choice(l)
    def update_from(self, cigna_from):
        endpoint = self.api + '/jobs/cigna/from'
        res = req.post(endpoint, data={'cigna_from': cigna_from},verify=False)
        return json.loads(res.text)
    def get_current_pg_jobs(self, url):
        page_html = req.get(url,verify=False)
        soup = BeautifulSoup(page_html.content, "lxml")
        p = soup.find_all('script')[1] #critical point!!!!!
        p = p.find_all(text=True)
        p = saxutils.unescape(str(p))
        p = p.split('};')[1]
        p = p + '}'
        p = p[p.find('{'):]
        p = p.replace("\\'", "")
        p = p.replace('\\xa0', '')
        p = json.loads(p)
        #jobs
        p = p['eagerLoadRefineSearch']['data']['jobs']
        job_ids = []
        for j in p:
            job_ids.append(j['jobId'])
        return job_ids
    def search_jobs(self):
        s_from = self.find_from()
        search_url = 'https://jobs.cigna.com/us/en/search-results?s=1'
        if s_from > 0:
            search_url = 'https://jobs.cigna.com/us/en/search-results?from=' + str(s_from) + '&s=1'
        current_pg_jobs = self.get_current_pg_jobs(search_url)
        if len(current_pg_jobs) == 0:
            self.update_from(0)
            return
        url = "https://jobs.cigna.com/us/en/job/"
        new_s_from = s_from + 10
        for idx, jobid in enumerate(current_pg_jobs):
            self.scrap_single_job(url + jobid)
            if idx + 1 == len(current_pg_jobs):
                self.update_from(new_s_from)
        return True
    def scrap_single_job(self, url):
        print('crawling', url)
        try:
            page_html = req.get(url,verify=False)
            soup = BeautifulSoup(page_html.content, "lxml")
            p = soup.find_all('script')[1]
            p = p.find_all(text=True)
            p = saxutils.unescape(str(p))
            p = p.replace("\\\\", "\\")
            p = p.replace("\\'", "")
            p = p.replace('\\xa0', '')
            p = p[2:-2]
            p = json.loads(p)
            jobid = p['identifier']['value']
            # f = open('soup.txt', 'w')
            # f.write(str(p))
            title = p['title']
            brief = p['title']
            description = p['description']
            organization = p['hiringOrganization']['name']
            logo = p['hiringOrganization']['logo']
            joblink = p['hiringOrganization']['url']
            link = 'https://jobs.cigna.com/us/en/apply?jobSeqNo=CIGNUS' + jobid
            location = p['jobLocation']['address']['addressLocality'] + ', ' + p['jobLocation']['address']['addressRegion'] + ', ' +  p['jobLocation']['address']['addressCountry']
            dateposted = p['datePosted']
            source = organization
            random_val = self.rand_sticky_week()
            req_body = {
                'title':title,
                'brief': brief,
                'description': description,
                'organization': organization,
                'location': location,
                'remote':0,
                'link': link,
                'source': source,
                'logo': logo,
                'date_posted': dateposted,
                'job_link': joblink,
                'ext_id':jobid,
                'primary_tag':p['occupationalCategory'],
                'created_at': dateposted,
                'is_visible': True,
                'show_logo': True,
                'sticky_week':random_val,
                'yellow_it':random_val
            }
            rtn = req.post(self.api + '/jobs/add', data=req_body,verify=False)
            return rtn.text
        except:
            print('errored out. passing ' + url)
            pass

