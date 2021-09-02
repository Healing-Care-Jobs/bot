# test bot
from kaiseranaheimbot import KaiserAnah
api = 'https://healthcareokay.com:8443/api/v1'
mo = KaiserAnah(api)
mo.search_jobs()