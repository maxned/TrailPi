# TrailPi
ECS 193 Senior Design Project for a DIY Web Cameras Network

## Image recognotion using CNN (Convolutional Neural Netowork)

### Requirements

Use:
 `pip install -r requirements.txt` to install packages that will work with the CNN model

### Running the Script
The script used to run:

    $ python test.py

 The scrip will load in the model and the will ask the user if they want to apply the model on a folder or a single image :

    $ Folder(F) or Single File(S)?: _

### Choosing Folder(F)
1. If user selects folder, then the script will check locally if `animals_and_humans` and `nothing` folders already exists, if they don't then it will create them. Then the user is asked to enter the folder name (local to the script) of the images they want to classify:

    $ Folder Name: folder_name_here

2. Hit `Return` and the script will begin sorting the images into their respective folders (`animals_and_humans` or `nothing`).
3. Once complete, the propt will ask if the user woulfd like to continue and sort other files or folders with the following prompt:

        $ Continue (Y/N): _

4. If user selects `'N'` then the script will terminate, and if the user selects `'Y'` then the script will repeat the steps above asking if the user wants a folder or single file.

### Choosing Single File(S)
1. If the user selects single file, then the script will prompt the user to give the name of the image (must be local to the script) as such:

        $ ImageName: my_image.jpg 

2. The script will then print out if the image contains an animal/human or if there is nothing in the image.
3. Once complete, the propt will ask if the user woulfd like to continue and sort other files or folders with the following prompt:

        $ Continue (Y/N): _ 
4. If user selects `'N'` then the script will terminate, and if the user selects `'Y'` then the script will repeat the steps above asking if the user wants a folder or single file.
