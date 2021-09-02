# test bot
from morinatexasbot import MorinaTx
api = 'https://healthcareokay.com:8443/api/v1'
mo = MorinaTx(api)
mo.search_jobs()
