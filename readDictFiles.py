# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 18:50:05 2011

@author: antoanne
"""
import plots as plots
from BeautifulSoup import BeautifulStoneSoup
from sqlite3 import dbapi2 as sqlite
import re, sys

#POS = "B"
if len(sys.argv) < 2:
    sys.exit('Usage: %s <letra[A-Z]>' % sys.argv[0])
POS = sys.argv[1].upper()

#tablatura [A-Z]\|[-|a-zA-Z0-9*]*[\|]
#html tags (?is)<.*?>
#re.split('\W+', 'Words, words, words.')
#re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE)


PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
FILE = "www.cifraclub.com.br"
DBFile = "cifraclub.db"
tons = {}

#def createDB(dbfile):
#    con=sqlite.connect(PATH+dbfile)    
#    con.execute('create table if not exists musica(musica,artista,tom,cifra,letra)')

#def insertMusic(dbfile, d):
#    con=sqlite.connect(PATH+dbfile)
#    print d['cifra']
#    con.execute("insert into musica (musica,artista,tom,cifra) values ('%s','%s','%s','" + str(d['cifra']) + "')" % (d['musica'],d['artista'],d['tom']))

#def uniqueList(seq):
#    set = {}
#    map(set.__setitem__, seq, [])
#    return set.keys()

def extractWords(cifra):
    letraLimpa = cifra
    letraLimpa = unicode(cifra).encode('utf-8')
    letraLimpa = re.subn(r'(Refrão(:?))|(.*\ parte\:)|(Solo:)|(Intro:)|\(|\)','',letraLimpa)
    letraLimpa = re.subn(r'[A-G]\|.*\||.*x','',letraLimpa[0])
    letraLimpa = re.subn(r'[A-Z]\|[-|a-zA-Z0-9*]*[\|]','',letraLimpa[0])
    letraLimpa = re.subn(r'<.*?>.*?</.*?>|</.*>|<.*>','',letraLimpa[0]) 
    letraLimpa = re.subn(r',.|\r|\n',' ',letraLimpa[0]) 
    letraLimpa = letraLimpa[0].split(' ')
    palavrasList = []
    for p in letraLimpa:
        if (p != ''):
            palavrasList.append(unicode(p))
    return palavrasList

def extractCifras(cifra):
    cifras = cifra.findAll('b')
    cifrasList = []
    for c in cifras:
        cifrasList.append(c.string)
    return cifrasList

def acumulaTons(tom):
    if (tom != ""):
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
        cifras = extractCifras(soup)
        if (len(cifras) == 0):
            print cifras
            #raise
        return cifras
    elif (key == 'letra'):
        return extractWords(soup)
    else:
        print "Chave desconhecida:%s" % key
    return cleanedData

def cleanDictData(d):
    cleanedDict = {}
    for k in d.keys():
        cleanedDict[k] = cleanFromCifraClub(k,d[k][0])
    cleanedDict['letra'] = cleanFromCifraClub('letra',d['cifra'][0])
    print "%s, %s" % (cleanedDict['musica'], cleanedDict['artista'])
    acumulaTons(cleanedDict['tom'])
    return cleanedDict

def readFromDictFile(fileName):
    f = open(PATH+fileName+'_'+ POS +'.dictFile','r')
    c = open(PATH+fileName+'_'+ POS +'.cleaned.dictFile','w')
    for line in f:
        print "_______________________________________________"
        try:
            line = line.replace('"','')
            c.write(str(cleanDictData(eval(line))) + '\r\n')
        except:
            #break
            print "ERROR"
    c.close()
    f.close()

def readForTest(fileName):
    f = open(PATH+fileName+'_'+ POS +'.dictFile','r')
    for line in f:
        cleanDictData(eval(line))
        break
    f.close()
    
#createDB(DBFile)
readFromDictFile(FILE)
#readForTest(FILE)
try:
    tons.pop(None)
except:
    pass
plots.constructQTDPlot(tons)