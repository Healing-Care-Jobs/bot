# test bot
from medelybot import Medely
api = 'https://healthcareokay.com:8443/api/v1'
md = Medely(api)
md.search_jobs()
