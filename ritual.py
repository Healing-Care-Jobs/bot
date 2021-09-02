# test bot
from ritualbot import Ritual
api = 'https://healthcareokay.com:8443/api/v1'
r = Ritual(api)
r.search_jobs()