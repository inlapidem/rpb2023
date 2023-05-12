'''hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
bound_lower = np.array([25, 20, 20])
bound_upper = np.array([100, 255, 255])

mask_green = cv2.inRange(hsv_img, bound_lower, bound_upper)
kernel = np.ones((7,7),np.uint8)

mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

seg_img = cv2.bitwise_and(img, img, mask=mask_green)
contours, hier = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
output = cv2.drawContours(seg_img, contours, -1, (0, 0, 255), 3)

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('왼쪽 마우스 클릭 했을 때 좌표 : ', x, y)
cv2.setMouseCallback('img', onMouse)'''

# !/usr/bin/env python3
import rospy
import numpy as np
import cv2

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0

    def callback(self, data):
        try:
            # listen image topic
            img = self.bridge.imgmsg_to_cv2(data, 'bgr8')

            cv2.waitKey(1)

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP
            
            #checking : data over 200
            #img data format : [G, B, R]
            etc = -520
            red = 0
            blue = 0
            end = 0
            for i in range(87, 559, 10):
                for j in range(49, 367, 10):
                    tmparr = img[j, i]
                    if tmparr[0] >= 200 and tmparr[1] >=200 and tmparr[2] >= 200:
                        end += 1
                    elif tmparr[2] >= 200 and tmparr[0] < 200 and tmparr[1] < 200:
                        red += 1
                    elif tmparr[0] >= 200 and tmparr[1] < 200 and tmparr[2] < 200:
                        blue += 1
                    else:
                        if tmparr[0] < 200 and tmparr[1] < 200 and tmparr[2] < 200:
                            if tmparr[0] > 100 and tmparr[0] > tmparr[2]:
                                blue += 1
                            else:
                                etc += 1
                        else:
                            etc += 1
            
            _max = max([etc, red, blue, end])
            if _max == etc:
                msg.frame_id = '0'
            elif _max == red:
                msg.frame_id = '-1'
            elif _max == blue:
                msg.frame_id = '+1'
            else:
                msg.frame_id = '0'
            
            # msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)
            
            self.color_pub.publish(msg)

        except CvBridgeError as e:
            print(e)

    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('CompressedImages1', anonymous=False)
    detector = DetermineColor()
    rospy.spin()
   
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            contours, _ = cv2.findContours(adaptive_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            img_copy = img.copy()
            cv2.drawContours(image = img_copy, contours = contours, contourIdx = -1, color = (0, 255, 0), thickness = 2, lineType = cv2.LINE_AA)
            cv2.imshow('Image', img_copy)
