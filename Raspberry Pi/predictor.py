import sys
import os
from PIL import Image
from classifier.classifier import Classifier



cnn = Classifier(json_file = 'classifier/model.json', weights_file = 'classifier/model.h5')

def predict_animal(image_path):
    assert os.path.exists(image_path), "Image not found at: "+ str(image_path)
    animal, accuracy = cnn.predict_animal(image_path)
    if animal:
        return accuracy
    else:
        return 1.0-accuracy