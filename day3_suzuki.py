# coding: utf-8
import sys
sys.path.append("/Users/masa/Ureka/variants/common/lib/python2.7/site-packages")
sys.path.append("/Users/masa/Ureka/python/lib/python2.7/site-packages")
#print sys.path
import math
import numpy #as np
#import matplotlib.mlab as mlab
import matplotlib.cm #as cm
import matplotlib.pyplot #as plt
import seaborn
import time

#----- class star -------------------------------------------------#
class star:
    
    def __init__(self, mv, log_D, D):

        self.Mv = mv - 5.0*(log_D - 1.0)
        self.D = D
        


#----- main -------------------------------------------------------#
if __name__=="__main__":

    start_time = time.time()
    
    f = open("hip_main.dat", 'r')
    count_ok=0
    count_error=0
    
    Star=[]

    print "start reading file"
    
    for line in f:

        data=line.split('|')

        try:
            mv = float(data[5])
            Plx = float(data[11])
            e_Plx = float(data[16])
            B_V = float(data[37])
            e_B_V = float(data[38])

            D = float(1000.0 / Plx)
            log_D = numpy.log10(1000.0 / Plx)

            dw_w = e_Plx / Plx
            
            
        except (ValueError, ZeroDivisionError, TypeError, IOError):
            count_error+=1
            #print "Error ", count_error
            
        else:
            if math.isnan(log_D)==False:
                if (dw_w < 0.2 and e_B_V < 0.1):
                    count_ok+=1
                    Star.append(star(mv, log_D, D))

    print "the number of error data is ", count_error
    print ""
        
    f.close()

    print "reading file is done."
    print "length of data is ", len(Star)

    D=[]
    Mv=[]
    for i in range(0, len(Star), 1):
        D.append(float(Star[i].D))
        Mv.append(float(Star[i].Mv))

    corr = numpy.corrcoef(D, Mv)

    #print D
    #print Mv
    print corr[0][1]

    #---------------------- plot --------------------------#

    fig = matplotlib.pyplot.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    for i in range(0, len(Star), 1):
        ax.scatter(Star[i].D, Star[i].Mv, s=3.0, marker='o', alpha=0.3, color="red")
    
    #aspect = 1.1*(ax.get_xlim()[1] - ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
    #ax.set_aspect(aspect)
    ax.set_xlim(0.0, 550.0)
    ax.set_title('Relation', size=30)
    ax.set_xlabel('Distance [pc]', size=12)
    ax.set_ylabel('Absolute magnitude', size=12)
    ax.text(300.0,15.0,'correlation coefficient = %.5f'%(corr[0][1]),ha='left',va='center')
    
    #ax.grid(True)

    end_time = time.time()
    dif=end_time-start_time
    hour = int((dif)/3600.0)
    minute=int((dif-3600.0*hour)/60.0)
    second=dif-3600.0*hour-60.0*minute
    print "time =", (end_time - start_time), '[sec]'
    print "time =", str(hour)+':'+str(minute)+':'+str(second)
    
    matplotlib.pyplot.savefig("plot_Mv_D_relation.png", format="png", dpi=500)
    print "save figure"
    matplotlib.pyplot.show()





















