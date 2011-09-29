# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 23:41:16 2011

@author: antoanne
"""
import plots as plots
from plot import plot, subplot, title, ylabel, xlabel, grid, 
from BeautifulSoup import BeautifulStoneSoup
from sqlite3 import dbapi2 as sqlite
import re, sys
import mingus.core.notes as notes
from mingus.containers.Note import Note

PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
FILE = "www.cifraclub.com.br_%s.cleaned"

letras = map(chr, range(65, 91))
#letras = map(chr, range(65, 66))

acords = {}
tons = {}

def acumulaTons(d, tons):
    if (d['tom'] != ""):
        try:
            if (notes.is_valid_note(d['tom'])):
                if (d['tom'] in tons.keys()):
                    tons[d['tom']] += 1
                else:
                    tons[d['tom']] = 1
        except:
            pass

def acumulaAcordes(d, acords):
    if (len(d['cifra']) > 0):
        for c in d['cifra']:
            if (str(c) in acords.keys()):
                acords[str(c)] += 1
            else:
                acords[str(c)] = 1

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
    
def reverse_numeric(x, y):
    return y - x

def acordesMaisTocados(acords):
    l=sorted([acords[x] for x in acords], cmp=reverse_numeric)
    mais = {}
    p = .02
    for x in acords:
        if (acords[x] >= min(l[:int(len(l)*p)])):
            print x, min(l[:int(len(l)*p)])
            mais[x] = acords[x]
    return mais

def plotRepeticoes():
    p = .02
    l=sorted([acords[x] for x in acords], cmp=reverse_numeric)
    subplot(211)
    title(unicode('Repetições dos acordes'))
    ylabel(unicode('repetições'))
    xlabel('acordes')
    grid(True)
    plot(l)
    subplot(212)
    title(unicode('\n1% das repetições'))
    ylabel(unicode('repetições'))
    xlabel('acordes')
    plot(l[:int(len(l)*p)])

plotRepeticoes()
wordleFile('maisTocados',acordesMaisTocados(acords))
#wordleFile('acordes', acords)
#plots.constructQTDPlot(tons)
#plots.constructQTDPlot(acords)