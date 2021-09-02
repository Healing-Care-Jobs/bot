# test bot
from cignabot import CignaJobs
api = 'https://healthcareokay.com:8443/api/v1'
cigna = CignaJobs(api)
cigna.search_jobs()