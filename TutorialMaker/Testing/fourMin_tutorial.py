import slicer
import SampleData

import Lib.utils as utils

from slicer.ScriptedLoadableModule import *

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
        self.Tutorial = utils.Tutorial( "Slicer4 Minute",
            "Sonia Pujol, Ph.D.",
            "28/08/2024",
            "description")
        
        util = utils.util()
        layoutManager = slicer.app.layoutManager()
        mainWindow = slicer.util.mainWindow()
        
        #Clear Output folder
        self.Tutorial.clearTutorial()
        self.Tutorial.beginTutorial()
        self.delayDisplay("Starting the test")
        
        # 1 shot: 
        mainWindow.moduleSelector().selectModule('Welcome')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #1: In the Welcome screen.')

        # 2 shot:
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
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #2: In the Models screen with the sample data loaded.')

        # 3 shot:
        slicer.app.layoutManager().sliceWidget("vtkMRMLSliceNode1").sliceController().pinButton().toggle()
        red = slicer.util.getNode(pattern="vtkMRMLSliceNode1")
        red.SetSliceVisible(1)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #3: With the red view panel opened.')
        slicer.app.layoutManager().sliceWidget("vtkMRMLSliceNode1").sliceController().pinButton().click()
        slicer.app.processEvents()
        
        # 4 shot:
        red.SetSliceOffset(-57)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #4: With the red view slided to -57.')

        # 5 shot
        skin = slicer.util.getNode(pattern='Skin')
        skin.GetDisplayNode().SetOpacity(0.5)
        nodeList = util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/ModelsModuleWidget/ResizableFrame/SubjectHierarchyTreeView").inner()
        nodeList.setCurrentNode(skin)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #5: With the skin node selected and opacity lowered to 0,5.')

        # 6 shot
        skin.GetDisplayNode().SetOpacity(0)
        cam = slicer.util.getNode(pattern='vtkMRMLCameraNode1')
        cam.GetCamera().Azimuth(60)
        cam.GetCamera().Elevation(30)
        cam.GetCamera().Zoom(1.3)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #6: Change the visibility of skin to 0 and rotate de camera to show the top of the head.')

        # 7 shot
        green = slicer.util.getNode(pattern="vtkMRMLSliceNode3")
        green.SetSliceVisible(1)
        slicer.app.layoutManager().sliceWidget("vtkMRMLSliceNode1").sliceController().pinButton().click()
        slicer.app.layoutManager().sliceWidget("vtkMRMLSliceNode3").sliceController().pinButton().click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #7: Set the visibility of the green view, showing the two view panel.')
        slicer.app.layoutManager().sliceWidget("vtkMRMLSliceNode1").sliceController().pinButton().click()
        slicer.app.layoutManager().sliceWidget("vtkMRMLSliceNode3").sliceController().pinButton().click()
        slicer.app.processEvents()

        # 8 shot
        skull = slicer.util.getNode(pattern='skull_bone')
        skull.GetDisplayNode().SetVisibility(0)
        nodeList.setCurrentNode(skull)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #8: Change the visibility of skull_bone, also click in the skull_bone in the node list.')

        # 9 shot
        hemispheric_white_matter = slicer.util.getNode(pattern='hemispheric_white_matter')
        nodeList.setCurrentNode(hemispheric_white_matter)
        slicer.util.findChildren(name="ClippingButton")[0].click()
        hemispheric_white_matter.GetDisplayNode().SetClipping(1)
        clip = slicer.util.getNode('ClipModelsParameters1')
        clip.SetRedSliceClipState(0)
        clip.SetYellowSliceClipState(0)
        clip.SetGreenSliceClipState(2)
        scrolBar = util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea").inner()
        scrolBar.verticalScrollBar().setValue(scrolBar.height)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #9: Select hemispheric_white_matter, click in the clipping and change the clip state of the node.')

        # 10 shot
        cam.GetCamera().Elevation(10)
        green.SetSliceOffset(-10)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #10: Rotate the camera to see the optical nerve.')
        
        # 11 shot
        skin.GetDisplayNode().SetOpacity(0.5)
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #11: Change the layout to 3D View only.')

        # 12 shot
        cam.GetCamera().Azimuth(-90)
        cam.GetCamera().Elevation(0)
        slicer.util.findChildren(name="PinButton")[3].click()
        self.Tutorial.nextScreenshot()
        slicer.util.findChildren(name="SpinButton")[0].click()
        self.delayDisplay('Screenshot #11: Active the 3D view spin button.')


        self.Tutorial.endTutorial()
        self.delayDisplay('Optic chiasm should be visible. Front part of white matter should be clipped.')
        
        # Done
        self.delayDisplay('Test passed!')