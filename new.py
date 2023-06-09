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
        #ㄱㅖㅅㅗㄱ ㅆㅓㅇㅑ ㅎㅏㄴㅡㄴ ㄷㅔㅇㅣㅌㅓ ㅈㅓㅈㅏㅇ
        self.count = 0
        self.tmpval = [] #ㅇㅣㅈㅓㄴ ㅍㅡㄹㅔㅇㅣㅁㅇㅔㅅㅓㅇㅡㅣ ㅍㅣㄱㅅㅔㄹ
        self.txt = '0' #ㅎㅗㅣㅈㅓㄴ ㄱㅕㄹㅈㅓㅇㅎㅏㄴㅡㄴ ㅌㅔㄱㅅㅡㅌㅡ
        self.diff = [] #ㅂㅕㄴㅎㅗㅏㅎㅏㄴ ㅍㅣㄱㅅㅔㄹㄷㅡㄹㅇㅡㅣ ㅁㅗㅇㅡㅁ
        self.initarr = []

    def callback(self, data):
        try:
            # listen image topic
            img = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            #ㅇㅣㅁㅣㅈㅣ ㅅㅏㅇㅣㅈㅡ ㅅㅓㄹㅈㅓㅇ
            h, w, c = img.shape
            
            #ㅍㅣㄱㅅㅔㄹ ㅅㅜ ㅅㅔㄹ ㄸㅐ ㅍㅣㄹㅇㅛㅎㅏㄴ ㅂㅕㄴㅅㅜ ㅅㅓㄹㅈㅓㅇ
            etc = 0
            blue = 0
            red = 0
            error = 0
            blackarr = []
           
            
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
            
            if len(self.tmpval) == 0: #ㅊㅓㅅ ㅎㅗㅏㅁㅕㄴ
                for i in range(0, h, 15):
                    tmparr = []
                    for j in range(0, w, 15):
                        _tmp = list(img[i, j])
                        tmparr.append(_tmp)
                        if sum(_tmp) <= 150:
                            blackarr.append([i, j]) #rgbㄱㅏㅂㅅㅇㅡㄹ ㅂㅏㅌㅏㅇㅇㅡㄹㅗ ㄱㅓㅁㅇㅡㄴㅅㅐㄱ ㅍㅣㄱㅅㅔㄹ(ㅎㅗㅏㅁㅕㄴ ㅌㅔㄷㅜㄹㅣ)ㄹㅡㄹ ㅍㅏㅈㅇㅡㅁ
                    val.append(tmparr) 
                        
                self.tmpval = val #ㅍㅣㄱㅅㅔㄹ ㅈㅓㅈㅏㅇㅎㅏㄴㅡㄴ ㄱㅗㅅㅇㅔ ㅈㅣㅂㅇㅓㄴㅓㅎㅇㅡㅁ
                
                #ㅁㅗㄷㅡㄴ ㄱㅓㅁㅇㅡㄴㅅㅐㄱ ㅍㅣㄱㅅㅔㄹㄷㅡㄹㅇㅡㅣ ㅍㅕㅇㄱㅠㄴㅇㅡㄹ ㅈㅜㅇㄱㅏㄴㄱㅏㅂㅅㅇㅡㄹㅗ ㅈㅣㅈㅓㅇ. ㄱㅡ ㄱㅓㄴㅇㅡㄴㅅㅔㄱ ㅍㅣㄱㅅㅔㄹ ㅈㅗㅏㅇㅜㄹㅗ ㄱㅓㅁㅇㅡㄴㅅㅐㄱ ㄱㅏㅈㅏㅇ ㄱㅏㄲㅏㅇㅜㄴ ㅍㅣㄱㅅㅔㄹㅇㅡㄹ ㅅㅓㄴㅈㅓㅇㅎㅐ ㅈㅣㄱㅅㅏㄱㅏㄱㅎㅕㅇㅇㅡㄹ ㅁㅏㄴㄷㅡㄹㅇㅓ ㄱㅡ ㅇㅏㄴㅇㅔ ㅇㅣㅆㄴㅡㄴ ㅍㅣㄱㅅㅔㄹㄷㅡㄹ rgbㄹㅡㄹ ㅍㅏㄴㄷㅏㄴㅎㅐ ㅊㅗㄱㅣ ㅎㅗㅣㅈㅓㄴ ㅂㅏㅇㅎㅑㅇㅇㅡㄹ ㅅㅓㄹㅈㅓㅇㅎㅏㄴㄷㅏ.
                x = 0
                y = 0
                for dot in blackarr:
                    x += dot[0]
                    y += dot[1]
                x = int(x / len(blackarr))
                y = int(y / len(blackarr))
                xmin = blackarr[1]
                ymin = blackarr[0]
                
                xminval = abs(blackarr[0][0] - x)
                yminval = abs(blackarr[0][1] - y)
                for dot in blackarr:
                    if abs(dot[0] - x) < xminval:
                        xmin = dot[1]
                    if abs(dot[1] - y) < yminval:
                        ymin = dot[0]
                        
                xinit = x - abs(ymin - x)
                xfin = x + abs(ymin - x)
                yinit = y - abs(xmin - y)
                yfin = y + abs(xmin - y)
                
                #rgbㄹㅡㄹ ㅍㅏㄴㄷㅏㄴㅎㅐ ㅃㅏㄹㄱㅏㄴㅅㅐㄱ, ㅍㅏㄹㅏㄴㅅㅐㄱ, ㄴㅏㅁㅓㅈㅣㄹㅡㄹ ㅍㅏㄴㄷㅏㄴㅎㅏㄴㅡㄴ ㅋㅜㄷㅡ
                for i in range(xinit, xfin, 15):
                    for j in range(yinit, yfin, 15):
                        tmp = list(img[i, j])
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
                _max = max([blue, red, etc]) #ㅊㅗㅣㅂㅣㄴㄱㅏㅂㅅㅇㅡㄹ ㅛㅐㅅㅇㅡㄹㅗ ㅅㅓㄹㅈㅓㅇ
                if _max == blue:
                    self.txt = '+1'
                elif _max == red:
                    self.txt = '-1'
                else:
                    self.txt = '0'
                        
                
            else: #ㅇㅏㅍㅇㅔ ㅎㅗㅏㅁㅕㄴㅇㅣㅇㅣㅆㅇㅓㅆㄷㅓㄴ ㄱㅕㅇㅇㅜ
                for i in range(0, h, 15):
                    tmparr = []
                    for j in range(0, w, 15):
                        tmp = list(img[i, j])
                        ttmp = list(self.tmpval[int(i / 15)][int(j / 15)])
                        
                        #ㅇㅣㅈㅓㄴㄱㅗㅏ ㅂㅣㄱㅛㅎㅐ ㅇㅓㄹㅁㅏㄴㅏㅁㅏㄴㅎㅇㅣ ㄷㅏㄹㄹㅏㅈㅕㅆㄴㅡㄴㅈㅣㄹㅡㄹ ㅍㅏㄴㄷㅏㄴㅎㅏㄴㄷㅏ
                        if (abs(int(tmp[0]) - int(ttmp[0])) + abs(int(tmp[1]) - int(ttmp[1])) + abs(int(tmp[2]) - int(ttmp[2]))) >= 200:
                            tmpdiff.append([i, j])
                            
                        tmparr.append(tmp)
                    val.append(tmparr)
                    
                if len(tmpdiff) > len(self.diff): # ㅂㅏㄲㅜㅣㄴ ㅂㅜㅂㅜㄴㅇㅣ ㄷㅓ ㅁㅏㄴㅎㄷㅏㅁㅕㄴ ㅎㅐㄷㅏㅇ ㅂㅏㄲㅜㅣㄴ ㅂㅜㅂㅜㄴㅇㅡㄹ ㅁㅗㄴㅣㅌㅓ ㅇㅕㅇㅇㅕㄱㅇㅡㄹㅗ ㅅㅓㄹㅈㅓㅇ
                    self.diff = tmpdiff
                    #ㅇㅕㄱㅣㅅㅓ ㅁㅜㄴㅈㅔㅈㅓㅁㅇㅣ ㅂㅏㄹㅅㅐㅇ->ㅈㅣㄴㄷㅗㅇㅅㅜ ㄸㅐㅁㅜㄴㅇㅔ ㄲㅗㅁㅅㅜㄹㅗ ㅂㅏㄲㅜㅣㄴ ㅍㅣㄱㅅㅔㄹ ㅇㅛㅅㅗㄹㅡㄹ ㅇㅣㄹㅇㅣㄹㅇㅣ ㅂㅣㄱㅛㅎㅐㅅㅓ ㅂㅜㅈㅗㄱㅎㅏㄴ ㅂㅜㅂㅜㄴㅇㅡㄹ ㅊㅐㅇㅜㅓㄴㅓㅎㄴㅡㄴㄱㅔ ㅇㅏㄴㅣㄹㅏ ㅌㅗㅇㅉㅐㄹㅗ ㅂㅕㄴㄱㅕㅇ. ㅇㅣ ㅂㅜㅂㅜㄴㅇㅣ ㄱㅐㅅㅓㄴㄷㅗㅣㄹ ㅅㅜ ㅇㅣㅆㄸㅏㄱㅗ ㅅㅐㅇㄱㅏㄱㅎㅏㅁ.
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
                    
                                   
                if len(tmpdiff) > 10: #ㅁㅏㄴㅎㅇㅣ ㅂㅏㄲ ㅣㅇㅓㅆㄷㅏㅁㅕㄴ ㅅㅐㄱㅅㅏㅇ ㅂㅕㄴㄱㅕㅇ
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
