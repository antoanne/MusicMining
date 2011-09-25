# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 11:51:03 2011

@author: antoanne
"""
import httplib
from BeautifulSoup import BeautifulSoup
import re, sys

if len(sys.argv) < 2:
    sys.exit('Usage: %s <letra[A-Z]>' % sys.argv[0])

SITE = "www.cifraclub.com.br/cifras/letra_%s.htm" % sys.argv[1].lower()
PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
classListABC = [{'tag' : 'ul',
             'classes': ['lis1',
                         'lis2'], 
            },]

classListHotsite = [{'tag' : 'a',
             'classes': ['ac_ol_a'], 
            },]

classListMusic = [{'tag' : 'ol',
             'classes': ['ac_ol'], 
            },]

classCifra = [{'tag':'h1',
               'id':['ai_musica']},
              {'tag':'h2',
               'id':['ai_artista']},
              {'tag':'pre',
               'id':['ct_tom', 'ct_cifra']},
             ]

linksCarregados = []
             
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
        return r1.read()
    else:
        print "erro..."    

def loadCifra(local):
    cifra = req(local)
    soup = BeautifulSoup(cifra)
    cifraData = {}
    for item in classCifra:
        tag = item['tag']
        for cls in item['id']:
            tagData = soup.findAll(tag, attrs={'id':cls})
            allTagData = []
            for d in tagData:
                allTagData.append(str(d))
            cifraData[cls.split("_")[1]] = allTagData
    return cifraData

def writeToDictFile(data, fileName):    
    f = open(PATH + re.findall('.*?([^/\'" >]+)', SITE)[0] + '_' + sys.argv[1].upper() +'.dictFile', 'a')
    f.write('%s\r\n' % str(data))
    f.close()
    
def readFromDictFile(fileName):
    f = open(PATH+fileName+'.dictFile','r')
    my_dict = eval(f.read())
    f.close()
    print "FROM FILE: ", my_dict['ai_musica']

def extractLink(soap, hotsite=None):
    for tag in soap.findAll('a', href=True):
        if (len(tag['href'].split('#')) <= 1):
            if (hotsite):
                link = re.findall('.*?([^/\'" >]+)', SITE)[0] + "/" + hotsite + tag['href'].lstrip("/")                
                if (link not in linksCarregados):
                    print "HOTSITE:", link
                    writeToDictFile(loadCifra(link), link.rstrip("/").replace("/","_"))
                linksCarregados.append(link)
            else:
                link = re.findall('.*?([^/\'" >]+)', SITE)[0] + "/" + tag['href'].lstrip("/")
                print "SITE:", link
                loadHomeMusicList( req(link), classListMusic, tag['href'].lstrip("/") )

def loadData(local, tag, cls, hotsite=None):
    soup = BeautifulSoup(local)
    tagData = soup.findAll(tag, attrs={'class':cls})
    #print tag, cls, len(tagData)
    for d in tagData:
        extractLink(d, hotsite)

def loadHomeMusicList(local, dic, hotsite=None):
    for item in dic:
        tag = item['tag']
        for cls in item['classes']:
            try:
                loadData(local, tag, cls, hotsite)
            except:
                print "Erro ao ler o html"

loadHomeMusicList(req(SITE), classListABC)