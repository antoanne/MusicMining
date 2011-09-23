# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 18:50:05 2011

@author: antoanne
"""
import plots as plots
from BeautifulSoup import BeautifulStoneSoup

PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
FILE = "www.cifraclub.com.br"
tons = {}

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
        return soup.pre.contents
    else:
        print "Key desconhecida:%s" % key
        return ""
    return cleanedData

def cleanDictData(d):
    cleanedDict = {}
    for k in d.keys():
        cleanedDict[k] = cleanFromCifraClub(k,d[k][0])
    print "%s, %s" % (cleanedDict['musica'], cleanedDict['artista'])
    #print cleanedDict['cifra']
    acumulaTons(cleanedDict['tom'])
    return cleanedDict

def readFromDictFile(fileName):
    f = open(PATH+fileName+'.dictFile','r')
    c = open(PATH+fileName+'.cleaned.dictFile','w')
    for line in f:
        c.write(str(cleanDictData(eval(line))))
    c.close()
    f.close()
   
def readForTest(fileName):
    f = open(PATH+fileName+'.dictFile','r')
    for line in f:
        cleanDictData(eval(line))
        #break
    f.close()
    
readFromDictFile(FILE)
#readForTest(FILE)
try:
    tons.pop(None)
except:
    pass
plots.constructQTDPlot(tons)