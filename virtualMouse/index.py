import cv2 as cv
import mediapipe
import numpy as np
# It includes functions for controlling the keyboard and mouse
import autopy

# 0 is used as a prop to return the first webcam on the device 
cap = cv.VideoCapture(0)
# Initializing mediapi
initHand = mediapipe.solutions.hands  
# initalize hand detication and tracking with seistivity values
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
# initialize object to draw the connections between each fingers tips
draw = mediapipe.solutions.drawing_utils  

# Outputs the high and width of the screen (1920 x 1080)
wScr, hScr = autopy.screen.size()  
pX, pY = 0, 0  # Previous x and y location
cX, cY = 0, 0  # Current x and y location


# image is sent as argumnet
def handLandmarks(colorImg):
    # Default values if no landmarks are tracked
    landmarkList = []  

    # processed image with hand mardks
    landmarkPositions = mainHand.process(colorImg) 
    
    # returns false(None) if no hands are detected
    landmarkCheck = landmarkPositions.multi_hand_landmarks 
    
    # if there is a detected hand
    if landmarkCheck:  
        for hand in landmarkCheck:  # Landmarks for each hand
            for index, landmark in enumerate(hand.landmark):  # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)  # Draws each individual index on the hand with connections
                h, w, c = img.shape  # Height, width and channel on the image
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)  # Converts the decimal coordinates relative to the image for each index
                landmarkList.append([index, centerX, centerY])  # Adding index and its coordinates to a list
    return landmarkList


def fingers(landmarks):
    fingerTips = []  # To store 4 sets of 1s or 0s
    # Indexes for the tips of each finger
    tipIds = [4, 8, 12, 16, 20]  
    
    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)
    
    # Check if index finder are up except the thumb
    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

positionX, positionY = 0,0

while True:
    ## check: image success check, img: frame, read(): reads frames from camera
    check, img = cap.read() 

    # Change color formate
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)
    
    # if lenght is not equal to zero (to avoid crashing in the first frame)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Gets index 8s x and y values (skips index value because it starts from 1)
        x2, y2 = lmList[12][1:]  # Gets index 12s x and y values (skips index value because it starts from 1)
        # Calling the fingers function to check which fingers are up
        finger = fingers(lmList)  

        
        if finger[1] == 1 and finger[2] == 0:  # Checks to see if the pointing finger is up and thumb finger is down
            x3 = np.interp(x1, (75, 640 - 75), (0, wScr))  # Converts the width of the window relative to the screen width
            print(x3)
            y3 = np.interp(y1, (75, 480 - 75), (0, hScr))  # Converts the height of the window relative to the screen height
            
            cX = pX + (x3 - pX) / 7  # Stores previous x locations to update current x location
            cY = pY + (y3 - pY) / 7  # Stores previous y locations to update current y location
            
            autopy.mouse.move(wScr-cX, cY)  # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)
            pX, pY = cX, cY  # Stores the current x and y location as previous x and y location for next loop
            if pX != 0 and pY != 0:
                positionX, positionY = pX,pY 

        print(positionX, positionY)
        # pointer down / thumb up => left click
        if finger[1] == 0 and finger[0] == 1:  
            autopy.mouse.click()
            
            img = cv.circle(img, (int(positionX//2.4), int(positionY//1.8)), 15, (0,255,255), -1)
            
    # display image on Webcam window
    cv.imshow("Webcam", img)
    # break the loop on q press
    if (cv.waitKey(1) == ord('q')):
        break

# close all windows after breaking the loop
cap.release()
cv.destroyAllWindows()