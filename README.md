## Tutorial Maker Prototype

This is an extension for 3D Slicer that contain tools for creating tutorials that can be automatically translated to multiple languages.

### Installation

- Install the latest [3D Slicer Stable Release](https://download.slicer.org/) (currently 3D Slicer-5.6.2) or [3D Slicer Preview Release version 5.7 or higher](https://download.slicer.org/) 
- Open the [Tutorial Maker repository on GitHub](https://github.com/SlicerLatinAmerica/TutorialMaker)
- Clone the green button Code' and select the option 'Download ZIP' as displayed in the image below to download the file 'TutorialMaker.zip' on your computer
- Unzip the 'TutorialMaker.zip' archive to access the 'TutorialMaker-main' directory
- **Windows users** :
  1. Start 3D Slicer
  2. Drag and drop the `TutorialMaker` folder to the Slicer application window
  3. A first pop-up window, 'Select a reader,' appears. Select 'Add Python scripted modules to the application' and click OK.
  4. A second pop-up window appears to load the Tutorial Maker module. Click on 'Yes'.
![TutorialMakerInstall](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/17ffda20-ee58-4e52-91c8-755655725d83)

- **MacOs users**:
   1. Start 3D Slicer
   2. Select 'Edit' in the main menu
   3. Select 'Application settings'
   4. A 'Parameters' window appears: select 'Modules' in the left panel
   5. Select the file 'TutoriaMaker.py' 
   6. Drag and drop the file `TutorialMaker.py` located in the sub-directory 'TutorialMaker-main/TutorialMaker/'into the field 'Additional module paths' and click on OK to restart Slicer
![TutorialMakerInstallMac](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/1aad7764-0eb6-4f2e-8a5e-ba46c3cf373d)


### How to use Tutorial Maker

- Select the 'Tutorial Maker' module from the 'Utilities' category in the list of modules in Slicer
![image](https://github.com/user-attachments/assets/881e77de-1778-445f-9d12-9ff7ed685a1c)
> [!IMPORTANT]
> Before starting this tutorial, switch Slicer to Full-Screen mode and set the font size to 14pt to ensure the screenshots are easy to read.
- Select `fourMin_tutorial`
![image](https://github.com/user-attachments/assets/1e15971b-eb7e-4a72-8ba4-d8f5a9aabdad)
- Click `Run and Annotate`
![image](https://github.com/user-attachments/assets/a9fed061-e0c1-474f-8678-d992efeeecc9)


### Annotation Tool

- The screenshots will appear on the left
![image](https://github.com/user-attachments/assets/bea6fe9f-6a0e-41ca-ae0f-7cde252b46d7)
- Each screenshot includes a title section (green arrow) and a Comments section (red arrow)
![image](https://github.com/user-attachments/assets/3023d6cd-3fcb-41a1-9a51-8f4b66d5e7f2)
- Select one of the three annotation tools
![image](https://github.com/user-attachments/assets/61e8f816-1c7c-4b7c-813c-257338de0c6d)
- After selecting a tool, specify the style and the text of the annotation
![image](https://github.com/user-attachments/assets/0dfcace2-cacb-4c09-8f5e-d01bbadbc82f)
- Then click on the element that will receive the annotation
![TutorialMakenAnnotation](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/49ef485f-c880-4a96-b4b5-75304752e5dc)

> [!WARNING]
> For people who have epilepsy, the screen will blink for each screenshot.

- After creating all annotations, click on the save file
![image](https://github.com/user-attachments/assets/1bdd56ad-2817-4981-a6a3-1e8fac2f728d)
<!--
> [!WARNING]
> For people who have epilepsy, don't run the translation. The screen will blink for each screenshot.

- And then click on the "Test Translation" button
![image](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/dae305bc-3fd1-4a7a-87b4-6e724037e728)
-->
The Screenshots with Annotations are now saved in the Module folder under Outputs;

![image](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/3a5feeb0-b7a3-41c8-923f-77239f5331c8)

### Writing tutorials
TODO: Create the "developer manual" to create new tutorials.
