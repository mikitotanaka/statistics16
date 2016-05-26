#!/usr/bin/env python

import math
import numpy
import matplotlib.pyplot as pyplot

def func_binomial(n,x,p):
        C=math.factorial(n)/math.factorial(n-x)/math.factorial(x)
        return float(C)*pow(p,x)*pow(1-p,n-x)

def binomial_dist():

        pyplot.figure(figsize=(11,7))
        n=6
        p=[0.2,0.5,0.1]
        x=numpy.arange(n+1)
        for pi in p:
                y=[func_binomial(n,xi,pi) for xi in x]
                E=n*pi
                V=n*pi*(1-pi)
                pyplot.plot(x,y,label='Bi (%s, %s), E(X)=%.2f, V(X)=%.2f'%(n,pi,E,V))
        pyplot.legend(loc='best')
        pyplot.xlabel('x', fontsize=20, fontname='serif')
        pyplot.ylabel('fraction', fontsize=20, fontname='serif')
        pyplot.title('binomial distribution', fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.savefig('day6_binomial.png')
        pyplot.show()

def func_poisson(lamda,x):
        return math.exp(-lamda)*pow(lamda,x)/math.factorial(x)

def poisson_dist():

        pyplot.figure(figsize=(11,7))
        n=4;lamda=0.6
        x=numpy.arange(n+1)
        y=[func_poisson(lamda,xi) for xi in x]
        E=V=lamda
        pyplot.plot(x,y,label='P0 (%s), E(X)=%.2f, V(X)=%.2f'%(lamda,E,V))
        n=6;lamda=1.5
        x=numpy.arange(n+1)
        y=[func_poisson(lamda,xi) for xi in x]
        E=V=lamda
        pyplot.plot(x,y,label='P0 (%s), E(X)=%.2f, V(X)=%.2f'%(lamda,E,V))
        n=9;lamda=3.5
        x=numpy.arange(n+1)
        y=[func_poisson(lamda,xi) for xi in x]
        E=V=lamda
        pyplot.plot(x,y,label='P0 (%s), E(X)=%.2f, V(X)=%.2f'%(lamda,E,V))
        pyplot.legend(loc='best')
        pyplot.xlabel('x', fontsize=20, fontname='serif')
        pyplot.ylabel('fraction', fontsize=20, fontname='serif')
        pyplot.title('Poisson distribution', fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.savefig('day6_poisson.png')
        pyplot.show()

        pyplot.figure(figsize=(11,7))
        n=150;p=0.01
        x=numpy.arange(n+1)
        lamda=n*p
        y=[func_poisson(lamda,xi) for xi in x]
        E=V=lamda
        pyplot.plot(x,y,label='P0 (%s), E(X)=%.2f, V(X)=%.2f'%(lamda,E,V))
        y=[func_binomial(n,xi,p) for xi in x]
        E=n*p
        V=n*p*(1-p)
        pyplot.plot(x,y,label='Bi (%s, %s), E(X)=%.2f, V(X)=%.2f'%(n,p,E,V))
        pyplot.xlim(xmax=20)
        pyplot.legend(loc='best')
        pyplot.xlabel('x', fontsize=20, fontname='serif')
        pyplot.ylabel('fraction', fontsize=20, fontname='serif')
        pyplot.title('Poisson vs binomial', fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.savefig('day6_povsbi.png')
        pyplot.show()

def func_gauss(mu,sigma,x):
        y0=1.0/(math.sqrt(2*math.pi)*sigma)
        return y0*numpy.exp(-pow(x-mu,2)/(2.0*sigma*sigma))

def gauss_dist():

        pyplot.figure(figsize=(11,7))
        mu=10;sigma=0.01
        x=numpy.linspace(mu-10*sigma,mu+10*sigma,2000)
        y=func_gauss(mu,sigma,x)
        pyplot.plot(x,y,label='N (%s, %s*%s)'%(mu,sigma,sigma))
        pyplot.legend(loc='best')
        pyplot.xlabel('x', fontsize=20, fontname='serif')
        pyplot.ylabel('fraction', fontsize=20, fontname='serif')
        pyplot.title('Gaussian distribution', fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.savefig('day6_gauss.png')
        pyplot.show()


def func_gamma(lamda,alpha,x):
        return (pow(lamda,alpha)/math.gamma(alpha))*pow(x,alpha-1)*numpy.exp(-lamda*x)

def func_chi(alpha,x):
        k=1.0/(pow(2.0,alpha/2.0)*math.gamma(alpha/2.0))
        return k*pow(x,alpha/2.0-1.0)*numpy.exp(-x/2.0)

def gamma_dist():

        pyplot.figure(figsize=(11,7))
        lamda=1.0;alpha=[1.0,2.0,3.0]
        x=numpy.linspace(0,9,100)

        for i in alpha:
                y=func_gamma(lamda,i,x)
                E=i/lamda
                V=i/(lamda*lamda)
                pyplot.plot(x,y,label='Ga (%s, %s), E(X)=%.2f, V(X)=%.2f'%(i,lamda,E,V))

        n=5
        alpha=n*0.5
        lamda=0.5
        y=func_gamma(lamda,alpha,x)
        E=alpha/lamda
        V=alpha/(lamda*lamda)
        pyplot.plot(x,y,label='Ga (%s, %s), E(X)=%.2f, V(X)=%.2f'%(alpha,lamda,E,V))

        alpha=n
        y=func_chi(alpha,x)
        E=alpha
        V=alpha*2.0
        pyplot.plot(x,y,label='Chi (%s), E(X)=%.2f, V(X)=%.2f'%(alpha,E,V))
        pyplot.legend(loc='best')
        pyplot.xlabel('x', fontsize=20, fontname='serif')
        pyplot.ylabel('fraction', fontsize=20, fontname='serif')
        pyplot.title('Gamma distribution', fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.savefig('day6_gamma.png')
        pyplot.show()

def func_t(alpha,x):
        k=(1.0/math.sqrt(alpha*math.pi))*math.gamma((alpha+1.0)/2.0)/math.gamma(alpha/2.0)
        return k*pow(1.0+x*x/alpha,-(alpha+1.0)/2.0)

def t_dist():

        pyplot.figure(figsize=(11,7))
        x=numpy.linspace(-10,10,2000)

        n=[2,4,10,100]
        for i in n:
                alpha=i-1
                V=1.0*alpha/(alpha-2)
                y=func_t(alpha,x)
                pyplot.plot(x,y,label='t (%s), V(X)=%.2f'%(alpha,V))

        mu=0;sigma=1
        x=numpy.linspace(mu-10*sigma,mu+10*sigma,2000)
        y=func_gauss(mu,sigma,x)
        pyplot.plot(x,y,label='N (%s, %s*%s)'%(mu,sigma,sigma))

        pyplot.legend(loc='best')
        pyplot.xlabel('x', fontsize=20, fontname='serif')
        pyplot.ylabel('fraction', fontsize=20, fontname='serif')
        pyplot.title('t distribution', fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.yticks(fontsize=20, fontname='serif')
        pyplot.savefig('day6_t.png')
        pyplot.show()

### main ###

if __name__== "__main__":

        binomial_dist()
        poisson_dist()
        gauss_dist()
        t_dist()
        gamma_dist()
