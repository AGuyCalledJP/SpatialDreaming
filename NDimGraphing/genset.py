import threading 
import multiprocessing as m
from itertools import combinations_with_replacement as comb
from itertools import permutations as perm
from sympy.utilities.iterables import multiset_permutations as mp
import numpy as np
import queue
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys

getBund = threading.Semaphore(1)
placeRes = threading.Semaphore(1)
dim = 5
depth = 41
rd = 2
line = np.linspace(-1,1,depth)
inds = []
bundles = queue.Queue()
total = 0
res = []
split = 8
ax2 = None
fig2 = None
f = None

def onclick(event):
    global rd
    global res
    global fig2
    if fig2 is not None:
        plt.close(fig2)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')
    x = round(event.xdata,rd)
    y = round(event.ydata,rd)
    for i in res: 
        if round(i[3],rd) == x and round(i[4],rd) == y:
            ax2.scatter(i[0], i[1], i[2], c='b')
    ax2.set_xlim([-1,1])
    ax2.set_ylim([-1,1])
    plt.show()

def plot():
    print("Generating Plot")
    global res
    global ax2

    if len(res[0]) == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d') 
        for i in res: 
            ax.scatter(i[0], i[1], i[2], c='b')
        plt.show()
    elif len(res[0]) == 4:
        pass
    elif len(res[0]) == 5:
        fig = plt.figure()
        ax = fig.add_subplot(111) 
        fig.canvas.mpl_connect('button_press_event', onclick)
        n = len(res)
        it = 0
        for i in res:
            print("iter " + str(it) + " of " + str(n))
            ax.scatter(i[3],i[4],c='b')
            it += 1
        plt.show()
    else:
        pass

def compute(l, who):
    global res
    global line
    global f
    n = dim
    finds = []
    if n is 2:
        one = inds[l[0]]
        two = inds[l[1]]
        for i in line[one[0]:one[1]]:
            i = round(i,rd)
            for j in line[two[0]:two[1]]:
                j = round(j,rd)
                if i**2 + j**2 == 1.0:
                    placeRes.acquire()
                    f.write(str([i,j]) + "\n")
                    placeRes.release()
    elif n is 3:
        one = inds[l[0]]
        two = inds[l[1]]
        three = inds[l[2]]
        for i in line[one[0]:one[1]]:
            i = round(i,rd)
            for j in line[two[0]:two[1]]:
                j = round(j,rd)
                for k in line[three[0]:three[1]]:
                    k = round(k,rd)
                    if i**2 + j**2 + k**2 == 1.0:
                        placeRes.acquire()
                        print("thread " + str(who) + " writing")
                        f.write(str([i,j,k]) + "\n")
                        placeRes.release()
    elif n is 4:
        one = inds[l[0]]
        two = inds[l[1]]
        three = inds[l[2]]
        four = inds[l[3]]
        for i in line[one[0]:one[1]]:
            i = round(i,rd)
            for j in line[two[0]:two[1]]:
                j = round(j,rd)
                for k in line[three[0]:three[1]]:
                    k = round(k,rd)
                    for a in line[four[0]:four[1]]:
                        a = round(a,rd)
                        if i**2 + j**2 + k**2 + a**2 == 1.0:
                            placeRes.acquire()
                            f.write(str([i,j,k,a]) + "\n")
                            placeRes.release()
    elif n is 5:
        one = inds[l[0]]
        two = inds[l[1]]
        three = inds[l[2]]
        four = inds[l[3]]
        five = inds[l[4]]
        for i in line[one[0]:one[1]]:
            i = round(i,rd)
            for j in line[two[0]:two[1]]:
                j = round(j,rd)
                for k in line[three[0]:three[1]]:
                    k = round(k,rd)
                    for a in line[four[0]:four[1]]:
                        a = round(a,rd)
                        for b in line[five[0]:five[1]]:
                            b = round(b,rd)
                            if i**2 + j**2 + k**2 + a**2 + b**2 == 1.0:
                                finds.append([i,j,k,a,b])

    elif n is 6:
        one = inds[l[0]]
        two = inds[l[1]]
        three = inds[l[2]]
        four = inds[l[3]]
        five = inds[l[4]]
        six = inds[l[5]]
        for i in line[one[0]:one[1]]:
            i = round(i,rd)
            for j in line[two[0]:two[1]]:
                j = round(j,rd)
                for k in line[three[0]:three[1]]:
                    k = round(k,rd)
                    for a in line[four[0]:four[1]]:
                        a = round(a,rd)
                        for b in line[five[0]:five[1]]:
                            b = round(b,rd)
                            for c in line[six[0]:six[1]]:
                                c = round(c,rd)
                                if i**2 + j**2 + k**2 + a**2 + b**2 + c**2 == 1.0:
                                    placeRes.acquire()
                                    f.write(str([i,j,k,a,b,c]) + "\n")
                                    placeRes.release()
    else:
        print("Feature in progress")

    placeRes.acquire()
    for i in finds:
        f.write(str(i) + "\n")
        #res.append(i)
    placeRes.release()
  
def calcChunk(inds):
    global getBund
    global bundles
    global total
    
    while not bundles.empty() and total is not 0:
        getBund.acquire()
        complete = bundles.get()
        total = total - 1
        getBund.release()
        compute(complete, inds)

def seriously():
    finds = []
    for i in line:
        i = round(i,rd)
        print(i)
        for j in line:
            j = round(j,rd)
            for k in line:
                k = round(k,rd)
                for a in line:
                    a = round(a,rd)
                    for b in line:
                        b = round(b,rd)
                        if i**2 + j**2 + k**2 + a**2 + b**2 == 1.0:
                            finds.append([i,j,k,a,b])
    return finds

def makeBundles():
    global dim
    global inds
    global split
    global total
    global bundles

    balance = int(depth / split)
    tracker = 0
    for i in range(0,split):
        hold = []
        hold.append(tracker)
        tracker += balance
        if i is split - 1:
            hold.append(depth)
        else:
            hold.append(tracker)
        inds.append(hold)
        #tracker += 1

    l = []
    for i in range(0,split):
        l.append(i)
    full = comb(l,dim)
    for i in list(full):
        p = mp(i)
        for j in list(p):
            bundles.put(j)
            total += 1

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def genset():
    global f
    global res
    makeBundles()
    print(line)
    print(inds)
    # creating threads
    start = time.time()
    numThreads = m.cpu_count()
    threads = []
    f = open("circle3.txt", "w+")
    for i in range(0,numThreads):
        threads.append(threading.Thread(target=calcChunk, args=(i,)))
  
    for i in range(0,numThreads):
        threads[i].start()

    for i in range(0,numThreads):
        threads[i].join()
    end = time.time()
    f.close()
    print("Time to calculate: " + str(end-start))
    useset()

#Method which takes in data from file and plots it
def useset():
    global res
    print("hello")
    f = open("circle3.txt", "r")
    for i in f:
        one = i.split(",")
        one[0] = one[0].split("[")[1]
        n = len(one) - 1
        one[n] = one[n].split("]")[0]
        respecc = []
        for j in one:
            respecc.append(float(j))
        res.append(respecc)
    f.close()
    cleanset()
    plot()

def cleanset():
    global res
    filt = []
    print(len(res))
    for i in res:
        if i not in filt:
            filt.append(i)
    print(filt)
    res = filt

genset()