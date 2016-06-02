# coding: utf-8
import sys
sys.path.append("/Users/masa/Ureka/variants/common/lib/python2.7/site-packages")
sys.path.append("/Users/masa/Ureka/python/lib/python2.7/site-packages")
#print sys.path
import numpy 
import matplotlib.pyplot as plt
import seaborn 
import scipy.interpolate 
import scipy.optimize
import time

from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)


def func(x, A, B):

    func = numpy.sqrt( pow(A,2.0)*pow(x,2.0)/( pow(x,2.0) + pow(B,2.0) ) )
    
    return func



def fit_func(param, x, y, w):
    A,B=param
    residual=(y-func(x,A,B))/w

    return residual
          

def leastsq(x0, y0, w0):

    x=numpy.array(x0, dtype=numpy.float)
    y=numpy.array(y0, dtype=numpy.float)
    w=numpy.array(w0, dtype=numpy.float)

    param0=numpy.array([3.0, 0.0])
    result=scipy.optimize.leastsq(fit_func, param0, args=(x,y,w), full_output=True)

    print result
    print ""
    print result[0]
    print ""
    print result[1]
    print ""
    

    A,B=result[0]
    A_std=numpy.sqrt(result[1][0][0])
    B_std=numpy.sqrt(result[1][1][1])

    print "A =",A,", A_std =",A_std,", B =",B,", B_std =",B_std

    return A, B, A_std, B_std



if __name__ == "__main__":

    start_time = time.time()

    X = [1.6, 2.9, 4.1, 6.7, 8.5, 13.9]

    Data=[226.0, 201.0, 211.0, 222.0, 218.0, 236.0]
    print len(Data)
    Data_std=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    


    #--- leastsq 1 ---#

    A, B, A_std, B_std = leastsq(X,Data,Data_std)

    X_sq=numpy.arange(0.0, 20.0, 0.01)
    Y_sq=func(X_sq,A,B)

    
    
    #----- plot start --------------------------------------
    fig = plt.figure(figsize=(9,7))
    fig.add_subplot(1, 1, 1)

    #plt.rc('text', usetex=True)
    #plt.rc('font', family='serif')
    
    plt.scatter(X, Data, c='blue', s=30, marker='o')
    
    plt.plot(X_sq, Y_sq, color="red", linewidth=1.5, linestyle="-")
    
    plt.xlim(0.0, 20.0)
    plt.ylim(0.0, 300.0)
    plt.xlabel("D [kpc]", fontsize=15, fontname='serif') # x軸のタイトル
    plt.ylabel(r"$v_{\phi}$ [km/s]", fontsize=18, fontname='serif') # y軸
    plt.title(r"Potential $ \frac{v_0^2}{2}log \{ R^2 + R_c^2 \} $", fontsize=25, fontname='serif') # タイトル
    plt.text(10.0,400.0,"$v_0$=%.3e, $R_c$=%.3e"%(numpy.sqrt(A),numpy.sqrt(B)),ha='left',va='center')
    #plt.text(10.0,370.0,"y2 = %.3e*x + %.3e"%(A2,B2),ha='left',va='center')
    

    plt.savefig("toukei_5.png", format="png", dpi=500)
    print "save figure"
    plt.show()













