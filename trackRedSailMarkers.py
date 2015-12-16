import cv2
import numpy as np
import matplotlib.pyplot as plt
import pprint
import math
import pickle
import scipy.stats as stats

testNum = 4

filename = 'Data1/t'+str(testNum)+'.mp4'

numberErrorsBk = 0
centerBk = 0; radiusBk = 0
centerPBk = 0; radiusPBk = 0;
numberErrorsFt = 0
centerPFt = 0; radiusPFt = 0;

frameNum = 0

Lbk = 240 #length of back flag, in pixels
centerArrayA = []; centerArrayB = [] ## Front Flag (red marker)
centerArrayX = []; centerArrayY = [] ## Back Flag (green marker)
thetaFlagFt = []; thetaFlagbk = []; 


def nothing(x):
    pass
    
hlg = 0
slg = 37
vlg = 60
hhg = 142
shg = 190
vhg = 135  


hlr = 104
slr = 69
vlr = 0
hhr = 255
shr = 255
vhr = 255

cv2.namedWindow('greenHSVMask')
# create trackbars for color change
cv2.createTrackbar('H_low_green','greenHSVMask',hlg,180,nothing)
cv2.createTrackbar('S_low_green','greenHSVMask',slg,255,nothing)
cv2.createTrackbar('V_low_green','greenHSVMask',vlg,255,nothing)
cv2.createTrackbar('H_high_green','greenHSVMask',hhg,180,nothing)
cv2.createTrackbar('S_high_green','greenHSVMask',shg,255,nothing)
cv2.createTrackbar('V_high_green','greenHSVMask',vhg,255,nothing)

cv2.namedWindow('redHSVMask')
# create trackbars for color change
cv2.createTrackbar('H_low_red','redHSVMask',hlr,180,nothing)
cv2.createTrackbar('S_low_red','redHSVMask',slr,255,nothing)
cv2.createTrackbar('V_low_red','redHSVMask',vlr,255,nothing)
cv2.createTrackbar('H_high_red','redHSVMask',hhr,180,nothing)
cv2.createTrackbar('S_high_red','redHSVMask',shr,255,nothing)
cv2.createTrackbar('V_high_red','redHSVMask',vhr,255,nothing)

def posToTheta(i):
    angle = math.acos( (Lbk - (max(centerArrayX) - i) )/Lbk )
    print angle
    return angle


def reject_outliers(data, m=2):
    """ From: 
    http://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
    """
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def colorImgPreProcess(image):
    """
    Prepare images to be analyzed in binary form by appling generic filtering.
    This makes them easier to work with and the resulting image less noisy.
    
    INPUT: image for pre-processing. Should be in color, though b&w should work.
    OUTPUT: returns a RGB image which has been filtered and looks nicer.
    """
    #do processing on the image while it's still in color
    image = cv2.medianBlur(image, 3)  #kernal size must be odd
    #image = cv2.bilateralFilter(image, 9, 75, 75) #TODO: uncomment when it won't cause C++ errors with ROS
    #self.closeImages() #uncomment if showing output image
    return image


def make_image_mask_green(img, a=40, b=10, c=10, d=80, e=200, f=255):
    # B G R
    #lower_blue = np.array([10,70,10],  dtype=np.uint8)# np.array([60,30,55])
    #upper_blue = np.array([150,250,60],  dtype=np.uint8)
    
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    # Threshold the HSV image to get only blue colors
    img = colorImgPreProcess(hsv_img)
    
    lower_bound = np.array([a, b, c],  dtype=np.uint8)
    upper_bound = np.array([d, e, f],  dtype=np.uint8)
    print 'upper_bound: ', upper_bound


    try:
        thresh = cv2.inRange(img, lower_bound, upper_bound)
        #cv2.imshow('green mask', thresh)
        return thresh
    except:
        print "Fatal inRange error in make_image_mask_green!"
        return ''
        

def make_image_mask_red(img, a=40, b=10, c=10, d=80, e=200, f=255):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    img = colorImgPreProcess(hsv_img)

    lower_bound = np.array([a, b, c],  dtype=np.uint8)
    upper_bound = np.array([d, e, f],  dtype=np.uint8)
    print 'red lower bound: ', lower_bound
    print 'red upper bound: ', upper_bound

    try:
        thresh = cv2.inRange(img, lower_bound, upper_bound)
        #cv2.imshow('Red Mask', thresh)
        return thresh
    except:
        print "Fatal inRange error in make_image_mask_red!"
        return ''


def make_image_mask_red_RGB(img):
    # B G R
    lower_blue = np.array([23,0,80],  dtype=np.uint8)# np.array([60,30,55])
    upper_blue = np.array([100,80,255],  dtype=np.uint8)
    
    # Threshold the HSV image to get only blue colors
    try:
        thresh = cv2.inRange(img, lower_blue, upper_blue)
        #cv2.imshow('Red RGB mask', thresh)
        return thresh
    except:
        print "Fatal inRange error in make_image_mask_red_RGB!"
        return ''
    
    

def get_red_circle(frame, hlr, slr, vlr, hhr, shr, vhr): 
    global numberErrorsFt
    global centerFt
    global radiusFt
    
    side_mask = make_image_mask_red(frame, hlr, slr, vlr, hhr, shr, vhr)
    if type(side_mask) != type(''):
        contours, hierarchy = cv2.findContours(side_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)        

        if len(contours):
            cnt = contours[0]
            (x,y),radiusFt = cv2.minEnclosingCircle(cnt)
            centerFt = (int(x),int(y))
            radiusFt = int(radiusFt)
            side_mask = cv2.cvtColor(side_mask, cv2.COLOR_GRAY2RGB)
            
            cv2.circle(side_mask, centerFt, radiusFt, np.array([0,0,255]), 10)
            cv2.imshow('Red mask', side_mask)

        else:
            numberErrorsFt = numberErrorsFt + 1



def get_green_circle(frame, hlg, slg, vlg, hhg, shg, vhg): 
    global numberErrorsBk
    global centerBk
    global radiusBk
    
    side_mask = make_image_mask_green(frame, hlg, slg, vlg, hhg, shg, vhg) #
    if type(side_mask) != type(''):
        contours, hierarchy = cv2.findContours(side_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours):
            cnt = contours[0]
            (x,y),radiusBk = cv2.minEnclosingCircle(cnt)
            centerBk = (int(x),int(y))
            radiusBk = int(radiusBk)
            side_mask = cv2.cvtColor(side_mask, cv2.COLOR_GRAY2RGB)
            
            cv2.circle(side_mask, centerBk, radiusBk, np.array([0,255,0]), 10)
            cv2.imshow('green mask', side_mask)
            #print 'center: ', center, 'radius: ', radius, ' found from side camera'

        else:
            print 'no contours found for green'
            numberErrorsBk = numberErrorsBk + 1
    else:
        print 'green string'



def findFtFlagMarker(frame, hlr, slr, vlr, hhr, shr, vhr):
    get_red_circle(frame, hlr, slr, vlr, hhr, shr, vhr)
    centerPFt, radiusPFt = centerFt, radiusFt
    if centerFt:
        centerArrayA.append(centerFt[0])
        centerArrayB.append(centerFt[1])
    else: 
        centerArrayA.append(centerPFt[0])
        centerArrayB.append(centerPFt[1])      
        
        
def findBkFlagMarker(frame, hlg, slg, vlg, hhg, shg, vhg):
    get_green_circle(frame, hlg, slg, vlg, hhg, shg, vhg)
    centerPBk, radiusPBk = centerBk, radiusBk

    if centerBk: 
        centerArrayX.append(centerBk[0])
        centerArrayY.append(centerBk[1])
    else: 
        'In P block. centerP is: ', centerPBk
        centerArrayX.append(centerPBk[0])
        centerArrayY.append(centerPBk[1])
        
        
def printSummaryStats():
    '''Display sumary stats: '''
    print 'SUMMARY: '
    print 'Back flag: ', numberErrorsBk, ' errors out of ', frameNum
    print '   ', 100*float(numberErrorsBk)/frameNum, ' % frames without a circle found'
    print 'Front flag: ', numberErrorsFt, ' errors out of ', frameNum
    print '   ', 100*float(numberErrorsFt)/frameNum, ' % frames without a circle found'  
    
          
def plotBothFlagPositions():
    ##Plot data!:
    plt.plot(centerArrayX, centerArrayY, marker='o', markersize=10, alpha=.7, linestyle='None', label = 'Back Flag Position', color='#AA3C39', linewidth=6)
    plt.plot(centerArrayA, centerArrayB, marker='o', markersize=10, alpha=.7, linestyle='None', label = 'Front Flag Position', color='#7A9E35', linewidth=6)
    plt.xlabel('Image Frame #', fontsize = 18)
    plt.ylabel('Angle (degrees)', fontsize = 18)
    plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
    plt.legend()
    plt.show()
    
def plotXXPositions():
    plt.plot(centerArrayA, centerArrayX, marker='o', markersize=10, alpha=.7, linestyle='None', color='#7A9E35', linewidth=6)
    plt.xlabel('Front Flag Position (pixels)', fontsize = 18)
    plt.ylabel('Back Flag Position (pixels)', fontsize = 18)
    plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
    #plt.legend()
    plt.show()

##Open Video file:
cap = cv2.VideoCapture(filename) 

while(cap.isOpened()):
    ret, frame = cap.read()
    height, width, channels = frame.shape
    frame = frame[350:600, 0:width] # Crop from x, y, w, h -> 100, 200, 300, 400
    
    #findFtFlagMarker(frame)
    hlg = cv2.getTrackbarPos('H_low_green','greenHSVMask')
    slg = cv2.getTrackbarPos('S_low_green','greenHSVMask')
    vlg = cv2.getTrackbarPos('V_low_green','greenHSVMask')
    hhg = cv2.getTrackbarPos('H_high_green','greenHSVMask')
    shg = cv2.getTrackbarPos('S_high_green','greenHSVMask')
    vhg = cv2.getTrackbarPos('V_high_green','greenHSVMask')  
    
    
    hlr = cv2.getTrackbarPos('H_low_red','redHSVMask')
    slr = cv2.getTrackbarPos('S_low_red','redHSVMask')
    vlr = cv2.getTrackbarPos('V_low_red','redHSVMask')
    hhr = cv2.getTrackbarPos('H_high_red','redHSVMask')
    shr = cv2.getTrackbarPos('S_high_red','redHSVMask')
    vhr = cv2.getTrackbarPos('V_high_red','redHSVMask')  

    
    ## Testing only, make image masks
    #make_image_mask_green(frame, hlg, slg, vlg, hhg, shg, vhg)
    #make_image_mask_red(frame, hlr, slr, vlr, hhr, shr, vhr)
    
    ## Testing only, only find circles
    #get_red_circle(frame, hlr, slr, vlr, hhr, shr, vhr)
    #get_green_circle(frame, hlg, slg, vlg, hhg, shg, vhg)
    
    ## Production Use!!!
    findFtFlagMarker(frame, hlr, slr, vlr, hhr, shr, vhr)
    findBkFlagMarker(frame, hlg, slg, vlg, hhg, shg, vhg)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    frameNum =frameNum + 1
    if frameNum >= cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
        ## Now that we're done, let's save the data!
        pickle.dump(centerArrayX, open( "Xt"+str(testNum)+".p", "wb" ) )
        pickle.dump(centerArrayY, open( "Yt"+str(testNum)+".p", "wb" ) )
        pickle.dump(centerArrayA, open( "At"+str(testNum)+".p", "wb" ) )
        pickle.dump(centerArrayB, open( "Bt"+str(testNum)+".p", "wb" ) )
        
        
##        ##Filter out extreme values: 
##        stdx = stats.tstd(centerArrayX)
##        meanx = stats.tmean(centerArrayX)
##        for x in centerArrayX:
##            if 


#        centerArrayX = np.array(centerArrayX)
#        plt.plot(centerArrayX, label='2')
#        centerArrayX = reject_outliers(centerArrayX)
#        plt.plot(centerArrayX, label='3')


        printSummaryStats()
        plotBothFlagPositions()
        plotXXPositions()

        break

cap.release()
#cv2.destroyAllWindows()
