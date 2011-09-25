# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 23:41:16 2011

@author: antoanne
"""
import plots as plots
from BeautifulSoup import BeautifulStoneSoup
from sqlite3 import dbapi2 as sqlite
import re, sys

PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
FILE = "www.cifraclub.com.br_%s.cleaned"

letras = map(chr, range(65, 91))

acords = {}
tons = {}

def acumulaTons(d, tons):
    if (d['tom'] != ""):
        if (d['tom'] in tons.keys()):
            tons[d['tom']] += 1
        else:
            tons[d['tom']] = 1

def acumulaAcordes(d, acords):
    if (len(d['cifra']) > 0):
        for c in d['cifra']:
            if (c in acords.keys()):
                acords[c] += 1
            else:
                acords[c] = 1

def wordleFile(fileName, d):
    f = open(PATH+fileName +'.wordle','w')
    for a in d:
        try:
            f.write("%s:%d\r\n" % (a,d[a]))
        except:
            pass
    f.close()

def readFromDictFile(fileName, tons, acords):
    f = open(PATH+fileName +'.dictFile','r')
    for line in f:
        try:
            acumulaTons(eval(line), tons)
            acumulaAcordes(eval(line), acords)
        except:
            print "ERROR on " + line
    f.close()

for l in letras:
    print "lendo %s..." % l
    try:
        readFromDictFile(FILE % l, tons, acords)
    except:
        pass
wordleFile('acordes', acords)