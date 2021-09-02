#!/home/healthcareokay/Temp/.env/bin/python3
from mckessonbot import McKesson
api = 'https://healthcareokay.com:8443/api/v1'
mo = McKesson(api)
mo.search_jobs()
