# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 20:47:22 2011

@author: antoanne
"""
import numpy as np
import matplotlib.pyplot as plot
import pylab

#tons = {u'A': 74, 
#        u'B': 32, 
#        u'E': 68, 
#        u'D': 119, 
#        u'G': 144, 
#        u'F': 45, 
#        u'D#': 6, 
#        u'F#': 9, 
#        u'G#': 5, 
#        u'A#': 17,
#        u'C#': 2,
#        u'C': 134}

def constructQTDPlot(tons):
    ind = np.arange(len(tons))
    qtd = [tons[x] for x in tons]
    lbl = [x for x in tons]
    fig = plot.figure()
    fig.canvas.set_window_title('Tons mais tocados')
    plot.title('Tons mais tocados')
    plot.subplot(111)
    plot.barh(ind, qtd, 0.5, color='green', align='center')
    pylab.yticks(ind,lbl)
    plot.show()

#constructQTDPlot(tons)