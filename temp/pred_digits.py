import cv2
import numpy as np
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import pandas as pd 
import matplotlib.pyplot as plt
IMG_SIZE=45
LR = 1e-3
label={'0':'(','1':')','2':'+','3':'-','4':'0','5':'1','6':'2','7':'3','8':'4','9':'5','10':'6','11':'7','12':'8','13':'9','14':'=','15':'/','16':'/','17':'*'}
convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input')

convnet = conv_2d(convnet, 32, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 32, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.5)

convnet = fully_connected(convnet, 18, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')

model.load('numbers-0.001-2conv-basic.model')  
#img = cv2.imread('6.jpg')
#img = cv2.imread('2.jpg')
img = cv2.imread('cl.jpg')
#img = cv2.imread('div.jpg')
new_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
new_img = cv2.resize(new_img, (IMG_SIZE,IMG_SIZE))
new_img = new_img.reshape(1,IMG_SIZE,IMG_SIZE,1)
#plt.imshow(new_img)
y_pred = model.predict(new_img)
index = 0
for i in y_pred:
    for j in i:
        index+=1
        if j==1:
            break
        

print(label[str(index)])