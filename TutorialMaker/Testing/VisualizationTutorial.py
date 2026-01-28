import os
import zipfile
import SampleData
import urllib.request
import time
import slicer
from slicer.ScriptedLoadableModule import *
from DICOMLib import DICOMUtils

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

        layoutManager = slicer.app.layoutManager()
        mainWindow = slicer.util.mainWindow()

        self.delayDisplay("Starting the test")
        # TUTORIALMAKER BEGIN

        try:
            dataProbe = slicer.util.findChild(mainWindow, 'DataProbeCollapsibleWidget')
            if dataProbe and not dataProbe.collapsed:
                dataProbe.collapsed = True
        except Exception:
            pass

        # TUTORIALMAKER INFO TITLE Slicer Visualization Tutorial
        # TUTORIALMAKER INFO AUTHOR Sonia Pujol, Ph.D.
        # TUTORIALMAKER INFO DATE 24/11/2024
        # TUTORIALMAKER INFO DESC This tutorial guides users through 3D Slicer’s advanced visualization features, including DICOM data import, volume rendering, slice manipulation, and model clipping techniques.

        # 1 shot: Welcome Screen
        mainWindow.moduleSelector().selectModule("Welcome")
        layoutManager.setLayout(
            slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView
        )
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #1: In the Welcome screen.")

        # 2 shot: Download and Select DICOM module
        
        # Download and Data Setup
        zip_url = "https://www.dropbox.com/s/03emcqnlec4t2s5/3DVisualizationDataset.zip?dl=1"
        extraction_subfolder = "3DVisualizationDataset/dataset1_Thorax_Abdomen"
        zip_path = os.path.join(slicer.app.temporaryPath, "3DVisualizationDataset.zip")
        extract_path_check = os.path.join(slicer.app.temporaryPath, "3DVisualizationDataset")

        def download_progress(count, block_size, total_size):
            slicer.app.processEvents()

        if not os.path.exists(zip_path):
            self.delayDisplay("Downloading dataset... (may take a while)")
            urllib.request.urlretrieve(zip_url, zip_path, reporthook=download_progress)
            self.delayDisplay("Download complete.")

        if not os.path.exists(extract_path_check):
            self.delayDisplay("Extracting dataset...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(slicer.app.temporaryPath)
            self.delayDisplay("Extraction complete.")

        # Setup DICOM Database
        mainWindow.moduleSelector().selectModule("DICOM")
        slicer.app.processEvents()

        if not slicer.dicomDatabase:
            dicomDatabasePath = os.path.join(slicer.app.temporaryPath, "DICOMDatabase")
            if not os.path.exists(dicomDatabasePath):
                os.makedirs(dicomDatabasePath)
            dicomWidget = slicer.modules.dicom.widgetRepresentation()
            if hasattr(dicomWidget, "onDatabaseDirectoryChanged"):
                dicomWidget.onDatabaseDirectoryChanged(dicomDatabasePath)

        dicom_data_path = os.path.join(slicer.app.temporaryPath, extraction_subfolder)
        
        self.delayDisplay("Importing DICOM data... (may take a while)") 
        DICOMUtils.importDicom(dicom_data_path)
        slicer.app.processEvents()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #2: Loaded the sample dataset.")

        # 3 shot: Load DICOM Data
        try:
            patient_uids = slicer.dicomDatabase.patients()
            if len(patient_uids) > 0:
                DICOMUtils.loadPatientByUID(patient_uids[0])
            else:
                logging.warning("No patients found in DICOM database to load.")
        except Exception as e:
            import logging
            logging.error(f"Failed to load patient via DICOMUtils: {e}")
            
        max_wait_time = 30
        start_time = time.time()
        ct_node = None
        
        while ct_node is None and (time.time() - start_time) < max_wait_time:
            slicer.app.processEvents()
            time.sleep(0.5)
            try:
                ct_node = slicer.util.getNode("6: CT_Thorax_Abdomen")
            except:
                volumeNodes = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')
                for node in volumeNodes:
                    if 'CT_Thorax_Abdomen' in node.GetName():
                        ct_node = node
                        break
        
        if ct_node is None:
            print("Warning: CT_Thorax_Abdomen node not found within timeout.")

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #3: DICOM data loaded into the scene.")

        # 4 shot: Volumes Module & Preset
        mainWindow.moduleSelector().selectModule("Volumes")
        
        volumes_widget = slicer.modules.volumes.widgetRepresentation()
        ct_preset_button = slicer.util.findChild(volumes_widget, "CT_ABDOMEN")
        if ct_preset_button:
            ct_preset_button.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #4: Applied 'CT Abdomen' display preset.")

        # 5 shot: Slice Controller Interaction
        
        def get_slice_controller(color):
            return layoutManager.sliceWidget(color).sliceController()

        red_controller = get_slice_controller("Red")
        
        pin_button = slicer.util.findChild(red_controller, "PinButton")
        if pin_button: pin_button.click()
        
        link_button = slicer.util.findChild(red_controller, "SliceLinkButton")
        if link_button: link_button.click()
        
        vis_button = slicer.util.findChild(red_controller, "SliceVisibilityButton")
        if vis_button: vis_button.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #5: Linked and activated red slice plane.")

        # 6 shot: Widescreen Layout
        layoutManager.setLayout(
            slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView
        )

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #6: Set widescreen layout.")

        # 7 shot: Camera Zoom
        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        if cam:
            cam.GetCamera().Zoom(0.4)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #7: Zoomed in on the region of interest.")

        # 8 shot: Camera Rotation
        if cam:
            cam.GetCamera().Azimuth(60)
            cam.GetCamera().Elevation(30)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #8: Rotated view (60° azimuth, 30° elevation).")

        # 9 shot: Center 3D View
        threeD_widget = layoutManager.threeDWidget(0)
        threeD_controller = threeD_widget.threeDController()
        center_button = slicer.util.findChild(threeD_controller, "CenterButton")
        if center_button:
            center_button.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #9: Centered the 3D view.")

        # 10 shot: Volume Rendering
        mainWindow.moduleSelector().selectModule("VolumeRendering")

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #10: Switched to 'Volume Rendering' module.")

        # 1 shot: Enable Vol Ren
        volumeNode = ct_node # Use robustly found node
        if not volumeNode:
            collection = slicer.mrmlScene.GetNodesByName("6: CT_Thorax_Abdomen")
            if collection.GetNumberOfItems() > 0:
                volumeNode = collection.GetItemAsObject(0)

        if volumeNode:
            volRenLogic = slicer.modules.volumerendering.logic()
            displayNode = volRenLogic.CreateDefaultVolumeRenderingNodes(volumeNode)
            volumePropertyNode = displayNode.GetVolumePropertyNode()
            preset = volRenLogic.GetPresetByName("CT-Cardiac3")
            if preset:
                volumePropertyNode.Copy(preset)
            displayNode.SetVisibility(1)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #1: Volume rendering enabled with 'CT-Cardiac3'.")

        # 2 shot: Adjust Volume Rendering Properties
        threeDView = threeD_widget.threeDView()
        threeDView.resetFocalPoint()

        volRenWidget = slicer.modules.volumerendering.widgetRepresentation()
        
        volumePropertyNodeWidget = slicer.util.findChild(volRenWidget, "VolumePropertyNodeWidget")
        if volumePropertyNodeWidget and volumePropertyNode:
            volumePropertyNodeWidget.setMRMLVolumePropertyNode(volumePropertyNode)
            volumePropertyNodeWidget.moveAllPoints(250, 0, False)

        if cam:
            cam.GetCamera().Elevation(-30)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #2:  Change shift value.")

        # 3 shot: Enable ROI
        roi_checkbox = slicer.util.findChild(volRenWidget, "ROICropDisplayCheckBox")
        if roi_checkbox:
            roi_checkbox.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #3: ROI cropping enabled.")

        # 4 shot: Adjust ROI 1
        if displayNode:
            displayNode.SetVisibility(0)

        roiNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLMarkupsROINode")
        if roiNode is None:
            roiNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsROINode")

        roiNode.SetXYZ(-66, 144, -225)
        roiNode.SetRadiusXYZ(30, 50, 60)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #4: ROI position and size adjusted (first configuration).")

        # 5 shot: Display ROI
        if displayNode:
            displayNode.SetVisibility(1)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #5: Displaying ROI.")

        # 6 shot: Adjust ROI 2
        roiNode.SetXYZ(0, 144, -225)
        roiNode.SetRadiusXYZ(100, 50, 60)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #6: ROI position and size adjusted (second configuration).")

        # Cleanup for Part 3
        slicer.mrmlScene.Clear(0)

        # 1 shot: Welcome
        mainWindow.moduleSelector().selectModule("Welcome")
        layoutManager.setLayout(
            slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView
        )
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #1: In the Welcome screen.")

        # 2 shot: Download Slicer4Minute Data
        TESTING_DATA_URL = "https://github.com/Slicer/SlicerTestingData/releases/download/"
        try:
            SampleData.downloadFromURL(
                fileNames="slicer4minute.mrb",
                loadFiles=True,
                uris=TESTING_DATA_URL + "SHA256/5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8",
                checksums="SHA256:5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8",
            )
        except Exception:
            pass

        mainWindow.moduleSelector().selectModule("Models")
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #2: In the Models screen with the sample data loaded.")

        # 3 shot: Adjust Slice Options
        red_slice_node = slicer.util.getNode("vtkMRMLSliceNodeRed")
        red_widget = layoutManager.sliceWidget("Red")
        
        red_controller = red_widget.sliceController() if red_widget else None
        
        if red_controller:
            pin_red = slicer.util.findChild(red_controller, "PinButton")
            if pin_red: pin_red.click()
            
            vis_red = slicer.util.findChild(red_controller, "SliceVisibilityButton")
            if vis_red: vis_red.click()
        
        if red_slice_node:
            red_slice_node.SetSliceOffset(-32)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #3: Red slice plane adjusted to position -32 and its visibility toggled on.")

        # 4 shot: Skin Opacity & Camera
        skin = slicer.util.getNode(pattern="Skin")
        if skin:
            skin.GetDisplayNode().SetOpacity(0.5)

        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        if cam:
            cam.GetCamera().Azimuth(45)
            cam.GetCamera().Elevation(30)
            cam.GetCamera().Zoom(1.4)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #4: Adjusted the opacity of the skin model to 50% and updated the camera view (45° azimuth, 30° elevation, 1.4x zoom).")

        # 5 shot: Skull Visibility
        skull_bone = slicer.util.getNode(pattern="skull_bone")
        if skull_bone:
            skull_bone.GetDisplayNode().SetVisibility(False)

        # TUTORIALMAKER SCREENSHOT
        # 6 shot: Green Slice
        green_widget = layoutManager.sliceWidget("Green")
        green_controller = green_widget.sliceController() if green_widget else None
        
        if green_controller:
            pin_green = slicer.util.findChild(green_controller, "PinButton")
            if pin_green: pin_green.click()
            
            vis_green = slicer.util.findChild(green_controller, "SliceVisibilityButton")
            if vis_green: vis_green.click()

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #6: Green slice plane visibility toggled on.")

        # 7 shot: Clipping
        models_widget = slicer.modules.models.widgetRepresentation()
        sh_tree = slicer.util.findChild(models_widget, "SubjectHierarchyTreeView")
        
        hemispheric_white_matter = slicer.util.getNode(pattern='hemispheric_white_matter')
        if sh_tree and hemispheric_white_matter:
            sh_tree.setCurrentNode(hemispheric_white_matter)

        if hemispheric_white_matter:
            hemispheric_white_matter.GetDisplayNode().SetClipping(True)
        
        clip = slicer.util.getNode('ClipModelsParameters1')
        
        # Select ClipModelsParameters1 in combobox
        clip_combo = slicer.util.findChild(models_widget, "ClipModelsNodeComboBox")
        if clip_combo and clip:
            clip_combo.setCurrentNode(clip)
            
        # Refresh clip node workaround (from original code)
        pos_radio = slicer.util.findChild(models_widget, "PositiveRadioButton")
        if pos_radio:
            pos_radio.click()

        if int(slicer.app.revision) >= 33142: 
            nodeID = "vtkMRMLSliceNodeGreen"
            if clip:
                clip.AddAndObserveClippingNodeID(nodeID)
                nodeIndex = clip.GetClippingNodeIndex(nodeID)
                clip.SetNthClippingNodeState(nodeIndex, 2)
        else:
            if clip:
                clip.SetRedSliceClipState(0)
                clip.SetYellowSliceClipState(0)
                clip.SetGreenSliceClipState(2)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #7: Enabled clipping for the hemispheric white matter model.")

        # 8 shot: Green Slice adjust
        green_slice_node = slicer.util.getNode("vtkMRMLSliceNodeGreen")
        if green_slice_node:
            green_slice_node.SetSliceOffset(-32)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #8: Adjusted the position of the green slice plane.")

        # 9 shot: Final Camera
        if cam:
            cam.GetCamera().Elevation(40)
            cam.GetCamera().Zoom(0.8)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay("Screenshot #9: Final visualization.")

        # Done
        # TUTORIALMAKER END
        self.delayDisplay("Test passed!")