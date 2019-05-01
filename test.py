import sys
from classifier import *

file_name = sys.argv[1]
im = Image.open(file_name)

cnn = Classifier()

prediction = cnn.predict_animal(file_name)
print('Prediction: '+ prediction)

