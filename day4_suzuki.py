# coding: utf-8
import sys
sys.path.append("/Users/masa/Ureka/variants/common/lib/python2.7/site-packages")
sys.path.append("/Users/masa/Ureka/python/lib/python2.7/site-packages")
#print sys.path
import numpy 
import matplotlib.pyplot as plt
import seaborn 
#from mpl_toolkits.mplot3d.axes3d import Axes3D
import scipy.interpolate 
import scipy.optimize
import csv
import time


def func(x, A, B):
    return A*x+B



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

    A,B=result[0]
    A_std=numpy.sqrt(result[1][0])
    B_std=numpy.sqrt(result[1][1])

    print "A =",A,", A_std =",A_std,", B =",B,", B_std =",B_std

    return A, B, A_std, B_std



if __name__ == "__main__":

    start_time = time.time()

    V = [35.0, 40.0, 45.1, 50.2, 55.3, 60.3]

    Data_0 = [16.03652*1.0e+3, 3.15928*1.0e+3, 12.50246*1.0e+3, 8.52321*1.0e+3, 1.35439*1.0e+3, 13.07839*1.0e+3, 2.38898*1.0e+3, 8.99005*1.0e+3, 775.5923, 2.808247*1.0e+3]
    Data_1 = [363.5246*1.0e+3, 572.4682*1.0e+3, 538.0784*1.0e+3, 1.247478*1.0e+6, 567.8405*1.0e+3, 1.63307*1.0e+6, 1.285684*1.0e+6, 0.850019*1.0e+6, 1.057948*1.0e+6, 0.705367*1.0e+6, 0.518471*1.0e+6, 0.607884*1.0e+6]
    Data_2 = [4.326006*1.0e+6, 4.326006*1.0e+6, 4.738820*1.0e+6, 3.321677*1.0e+6, 2.014175*1.0e+6, 4.075296*1.0e+6, 5.116415*1.0e+6, 1.779342*1.0e+6, 3.319255*1.0e+6, 2.288642*1.0e+6, 2.981782*1.0e+6]
    Data_3 = [6.091210*1.0e+6, 3.068490*1.0e+6, 6.938694*1.0e+6, 7.064614*1.0e+6, 7.263056*1.0e+6, 5.757792*1.0e+6, 7.198832*1.0e+6, 6.027072*1.0e+6, 3.433851*1.0e+6, 6.090596*1.0e+6, 6.851236*1.0e+6]
    Data_4 = [7.065627*1.0e+6, 7.114796*1.0e+6, 7.113154*1.0e+6, 7.074449*1.0e+6, 7.074180*1.0e+6, 7.095503*1.0e+6, 7.113240*1.0e+6, 7.091928*1.0e+6, 7.104446*1.0e+6, 7.120877*1.0e+6]
    Data_5 = [7.088113*1.0e+6, 7.087233*1.0e+6, 7.089680*1.0e+6, 7.089785*1.0e+6, 7.094208*1.0e+6]

    Data=[Data_0, Data_1, Data_2, Data_3, Data_4, Data_5]
    print len(Data)

    Data_mean=[]
    Data_std=[]
    for i in range(0, len(Data), 1):
        mean = numpy.mean(Data[i])
        Data_mean.append(mean)
        std=numpy.std(Data[i])
        Data_std.append(std)


    #--- leastsq 1 ---#

    A, B, A_std, B_std = leastsq(V,Data_mean,Data_std)

    X_sq=numpy.arange(35.0, 60.3, 0.01)
    Y_sq=A*X_sq + B

    #--- leastsq 2 ---#
    V2=[]
    Data_mean2=[]
    Data_std2=[]
    for i in range(1, 4):
        V2.append(V[i])
        Data_mean2.append(Data_mean[i])
        Data_std2.append(Data_std[i])

    A2, B2, A_std2, B_std2 = leastsq(V2,Data_mean2,Data_std2)

    Y_sq2=A2*X_sq + B2

    #--- spline ---#
    
    V_o = V
    V = numpy.array(V)
    xn = numpy.arange(35.0, 60.3, 0.01)

    rp = scipy.interpolate.splrep(V, Data_mean, s=0)
    yn = scipy.interpolate.splev(xn, rp, der=0)
    
    #----- plot start --------------------------------------
    fig = plt.figure(figsize=(9,7))
    fig.add_subplot(1, 1, 1)
    
    #plt.plot(xn, yn, color="green", linewidth=0.5, linestyle="-")

    (_, caps, _) = plt.errorbar(V_o, Data_mean, yerr=Data_std, fmt='o', markersize=4, capsize=10)
    for cap in caps:
        cap.set_markeredgewidth(1)
    #plt.scatter(V_o, Data_mean, c='blue', s=30, marker='o')
    plt.plot(X_sq, Y_sq, color="red", linewidth=1.5, linestyle="-")
    plt.plot(X_sq, Y_sq2, color="green", linewidth=1.5, linestyle="-")
    
    plt.xlim(35.0, 60.3)
    plt.ylim(-1.0e+5, 8.0e+6)
    plt.xlabel("V [V]", fontsize=12, fontname='serif') # x軸のタイトル
    plt.ylabel("Hz [Hz]", fontsize=12, fontname='serif') # y軸
    plt.title("The number of photon", fontsize=25, fontname='serif') # タイトル
    plt.text(35.5,7.0e+6,"y1 = %.3e*x + %.3e"%(A,B),ha='left',va='center')
    plt.text(35.5,6.7e+6,"y2 = %.3e*x + %.3e"%(A2,B2),ha='left',va='center')
    

    plt.savefig("toukei_4_photon.png", format="png", dpi=500)
    print "save figure"
    plt.show()













