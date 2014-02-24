#!/usr/bin/env python
##
## nbody-slicer, an n-body viz tool written in python
## ben wibking <ben.wibking@gmail.com>
##

basefilename = ""

leftfile = basefilename+""
rightfile = basefilename+""

boxsize = 1000.
numbins = 100
zaxis = 0

zmin = 0.
zmax = 10.

xmin = 500.
xmax = 1000.

ymin = 500.
ymax = 1000.

#######

import matplotlib

import time
import numpy
import pynbody
import matplotlib.pyplot as plt

plt.ion()

print "loading snapshots..."

leftsim = pynbody.load(leftfile)
rightsim = pynbody.load(rightfile)

print "done."

leftparticles = leftsim.dm['pos']
rightparticles = rightsim.dm['pos']

print "Lo particles: ",len(leftparticles)
print "Hi particles: ",len(rightparticles)

print "done."
print "plotting particles..."

from matplotlib.widgets import Slider, Button, RadioButtons

f, (left, right) = plt.subplots(1,2)
plt.subplots_adjust(left=0.1, bottom=0.25)

rightindex = (rightparticles[:,zaxis] > zmin) & (rightparticles[:,zaxis] < zmax) & (rightparticles[:,(zaxis+1)%3] > xmin) & (rightparticles[:,(zaxis+1)%3] < xmax) & (rightparticles[:,(zaxis+2)%3] > xmin) & (rightparticles[:,(zaxis+2)%3] < ymax)
leftindex = (leftparticles[:,zaxis] > zmin) & (leftparticles[:,zaxis] < zmax) & (leftparticles[:,(zaxis+1)%3] > xmin) & (leftparticles[:,(zaxis+1)%3] < xmax) & (leftparticles[:,(zaxis+2)%3] > xmin) & (leftparticles[:,(zaxis+2)%3] < ymax)

## we want to plot density fields
lefthist,xedges,yedges = numpy.histogram2d(leftparticles[leftindex,(zaxis+1)%3],leftparticles[leftindex,(zaxis+2)%3],bins=numbins,normed=True)
righthist,xedges,yedges= numpy.histogram2d(rightparticles[rightindex,(zaxis+1)%3],rightparticles[rightindex,(zaxis+2)%3],bins=numbins,normed=True)

norm = matplotlib.colors.Normalize(vmin=righthist.min(), vmax=righthist.max())
g = left.imshow(lefthist,interpolation='none')
g.set_norm(norm)
#c = right.imshow((righthist-lefthist),interpolation='none')
c = right.imshow((righthist),interpolation='none')
c.set_norm(norm)
#plt.colorbar(g)
#plt.colorbar(c)

left.set_title('Low-res phases')
right.set_title('High-res phases')

axcolor = 'lightgoldenrodyellow'
axz = plt.axes([0.1, 0.1, 0.65, 0.03], axisbg=axcolor)
axzwidth  = plt.axes([0.1, 0.15, 0.65, 0.03], axisbg=axcolor)

sz = Slider(axz, 'z', 0., boxsize, valinit=10.0)
szwidth = Slider(axzwidth, 'z-width', 0.1, 20.0, valinit=20.0)

def update(val):
    start = time.clock()

    z = sz.val
    zwidth = szwidth.val

    zmin = z - zwidth/2.
    zmax = z + zwidth/2.

    rightindex = (rightparticles[:,zaxis] > zmin) & (rightparticles[:,zaxis] < zmax) & (rightparticles[:,(zaxis+1)%3] > xmin) & (rightparticles[:,(zaxis+1)%3] < xmax) & (rightparticles[:,(zaxis+2)%3] > xmin) & (rightparticles[:,(zaxis+2)%3] < ymax)
    leftindex = (leftparticles[:,zaxis] > zmin) & (leftparticles[:,zaxis] < zmax) & (leftparticles[:,(zaxis+1)%3] > xmin) & (leftparticles[:,(zaxis+1)%3] < xmax) & (leftparticles[:,(zaxis+2)%3] > xmin) & (leftparticles[:,(zaxis+2)%3] < ymax)

    lefthist,xedges,yedges = numpy.histogram2d(leftparticles[leftindex,(zaxis+1)%3],leftparticles[leftindex,(zaxis+2)%3],normed=True,bins=numbins)
    righthist,xedges,yedges= numpy.histogram2d(rightparticles[rightindex,(zaxis+1)%3],rightparticles[rightindex,(zaxis+2)%3],normed=True,bins=numbins)

    g.set_array(lefthist)
    c.set_array(righthist)

    print "Updated data in",time.clock()-start,"seconds."

    f.canvas.draw_idle()

sz.on_changed(update)
szwidth.on_changed(update)

plt.show(block=True)
