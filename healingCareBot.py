#!/home/dietpi/Temp/.env/bin/python3
api = 'https://healingcarejobs.com:8443/api/v1'
# try:
#1
from bscortbot import BaylorScottWhite
bsw = BaylorScottWhite(api)
bsw.search_jobs()
#2
from cignabot import CignaJobs
cigna = CignaJobs(api)
cigna.search_jobs()
#3
from goodrxbot import GoodRx
gr = GoodRx(api)
gr.search_jobs()
#4
from headspacebot import HeadSpace
hs = HeadSpace(api)
hs.search_jobs()
#5
from kaiseranaheimbot import KaiserAnah
mo = KaiserAnah(api)
mo.search_jobs()
#6
from kaiserbellbot import KaiserBell
mo = KaiserBell(api)
mo.search_jobs()
#7
from mckessonbot import McKesson
mo = McKesson(api)
mo.search_jobs()
#8
from medelybot import Medely
md = Medely(api)
md.search_jobs()
#9
from morinacalifbot import MorinaCa
mo = MorinaCa(api)
mo.search_jobs()
#10
from morinatexasbot import MorinaTx
mo = MorinaTx(api)
mo.search_jobs()
#11
from ritualbot import Ritual
r = Ritual(api)
r.search_jobs()
# except Exception as err :
#     print('error occured', err)
#     pass