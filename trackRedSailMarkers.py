import cv2
import numpy as np
import matplotlib.pyplot as plt
import pprint
import time
import math

filename = 'Data1/t4.mp4'

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


def make_image_mask_green(img):
    # B G R
    lower_blue = np.array([10,70,10],  dtype=np.uint8)# np.array([60,30,55])
    upper_blue = np.array([150,250,60],  dtype=np.uint8)
    
    # Threshold the HSV image to get only blue colors
    img = colorImgPreProcess(img)
    try:
        thresh = cv2.inRange(img, lower_blue, upper_blue)
        #cv2.imshow('mask', thresh)
        return thresh
    except:
        print "Fatal inRange error!"
        return ''


def make_image_mask_red(img):
    # B G R
    lower_blue = np.array([23,0,80],  dtype=np.uint8)# np.array([60,30,55])
    upper_blue = np.array([100,80,255],  dtype=np.uint8)
    
    # Threshold the HSV image to get only blue colors
    try:
        thresh = cv2.inRange(img, lower_blue, upper_blue)
        #cv2.imshow('mask', thresh)
        return thresh
    except:
        print "Fatal inRange error!"
        return ''
    
    

def get_red_circle(frame): 
    global numberErrorsFt
    global centerFt
    global radiusFt
    
    side_mask = make_image_mask_red(frame)
    if type(side_mask) != type(''):
        contours, hierarchy = cv2.findContours(side_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)        

        if len(contours):
            cnt = contours[0]
            (x,y),radiusFt = cv2.minEnclosingCircle(cnt)
            centerFt = (int(x),int(y))
            radiusFt = int(radiusFt)
            side_mask = cv2.cvtColor(side_mask, cv2.COLOR_GRAY2RGB)
            
            #cv2.circle(side_mask, center, radius, np.array([0,0,255]), 10)
            #cv2.rectangle(frame,center,(center[0]+240,center[1]+40),(0,255,0),3)
            #cv2.imshow('mask', frame)#side_mask)
            #cv2.imshow('mask', side_mask)

        else:
            numberErrors = numberErrors + 1
            #print 'Current number of front error frames is: ', numberErrorsFt, ' Out of: ', frameNum
            #print 'Front percent error is: ', 100*float(numberErrors)/frameNum
            #cv2.circle(side_mask, centerFt, radiusFt, np.array([0,255,0]), 10)



def get_green_circle(frame): 
    global numberErrorsBk
    global centerBk
    global radiusBk
    
    side_mask = make_image_mask_green(frame)
    if type(side_mask) != type(''):
        contours, hierarchy = cv2.findContours(side_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours):
            cnt = contours[0]
            (x,y),radiusBk = cv2.minEnclosingCircle(cnt)
            centerBk = (int(x),int(y))
            radiusBk = int(radiusBk)
            side_mask = cv2.cvtColor(side_mask, cv2.COLOR_GRAY2RGB)
            
            #cv2.circle(side_mask, center, radius, np.array([0,0,255]), 10)
            #cv2.rectangle(frame,center,(center[0]+240,center[1]+40),(0,255,0),3)
            #cv2.imshow('mask', frame)#side_mask)
            #cv2.imshow('mask', side_mask)
            #print 'center: ', center, 'radius: ', radius, ' found from side camera'
            
#            return center, radius

        else:
            numberErrorsBk = numberErrorsBk + 1
            #print 'Current number of back error frames is: ', numberErrorsBk, ' Out of: ', frameNum
            #print 'Back percent error is: ', 100*float(numberErrorsBk)/frameNum
            #cv2.circle(side_mask, centerBk, radiusBk, np.array([0,255,0]), 10)
            #cv2.imshow('mask', side_mask)
        #cv2.imshow('mask', side_mask)
#            return 0, 0



##Open Video file:
cap = cv2.VideoCapture(filename) 

while(cap.isOpened()):
    ret, frame = cap.read()
    get_green_circle(frame)
    centerPBk, radiusPBk = centerBk, radiusBk
    get_red_circle(frame)
    centerPFt, radiusPFt = centerFt, radiusFt
    
    if centerBk: 
        centerArrayX.append(centerBk[0])
        centerArrayY.append(centerBk[1])
    else: 
        'In P block. centerP is: ', centerPBk
        centerArrayX.append(centerPBk[0])
        centerArrayY.append(centerPBk[1])
    if centerFt:
        centerArrayA.append(centerFt[0])
        centerArrayB.append(centerFt[1])
    else: 
        centerArrayA.append(centerPFt[0])
        centerArrayB.append(centerPFt[1])        

    #cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frameNum =frameNum + 1
    ##print 'Frame num is: ', frameNum
    if frameNum >= cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
        plt.plot(centerArrayX, label='1')
        ##Filter out extreme values: 
#        centerArrayX = np.array(centerArrayX)
#        plt.plot(centerArrayX, label='2')
#        centerArrayX = reject_outliers(centerArrayX)
#        plt.plot(centerArrayX, label='3')
#        
#        ##Convert to angle:
#        #bkDegrees = [ for i in centerArrayX]
#        f = np.vectorize(posToTheta, otypes=[np.float])
#        bkDegrees = f(centerArrayX)  # if A is your Numpy array

        ##Display sumary stats: 
        print 'SUMMARY: '
        print 'Back flag: ', numberErrorsBk, ' errors out of ', frameNum
        print '   ', 100*float(numberErrorsBk)/frameNum, ' % frames without a circle found'
        print 'Front flag: ', numberErrorsFt, ' errors out of ', frameNum
        print '   ', 100*float(numberErrorsFt)/frameNum, ' % frames without a circle found'
                
        ##Plot data!:
        plt.plot(centerArrayX, label = 'Back Flag Angle', color='#AA3C39', linewidth=6)
        plt.plot(centerArrayA, label = 'Front Flag Angle', color='#7A9E35', linewidth=6)
        plt.xlabel('Image Frame #', fontsize = 18)
        plt.ylabel('Angle (degrees)', fontsize = 18)
        plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
        plt.legend()
        plt.show()
        
        break

cap.release()
#cv2.destroyAllWindows()
