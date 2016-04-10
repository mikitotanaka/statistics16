#! /usr/bin/env python

import numpy
import matplotlib.pyplot as pyplot

# drawing a math function.

x=numpy.arange(-3,3,0.1)
y=numpy.sin(x)
pyplot.plot(x,y)
pyplot.show()
pyplot.savefig('day1_1.png')

# drawing an external data.

data=numpy.genfromtxt("./day1_data.csv", delimiter=",", names=True, dtype=[('date','a9'),('precipitation',float),('cloudage',float),('sunshine',float)])
dcount=[j for i in range(55) for j in range(66)]
ticks=range(0,66,5)
pyplot.scatter(dcount,data['sunshine'])
pyplot.xticks(ticks, ['%s/%s'%(data['date'][i].split('/')[1],data['date'][i].split('/')[2]) for i in ticks], rotation='vertical')
pyplot.xlabel('Date')
pyplot.ylabel('hours')
pyplot.title('Sunshine')
pyplot.show()
pyplot.savefig('day1_2.png')
