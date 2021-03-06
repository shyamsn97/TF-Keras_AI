import numpy as np
import tensorflow as tf
from keras import *
from keras.layers import *
from keras import backend as K
from keras.utils import np_utils 
from keras.utils import plot_model
from keras.utils import to_categorical
from keras.models import *
from keras.optimizers import SGD
from keras.datasets import mnist
import pydot
import graphviz
import warnings
warnings.filterwarnings("ignore")

class AlexNet():
    """
    AlexNet implemented with Keras
    introduced in the paper "ImageNet Classification with Deep Convolutional Neural Networks"
    https://www.nvidia.cn/content/tesla/pdf/machine-learning/imagenet-classification-with-deep-convolutional-nn.pdf
    Parameters:
        X: numpy array data matrix 
        y: numpy array of labels, to_categorical changes it to a sparse binary matrix
        weights: name of file that denotes weights to load in
    """
    def __init__(self,X,y,weights="None"):
        
        self.X = X
        self.y = to_categorical(y)
                
        self.weights = weights
        self.model = None
        
        if self.weights == "None":
            self.initialize()
        else:
            self.model = load_model(weights)
    
    def transfer(self,path):
        self.model = load_model(path)
                
    def initialize(self):
        
        K.clear_session()
        
        n_outputs = self.y.shape[1]
        height = self.X.shape[1]
        width = self.X.shape[2]
        
        if len(self.X.shape) == 3:
            self.X = self.X.reshape(self.X.shape[0],self.X.shape[1],self.X.shape[2],1)
            inp = Input(shape=(self.X.shape[1],self.X.shape[2],1))
        else:
            inp = Input(shape=(self.X.shape[1],self.X.shape[2],3))

        conv1 = Conv2D(96,kernel_size=11,strides=4,border_mode='valid',activation='relu')(inp)
        max1 = MaxPool2D(3,strides=2,border_mode='same')(conv1)
        dropout1 = Dropout(0.5)(max1)
        normal1 = BatchNormalization()(dropout1)
        conv2 = Conv2D(256,kernel_size=5,border_mode='same')(normal1)
        max2 = MaxPool2D(3,strides=2,border_mode='same')(conv2)
        dropout2 = Dropout(0.5)(max2)
        normal2 = BatchNormalization()(dropout2)
        conv3 = Conv2D(384,kernel_size=3,border_mode='same')(normal2)
        conv4 = Conv2D(384,kernel_size=3,border_mode='same')(conv3)
        conv5 = Conv2D(256,kernel_size=5,border_mode='same')(conv4)
        max3 = MaxPool2D(3,strides=2,border_mode='same')(conv5)
        dropout3 = Dropout(0.5)(max3)
        flatten = Flatten()(dropout3)
        dense1 = Dense(4096,activation="relu")(flatten)
        dropout4 = Dropout(0.5)(dense1)
        dense2 = Dense(4096,activation="relu")(dropout4)
        dropout5 = Dropout(0.5)(dense2)
        dense3 = Dense(n_outputs,activation="linear")(dropout5)
        softmax = Softmax(n_outputs)(dense3)
        
        model = Model(inputs=inp,outputs=softmax)
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])
        self.model = model
        print(self.model.summary())
        
    def save_picture(self,filename):
        plot_model(self.model, to_file=filename)
        
    def train(self,epochs,save=True):

        self.model.fit(self.X, self.y ,validation_split=0.1, epochs=epochs,verbose=1)
        if save == True:
            self.model.save('saved_models/AlexNet.h5')
        loss, acc = self.model.evaluate(self.X, self.y, verbose=0)
        print('Train Accuracy: %f' % (acc*100))
        
    def predict(self,X):
        
        if len(X.shape) == 3:
            X = X.reshape(1,X.shape[0],X.shape[1],X.shape[2])
        predictions = self.model.predict(X)
        return np.argmax(predictions)

if __name__ == '__main__':

    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    #mini
    X_train = X_train[:1000]
    y_train = y_train[:1000]
    model = AlexNet(X_train,y_train)
    model.train(1)

        
        