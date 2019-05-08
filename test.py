import sys
from PIL import Image
from classifier import Classifier

#file_name = sys.argv[1]
im = Image.open(file_name)

cnn = Classifier(json_file = 'UPDATED_model.json', weights_file = 'UPDATED_model.h5')
exit_program = False
while(exit_program == False):
    file_name = input("ImageName: ")
    prediction = cnn.predict_animal(file_name)
    print('Prediction: '+ prediction)
    answer = input("Continue (Y/N): ")
    if answer == "N" or answer == "n":
        exit_program = True

