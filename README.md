# TrailPi
ECS 193 Senior Design Project for a DIY Web Cameras Network

## Image recognition using a 5-layer CNN (Convolutional Neural Network)

### Requirements

To install packages that will work with the CNN model type into the termial:

     `pip install -r requirements.txt` 

### **Running the Script**
The script used to run:

    $ python test.py

 The scrip will load in the model and then will ask the user if they want to apply the model on a folder or a single image :

    $ Folder(F) or Single File(S)?: _

### **Choosing Folder(F)**
1. If user selects folder, then the script will check locally if `animals_and_humans` and `nothing` folders already exists, if they don't then it will create them. Then the user is asked to enter the folder name (local to the script) of the images they want to classify:

    $ Folder Name: folder_name_here

2. Hit `Return` and the script will begin sorting the images into their respective folders (`animals_and_humans` or `nothing`).
3. Once complete, the propt will ask if the user woulfd like to continue and sort other files or folders with the following prompt:

        $ Continue (Y/N): _

4. If user selects `'N'` then the script will terminate, and if the user selects `'Y'` then the script will repeat the steps above asking if the user wants a folder or single file.

### **Choosing Single File(S)**
1. If the user selects single file, then the script will prompt the user to give the name of the image (must be local to the script) as such:

        $ ImageName: my_image.jpg 

2. The script will then print out if the image contains an animal/human or if there is nothing in the image.
3. Once complete, the propt will ask if the user woulfd like to continue and sort other files or folders with the following prompt:

        $ Continue (Y/N): _ 
4. If user selects `'N'` then the script will terminate, and if the user selects `'Y'` then the script will repeat the steps above asking if the user wants a folder or single file.


## **Retraining the Image Classifier**

1. Ensure that the **requirements** are installed before running the model.
2. Ensure that the script `cnn.py` has  `animals`, `nothing` and `people` folder local to it. The reason the `animals` and `people` folder are kept seperate is in case the user may want to modify the classes to determine if its a person or animal instead. 
3. In  a terminal window run:

     $ pyhton cnn.py
4. The script is now creating a new model with the provided images.
5. A `labels.npy` and `trail_pics.pny` file will be created, these are the numpy representation of the images, very useful if later the user decides to use the same images, the user would uncomment the following lines in the `cnn.py` file:

        trail_pics = np.load("trail_pics.npy")
        labels = np.load("labels.npy")
6. Once the neural network is done with it's training and validation, two files will  be created locally named `model.h5` (containing the weights for the model) and `model.json` (containing the actual model).
7. Replace the `model.h5` and `model.json` that are local to the `test.py` and `classifier.py` folder with the new ones generated.
8. The new model will now be used by the `test.py` to make predictions on new images. 