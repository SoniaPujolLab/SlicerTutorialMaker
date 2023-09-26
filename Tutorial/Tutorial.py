import logging
import os
from typing import Annotated, Optional

import vtk

import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLScalarVolumeNode

import json
import qt



#
# Tutorial
#

################### EHL TESTING 
metadata = {} # JSON METADATA FILE

# Get widget at clicked position
class MetaFinder(qt.QWidget):
   def __init__(self, parent=None):
    print("M1")
    super(TextFinder, self).__init__(parent)
    self.setAttribute(qt.Qt.WA_StyledBackground)
    self.setStyleSheet("QWidget { background-color: rgba(255, 0, 0, 50) }")

   def __del__(self):
    print("M2")
    self.showPointCursor(True)
<<<<<<< HEAD
   

=======
<<<<<<< HEAD:Tutorial/Tutorial/Tutorial.py
   

=======
>>>>>>> victor:Tutorial/Tutorial.py
>>>>>>> enrique

class TextFinder(qt.QWidget):
  

  def __init__(self, parent=None):
    print("T1")
    super(TextFinder, self).__init__(parent)
    self.setAttribute(qt.Qt.WA_StyledBackground)
    self.setStyleSheet("QWidget { background-color: rgba(0, 255, 0, 50) }")
    self.focusPolicy = qt.Qt.StrongFocus
    self.LanguageToolsLogic = None
    self.shortcutKeySequence = qt.QKeySequence("Ctrl+6")
    self.shortcut = None
    self.logic = None
    self.cursorOverridden = True
 

  def __del__(self):
    print("T2")
    self.showPointCursor(True)

  def enableShortcut(self, enable):
    print("T3")
    enable = True
    if (self.shortcut is not None) == enable:
      return
    if self.shortcut:
      self.shortcut.disconnect("activated()")
      self.shortcut.setParent(None)
      self.shortcut.deleteLater()
      self.shortcut = None
      self.hideOverlay()
    else:
      self.shortcut = qt.QShortcut(self.parent())
      self.shortcut.setKey(self.shortcutKeySequence)
      self.shortcut.connect( "activated()", self.showFullSize)

  def showPointCursor(self, enable):
    print("T4")
    enable = True
    if enable == self.cursorOverridden:
      return
    if enable:
      slicer.app.setOverrideCursor(qt.Qt.PointingHandCursor)
    else:
      slicer.app.restoreOverrideCursor()
    self.cursorOverridden = enable

  def showFullSize(self):
    print("T5")
    self.pos = qt.QPoint()
    self.setFixedSize(self.parent().size)
    self.show()
    self.setFocus(qt.Qt.ActiveWindowFocusReason)
    self.showPointCursor(True)

  def overlayOnWidget(self, widget):
    print("T6")
    pos = widget.mapToGlobal(qt.QPoint())
    pos = self.parent().mapFromGlobal(pos)
    self.pos = pos
    self.setFixedSize(widget.size)

  def hideOverlay(self):
    print("T7")
    self.hide()
    self.showPointCursor(True)

  def widgetAtPos(self, pos):
    print("T8")
    self.setAttribute(qt.Qt.WA_TransparentForMouseEvents)
    widget = qt.QApplication.widgetAt(pos)
    self.setAttribute(qt.Qt.WA_TransparentForMouseEvents, False)
    print("Test1:", widget)
    return widget

  def keyPressEvent(self, event):
    print("T9")
    self.hideOverlay()

  def mousePressEvent(self, event):
    # Get widget at mouse position
    print("T10")
    pos = qt.QCursor().pos()
    widget = self.widgetAtPos(pos)
    slicer.TextFinderLastWidget = widget  # useful for debugging
    print("Test1:", widget.objectName)
    #logging.info("Widget found: "+widget.objectName)
    self.overlayOnWidget(widget)
    self.showPointCursor(False)
    print("Tfin")
    # # Extract text

################## EHL TESTTING END

class Tutorial(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Tutorial"  # TODO: make this more human readable by adding spaces
        self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#Tutorial">module documentation</a>.
"""
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#

def registerSampleData():
    """
    Add data sets to Sample Data module.
    """
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData
    iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # Tutorial1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='Tutorial',
        sampleName='Tutorial1',
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, 'Tutorial1.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames='Tutorial1.nrrd',
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums='SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
        # This node name will be used when the data set is loaded
        nodeNames='Tutorial1'
    )

    # Tutorial2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='Tutorial',
        sampleName='Tutorial2',
        thumbnailFileName=os.path.join(iconsPath, 'Tutorial2.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames='Tutorial2.nrrd',
        checksums='SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
        # This node name will be used when the data set is loaded
        nodeNames='Tutorial2'
    )


#
# TutorialParameterNode
#

@parameterNodeWrapper
class TutorialParameterNode:
    """
    The parameters needed by module.

    inputVolume - The volume to threshold.
    imageThreshold - The value at which to threshold the input volume.
    invertThreshold - If true, will invert the threshold.
    thresholdedVolume - The output volume that will contain the thresholded volume.
    invertedVolume - The output volume that will contain the inverted thresholded volume.
    """
    inputVolume: vtkMRMLScalarVolumeNode
    imageThreshold: Annotated[float, WithinRange(-100, 500)] = 100
    invertThreshold: bool = False
    thresholdedVolume: vtkMRMLScalarVolumeNode
    invertedVolume: vtkMRMLScalarVolumeNode


#
# TutorialWidget
#

class TutorialWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None
        self.textFinder = TextFinder(slicer.util.mainWindow())


    def setup(self) -> None:
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)
        print('1')
        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/Tutorial.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)
        print('2')
        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)
        print('3')
        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = TutorialLogic()
        print('4')
        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.StartButton.connect('clicked(bool)', self.TutorialButton)

        # Make sure parameter node is initialized (needed for module reload)
        #self.initializeParameterNode()

    def cleanup(self) -> None:
        """
        Called when the application closes and the module widget is destroyed.
        """
        self.removeObservers()

    def enter(self) -> None:
        """
        Called each time the user opens this module.
        """
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self) -> None:
        """
        Called each time the user opens a different module.
        """
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)

    def onSceneStartClose(self, caller, event) -> None:
        """
        Called just before the scene is closed.
        """
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """
        Called just after the scene is closed.
        """
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self) -> None:
        """
        Ensure parameter node exists and observed.
        """
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

        # Select default input nodes if nothing is selected yet to save a few clicks for the user
        if not self._parameterNode.inputVolume:
            firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            if firstVolumeNode:
                self._parameterNode.inputVolume = firstVolumeNode

    def setParameterNode(self, inputParameterNode: Optional[TutorialParameterNode]) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
        self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
            self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
            self._checkCanApply()

    def _checkCanApply(self, caller=None, event=None) -> None:
        if self._parameterNode and self._parameterNode.inputVolume and self._parameterNode.thresholdedVolume:
            self.ui.applyButton.toolTip = "Compute output volume"
            self.ui.applyButton.enabled = True
        else:
            self.ui.applyButton.toolTip = "Select input and output volume nodes"
            self.ui.applyButton.enabled = False

    def TutorialButton(self) -> None:
        metadata["title"] = self.ui.lineEdit_Tutorialname.text
        metadata["authors"]  = self.ui.lineEdit_Authorname.text
        metadata["description"]  = self.ui.lineEdit_Description.text
        print(metadata)
        #self.record_instructions()

###############################################################
    # def enableTextFinder(self, enable):
    #     if enable:
    #         self.updateSettingsFromGUI()
    #         self.logic.preferredLanguage = self.ui.textFinderLanguageEdit.text
    #     self.textFinder.enableShortcut(enable)
    #     # Only allow changing language if finder is disabled
    #     self.ui.textFinderLanguageEdit.enabled = not enable
###############################################################

    def record_instructions(self)-> None:
        slicer.app.processEvents()
        self.widgetrecord()


    def widgetrecord(self)-> None:
        mainWindow = slicer.util.mainWindow()
        mainWindowPos_global = mainWindow.mapToGlobal(mainWindow.rect.topLeft())

        widgetsInfo = []
        widgets = slicer.util.findChildren()
        for widget in widgets:
            if hasattr(widget, "isVisible") and widget.isVisible() and hasattr(widget, "mapToGlobal"):
                widgetTopLeft_global = widget.mapToGlobal(widget.rect.topLeft())
                widgetBottomRight_global = widget.mapToGlobal(widget.rect.bottomRight())
                widgetPos_mainWindow = [widgetTopLeft_global.x() - mainWindowPos_global.x(), widgetTopLeft_global.y() - mainWindowPos_global.y()]
                widgetSize_mainWindow = [widgetBottomRight_global.x() - widgetTopLeft_global.x(), widgetBottomRight_global.y() - widgetTopLeft_global.y()]
                widgetInfo = {
                    #"widget": widgetPath(widget),
                    "className": widget.className(),
                    "position": widgetPos_mainWindow,
                    "size": widgetSize_mainWindow,
                    }
                if hasattr(widget, "windowTitle") and widget.windowTitle:
                    widgetInfo["windowWitle"] = widget.windowTitle
                if hasattr(widget, "text") and widget.text:
                    widgetInfo["text"] = widget.text
                widgetsInfo.append(widgetInfo)
                print(widgetsInfo)

    def widgetPath(widget):
        path = ""
        while widget:
            path = (widget.objectName if widget.objectName else "?") + ("/" + path if path else "")
            widget = widget.parent()
            print(path)
        return path


    

    
        
        

#
# TutorialLogic
#


class TutorialLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self) -> None:
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return TutorialParameterNode(super().getParameterNode())

    def process(self,
                inputVolume: vtkMRMLScalarVolumeNode,
                outputVolume: vtkMRMLScalarVolumeNode,
                imageThreshold: float,
                invert: bool = False,
                showResult: bool = True) -> None:
        """
        Run the processing algorithm.
        Can be used without GUI widget.
        :param inputVolume: volume to be thresholded
        :param outputVolume: thresholding result
        :param imageThreshold: values above/below this threshold will be set to 0
        :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
        :param showResult: show output volume in slice viewers
        """

        if not inputVolume or not outputVolume:
            raise ValueError("Input or output volume is invalid")

        import time
        startTime = time.time()
        logging.info('Processing started')

        # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
        cliParams = {
            'InputVolume': inputVolume.GetID(),
            'OutputVolume': outputVolume.GetID(),
            'ThresholdValue': imageThreshold,
            'ThresholdType': 'Above' if invert else 'Below'
        }
        cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
        # We don't need the CLI module node anymore, remove it to not clutter the scene with it
        slicer.mrmlScene.RemoveNode(cliNode)

        stopTime = time.time()
        logging.info(f'Processing completed in {stopTime-startTime:.2f} seconds')


#
# TutorialTest
#

class TutorialTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_Tutorial1()

    def test_Tutorial1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData
        registerSampleData()
        inputVolume = SampleData.downloadSample('Tutorial1')
        self.delayDisplay('Loaded test data set')

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = TutorialLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay('Test passed')