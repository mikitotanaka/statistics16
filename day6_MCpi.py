#!/usr/bin/env python

import random,math
import numpy
import matplotlib.pyplot as pyplot
import multiprocessing as mp

### monte carlo n roop ###

def argwrapper(args):

        return args[0](*args[1:])

def calcpi(n):

        random.seed(1)
        #n=decimal.Decimal(n)
        j=0
        random.jumpahead(n)
        for i in range(n):
                x,y=random.uniform(0,1),random.random()
                if x*x+y*y<=1.0: j+=1
        return n,4.0*float(j)/float(n)

### main ###

if __name__== "__main__":

	ntot=1000
	n_cpu=mp.cpu_count()
	#n_cpu=1
	print "The number of CPUs: %d" % (n_cpu)

        pool=mp.Pool(processes=n_cpu)
        target=[(calcpi,i) for i in xrange(1,ntot+1)]
        result=pool.map(argwrapper, target)
        vstack_map=[]
        for i in result: vstack_map.append(i)
        pidist=numpy.vstack(vstack_map)

        ncut=1
        mean=numpy.mean(pidist[:,1][numpy.where((pidist[:,0]>ncut))])
        print mean

	myrange=[0,ntot,2.9,3.4]
        pyplot.figure(figsize=(11,7))
        pyplot.scatter(pidist[:,0],pidist[:,1])
        pyplot.axhline(y=math.pi, xmin=0, xmax=ntot, color="red", lw=3)
        pyplot.axis(myrange)
        pyplot.title("$\pi_{mean}(n>%d)=$%.6f"%(ncut,mean), fontsize=20, fontname='serif')
	pyplot.xlabel("n", fontsize=20, fontname='serif')
	pyplot.ylabel("$\pi$", fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
	pyplot.savefig("day6_MCpi.png") # output to png
        pyplot.show()
