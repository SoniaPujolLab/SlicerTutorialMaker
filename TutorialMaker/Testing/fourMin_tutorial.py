import ctk
import qt

import slicer

from slicer.ScriptedLoadableModule import *
import Lib.utils as utils

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

        Currently testing 'Part 2' which covers volumes, models, visibility and clipping.
        """
        self.Tutorial = utils.Tutorial( "Slicer4 Minute",
            "Sonia Pujol, Ph.D.",
            "28/08/2024",
            "description")

        #Clear Output folder
        self.Tutorial.clearTutorial()

        self.Tutorial.beginTutorial()
        self.delayDisplay("Starting the test")
        layoutManager = slicer.app.layoutManager()
        # 1 shot: 
        m = slicer.util.mainWindow()
        m.moduleSelector().selectModule('Welcome')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)
        self.Tutorial.nextScreenshot()

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

        m.moduleSelector().selectModule('Models')
        self.Tutorial.nextScreenshot()

        # 3 shot:
        slicer.util.findChildren(name="PinButton")[3].click()
        red = slicer.util.getNode(pattern="vtkMRMLSliceNode1")
        red.SetSliceVisible(1)

        self.Tutorial.nextScreenshot()
        slicer.util.findChildren(name="PinButton")[3].click()
        
        # 4 shot:
        red.SetSliceOffset(-57)
        self.Tutorial.nextScreenshot()

        # 5 shot
        skin = slicer.util.getNode(pattern='Skin')
        skin.GetDisplayNode().SetOpacity(0.5)
        self.Tutorial.nextScreenshot()

        # 6 shot
        skin.GetDisplayNode().SetOpacity(0)
        cam = slicer.util.getNode(pattern='vtkMRMLCameraNode1')
        cam.GetCamera().Azimuth(60)
        cam.GetCamera().Elevation(30)
        cam.GetCamera().Zoom(1.3)
        self.Tutorial.nextScreenshot()

        # 7 shot
        green = slicer.util.getNode(pattern="vtkMRMLSliceNode3")
        green.SetSliceVisible(1)
        self.Tutorial.nextScreenshot()

        # 8 shot
        skull = slicer.util.getNode(pattern='skull_bone')
        skull.GetDisplayNode().SetVisibility(0)
        self.Tutorial.nextScreenshot()

        # 9 shot
        hemispheric_white_matter = slicer.util.getNode(pattern='hemispheric_white_matter')
        hemispheric_white_matter.GetDisplayNode().SetClipping(1)
        clip = slicer.util.getNode('ClipModelsParameters1')
        clip.SetRedSliceClipState(0)
        clip.SetYellowSliceClipState(0)
        clip.SetGreenSliceClipState(2)
        self.Tutorial.nextScreenshot()

        # 10 shot
        cam.GetCamera().Elevation(10)
        self.Tutorial.nextScreenshot()
        
        # 11 shot
        skin.GetDisplayNode().SetOpacity(0.5)
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
        self.Tutorial.nextScreenshot()

        # 12 shot
        cam.GetCamera().Azimuth(-90)
        cam.GetCamera().Elevation(0)
        self.Tutorial.nextScreenshot()


        self.Tutorial.endTutorial()
        self.delayDisplay('Optic chiasm should be visible. Front part of white matter should be clipped.')
        
        # Done
        self.delayDisplay('Test passed!')