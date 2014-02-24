#!/usr/bin/env python

## read Fortran 77 unformatted binary array into numpy array
## ben wibking <ben.wibking@gmail.com>

import numpy

pad_size = 8 # bytes
header_size = 256 # bytes
header_dtype = numpy.dtype([
        ('npart',(numpy.int32,6)),
        ('mass',(numpy.float64,6)),
        ('time',numpy.float64),
        ('redshift',numpy.float64),
        ('flag_sfr',numpy.int32),
        ('flag_feedback',numpy.int32),
        ('npartTotal',(numpy.uint32,6)),
        ('flag_cooling',numpy.int32),
        ('num_files',numpy.int32),
        ('BoxSize',numpy.float64),
        ('Omega0',numpy.float64),
        ('OmegaLambda',numpy.float64),
        ('HubbleParam',numpy.float64),
        ('flag_stellarage',numpy.int32),
        ('flag_metals',numpy.int32),
        ('npartTotalHighWord',(numpy.uint32,6)),
        ('flag_entropy_instead_u',numpy.int32),
        ('fill',(numpy.uint8,60))
])

def fromfile(filename):
    # use recarrays to read in header, then read in array separately
    myfile = open(filename,'rb')

    padding = myfile.read(pad_size)
    Nbins_string = myfile.read(numpy.dtype(numpy.int32).itemsize)
    padding = myfile.read(pad_size)

    Nbins = numpy.fromstring(Nbins_string,dtype=numpy.int32)
    print "Nbins:",Nbins
    print "Memory needed:",numpy.dtype(numpy.float64).itemsize*float(Nbins)**3./1024./1024./1024.,"GiB"

    padding = myfile.read(pad_size)
    header = myfile.read(header_size)
    padding = myfile.read(pad_size)

    header_struct = numpy.fromstring(header,dtype=header_dtype)

    padding = myfile.read(pad_size)
    array = numpy.fromfile(myfile,dtype=numpy.float64,count=Nbins**3)
    padding = myfile.read(pad_size)

    array = numpy.reshape(array,(Nbins,Nbins,Nbins))

    myfile.close()

    # return array contents
    return header_struct,array
