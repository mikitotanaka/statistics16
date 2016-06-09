#!/usr/bin/env python

import numpy
import scipy.stats as stats
import matplotlib.pyplot as pyplot

def continous():

    print "continuous"

    data=numpy.genfromtxt("./akbheight.dat")

    nsample=int(len(data))
    min=numpy.min(data)
    max=numpy.max(data)
    bins=max-min
    mean=numpy.mean(data)
    std=numpy.std(data, ddof=1)
    print nsample,mean,std

    pyplot.figure(figsize=(11,7))
    pyplot.hist(data,bins=bins)
    pyplot.xlabel("cm", fontsize=20, fontname='serif')
    pyplot.ylabel("N", fontsize=20, fontname='serif')
    pyplot.title("Height distribution of AKB members", fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.text(168,7.1,r"nsample$=%d$"%(nsample),fontsize=20, fontname='serif')
    pyplot.text(168,6.5,r"$\mu=%.1f$cm"%(mean),fontsize=20, fontname='serif')
    pyplot.text(168,6.0,r"$\sigma=%.1f$cm"%(std),fontsize=20, fontname='serif')
    pyplot.savefig("day8_akbheight.png")
    pyplot.show()

    # reshaping observting data.

    data_o=numpy.zeros(4)
    for x in data:
        if x < mean-std: data_o[0]+=1
        if x > mean-std and x < mean: data_o[1]+=1
        if x > mean and x < mean+std: data_o[2]+=1
        if x > mean+std: data_o[3]+=1

    print data_o

    # shaping theoretical data assuming Gauss distribution.

    data_e=numpy.zeros(4)
    data_e[0]=nsample*stats.norm.cdf(mean-std,loc=mean,scale=std)
    data_e[1]=nsample*(stats.norm.cdf(mean,loc=mean,scale=std)-stats.norm.cdf(mean-std,loc=mean,scale=std))
    data_e[2]=nsample*(stats.norm.cdf(mean+std,loc=mean,scale=std)-stats.norm.cdf(mean,loc=mean,scale=std))
    data_e[3]=nsample*(1.-stats.norm.cdf(mean+std,loc=mean,scale=std))

    print data_e

    # calculating chi square and p-value.

    ddof=2 # the number of parameters
    df=int(len(data_o))-1-ddof
    chisq,pvalue=stats.chisquare(data_o, f_exp=data_e, ddof=ddof)
    print chisq/df,pvalue
    print 1.-stats.chi2.cdf(chisq,df)


def discrete():

    print "discrete"

    nsample=100
    n=10;p=1./6
    m=n+1

    # shaping theoretical data assuming Binomial distribution.

    data_e=numpy.zeros(m)
    for i in range(m):
        data_e[i]=stats.binom.pmf(i,n,p)*nsample

    print data_e

    # reshapeing too small bins (less than 5) of theoretical data.

    data_e2=numpy.array([])
    j=0;y=0;num=[]
    for i in range(len(data_e)):
        x=data_e[i]
        if x > 5.:
            data_e2=numpy.append(data_e2,x)
            j+=1
        else:
            num.append(i)
            data_e2[j-1]+=x

    #print num
    print data_e2

    # creating observting data.

    data_o=numpy.zeros(m)
    for i in range(nsample):
        a=0
        for j in numpy.random.randint(0,6,n):
            if j==5:a+=1
        data_o[a]+=1

    print data_o

    # reshaping observting data.

    data_o2=numpy.array([])
    x=0
    for i in range(len(data_o)):
        x=data_o[i]
        if i < num[0]:
            data_o2=numpy.append(data_o2,x)
        else:
            data_o2[num[0]-1]+=x

    print data_o2

    # calculating chi square and p-value.

    ddof=0 # the number of parameters
    df=int(len(data_o2))-1-ddof
    chisq,pvalue=stats.chisquare(data_o2, f_exp=data_e2, ddof=ddof)
    print chisq/df,pvalue
    print "d =",df
    print 1.-stats.chi2.cdf(chisq,df)

    # simulation

    nloop=100
    vstack_tmp=[]
    for j in xrange(nloop):

        # creating observting data.

        data_o=numpy.zeros(m)
        for i in range(nsample):
            a=0
            for j in numpy.random.randint(0,6,n):
                if j==5:a+=1
            data_o[a]+=1

        # reshaping observting data.

        data_o2=numpy.array([])
        x=0
        for i in range(len(data_o)):
            x=data_o[i]
            if i < num[0]:
                data_o2=numpy.append(data_o2,x)
            else:
                data_o2[num[0]-1]+=x

        # calculating chi square and p-value.

        ddof=0 # the number of parameters
        df=int(len(data_o2))-1-ddof
        chisq,pvalue=stats.chisquare(data_o2, f_exp=data_e2, ddof=ddof)
        vstack_tmp.append([chisq/df,pvalue])

    chidist=numpy.vstack(vstack_tmp)

    fig=pyplot.figure(figsize=(7,9))
    pyplot.subplot(211)
    pyplot.hist(chidist[:,0],bins=20,range=(0,10))
    pyplot.xlabel("reduced chi squared",fontsize=18, fontname='serif')
    pyplot.ylabel("N",fontsize=18, fontname='serif')
    pyplot.title("Normal Dice",fontsize=18, fontname='serif')
    pyplot.xticks(fontsize=18, fontname='serif')
    pyplot.yticks(fontsize=18, fontname='serif')
    pyplot.subplot(212)
    pyplot.hist(chidist[:,1],bins=20,range=(0,0.2))
    pyplot.xlabel("p-value",fontsize=18, fontname='serif')
    pyplot.ylabel("N",fontsize=18, fontname='serif')
    pyplot.xticks(fontsize=18, fontname='serif')
    pyplot.yticks(fontsize=18, fontname='serif')
    pyplot.savefig("day8_chitest_discrete_normaldice.png")
    pyplot.show()


    ## Ikasama ##


    # creating observting data.

    data_o=numpy.zeros(m)
    for i in range(nsample):
        a=0
        for j in numpy.random.choice(6,n,p=[0.1,0.1,0.19,0.2,0.2,0.21]):
            if j==5:a+=1
        data_o[a]+=1

    print data_o

    # reshaping observting data.

    data_o2=numpy.array([])
    x=0
    for i in range(len(data_o)):
        x=data_o[i]
        if i < num[0]:
            data_o2=numpy.append(data_o2,x)
        else:
            data_o2[num[0]-1]+=x

    print data_o2

    # calculating chi square and p-value.

    ddof=0 # the number of parameters
    df=int(len(data_o2))-1-ddof
    chisq,pvalue=stats.chisquare(data_o2, f_exp=data_e2, ddof=ddof)
    print chisq/df,pvalue
    print 1.-stats.chi2.cdf(chisq,df)

    # simulation

    nloop=100
    vstack_tmp=[]
    for j in xrange(nloop):

        # creating observting data.

        data_o=numpy.zeros(m)
        for i in range(nsample):
            a=0
            for j in numpy.random.choice(6,n,p=[0.1,0.1,0.19,0.2,0.2,0.21]):
                if j==5:a+=1
            data_o[a]+=1

        # reshaping observting data.

        data_o2=numpy.array([])
        x=0
        for i in range(len(data_o)):
            x=data_o[i]
            if i < num[0]:
                data_o2=numpy.append(data_o2,x)
            else:
                data_o2[num[0]-1]+=x

        # calculating chi square and p-value.

        ddof=0 # the number of parameters
        df=int(len(data_o2))-1-ddof
        chisq,pvalue=stats.chisquare(data_o2, f_exp=data_e2, ddof=ddof)
        vstack_tmp.append([chisq/df,pvalue])

    chidist=numpy.vstack(vstack_tmp)

    fig=pyplot.figure(figsize=(7,9))
    pyplot.subplot(211)
    pyplot.hist(chidist[:,0],bins=20,range=(0,10))
    pyplot.xlabel("reduced chi squared",fontsize=18, fontname='serif')
    pyplot.ylabel("N",fontsize=18, fontname='serif')
    pyplot.title("Ikasama Dice",fontsize=18, fontname='serif')
    pyplot.xticks(fontsize=18, fontname='serif')
    pyplot.yticks(fontsize=18, fontname='serif')
    pyplot.subplot(212)
    pyplot.hist(chidist[:,1],bins=20,range=(0,0.2))
    pyplot.xlabel("p-value",fontsize=18, fontname='serif')
    pyplot.ylabel("N",fontsize=18, fontname='serif')
    pyplot.xticks(fontsize=18, fontname='serif')
    pyplot.yticks(fontsize=18, fontname='serif')
    pyplot.savefig("day8_chitest_discrete_ikasamadice.png")
    pyplot.show()


if __name__== "__main__":

    #continous()
    discrete()

    """
    fig=pyplot.figure(figsize=(9,7))
    x=numpy.linspace(2.19,8,200)
    pyplot.fill_between(x,stats.chi2.pdf(x,1),alpha=0.5)
    x=numpy.linspace(0,8,200)
    pyplot.plot(x,stats.chi2.pdf(x,1),lw=3,label="$d=1$")
    pyplot.plot(x,stats.chi2.pdf(x,2),lw=3,label="$d=2$")
    pyplot.plot(x,stats.chi2.pdf(x,3),lw=3,label="$d=3$")
    pyplot.plot(x,stats.chi2.pdf(x,4),lw=3,label="$d=4$")
    pyplot.plot(x,stats.chi2.pdf(x,5),lw=3,label="$d=5$")
    pyplot.legend()
    pyplot.xlim(0,8)
    pyplot.ylim(0,0.55)
    pyplot.xlabel("chi squared",fontsize=20, fontname='serif')
    pyplot.xticks(fontsize=20, fontname='serif')
    pyplot.yticks(fontsize=20, fontname='serif')
    pyplot.savefig("chisq_dist.png")
    pyplot.show()
    """
