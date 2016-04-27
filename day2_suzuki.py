# coding: utf-8
import sys
sys.path.append("/Users/masa/Ureka/variants/common/lib/python2.7/site-packages")
sys.path.append("/Users/masa/Ureka/python/lib/python2.7/site-packages")
#print sys.path
import numpy as np
import scipy.stats as stats
import xlrd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#from mpl_toolkits.mplot3d.axes3d import Axes3D
#import csv
import time

#import calc_toukei as ta




if __name__=="__main__":

    start_time = time.time()
    
    print "start reading data"

    
    
    #====== read data ==================#
    FILE = "cinii.xlsx"
    book = xlrd.open_workbook(FILE)

    print 'number of sheets:', book.nsheets

    s=[0, 0]
    i=0
    print 'sheets:'
    for s[i] in book.sheets():
        print '%s %sx%s' % (s[i].name, s[i].nrows, s[i].ncols)
        i+=1
        #print s

    sheet = book.sheet_by_name(s[0].name)
        
    data = sheet.col_values(1)

    #print data

    #======== calculation ===================#
    mean = np.mean(data)
    print mean

    median = np.median(data)
    print median

    mode = stats.mode(data)
    mode = [mode[0][0], mode[1][0]]
    print mode[0], mode[1]

    var = np.var(data)
    print var

    std = np.std(data)
    print std

    quad_var = (stats.scoreatpercentile(data, 75) - stats.scoreatpercentile(data, 25))/2.0 
    print quad_var

    skew = stats.skew(data) 
    print skew

    kurt = stats.kurtosis(data)
    print kurt

    #======== plot ===============================#
    Y_data = [ 0 for i in range(0, int(max(data)+1),1)]
    X_data = [ i for i in range(0, int(max(data)+1),1)]

    for i in range(0, len(data),1):
        
        Y_data[int(data[i])] += 1

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(111)
    ax.set_xlim(0.0, max(data))
    sns.distplot(data, kde=False, rug=False)
    ax.set_title('Distribution of the number of literatures', size=25)
    ax.set_xlabel('the number of literatures', size=12)
    ax.set_ylabel('the number fo universities', size=12)
    plt.text(8.0e+4,1100,'mean=%.2f'%(mean),ha='left',va='center')
    plt.text(8.0e+4,1050,'median=%.2f'%(median),ha='left',va='center')
    plt.text(8.0e+4,1000,'variance=%.2f'%(var),ha='left',va='center')
    plt.text(8.0e+4,950,'standard deviation=%.2f'%(std),ha='left',va='center')
    plt.text(8.0e+4,900,'quartile deviation=%.2f'%(quad_var),ha='left',va='center')
    plt.text(8.0e+4,850,'mode=%.2f'%(mode[0]),ha='left',va='center')
    plt.text(8.0e+4,800,'skewness=%.2f'%(skew),ha='left',va='center')
    plt.text(8.0e+4,750,'kuriosis=%.2f'%(kurt),ha='left',va='center')
    plt.savefig("dens_data0.png", format="png", dpi=500)
    sns.plt.show()
    
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(111)
    ax.set_xlim(0.0, max(data))
    sns.distplot(data, kde=True, rug=False)
    plt.savefig("dens_data1.png", format="png", dpi=500)
    sns.plt.show()

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(111)
    ax.set_xlim(0.0, max(data))
    sns.distplot(data, kde=False, rug=True)
    plt.savefig("dens_data2.png", format="png", dpi=500)
    sns.plt.show()
    

    #========= get time ==========================#
    end_time = time.time()
    dif=end_time-start_time
    hour = int((dif)/3600.0)
    minute=int((dif-3600.0*hour)/60.0)
    second=dif-3600.0*hour-60.0*minute
    print "time =", (end_time - start_time), "[sec]"
    print "time =", str(hour)+":"+str(minute)+":"+str(second)













