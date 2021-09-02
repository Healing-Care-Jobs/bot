
# test bot
from bscortbot import BaylorScottWhite
api = 'https://healthcareokay.com:8443/api/v1'
bsw = BaylorScottWhite(api)
bsw.search_jobs()