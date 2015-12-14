import cv2
import numpy as np

filename = 'Transport TestFlutter0.mp4'


def make_image_mask(img):
    # B G R
    lower_blue = np.array([0,0,120])# np.array([60,30,55])
    upper_blue = np.array([70,70,200])
    
    # Threshold the HSV image to get only blue colors
    thresh = cv2.inRange(img, lower_blue, upper_blue)
    
    cv2.imshow('mask', thresh)
    return thresh

def get_circle(frame): 
       
    side_mask = make_image_mask(frame)
    contours, hierarchy = cv2.findContours(side_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    print len(contours)
    cnt = contours[0]
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    side_mask = cv2.cvtColor(side_mask, cv2.COLOR_GRAY2RGB)
    #cv2.circle(side_mask, (447,63), 63, (0,0,255), -1)
    cv2.circle(side_mask, center, radius, np.array([0,0,255]), 10)
    cv2.imshow('mask', side_mask)
    print 'center: ', center, 'radius: ', radius, ' found from side camera'
    
###    return side_center, radius

    return 1, 2



##Open Video file:
cap = cv2.VideoCapture(filename) 

while(cap.isOpened()):
    ret, frame = cap.read()
    center, radius = get_circle(frame)

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
