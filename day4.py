#! /usr/bin/env python

import numpy
import matplotlib.pyplot as pyplot
import scipy.optimize

## Time sequence of pisa test ##

def func(x,A,B): return A+B*x

def fit_func(param,x,y,w):
    A,B=param
    residual=(y-func(x,A,B))/w
    return residual

def leastsq(x0,y0,w0):

    x=numpy.array(x0,dtype=numpy.float)
    y=numpy.array(y0,dtype=numpy.float)
    w=numpy.array(w0,dtype=numpy.float)

    param0=numpy.array([3.0,-5000.0])
    result=scipy.optimize.leastsq(fit_func,param0,args=(x,y,w),full_output=True)
    #print result[0]
    A,B=result[0]
    A_std=numpy.sqrt(result[1][0,0])
    B_std=numpy.sqrt(result[1][1,1])
    print A,A_std,B,B_std
    return A,A_std,B,B_std

def readfile():

    ### Science ###
    
    data1=numpy.genfromtxt('./science_tseq.dat')
    sciau1=[2006,2009,2012]
    sciau2=[];sciau3=[]
    i=0
    for j in data1[0]:
        if i==1 or i==3 or i==5: sciau2.append(j)
        if i==2 or i==4 or i==6: sciau3.append(j)
        i+=1
    scijp1=[2006,2009,2012]
    scijp2=[];scijp3=[]
    i=0
    for j in data1[17]:
        if i==1 or i==3 or i==5: scijp2.append(j)
        if i==2 or i==4 or i==6: scijp3.append(j)
        i+=1

    ### Mathematics ###

    data2=numpy.genfromtxt('./mathematics_tseq.dat')
    matau1=[2003,2006,2009,2012]
    matau2=[];matau3=[]
    i=0
    for j in data2[0]:
        if i==1 or i==3 or i==5 or i==7: matau2.append(j)
        if i==2 or i==4 or i==6 or i==8: matau3.append(j)
        i+=1
    matjp1=[2003,2006,2009,2012]
    matjp2=[];matjp3=[]
    i=0
    for j in data2[17]:
        if i==1 or i==3 or i==5 or i==7: matjp2.append(j)
        if i==2 or i==4 or i==6 or i==8: matjp3.append(j)
        i+=1

    ### Reading ###

    data3=numpy.genfromtxt('./reading_tseq.dat')
    readau1=[2000,2003,2006,2009,2012]
    readau2=[];readau3=[]
    i=0
    for j in data3[0]:
        if i==1 or i==3 or i==5 or i==7 or i==9: readau2.append(j)
        if i==2 or i==4 or i==6 or i==8 or i==10: readau3.append(j)
        i+=1
    readjp1=[2000,2003,2006,2009,2012]
    readjp2=[];readjp3=[]
    i=0
    for j in data3[17]:
        if i==1 or i==3 or i==5 or i==7 or i==9: readjp2.append(j)
        if i==2 or i==4 or i==6 or i==8 or i==10: readjp3.append(j)
        i+=1

    return sciau1,sciau2,sciau3,scijp1,scijp2,scijp3,matau1,matau2,matau3,matjp1,matjp2,matjp3,readau1,readau2,readau3,readjp1,readjp2,readjp3

if __name__== "__main__":

    ### reading files ###

    sciau1,sciau2,sciau3,scijp1,scijp2,scijp3,matau1,matau2,matau3,matjp1,matjp2,matjp3,readau1,readau2,readau3,readjp1,readjp2,readjp3=readfile()

    ### least-square fitting ###

    A_scijp,A_std_scijp,B_scijp,B_std_scijp=leastsq(scijp1,scijp2,scijp3)
    A_sciau,A_std_sciau,B_sciau,B_std_sciau=leastsq(sciau1,sciau2,sciau3)
    A_matjp,A_std_matjp,B_matjp,B_std_matjp=leastsq(matjp1,matjp2,matjp3)
    A_matau,A_std_matau,B_matau,B_std_matau=leastsq(matau1,matau2,matau3)
    A_readjp,A_std_readjp,B_readjp,B_std_readjp=leastsq(readjp1,readjp2,readjp3)
    A_readau,A_std_readau,B_readau,B_std_readau=leastsq(readau1,readau2,readau3)


    fig=pyplot.figure(figsize=(7,9))

    xmin=1999;xmax=2016;ymin=480;ymax=560
    x=numpy.arange(xmin,xmax,0.001)
    y_scijp=A_scijp+B_scijp*x
    y_sciau=A_sciau+B_sciau*x
    y_matjp=A_matjp+B_matjp*x
    y_matau=A_matau+B_matau*x
    y_readjp=A_readjp+B_readjp*x
    y_readau=A_readau+B_readau*x
    myrange=[xmin,xmax,ymin,ymax]
    pyplot.subplot(3,1,1)
    pyplot.errorbar(sciau1,sciau2,yerr=sciau3,color='b',fmt='o', capsize=4, ms=4, label='AU')
    pyplot.errorbar(scijp1,scijp2,yerr=scijp3,color='r',fmt='o', capsize=4, ms=4, label='JP')
    pyplot.plot(x,y_scijp,color='r')
    pyplot.plot(x,y_sciau,color='b')
    pyplot.text(1999.5,550,'Science',ha='left',va='center', color='k')
    pyplot.text(2003,497,'AU: y=%.2f($\pm$%.2f)%.2f($\pm$%.2f)x'%(round(A_sciau,2),round(A_std_sciau,2),round(B_sciau,2),round(B_std_sciau,2)),ha='left',va='center')
    pyplot.text(2003,489,'JP: y=%.2f($\pm$%.2f)+%.2f($\pm$%.2f)x'%(round(A_scijp,2),round(A_std_scijp,2),round(B_scijp,2),round(B_std_scijp,2)),ha='left',va='center')
    pyplot.axis(myrange)
    pyplot.ylabel("score")
    pyplot.title("y=A+Bx")
    pyplot.legend(loc='lower left')
    pyplot.subplot(3,1,2)
    pyplot.errorbar(matau1,matau2,yerr=matau3,color='b',fmt='o', capsize=4, ms=4, label='AU')
    pyplot.errorbar(matjp1,matjp2,yerr=matjp3,color='r',fmt='o', capsize=4, ms=4, label='JP')
    pyplot.plot(x,y_matjp,color='r')
    pyplot.plot(x,y_matau,color='b')
    pyplot.text(1999.5,550,'Mathematics',ha='left',va='center', color='k')
    pyplot.text(2003,496,'AU: y=%.2f($\pm$%.2f)%.2f($\pm$%.2f)x'%(round(A_matau,2),round(A_std_matau,2),round(B_matau,2),round(B_std_matau,2)),ha='left',va='center')
    pyplot.text(2003,488,'JP: y=%.2f($\pm$%.2f)+%.2f($\pm$%.2f)x'%(round(A_matjp,2),round(A_std_matjp,2),round(B_matjp,2),round(B_std_matjp,2)),ha='left',va='center')
    pyplot.axis(myrange)
    pyplot.ylabel("score")
    pyplot.legend(loc='lower left')
    pyplot.subplot(3,1,3)
    pyplot.errorbar(readau1,readau2,yerr=readau3,color='b',fmt='o', capsize=4, ms=4, label='AU')
    pyplot.errorbar(readjp1,readjp2,yerr=readjp3,color='r',fmt='o', capsize=4, ms=4, label='JP')
    pyplot.plot(x,y_readjp,color='r')
    pyplot.plot(x,y_readau,color='b')
    pyplot.text(1999.5,550,'Reading',ha='left',va='center', color='k')
    pyplot.text(2003,553,'AU: y=%.2f($\pm$%.2f)%.2f($\pm$%.2f)x'%(round(A_readau,2),round(A_std_readau,2),round(B_readau,2),round(B_std_readau,2)),ha='left',va='center')
    pyplot.text(2003,545,'JP: y=%.2f($\pm$%.2f)+%.2f($\pm$%.2f)x'%(round(A_readjp,2),round(A_std_readjp,2),round(B_readjp,2),round(B_std_readjp,2)),ha='left',va='center')
    pyplot.axis(myrange)
    pyplot.xlabel("year")
    pyplot.ylabel("score")
    pyplot.legend(loc='lower left')
    pyplot.show()
    fig.tight_layout()
    fig.savefig('day4.png')
