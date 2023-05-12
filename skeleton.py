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
            
            #img data format : [B, G, R]
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
            cv2.imshow('Binary', thresh)
            
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
