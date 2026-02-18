# Slicer Tutorial Maker

The Slicer Tutorial Maker is an extension for 3D Slicer that streamlines the creation of illustrated tutorials in multiple languages. It automates screenshot capture, provides a visual annotation editor, and exports finished tutorials to HTML and Markdown formats.

[Documentação em Português](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README_pt-br.md)
[Documentación en español](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README_esp.md)

---

## Table of Contents

1. [Installation: Extension Manager](#installation-extension-manager)
2. [Installation: Manual / Developer](#installation-manual--developer)
3. [How to Use Tutorial Maker](#how-to-use-tutorial-maker)
   - [1. Select a Tutorial](#1-select-a-tutorial)
   - [2. Capture Screenshots](#2-capture-screenshots)
   - [3. Annotate Your Tutorial](#3-annotate-your-tutorial)
   - [4. Generate Tutorial Output](#4-generate-tutorial-output)
4. [Annotation Tool](#annotation-tool)
   - [Keyboard Shortcuts](#keyboard-shortcuts)
5. [Developer Mode](#developer-mode)
6. [Writing Tutorials](#writing-tutorials)
7. [Uninstallation](#uninstallation)

---

## Installation: Extension Manager

1. Install [3D Slicer 5.10.0](https://download.slicer.org/) or the [latest stable release](https://download.slicer.org/).
2. Open the **Extension Manager** and search for `TutorialMaker`.
   <p align="center"><img src="https://github.com/user-attachments/assets/a6060e33-34bd-444c-a230-293c580962ca" alt="TutorialMakerAnnotation"></p>
3. Click **Install**, then restart Slicer when prompted.
   <p align="center"><img src="https://github.com/user-attachments/assets/5b035504-fcc3-42e5-9ae3-2d45615daea7" alt="Restart prompt"></p>
4. Continue to [**How to Use Tutorial Maker**](#how-to-use-tutorial-maker).

---

## Installation: Manual / Developer

Follow these steps to use the latest development version before it appears in the Extension Manager build (published every morning around 9 AM EST).

> [!WARNING]
> We strongly recommend keeping **Developer Mode disabled** unless you are actively developing the extension. Developer Mode exposes experimental features that may cause instability.

1. Install the [3D Slicer Stable Release](https://download.slicer.org/) or [Preview Release](https://download.slicer.org/).
2. Open the [TutorialMaker repository on GitHub](https://github.com/SlicerLatinAmerica/TutorialMaker).
3. Click the green **Code** button and select **Download ZIP** to download `TutorialMaker.zip`.
4. Extract the archive to obtain the `TutorialMaker-main` directory.

**Windows**

1. Start 3D Slicer.
2. Drag and drop the `TutorialMaker` folder onto the Slicer application window.
3. In the **Select a reader** dialog, choose **Add Python scripted modules to the application** and click **OK**.
4. When asked to load the Tutorial Maker module, click **Yes**.

<p align="center"><img src="https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/17ffda20-ee58-4e52-91c8-755655725d83" alt="TutorialMakerInstall"></p>

**macOS / Linux**

1. Start 3D Slicer.
2. Go to **Edit → Application Settings → Modules**.
3. In the **Additional module paths** field, drag and drop the file `TutorialMaker.py` found inside the `TutorialMaker-main/TutorialMaker/` directory.
4. Click **OK** and restart Slicer.

<p align="center"><img src="https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/1aad7764-0eb6-4f2e-8a5e-ba46c3cf373d" alt="TutorialMakerInstallMac"></p>

---

## How to Use Tutorial Maker

### 1. Select a Tutorial

Open the **Tutorial Maker** module from the **Utilities** category in the Slicer module selector.

<p align="center"><img src="https://github.com/user-attachments/assets/61f70e02-fd7c-4f0b-b2ec-b190021eaf5d" alt="Module selector"></p>

> [!IMPORTANT]
> Before starting this tutorial, switch Slicer to Full-Screen mode and set the font size to 14pt to ensure the screenshots are easy to read.
- Select `FourMinuteTutorial`
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/33bb0de0-24e6-4edc-b807-69f593443dce" />

- Click `Capture screenshots`  and follow the instructions to close the scene and close the Python console
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/1eac96d9-150f-416c-ba40-18730ef02ccd" />

- After capturing the tutorial, click `Edit annotations.`
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/e2d1f02c-e8d6-4620-ade8-cc8dd2d30e30" />

## Annotation Tool

- The screenshots will appear on the left
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/dcabfa14-8454-4458-a32a-a2040d03ef10" />

- Each screenshot includes a title section (green arrow) and a Comments section (red arrow)
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/de1a97a9-a5e4-4cbd-8c8b-208a9b9e0ebe" />

- Select one of the four annotation tools
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/3b345eb6-5ac3-46c8-a87f-b2bd935173a9" />

- After selecting a tool, specify the style
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/62acbbba-c118-40f9-9a34-97674c64d121" />

- Then click on the element that will receive the annotation and start typing
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/32a7de11-6dc8-4bcc-a78c-5aacc1e83087" />

- After creating all annotations, click on Save file
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/983da69f-78ae-4812-afa2-7d30eeec687f" />

The Screenshots with Annotations are now saved in the Module folder under Outputs, inside the extension installation folder.

- Click `Generate output` to generate the MD and HTML files.
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/6422a4fa-bcac-4634-8c1c-c03b20d55aee" />

- You will receive a message warning you about the generation
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/4f0dd1cc-6d5f-44c6-8d9b-5579145aaa04" />

- The extension will open the folder containing the screenshots annotated, and also the HTML and MD
<img width="1706" height="1029" alt="image" src="https://github.com/user-attachments/assets/3e1b91bd-0d9f-42f6-8e47-e27ceeba72d4" />

<img width="1254" height="774" alt="image" src="https://github.com/user-attachments/assets/a7201cae-30b6-4ddd-8e4f-cd60079ba9a7" />

You can also change the layout from the annotator, dragging the menus.
![dg](https://github.com/user-attachments/assets/b4269d5d-7c37-43f1-9e2e-f90d8aacb730)

It's possible to change the slide title and descriptions
![dg2](https://github.com/user-attachments/assets/a0264344-6c3d-403d-ae49-db8b30507623)

## Developer mode
- If you have enabled developer mode (Edit > Application Settings > Developer > Enable developer mode) in Slicer, you may notice additional options within the extension. These represent experimental features and unstable processes currently undergoing test
<img width="598" height="1007" alt="image" src="https://github.com/user-attachments/assets/ce9478fa-e195-4cc8-b2ef-f90b3d4c9ed1" />

- The Fetch From GitHub feature allows users to download tutorials directly from a curated list of external repositories. Currently, this feature is disabled to prevent issues regarding GitHub API rate limits.
- .Tutorial Creation Tools: These features assist in developing new tutorials by allowing you to record widget names and paths automatically.

## Writing tutorials
- For guidance on developing your own tutorials, please follow the template and examples hosted at the SlicerTestRepository (https://github.com/SoniaPujolLab/SlicerTestTutorial).
