# Slicer Tutorial Maker

The Slicer Tutorial Maker is an extension to 3D Slicer to streamline the creation of 3D Slicer tutorials in multiple languages. The sections below provide a user guide to the tool.

[Documentação em Português](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README_pt-br.md)
[Documentación en español](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README_esp.md)

## Installation (Using Extension Manager)
- Install [3D Slicer 5.10.0](https://download.slicer.org/) version or [latest stable available](https://download.slicer.org/)
- Go to the "Extension Manager" and search for "TutorialMaker."
![TutorialMakenAnnotation](https://github.com/user-attachments/assets/a6060e33-34bd-444c-a230-293c580962ca)
- Click to restart to get the extension loaded
![image](https://github.com/user-attachments/assets/5b035504-fcc3-42e5-9ae3-2d45615daea7)
- Proceed to [**How to use Tutorial Maker**](#how-to-use-tutorial-maker)

## Installation (Manually)
Follow these steps if you want to get the latest version of the extension before the preview build (which occurs in the morning ~9 EST).
### We strongly recomend to disable Developer Mode, as it uses features that are currently in development and can break during the use of the extension.

- Install the latest [3D Slicer Stable Release](https://download.slicer.org/) or [3D Slicer Preview Release](https://download.slicer.org/)
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
   3. Select 'Application settings.'
   4. A 'Parameters' window appears: select 'Modules' in the left panel
   5. Select the file 'TutoriaMaker.py.'
   6. Drag and drop the file `TutorialMaker.py` located in the sub-directory 'TutorialMaker-main/TutorialMaker/'into the field 'Additional module paths' and click on OK to restart Slicer
![TutorialMakerInstallMac](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/1aad7764-0eb6-4f2e-8a5e-ba46c3cf373d)


## How to use Tutorial Maker

- Select the 'Tutorial Maker' module from the 'Utilities' category in the list of modules in Slicer
![image](https://github.com/user-attachments/assets/61f70e02-fd7c-4f0b-b2ec-b190021eaf5d)
> [!IMPORTANT]
> Before starting this tutorial, switch Slicer to Full-Screen mode and set the font size to 14pt to ensure the screenshots are easy to read.
- Select `FourMinuteTutorial`
![image](https://github.com/user-attachments/assets/33bb0de0-24e6-4edc-b807-69f593443dce)

- Click `Capture screenshots`  and follow the instructions to close the scene and close the Python console
![image](https://github.com/user-attachments/assets/1eac96d9-150f-416c-ba40-18730ef02ccd)

- After capturing the tutorial, click `Edit annotations.`
![image](https://github.com/user-attachments/assets/e2d1f02c-e8d6-4620-ade8-cc8dd2d30e30)

## Annotation Tool

- The screenshots will appear on the left
![image](https://github.com/user-attachments/assets/dcabfa14-8454-4458-a32a-a2040d03ef10)

- Each screenshot includes a title section (green arrow) and a Comments section (red arrow)
![image](https://github.com/user-attachments/assets/de1a97a9-a5e4-4cbd-8c8b-208a9b9e0ebe)

- Select one of the four annotation tools
![image](https://github.com/user-attachments/assets/3b345eb6-5ac3-46c8-a87f-b2bd935173a9)

- After selecting a tool, specify the style
![image](https://github.com/user-attachments/assets/62acbbba-c118-40f9-9a34-97674c64d121)

- Then click on the element that will receive the annotation and start typing
![image](https://github.com/user-attachments/assets/32a7de11-6dc8-4bcc-a78c-5aacc1e83087)

- After creating all annotations, click on Save file
![image](https://github.com/user-attachments/assets/983da69f-78ae-4812-afa2-7d30eeec687f)

The Screenshots with Annotations are now saved in the Module folder under Outputs, inside the extension installation folder.

- Click `Generate output` to generate the MD and HTML files.
![image](https://github.com/user-attachments/assets/6422a4fa-bcac-4634-8c1c-c03b20d55aee)

- You will receive a message warning you about the generation
![image](https://github.com/user-attachments/assets/4f0dd1cc-6d5f-44c6-8d9b-5579145aaa04)

- The extension will open the folder containing the screenshots annotated, and also the HTML and MD
![image](https://github.com/user-attachments/assets/3e1b91bd-0d9f-42f6-8e47-e27ceeba72d4)

![image](https://github.com/user-attachments/assets/a7201cae-30b6-4ddd-8e4f-cd60079ba9a7)

You can also change the layout from the annotator, dragging the menus.
![dg](https://github.com/user-attachments/assets/b4269d5d-7c37-43f1-9e2e-f90d8aacb730)

It's possible to change the slide title and descriptions
![dg2](https://github.com/user-attachments/assets/a0264344-6c3d-403d-ae49-db8b30507623)

## Developer mode
- If you have enabled developer mode (Edit > Application Settings > Developer > Enable developer mode) in Slicer, you may notice additional options within the extension. These represent experimental features and unstable processes currently undergoing test
![image](https://github.com/user-attachments/assets/ce9478fa-e195-4cc8-b2ef-f90b3d4c9ed1)

- The Fetch From GitHub feature allows users to download tutorials directly from a curated list of external repositories. Currently, this feature is disabled to prevent issues regarding GitHub API rate limits.
- .Tutorial Creation Tools: These features assist in developing new tutorials by allowing you to record widget names and paths automatically.

## Writing tutorials
- For guidance on developing your own tutorials, please follow the template and examples hosted at the SlicerTutorialMakerCollection (https://github.com/SoniaPujolLab/SlicerTutorialMakerCollection).
