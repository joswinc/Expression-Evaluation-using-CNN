import flask
import werkzeug
import time
from contour import evaluate
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

result=''
IMG_SIZE=40
LR = 1e-3
label={'0':'5','1':'6','2':'*','3':'3','4':'(','5':'+','6':'0','7':'4','8':'-','9':'7','10':'8','11':'9','12':'1','13':'2','14':')'}
#label={'0':'(','1':')','2':'+','3':'-','4':'0','5':'1','6':'2','7':'3','8':'4','9':'5','10':'6','11':'7','12':'8','13':'9','14':'=','15':'*'}
    
convnet = input_data(shape=[None, IMG_SIZE,IMG_SIZE,1], name='input')
    
convnet = conv_2d(convnet, 18, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)
    
convnet = conv_2d(convnet, 36, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)
    
convnet = conv_2d(convnet, 72, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)
    
convnet = conv_2d(convnet, 36, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)
    
convnet = conv_2d(convnet, 18, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)
    
convnet = fully_connected(convnet, 25, activation='relu')
convnet = dropout(convnet, 0.5)
    
convnet = fully_connected(convnet, 15, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    
model = tflearn.DNN(convnet, tensorboard_dir='log')
    
model.load('Trained_model/numbers_new')

app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    files_ids = list(flask.request.files)
    print("IMAGE RECEIVED : ", len(files_ids))
    result=''
    for file_id in files_ids:
        print("\nSaving Image ", len(files_ids))
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        
        
        imagefile.save(filename)
        result = str(evaluate("test.jpg",model))
        print(result)
        
        
    
    return result

app.run(host="192.168.137.1", port=5000, debug=True)