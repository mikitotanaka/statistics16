# coding: utf-8
import sys
sys.path.append("/Users/masa/Ureka/variants/common/lib/python2.7/site-packages")
sys.path.append("/Users/masa/Ureka/python/lib/python2.7/site-packages")
#print sys.path
import math,decimal
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing as mp
import time

proc=4

def factorial(n):
    func=decimal.Decimal(1.0)
    for i in range(2,n+1):
        func*=decimal.Decimal(i)

    return func





def func(x, n):
    decimal.getcontext().prec = 28

    if (x==0):
        func=decimal.Decimal(float(n))/decimal.Decimal(math.pi)
    else:
        func=decimal.Decimal(np.sin(float(n)*x))/decimal.Decimal(math.pi*x)

    return float(func)

    #
    '''
    func=decimal.Decimal(float(n))
    count=0
    for i in range(1,k+1,1):
        if(count==0):
            nx=decimal.Decimal(float(n))
            for j in range(0,i):
                nx*=decimal.Decimal(float(n)*x)*decimal.Decimal(float(n)*x)
            func -= nx/decimal.Decimal(factorial(int(2*i+1)))
            count=1
        else:
            nx=decimal.Decimal(float(n))
            for j in range(0,i):
                nx*=decimal.Decimal(n*x)*decimal.Decimal(n*x)
            func += nx/decimal.Decimal(factorial(int(2*i+1)))
            count=0
            
    func /= decimal.Decimal(math.pi)
    '''
    return float(func)




def subcalc(queue, p, j):
    
    ini = decimal.Decimal(len(X) * float(p) / float(proc))
    fin = decimal.Decimal(len(X) * float(p+1) / float(proc))

    count=0    
    for i in range(ini, fin, 1):
        if (Y[i]<=func(X[i],num[j])):
            count+=1
    
    queue.put(count)





if __name__ == "__main__":

    num=[20,int(1.0e+2),int(1.0e+3),int(1.0e+4),int(1.0e+6)]
    N=[int(1.0e+3*i) for i in range(1,int(1.0e+3))]
    X=[-1.0 + 1.0e-3*float(i) for i in range(0,2000,1) ]

    #
    '''
    for i in range(0,len(num),1):

        start_time = time.time()

        Y=[func(X[j],num[i]) for j in range(0,len(X),1) ]

        print "N=%d, max=%.3f"%(num[i],max(Y))
    
        fig = plt.figure(figsize=(13,8))
        fig.add_subplot(1, 1, 1)

        plt.plot(X,Y,color="red",linewidth=1.5,linestyle="-")
        

        plt.xlabel("$x$ ", fontsize=12, fontname='serif') # x軸のタイトル
        plt.ylabel("$y$", fontsize=12, fontname='serif') # y軸
        plt.title("plot delta n=%d"%(num[i]), fontsize=25, fontname='serif') # タイトル
        plt.savefig("toukei_6_%d.png"%(num[i]), format="png", dpi=500)
        plt.show()
        
        end_time = time.time()
        dif=end_time-start_time
        hour = int((dif)/3600.0)
        minute=int((dif-3600.0*hour)/60.0)
        second=dif-3600.0*hour-60.0*minute
        print "time =", (end_time - start_time), "[sec]"
        print "time =", str(hour)+":"+str(minute)+":"+str(second)
    '''
    
    
    for i in range(0,len(num),1):
        S_num=[]
        fig = plt.figure(figsize=(13,8))
        fig.add_subplot(1, 1, 1)
        for j in range(0,len(N),1):
            func_max=func(0.0,num[i])
            np.random.seed()
            X = np.random.uniform(-1.0, 1.0, N[j])
            Y = np.random.uniform(0.0, func_max, N[j])

            queue = mp.Queue()

            ps=[]
            for k in range(0, proc, 1):
                ps.append(mp.Process(target=subcalc, args=(queue, k,i)))
                  
            for p in ps:
                p.start()

            
            count=0
            for k in range(proc):
                T=queue.get()
                count+=T
            S=2.0*func_max*float(count)/float(N[j])
            #print "S=%e (N=%e, num=%e)"%(S,N[j],num[i])
            if (N[j]>=1.0e+5):
                S_num.append(S)

            plt.scatter(N[j], S, c='blue', s=30, marker='o')               

        print "S=%e (num=%e)"%(np.mean(S_num),num[i])
        plt.plot([0.0,N[len(N)-1]],[np.mean(S_num),np.mean(S_num)],color="red",linewidth=1.5,linestyle="-")
        plt.xlabel("$N$ ", fontsize=12, fontname='serif') # x軸のタイトル
        plt.ylabel("$S$", fontsize=12, fontname='serif') # y軸
        plt.title("plot delta n=%d"%(num[i]), fontsize=25, fontname='serif') # タイトル
        plt.savefig("toukei_6_S_%d.png"%(num[i]), format="png", dpi=500)
        print "plot"
        #plt.show()



















