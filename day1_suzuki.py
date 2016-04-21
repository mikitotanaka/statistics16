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
    
    def __init__(self, B_V, mv, log_D):

        self.B_V = B_V
        self.Mv = mv - 5.0*(log_D - 1.0)
        


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

            log_D = numpy.log10(1000.0 / Plx)

            dw_w = e_Plx / Plx
            
        except (TypeError, ValueError, ZeroDivisionError):
            count_error+=1
            #print "Error ", count_error
            
        else:
            if (dw_w < 0.2 and e_B_V < 0.1):
                count_ok+=1
                Star.append(star(B_V, mv, log_D))

    print "the number of error data is ", count_error
    print "the number of data I can use is ", count_ok           
        
    f.close()

    print "reading file is done."
    print "length of data is ", len(Star)

    fig = matplotlib.pyplot.figure(figsize=(7,9))
    seaborn.set_style("ticks") #darkgrid, whitegrid, dark, white, ticks, sns.despine()
    ax = fig.add_subplot(111)
    ax.patch.set_facecolor("black")
    ax.patch.set_alpha(1.0)
    #ax.set_yscale("log")
    ax.set_xlim(-0.5, 2.2)
    ax.invert_yaxis()

    for i in range(0, len(Star), 1):
        ax.scatter(Star[i].B_V, Star[i].Mv, s=3.0, marker='o', alpha=0.3, color=matplotlib.cm.hot((3.0 - Star[i].B_V - 0.5)/3.0))
    
    #aspect = 1.1*(ax.get_xlim()[1] - ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
    #ax.set_aspect(aspect)
    ax.set_title('Spectral Class', size=30)
    ax.set_xlabel('Colour (B-V)', size=12)
    ax.set_ylabel('Luminosity (Sun=1)', size=12)
    
    #ax.grid(True)

    end_time = time.time()
    dif=end_time-start_time
    hour = int((dif)/3600.0)
    minute=int((dif-3600.0*hour)/60.0)
    second=dif-3600.0*hour-60.0*minute
    print "time =", (end_time - start_time), '[sec]'
    print "time =", str(hour)+':'+str(minute)+':'+str(second)
    
    matplotlib.pyplot.savefig("plot_Mv_middle.png", format="png", dpi=500)
    print "save figure"
    matplotlib.pyplot.show()





















