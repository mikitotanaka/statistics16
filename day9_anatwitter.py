#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys,math
import numpy
import scipy.stats as stats
import scipy.integrate as integrate
import matplotlib.pyplot as pyplot
import pandas
from collections import Counter
import codecs
import MeCab
import re
import csv

def beta(theta, a, b):
    B = math.gamma(a) * math.gamma(b) / math.gamma(a + b)
    return (theta ** (a - 1)) * ((1 - theta) ** (b - 1)) / B


def is_ascii(string):
    """return true if non ascii characters are detected in the given string
    """
    if string:
        return max([ord(char) for char in string]) < 128
    return True

def countsukikawaii(data,file):

    n=int(len(data))
    i=0;i1=0;i2=0
    j=0;j1=0;j2=0
    k=0;k1=0;k2=0
    for s in data['text']:
        if '好き' in s or 'すき' in s or 'スキ' in s:
            i+=1
            if 'かわいい' in s or '可愛' in s or 'カワイイ' in s:
                i1+=1
            else:
                i2+=1
        if 'かわいい' in s or '可愛' in s or 'カワイイ' in s:
            j+=1
            if '好き' in s or 'すき' in s or 'スキ' in s:
                j1+=1
            else:
                j2+=1

    print i,i1,i2,j,j1,j2,n,file

def countword(data):

    texts=(tw for tw in data['text'])
    tagger = MeCab.Tagger('-Ochasen')
    counter = Counter()
    for text in texts:
        nodes = tagger.parseToNode(text)
        while nodes:
            if nodes.feature.split(',')[0] == '名詞' or nodes.feature.split(',')[0] == '形容詞' or nodes.feature.split(',')[0] == '動詞':
                word = nodes.surface.decode('utf-8')
                if int(len(word))<1:
                    nodes = nodes.next
                    continue
                else:
                    if is_ascii(word):
                        nodes = nodes.next
                        continue
                    else:
                        counter[word] += 1

            nodes = nodes.next

    #for word,cnt in counter.most_common():
    #    print word,cnt
    #exit()

    wordlist=numpy.vstack([list(i) for i in counter.most_common()])
    sum=0
    for i in xrange(len(wordlist)):
        sum+=int(wordlist[i,1])+1.
    for i in xrange(len(wordlist)):
        wordlist[i,1]=1.*(int(wordlist[i,1])+1.)/sum

    return wordlist,sum

def Bernoulli(data):

    def makegraph(file,i):
        pyplot.xlabel("probability", fontsize=20, fontname='serif')
        pyplot.xticks(fontsize=20, fontname='serif')
        pyplot.ylim(0,1.05)
        pyplot.tick_params(labelleft='off')
        pyplot.title('i = %s'%(i), fontsize=20, fontname='serif')
        pyplot.grid()
        pyplot.savefig(file)

    ntot=int(len(data['text']))
    i=0;j=0

    p=numpy.linspace(0,1,10000)
    alpha=2.0;beta=2.0
    f=stats.beta.pdf(p,alpha,beta)
    f0=integrate.simps(f,p)
    f=f/f0
    g=stats.beta.pdf(p,alpha,beta)
    g0=integrate.simps(g,p)
    g=g/g0

    fig = pyplot.figure(figsize=(7,7))
    pyplot.plot(p,g/max(g),'--',lw=3)
    makegraph('day9_Bernoulli_%s.png'%(i),i)
    for s in data['text']:
        i+=1
        if '彩音' in s or 'ピンキー' in s or 'ぴんきー' in s or 'ピンちゃん' in s or 'ぴんちゃん' in s:
            f=f*p
            f0=integrate.simps(f,p)
            f=f/f0
            j+=1
        else:
            f=f*(1-p)
            f0=integrate.simps(f,p)
            f=f/f0
        if i<11:
            print s
            fig = pyplot.figure(figsize=(7,7))
            pyplot.plot(p,g/max(g),'--',lw=3)
            pyplot.plot(p,f/max(f),'r',lw=3)
            makegraph('day9_Bernoulli_%s.png'%(i),i)

    f0=integrate.simps(f,p)
    f=f/f0
    print p[numpy.where(f==(max(f)))]
    print j,1.*j/ntot

    fig = pyplot.figure(figsize=(10,7))
    pyplot.plot(p,g/max(g),'--')
    pyplot.plot(p,f/max(f),'r',lw=3)
    makegraph('day9_Bernoulli_%s.png'%(i),i)

def NaiveBayes():

    data_all=pandas.read_csv('./tweet_all.csv')
    data_mirin=pandas.read_csv('./tweet_FurukawaMirin.csv')
    data_pinky=pandas.read_csv('./tweet_PINKY_neko.csv')
    data_risa=pandas.read_csv('./tweet_RISA_memesama.csv')
    data_eitaso=pandas.read_csv('./tweet_eitaso.csv')
    data_moga=pandas.read_csv('./tweet_mogatanpe.csv')
    data_nemu=pandas.read_csv('./tweet_yumeminemu.csv')

    ntot=int(len(data_all))
    n_mirin=int(len(data_mirin))
    n_pinky=int(len(data_pinky))
    n_risa=int(len(data_risa))
    n_eitaso=int(len(data_eitaso))
    n_moga=int(len(data_moga))
    n_nemu=int(len(data_nemu))

    m_mirin=0
    m_pinky=0
    m_risa=0
    m_eitaso=0
    m_moga=0
    m_nemu=0

    p_mirin=1.*n_mirin/ntot
    p_pinky=1.*n_pinky/ntot
    p_risa=1.*n_risa/ntot
    p_eitaso=1.*n_eitaso/ntot
    p_moga=1.*n_moga/ntot
    p_nemu=1.*n_nemu/ntot

    print 'P(みりん) =',p_mirin
    print 'P(ピンキー) =',p_pinky
    print 'P(りさちー) =',p_risa
    print 'P(えいたそ) =',p_eitaso
    print 'P(もが) =',p_moga
    print 'P(ねむきゅん) =',p_nemu

    wordlist_mirin,sum_mirin=countword(data_mirin)
    wordlist_pinky,sum_pinky=countword(data_pinky)
    wordlist_risa,sum_risa=countword(data_risa)
    wordlist_eitaso,sum_eitaso=countword(data_eitaso)
    wordlist_moga,sum_moga=countword(data_moga)
    wordlist_nemu,sum_nemu=countword(data_nemu)

    csv_out=open('NaiveBayesResult.csv', mode='w')
    writer=csv.writer(csv_out)
    fields=['expected_name', 'log_P(cat|doc)', 'full_text']
    writer.writerow(fields)

    tagger = MeCab.Tagger('-Ochasen')
    num=range(int(len(data_all['text'])))
    n_ini=int(len(data_all['text']))
    while True:
        n=int(len(num))
        if n==0: break
        if n%100==0:
            print n
            break

        frac_mirin=numpy.log(p_mirin)
        frac_pinky=numpy.log(p_pinky)
        frac_risa=numpy.log(p_risa)
        frac_eitaso=numpy.log(p_eitaso)
        frac_moga=numpy.log(p_moga)
        frac_nemu=numpy.log(p_nemu)

        i=numpy.random.choice(num)
        text=(data_all['text'][i])
        nodes = tagger.parseToNode(text)
        #print text
        while nodes:
            #print nodes.feature.decode('utf-8')
            if nodes.feature.split(',')[0] == '名詞' or nodes.feature.split(',')[0] == '形容詞' or nodes.feature.split(',')[0] == '動詞':
                word = nodes.surface.decode('utf-8')
                if int(len(word))<1:
                    nodes = nodes.next
                    continue
                else:
                    if is_ascii(word):
                        nodes = nodes.next
                        continue
                    else:

                        k=0
                        for j in xrange(len(wordlist_mirin)):
                            if word == wordlist_mirin[j,0]:
                                k+=1
                                frac_mirin=frac_mirin+numpy.log(float(wordlist_mirin[j,1]))
                        if k==0:frac_mirin=frac_mirin+numpy.log(float(1./sum_mirin))

                        k=0
                        for j in xrange(len(wordlist_pinky)):
                            if word == wordlist_pinky[j,0]:
                                k+=1
                                frac_pinky=frac_pinky+numpy.log(float(wordlist_pinky[j,1]))
                        if k==0:frac_pinky=frac_pinky+numpy.log(float(1./sum_pinky))

                        k=0
                        for j in xrange(len(wordlist_risa)):
                            if word == wordlist_risa[j,0]:
                                k+=1
                                frac_risa=frac_risa+numpy.log(float(wordlist_risa[j,1]))
                        if k==0:frac_risa=frac_risa+numpy.log(float(1./sum_risa))

                        k=0
                        for j in xrange(len(wordlist_eitaso)):
                            if word == wordlist_eitaso[j,0]:
                                k+=1
                                frac_eitaso=frac_eitaso+numpy.log(float(wordlist_eitaso[j,1]))
                        if k==0:frac_eitaso=frac_eitaso+numpy.log(float(1./sum_eitaso))

                        k=0
                        for j in xrange(len(wordlist_moga)):
                            if word == wordlist_moga[j,0]:
                                k+=1
                                frac_moga=frac_moga+numpy.log(float(wordlist_moga[j,1]))
                        if k==0:frac_moga=frac_moga+numpy.log(float(1./sum_moga))

                        k=0
                        for j in xrange(len(wordlist_nemu)):
                            if word == wordlist_nemu[j,0]:
                                k+=1
                                frac_nemu=frac_nemu+numpy.log(float(wordlist_nemu[j,1]))
                        if k==0:frac_nemu=frac_nemu+numpy.log(float(1./sum_nemu))

            nodes = nodes.next

        frac=[frac_mirin,frac_pinky,frac_risa,frac_eitaso,frac_moga,frac_nemu]
        frac_max=max(frac)
        n_max=frac.index(frac_max)

        if n_max==0: 
            writer.writerow(["みりん",frac_mirin,text])
            print "みりん",frac_mirin,text
            if '@FurukawaMirin' in text: m_mirin+=1
        if n_max==1:
            writer.writerow(["ピンキー",frac_pinky,text])
            print "ピンキー",frac_pinky,text
            if '@PINKY_neko' in text: m_pinky+=1
        if n_max==2:
            writer.writerow(["りさちー",frac_risa,text])
            print "りさちー",frac_risa,text
            if '@RISA_memesama' in text: m_risa+=1
        if n_max==3:
            writer.writerow(["えいたそ",frac_eitaso,text])
            print "えいたそ",frac_eitaso,text
            if '@eitaso' in text: m_eitaso+=1
        if n_max==4:
            writer.writerow(["もが",frac_moga,text])
            print "もが",frac_moga,text
            if '@mogatanpe' in text: m_moga+=1
        if n_max==5:
            writer.writerow(["ねむきゅん",frac_nemu,text])
            print "ねむきゅん",frac_nemu,text
            if '@yumeminemu' in text: m_nemu+=1

        num.remove(i)

    print "みりん:",1.*m_mirin/n_mirin
    print "ピンキー:",1.*m_pinky/n_pinky
    print "りさちー:",1.*m_risa/n_risa
    print "えいたそ:",1.*m_eitaso/n_eitaso
    print "もが:",1.*m_moga/n_moga
    print "ねむきゅん:",1.*m_nemu/n_nemu

    csv_out.close()

if __name__== "__main__":

    #file=sys.argv[1]
    #data=pandas.read_csv(file)
    #countsukikawaii(data,file)
    #Bernoulli(data)

    NaiveBayes()
