from keras.models import model_from_json
from PIL import Image
import numpy as np
import cv2
import tensorflow as tf
tf.logging.info('TensorFlow')
tf.logging.set_verbosity(tf.logging.ERROR)
tf.logging.info('TensorFlow')

class Classifier:
    def __init__(self, json_file = 'model.json', weights_file = 'model.h5'):
        # load json and create model
        self.json_file = open(json_file, 'r')
        self.loaded_model_json = self.json_file.read()
        self.json_file.close()
        self.model = model_from_json(self.loaded_model_json)
        # load weights into new model
        self.model.load_weights(weights_file)
        print('Loaded Model From Disk successfully')
        
        # compile the model
        #self.model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', 
        #                    metrics = ['accuracy'])
        #print('Compiled model successfully')
    
    def convert_to_array(self, image):
        image = cv2.imread(image)
        image = Image.fromarray(image, 'RGB')
        image = image.resize((50,50))

        return np.array(image)

    def get_animal_name(self, label):
        if label==0:
            return True
        if label==1:
            return False
    
    def predict_animal(self, file):
     
        ar = self.convert_to_array(file)
        ar = ar/255.0
        label = 1
        a = []
        a.append(ar)
        a = np.array(a)
        #verbose == 0 is silent and verbose of 1 displayes the calculation
        score = self.model.predict(a,verbose = 0) 
        #print(score)
        label_index = np.argmax(score)
        #print(label_index)
        accuracy = np.max(score)
        animal = self.get_animal_name(label_index)
        return animal, accuracy



