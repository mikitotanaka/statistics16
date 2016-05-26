#!/usr/bin/env python

import numpy,math
from scipy.stats import norm
import matplotlib.pyplot as pyplot

def func_gauss(mu,sigma,x):
        return norm.pdf(x, loc=mu, scale=sigma)

def gauss_dist():

        mu=0;sigma=1

        y0=1.0/(numpy.sqrt(2*numpy.pi)*sigma)
        x=numpy.linspace(-6,6,2000)
        y=func_gauss(mu,sigma,x)

        fig,ax1=pyplot.subplots(figsize=(12,8))
        ax1.axvline(x=0, color='k')

        xlab=[]
        for i in range(-6,7):
                a=norm.cdf(x=sigma*i,loc=mu,scale=sigma)
                b=norm.cdf(x=-sigma*i,loc=mu,scale=sigma)
                per=(a-b)*100
                print "%dsigma = %f" % (i,per)
                ax1.axvline(x=i, color='k', ls='--')
                xlab.append("%.2f"%(per))

        ax1.plot(x,y,lw=3)
        ax1.set_xlabel(r'$x$', fontsize=20, fontname='serif')
        ax1.set_xticks(numpy.arange(-6,7,1))
        pyplot.xticks(fontsize=17, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.text(1.0,0.3,r'$N(\mu=0,\sigma^2=1)=\frac{1}{\sqrt{2\pi}}e^{-\frac{x^2}{2}}$',fontsize=25, fontname='serif')
        ax2=ax1.twiny()
        ax2.set_xlabel(r'$\%$', fontsize=20, fontname='serif')
        ax2.set_xticks(numpy.arange(-6,7,1))
        ax2.set_xticklabels(xlab)
        pyplot.xticks(fontsize=15, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.ylim(0,y0)
	pyplot.savefig("day6_normaldist.png") # output to png
        pyplot.show()

def func_err(x):
        return math.erf(x/numpy.sqrt(2.0))*100

def err_dist():

        x=numpy.linspace(0,4.3,2000)
        y=[func_err(i) for i in x]
        pyplot.figure(figsize=(11,7))
        pyplot.hlines(y=100, xmin=0, xmax=4.3, color='k', linestyle="--")
        for i in range(1,5): pyplot.vlines(x=i, ymin=0, ymax=100, color='k', linestyle="--")
        pyplot.vlines(x=0.674, ymin=0, ymax=func_err(0.674), color='k', linestyle="--")
        pyplot.hlines(y=50, xmin=0, xmax=0.674, color='k', linestyle="--")
        pyplot.plot(x,y,lw=3)
        pyplot.text(0.53,10,"0.674", fontsize=15, fontname='serif')
        pyplot.text(1.05,65,"68%", fontsize=15, fontname='serif')
        pyplot.text(2.05,91,"95.4%", fontsize=15, fontname='serif')
        pyplot.text(2.90,102,"99.7%", fontsize=15, fontname='serif')
        pyplot.text(3.85,102,"99.99%", fontsize=15, fontname='serif')
        pyplot.xlabel("$t$", fontsize=20, fontname='serif')
        pyplot.ylabel("$\%$", fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=18, fontname='serif')
        pyplot.yticks([0,50,100], fontsize=18, fontname='serif')
        pyplot.xlim(0,4.3)
        pyplot.ylim(0,110)
	pyplot.savefig("day6_errfunc.png") # output to png
        pyplot.show()

if __name__== "__main__":

        gauss_dist()
        err_dist()
