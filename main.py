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
        self.tmpval = []
        self.txt = '0'
        self.diff = []

    def callback(self, data):
        try:
            # listen image topic
            img = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            h, w, c = img.shape
            etc = 0
            blue = 0
            red = 0
            error = 0
            
            #cv2.imshow('Image', img)
            cv2.waitKey(1)

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP
            
            #img data format : [B, G, R]
            val = []
            tmpdiff = []
            
            if len(self.tmpval) == 0:
                for i in range(0, h, 15):
                    tmparr = []
                    for j in range(0, w, 15):
                        tmparr.append(list(img[i, j]))
                    val.append(tmparr)
                        
                self.tmpval = val
                
            else:
                for i in range(0, h, 15):
                    tmparr = []
                    for j in range(0, w, 15):
                        tmp = list(img[i, j])
                        ttmp = list(self.tmpval[int(i / 15)][int(j / 15)])
                        
                        if (abs(int(tmp[0]) - int(ttmp[0])) + abs(int(tmp[1]) - int(ttmp[1])) + abs(int(tmp[2]) - int(ttmp[2]))) >= 200:
                            tmpdiff.append([i, j])
                            
                        tmparr.append(tmp)
                    val.append(tmparr)
                    
                if len(tmpdiff) > len(self.diff):
                    self.diff = tmpdiff
                for arr in self.diff:
                    tmp = list(img[arr[0], arr[1]])
                    if tmp[0] >= 200 and tmp[1] >=200 and tmp[2] >= 200:
                        etc += 1
                    elif tmp[2] >= 200 and tmp[0] < 200 and tmp[1] < 200:
                        red += 1
                    elif tmp[0] >= 200 and tmp[1] < 200 and tmp[2] < 200:
                        blue += 1
                    else:
                        if tmp[0] < 200 and tmp[1] < 200 and tmp[2] < 200:
                            if tmp[0] > 100 and tmp[0] > tmp[2]:
                                blue += 1
                            else:
                                etc += 1
                        else:
                            etc += 1
                    
                                   
                if len(tmpdiff) > 10:
                    _max = max([blue, red, etc])
                    if _max == blue:
                        self.txt = '+1'
                    elif _max == red:
                        self.txt = '-1'
                    else:
                        self.txt = '0'
                

            # msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)
            
            msg.frame_id = self.txt
            
            self.color_pub.publish(msg)
            
            self.tmpval = val

        except CvBridgeError as e:
            print(e)

    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('CompressedImages1', anonymous=False)
    detector = DetermineColor()
    rospy.spin()
