import requests as req
from bs4 import BeautifulSoup
import json
import html
import xml.sax.saxutils as saxutils
import re

url = "https://mckesson.wd3.myworkdayjobs.com/External_Careers/3/refreshFacet/318c8bb6f553100021d223d9780d30be"

page_html = req.get(url,verify=False)
# print(page_html)
soup = BeautifulSoup(page_html.content, "lxml")
p = soup.find('div', {"class":"WGTO"})
print(p)
exit()

head = p.find('div', {"class":"posting-headline"})
job_id = url.split("/")[-1]
organization = "GoodRx"
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
print(description)
job_list = []

# print(len(job_list))
exit()
# p = soup.find("section", { "id" : "search-results-list"})
# print(p)
# p = soup.find_all('script')[1] #critical point!!!!!
# p = p.find_all(text=True)
# p = saxutils.unescape(str(p))
# p = p.split('};')[1]
# p = p + '}'
# p = p[p.find('{'):]
# p = p.replace("\\'", "")
# p = json.loads(p)
# #jobs
# p = p['eagerLoadRefineSearch']['data']['jobs']
# job_ids = []
# for j in p:
#     job_ids.append(j['jobId'])
# print(job_ids)

exit()
#single job page
url = "https://jobs.cigna.com/us/en/job/20013903/Application-Development-Advisor"
page_html = req.get(url)
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
f = open('soup.txt', 'w')
f.write(str(p))
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
    'created_at': dateposted
}
rtn = req.post('http://127.0.0.1:8000/api/v1/jobs/add', data=req_body)
print(rtn.text)