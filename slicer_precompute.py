#!/usr/bin/env python
##
## nbody-slicer, an n-body viz tool written in python
## ben wibking <ben.wibking@gmail.com>
##

basefilename = "/work/02661/bwibking/"

leftfile = basefilename+"Carmen/histogram_numbers.f77binary"
rightfile = basefilename+"Carmelota/histogram_numbers.f77binary"

zaxis = 0

#zmin = 0.
#zmax = 10.
z = 0.

xmin = 500.
xmax = 1000.

ymin = 500.
ymax = 1000.

#######

import matplotlib

import time
import numpy
import loadf77
import matplotlib.pyplot as plt

plt.ion()

print "loading precomputed density histograms..."

leftheader,lefthist = loadf77.fromfile(leftfile)
print leftheader
rightheader,righthist = loadf77.fromfile(rightfile)
print rightheader

print "done."

print "plotting density field..."

from matplotlib.widgets import Slider, Button, RadioButtons

f, (left, right) = plt.subplots(1,2)
plt.subplots_adjust(left=0.1, bottom=0.15)

# TODO: have to determine indices of density array from zmin/zmax, xmin/max, ymin/max
boxsize = leftheader['BoxSize']
leftindex = int(z / leftheader['BoxSize'] * lefthist.shape[0])
rightindex = int(z / rightheader['BoxSize']* righthist.shape[0])

print lefthist.shape
print righthist.shape

norm = matplotlib.colors.Normalize(vmin=righthist.min(), vmax=righthist.max())
g = left.imshow(lefthist[leftindex,:,:],interpolation='none')
g.set_norm(norm)
#c = right.imshow((righthist-lefthist),interpolation='none')
diff = righthist[rightindex,:,:] - lefthist[leftindex,:,:]
c = right.imshow(diff,interpolation='none')
#c = right.imshow((righthist[rightindex,:,:]),interpolation='none')
c.set_norm(norm)
#plt.colorbar(g)
#plt.colorbar(c)

left.set_title('Low-res phases')
right.set_title('High-res phases')

axcolor = 'lightgoldenrodyellow'
axz = plt.axes([0.1, 0.1, 0.65, 0.03], axisbg=axcolor)
#axzwidth  = plt.axes([0.1, 0.15, 0.65, 0.03], axisbg=axcolor)

sz = Slider(axz, 'z', 0., boxsize, valinit=10.0)
#szwidth = Slider(axzwidth, 'z-width', 0.1, 20.0, valinit=20.0)

def update(val):
    start = time.clock()

    z = sz.val
#    zwidth = szwidth.val

#    zmin = z - zwidth/2.
#    zmax = z + zwidth/2.

    leftindex = int(z / leftheader['BoxSize'] * lefthist.shape[0])
    rightindex = int(z / rightheader['BoxSize']* righthist.shape[0])

    g.set_array(lefthist[leftindex,:,:])
    diff = righthist[rightindex,:,:] - lefthist[leftindex,:,:]
    c.set_array(diff)
#    c.set_array(righthist[rightindex,:,:])

    print "Updated data in",time.clock()-start,"seconds."

    f.canvas.draw_idle()

sz.on_changed(update)

plt.show(block=True)
