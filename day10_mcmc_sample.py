#! /usr/bin/env python

import numpy,copy
import scipy.stats
from scipy.stats import multivariate_normal
import matplotlib.pyplot as pyplot
import mpl_toolkits.mplot3d as mplot3d
import seaborn

#P(x):Target distribution
def P(x,y,mu,cov):
    return multivariate_normal.pdf([x,y],mu,cov)

#Q(x):Proposal distribution
def Q(c,mu1,mu2,sigma):
    return [c[0]+numpy.random.normal(mu1,sigma), c[1]+numpy.random.normal(mu2,sigma)]

def metropolis(nmax,xini,yini,mu1,mu2,sigma,cov):
    pt=P(xini, yini, [mu1,mu2], cov)
    current=[xini,yini,pt]
    sample=[]
    sample.append(current)
    accept_ratio=[]

    for i in range(nmax):
        candidate=Q(current,mu1,mu2,sigma)

        T_prev=P(current[0], current[1], [mu1,mu2], cov)
        T_next=P(candidate[0], candidate[1], [mu1,mu2], cov)
        a=T_next/T_prev

        if a>1 or a>numpy.random.uniform(0,1):
            #Update state
            current=copy.copy(candidate+[T_next])
            sample.append(current)
            accept_ratio.append(i)
        else:
            current[2]=T_prev
            sample.append(current)

    print 'Accept ratio :', float(len(accept_ratio)) / nmax
    return numpy.array(sample)


def mlf(nmax,xini,yini,mu1,mu2,sigma,cov):
    pt=P(xini, yini, [mu1,mu2], cov)
    current=[xini,yini,pt]
    sample=[]
    sample.append(current)

    for i in range(nmax):
        candidate=Q(current,mu1,mu2,sigma)

        T_prev=P(current[0], current[1], [mu1,mu2], cov)
        T_next=P(candidate[0], candidate[1], [mu1,mu2], cov)
        a=T_next/T_prev

        if a>1:
            #Update state
            current=copy.copy(candidate+[T_next])
            sample.append(current)

    return numpy.array(sample)


def mcmc():

    mu1=0.
    mu2=0.
    sigma=1.
    cov=[[0.1,0.],[0.,0.1]]
    nmax=5000
    burn_in=500

    xini=2.;yini=-2.
    sample1=metropolis(nmax,xini,yini,mu1,mu2,sigma,cov)

    xini=-2.;yini=2.
    sample2=metropolis(nmax,xini,yini,mu1,mu2,sigma,cov)

    xini=2.;yini=2.
    sample3=metropolis(nmax,xini,yini,mu1,mu2,sigma,cov)

    xini=-2.;yini=-2.
    sample4=metropolis(nmax,xini,yini,mu1,mu2,sigma,cov)

    fig = pyplot.figure(figsize=(10,8))
    pyplot.scatter(sample1[:,0],sample1[:,1],color='b',s=20,alpha=0.1,edgecolor='None')
    pyplot.scatter(sample2[:,0],sample2[:,1],color='r',s=20,alpha=0.1,edgecolor='None')
    pyplot.scatter(sample3[:,0],sample3[:,1],color='g',s=20,alpha=0.1,edgecolor='None')
    pyplot.scatter(sample4[:,0],sample4[:,1],color='m',s=20,alpha=0.1,edgecolor='None')
    pyplot.xlim(-2,2)
    pyplot.ylim(-2,2)
    pyplot.xlabel(r'$\theta_1$', fontsize=20, fontname='serif')
    pyplot.ylabel(r'$\theta_2$', fontsize=20, fontname='serif')
    #pyplot.title('MCMC (Metropolis)', fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.savefig('day10_metropolis1.png')
    pyplot.show()

    x,y= numpy.mgrid[-2:2:.1, -2:2:.1]
    pos = numpy.empty(x.shape + (2,))
    pos[:,:,0] = x; pos[:,:,1] = y
    mu=[mu1,mu2]
    rv = multivariate_normal(mu, cov)
    z = rv.pdf(pos)

    fig = pyplot.figure(figsize=(13,9))
    ax = mplot3d.Axes3D(fig)
    ax.plot_wireframe(x,y,z,color='k',alpha=0.3)
    #ax.plot(sample[:,0],sample[:,1],sample[:,2],c='r',lw=0.5)
    ax.scatter3D(sample1[:,0],sample1[:,1],sample1[:,2],c='b',s=15,alpha=0.5)
    ax.scatter3D(sample2[:,0],sample2[:,1],sample2[:,2],c='r',s=15,alpha=0.5)
    ax.scatter3D(sample3[:,0],sample3[:,1],sample3[:,2],c='g',s=15,alpha=0.5)
    ax.scatter3D(sample4[:,0],sample4[:,1],sample4[:,2],c='m',s=15,alpha=0.5)
    ax.set_xlabel(r'$\theta_1$', fontsize=20, fontname='serif')
    ax.set_ylabel(r'$\theta_2$', fontsize=20, fontname='serif')
    ax.set_zlabel("P", fontsize=20, fontname='serif')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(0,1.5)
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.savefig('day10_metropolis2.png')
    pyplot.show()

    n=range(nmax+1)
    fig = pyplot.figure(figsize=(8,10))
    pyplot.subplot(211)
    pyplot.plot(n,sample1[:,0])
    pyplot.plot(n,sample2[:,0])
    pyplot.plot(n,sample3[:,0])
    pyplot.plot(n,sample4[:,0])
    pyplot.xlabel(r'$n$', fontsize=20, fontname='serif')
    pyplot.ylabel(r'$\theta_1$', fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=10, fontname='serif')
    pyplot.subplot(212)
    pyplot.plot(n,sample1[:,1])
    pyplot.plot(n,sample2[:,1])
    pyplot.plot(n,sample3[:,1])
    pyplot.plot(n,sample4[:,1])
    pyplot.xlabel(r'$n$', fontsize=20, fontname='serif')
    pyplot.ylabel(r'$\theta_2$', fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=10, fontname='serif')
    pyplot.savefig('day10_metropolis3.png')
    pyplot.show()

    fig = pyplot.figure(figsize=(8,10))
    pyplot.subplot(211)
    pyplot.hist(sample1[:,0],bins=20,normed=True,alpha=0.9)
    pyplot.hist(sample2[:,0],bins=20,normed=True,alpha=0.9)
    pyplot.hist(sample3[:,0],bins=20,normed=True,alpha=0.9)
    pyplot.hist(sample4[:,0],bins=20,normed=True,alpha=0.9)
    pyplot.xlabel(r'$\theta_1$', fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.subplot(212)
    pyplot.hist(sample1[:,1],bins=20,normed=True,alpha=0.9)
    pyplot.hist(sample2[:,1],bins=20,normed=True,alpha=0.9)
    pyplot.hist(sample3[:,1],bins=20,normed=True,alpha=0.9)
    pyplot.hist(sample4[:,1],bins=20,normed=True,alpha=0.9)
    pyplot.xlabel(r'$\theta_2$', fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.savefig('day10_metropolis4.png')
    pyplot.show()

    theta1=sample1[burn_in:,0]+sample2[burn_in:,0]+sample3[burn_in:,0]+sample4[burn_in:,0]
    x1mean=numpy.mean(theta1)
    x1med=numpy.median(theta1)
    x1std=numpy.std(theta1)
    x1q0=scipy.stats.scoreatpercentile(theta1, 2.5)
    x1q1=scipy.stats.scoreatpercentile(theta1, 25)
    x1q3=scipy.stats.scoreatpercentile(theta1, 75)
    x1q4=scipy.stats.scoreatpercentile(theta1, 97.5)

    print x1mean,x1std,x1q0,x1q1,x1med,x1q3,x1q4

    theta2=sample1[burn_in:,1]+sample2[burn_in:,1]+sample3[burn_in:,1]+sample4[burn_in:,1]
    x2mean=numpy.mean(theta2)
    x2med=numpy.median(theta2)
    x2std=numpy.std(theta2)
    x2q0=scipy.stats.scoreatpercentile(theta2, 2.5)
    x2q1=scipy.stats.scoreatpercentile(theta2, 25)
    x2q3=scipy.stats.scoreatpercentile(theta2, 75)
    x2q4=scipy.stats.scoreatpercentile(theta2, 97.5)
    
    print x2mean,x2std,x2q0,x2q1,x1med,x2q3,x2q4

    x=numpy.linspace(-3,3,10000)
    
    fig = pyplot.figure(figsize=(8,10))
    pyplot.subplot(211)
    pyplot.hist(theta1,bins=20,normed=True,alpha=0.9)
    pyplot.plot(x,scipy.stats.norm.pdf(x,loc=x1mean,scale=x1std),lw=2)
    pyplot.xlabel(r'$\theta_1$', fontsize=20, fontname='serif')
    pyplot.text(1.4,0.64,r"$mean = %.2f$"%(x1mean), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.58,r"$std = %.2f$"%(x1std), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.52,r"$2.5\%% = %.2f$"%(x1q0), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.46,r"$25\%% = %.2f$"%(x1q1), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.40,r"$50\%% = %.2f$"%(x1med), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.34,r"$75\%% = %.2f$"%(x1q3), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.28,r"$97.5\%% = %.2f$"%(x1q4), fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.subplot(212)
    pyplot.hist(theta2,bins=20,normed=True,alpha=0.9)
    pyplot.plot(x,scipy.stats.norm.pdf(x,loc=x2mean,scale=x2std),lw=2)
    pyplot.xlabel(r'$\theta_2$', fontsize=20, fontname='serif')
    pyplot.text(1.4,0.64,r"$mean = %.2f$"%(x2mean), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.58,r"$std = %.2f$"%(x2std), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.52,r"$2.5\%% = %.2f$"%(x2q0), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.46,r"$25\%% = %.2f$"%(x2q1), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.40,r"$50\%% = %.2f$"%(x2med), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.34,r"$75\%% = %.2f$"%(x2q3), fontsize=20, fontname='serif')
    pyplot.text(1.4,0.28,r"$97.5\%% = %.2f$"%(x2q4), fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.savefig('day10_metropolis5.png')
    pyplot.show()

def randomwalk():

    """
    n=100
    x=0;y=0
    coo=[[x,y]]
    for i in range(n):
        xstep,ystep=numpy.random.choice([-1,1],p=[0.5,0.5]),numpy.random.choice([-1,1],p=[0.5,0.5])
        x+=xstep;y+=ystep
        coo.append([x,y])
    coo=numpy.array(coo)
    pyplot.plot(coo[:,0],coo[:,1])
    pyplot.scatter(coo[:,0],coo[:,1])
    pyplot.savefig('day10_randomwalk1.png')
    pyplot.show()
    exit()
    """

    n=1000
    x=0;y=0
    coo=[[x,y]]
    for i in range(n):
        xstep,ystep=numpy.random.choice([-1,1],p=[0.5,0.5]),numpy.random.choice([-1,1],p=[0.5,0.5])
        x+=xstep;y+=ystep
        coo.append([x,y])
    coo=numpy.array(coo)
    pyplot.plot(coo[:,0],coo[:,1])
    pyplot.scatter(coo[:,0],coo[:,1])
    pyplot.savefig('day10_randomwalk2.png')
    pyplot.show()

    n=1000
    x=0;y=0
    coo=[[x,y]]
    for i in range(n):
        xstep,ystep=numpy.random.choice([-1,1],p=[0.4,0.6]),numpy.random.choice([-1,1],p=[0.4,0.6])
        x+=xstep;y+=ystep
        coo.append([x,y])
    coo=numpy.array(coo)
    pyplot.plot(coo[:,0],coo[:,1])
    pyplot.scatter(coo[:,0],coo[:,1])
    pyplot.savefig('day10_randomwalk3.png')
    pyplot.show()

def maximumlikelihood():

    """
    x=numpy.linspace(-4,4,1000)
    pyplot.figure(figsize=(15,8))
    seaborn.set_style('white')
    pyplot.plot(x,scipy.stats.norm.pdf(x),lw=5)
    pyplot.xlim(-4.5,4.5)
    pyplot.ylim(-0.05,0.45)
    pyplot.tick_params(labelleft='off',labelbottom='off')
    #seaborn.despine()
    pyplot.savefig('day10_maximulikelihood1.png')
    pyplot.show()
    exit()
    """

    mu1=0.
    mu2=0.
    sigma=0.1
    cov=[[0.1,0.],[0.,0.1]]

    nmax=1000
    xini=1.;yini=-1.
    #sample1=mlf(nmax,xini,yini,mu1,mu2,sigma,cov)

    x,y= numpy.mgrid[-2:2:.1, -2:2:.1]
    pos = numpy.empty(x.shape + (2,))
    pos[:,:,0] = x; pos[:,:,1] = y
    mu=[mu1,mu2]
    rv = multivariate_normal(mu, cov)
    z = rv.pdf(pos)

    fig = pyplot.figure(figsize=(13,9))
    seaborn.set_style('white')
    ax = mplot3d.Axes3D(fig)
    ax.plot_wireframe(x,y,z)
    #ax.plot(sample1[:,0],sample1[:,1],sample1[:,2],c='r',lw=2)
    #ax.scatter3D(sample1[:,0],sample1[:,1],sample1[:,2],c='r',s=80)
    #ax.set_xlabel(r'$\theta_1$', fontsize=20, fontname='serif')
    #ax.set_ylabel(r'$\theta_2$', fontsize=20, fontname='serif')
    #ax.set_zlabel("P", fontsize=20, fontname='serif')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(0,1.5)
    pyplot.tick_params(labelleft='off',labelbottom='off')
    #pyplot.xticks(fontsize=20, fontname='serif')
    #pyplot.yticks(fontsize=20, fontname='serif')
    #seaborn.despine()
    pyplot.savefig('day10_maximulikelihood0.png')
    pyplot.show()


if __name__== "__main__":

    #randomwalk()
    #maximumlikelihood()
    mcmc()
