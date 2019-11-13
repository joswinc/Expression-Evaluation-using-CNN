#program to predict the handwritten numbers
import numpy as np
import cv2
import matplotlib.pyplot as plt
#import joblib
import cv2
import numpy as np
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import pandas as pd 
import matplotlib.pyplot as plt
label={}
result=''
IMG_SIZE=40
LR = 1e-3

      





def evaluate(path,model):
    label={'0':'5','1':'6','2':'*','3':'3','4':'(','5':'+','6':'0','7':'4','8':'-','9':'7','10':'8','11':'9','12':'1','13':'2','14':')'}
    image = cv2.imread(path,0)
    infix=""
    #plt.imshow(image,cmap="gray")
    #blured = cv2.GaussianBlur(image,(5,5),0)
    #plt.imshow(blured,cmap="gray")
    #_, thresholdImage = cv2.threshold(blured, 95, 255, cv2.THRESH_BINARY_INV)
    ret,thresholdImage1 = cv2.threshold(image,100,255,cv2.THRESH_BINARY_INV)
    plt.imshow(thresholdImage1,cmap="gray")
    #ret,thresholdImage = cv2.threshold(image,245,255,cv2.THRESH_BINARY)
    #plt.imshow(thresholdImage,cmap="gray")
    contours,_heir = cv2.findContours(thresholdImage1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(ctr) for ctr in contours]
    rects.sort()
    for i in range(0,len(rects)):
        val1 = rects[i]
        x,y,w,h=rects[i]
        #image = cv2.rectangle(thresholdImage,(x-10,y-10),(x+w+10,y+h+10),(255,255,255),2)
        #plt.imshow(image,cmap="gray")
        #plt.imshow(thresholdImage[val1[1]-5:val1[1]+val1[3]+5,val1[0]-5:val1[0]+val1[2]+5])
        #leng = int(h*1.5)
        #pt1 = int(y+h//2-leng//2)
        #pt2 = int(x+w//2-leng//2)
        test = image[val1[1]-5:val1[1]+val1[3]+5,val1[0]-5:val1[0]+val1[2]+5]
        #plt.imshow(test,cmap="gray")
        new_img = cv2.resize(test, (IMG_SIZE,IMG_SIZE))
        #plt.imshow(new_img,cmap="gray")
        new_img = new_img.reshape(1,IMG_SIZE,IMG_SIZE,1)
        
        y_pred = model.predict(new_img)
        index = 0
        count = -1
        max_pred=y_pred[0][0]
        for i in y_pred[0]:
            count+=1
            if max_pred<i:
                max_pred=i
                index=count
            
        #for label_val, value in label.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
        #    if value == index:
        #       print(label_val)
        #cv2.putText(image,label_val,(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)
        #print(label[str(index)])
        infix=infix+label[str(index)]
        
        #cv2.putText(image,label[str(index)],(x,y),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)
        
    #plt.imshow(image,cmap="gray")
    
    def Infix(expr):
        expr = list(expr)
        stack = list()
        num = ""
        while len(expr) > 0:
            c = expr.pop(0)
            if c in "0123456789.":
                num += c
                if len(expr)==0:
                    return num
            else:
                if num != "":
                    stack.append(num)
                    num = ""
                if c in "+-*/":
                    stack.append(c)
                elif c == ")":
                    num2 = stack.pop()
                    op = stack.pop()
                    num1 = stack.pop()
                    if op == "+":
                        stack.append(str(float(num1) + float(num2)))
                    elif op == "-":
                        stack.append(str(float(num1) - float(num2)))
                    elif op == "*":
                        stack.append(str(float(num1) * float(num2)))
                    elif op == "/":
                        stack.append(str(float(num1) / float(num2)))
        return stack.pop()
    
    print(infix)
    result = eval(infix)
    return result

