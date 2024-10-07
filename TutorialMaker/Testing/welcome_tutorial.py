import slicer
import SampleData

import Lib.utils as utils

from slicer.ScriptedLoadableModule import *

# SlicerWelcome


class SlicerWelcomeTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Do whatever is needed to reset the state - typically a scene clear will be enough."""
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_SlicerWelcome1()

    def test_SlicerWelcome1(self):
        """Tests parts of the SlicerWelcome tutorial."""
        # General Useful Constants and Variables
        COLORS = ["Red", "Green", "Yellow"]
        TESTING_DATA_URL = (
            "https://github.com/Slicer/SlicerTestingData/releases/download/"
        )
        CENTRAL_WIDGETS_PATH = "CentralWidget/CentralWidgetLayoutFrame/QSplitter:0/QWidget:0/qMRMLSliceWidget"
        SCROLL_AREA_PATH = "PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents"
        WELCOME_BUTTONS_PATH = f"{SCROLL_AREA_PATH}/WelcomeModuleWidget"
        SAMPLE_DATA_PATH = (
            f"{SCROLL_AREA_PATH}/SampleDataModuleWidget/GeneralCollapsibleGroupBox"
        )

        self.Tutorial = utils.Tutorial(
            "Slicer4 Minute", "Sonia Pujol, Ph.D.", "28/08/2024", "description"
        )

        util = utils.util()
        layoutManager = slicer.app.layoutManager()
        mainWindow = slicer.util.mainWindow()

        # Clear Output folder
        self.Tutorial.clearTutorial()
        self.Tutorial.beginTutorial()
        self.delayDisplay("Starting the test")

        # 1 shot:
        mainWindow.moduleSelector().selectModule("Welcome")
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)
        self.Tutorial.nextScreenshot()
        self.delayDisplay("Screenshot #1: In the Welcome screen.")

        # 2 shot:

        about_button = util.getNamedWidget(
            f"{WELCOME_BUTTONS_PATH}/WelcomeAndAboutCollapsibleWidget"
        ).inner()
        about_button.click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            'Screenshot #2: In the Welcome screen after pressing the "About" button.'
        )

        # 3 shot:
        try:
            SampleData.downloadFromURL(
                fileNames="slicer4minute.mrb",
                loadFiles=True,
                uris=TESTING_DATA_URL
                + "SHA256/5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8",
                checksums="SHA256:5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8",
            )
            self.delayDisplay("Finished with download and loading")
        except:
            pass

        about_button.click()

        skin = slicer.util.getNode(pattern="Skin")
        skin.GetDisplayNode().SetOpacity(0.5)

        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        cam.GetCamera().Azimuth(45)
        cam.GetCamera().Elevation(30)
        cam.GetCamera().Zoom(1.4)

        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            "Screenshot #3: In the Welcome screen with downloaded example."
        )

        # 4 shot:
        documentation_and_tutorials_button = util.getNamedWidget(
            f"{WELCOME_BUTTONS_PATH}/OtherUsefulHintsCollapsibleWidget"
        ).inner()
        documentation_and_tutorials_button.click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            'Screenshot #4: In the Welcome screen after pressing the "Documentation & Tutorials" button.'
        )

        # 5 shot:
        slicer.mrmlScene.Clear(0)
        slicer.app.layoutManager().setLayout(
            slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView
        )

        download_button = util.getNamedWidget(
            f"{WELCOME_BUTTONS_PATH}/ButtonsFrame/LoadSampleDataButton"
        ).inner()
        download_button.click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            'Screenshot #5: In the Sample Data screen after pressing the "Download Sample Data" button.'
        )

        # 6 shot:
        mrh_head_button = util.getNamedWidget(
            f"{SAMPLE_DATA_PATH}/MRHeadPushButton"
        ).inner()
        mrh_head_button.click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            'Screenshot #6: MRHead sample data loading after pressing the "MRHead" button.'
        )

        # 7 shot:
        pin_buttons = {
            color: util.getNamedWidget(
                f"{CENTRAL_WIDGETS_PATH}{color}/SliceController/BarWidget/PinButton"
            )
            for color in COLORS
        }

        more_buttons = {
            color: util.getNamedWidget(
                f"{CENTRAL_WIDGETS_PATH}{color}/SliceController/qMRMLSliceControllerWidget/MoreButton"
            )
            for color in COLORS
        }

        pin_buttons["Red"].click()
        more_buttons["Red"].click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            "Screenshot #7: Red slice view with the pin and more options opened."
        )

        # 8 shot:
        visibility_buttons = {
            color: util.getNamedWidget(
                f"{CENTRAL_WIDGETS_PATH}{color}/SliceController/qMRMLSliceControllerWidget/SliceFrame/SliceVisibilityButton"
            )
            for color in COLORS
        }

        visibility_buttons["Red"].click()
        pin_buttons["Red"].click()

        more_buttons["Green"].click()
        visibility_buttons["Green"].click()

        more_buttons["Yellow"].click()
        visibility_buttons["Yellow"].click()

        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        cam.GetCamera().Azimuth(30)
        cam.GetCamera().Elevation(30)
        cam.GetCamera().Zoom(1.4)

        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            "Screenshot #8: Adjusting red, green, and yellow slice visibility with more options expanded."
        )

        # 9 shot:
        mainWindow.moduleSelector().selectModule("Welcome")
        self.Tutorial.nextScreenshot()
        self.delayDisplay(
            "Screenshot #9: Returning to the Welcome screen with the final view."
        )

        self.Tutorial.endTutorial()

        # Done
        self.delayDisplay("Test passed!")
