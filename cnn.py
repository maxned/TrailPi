from PIL import Image
import numpy as np 
import os
import cv2

import keras
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard

#create a cropper
def crop_image(img):
    w, h = img.size
    #croping 30 pixes from the bottom and 70 pixels from the top
    #in order to remove the labels that the trail pictures came with
    return img.crop((0, 30, w, h-70)) 

data = []
labels = []

animals = os.listdir("animals")
for animal in animals:
    if animal.startswith('.'):
        print(f'{animal} not read')
    else:
        img = Image.open("animals/" + animal)
        img = img.convert('RGB')
        #remove this next line if the image does not need cropping
        img = crop_image(img)
        resized_image = img.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(0)


people_images = os.listdir("people")
for people in people_images:
    if people.startswith('.'):
        print(f'{people} not read')
    else:
        img = Image.open("people/" + people)
        img = img.convert('RGB')
        #remove this next line if the image does not need cropping
        img = crop_image(img)
        resized_image = img.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(0)

nothing_images = os.listdir("nothing")
for nothing in nothing_images:
    if nothing.startswith('.'):
        print(f'{nothing} not read')
    else:
        img = Image.open("nothing/" + nothing)
        img = img.convert('RGB')
        #remove this next line if the image does not need cropping
        img = crop_image(img)
        resized_image = img.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(1)        

#creating the data augmentation object so that the training data can be more than what we have
datagen = ImageDataGenerator(
        rotation_range=10,
        zoom_range = 0.1,
        width_shift_range=0.1,
        height_shift_range=0.1)

# Converting data and labels to np array
trail_pics = np.array(data)
labels = np.array(labels)

#saving the np arrays to load later and not have to parse through the images again
np.save("trail_pics", trail_pics)
np.save("labels",labels)

#when we need to load them we use:
#trail_pics = np.load("trail_pics.npy")
#labels = np.load("labels.npy")

#shuffling animals and labels to get a good mixture
s = np.arange(trail_pics.shape[0])
np.random.shuffle(s)
trail_pics = trail_pics[s]
labels=labels[s]

#Make a variable num_classes which is the total 
#number of animal categories and a variable data_length which is size of dataset
num_classes = len(np.unique(labels))
data_length = len(trail_pics)

# Now we divide the data into a train (90%) and a test (10%) set
(x_train, x_test) = trail_pics[(int)(0.1 * data_length):],trail_pics[:(int)(0.1 * data_length)]
x_train = x_train.astype('float32')/255 #to convert to grayscale we didvide by 255
x_test = x_test.astype('float32')/255
train_length = len(x_train)
test_length = len(x_test)

#lables split into train and test
(y_train,y_test) = labels[(int)(0.1*data_length):],labels[:(int)(0.1*data_length)]

datagen.fit(x_train)

#Now we make the labels using one hot encoding
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

#making the Keras model with mulitple layers
model = Sequential()

model.add(Conv2D(32, kernel_size=5,input_shape=(50, 50, 3), activation = 'relu'))
model.add(Conv2D(32, kernel_size=5, activation = 'relu'))
model.add(MaxPool2D(2,2))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(64, kernel_size=3,activation = 'relu'))
model.add(Conv2D(64, kernel_size=3,activation = 'relu'))
model.add(MaxPool2D(2,2))
model.add(BatchNormalization())
model.add(Dropout(0.4))

model.add(Conv2D(128, kernel_size=3, activation = 'relu'))
model.add(BatchNormalization())

model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(0.4))
model.add(Dense(128, activation = "relu"))
model.add(Dropout(0.4))
model.add(Dense(2, activation = "softmax"))


#Now we need to compile the model
# params:
#              loss- 'ategorical_optimizer' is commonly used as the loss funciton for classification
#         optimizer- 'adam' optimizer will tend to adjuts learning rate all throughout the training
#          matrics - 'accuracy' is the easiest one to think about in terms of how accurate our fitting is
optimizer=Adam(lr=0.001)
model.compile(optimizer = optimizer , loss = "categorical_crossentropy", metrics=["accuracy"])

#uncomment next line to see the summary of the various layers, 
#the shape of each filter and the number of parameters used
#model.summary() 

#To get a visualiation of the learning go to the location of the script and fid a folder called logs
#in terminal change your directory to the logs folder 
#example: cd C:\Users\Student\Desktop\DataSet\logs\1
#to see tensorboard open up a command prompt, if using a virtual environment, activate it, and cd to location of logs
#mentioned above. 
# type: tensorboard --logdir .
# the reason we use '.' is because we are in the directory that the log is in, if you're in 
#another directory then after --logdir put the directory location
#then open up a browser and go to: the site displayed on the terminal window, it will look somethign like: http://localhost:6006/
#tensorboard = TensorBoard(log_dir="logs/{}".format(time()))
tensorboard = TensorBoard(log_dir="logs/1")

#Training the model
model_try = model.fit_generator(datagen.flow(x_train,y_train, batch_size=64),
                              epochs = 1000, validation_data = (x_test,y_test),verbose = 1, steps_per_epoch=70,
                               callbacks = [tensorboard])



# Saving Model to JSON and weights
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

