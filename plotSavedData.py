import numpy as np
import matplotlib.pyplot as plt
import pprint
import math
import pickle
import scipy.stats as stats
#from trackRedSailMarkers import plotBothFlagPositions
#from trackRedSailMarkers import plotXXPositions




testNum = 24

filename = 'Data1/t'+str(testNum)+'.mp4'


centerArrayA = pickle.load( open( "At"+str(testNum)+".p", "rb" ) )
centerArrayB = pickle.load( open( "Bt"+str(testNum)+".p", "rb" ) )
centerArrayX = pickle.load( open( "Xt"+str(testNum)+".p", "rb" ) )
centerArrayY = pickle.load( open( "Yt"+str(testNum)+".p", "rb" ) )


def plotBothFlagPositions(a, b, x, y):
    ##Plot data!:
    plt.plot(x, y, marker='o', markersize=10, alpha=.7, linestyle='None', label = 'Back Flag Position', color='#AA3C39', linewidth=6)
    plt.plot(a, b, marker='o', markersize=10, alpha=.7, linestyle='None', label = 'Front Flag Position', color='#7A9E35', linewidth=6)
    plt.xlabel('Image Frame #', fontsize = 18)
    plt.ylabel('Angle (degrees)', fontsize = 18)
    plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
    plt.legend()
    plt.show()
    
# ## delete when on a real computer and replace with importing the correct plotting function
def plotXXPositions(a, x):
    plt.plot(a, x, marker='o', markersize=10, alpha=.7, linestyle='None', color='#7A9E35', linewidth=6)
    plt.xlabel('Front Flag Position (pixels)', fontsize = 18)
    plt.ylabel('Back Flag Position (pixels)', fontsize = 18)
    plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
    #plt.legend()
    plt.show()


#plotXXPositions(centerArrayA,centerArrayX)


## delete when on a real computer and replace with importing the correct plotting function



def filterByRemoval(data, ydata, time):
    std = stats.tstd(data)
    mean = stats.tmean(data)

    for i, x in enumerate(data):
        if x > mean + (1*std):
            data[i] = 'x'           
            ydata[i] = 'x'
            time[i] = 'x'
        elif x < mean - (2*std):
            data[i] = 'x'
            ydata[i] = 'x'
            time[i] = 'x'
    time.remove('x')
    data.remove('x')
    ydata.remove('x')
    return data, ydata, time
    
def filterByMutualRemoval(data1, data2):
    nSTD = .6

    std1 = stats.tstd(data1)
    mean1 = stats.tmean(data1)
    
    std2 = stats.tstd(data2)
    mean2 = stats.tmean(data2)
    
    print 'm1, std1: ', mean1, std1
    print 'm2, std2: ', mean2, std2
    
    for i, value in enumerate(data1): 
        if value > mean1 + (nSTD*std1):
            print 'c1: ', data1[i], data2[i]
            del data1[i]
            del data2[i]
        elif value < mean1 - (nSTD*std1):
            print 'c2: ', data1[i], data2[i]
            del data1[i]
            del data2[i]
            
    print 't2-t: ', mean2 + (nSTD*std2)
    print 't2-b ', mean2 - (nSTD*std2)
    for i, value in enumerate(data2): 
        if value > mean2 + (nSTD*std2):
            print 'c3: ', data1[i], data2[i]
            del data1[i]
            del data2[i]
        elif value < mean2 - (nSTD*std2):
            print 'c4: ', data1[i], data2[i]
            del data1[i]
            del data2[i]
    
    return data1, data2
	
	
timeArray = range(0, len(centerArrayA)) #np.arange(0, len(centerArrayA), 1)

## x is back flag

##Filter out extreme values: 
a, b, ta = filterByRemoval(centerArrayA[:], centerArrayB[:], timeArray[:])


#b, tb = filterByRemoval(centerArrayB[:], timeArray[:])
x, y, tx = filterByRemoval(centerArrayX[:], centerArrayY[:], timeArray[:])
#y, ty = filterByRemoval(centerArrayY[:], timeArray[:])




am, xm = filterByMutualRemoval(centerArrayA[:], centerArrayX[:])

	
#pprint.pprint( zip(am,xm))
#plotBothFlagPositions(a, b, x, y)
print 'lens: ', len(centerArrayA), len(am), len(centerArrayX), len(xm)

plt.clf()
plotXXPositions(xm, am)
plt.clf()
plotXXPositions(centerArrayX, centerArrayA)


