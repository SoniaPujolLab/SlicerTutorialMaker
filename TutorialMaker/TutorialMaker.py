import logging
import os
 
import vtk
import slicer
import Lib.utils as utils
from Lib.utils import *
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# TutorialMaker
#

class TutorialMaker(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Tutorial Maker"  # TODO: make this more human readable by adding spaces
        self.parent.categories = ["TUTORIAL"]  # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["Douglas Gonçalves (USP)", "Enrique Hernández (UAEM)", "João Januário (USP)", "Lucas Silva (USP)", "Victor Montaño (UAEM)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """help text"""
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
Development of this module was funded by <a href="https://chanzuckerberg.com/eoss/proposals/3d-slicer-for-latin-america-localization-and-outreach/">CZI EOSS grant</a>.
"""

        # Additional initialization step after application startup is complete
        #slicer.app.connect("startupCompleted()", registerSampleData)

#
# TutorialMakerWidget
#

class TutorialMakerWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._updatingGUIFromParameterNode = False
        self.widgetFinder = WidgetFinder(slicer.util.mainWindow())
        self.widgetPainter = Shapes(slicer.util.mainWindow())
        self.__tableSize = 0

        #PROTOTYPE FOR PLAYBACK

        self.actionList = []
        
    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/TutorialMaker.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        self.__tableInitiliaze()

        #setStyle of widget info table
        self.ui.widgetName.setStyleSheet("border: 1px solid black;")
        self.ui.widgetText.setStyleSheet("border: 1px solid black;")
        self.ui.widgetToolTip.setStyleSheet("border: 1px solid black;")
        self.ui.widgetClassName.setStyleSheet("border: 1px solid black;")
        self.ui.widgetID.setStyleSheet("border: 1px solid black;")

        self.ui.widgetName.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.ui.widgetText.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.ui.widgetToolTip.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.ui.widgetClassName.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.ui.widgetID.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = TutorialMakerLogic()

        # Connections
        self.widgetFinder.sinalManager.connect(self.updateStatus)

        # will only draw the circle at playback for now
        #self.widgetFinder.sinalManager.connect(self.widgetPainter.setTargetWidget)

        # Buttons

        #Main
        self.ui.pushButtonRecordMain.connect('clicked(bool)', self.logic.startRecorder)
        self.ui.pushButtonEditMain.connect('clicked(bool)', self.logic.startEditor)
        self.ui.pushButtonConvertMain.connect('clicked(bool)', self.logic.startConverter)

        #Experimental
        self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)
        self.ui.pushButtonRecord.connect('clicked(bool)', self.onRecordButton)
        self.ui.pushButtonStop.connect('clicked(bool)', self.onStopButton)

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self):
        """
        Called when the application closes and the module widget is destroyed.
        """
        return

    def enter(self):
        """
        Called each time the user opens this module.
        """
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self):
        """
        Called each time the user opens a different module.
        """
        # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
        #self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
        print('goodbye, world!')
    
    def initializeParameterNode(self):
        """
        Ensure parameter node exists and observed.
        """
        return

    def setParameterNode(self, inputParameterNode):
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """
        return
        
    def updateGUIFromParameterNode(self, caller=None, event=None):
        """
        This method is called whenever parameter node is changed.
        The module GUI is updated to show the current state of the parameter node.
        """
        return
    
    def onApplyButton(self):
        self.widgetFinder.showFullSize()

    def onRecordButton(self):
        print("Record")

        self.widgetFinder.showFullSize()
        #self.widgetFinder.raise_()
        return

    def onStopButton(self):
        import time
        self.widgetPainter.showFullSize()
        self.widgetPainter.raise_()
        for widget in self.actionList:
            self.widgetPainter.setTargetWidget(widget.inner())
            time.sleep(0.1)
            self.widgetPainter.repaint()
            time.sleep(4)

            print(widget.inner())
            #Só da pra usar este se for um qMRML
            #slicer.util.clickAndDrag(widget.inner(), steps=0)
            

        print("Stop")
        self.widgetPainter.hideOverlay()
        return

    def getCurrentWidget(self):
        widget = self.widgetFinder.currentWidgetSelect
        if widget == '':
            self.ui.AlertText.setText('Click in "Apply" and select a widget!')
            return
        
        self.ui.AlertText.setText('Copy! (Its not true)')
    
    def updateStatus(self, w):
        widget = Widget(w)
        widgetData = widget.__dict__()
        
        self.addItemOnTable(widgetData['name'], widgetData['className'], 'Circle')
        self.actionList.append(widget)

        self.ui.widgetName.setText(widgetData['name'])
        self.ui.widgetText.setText(widgetData['text'])
        self.ui.widgetToolTip.setText(widgetData['toolTip'])
        self.ui.widgetClassName.setText(widgetData['className'])
        self.ui.widgetID.setText(widgetData['id'])


    #table func
    def __tableInitiliaze(self):
        table = self.ui.tableWidget
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Name', 'Widget', 'Shape'])

    def addItemOnTable(self, name:str='', code:str='', shape:str=''):
        item_name = qt.QTableWidgetItem(name)
        item_code = qt.QTableWidgetItem(code)
        item_shape = qt.QTableWidgetItem(shape)
        
        table = self.ui.tableWidget
        table.setRowCount(self.__tableSize+1)
        table.setItem(self.__tableSize, 0, item_name)
        table.setItem(self.__tableSize, 1, item_code)
        table.setItem(self.__tableSize, 2, item_shape)

        self.__tableSize += 1

    def delItemOnTable(self):
        print(self.__tableSize)
        if self.__tableSize == 0:
            return
        
        self.__tableSize -= 1
        table = self.ui.tableWidget
        table.setRowCount(self.__tableSize)



#
# TutorialMakerLogic
#

class TutorialMakerLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self):
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)

    def setDefaultParameters(self, parameterNode):
        """
        Initialize parameter node with default settings.
        """
        print("World!")
        

    #And all of this will be converted to be python modules so we can load them properly
    def startRecorder(self):
        #These dependencies will be removed shortly
        import pip
        pip.main(['install', 'pyautogui', 'PyQt5'])
        path = os.path.dirname(os.path.abspath(__file__)) + "\Lib\standalone\metadata_gui.py"
        path = path.replace("\\", "/").encode("ascii")
        exec(open(path).read())
        #pip.main(['uninstall', 'pyautogui', 'PyQt5'])


    def startEditor(self):
        import pip
        pip.main(['install', 'pyautogui', 'PyQt5', 'imutils', 'opencv-python'])
        path = os.path.dirname(os.path.abspath(__file__)) + "\Lib\standalone\Editor\gui_test.py"
        path = path.replace("\\", "/").encode("ascii")
        exec(open(path).read())
        #pip.main(['uninstall', 'pyautogui', 'PyQt5', 'imutils', 'opencv-python'])

    def startConverter(self):
        print(self)

#
# TutorialMakerTest
#

class TutorialMakerTest(ScriptedLoadableModuleTest):
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
        self.test_TutorialMaker1()

    def test_TutorialMaker1(self):
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
        self.delayDisplay('Test passed')
