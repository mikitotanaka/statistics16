# coding: utf-8
import sys
sys.path.append("/Users/masa/Ureka/variants/common/lib/python2.7/site-packages")
sys.path.append("/Users/masa/Ureka/python/lib/python2.7/site-packages")
import numpy as np
import scipy,math
import matplotlib.pyplot as plt
import seaborn as sns
import time

def poisson(k,x):

    p = pow(x,k)*np.exp(-x)/float(math.factorial(k))

    return p

if __name__=="__main__":

    N=10

    data=[2,1,4,0,1,1,3,3,3,0]

    O_k=[0.0 for i in range(0,5,1)]

    for i in range(0,len(data),1):

        if (int(data[i])<=3.0):
            
            O_k[int(data[i])]+=1.0
            
        else:

            O_k[4]+=1.0
            
    X=np.arange(0.01,3.0,0.01)
    P=[]
    for x in X:


        E_k=[]
        for k in range(0,4,1):

            E_k.append(N*poisson(k,x))

        E_k.append(N - (E_k[0]+E_k[1]+E_k[2]+E_k[3]))

        P.append( scipy.stats.chisquare(O_k,f_exp=E_k,ddof=1)[1] )

    P_max=P[0]
    X_max=0
    for i in range(1,len(P),1):

        if ( P[i]>=P_max ):

            P_max=P[i]
            X_max=X[i]


    print "P =",P_max,", X =",X_max,max(P)


    x=[i for i in range(0,10)]
    y=[poisson(i,X_max) for i in range(0,10)]
    plt.plot(x,y,color="red",linewidth=1.5,linestyle="-")
    plt.title(" poisson $\lambda=%.3f$"%(X_max), fontsize=25, fontname='serif')
    plt.show()

    plt.plot(X,P,color="red",linewidth=1.5,linestyle="-")
    plt.xlabel("$\lambda$ ", fontsize=12, fontname='serif') # x軸のタイトル
    plt.ylabel("probability", fontsize=12, fontname='serif') 
    plt.title("Relation betweeen P and $\lambda$", fontsize=25, fontname='serif')
    plt.show()
        

        

    































    

    
