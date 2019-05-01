import sys
from PIL import Image
from classifier import Classifier

file_name = sys.argv[1]
im = Image.open(file_name)

cnn = Classifier()

prediction = cnn.predict_animal(file_name)
print('Prediction: '+ prediction)

