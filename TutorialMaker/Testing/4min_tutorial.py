import ctk
import qt

import slicer

from Lib.ScriptedLoadableModule import *
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
        self.Tutorial = utils.Tutorial( "title",
            "author",
            "date",
            "description")

        #Clear Output folder
        self.Tutorial.clearTutorial()

        self.Tutorial.beginTutorial()
        self.delayDisplay("Starting the test")
        #logic = Slicer4MinuteLogic()
        
        # first, get some data

        import SampleData

        TESTING_DATA_URL = "https://github.com/Slicer/SlicerTestingData/releases/download/"

        SampleData.downloadFromURL(
            fileNames='slicer4minute.mrb',
            loadFiles=True,
            uris=TESTING_DATA_URL + 'SHA256/5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8',
            checksums='SHA256:5a1c78c3347f77970b1a29e718bfa10e5376214692d55a7320af94b9d8d592b8')
        self.delayDisplay('Finished with download and loading')

       
        self.Tutorial.nextScreenshot()
        # Testing "Part 2" of Tutorial
        #
        #
        self.delayDisplay('Testing Part 2 of the Tutorial')

        # check volume is loaded out of scene
        volumeNode = slicer.util.getNode(pattern="grayscale")
        #self.assertIsNotNone(logic.hasImageData(volumeNode))
        self.Tutorial.nextScreenshot()


        # check the slice planes
        red = slicer.util.getNode(pattern="vtkMRMLSliceNode1")
        red.SetSliceVisible(1)

        green = slicer.util.getNode(pattern="vtkMRMLSliceNode3")
        green.SetSliceVisible(1)    

        self.Tutorial.nextScreenshot()

        # rotate a bit
        cam = slicer.util.getNode(pattern='vtkMRMLCameraNode1')
        cam.GetCamera().Azimuth(90)
        cam.GetCamera().Elevation(20)

        self.Tutorial.nextScreenshot()

        # turn off skin and skull
        skin = slicer.util.getNode(pattern='Skin')
        skin.GetDisplayNode().SetVisibility(0)

        skull = slicer.util.getNode(pattern='skull_bone')
        skull.GetDisplayNode().SetVisibility(0)

        self.Tutorial.nextScreenshot()

        # clip the model hemispheric_white_matter.vtk
        m = slicer.util.mainWindow()
        m.moduleSelector().selectModule('Models')

        models = slicer.util.getModule('Models')
        #logic = models.logic()

        hemispheric_white_matter = slicer.util.getNode(pattern='hemispheric_white_matter')
        hemispheric_white_matter.GetDisplayNode().SetClipping(1)

        clip = slicer.util.getNode('ClipModelsParameters1')
        clip.SetRedSliceClipState(0)
        clip.SetYellowSliceClipState(0)
        clip.SetGreenSliceClipState(2)

        # Can we make this more than just a Smoke Test?
        self.delayDisplay('Optic chiasm should be visible. Front part of white matter should be clipped.')

        # Done
        #
        #
        self.delayDisplay('Test passed!')
