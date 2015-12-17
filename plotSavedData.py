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


## delete when on a real computer and replace with importing the correct plotting function
def plotBothFlagPositions():
    ##Plot data!:
    plt.plot(centerArrayX, centerArrayY, marker='o', markersize=10, alpha=.7, linestyle='None', label = 'Back Flag Position', color='#AA3C39', linewidth=6)
    plt.plot(centerArrayA, centerArrayB, marker='o', markersize=10, alpha=.7, linestyle='None', label = 'Front Flag Position', color='#7A9E35', linewidth=6)
    plt.xlabel('Image Frame #', fontsize = 18)
    plt.ylabel('Angle (degrees)', fontsize = 18)
    plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
    plt.legend()
    plt.show()
    
## delete when on a real computer and replace with importing the correct plotting function
def plotXXPositions():
    plt.plot(centerArrayA, centerArrayX, marker='o', markersize=10, alpha=.7, linestyle='None', color='#7A9E35', linewidth=6)
    plt.xlabel('Front Flag Position (pixels)', fontsize = 18)
    plt.ylabel('Back Flag Position (pixels)', fontsize = 18)
    plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
    #plt.legend()
    plt.show()
	
	
	

plotBothFlagPositions()
plotXXPositions()


