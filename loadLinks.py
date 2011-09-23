"""
Created on Mon Aug 22 22:57:23 2011

@author: antoanne
"""
import httplib
from BeautifulSoup import BeautifulSoup
import re

#http://www.englishexperts.com.br/2008/01/03/as-palavras-mais-comuns-da-lingua-inglesa/

#http://www.e-chords.com/browse/a
#http://www.e-chords.com/site/text-version.htm?p3=15746

SITE = "www.cifraclub.com.br/cifras"
PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
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
        # print("loading...")
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
            #print cls
            tagData = soup.findAll(tag, attrs={'id':cls})
            allTagData = []
            for d in tagData:
                allTagData.append(str(d))
            cifraData[cls.split("_")[1]] = allTagData
    return cifraData

def writeToDictFile(data, fileName):    
    f = open(PATH + re.findall('.*?([^/\'" >]+)', SITE)[0] + '.dictFile', 'a')
    f.write('%s\r\n' % str(data))
    f.close()
    
def readFromDictFile(fileName):
    f = open(PATH+fileName+'.dictFile','r')
    my_dict = eval(f.read())
    f.close()
    print "FROM FILE: ", my_dict['ai_musica']

def extractLink(soap):
    #urls = re.findall(r'href=[\'"]?([^\'" >]+)', html, re.I)
    for tag in soap.findAll('a', href=True):
        cifraLink = re.findall('.*?([^/\'" >]+)', SITE)[0] + tag['href']
        print "Cifra:", cifraLink
        writeToDictFile(loadCifra(cifraLink), cifraLink.rstrip("/").replace("/","_"))
        #readFromDictFile(cifraLink.rstrip("/").replace("/","_"))

def loadData(local, tag, cls):
    soup = BeautifulSoup(local)
    tagData = soup.findAll(tag, attrs={'class':cls})
    for d in tagData:
        extractLink(d)

def loadHomeMusicList(local, dic):
    for item in dic:
        tag = item['tag']
        for cls in item['classes']:
            try:
                loadData(local, tag, cls)
            except:
                print "Erro: %s" % local
            #break

local = req(SITE)
loadHomeMusicList(local, classList)