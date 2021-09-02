# test bot
from goodrxbot import GoodRx
api = 'https://healthcareokay.com:8443/api/v1'
gr = GoodRx(api)
gr.search_jobs()
