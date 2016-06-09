# coding: utf-8
import sys
sys.path.append("/Users/masa/Ureka/variants/common/lib/python2.7/site-packages")
sys.path.append("/Users/masa/Ureka/python/lib/python2.7/site-packages")
#print sys.path
import numpy # numpy.random
import matplotlib.pyplot as plt
import seaborn as sns
#from mpl_toolkits.mplot3d.axes3d import Axes3D
import csv
import time
import matplotlib.patches as mpatches

num_max=500
p0=0.4
name="fast"

class State_c:

    def __init__(self, time, num_c):
        #float time
        #int num

        self.time=time
        self.num=num_c
        


if __name__=="__main__":

    start_time = time.time()

    Time=[0.1+numpy.random.rand()*1.9 for i in range(0,num_max+10)]
    #Time=numpy.random.uniform(0.0,30.0,num_max+10)
    #int count_customer=0,i_time=0,i_customer=1
    count_c=0
    i_time=0
    i_c=0

    #0 or 1 leave_bool=0
    leave_bool=0

    wait_time=Time[i_time]
    
    leave_time=[Time[i_time] + float(numpy.random.binomial(n=200, p=p0))/100.0]

    #float day_time time of the day from initial point [min]
    day_time=0.0

    Customer=[]

    ##----------- loop ----------------##

    while(1):

        if (i_time==num_max):
            break

        if (day_time >= wait_time):

            #print wait_time

            count_c+=1
            i_time+=1

            wait_time+=Time[i_time]

            #leave_time.append(leave_time[i_time-1] + 5.0 + float(numpy.random.binomial(n=200, p=0.5))/10.0)
            #leave_time.append(leave_time[i_time-1] + 5.0 + float(numpy.random.binomial(n=200, p=0.5))/10.0)
            #leave_time.append(leave_time[i_time-1] + 5.0 + float(numpy.random.binomial(n=400, p=0.495))/10.0)
            leave_bool=1

        if (leave_bool==1):

            if (day_time>=leave_time[i_c]):

                count_c-=1
                i_c+=1
                leave_time.append(day_time + float(numpy.random.binomial(n=200, p=p0))/100.0)

                if(count_c==0):
                    leave_bool=0
                    
                    

        
        Customer.append(State_c(day_time,count_c))

        day_time+=0.1


    ##------- end loop -----------#

    X=[]
    Y=[]
    for i in range(0,len(Customer),1):

        X.append(Customer[i].time)
        Y.append(Customer[i].num)
        

    fig = plt.figure(figsize=(13,9))
    ax = fig.add_subplot(111)

    ax.plot(X,Y,color="red",linewidth=1.5,linestyle="-")

    plt.xlabel("count", fontsize=16, fontname='serif')
    plt.ylabel("the number of customer", fontsize=16, fontname='serif')
    plt.title("plot binomial: %s"%(name), fontsize=25, fontname='serif')

    end_time = time.time()
    dif=end_time-start_time
    hour = int((dif)/3600.0)
    minute=int((dif-3600.0*hour)/60.0)
    second=dif-3600.0*hour-60.0*minute
    print "time =", (end_time - start_time), '[sec]'
    print "time =", str(hour)+':'+str(minute)+':'+str(second)
    
    plt.savefig("toukei_7_bi_%s.png"%(name), format="png", dpi=500)
    print "save figure"
    plt.show()

    

    X=[i for i in range(0,201)]
    Y=[0 for i in range(0,201)]
    B=numpy.random.binomial(200,0.5,int(1.0e+5))

    for i in range(0,len(B)):

        Y[B[i]]+=1.0/len(B)

    X1=[i for i in range(0,201)]
    Y1=[0 for i in range(0,201)]
    B1=numpy.random.binomial(200,0.4,int(1.0e+5))

    for i in range(0,len(B1)):

        Y1[B1[i]]+=1.0/len(B1)

        

    fig = plt.figure(figsize=(13,9))
    ax = fig.add_subplot(111)
    
    ax.plot(X1,Y1,color="blue",linewidth=1.5,linestyle="-",label="p=0.4")
    
    ax.plot(X,Y,color="red",linewidth=1.5,linestyle="-",label="p=0.5")

    ax.text(10,0.057,'mean(p=0.5):%.2f'%(numpy.mean(B)),ha='left',va='center')
    ax.text(10,0.055,'mean(p=0.4):%.2f'%(numpy.mean(B1)),ha='left',va='center')
    ax.legend(bbox_to_anchor=(1.0, 1), loc=2, borderaxespad=0.)
    plt.savefig("toukei_7_bi_dis.png", format="png", dpi=500)
    print "save figure"
    plt.show()
    
     


        


























        

        
