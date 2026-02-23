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
> Before capturing screenshots, switch Slicer to **Full-Screen** mode and set the application font size to **14 pt** to ensure the screenshots are easy to read.

Select the desired tutorial from the list, for example `FourMinuteTutorial`.

<p align="center"><img src="https://github.com/user-attachments/assets/33bb0de0-24e6-4edc-b807-69f593443dce" alt="Tutorial list"></p>

---

### 2. Capture Screenshots

Click **Capture Screenshots**. A preparation dialog will appear before the capture begins.

<p align="center"><img src="DOCS/README_18_02_2026/1.gif" alt="Capture Screenshots: preparation dialog"></p>

The **Screenshot Capture Environment Setup** dialog offers three options:

| Option | Default | Description |
|--------|---------|-------------|
| Save current scene data | Off | Opens the Save Data dialog so you can preserve your work before the scene is cleared. |
| Maximize 3D Slicer window for screen capture | On | Ensures consistent screenshot dimensions across all slides. |
| Close Python console and Error Log window | On | Hides developer panels for cleaner screenshots. |

> [!WARNING]
> The current scene will always be cleared before capture begins, regardless of the options chosen.

Click **OK** to proceed. A progress dialog will track each capture step and ask you not to interact with Slicer until the capture is complete.

<p align="center"><img src="DOCS/README_18_02_2026/2.gif" alt="Screenshot capture progress dialog"></p>

When the capture finishes, Slicer returns to the Tutorial Maker module and displays a confirmation:

> **Screenshot Capture Completed:** *Captured Tutorial: `<tutorial name>`*

---

### 3. Annotate Your Tutorial

After capturing screenshots, the panel shows two buttons side by side:

| Button | Behavior |
|--------|----------|
| **Edit Annotations** | Opens the Annotator with no annotations loaded. Use this button to start annotating from scratch or to discard all previous work. |
| **Resume Annotations** | Opens the Annotator **and automatically reloads** the most recently saved `annotations.json` file for the selected tutorial. Use this button to continue work from a previous session. |

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_1.png" alt="Edit Annotations and Resume Annotations buttons"></p>

<p align="center"><img src="DOCS/README_18_02_2026/3.gif" alt="Resume Annotations: annotator opening with saved annotations"></p>

> [!NOTE]
> **Edit Annotations** is enabled as soon as a tutorial is selected. **Resume Annotations** is only enabled when an `annotations.json` file already exists for the selected tutorial (i.e., you have saved at least once). When enabled, it restores all annotations (labels, positions, styles, slide titles and descriptions) exactly as you left them.

---

### 4. Generate Tutorial Output

After saving your annotations, click **Generate Tutorial** to produce the final HTML and Markdown files.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_2.png" alt="Generate Tutorial button"></p>

If no annotations file is found, you will see a warning:

> **No Annotations Found:** *You don't have any annotations to export. Please annotate your screenshots first using "Edit Annotations".*

When generation completes successfully, Slicer opens the output folder automatically and displays a confirmation:

> **Tutorial Generated:** *Generated Tutorial: `<tutorial name>`*

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_3.png" alt="Output folder opened in File Explorer"></p>

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_4.png" alt="Generated HTML output in browser"></p>

---

## Annotation Tool

The Annotator window opens as a separate modal window.

The thumbnail strip on the left displays all captured slides. Click any thumbnail to select it.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_5.png" alt="Annotator window: full layout overview"></p>

**Editing slide content**

On regular screenshot slides, you can edit the **Title** and **Description** fields at the top of the panel at any time during the annotation session.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_6_2.png" alt="Slide title and description fields"></p>

Special slides (such as the **Cover Slide**) do not have Title and Description fields. Instead, they contain pre-made annotations (author, date, description, etc.) that you can select and edit directly on the slide canvas.

<p align="center"><img src="DOCS/README_18_02_2026/6.gif" alt="Editing cover slide premade annotations"></p>

**Adding annotations**

1. Select an annotation tool from the toolbar (Rectangle, Arrow, Text, etc.).
   <p align="center"><img src="DOCS/README_18_02_2026/Screenshot_7.png" alt="Annotation toolbar"></p>
2. Choose the annotation style (color, font size, line thickness).
   <p align="center"><img src="DOCS/README_18_02_2026/Screenshot_8.png" alt="Annotation style options"></p>
3. Click on the slide area where you want to place the annotation and type the label.
   <p align="center"><img src="DOCS/README_18_02_2026/4.gif" alt="Placing a rectangle annotation"></p>

**Saving**

Click the **Save** button in the toolbar to save annotations to `Outputs/Annotations/<tutorial name>/annotations.json` inside the extension installation folder.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_9.png" alt="Save button in toolbar"></p>

> [!NOTE]
> When closing the Annotator, a dialog will ask whether you want to **Save**, **Discard**, or **Cancel** unsaved changes.

**Layout customization**

You can resize or rearrange panels by dragging the dividers.

<p align="center"><img src="DOCS/README_18_02_2026/5.gif" alt="Dragging panel dividers to rearrange layout"></p>

---

### Keyboard Shortcuts

The following keyboard shortcuts are available while the Annotator window is in focus:

| Key | Action |
|-----|--------|
| `Del` | Deletes the selected annotation. |
| `Esc` | Deselects the current annotation without deleting it. |
| `Shift` + click | Places an annotation and **keeps the same tool active**, allowing you to add multiple annotations in quick succession without reselecting the tool. |

<p align="center"><img src="DOCS/README_18_02_2026/7.gif" alt="Shift+click to place multiple annotations in succession"></p>

---

## Developer Mode

If **Developer Mode** is enabled in Slicer (**Edit → Application Settings → Developer → Enable developer mode**), additional options will appear in the Tutorial Maker panel.

<p align="center"><img src="DOCS/README_18_02_2026/Screenshot_10.png" alt="Developer Mode extra options"></p>

- **Fetch From GitHub:** Downloads tutorial scripts directly from a curated list of external repositories. Currently disabled by default to avoid issues with GitHub API rate limits.
- **Tutorial Creation Tools:** Assists in developing new tutorials by automatically recording widget names and paths.

> [!WARNING]
> Developer Mode features are experimental and may cause instability. We strongly recommend keeping Developer Mode disabled for routine tutorial creation.

---

## Writing Tutorials

For guidance on developing your own tutorial scripts, follow the templates and examples available at the [SlicerTutorialMakerCollection](https://github.com/SoniaPujolLab/SlicerTutorialMakerCollection).

---

## Uninstallation

### Via Extension Manager (recommended)

1. In 3D Slicer, open **View → Extension Manager** (or the **Extensions Manager** button in the toolbar).
2. Switch to the **Installed Extensions** tab.
3. Locate **TutorialMaker** in the list.
4. Click the **Uninstall** (trash / remove) button next to the extension.
5. Restart 3D Slicer when prompted to complete the removal.

<p align="center"><img src="DOCS/README_18_02_2026/8.gif" alt="Uninstalling via Extension Manager"></p>

### Manual removal (developer / source installation)

If you installed the extension by adding it to the **Additional module paths**, follow these steps:

1. Open **Edit → Application Settings → Modules**.
2. In the **Additional module paths** list, select the entry pointing to the `TutorialMaker` folder (or `TutorialMaker.py`).
3. Click the **Remove** (minus) button to delete the path entry.
4. Click **OK** and restart 3D Slicer.
5. After restarting, you can safely delete the `TutorialMaker-main` directory from your file system.

> [!NOTE]
> Removing the module path only unregisters the extension in Slicer. You must manually delete the source folder from disk to remove all files.

**Removing generated output files**

Tutorial output files (screenshots, annotations, HTML and Markdown) are stored inside the extension installation folder under `TutorialMaker/Outputs/`. These files are not removed automatically. Delete the `Outputs/` directory manually if you no longer need them.
