import cv2
import numpy as np
import matplotlib.pyplot as plt
import pprint

filename = 'Data1/t2.mp4'

numberErrors = 0
centerP = 0; radiusP = 0;
frameNum = 0
centerArrayX = []; centerArrayY = []


def make_image_mask(img):
    # B G R
    lower_blue = np.array([0,0,120],  dtype=np.uint8)# np.array([60,30,55])
    upper_blue = np.array([70,70,200],  dtype=np.uint8)
    
    # Threshold the HSV image to get only blue colors
    ##print 'hi 1'
    try:
        ##print 'trying thresh'
        thresh = cv2.inRange(img, lower_blue, upper_blue)
        ##print 'thresh successful: '
        ##print thresh
        #cv2.imshow('mask', thresh)
        return thresh
    except:
        print "Fatal inRange error!"
        cv2.imshow('mask', img)
        return ''
    
    

def get_circle(frame): 
    global numberErrors
    global center
    global radius
    
    ##print 'b4 mask'
    side_mask = make_image_mask(frame)
    ##print 'made mask'
    if type(side_mask) != type(''):
        contours, hierarchy = cv2.findContours(side_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ##print 'found contrs'
        

        if len(contours):
            cnt = contours[0]
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            side_mask = cv2.cvtColor(side_mask, cv2.COLOR_GRAY2RGB)
            
            cv2.circle(side_mask, center, radius, np.array([0,0,255]), 10)
            cv2.imshow('mask', side_mask)
            #print 'center: ', center, 'radius: ', radius, ' found from side camera'
            
#            return center, radius

#        else:
#            numberErrors = numberErrors + 1
#            print 'Current number of error frames is: ', numberErrors
#            return 0, 0



##Open Video file:
cap = cv2.VideoCapture(filename) 

while(cap.isOpened()):
    ret, frame = cap.read()
    #center, radius = 
    get_circle(frame)
    centerP, radiusP = center, radius
    
    if center: 
        centerArrayX.append(center[0])
        centerArrayY.append(center[1])
    else: 
        'In P block. centerP is: ', centerP
        centerArrayX.append(centerP[0])
        centerArrayY.append(centerP[1])
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frameNum =frameNum + 1
    ##print 'Frame num is: ', frameNum
    if frameNum == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):#frameNum > 273:
        #pprint.pprint(centerArray)
        plt.plot(centerArrayX, label = 'X marker positon', color='#AA3C39', linewidth=6)
        plt.plot(centerArrayY, label = 'Y marker positon', color='#7A9E35', linewidth=6)
        plt.xlabel('Time', fontsize = 18)
        plt.ylabel('Pixel Position', fontsize = 18)
        plt.title('Position of Fluttering Sail Through Time', fontsize = 20)
        plt.legend()
        plt.show()

cap.release()
#cv2.destroyAllWindows()
