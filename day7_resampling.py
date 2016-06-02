#!/usr/bin/env python

import numpy
import scipy.stats
import matplotlib.pyplot as pyplot

c=299722.22222223717 # km/s
G=6.67408e-20 # km^3 kg^-1 s^-2
R=87.49*20*3.086e+16 # km
Msun=1.9884e30 # kg
frac=1.0

def calcmass(meantmp,stdtmp):

    meanmean=numpy.mean(meantmp)
    meanstd=numpy.std(meantmp, ddof=1)
    stdmean=numpy.mean(stdtmp)
    stdstd=numpy.std(stdtmp, ddof=1)

    mass=frac*stdmean*stdmean*R/G/Msun
    massp=frac*(stdmean+stdstd)*(stdmean+stdstd)*R/G/Msun-mass
    massm=mass-frac*(stdmean-stdstd)*(stdmean-stdstd)*R/G/Msun

    print "mean velicity: %.0f +/- %.0f km/s"%(meanmean,meanstd)
    print "velocity dispersion: %.0f +/- %.0f km/s"%(stdmean,stdstd)
    print "dynamical mass: %.1f[+%.1f,-%.1f]e14 Msun"%(mass/10**14,massp/10**14,massm/10**14)

    return meanmean,meanstd,stdmean,stdstd,mass,massp,massm

if __name__== "__main__":


    data0=numpy.genfromtxt("./abell2255_SDSS.csv", delimiter=",", names=True, dtype=[('objid',int),('ra',float),('dec',float),('u',float),('g',float),('r',float),('i',float),('z',float),('class','a6'),('redshift',float),('velDisp',float),('velDispErr',float)])

    data0['redshift']=data0['redshift']*c
    data1=data0[numpy.where((data0['redshift']<30000)&(data0['redshift']>20000))]

    print "Abell 2255 analysis"

    nsample=int(len(data1))
    print "sample size: %d"%(nsample)

    velmean0=numpy.mean(data1['redshift'])
    velstd0=numpy.std(data1['redshift'], ddof=1)
    mass=frac*velstd0*velstd0*R/G/Msun
    print "mean velicity: %.0f km/s"%(velmean0)
    print "velocity dispersion: %.0f km/s"%(velstd0)
    print "dynamical mass: %.1fe14 Msun"%(mass/10**14)

    nresample=100

    print "bootstrap"

    meantmp=[];stdtmp=[]
    for x in xrange(nresample):
        velbs=[]
        for i in xrange(nsample):
            j=numpy.random.randint(nsample)
            velbs.append(data1['redshift'][j])
        velmean=numpy.mean(velbs)
        velstd=numpy.std(velbs, ddof=1)
        meantmp.append(velmean)
        stdtmp.append(velstd)

    meanmean1,meanstd1,stdmean1,stdstd1,mass1,massp1,massm1=calcmass(meantmp,stdtmp)

    print "jack knife"

    meantmp=[];stdtmp=[]
    for x in xrange(nresample):
        j=numpy.random.randint(nsample)
        data=numpy.hstack([data1['redshift'][:j],data1['redshift'][j+1:]])
        velmean=numpy.mean(data)
        velstd=numpy.std(data, ddof=1)
        meantmp.append(velmean)
        stdtmp.append(velstd)

    meanmean2,meanstd2,stdmean2,stdstd2,mass2,massp2,massm2=calcmass(meantmp,stdtmp)

    print "parametric bootstrap"

    meantmp=[];stdtmp=[]
    for x in xrange(nresample):
        data=numpy.random.normal(velmean0,velstd0,nsample)
        velmean=numpy.mean(data)
        velstd=numpy.std(data, ddof=1)
        meantmp.append(velmean)
        stdtmp.append(velstd)

    meanmean3,meanstd3,stdmean3,stdstd3,mass3,massp3,massm3=calcmass(meantmp,stdtmp)

    x=numpy.linspace(20000,35000,15000)
    fig=pyplot.figure(figsize=(13,9))
    pyplot.hist(data1['redshift'], bins=20)
    pyplot.plot(x,scipy.stats.norm.pdf(x,loc=velmean0,scale=velstd0)*40000,color="red",lw=1.5)
    pyplot.xlim(20000,35000)
    pyplot.ylim(0,19)
    pyplot.xlabel('km/s', fontsize=20, fontname='serif')
    pyplot.ylabel('N', fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.title('Radial Velocity Distribution of Abell 2255 (cluster of galaxies)',fontsize=20, fontname='serif')
    pyplot.text(28000,18,"mean velicity: %.0f km/s"%(velmean0),fontsize=15, fontname='serif')
    pyplot.text(28000,17,"velocity dispersion: %.0f km/s"%(velstd0),fontsize=15, fontname='serif')
    pyplot.text(28000,16,"dynamical mass: %.1fe14 Msun"%(mass/10**14),fontsize=15, fontname='serif')
    pyplot.text(27800,15,"Bootstrap:",fontsize=15, fontname='serif')
    pyplot.text(28000,14,"mean velicity: %.0f +/- %.0f km/s"%(meanmean1,meanstd1),fontsize=15, fontname='serif')
    pyplot.text(28000,13,"velocity dispersion: %.0f +/- %.0f km/s"%(stdmean1,stdstd1),fontsize=15, fontname='serif')
    pyplot.text(28000,12,"dynamical mass: %.1f[+%.1f,-%.1f]e14 Msun"%(mass1/10**14,massp1/10**14,massm1/10**14),fontsize=15, fontname='serif')
    pyplot.text(27800,11,"Jack Knife:",fontsize=15, fontname='serif')
    pyplot.text(28000,10,"mean velicity: %.0f +/- %.0f km/s"%(meanmean2,meanstd2),fontsize=15, fontname='serif')
    pyplot.text(28000,9,"velocity dispersion: %.0f +/- %.0f km/s"%(stdmean2,stdstd2),fontsize=15, fontname='serif')
    pyplot.text(28000,8,"dynamical mass: %.1f[+%.1f,-%.1f]e14 Msun"%(mass2/10**14,massp2/10**14,massm2/10**14),fontsize=15, fontname='serif')
    pyplot.text(27800,7,"Parametric Bootstrap:",fontsize=15, fontname='serif')
    pyplot.text(28000,6,"mean velicity: %.0f +/- %.0f km/s"%(meanmean3,meanstd3),fontsize=15, fontname='serif')
    pyplot.text(28000,5,"velocity dispersion: %.0f +/- %.0f km/s"%(stdmean3,stdstd3),fontsize=15, fontname='serif')
    pyplot.text(28000,4,"dynamical mass: %.1f[+%.1f,-%.1f]e14 Msun"%(mass3/10**14,massp3/10**14,massm3/10**14),fontsize=15, fontname='serif')
    pyplot.savefig("day7_resampling.png")
    pyplot.show()
