import cv2
import numpy as np

filename = 'Transport TestFlutter0.mp4'


def make_image_mask(img):
#    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
#    ret,thresh = cv2.threshold(img,40,255,cv2.THRESH_BINARY)
#         define range of blue color in HSV
    lower_blue = np.array([60,30,55])
    upper_blue = np.array([200,50,80])

    # Threshold the HSV image to get only blue colors
    thresh = cv2.inRange(img, lower_blue, upper_blue)
    cv2.imshow('mask', thresh)
    return thresh

def get_circle(frame):    
    side_mask = make_image_mask(frame)
    contours, hierarchy = cv2.findContours(side_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
###    cnt = contours[0]
###    (x,y),radius = cv2.minEnclosingCircle(cnt)
###    side_center = (int(x),int(y))
###    side_radius = int(radius)
    #print 'center: ', side_center, 'radius: ', side_radius, ' found from side camera'
    
###    return side_center, radius



##Open Video file:
cap = cv2.VideoCapture(filename) 

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

###for i in range(start_val,end_val):
###    # Capture frame-by-frame
###    #frame = cv2.imread('5-11_data_collection/test{}/test{}image{}.jpg'.format(str(testNum), str(testNum), str(i)))
###    
###    

###    # Our operations on the frame come here
###    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
######    center, radius = get_circle(frame)
###    get_circle(frame)
######    radius = int(radius)
######    print center , radius
######    img = cv2.circle(frame,center,radius,(0,255,0),2)
###    # Display the resulting frame
###    cv2.imshow('frame',frame)
###    time.sleep(.1)

###    if cv2.waitKey(1) & 0xFF == ord('q'):
###        print 'hi'

#### When everything done, release the capture
cv2.destroyAllWindows()
