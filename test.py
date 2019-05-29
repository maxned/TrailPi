import sys
import os
from PIL import Image
from classifier import Classifier


cnn = Classifier(json_file = 'model.json', weights_file = 'model.h5')
exit_program = False
while(exit_program == False):
    type_input = input("Folder(F) or Single File (S)?: ")
    if type_input == "F" or type_input == "f":
        os.mkdir('animals_and_humans')
        os.mkdir('nothing')
        folder_name = input("Folder Name: ")
        test_images = os.listdir(folder_name)
        for image in test_images:
            print(image)
            path_image = "./" + folder_name + "/" + image
            if(cnn.predict_animal(path_image)):
                os.rename(path_image, "./animals_and_humans/" + image)
            else:
                os.rename(path_image, "./nothing/" + image)
        answer = input("Continue (Y/N): ")
        if answer == "N" or answer == "n":
            exit_program = True
    else:
        file_name = input("ImageName: ")
        prediction = cnn.predict_animal(file_name)
        print('Prediction: '+ prediction)
        answer = input("Continue (Y/N): ")
        if answer == "N" or answer == "n":
            exit_program = True

