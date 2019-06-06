import sys
import os
from PIL import Image
from classifier.classifier import Classifier


cnn = Classifier(json_file = 'model.json', weights_file = 'model.h5')
exit_program = False
count_true = 0
count_false =0
while(exit_program == False):
    type_input = input("Folder(F) or Single File(S)?: ")
    if type_input == "F" or type_input == "f":
        if not os.path.exists('animals_and_humans'):
            os.mkdir('animals_and_humans')
        if not os.path.exists('nothing'):
            os.mkdir('nothing')
        folder_name = input("Folder Name: ")
        if os.path.exists(folder_name):
            test_images = os.listdir(folder_name)
            if len(test_images) > 0:
                for image in test_images:
                    print(image)
                    if image.startswith('.'):
                        print(image + " not read")
                    else:
                        path_image = "./" + folder_name + "/" + image
                        animal, accuracy = cnn.predict_animal(path_image)
                        if(animal):
                            os.rename(path_image, "./animals_and_humans/" + image)
                            count_true +=1
                        else:
                            os.rename(path_image, "./nothing/" + image)
                            count_false +=1
            else:
                print("Folder is Empty.")
        else:
            print("Folder does not exists.")
        print(f"True Motion Images Found: {count_true}")
        print(f"False Motion Images Found: {count_false}")
        answer = input("Continue (Y/N): ")
        if answer == "N" or answer == "n":
            exit_program = True
    else:
        file_name = input("ImageName: ")
        animal, accuracy = cnn.predict_animal(file_name)
        if(animal):
            print("Image contains animal or human in it with :{0:.2f} accuracy".format(accuracy))
        else:
            print("Image does NOT contain an animal or human in it with :{0:.2f} accuracy".format(accuracy))
        answer = input("Continue (Y/N): ")
        if answer == "N" or answer == "n":
            exit_program = True

