import urllib2
from bs4 import BeautifulSoup
from time import sleep
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')


hasil=[]
for n in range(1926,2018,1):
    preurl = 'http://filmindonesia.or.id/movie/title/list/year/'+str(n)
    w = urllib2.urlopen(urllib2.Request(preurl, None, headers)).read()
    ds = BeautifulSoup(w)
    print "proses tahun "+str(n)+"....."
    try :
       for k in range(0,int(ds.find('div', {'class':'pagination'}).find_all('li')[-1].find('a',href=True).attrs['href'].split('/')[-1])+10,10) :
            req = urllib2.Request(preurl+'/'+str(k), None, headers)
            dres = urllib2.urlopen(req)
            dhtml = dres.read()
            dsoup = BeautifulSoup(dhtml)
            for i in dsoup.find_all('h3', {'class':'content-lead'}) :
                print i.find('a', href=True).text
                l = {}
                l['judul'] = i.find('a', href=True).text
                l['url'] = i.find('a', href=True).attrs['href']
                r = BeautifulSoup(urllib2.urlopen(urllib2.Request(l['url'], None, headers)).read())
                l['Tahun']= r.find('div',{'class':'movie-meta-info'}).text.split("::")[0] if r.find('div',{'class':'movie-meta-info'}).text.split("::")[0] else "NA"
                l['Genre']= r.find('div',{'class':'movie-meta-info'}).text.split("::")[1] if len(r.find('div',{'class':'movie-meta-info'}).text.split("::")) > 1 else "NA"
                l['Sutradara'] = r.find('span',{'itemprop':'director'}).text if r.find('span',{'itemprop':'director'}) else "NA"
                hasil.append(l)
    except :
        for i in ds.find_all('h3', {'class':'content-lead'}) :
            print i.find('a', href=True).text
            l = {}
            l['judul'] = i.find('a', href=True).text
            l['url'] = i.find('a', href=True).attrs['href']
            r = BeautifulSoup(urllib2.urlopen(urllib2.Request(l['url'], None, headers)).read())
            l['Tahun']= r.find('div',{'class':'movie-meta-info'}).text.split("::")[0] if r.find('div',{'class':'movie-meta-info'}).text.split("::")[0] else "NA"
            l['Genre']= r.find('div',{'class':'movie-meta-info'}).text.split("::")[1] if len(r.find('div',{'class':'movie-meta-info'}).text.split("::")) >1 else "NA"
            l['Sutradara'] = r.find('span',{'itemprop':'director'}).text if r.find('span',{'itemprop':'director'}) else "NA"
            hasil.append(l)

keys = hasil[0].keys()
with open('filmindonesia.csv', 'wb') as o_f:
    d_w = csv.DictWriter(o_f, keys)
    d_w.writeheader()
    d_w.writerows(hasil)