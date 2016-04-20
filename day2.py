#! /usr/bin/env python

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

if __name__== "__main__":

        data1=np.genfromtxt('./science12.dat')
        data2=np.genfromtxt('./mathematics12.dat')
        data3=np.genfromtxt('./reading12.dat')

        x1=data1[:,1]
        x2=data2[:,1]
        x3=data3[:,1]

        x1mean=np.mean(x1)
        x1med=np.median(x1)
        x1mode=stats.mode(x1)
        x1std=np.std(x1)
        x1var=np.var(x1)
        x1q1=stats.scoreatpercentile(x1, 25)
        x1q3=stats.scoreatpercentile(x1, 75)
        x1qd=(x1q3-x1q1)/2.0
        x1skew=stats.skew(x1)
        x1kurtosis=stats.kurtosis(x1)

        x2mean=np.mean(x2)
        x2med=np.median(x2)
        x2mode=stats.mode(x2)
        x2std=np.std(x2)
        x2var=np.var(x2)
        x2q1=stats.scoreatpercentile(x2, 25)
        x2q3=stats.scoreatpercentile(x2, 75)
        x2qd=(x2q3-x2q1)/2.0
        x2skew=stats.skew(x2)
        x2kurtosis=stats.kurtosis(x2)

        x3mean=np.mean(x3)
        x3med=np.median(x3)
        x3mode=stats.mode(x3)
        x3std=np.std(x3)
        x3var=np.var(x3)
        x3q1=stats.scoreatpercentile(x3, 25)
        x3q3=stats.scoreatpercentile(x3, 75)
        x3qd=(x3q3-x3q1)/2.0
        x3skew=stats.skew(x3)
        x3kurtosis=stats.kurtosis(x3)

        fig=plt.figure(figsize=(7,9))

        xmin=300;xmax=650;ymin=0;ymax=15
        myrange=[xmin,xmax,ymin,ymax]
        plt.subplot(3,1,1)
        plt.hist(x1, bins=20, range=(300,600), normed=False, stacked=False, fill=True, facecolor='g', alpha=0.8)
        plt.text(308,13.5,'Science',ha='left',va='center', color='g')
        plt.text(308,12.4,'N=%d'%(len(x1)),ha='left',va='center')
        plt.text(308,11.3,'mean=%.2f'%(x1mean),ha='left',va='center')
        plt.text(308,10.2,'median=%d'%(x1med),ha='left',va='center')
        plt.text(308,9.1,'mode=%d'%(x1mode[0]),ha='left',va='center')
        plt.text(308,8.0,'std=%.2f'%(x1std),ha='left',va='center')
        plt.text(308,6.9,'var=%.2f'%(x1var),ha='left',va='center')
        plt.text(308,5.8,'QD=%.1f'%(x1qd),ha='left',va='center')
        plt.text(308,4.7,'skew=%.2f'%(x1skew),ha='left',va='center')
        plt.text(308,3.6,'kurt=%.2f'%(x1kurtosis),ha='left',va='center')
        plt.text(547,12.5,'JP(547)',ha='center',va='center')
        a=[547,547]
        b=[9.7,11.7]
        plt.plot(a,b,'k-',lw=1.5)
        plt.text(521,13.8,'AU(521)',ha='center',va='center')
        a=[521,521]
        b=[11,13]
        plt.plot(a,b,'k-',lw=1.5)
        plt.axis(myrange)
        plt.ylabel("n")
        plt.subplot(3,1,2)
        plt.hist(x2, bins=20, range=(300,600), normed=False, stacked=False, fill=True, facecolor='r', alpha=0.8)
        plt.text(308,13.5,'Mathematics',ha='left',va='center', color='r')
        plt.text(308,12.4,'N=%d'%(len(x2)),ha='left',va='center')
        plt.text(308,11.3,'mean=%.2f'%(x2mean),ha='left',va='center')
        plt.text(308,10.2,'median=%d'%(x2med),ha='left',va='center')
        plt.text(308,9.1,'mode=%d'%(x2mode[0]),ha='left',va='center')
        plt.text(308,8.0,'std=%.2f'%(x2std),ha='left',va='center')
        plt.text(308,6.9,'var=%.2f'%(x2var),ha='left',va='center')
        plt.text(308,5.8,'QD=%.1f'%(x2qd),ha='left',va='center')
        plt.text(308,4.7,'skew=%.2f'%(x2skew),ha='left',va='center')
        plt.text(308,3.6,'kurt=%.2f'%(x2kurtosis),ha='left',va='center')
        plt.text(536,12.5,'JP(536)',ha='center',va='center')
        a=[536,536]
        b=[9.7,11.7]
        plt.plot(a,b,'k-',lw=1.5)
        plt.text(504,13.8,'AU(504)',ha='center',va='center')
        a=[504,504]
        b=[11,13]
        plt.plot(a,b,'k-',lw=1.5)
        plt.axis(myrange)
        plt.ylabel("n")
        plt.subplot(3,1,3)
        plt.hist(x3, bins=20, range=(300,600), normed=False, stacked=False, fill=True, facecolor='b', alpha=0.8)
        plt.text(308,13.5,'Reading',ha='left',va='center', color='b')
        plt.text(308,12.4,'N=%d'%(len(x3)),ha='left',va='center')
        plt.text(308,11.3,'mean=%.2f'%(x3mean),ha='left',va='center')
        plt.text(308,10.2,'median=%d'%(x3med),ha='left',va='center')
        plt.text(308,9.1,'mode=%d'%(x3mode[0]),ha='left',va='center')
        plt.text(308,8.0,'std=%.2f'%(x3std),ha='left',va='center')
        plt.text(308,6.9,'var=%.2f'%(x3var),ha='left',va='center')
        plt.text(308,5.8,'QD=%.1f'%(x3qd),ha='left',va='center')
        plt.text(308,4.7,'skew=%.2f'%(x3skew),ha='left',va='center')
        plt.text(308,3.6,'kurt=%.2f'%(x3kurtosis),ha='left',va='center')
        plt.text(538,12.5,'JP(538)',ha='center',va='center')
        a=[538,538]
        b=[9.7,11.7]
        plt.plot(a,b,'k-',lw=1.5)
        plt.text(512,13.8,'AU(512)',ha='center',va='center')
        a=[512,512]
        b=[11,13]
        plt.plot(a,b,'k-',lw=1.5)
        plt.axis(myrange)
        plt.xlabel("score")
        plt.ylabel("n")
        fig.tight_layout()
        plt.show()
        fig.savefig('day2.png')
