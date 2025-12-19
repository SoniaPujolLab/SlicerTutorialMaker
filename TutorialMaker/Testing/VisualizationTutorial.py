import os
import slicer
import zipfile
import SampleData
import urllib.request

from Lib.TutorialUtils import Util

from slicer.ScriptedLoadableModule import *

# VisualizationTutorial


class VisualizationTutorialTest(ScriptedLoadableModuleTest):
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
        self.test_VisualizationTutorial1()

    def test_VisualizationTutorial1(self):
        """Tests parts of the VisualizationTutorial tutorial."""

        self.util = Util()
        self.layoutManager = slicer.app.layoutManager()
        self.mainWindow = slicer.util.mainWindow()

        self.COLORS = ["Red", "Green", "Yellow"]
        self.CENTRAL_WIDGETS_PATH = "CentralWidget/CentralWidgetLayoutFrame/QSplitter:0/QWidget:0/qMRMLSliceWidget"

        self.delayDisplay("Starting the test")
        # TUTORIALMAKER BEGIN

        # TUTORIALMAKER INFO TITLE Slicer Visualization Tutorial
        # TUTORIALMAKER INFO AUTHOR Sonia Pujol, Ph.D.
        # TUTORIALMAKER INFO DATE 24/11/2024
        # TUTORIALMAKER INFO DESC This tutorial guides users through 3D Slicer’s advanced visualization features, including DICOM data import, volume rendering, slice manipulation, and model clipping techniques.


        # Run Visualization Tutorial - Part 1
        # 1 shot:
        self.mainWindow.moduleSelector().selectModule("Welcome")
        self.layoutManager.setLayout(
            slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView
        )
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #1: In the Welcome screen.")

        # 2 shot:
        print("Downloading zip file...")
        self.downloadAndLoadZip()
        self.mainWindow.moduleSelector().selectModule("DICOM")
        print("Zip file was downloaded.")

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #2: Loaded the sample dataset.")

        # 3 shot:
        scroll_area = self.util.getNamedWidget(
            "CentralWidget/CentralWidgetLayoutFrame/QWidget:0/SlicerDICOMBrowser/ctkDICOMBrowser/dicomTableManager/tableSplitter/patientsTable/tblDicomDatabaseView"
        ).getChildren()
        load_button = self.util.getNamedWidget(
            "CentralWidget/CentralWidgetLayoutFrame/QWidget:0/SlicerDICOMBrowser/ActionButtonsFrame/QPushButton:2"
        )

        self.util.getNamedWidget("CentralWidget/CentralWidgetLayoutFrame/QWidget:0/SlicerDICOMBrowser/ctkDICOMBrowser/dicomTableManager/tableSplitter/patientsTable/tblDicomDatabaseView").inner().selectRow(0)

        load_button.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #3: DICOM data loaded into the scene.")

        # 4 shot:
        self.mainWindow.moduleSelector().selectModule("Volumes")

        ct_button = self.util.getNamedWidget(
            "PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/qSlicerVolumesModuleWidget/DisplayCollapsibleButton/VolumeDisplayWidget/qSlicerScalarVolumeDisplayWidget/PresetsGroupBox/CT_ABDOMEN"
        )
        ct_button.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #4: Applied 'CT Abdomen' display preset.")

        # 5 shot:
        pin_buttons = {
            color: self.util.getNamedWidget(
                f"{self.CENTRAL_WIDGETS_PATH}{color}/SliceController/BarWidget/PinButton"
            )
            for color in self.COLORS
        }

        link_button = self.util.getNamedWidget(
            "CentralWidget/CentralWidgetLayoutFrame/QSplitter:0/QWidget:0/qMRMLSliceWidgetRed/SliceController/qMRMLSliceControllerWidget/SliceFrame/SliceLinkButton"
        )

        visibility_buttons = {
            color: self.util.getNamedWidget(
                f"{self.CENTRAL_WIDGETS_PATH}{color}/SliceController/qMRMLSliceControllerWidget/SliceFrame/SliceVisibilityButton"
            )
            for color in self.COLORS
        }

        pin_buttons["Red"].click()
        link_button.click()
        visibility_buttons["Red"].click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #5: Linked and activated red slice plane.")

        # 6 shot:
        self.layoutManager.setLayout(
            slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView
        )

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #6: Set widescreen layout.")

        # 7 shot:
        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        cam.GetCamera().Zoom(0.4)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #7: Zoomed in on the region of interest.")

        # 8 shot:
        cam.GetCamera().Azimuth(60)
        cam.GetCamera().Elevation(30)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #8: Rotated view (60° azimuth, 30° elevation).")

        # 9 shot:
        center_button = self.util.getNamedWidget(
            "CentralWidget/CentralWidgetLayoutFrame/QSplitter:0/ThreeDWidget1/qMRMLThreeDViewControllerWidget:0/qMRMLThreeDViewControllerWidget/CenterButton"
        )
        center_button.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #9: Centered the 3D view.")

        # 10 shot:
        self.mainWindow.moduleSelector().selectModule("VolumeRendering")

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #10: Switched to 'Volume Rendering' module.")

        # Run Visualization Tutorial - Part 2
        # 1 shot:
        volumeNode = slicer.util.getNode("6: CT_Thorax_Abdomen")

        volRenLogic = slicer.modules.volumerendering.logic()

        displayNode = volRenLogic.CreateDefaultVolumeRenderingNodes(volumeNode)

        volumePropertyNode = displayNode.GetVolumePropertyNode()

        preset = volRenLogic.GetPresetByName("CT-Cardiac3")

        volumePropertyNode.Copy(preset)

        displayNode.SetVisibility(1)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #1: Volume rendering enabled with 'CT-Cardiac3'.")

        # 2 shot:
        layoutManager = slicer.app.layoutManager()
        threeDWidget = layoutManager.threeDWidget(0)
        threeDView = threeDWidget.threeDView()
        threeDView.resetFocalPoint()

        volRenWidget = slicer.modules.volumerendering.widgetRepresentation()

        volumePropertyNodeWidget = slicer.util.findChild(
            volRenWidget, "VolumePropertyNodeWidget"
        )
        volumePropertyNodeWidget.setMRMLVolumePropertyNode(volumePropertyNode)
        volumePropertyNodeWidget.moveAllPoints(250, 0, False)

        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        cam.GetCamera().Elevation(-30)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #2:  Change shift value.")

        # 3 shot:
        roi_button = self.util.getNamedWidget(
            "PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/qSlicerVolumeRenderingModuleWidget/DisplayCollapsibleButton/ROICropDisplayCheckBox"
        )

        roi_button.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #3: ROI cropping enabled.")

        # 4 shot:
        displayNode.SetVisibility(0)

        roiNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLMarkupsROINode")

        # If ROI node is None, create a new one
        if roiNode is None:
            roiNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsROINode")

        roiNode.SetXYZ(-66, 144, -225)

        roiNode.SetRadiusXYZ(30, 50, 60)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #4: ROI position and size adjusted (first configuration)."
        )

        # 5 shot:
        displayNode.SetVisibility(1)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #5: Displaying ROI.")

        # 6 shot:
        roiNode.SetXYZ(0, 144, -225)

        roiNode.SetRadiusXYZ(100, 50, 60)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #6: ROI position and size adjusted (second configuration)."
        )

        slicer.mrmlScene.Clear(0)

        # Run Visualization Tutorial - Part 3
        # 1 shot:
        self.mainWindow.moduleSelector().selectModule("Welcome")
        self.layoutManager.setLayout(
            slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView
        )
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #1: In the Welcome screen.")

        # 2 shot:
        TESTING_DATA_URL = (
            "https://github.com/Slicer/SlicerTestingData/releases/download/"
        )

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

        self.mainWindow.moduleSelector().selectModule("Models")
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #2: In the Models screen with the sample data loaded."
        )

        # 3 shot:
        self.pin_buttons = {
            color: self.util.getNamedWidget(
                f"{self.CENTRAL_WIDGETS_PATH}{color}/SliceController/BarWidget/PinButton"
            )
            for color in self.COLORS
        }

        self.visibility_buttons = {
            color: self.util.getNamedWidget(
                f"{self.CENTRAL_WIDGETS_PATH}{color}/SliceController/qMRMLSliceControllerWidget/SliceFrame/SliceVisibilityButton"
            )
            for color in self.COLORS
        }

        red_slice_position = -32
        self.red_slice_node = slicer.util.getNode("vtkMRMLSliceNodeRed")

        self.pin_buttons["Red"].click()
        self.visibility_buttons["Red"].click()
        self.red_slice_node.SetSliceOffset(red_slice_position)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #3: Red slice plane adjusted to position -32 and its visibility toggled on."
        )

        # 4 shot:
        skin = slicer.util.getNode(pattern="Skin")
        skin.GetDisplayNode().SetOpacity(0.5)

        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        cam.GetCamera().Azimuth(45)
        cam.GetCamera().Elevation(30)
        cam.GetCamera().Zoom(1.4)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #4: Adjusted the opacity of the skin model to 50% and updated the camera view (45° azimuth, 30° elevation, 1.4x zoom)."
        )

        # 5 shot:
        skull_bone = slicer.util.getNode(pattern="skull_bone")
        skull_bone.GetDisplayNode().SetVisibility(False)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #5: Skull bone model visibility turned off to isolate other structures."
        )

        # 6 shot:
        self.pin_buttons["Green"].click()
        self.visibility_buttons["Green"].click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #6: Green slice plane visibility toggled on and its position adjusted."
        )

        # 7 shot:
        #Select the hemispheric white matter in the node list
        nodeList = self.util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/ModelsModuleWidget/ResizableFrame/SubjectHierarchyTreeView").inner()
        hemispheric_white_matter = slicer.util.getNode(pattern='hemispheric_white_matter')
        nodeList.setCurrentNode(hemispheric_white_matter)

        #Set Clipping
        hemispheric_white_matter_display_node = hemispheric_white_matter.GetDisplayNode()
        hemispheric_white_matter_display_node.SetClipping(True)
        
        clip = slicer.util.getNode('ClipModelsParameters1')
        #We have to select the ClipModelsParameters1 in the combobox
        self.util.getNamedWidget(
            "PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/ModelsModuleWidget/ClippingButton/ClipModelsNodeComboBox"
        ).inner().setCurrentNode(clip)
        #We also have to select any of the unselected options on the clipping node nodes, this will force a refresh that will remove some bugged state from the clipping node
        #This workaround shouldn't be necessary but for now it works
        self.util.getNamedWidget(
            "PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/ModelsModuleWidget/ClippingButton/MRMLClipNodeWidget/ClipNodeFrame/QWidget:0/PositiveRadioButton"
        ).inner().click()

        if int(slicer.app.revision) >= 33142: # Clipping API has changed around Slicer 5.7.0-2024-12-06
            nodeID = "vtkMRMLSliceNodeGreen"
            clip.AddAndObserveClippingNodeID(nodeID)
            nodeIndex = clip.GetClippingNodeIndex(nodeID)
            clip.SetNthClippingNodeState(nodeIndex, 2)
        else:
            clip.SetRedSliceClipState(0)
            clip.SetYellowSliceClipState(0)
            clip.SetGreenSliceClipState(2)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #7: Enabled clipping for the hemispheric white matter model using red and green slice planes."
        )

        # 8 shot:
        green_slice_position = -32
        self.green_slice_node = slicer.util.getNode("vtkMRMLSliceNodeGreen")
        self.green_slice_node.SetSliceOffset(green_slice_position)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #8: Adjusted the position of the green slice plane to -32 for further analysis."
        )

        # 9 shot:
        cam.GetCamera().Elevation(40)
        cam.GetCamera().Zoom(0.8)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay(
            "Screenshot #9: Final visualization with adjusted camera elevation (40°) and zoom level (0.8x)."
        )

        # Done
        # TUTORIALMAKER END
        self.delayDisplay("Test passed!")


    def downloadAndLoadZip(self):
        zip_url = (
            "https://www.dropbox.com/s/03emcqnlec4t2s5/3DVisualizationDataset.zip?dl=1"
        )
        
        extraction_subfolder = "3DVisualizationDataset/dataset1_Thorax_Abdomen"
        zip_path = f"{slicer.app.temporaryPath}/3DVisualizationDataset.zip"

        urllib.request.urlretrieve(zip_url, zip_path)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(slicer.app.temporaryPath)

        os.makedirs(slicer.dicomDatabase.databaseDirectory, exist_ok=True)

        slicer.util.selectModule("DICOM")
        from DICOMLib import DICOMUtils
        DICOMUtils.importDicom(f"{slicer.app.temporaryPath}/{extraction_subfolder}")