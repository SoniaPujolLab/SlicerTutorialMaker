import qt
import slicer
import os

import Lib.utils as utils

#
# Tutorial Editor
#

class TutorialEditor():

    def __init__(self):
        self.window = qt.QMainWindow()
        self.mainWidget = qt.QWidget()
        self.layout = qt.QVBoxLayout()
        self.logic = TutorialEditorLogic(self)
        self.window.setWindowTitle("Tutorial Editor")  # Make translatable # needs TR directives maybe?

        uiWidget = slicer.util.loadUI(self.resourcePath('UI/TutorialEditor.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        self.mainWidget.setLayout(self.layout)
        self.window.setCentralWidget(self.mainWidget)


        self.Setup()

        pass

    def Setup(self):
        self.ui.pushButtonStartStopRecord.clicked.connect(self.logic.StopStartRecording)

        pass

    def Show(self):
        self.window.show()

    def Annotate(self):
        pass


    def TableItemSelected(self):
        pass
    
    def TableAddItem(self, widget):

        pass
    
    def exit(self):
        self.logic.StopRecording()
        self.window.close()

    # There should be a better way to expose the resource path to the underlying classes of a module but I couldn't think of a clean way.
    def resourcePath(self, filename):
        """Return the absolute path of the module ``Resources`` directory."""
        scriptedModulesPath = os.path.dirname(slicer.util.modulePath("TutorialMaker"))
        return os.path.join(scriptedModulesPath, "Resources", filename)

    pass

class TutorialEditorLogic():
    def __init__(self, gui=None):
        self.stateManager = StateManager()
        self.widgetFinder = utils.WidgetFinder(slicer.util.mainWindow())
        self.widgetFinder.sinalManager.connect(self.NextWidget)
        self.isRecording = False
        self.gui = gui
        pass

    def StopStartRecording(self):
        if not self.isRecording:
            self.StartRecording()
        else:
            self.StopRecording()
        self.isRecording = not self.isRecording
        pass

    def StartRecording(self):
        self.gui.window.showMinimized()
        self.gui.ui.pushButtonStartStopRecord.text = "Stop Recording" # needs TR directives
        self.widgetFinder.showFullSize()
        pass

    def StopRecording(self):
        self.gui.ui.pushButtonStartStopRecord.text = "Start Recording" # needs TR directives
        self.widgetFinder.hideOverlay()
        pass


    def NextWidget(self, widget):
        print(widget)
        if self.isRecording:
            self.SaveState(widget)
            self.widgetFinder.showFullSize()
            self.gui.TableAddItem(widget)
        pass

    def SaveState(self, widget):
        _state = SlicerState(widget)

        self.stateManager.InsertState(_state)
        pass



class StateManager():
    def __init__(self):
        self.states = []
        pass

    def InsertState(self, state):
        self.states.append(state)
        pass


    def deleteState(self, index):
        self.states.pop(index)
        pass

    def annotateState(self, index):
        #
        pass


class SlicerState():
    def __init__(self, nextWidget):
        self.nextWidget = nextWidget

        self.annotations = []
        pass
    
