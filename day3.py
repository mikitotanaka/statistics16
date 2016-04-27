#! /usr/bin/env python

import numpy
import matplotlib.pyplot as pyplot
from scipy import stats

## black hole mass of galaxies ##
## http://blackhole.berkeley.edu ##

data=numpy.genfromtxt("./McConnell2013.dat", comments='#')
corr1=numpy.corrcoef(data[:,6],data[:,2])
corr2=numpy.corrcoef(data[:,13],data[:,2])
print corr1[0,1],corr2[0,1]

fig=pyplot.figure(figsize=(7,9))
pyplot.subplot(2,1,1)
pyplot.errorbar(data[:,6],data[:,2],xerr=[data[:,6]-data[:,7],data[:,8]-data[:,6]],yerr=[data[:,2]-data[:,3],data[:,4]-data[:,2]],fmt='bo')
pyplot.yscale("log")
pyplot.xlabel('$\sigma$ (km/s)', fontsize=15, fontname='serif')
pyplot.ylabel('$M_{BH} \ (M_\odot)$', fontsize=15, fontname='serif')
pyplot.title('$M-\sigma$ relation of galaxies', fontsize=15, fontname='serif')
pyplot.text(60,5e10,'r = %.3f'%(corr1[0,1]),ha='left',va='center', fontsize=18, fontname='serif')
pyplot.xticks(fontsize=13, fontname='serif')
pyplot.yticks(fontsize=13, fontname='serif')
pyplot.subplot(2,1,2)
#pyplot.plot(data[:,13],data[:,2],'bo')
pyplot.errorbar(data[:,13],data[:,2],yerr=[data[:,2]-data[:,3],data[:,4]-data[:,2]],fmt='bo')
pyplot.xscale("log")
pyplot.yscale("log")
pyplot.xlabel('$M_{bulge} \ (M_\odot)$', fontsize=15, fontname='serif')
pyplot.ylabel('$M_{BH} \ (M_\odot)$', fontsize=15, fontname='serif')
pyplot.text(1.5e8,5e10,'r = %.3f'%(corr2[0,1]),ha='left',va='center', fontsize=18, fontname='serif')
pyplot.xticks(fontsize=13, fontname='serif')
pyplot.yticks(fontsize=13, fontname='serif')
pyplot.savefig('day3_1.png')
pyplot.show()


## pisa test ##

data1=numpy.genfromtxt('./science12.dat')
data2=numpy.genfromtxt('./reading12.dat')

corr1=numpy.corrcoef(data1[:,1],data2[:,1])
print corr1[0,1]

fig=pyplot.figure(figsize=(8,8))
pyplot.plot(data1[:,1],data2[:,1],'ro')
pyplot.xlabel('science scores', fontsize=25, fontname='serif')
pyplot.ylabel('reading scores', fontsize=25, fontname='serif')
pyplot.title('a relation of pisa test results', fontsize=25, fontname='serif')
pyplot.text(360,580,'r = %.3f'%(corr1[0,1]),ha='left',va='center', fontsize=25, fontname='serif')
pyplot.xticks(fontsize=18, fontname='serif')
pyplot.yticks(fontsize=18, fontname='serif')
pyplot.savefig('day3_2.png')
pyplot.show()
