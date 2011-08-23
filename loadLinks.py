# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 22:57:23 2011

@author: antoanne
"""
import httplib, xml.dom.minidom
from BeautifulSoup import BeautifulSoup
import re

def req(url):
    adress = url.replace("http://", "").split("/")
    conn = httplib.HTTPConnection(adress[0])
    conn.request("GET", "/"+"/".join(adress[1:])) # /cavaco
    r1 = conn.getresponse()
    if (r1.status == 301):
        # redirected
        print("redirect...")
        return req(r1.msg.dict['location'])
    elif (r1.status == 404):
        # fora do ar
        return None
    elif (r1.status == 200):
        # OK
        print("loading...")
        return r1.read()
    else:
        print "erro..."
    
dados = req("www.cifraclub.com.br/cifras")
soup = BeautifulSoup(dados)

c = 0
liData = soup.findAll('li', attrs={'class':'img li1'})
for li in liData:
    print li, '\n'
    c+=1

liData = soup.findAll('li', attrs={'class':'img li2'})
for li in liData:
    print li, '\n'
    c+=1

liData = soup.findAll('li', attrs={'class':'img li3'})
for li in liData:
    print li, '\n'
    c+=1

liData = soup.findAll('li', attrs={'class':'img li4'})
for li in liData:
    print li, '\n'
    c+=1

liData = soup.findAll('li', attrs={'class':'img '})
for li in liData:
    print li, '\n'
    c+=1

liData = soup.findAll('li', attrs={'class':''})
for li in liData:
    print li, '\n'
    c+=1

liData = soup.findAll('li', attrs={'class':'fix3 '})
for li in liData:
    print li, '\n'
    c+=1

liData = soup.findAll('li', attrs={'class':'fix4 '})
for li in liData:
    print li, '\n'
    c+=1

print c

divData = liData[0].findAll('div')

olStrong = olData[0].findAll('strong')
for link in olStrong:
    olLink = link.findAll('a')
    print olLink, '\n'
#soup = BeautifulSoup(olData[0])
