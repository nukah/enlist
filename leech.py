from BeautifulSoup import BeautifulSoup
from pymongo import Connection
import urllib2, re
import time
from datetime import datetime, timedelta, tzinfo

class MSK(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours = 3)
    def tzname(self, dt):
        return "GMT + 3"
    def dst(self, dt):
        return timedelta(0)

MSK = MSK()

c = Connection('localhost')
db = c.notik
q = db['notebooks']

url = r'http://www.notik.ru/search_catalog/filter/New.htm'

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
page = opener.open(url)
content = BeautifulSoup(page)
price_pattern = re.compile('(\d*)&nbsp;(\d*)&nbsp;')
hard_pattern = re.compile('(\d*)')

list = content.find('ul', 'resultNotesList').findAll('li')
for item in list:
    name = item.find('h3').string
    notebook = q.find_one({'name' : name})
    if not notebook:
        new = {
               "name" : name,
               "added" : datetime.now(MSK).strftime('[ %d/%m/%Y ] -> %H:%M:%S'),
               "weight" : item.find('div', 'noteTable').find('div', 'paramsDiv1').findAll('div')[1].find('span').string
        }
        complectations = []
        compList = item.findAll('tr', 'noteComplectation')

        for comp in compList:
            complect = {}
            complect['name'] = ''.join(comp.find('td', 'cell1').findAll('div')[1].findAll('strong')[1].string.split('.'))
            complect['processor_type'] = comp.find('td', 'cell2').find('strong').string
            complect['processor_speed'] = comp.find('td', 'cell2').find('strong').nextSibling.nextSibling.split()[0]
            complect['memory_amount'] = ''.join(hard_pattern.search(comp.find('td', 'cell3').find('strong').string).group(1))
            complect['harddrive'] = hard_pattern.search(comp.find('td', 'cell4').find('strong').string).group(0)
            complect['videocard'] = comp.find('td', 'cell6').find('strong').string
            complect['screensize'] = comp.find('td', 'cell8').find('strong').string
            complect['price'] = ''.join(price_pattern.search(comp.find('td', 'cell10').find('span').string).groups())
            complectations.append(complect)
        new['complectations'] = complectations
        q.insert(new)
