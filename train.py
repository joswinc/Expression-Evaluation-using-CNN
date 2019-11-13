import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm      # a nice pretty percentage bar for tasks. 
import os, os.path
from os import listdir
from os.path import isfile, join,isdir
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"]="1"

DIR = 'extracted_images'
subDIR = []
IMG_SIZE = 40
LR = 1e-3
training_data = []
test_data = []
label = {}

def check_labels():
    subDIR = [f for f in listdir(DIR) if isdir(join(DIR, f))]
    subDIRoriginal = subDIR
    labelcount=0
    for subD in subDIRoriginal:
        label[labelcount]=subD
        labelcount+=1
    return subDIR
    

#MODEL_NAME = 'numbers-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match


subDIR = check_labels()
for m in label:
    print(m)
    print(label[m])

def create_train_data():
    
    
    for subD in subDIR:
        temp_array = []
        temp = []
        for i in range (0,len(subDIR)):
                if(subD!=label[i]):
                    temp.append(0)
                else:
                    temp.append(1)
        count=0
        for img in tqdm(os.listdir(DIR+'/'+subD)):
            if count<950:
                path = os.path.join(DIR+'/'+subD,img)
                img = cv2.imread(path,0)            
                img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))            
                training_data.append([np.array(img),np.array(temp)])
                count+=1
            elif count<2800:
                path = os.path.join(DIR+'/'+subD,img)
                img = cv2.imread(path,0)            
                img = cv2.resize(img, (IMG_SIZE,IMG_SIZE)) 
                test_data.append([np.array(img),np.array(temp)])
                count+=1
            else:
                break
        
        
    shuffle(training_data)
    shuffle(test_data)
    
    #np.save('train_data.npy', training_data)
    
create_train_data()
print(len(training_data))
print(len(test_data))


import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

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

convnet = fully_connected(convnet, len(subDIR), activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')



train = training_data


count = len(train)
X = np.array([i[0].reshape(IMG_SIZE,IMG_SIZE,1) for i in training_data])
Y = [i[1] for i in training_data]
Y = np.array(Y).reshape(-1,len(subDIR))

test_x = np.array([i[0].reshape(IMG_SIZE,IMG_SIZE,1) for i in test_data])
test_y = [i[1] for i in test_data]
test_y = np.array(test_y).reshape(-1,len(subDIR))

model.fit({'input': X}, {'targets': Y}, n_epoch=40, validation_set=({'input': test_x}, {'targets': test_y}),snapshot_step=len(train), show_metric=True, run_id='numbers')

model.save('numbers_new')


#print(model.predict(test_x[0].reshape(1,IMG_SIZE,IMG_SIZE,1)))
#print(test_y[0])
