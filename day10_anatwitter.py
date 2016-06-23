#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import time
import datetime
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
import pandas
import pystan
import scipy.stats as stats
import seaborn

def gmllfit(cat):

    stan_code = """
data {
    int<lower=0> N_sample;
    int<lower=0> N_day;
    int<lower=0> N_hour;
    int<lower=0> N_sigma;
    int<lower=0> Y[N_sample];
    int<lower=0> day[N_sample];
    int<lower=0> hour[N_sample];
}
parameters {
    real beta;
    real rd[N_day];
    real rh[N_hour];
    real<lower=0> sigma[N_sigma];
}
transformed parameters{
    real<lower=0> lambda[N_sample];
    for (i in 1:N_sample) {
        lambda[i] <- exp(beta + rd[day[i]] + rh[hour[i]]);
    }
}
model {
    for (i in 1:N_sample) {
        Y[i] ~ poisson(lambda[i]);
    }
    beta ~ normal(0,100);
    rd ~ normal(0,sigma[1]);
    rh ~ normal(0,sigma[2]);
    for (k in 1:N_sigma) {
        sigma[k] ~ uniform(0, 10000);
    }
}
"""

    d=cat[:,0]-12
    h=cat[:,1]+1
    y=cat[:,2]
    N_sample=cat.shape[0]
    N_day=9 # 13th - 21th
    N_hour=24 # 0h - 23h
    N_sigma=2
    print N_sample
    stan_data = {'N_sample': N_sample,
                 'N_day': N_day,
                 'N_hour': N_hour,
                 'N_sigma': N_sigma,
                 'Y': y,
                 'day': d,
                 'hour': h
    }

    fit = pystan.stan(model_code=stan_code, data=stan_data, iter=3000, chains=4, thin=10, warmup=500, n_jobs=-1, algorithm="NUTS", verbose=False)

    data1=fit.extract(permuted=True)
    #names = fit.model_pars
    #n_param = numpy.sum([1 if len(x) == 0 else x[0] for x in fit.par_dims])
    #data2=fit.extract(permuted=False)

    #print(fit)
    fit.summary()
    #mean_list = numpy.array(fit.summary()['summary'])[:,0]

    #fit.plot()

    f, axes = pyplot.subplots(4, 2, figsize=(15, 16))
    seaborn.distplot(data1['beta'], hist=False, rug=True, ax=axes[0,0])
    seaborn.tsplot(data1['beta'],   alpha=0.8, lw=.5, ax=axes[0,1])
    axes[0, 0].set_title('beta')
    axes[0, 1].set_title('beta')
    for i in range(N_day):
        seaborn.distplot(data1['rd'][:,i], hist=False, rug=True, ax=axes[1,0])
        seaborn.tsplot(data1['rd'][:,i],   alpha=0.8, lw=.5, ax=axes[1,1])
    axes[1, 0].set_title('rd')
    axes[1, 1].set_title('rd')
    for i in range(N_hour):
        seaborn.distplot(data1['rh'][:,i], hist=False, rug=True, ax=axes[2,0])
        seaborn.tsplot(data1['rh'][:,i],   alpha=0.8, lw=.5, ax=axes[2,1])
    axes[2, 0].set_title('rh')
    axes[2, 1].set_title('rh')
    for i in range(N_sigma):
        seaborn.distplot(data1['sigma'][:,i], hist=False, rug=True, ax=axes[3,0])
        seaborn.tsplot(data1['sigma'][:,i],   alpha=0.8, lw=.5, ax=axes[3,1])
    axes[3, 0].set_title('sigma')
    axes[3, 1].set_title('sigma')

    pyplot.savefig('day10_moso2.png')
    #pyplot.show()

    f, axes = pyplot.subplots(1, 2, figsize=(15, 4))
    seaborn.distplot(data1['lp__'], hist=False, rug=True, ax=axes[0])
    seaborn.tsplot(data1['lp__'],   alpha=0.8, lw=.5, ax=axes[1])
    axes[0].set_title("Histgram of likelihood.")
    axes[1].set_title("Traceplot of likelihood.")
    pyplot.savefig('day10_moso3.png')
    #plt.show()

    return data1

def makegraph(cat):

    fig = pyplot.figure(figsize=(15,8))
    pyplot.subplot(121)
    pyplot.scatter(cat[:,1][numpy.where((cat[:,2]>0))],cat[:,2][numpy.where((cat[:,2]>0))],s=60,alpha=0.8)
    pyplot.yscale("log")
    pyplot.ylim(0.9,max(cat[:,2])+30.)
    pyplot.xlim(-1.,max(cat[:,1])+1.)
    pyplot.ylabel('counts of tweets', fontsize=20)
    pyplot.xlabel('hour', fontsize=20)
    pyplot.xticks(fontsize=20)
    pyplot.yticks(fontsize=20)
    pyplot.subplot(122)
    pyplot.scatter(cat[:,0][numpy.where((cat[:,2]>0))],cat[:,2][numpy.where((cat[:,2]>0))],s=60,alpha=0.8)
    pyplot.yscale("log")
    pyplot.ylim(0.9,max(cat[:,2])+30.)
    pyplot.xlim(dmin+0.5,dmax-0.5)
    pyplot.ylabel('counts of tweets', fontsize=20)
    pyplot.xlabel('2016/06/XX', fontsize=20)
    pyplot.xticks(fontsize=20)
    pyplot.yticks(fontsize=20)
    pyplot.savefig('day10_moso0a.png')
    pyplot.show()

    fig = pyplot.figure(figsize=(17,8))
    pyplot.subplot(121)
    pyplot.scatter(cat[:,1][numpy.where((cat[:,2]>0))],cat[:,2][numpy.where((cat[:,2]>0))],c=cat[:,0][numpy.where((cat[:,2]>0))],cmap=cm.jet,s=60,alpha=0.8)
    cb1=pyplot.colorbar(boundaries=numpy.arange(dmin+1,dmax+1))
    cb1.set_label('2016/06/XX', fontsize=20)
    cb1.ax.tick_params(labelsize=20)
    pyplot.yscale("log")
    pyplot.ylim(0.9,max(cat[:,2])+30.)
    pyplot.xlim(-1.,max(cat[:,1])+1.)
    pyplot.ylabel('counts of tweets', fontsize=20)
    pyplot.xlabel('hour', fontsize=20)
    pyplot.xticks(fontsize=20)
    pyplot.yticks(fontsize=20)
    pyplot.subplot(122)
    pyplot.scatter(cat[:,0][numpy.where((cat[:,2]>0))],cat[:,2][numpy.where((cat[:,2]>0))],c=cat[:,1][numpy.where((cat[:,2]>0))],cmap=cm.jet,s=60,alpha=0.8)
    cb2=pyplot.colorbar(boundaries=numpy.arange(25))
    cb2.set_label('hour', fontsize=20)
    cb2.ax.tick_params(labelsize=20)
    pyplot.yscale("log")
    pyplot.ylim(0.9,max(cat[:,2])+30.)
    pyplot.xlim(dmin+0.5,dmax-0.5)
    pyplot.ylabel('counts of tweets', fontsize=20)
    pyplot.xlabel('2016/06/XX', fontsize=20)
    pyplot.xticks(fontsize=20)
    pyplot.yticks(fontsize=20)
    pyplot.savefig('day10_moso0b.png')
    pyplot.show()

    exit()

if __name__== "__main__":

    #a=datetime.datetime(2016, 6, 21, 0, 0, 0)
    #epoch = int(time.mktime(a.timetuple()))

    data=pandas.read_csv('./tweet_moso.csv')
    n=int(len(data['created_at']))-1

    """
    bins=int((data['created_at'][0]-data['created_at'][n])/3600.)
    print bins
    pyplot.hist(data['created_at'],bins=bins)
    pyplot.xlim(data['created_at'][n],data['created_at'][0])
    pyplot.xlabel('seconds')
    pyplot.ylabel('N')
    pyplot.savefig('day10_moso1.png')
    pyplot.show()
    """

    print datetime.datetime.fromtimestamp(data['created_at'][0])
    print datetime.datetime.fromtimestamp(data['created_at'][n])
    #print (data['created_at'][0]-data['created_at'][n])/3600./24.

    dmax=datetime.datetime.fromtimestamp(data['created_at'][0]).day
    hmax=datetime.datetime.fromtimestamp(data['created_at'][0]).hour
    dmin=datetime.datetime.fromtimestamp(data['created_at'][n]).day
    hmin=datetime.datetime.fromtimestamp(data['created_at'][n]).hour

    cat=[]
    for d in range(dmin+1,dmax):
        for h in range(24):
            i=0
            for epoch in data['created_at']:

                day=datetime.datetime.fromtimestamp(epoch).day
                hour=datetime.datetime.fromtimestamp(epoch).hour

                if d==day and h==hour:
                    i+=1
            cat.append([d,h,i])

    cat=numpy.array(cat)
    #makegraph(cat)
    result=gmllfit(cat)

    beta=numpy.median(result['beta'])
    N_hour=24
    N_day=9
    #print len(result['rd'][:,0]),len(result['rd'][0,:]),len(result['rh'][:,0]),len(result['rh'][0,:])

    lambda1=[]
    for t in range(N_hour):
        a=[]
        for i in range(len(result['rd'])):
            for j in range(N_day):
                for s in range(len(result['rh'])):
                    a0=numpy.exp(beta + result['rd'][i,j] + result['rh'][s,t])
                    a.append(a0)

        b0=[stats.scoreatpercentile(a, 2.5),stats.scoreatpercentile(a, 25),stats.scoreatpercentile(a, 50),stats.scoreatpercentile(a, 75),stats.scoreatpercentile(a, 97.5)]
        lambda1.append(b0)

    lambda1=numpy.array(lambda1)
    x1=numpy.arange(N_hour)

    lambda2=[]
    for t in range(N_day):
        a=[]
        for i in range(len(result['rh'])):
            for j in range(N_hour):
                for s in range(len(result['rd'])):
                    a0=numpy.exp(beta + result['rh'][i,j] + result['rd'][s,t])
                    a.append(a0)

        b0=[stats.scoreatpercentile(a, 2.5),stats.scoreatpercentile(a, 25),stats.scoreatpercentile(a, 50),stats.scoreatpercentile(a, 75),stats.scoreatpercentile(a, 97.5)]
        lambda2.append(b0)

    lambda2=numpy.array(lambda2)
    x2=numpy.arange(N_day)+13

    fig = pyplot.figure(figsize=(17,8))
    pyplot.subplot(121)
    pyplot.fill_between(x1,lambda1[:,0],lambda1[:,4],alpha=0.3)
    pyplot.fill_between(x1,lambda1[:,1],lambda1[:,3],alpha=0.6)
    pyplot.scatter(cat[:,1][numpy.where((cat[:,2]>0))],cat[:,2][numpy.where((cat[:,2]>0))],c=cat[:,0][numpy.where((cat[:,2]>0))],cmap=cm.jet,s=60,alpha=0.8)
    pyplot.plot(x1,lambda1[:,2],'k',lw=3)
    cb1=pyplot.colorbar(boundaries=numpy.arange(dmin+1,dmax+1))
    cb1.set_label('2016/06/XX', fontsize=20)
    cb1.ax.tick_params(labelsize=20)
    pyplot.yscale("log")
    pyplot.ylim(0.9,max(cat[:,2])+30.)
    pyplot.xlim(-1.,max(cat[:,1])+1.)
    pyplot.ylabel('counts of tweets', fontsize=20)
    pyplot.xlabel('hour', fontsize=20)
    pyplot.xticks(fontsize=20)
    pyplot.yticks(fontsize=20)
    pyplot.subplot(122)
    pyplot.fill_between(x2,lambda2[:,0],lambda2[:,4],alpha=0.3)
    pyplot.fill_between(x2,lambda2[:,1],lambda2[:,3],alpha=0.6)
    pyplot.scatter(cat[:,0][numpy.where((cat[:,2]>0))],cat[:,2][numpy.where((cat[:,2]>0))],c=cat[:,1][numpy.where((cat[:,2]>0))],cmap=cm.jet,s=60,alpha=0.8)
    pyplot.plot(x2,lambda2[:,2],'k',lw=3)
    cb2=pyplot.colorbar(boundaries=numpy.arange(25))
    cb2.set_label('hour', fontsize=20)
    cb2.ax.tick_params(labelsize=20)
    pyplot.yscale("log")
    pyplot.ylim(0.9,max(cat[:,2])+30.)
    pyplot.xlim(dmin+0.5,dmax-0.5)
    pyplot.ylabel('counts of tweets', fontsize=20)
    pyplot.xlabel('2016/06/XX', fontsize=20)
    pyplot.xticks(fontsize=20)
    pyplot.yticks(fontsize=20)
    pyplot.savefig('day10_moso4.png')
    #pyplot.show()
