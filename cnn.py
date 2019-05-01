from PIL import Image
import numpy as np 
import os
import cv2

import keras
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout

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
    
    img = Image.open("animals/" + animal)
    img = img.convert('RGB')
    img = crop_image(img)
    resized_image = img.resize((50, 50))
    data.append(np.array(resized_image))
    labels.append(0)

useless_images = os.listdir("useless")
for useless in useless_images:
    if useless.startswith('.'): #removing any images that start with a '.' as that messes with the parser
        print(f'{useless} not read')
    else:
        img = Image.open("useless/" + useless)
        img = img.convert('RGB')
        img = crop_image(img)
        resized_image = img.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(0)

false_positives = os.listdir("nothing")
for false in false_positives:
    
    img = Image.open("nothing/" + false)
    img = img.convert('RGB')
    img = crop_image(img)
    resized_image = img.resize((50, 50))
    data.append(np.array(resized_image))
    labels.append(1)        

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

#Now we make the labels using one hot encoding
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

#making the Keras model with mulitple layers
model=Sequential()

model.add(Conv2D(filters = 16,kernel_size = 2,padding="same",activation ="relu",input_shape =(50,50,3)))
model.add(MaxPooling2D(pool_size = 2))

model.add(Conv2D(filters = 32,kernel_size = 2,padding="same",activation ="relu"))
model.add(MaxPooling2D(pool_size = 2))

model.add(Conv2D(filters = 64,kernel_size = 2,padding = "same",activation ="relu"))
model.add(MaxPooling2D(pool_size=2))

model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(2,activation="softmax"))
#uncomment next line to see the summary of the various layers, 
#the shape of each filter and the number of parameters used
#model.summary() 

#Now we need to compile the model
# params:
#              loss- 'ategorical_optimizer' is commonly used as the loss funciton for classification
#         optimizer- 'adam' optimizer will tend to adjuts learning rate all throughout the training
#          matrics - 'accuracy' is the easiest one to think about in terms of how accurate our fitting is
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])


#Training the model
model.fit(x_train,y_train, batch_size = 500 ,epochs=10000, verbose=1)



# Saving Model to JSON and weights
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

