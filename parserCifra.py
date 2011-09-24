# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 22:00:16 2011

@author: antoanne
"""
from BeautifulSoup import BeautifulStoneSoup

PATH = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/musica/data/"
FILE = "www.cifraclub.com.br"



def cleanCifra(cifra):
    return cifra

def splitCifraLetra(cifra):
    cifra = []
    letra = []
    return letra, cifra

def cleanDictCifra(d):
    pass
    #print d['cifra']
    #d['letra'], d['cifra'] = splitCifraLetra(d['cifra'])
    #print '==================================================='
    #print d['cifra']
    #return d

def readFromDictFile(fileName):
    c = open(PATH+fileName+'.cleaned.dictFile','r')
    c.readAll
    for line in c:
        print eval(line)
        cleanDictCifra(eval(line))
        break
        #c.write(str(cleanDictCifra(eval(line))))
    c.close()

readFromDictFile(FILE)
