# test bot
from kaiserbellbot import KaiserBell
api = 'https://healthcareokay.com:8443/api/v1'
mo = KaiserBell(api)
mo.search_jobs()