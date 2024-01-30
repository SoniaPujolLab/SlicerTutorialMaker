import slicer
import qt
import os

class util():

    def __init__(self) -> None:
        #self.listOnScreenWidgets()
        self.mw = Widget(slicer.util.mainWindow())
        pass
    
    __shortcutDict = {
        "Scene3D"     : "CentralWidget/CentralWidgetLayoutFrame/ThreeDWidget1",
        "SceneRed"    : "CentralWidget/CentralWidgetLayoutFrame/qMRMLSliceWidgetRed",
        "SceneYellow" : "CentralWidget/CentralWidgetLayoutFrame/qMRMLSliceWidgetYellow",
        "SceneGreen"  : "CentralWidget/CentralWidgetLayoutFrame/qMRMLSliceWidgetGreen",
        "Module"      : "PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents"
    }

    def listOnScreenWidgets(self):
        print(self.mw.className, end=", ")
        print(self.mw.name)
        self.__listWidgetsRecursive(self.mw, 1)

    def __listWidgetsRecursive(self, widget, depth):
        children = widget.getChildren()
        for child in children:
            if child.name != "":
                for i in range(depth):
                    print("\t", end="")
                print(child.className, end=", ")
                print(child.name)
                self.__listWidgetsRecursive(child, depth + 1)
    
    def getOnScreenWidgets(self, window=None):
        if window is None:
            window = self.mw
        window = Widget(window)
        widgets = self.__getWidgetsRecursive(window, 1)
        return widgets

    def __getWidgetsRecursive(self, widget, depth):
        widgets = []
        children = widget.getChildren()
        for child in children:
            widgets.append(child)
            widgets = widgets + self.__getWidgetsRecursive(child, depth + 1)
        return widgets

    def getNamedWidget(self, path, widget=None):
        if path == "":
            return
        if not widget:
            widget = self.mw
        wNames = path.split("/")
        extendedPath = self.widgetShortcuts(wNames[0])
        extendedPath.extend(wNames[1:])
        for name in extendedPath:
            widget = widget.getNamedChild(name)
            if not widget:
                return None
        return widget
    
    def widgetShortcuts(self, shortcut):
        if shortcut in self.__shortcutDict.keys():
            return self.__shortcutDict[shortcut].split("/")
        else:
            return [shortcut]
    
    def getWidgetsByToolTip(self, parent, tooltip):
        widgets = []
        if not parent:
            parent = self.mw
        if tooltip == "":
            return widgets
        for child in parent.getChildren():
            if child.toolTip == tooltip:
                widgets.append(child)
        return widgets
    
    def getWidgetsByClassName(self, parent, classname):
        widgets = []
        if not parent:
            parent = self.mw
        if classname == "":
            return widgets
        for child in parent.getChildren():
            if child.className == classname:
                widgets.append(child)
        return widgets
    
    def uniqueWidgetPath(self, widgetToID):
        path = widgetToID.name
        parent = widgetToID
        while(True):
            parent = parent.parent()
            if not parent:
                break
            if parent.name != "":
                path = parent.name + "/" + path
            else:
                path = "/" + path
        return path

        


class WidgetFinder(qt.QWidget):
    def __init__(self, parent=None):
        super(WidgetFinder, self).__init__(None)
        self.setAttribute(qt.Qt.WA_StyledBackground)
        self.setStyleSheet("QWidget { background-color: rgba(153, 51, 153, 50)}")
        self.focusPolicy = qt.Qt.StrongFocus
        self.LanguageToolsLogic = None
        self.shortcutKeySequence = qt.QKeySequence("Ctrl+6")
        self.shortcut = None
        self.logic = None
        self.cursorOverridden = False
        self.currentWidget = None
        self.sinalManager = SignalManager()
        self.aux = parent

    def __del__(self):
        self.showPointCursor(False)

    def enableShortcut(self, enable):
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
        if enable == self.cursorOverridden:
            return
        if enable:
            slicer.app.setOverrideCursor(qt.Qt.PointingHandCursor)
        else:
            slicer.app.restoreOverrideCursor()
        self.cursorOverridden = enable

    def showFullSize(self):
        self.pos = qt.QPoint()
        self.setFixedSize(self.aux.size)
        self.setWindowOpacity(0.2)
        self.show()
        self.setFocus(qt.Qt.ActiveWindowFocusReason)
        self.showPointCursor(True)

    def overlayOnWidget(self, widget):
        pos = widget.mapToGlobal(qt.QPoint())
        pos = self.aux.mapFromGlobal(pos)
        self.pos = pos
        self.setFixedSize(widget.size)

    def hideOverlay(self):
        self.hide()
        self.showPointCursor(False)

    def widgetAtPos(self, pos):
        self.setAttribute(qt.Qt.WA_TransparentForMouseEvents)
        widget = qt.QApplication.widgetAt(pos)
        self.setAttribute(qt.Qt.WA_TransparentForMouseEvents, False)
        return widget

    def keyPressEvent(self, event):
        self.hideOverlay()

    def mousePressEvent(self, event):
        # Get widget at mouse position
        pos = qt.QCursor().pos()
        widget = self.widgetAtPos(pos)
        self.overlayOnWidget(widget)
        self.hideOverlay()
        self.showPointCursor(False)
        #self.currentWidgetSelect = str(widget)
        self.sinalManager.emit(Widget(widget))

        self.currentWidget = widget

    def paintEvent(self, event):
        #we need to work on this
        self.setFixedSize(self.aux.size)
        self.pos = self.aux.pos
        

class Shapes(qt.QWidget):
    def __init__(self, parent=None):
        super(Shapes, self).__init__(parent)
        self.focusPolicy = qt.Qt.StrongFocus
        self.setAttribute(qt.Qt.WA_TransparentForMouseEvents)
        self.widget = None
        #slicer.app.setOverrideCursor(qt.Qt.PointingHandCursor)

    def setTargetWidget(self, widget):
        if widget is None:
            return

        self.widget = widget
        self.setFixedSize(widget.size)
        self.showFullSize()
        
    def showFullSize(self):
        self.pos = qt.QPoint()
        self.setFixedSize(self.parent().size)
        self.show()
        self.setFocus(qt.Qt.ActiveWindowFocusReason)

    def hideOverlay(self):
        self.hide()

    def paintEvent(self, event):
        if self.widget is None:
            return
        
        self.setFixedSize(self.parent().size)
        widget = self.widget

        pen = qt.QPen()
        pen.setWidth(20)
        pen.setColor(qt.QColor(255,0,0))

        pos = widget.mapToGlobal(qt.QPoint())
        pos = self.parent().mapFromGlobal(pos)
        painter = qt.QPainter(self)
        painter.setPen(pen)
        painter.drawEllipse(pos.x() - (200/2) + widget.rect.width()/2, pos.y() - (200/2) + widget.rect.height()/2, 200, 200)
    
    
        
class Widget():
    def __init__(self, widgetData) -> None:
        self.__widgetData = widgetData
        self.name = widgetData.name
        self.className = widgetData.className()
        if not hasattr(self.__widgetData, 'toolTip'):
            self.toolTip = "None"
        else:
            self.toolTip = widgetData.toolTip
        if not hasattr(self.__widgetData, 'text'):
            self.text = "None"
        else:
            self.text = widgetData.text
        pass

    def __str__(self):
        string = "Widget:\n"
        string += "\tName:      " + self.name + "\n"
        string += "\tText:      " + self.text + "\n"
        string += "\tToolTip:   " + self.toolTip + "\n"
        string += "\tClassName: " + self.className + "\n"
        string += "\tID:        " + hex(id(self.__widgetData)) + "\n"
        return string
    
    def __dict__(self):
        dict = {
            "name": self.name,
            "text": self.text,
            "toolTip": self.toolTip,
            "className": self.className,
            "id": hex(id(self.__widgetData)) 
        }
        return dict
    
    def inner(self):
        return self.__widgetData
    
    def parent(self):
        parent = self.__widgetData.parent()
        if not parent:
            return None
        return Widget(parent)

    def getNamedChild(self, childName):
        if not hasattr(self.__widgetData, 'children'):
            return None
        for child in self.__widgetData.children():
            if child.name == childName:
                return Widget(child)
        return None

    def getChildren(self):
        children = []
        if not hasattr(self.__widgetData, 'children'):
            return children
        for child in self.__widgetData.children():
            children.append(Widget(child))
        return children
    
    def childrenDetails(self):
        children = self.getChildren()
        for child in children:
            print(child)
    
    def click(self):
        return self.__widgetData.click()
    
    def getGlobalPos(self):
        mw = slicer.util.mainWindow()
        windowPos = mw.mapToGlobal(mw.rect.topLeft())

        globalPosTopLeft = self.__widgetData.mapToGlobal(self.__widgetData.rect.topLeft())
        return [globalPosTopLeft.x() - windowPos.x(), globalPosTopLeft.y() - windowPos.y()]
    
    def getSize(self):
        posTopLeft = self.__widgetData.rect.topLeft()
        posBotRight = self.__widgetData.rect.bottomRight()
        return [posBotRight.x() - posTopLeft.x(), posBotRight.y() - posTopLeft.y()]

class SignalManager(qt.QObject):
    received = qt.Signal(object)
    def __init__(self):
        super(SignalManager, self).__init__(None)

    def connect(self,func):
        self.received.connect(func)

    def emit(self, msg):
        self.received.emit(msg)

class ScreenshotTools():
    def __init__(self) -> None:
        self.handler = JSONHandler()
        pass

    def saveScreenshotMetadata(self, index):
        path = os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/"

        openWindows = []
        for w in slicer.app.topLevelWidgets():
            if hasattr(w, "isVisible") and not w.isVisible():
                continue
            print("test")
            openWindows.append(w)
            
            pass

        windows = []
        for wIndex in range(len(openWindows)):
            if not os.path.exists(path + str(index)):
                os.mkdir(path + str(index))
                pass

            
            screenshotData = TutorialScreenshot()
            screenshotData.screenshot = path + str(index) + "/" + str(wIndex) + ".png"
            screenshotData.metadata = path + str(index) + "/" + str(wIndex) + ".json"

            self.saveAllWidgetsData(screenshotData.screenshot, openWindows[wIndex])
            self.saveScreenshot(screenshotData.metadata, openWindows[wIndex])

            windows.append(screenshotData)
            pass
        pass
        return windows


    def getPixmap(self, window):
        screen = slicer.app.screens()[0]
        slicer.app.processEvents()
        pixmap = screen.grabWindow(window.winId())

        #return a qt object: QPixmap
        return pixmap
    
    def saveScreenshot(self, filename, window):
        self.getPixmap(window).save(filename, "PNG")
        pass

    def saveAllWidgetsData(self, filename, window):
        tool = util()
        data = {}
        widgets = tool.getOnScreenWidgets(window)
        for index in range(len(widgets)):
            try:
                if hasattr(widgets[index].inner(), "isVisible") and not widgets[index].inner().isVisible():
                    continue
                data[index] = {"name": widgets[index].name, "path": tool.uniqueWidgetPath(widgets[index]), "text": widgets[index].text, "position": widgets[index].getGlobalPos(), "size": widgets[index].getSize()}
            except:
                pass
        self.handler.saveScreenshotMetadata(data, filename)

class Tutorial:
    def __init__(self,
            title,
            author,
            date,
            description
    ):
        self.metadata = {}
        self.metadata["title"] = title
        self.metadata["author"] = author
        self.metadata["date"] = date
        self.metadata["desc"] = description

        self.steps = []

    
    def beginTutorial(self):
        screenshotTools = ScreenshotTools()
        #Screenshot counter
        self.nSteps = 0
        self.screenshottools = screenshotTools
        
    #TODO:Unsafe, there should be a better method to do this, at least add some conditions
    def clearTutorial(self):
        outputPath = os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/"
        if not os.path.exists(outputPath):
            return
        dirs = os.listdir(outputPath)
        for dir in dirs:
            if os.path.isdir(outputPath + dir):
                for sdir in os.listdir(outputPath + dir):
                    os.remove(outputPath + "/" + dir + "/" + sdir)
                os.rmdir(outputPath + dir)
            else:
                os.remove(outputPath + dir)
        pass

    def nextScreenshot(self):
        self.steps.append(self.screenshottools.saveScreenshotMetadata(self.nSteps))
        self.nSteps = self.nSteps + 1
    pass

    def endTutorial(self):
        handler = JSONHandler()
        handler.saveTutorial(self.metadata, self.steps)


class TutorialScreenshot:
    def __init__(self, screenshot="", metadata=""):
        self.screenshot = screenshot
        self.metadata = metadata
        pass
class JSONHandler:
    def __init__(self):
        self.path = os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        import json
        self.json = json
        pass

    def parseTutorial(self):
        
        pass

    def saveTutorial(self, metadata, stepsList):
        metadata["steps"] = []
        for step in stepsList:
            windows = []            
            for screenshot in step:
                datapair = {}
                datapair["window"] = screenshot.screenshot.replace(self.path, "")
                datapair["metadata"] = screenshot.metadata.replace(self.path, "")
                windows.append(datapair)
            pass
            metadata["steps"].append(windows)
        with open(self.path + "Tutorial.json", 'w', encoding='utf-8') as f:
            self.json.dump(metadata, f, ensure_ascii=False, indent=4)
        pass

    def saveScreenshotMetadata(self, data, path):
        with open(path, 'w', encoding='utf-8') as f:
            self.json.dump(data, f, ensure_ascii=False, indent=4)
        pass




