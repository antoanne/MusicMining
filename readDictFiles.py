# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 18:50:05 2011

@author: antoanne
"""
import plots as plots
from BeautifulSoup import BeautifulStoneSoup
from sqlite3 import dbapi2 as sqlite
import re

#tablatura [A-Z]\|[-|a-zA-Z0-9*]*[\|]
#html tags (?is)<.*?>
#re.split('\W+', 'Words, words, words.')
#re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE)


PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
FILE = "www.cifraclub.com.br"
DBFile = "cifraclub.db"
tons = {}

def createDB(dbfile):
    con=sqlite.connect(PATH+dbfile)    
    con.execute('create table if not exists musica(musica,artista,tom,cifra,letra)')

#def insertMusic(dbfile, d):
    #con=sqlite.connect(PATH+dbfile)
    #print d['cifra']
    #con.execute("insert into musica (musica,artista,tom,cifra) values ('%s','%s','%s','" + str(d['cifra']) + "')" % (d['musica'],d['artista'],d['tom']))

def extractCifras(cifra):
    letraLimpa = str(cifra)
    letraLimpa = re.subn(r'[A-Z]\|[-|a-zA-Z0-9*]*[\|]','',str(letraLimpa))
    letraLimpa = re.subn(r'<.*?>[a-zA-Z]</.*?>|</.*>|\\r\\n','',str(letraLimpa))
    #TODO: separar as letras usando re também
    print str(letraLimpa)
    cifras = cifra.findAll('b')
    cifrasList = []
    for c in cifras:
        cifrasList.append(c.string)
    return cifrasList

def acumulaTons(tom):
    if (tom in tons.keys()):
        tons[tom] += 1
    else:
        tons[tom] = 1

def cleanFromCifraClub(key, data):
    cleanedData = ""
    soup = BeautifulStoneSoup(unicode(data))
    if (key == 'musica'):
        return soup.h1.string
    elif (key == 'tom'):
        return soup.a.string
    elif (key == 'artista'):
        return soup.a.string
    elif (key == 'cifra'):
        return extractCifras(soup)
        #if (soup.pre.string != None):
        #    return soup.pre.string
        #else:
        #    return soup.pre.contents
    else:
        print "Key desconhecida:%s" % key
        return ""
    return cleanedData

def cleanDictData(d):
    cleanedDict = {}
    for k in d.keys():
        cleanedDict[k] = cleanFromCifraClub(k,d[k][0])
    #insertMusic(DBFile, cleanedDict)
    print "%s, %s" % (cleanedDict['musica'], cleanedDict['artista'])
    #print cleanedDict['cifra']
    acumulaTons(cleanedDict['tom'])
    return cleanedDict

def readFromDictFile(fileName):
    f = open(PATH+fileName+'.dictFile','r')
    c = open(PATH+fileName+'.cleaned.dictFile','w')
    for line in f:
        c.write(str(cleanDictData(eval(line))) + '\r\n')
        break
    c.close()
    f.close()
   
def readForTest(fileName):
    f = open(PATH+fileName+'.dictFile','r')
    for line in f:
        cleanDictData(eval(line))
        #break
    f.close()
    
#createDB(DBFile)
readFromDictFile(FILE)
#readForTest(FILE)
try:
    tons.pop(None)
except:
    pass
#plots.constructQTDPlot(tons)