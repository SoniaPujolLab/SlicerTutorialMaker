import ctk
import qt

import slicer

from slicer.ScriptedLoadableModule import *
from Lib.TutorialUtils import Util

# Slicer4Minute

class Slicer4MinuteTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_Slicer4Minute1()

    def test_Slicer4Minute1(self):
        """ Tests parts of the Slicer4Minute tutorial.
        """
        
        layoutManager = slicer.app.layoutManager()
        mainWindow = slicer.util.mainWindow()  
        
        self.delayDisplay("Starting the test")
        # TUTORIALMAKER BEGIN

        # TUTORIALMAKER INFO TITLE FourMinuteTutorial
        # TUTORIALMAKER INFO AUTHOR Sonia Pujol, Ph.D.
        # TUTORIALMAKER INFO DATE 28/08/2024
        # TUTORIALMAKER INFO DESC This tutorial is a 4-minute introduction to the 3D visualization capabilities of the Slicer4 software for medical image analysis.
        
        # 1 shot: 
        mainWindow.moduleSelector().selectModule('Welcome')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #1: In the Welcome screen.')

        # 2 shot:
        import SampleData

        TESTING_DATA_URL = "https://github.com/Slicer/SlicerTestingData/releases/download/"

        try:
            SampleData.downloadFromURL(
                fileNames='slicer4minute.mrb',
                loadFiles=True,
                uris=TESTING_DATA_URL + 'SHA256/5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8',
                checksums='SHA256:5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8')
            self.delayDisplay('Finished with download and loading')
        except:
            pass

        mainWindow.moduleSelector().selectModule('Models')
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #2: In the Models screen with the sample data loaded.')

        # 3 shot:
        redControl = Util.getNamedWidget("CentralWidget/CentralWidgetLayoutFrame/QSplitter:0/QWidget:0/qMRMLSliceWidgetRed/SliceController/qMRMLSliceControllerWidget").inner()
        greenControl = Util.getNamedWidget("CentralWidget/CentralWidgetLayoutFrame/QSplitter:0/QWidget:0/qMRMLSliceWidgetGreen/SliceController/qMRMLSliceControllerWidget").inner()
        yellowControl = Util.getNamedWidget("CentralWidget/CentralWidgetLayoutFrame/QSplitter:0/QWidget:0/qMRMLSliceWidgetYellow/SliceController/qMRMLSliceControllerWidget").inner()
        red = slicer.util.getNode(pattern="vtkMRMLSliceNode1")
        red.SetSliceVisible(1)
        redControl.show()
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #3: With the red view panel opened.')
        redControl.hide()
        
        # 4 shot:
        red.SetSliceOffset(-57)
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #4: With the red view slided to -57.')

        # 5 shot
        skin = slicer.util.getNode(pattern='Skin')
        skin.GetDisplayNode().SetOpacity(0.5)
        nodeList = Util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/ModelsModuleWidget/ResizableFrame/SubjectHierarchyTreeView").inner()
        nodeList.setCurrentNode(skin)
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #5: With the skin node selected and opacity lowered to 0,5.')

        # 6 shot
        skin.GetDisplayNode().SetOpacity(0)
        cam = slicer.util.getNode(pattern='vtkMRMLCameraNode1')
        cam.GetCamera().Azimuth(60)
        cam.GetCamera().Elevation(30)
        cam.GetCamera().Zoom(1.3)
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #6: Change the visibility of skin to 0 and rotate de camera to show the top of the head.')

        # 7 shot
        green = slicer.util.getNode(pattern="vtkMRMLSliceNode3")
        green.SetSliceVisible(1)
        greenControl.show()
        yellowControl.show()
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #7: Set the visibility of the green view, showing the two view panel.')
        greenControl.hide()
        yellowControl.hide()

        # 8 shot
        skull = slicer.util.getNode(pattern='skull_bone')
        skull.GetDisplayNode().SetVisibility(0)
        nodeList.setCurrentNode(skull)
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #8: Change the visibility of skull_bone, also click in the skull_bone in the node list.')

        # 9 shot
        hemispheric_white_matter = slicer.util.getNode(pattern='hemispheric_white_matter')
        nodeList.setCurrentNode(hemispheric_white_matter)
        slicer.util.findChildren(name="ClippingButton")[0].click()
        hemispheric_white_matter.GetDisplayNode().SetClipping(1)
        clip = slicer.util.getNode('ClipModelsParameters1')
        if int(slicer.app.revision) >= 33142: # Clipping API has changed around Slicer 5.7.0-2024-12-06
            nodeID = "vtkMRMLSliceNodeGreen"
            clip.AddAndObserveClippingNodeID(nodeID)
            nodeIndex = clip.GetClippingNodeIndex(nodeID)
            clip.SetNthClippingNodeState(nodeIndex, 2)
        else:
            clip.SetRedSliceClipState(0)
            clip.SetYellowSliceClipState(0)
            clip.SetGreenSliceClipState(2)
        scrolBar = Util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea").inner()
        scrolBar.verticalScrollBar().setValue(scrolBar.height)
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #9: Select hemispheric_white_matter, click in the clipping and change the clip state of the node.')

        # 10 shot
        cam.GetCamera().Elevation(10)
        green.SetSliceOffset(-10)
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #10: Rotate the camera to see the optical nerve.')
        
        # 11 shot
        scrolBar.verticalScrollBar().setValue(0)
        skin.GetDisplayNode().SetOpacity(0.5)
        nodeList.setCurrentNode(skin)
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #11: Change the layout to 3D View only.')

        # 12 shot
        cam.GetCamera().Azimuth(-90)
        cam.GetCamera().Elevation(0)
        Util.getNamedWidget("CentralWidget/CentralWidgetLayoutFrame/ThreeDWidget1/qMRMLThreeDViewControllerWidget:0/qMRMLThreeDViewControllerWidget").inner().show()
        slicer.util.findChildren(name="SpinButton")[0].click()
        threeDWidget = slicer.app.layoutManager().threeDWidget(0)
        controller = threeDWidget.controllerWidget()
        controller.setAnimationMode(0) 
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #11: Active the 3D view spin button.')
        #util.getNamedWidget("CentralWidget/CentralWidgetLayoutFrame/ThreeDWidget1/qMRMLThreeDViewControllerWidget:0/qMRMLThreeDViewControllerWidget").inner().hide()

        self.delayDisplay('Optic chiasm should be visible. Front part of white matter should be clipped.')
        
        # Done
        # TUTORIALMAKER END
        self.delayDisplay('Test passed!')
