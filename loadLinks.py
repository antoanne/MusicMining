# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 22:57:23 2011

@author: antoanne
"""
import httplib
from BeautifulSoup import BeautifulSoup
import re

SITE = "www.cifraclub.com.br/cifras"
classList = [{'tag' : 'li',
             'classes': ['img li1',
                         'img li2',
                         'img li3',
                         'img li4',
                         'img ',
                         '',
                         'fix3 ',
                         'fix4 '], 
            },]

classCifra = [{'tag':'h1',
               'id':['ai_musica']},
              {'tag':'h2',
               'id':['ai_artista']},
              {'tag':'pre',
               'id':['ct_tom', 'ct_cifra']},
             ]
             
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

def loadCifra(local):
    cifra = req(local)
    soup = BeautifulSoup(cifra)
    for item in classCifra:
        tag = item['tag']
        for cls in item['id']:
            print cls
            tagData = soup.findAll(tag, attrs={'id':cls})
            for d in tagData:
                print d

def extractLink(soap):
    #urls = re.findall(r'href=[\'"]?([^\'" >]+)', html, re.I)
    for tag in soap.findAll('a', href=True):
        cifraLink = re.findall('.*?([^/\'" >]+)', SITE)[0] + tag['href']
        print cifraLink
        loadCifra(cifraLink)

def loadData(local, tag, cls):
    soup = BeautifulSoup(local)
    tagData = soup.findAll(tag, attrs={'class':cls})
    for d in tagData:
        extractLink(d)

def loadHomeMusicList(local, dic):
    for item in dic:
        tag = item['tag']
        for cls in item['classes']:
            loadData(local, tag, cls)
            break

local = req(SITE)
loadHomeMusicList(local, classList)