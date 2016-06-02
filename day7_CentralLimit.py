#!/usr/bin/env python

import numpy
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
from moviepy.editor import *

def update_hist(i, data1, data2, data3, data4, num):
        pyplot.clf()
        bins=20
        pyplot.subplot(221)
        pyplot.hist(data1[i], bins=bins, normed=True)
        pyplot.ylabel("Fraction")
        pyplot.title("Normal")
        pyplot.subplot(222)
        pyplot.hist(data2[i], bins=bins, normed=True)
        pyplot.ylabel("Fraction")
        pyplot.title("Gamma")
        pyplot.subplot(223)
        pyplot.hist(data3[i], bins=bins, normed=True)
        pyplot.xlabel("x")
        pyplot.ylabel("Fraction")
        pyplot.title("Uniform")
        pyplot.subplot(224)
        pyplot.hist(data4[i], bins=bins, normed=True)
        pyplot.xlabel("x")
        pyplot.ylabel("Fraction")
        pyplot.title("Beta")
        pyplot.suptitle("The number of data: %d, Sample Size: %d"%(num,i+1))

num=100000
n=100

x1=numpy.zeros(num)
x2=numpy.zeros(num)
x3=numpy.zeros(num)
x4=numpy.zeros(num)
vstack_tmp1=[]
vstack_tmp2=[]
vstack_tmp3=[]
vstack_tmp4=[]
for i in xrange(1,n+1):
        x1+=numpy.random.randn(num)
        x2+=numpy.random.gamma(1,1,num)
        x3+=numpy.random.uniform(0,1,num)
        x4+=numpy.random.beta(0.5,0.5,num)
        vstack_tmp1.append(x1/i)
        vstack_tmp2.append(x2/i)
        vstack_tmp3.append(x3/i)
        vstack_tmp4.append(x4/i)

data1=numpy.vstack(vstack_tmp1)
data2=numpy.vstack(vstack_tmp2)
data3=numpy.vstack(vstack_tmp3)
data4=numpy.vstack(vstack_tmp4)

fig = pyplot.figure(figsize=(9,8))

animation = animation.FuncAnimation(fig, update_hist, fargs=(data1, data2, data3, data4, num), frames=100, interval=100)
animation.save('day7_CentralLimit.mp4', fps=3)

clip = VideoFileClip("day7_CentralLimit.mp4")
clip.write_gif("day7_CentralLimit.gif")
#pyplot.show()
