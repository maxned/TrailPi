from keras.models import model_from_json
from PIL import Image
import numpy as np
import cv2

class classifier:
    def __init__(self, json_file = 'model.json', weights_file = 'model.h5'):
        # load json and create model
        self.json_file = open(json_file, 'r')
        self.model = self.json_file.read()
        self.json_file.close()
        # load weights into new model
        self.model.load_weights(weights_file)
        print('Loaded Model From Disk successfully')
        # compile the model
        self.model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', 
                            metrics = ['accuracy'])
        print('Compiled model successfully')
    
    def convert_to_array(self, image):
        image = cv2.imread(image)
        image = Image.fromarray(image, 'RGB')
        image = image.resize((50,50))

        return np.array(image)

    def get_animal_name(self, label):
        if label==0:
            return "animal"
        if label==1:
            return "nothing"
    
    def predict_animal(self, file):
        print("Predicting .................................")
        ar = self.convert_to_array(file)
        ar = ar/255
        label = 1
        a = []
        a.append(ar)
        a = np.array(a)
        score = model.predict(a,verbose = 1)
        #print(score)
        label_index = np.argmax(score)
        #print(label_index)
        acc = np.max(score)
        animal = get_animal_name(label_index)
        print(animal)
        print("The predicted image is  "+ animal +" with accuracy =    "+str(acc))
        return animal



