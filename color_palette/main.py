import numpy as np
import pandas as pd
import cv2

img= cv2.imread("img.jpg")

index = ["color","color_name","hex","R","G","B"]

colors = pd.read_csv("color.csv",names=index, header=None)

clicked = False
r=g=b=xpos=ypos=0

#function to recognise the color using knn and return the name from colors.csv file
def detect_color(R,G,B):
    minimum = 10000
    for i in range(len(colors)):
        #Using K nearest neighbor to find the closest colors to the point clicked
        d = abs(R - int(colors.loc[i, "R"])) + abs(G - int(colors.loc[i, "G"])) + abs(B - int(colors.loc[i, "B"]))
        if (d <= minimum):
            minimum = d
            colorname = colors.loc[i, "color_name"]
    return colorname
#define the double click process
def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#create application window
cv2.namedWindow('Color Detector')
cv2.setMouseCallback('Color Detector', mouse_click)

while (1):
    cv2.imshow("Color Detector", img)
    if (clicked):

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        # Creating text string to display( Color name and RGB values )
        text = detect_color(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # For very light colours the text is displayed in black
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()