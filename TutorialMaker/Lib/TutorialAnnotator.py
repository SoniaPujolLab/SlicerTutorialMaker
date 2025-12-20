import slicer
import qt
import json
import os
import copy
from Lib.Annotations import Annotation, AnnotationType, AnnotatorSlide, AnnotatedTutorial
from Lib.TutorialUtils import Tutorial, TutorialScreenshot

import slicer
from slicer.i18n import tr as _



class TutorialAnnotator(qt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.READY_EVENTS = False

        self.defaultHelperOffset = [60,60]
        self.thumbnailRatio = [280, 165]
        self.selectedSlideSize = [0, 0]

        self.slides : list[AnnotatorSlideWidget] = []

        self.selectedSlideIndex = 0
        self.selectedAnnotator : AnnotatorSlide = None
        self.selectedAnnotationType : AnnotationType = AnnotationType.Nil
        self.selectedAnnotation : Annotation = None
        

        # Default settings for the annotations
        _penSettings = {"color": qt.QColor(255, 128, 0),
                       "fontSize": 14,
                       "penThickness": 4}

        self.penSettings = _penSettings

        # Move through stacked widgets
        self.selectorParentCount = 0

        # Update function to refresh thumbnails and the annotations previews
        self.updateTimer = qt.QTimer()
        self.updateTimer.setTimerType(qt.Qt.PreciseTimer)
        self.updateTimer.setInterval(34) #34ms Interval = 30 ups
        self.updateTimer.timeout.connect(self.refreshViews)
        self.updateTimer.start()

        # Need to do a overhaul of the preview function so this isn't necessary
        self.lastAppPos = qt.QPoint()
        
        self.outputFolder = f"{os.path.dirname(__file__)}/../Outputs/Annotations"

        # Tutorial Information
        self.tutorialInfo = {"name": "", "author" : "", "date": "", "desc": ""}
        self.outputName = ""

        self.setupGUI()

        self.installEventFilter(self)

        self.READY_EVENTS = True




    def setupGUI(self):
        # Get and load UI Fle
        self.dir_path = os.path.dirname(__file__)
        UI_window = slicer.util.loadUI(self.dir_path+'/../Resources/UI/TutorialAnnotator.ui')

        self.windowLayout = qt.QVBoxLayout()
        self.windowLayout.addWidget(UI_window)

        self.setCentralWidget(UI_window)

        self.setWindowTitle(_("TutorialMaker - Annotator"))

        # Setup Slide
        self.selectedSlideWidget = self.findChild(qt.QLabel, "label_selectedSlide")
        self.selectedSlideWidget.installEventFilter(self)
        self.selectedSlideWidget.setMouseTracking(True)
        self.selectedSlideWidget.setScaledContents(False) #

        # Configure the Slide Title and Slide body text boxes
        self.slideTitleWidget = self.findChild(qt.QLineEdit, "lineEdit_slideTitle")
        self.slideTitleWidget.placeholderText = _("Title for the slide")

        self.slideBodyWidget = self.findChild(qt.QTextEdit, "textEdit_slideDescription")
        self.slideBodyWidget.placeholderText = _("Write a description for the slide")

        # Left Scroll Area
        self.slidesScrollArea = self.findChild(qt.QScrollArea, "scrollArea_loadedSlides")
        self.slide_gridLayout = qt.QGridLayout(self.slidesScrollArea.widget())
        self.slidesScrollArea.setAcceptDrops(True)
        self.slidesScrollArea.installEventFilter(self)

        # Offset positional helper
        self.OffsetHelperWidget = DraggableLabel()
        self.OffsetHelperWidget.setParent(self.selectedSlideWidget)
        self.OffsetHelperWidget.setFixedSize(10,10)
        self.OffsetHelperWidget.setStyleSheet("background-color: #03fc0b;border-style: outset; border-width: 2px; border-color: #fc034e;")
        self.OffsetHelperWidget.SetCenter(250,250)
        self.OffsetHelperWidget.installEventFilter(self.OffsetHelperWidget)
        self.OffsetHelperWidget.SetActive(False)

        # Optional positional helper
        self.OptHelperWidget = DraggableLabel()
        self.OptHelperWidget.setParent(self.selectedSlideWidget)
        self.OptHelperWidget.setFixedSize(10,10)
        self.OptHelperWidget.setStyleSheet("background-color: #fc034e;border-style: outset; border-width: 2px; border-color: #03fc0b;")
        self.OptHelperWidget.SetCenter(250,250)
        self.OptHelperWidget.installEventFilter(self.OptHelperWidget)
        self.OptHelperWidget.SetActive(False)

        # Load Used Resources
        resourceFolder = os.path.dirname(__file__) + '/../Resources'
        self.image_ChevronUp = qt.QImage(f'{resourceFolder}/Icons/ScreenshotAnnotator/chevron_up.png').scaled(20,20, qt.Qt.KeepAspectRatio, qt.Qt.SmoothTransformation)
        self.image_ChevronDown = qt.QImage(f'{resourceFolder}/Icons/ScreenshotAnnotator/chevron_down.png').scaled(20,20, qt.Qt.KeepAspectRatio, qt.Qt.SmoothTransformation)
        self.image_ArrowUp = qt.QImage(f'{resourceFolder}/Icons/ScreenshotAnnotator/arrow_up.png').scaled(20,20, qt.Qt.KeepAspectRatio, qt.Qt.SmoothTransformation)
        self.image_ArrowDown = qt.QImage(f'{resourceFolder}/Icons/ScreenshotAnnotator/arrow_down.png').scaled(20,20, qt.Qt.KeepAspectRatio, qt.Qt.SmoothTransformation)

        self.icon_chevron = qt.QIcon()
        self.icon_chevron.addPixmap(qt.QPixmap.fromImage(self.image_ChevronDown), qt.QIcon.Normal, qt.QIcon.Off)
        self.icon_chevron.addPixmap(qt.QPixmap.fromImage(self.image_ChevronUp), qt.QIcon.Normal, qt.QIcon.On)
        self.icon_arrowUp = qt.QIcon(qt.QPixmap.fromImage(self.image_ArrowUp))
        self.icon_arrowDown = qt.QIcon(qt.QPixmap.fromImage(self.image_ArrowDown))

        self.createToolbarActions()
        pass

    def createToolbarActions(self):

        def addActions(_toolbar, _actions):
            for _action in _actions:
                qAction = qt.QAction(_action["text"], _toolbar)
                qIcon = qt.QIcon()
                qIcon.addPixmap(qt.QPixmap(_action["icon"]), qt.QIcon.Mode.Normal, qt.QIcon.State.On)
                if "checkable" in _action and _action["checkable"]:
                    qAction.setCheckable(True)
                    if "icon_inactive" in _action:
                        qIcon.addPixmap(qt.QPixmap(_action["icon_inactive"]), qt.QIcon.Mode.Normal, qt.QIcon.State.Off)

                qAction.setIcon(qIcon)
                qAction.triggered.connect(_action["trigger"])
                _toolbar.addAction(qAction)
        # System Toolbar
        toolbar = self.centralWidget().findChild(qt.QToolBar, "toolBar_menu")

        systemActions = [
            {"text": _("Open"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/open.png', "trigger": self.loadAnnotations},
            {"text": _("Save"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/save.png', "trigger": self.saveAnnotations},
            {"text": _("Undo"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/back.png', "trigger": self.deleteSelectedAnnotation},
            {"text": _("Delete"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/remove.png', "trigger": self.deleteSlide},
            {"text": _("Add"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/add.png', "trigger": self.addBlankPage},
            {"text": _("Copy"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/copy.png', "trigger": self.copySlide}
        ]
        addActions(toolbar, systemActions)

        # Annotation Toolbar
        toolbar = self.centralWidget().findChild(qt.QToolBar, "toolBar_tools")

        annotationsActions = [
            {   "text": _("Select"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/actselect.png', "checkable" : True,
                "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/select.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.Selecting))},

            {   "text": _("Square"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act1_p.png', "checkable" : True,
                "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act1.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.Rectangle))},

            #{   "text": _("Circle"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act2_p.png', "checkable" : True,
            #    "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act2.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.Selecting))},

            #{   "text": _("Click"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/pointer_p.png', "checkable" : True,
            #    "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/pointer.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.Click))},

            {   "text": _("Arrow"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/arrow_enabled.png', "checkable" : True,
                "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/arrow_disabled.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.Arrow))},

            {   "text": _("Arrow text"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act3_p.png', "checkable" : True,
                "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act3.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.ArrowText))},
            
            #{   "text": _("Icon"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act4_p.png', "checkable" : True,
            #    "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act4.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.Selecting))},
            
            {   "text": _("Text"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act5_p.png', "checkable" : True,
                "icon_inactive": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act5.png', "trigger": (lambda: self.changeAnnotationType(AnnotationType.TextBox))},
            
        ]
        addActions(toolbar, annotationsActions)
        self.AnnotationToolbarActions = qt.QActionGroup(toolbar)
        for action in toolbar.actions():
            self.AnnotationToolbarActions.addAction(action)

        # Style Toolbar
        toolbar = self.centralWidget().findChild(qt.QToolBar, "toolBar_style")

        label_text_color = qt.QLabel("Color")
        toolbar.addWidget(label_text_color)

        addActions(toolbar, [{"text": _("color"), "icon": self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/color.png', "trigger": self.changeColor}])

        thickenesValue = 4
        thickenesSpinbox = qt.QSpinBox()
        thickenesSpinbox.setSuffix(_(" thick."))
        thickenesSpinbox.setMinimum(1)
        thickenesSpinbox.setMaximum(15)
        thickenesSpinbox.setSingleStep(1)
        thickenesSpinbox.setValue(thickenesValue)
        thickenesSpinbox.valueChanged.connect(self.updateAnnotationThicknessValue)
        self.thickenesSpinbox = thickenesSpinbox
        toolbar.addWidget(thickenesSpinbox)

        textLabel = qt.QLabel("Text: ")
        toolbar.addWidget(textLabel)

        fontSize = 14
        fontSpinbox = qt.QSpinBox()
        fontSpinbox.setSuffix(" px")
        fontSpinbox.setMinimum(5)
        fontSpinbox.setMaximum(120)
        fontSpinbox.setSingleStep(1)
        fontSpinbox.setValue(fontSize)
        fontSpinbox.valueChanged.connect(self.updateTextFontSize)
        self.fontSpinbox = fontSpinbox
        toolbar.addWidget(fontSpinbox)
        pass

    def updateAnnotationThicknessValue(self):
        self.penSettings["penThickness"] = self.thickenesSpinbox.value
        self.updateSelectedAnnotationSettings()
        pass

    def updateTextFontSize(self):
        self.penSettings["fontSize"] = self.fontSpinbox.value
        self.updateSelectedAnnotationSettings()
        pass

    def changeColor(self):
        color_dialog = qt.QColorDialog()
        color_dialog.setCurrentColor(self.penSettings["color"])
        if color_dialog.exec_():
            color = color_dialog.selectedColor()
            self.penSettings["color"] = color
        self.updateSelectedAnnotationSettings()

    def updateSelectedAnnotationSettings(self):
        if self.selectedAnnotation is not None:
            self.selectedAnnotation.penConfig(self.penSettings["color"], self.penSettings["fontSize"],self.penSettings["penThickness"], brush=True)
        pass

    def changeAnnotationType(self, annotationType):
        self.finishCurrentAnnotation()
        if self.selectedAnnotationType == annotationType or annotationType == AnnotationType.Nil:
            toolbar = self.centralWidget().findChild(qt.QToolBar, "toolBar_tools")
            for action in toolbar.actions():
                action.setChecked(False)
            self.selectedAnnotationType = AnnotationType.Nil
            return
        self.selectedAnnotationType = annotationType
        pass

    def loadAnnotations(self):
        from Lib.TutorialUtils import get_module_basepath as getModulePath
        parent = slicer.util.mainWindow()
        basePath = getModulePath("TutorialMaker")
        jsonPath = qt.QFileDialog.getOpenFileName(
            parent,
            _("Select a JSON file"),
            basePath + "/Outputs/Annotations/",              
            _("JSON Files (*.json)") 
        )
        self.raise_()
        self.activateWindow()
        if not os.path.exists(jsonPath):
            return
        
        [tInfo, tSlides] = AnnotatedTutorial.LoadAnnotatedTutorial(jsonPath)
        for slide in self.slides:
            self.slide_gridLayout.removeWidget(slide)
            slide.deleteLater()
        self.slides = []

        for slideIndex in range(len(tSlides)):
            slideWidget = AnnotatorSlideWidget(slideIndex, self.thumbnailRatio, self.slidesScrollArea.widget())
            slideWidget.thumbnailClicked.connect(self.changeSelectedSlide)
            slideWidget.swapRequest.connect(self.swapSlidePosition)
            slideWidget.SetTutorialSlide(tSlides[slideIndex])

            self.slides.append(slideWidget)
            self.slide_gridLayout.addWidget(slideWidget)  # noqa: F821
        self.tutorialInfo = tInfo
        pass

    def saveAnnotations(self):
        slides : list[AnnotatorSlide] = []
        for slide in self.slides:
            slides.append(slide.Slide)
        AnnotatedTutorial.SaveAnnotatedTutorial(self.tutorialInfo, slides)
        pass

    def deleteSelectedAnnotation(self):
        self.selectedAnnotation = None
        if self.selectedAnnotationType == AnnotationType.Selected:
            self.selectedAnnotationType = AnnotationType.Selecting
        pass

    def deleteSlide(self):
        deletedSlide = self.slides.pop(self.selectedSlideIndex)
        for index, slide in enumerate(self.slides):
            slide.slideIndex = index
        indexFixer = 0
        if len(self.slides) <= self.selectedSlideIndex:
            indexFixer = -1

        self.changeSelectedSlide(self.selectedSlideIndex + indexFixer)
        self.slide_gridLayout.removeWidget(deletedSlide)
        deletedSlide.deleteLater()
        pass

    def addBlankPage(self):

        pass

    def copySlide(self):
        return 
        originalSlide = self.slides[self.selectedSlideIndex].Slide

        newImage = originalSlide.image.copy()
        newMetadata = copy.deepcopy(originalSlide.metadata)
        newAnnotations = copy.deepcopy(originalSlide.annotations)
        newWindowOffset = copy.deepcopy(originalSlide.windowOffset)

        newSlide = AnnotatorSlide(newImage, newMetadata, newAnnotations, newWindowOffset)

        slideWidget = AnnotatorSlideWidget(self.selectedSlideIndex + 1, self.thumbnailRatio, self.slidesScrollArea.widget())
        slideWidget.SetTutorialSlide(newSlide)
        self.slide_gridLayout.addWidget(slideWidget, self.selectedSlideIndex + 1, 0)
        slideWidget.thumbnailClicked.connect(self.changeSelectedSlide)
        slideWidget.swapRequest.connect(self.swapSlidePosition)
        self.slides.insert(slideWidget, self.selectedSlideIndex + 1)
        for index, slide in enumerate(self.slides):
            slide.slideIndex = index
        pass

    def onActionTriggered(self, sender):
        pass

    

    def swapSlidePosition(self, index, swapTo):
        if swapTo >= len(self.slides) or swapTo < 0:
            return
        tmp = self.slides[swapTo]
        self.slides[swapTo] = self.slides[index]
        self.slides[swapTo].slideIndex = swapTo
        self.slide_gridLayout.addWidget(self.slides[swapTo], swapTo, 0)

        self.slides[index] = tmp
        self.slides[index].slideIndex = index
        self.slide_gridLayout.addWidget(self.slides[index], index, 0)
        pass

    def changeSelectedSlide(self, slideId):
        self.finishCurrentAnnotation()

        # Save text to slideAnnotator
        if self.selectedAnnotator is not None:
            self.selectedAnnotator.SlideTitle = self.slideTitleWidget.text
            self.selectedAnnotator.SlideBody = self.slideBodyWidget.toPlainText()

        # Change the slide variables
        self.selectedSlideIndex = slideId
        selectedSlideWidget = self.slides[slideId]
        selectedScreenshot = selectedSlideWidget.Slide

        self.selectedSlideWidget.setPixmap(selectedScreenshot.GetResized(*self.selectedSlideSize, keepAspectRatio=True))
        self.selectedAnnotator = selectedScreenshot

        # Load text from slideAnnotator
        self.slideTitleWidget.setText(self.selectedAnnotator.SlideTitle)
        self.slideBodyWidget.setText(self.selectedAnnotator.SlideBody)
        pass

    def finishCurrentAnnotation(self):
        if self.selectedAnnotation is not None:
            self.selectedAnnotation.drawBoundingBox = False
            if not self.selectedAnnotation.PERSISTENT:
                self.selectedAnnotator.annotations.remove(self.selectedAnnotation)
            self.selectedAnnotation = None
            if self.selectedAnnotationType == AnnotationType.Selected:
                self.selectedAnnotationType = AnnotationType.Selecting

    def selectionHandler(self, appPos):
        posInImage = self.selectedAnnotator.MapScreenToImage(appPos, self.selectedSlideWidget)
        annotations = self.selectedAnnotator.FindAnnotationsAtPos(*posInImage)

        if len(annotations) < 1:
            return
        # Using the parent counter to go back a set amount from the widget parents
        if self.selectorParentCount > len(annotations) - 1:
            self.selectorParentCount = len(annotations) - 1
        elif self.selectorParentCount < 0:
            self.selectorParentCount = 0
        selectedAnnotation = annotations[len(annotations) - 1 - self.selectorParentCount]
        if selectedAnnotation is None:
            return
        optValuesInImage = self.selectedAnnotator.MapImageToScreen(qt.QPointF(selectedAnnotation.optX, selectedAnnotation.optY,), self.selectedSlideWidget)
        self.OptHelperWidget.SetCenter(*optValuesInImage)
        _offsetPos = self.selectedAnnotator.MapImageToScreen(qt.QPointF(selectedAnnotation.target["position"][0] + selectedAnnotation.offsetX,
                                                                       selectedAnnotation.target["position"][1] + selectedAnnotation.offsetY), self.selectedSlideWidget)

        self.OffsetHelperWidget.SetCenter(*_offsetPos)

        self.selectedAnnotation = selectedAnnotation
        self.selectedAnnotationType = AnnotationType.Selected
        self.selectedAnnotation.drawBoundingBox = True

    def annotationHandler(self, appPos):
        if self.selectedAnnotation is None:
            return
        self.selectedAnnotation.PERSISTENT = True
        selectedAnnotation = self.selectedAnnotation
        self.finishCurrentAnnotation()

        self.selectedAnnotation = selectedAnnotation
        self.selectedAnnotationType = AnnotationType.Selected
        self.selectedAnnotation.drawBoundingBox = True

    def previewAnnotation(self, appPos):
        if self.selectedAnnotator is None:
            return
        self.lastAppPos = appPos
        posInImage = self.selectedAnnotator.MapScreenToImage(appPos, self.selectedSlideWidget)
        widgets = self.selectedAnnotator.FindWidgetsAtPos(*posInImage)

        def ApplyHelper():
            optValuesInImage = self.selectedAnnotator.MapScreenToImage(qt.QPointF(*self.OptHelperWidget.GetCenter()), self.selectedSlideWidget)
            self.selectedAnnotation.setValuesOpt(*optValuesInImage)


            _helperPos = self.selectedAnnotator.MapScreenToImage(qt.QPointF(*self.OffsetHelperWidget.GetCenter()), self.selectedSlideWidget)
            offsetFromTargetWidget = [_helperPos[0] - self.selectedAnnotation.target["position"][0],
                                      _helperPos[1] - self.selectedAnnotation.target["position"][1]]

            self.selectedAnnotation.setValuesOffset(*offsetFromTargetWidget)

        if self.selectedAnnotationType == AnnotationType.Selected:
            self.OptHelperWidget.SetActive(self.selectedAnnotation.wantsOptHelper())
            self.OffsetHelperWidget.SetActive(self.selectedAnnotation.wantsOffsetHelper())
            ApplyHelper()
            return

        if len(widgets) < 1:
            return

        # Using the parent counter to go back a set amount from the widget parents
        if self.selectorParentCount > len(widgets) - 1:
            self.selectorParentCount = len(widgets) - 1
        elif self.selectorParentCount < 0:
            self.selectorParentCount = 0

        selectedWidget = widgets[len(widgets) - 1 - self.selectorParentCount]

        if selectedWidget is None:
            return

        if self.selectedAnnotation is None:
            self.selectedAnnotation = Annotation(TargetWidget=selectedWidget, Type=self.selectedAnnotationType)
            self.selectedAnnotator.AddAnnotation(self.selectedAnnotation)
            self.selectedAnnotation.penConfig(self.penSettings["color"], self.penSettings["fontSize"],self.penSettings["penThickness"], brush=True)
            self.OptHelperWidget.SetActive(self.selectedAnnotation.wantsOptHelper())
            self.OffsetHelperWidget.SetActive(self.selectedAnnotation.wantsOffsetHelper())

        self.selectedAnnotation.target = selectedWidget

        # Configure The Annotation Optional Helper so that its always towards the center

        helperPosition = copy.deepcopy(self.defaultHelperOffset)
        if appPos.x() > self.selectedSlideSize[0]/2:
            helperPosition[0] = -helperPosition[0]
        if appPos.y() > self.selectedSlideSize[1]/2:
            helperPosition[1] = -helperPosition[1]
        self.OptHelperWidget.SetCenter(appPos.x() + helperPosition[0], appPos.y() + helperPosition[1])

        # Configure The Annotation Offset Helper so it defaults to zero
        # Probably one the ugliest way to do this, maybe find someway better
        _reversePostion = self.selectedAnnotator.MapImageToScreen(qt.QPointF(*selectedWidget["position"]), self.selectedSlideWidget)
        self.OffsetHelperWidget.SetCenter(*_reversePostion)

        ApplyHelper()
        pass

    def refreshViews(self):
        if self.selectedAnnotator is None:
            return
        self.selectedAnnotator.ReDraw()
        self.selectedSlideWidget.setPixmap(self.selectedAnnotator.GetResized(*self.selectedSlideSize, keepAspectRatio=True))
        pass

    def forceTutorialOutputName(self, name):
        self.outputName = name
        pass

    def selectorParentDelta(self, delta : int):
        self.selectorParentCount += delta
        self.previewAnnotation(self.lastAppPos)

    def mousePressEvent(self, event):
        self.setFocus()
        if self.selectedAnnotationType == AnnotationType.Nil:
            return
        if self.selectedAnnotationType == AnnotationType.Selecting:
            self.selectionHandler(event.pos())
            return
        self.annotationHandler(event.pos())

    def mouseReleaseEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        if self.selectedAnnotationType is not AnnotationType.Nil and self.selectedAnnotationType is not AnnotationType.Selecting:
            self.previewAnnotation(event.pos())

    def keyboardEvent(self, event):
        if event.key() == qt.Qt.Key_Escape:
            self.setFocus()
            return False

        if self.selectedAnnotationType == AnnotationType.Selected:
            if event.key() == qt.Qt.Key_Delete:
                self.selectedAnnotation.PERSISTENT = False
                self.finishCurrentAnnotation()

            elif self.selectedAnnotation.type in [AnnotationType.TextBox, AnnotationType.ArrowText]:
                # Detect command Ctrl+C copy text
                if event.key() == qt.Qt.Key_C and event.modifiers() & qt.Qt.ControlModifier:
                    qt.QApplication.clipboard().setText(self.selectedAnnotation.text)
                
                # Detect command Ctl+v page text
                elif event.key() == qt.Qt.Key_V and event.modifiers() & qt.Qt.ControlModifier:
                    self.selectedAnnotation.text += qt.QApplication.clipboard().text()

                # Detect Enter to add a line break
                elif event.key() in [qt.Qt.Key_Return, qt.Qt.Key_Enter]:
                    self.selectedAnnotation.text += "\n"

                # Detect Backspace
                elif event.key() == qt.Qt.Key_Backspace:
                    self.selectedAnnotation.text = self.selectedAnnotation.text[:-1]

                else:
                    self.selectedAnnotation.text += event.text()

            return True

        elif self.selectedAnnotator is not None and self.selectedAnnotation is not None:
            if event.key() == qt.Qt.Key_Up:
                self.selectorParentDelta(-1)
                return True
            elif event.key() == qt.Qt.Key_Down:
                self.selectorParentDelta(1)
                return True

        return False
    
    def scrollEvent(self, event):
        threshold = 4 #scroll threshold

        delta = event.angleDelta().y()
        if delta > threshold:
            self.selectorParentDelta(-1)
        elif delta < threshold:
            self.selectorParentDelta(1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            if event.mimeData().text() == "AnnotatorSlideWidget":
                event.accept()
                return True
        event.ignore()
        return True

    def dragDropEvent(self, event):
        slideWidget : AnnotatorSlideWidget = event.source()
        pos = event.pos()
        for slide in self.slides:
            if pos.y() + self.slidesScrollArea.verticalScrollBar().value < slide.pos.y() + slide.size.height():
                self.swapSlidePosition(slideWidget.slideIndex, slide.slideIndex)
                break
        event.accept()
        return True
    
    def windowResizeEvent(self, event):
        mainScreenWidth = (self.slidesScrollArea.width * 3)
        ratio = mainScreenWidth/self.selectedSlideWidget.width
        mainScreenHeight = self.selectedSlideWidget.height * ratio
        self.selectedSlideSize = [mainScreenWidth, mainScreenHeight]

        for slide in self.slides:
            slide._resizeEvent(event)
        return True

    def eventFilter(self, obj, event):
        if not self.READY_EVENTS:
            return False
        if obj == self.selectedSlideWidget:
            if event.type() == qt.QEvent.Leave:
                if self.selectedAnnotation is not None and not self.selectedAnnotation.PERSISTENT:
                    return self.finishCurrentAnnotation()
            elif event.type() == qt.QEvent.MouseButtonPress:
                return self.mousePressEvent(event)
            elif event.type() == qt.QEvent.MouseMove:
                return self.mouseMoveEvent(event)
            elif event.type() == qt.QEvent.MouseButtonRelease:
                return self.mouseReleaseEvent(event)
            elif event.type() == qt.QEvent.Wheel:
                return self.scrollEvent(event)
        if obj == self.slidesScrollArea:
            if event.type() == qt.QEvent.DragEnter:
                return self.dragEnterEvent(event)
            elif event.type() == qt.QEvent.DragMove:
                return self.dragEnterEvent(event)
            elif event.type() == qt.QEvent.Drop:
                return self.dragDropEvent(event)
            
        else:
            if event.type() == qt.QEvent.KeyPress:
                return self.keyboardEvent(event)
            elif event.type() == qt.QEvent.Resize:
                return self.windowResizeEvent(event)
            elif event.type() == qt.QEvent.WindowStateChange:
                def callback():
                    self.windowResizeEvent(event)
                qt.QTimer.singleShot(100, callback)
                return False
        return False
            
            
    def loadImagesAndMetadata(self, tutorialData):
        for stepIndex, screenshots in enumerate(tutorialData.steps):
            slideWidget = AnnotatorSlideWidget(stepIndex, self.thumbnailRatio, self.slidesScrollArea.widget())
            slideWidget.thumbnailClicked.connect(self.changeSelectedSlide)
            slideWidget.swapRequest.connect(self.swapSlidePosition)

            #>>>>>> This assumes that the first window is always the SlicerAppMainWindow <<<<<<<

            #Main window
            if len(screenshots) > 1:
                try:
                    cImage, cMetadata = AnnotatedTutorial.GetCompositeSlide(screenshots)
                    annotatorSlide = AnnotatorSlide(cImage, cMetadata)
                    annotatorSlide.SlideLayout = "Screenshot"
                    slideWidget.SetTutorialSlide(annotatorSlide)
                    for screenshotIndex, sreenshot in enumerate(screenshots):
                        annotatorSlide.screenshotPaths.append(f"{stepIndex}/{screenshotIndex}")
                except Exception as e:
                    print(e)
                    print(f"ERROR: Annotator Failed to add window in step:{stepIndex}, loadImagesAndMetadata")
                    continue

            else:
                try:
                    annotatorSlide = AnnotatorSlide(screenshots[0].getImage(), screenshots[0].getWidgets())
                    annotatorSlide.SlideLayout = "Screenshot"
                    slideWidget.SetTutorialSlide(annotatorSlide)
                    annotatorSlide.screenshotPaths = [f"{stepIndex}/0"]
                except Exception:
                    print(f"ERROR: Annotator Failed to add top level window in step:{stepIndex}, loadImagesAndMetadata")
                    del slideWidget
                    continue
                

            self.slides.append(slideWidget)  # noqa: F821
            self.slide_gridLayout.addWidget(slideWidget)  # noqa: F821
        def callback():
            self.windowResizeEvent(None)
            self.changeSelectedSlide(0)
        qt.QTimer.singleShot(100, callback)

    def openJsonFile(self, filepath):
        directory_path = os.path.dirname(filepath)
        # Read the data from the file
        with open(filepath, encoding='utf-8') as file:
            rawTutorialData = json.load(file)
            file.close()


        tutorial = Tutorial(
            rawTutorialData["title"],
            rawTutorialData["author"],
            rawTutorialData["date"],
            rawTutorialData["desc"]
        )

        self.tutorialInfo = tutorial.metadata

        stepList = []
        tutorial.steps = stepList
        for step in rawTutorialData["steps"]:
            screenshotList = []
            for window in step:
                wScreenshot = TutorialScreenshot(
                    directory_path + "/" + window["window"],
                    directory_path + "/" + window["metadata"]
                )
                screenshotList.append(wScreenshot)
            tutorial.steps.append(screenshotList)
        self.loadImagesAndMetadata(tutorial)

class AnnotatorSlideWidget(qt.QWidget):
    thumbnailClicked = qt.Signal(int)
    swapRequest = qt.Signal(int, int)

    def __init__(self, slideIndex : int, thumbnailRatio, parent = None):
        super().__init__(parent)

        self.slideIndex = slideIndex

        self.UNDELETABLE = False
        self.thumbnailSize = [280, 165] #Default Value

        self.buttonSize = [24, 24]

        self.Slide : AnnotatorSlide = None
        self.SlideWidget : tmLabel = None

        self.SetupGUI()
        
        self.slideUpButton.clicked.connect(self.swapUp)
        self.slideDownButton.clicked.connect(self.swapDown)

    def SetupGUI(self):
        self.slideLayout = qt.QGridLayout()
        self.setLayout(self.slideLayout)
        self.setAttribute(qt.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #9e9493;')
        self.setObjectName(f"label_step_{self.slideIndex}")

        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

        #This can be done in a UI file

        self.slideUpButton = qt.QPushButton()
        self.slideDownButton = qt.QPushButton()

        self.slideUpButton.setParent(self)
        self.slideUpButton.setFixedSize(*self.buttonSize)
        self.slideUpButton.move(self.thumbnailSize[0] - 50, 10)
        self.slideUpButton.setIcon(self.window().icon_arrowUp)

        self.slideDownButton.setParent(self)
        self.slideDownButton.setFixedSize(*self.buttonSize)
        self.slideDownButton.move(self.thumbnailSize[0] - 20, 10)
        self.slideDownButton.setIcon(self.window().icon_arrowDown)
        pass

    def SetTutorialSlide(self, annotatorSlide : AnnotatorSlide):
        screenshotWidget = tmLabel(f"label_window_{self.slideIndex}", self.slideIndex)
        screenshotWidget.setObjectName(f"label_window_{self.slideIndex}")
        self.slideLayout.addWidget(screenshotWidget)

        self.SlideWidget = screenshotWidget
        self.Slide = annotatorSlide

        screenshotWidget.clicked.connect(lambda:self.thumbnailClick())

        screenshotWidget.stackUnder(self.slideUpButton)

    def swapUp(self, state):
        self.swapRequest.emit(self.slideIndex, self.slideIndex - 1)
        pass

    def swapDown(self, state):
        self.swapRequest.emit(self.slideIndex, self.slideIndex + 1)
        pass

    def thumbnailClick(self):
        self.thumbnailClicked.emit(self.slideIndex)
        pass

    def _resizeEvent(self, event):
        scrollViewport = self.parent().parent()
        if scrollViewport is None:
            return
        scrollareaWidth = scrollViewport.width - 25
        scaleFactor = scrollareaWidth/self.Slide.image.width()
        self.thumbnailSize = [scrollareaWidth, scaleFactor*self.Slide.image.height()]
        self.SlideWidget.setPixmap(self.Slide.GetResized(*self.thumbnailSize))

        self.slideUpButton.move(self.thumbnailSize[0] - 50, 10)
        self.slideDownButton.move(self.thumbnailSize[0] - 20, 10)
        pass

    def mousePressEvent(self, event):
        pass
    def mouseMoveEvent(self, event):
        if event.buttons() == qt.Qt.LeftButton:
            drag = qt.QDrag(self)
            mime = qt.QMimeData()
            mime.setText("AnnotatorSlideWidget")
            drag.setMimeData(mime)
            drag.exec_(qt.Qt.MoveAction)
        pass

class DraggableLabel(qt.QLabel):
    def __init__(self, text="",parent=None):
        super().__init__(text, parent)

    def GetCenter(self):
        pos = self.pos
        x = pos.x()
        y = pos.y()
        size = self.size
        width = size.width()
        height = size.height()

        return [x + width/2, y + height/2]

    def SetCenter(self, x : int, y : int):
        size = self.size
        width = size.width()
        height = size.height()

        self.move(x - width/2, y - height/2)

    def SetActive(self, state : bool):
        if state:
            self.show()
            self.setAttribute(qt.Qt.WA_TransparentForMouseEvents, False)
            pass
        else:
            self.hide()
            self.setAttribute(qt.Qt.WA_TransparentForMouseEvents)
            pass

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == qt.QEvent.MouseMove:
                if event.button() == 0: # Left Button pressed
                    sPos = event.screenPos().toPoint()
                    pos = self.parent().mapFromGlobal(sPos)
                    self.SetCenter(pos.x(), pos.y())

class tmLabel(qt.QLabel):
    clicked = qt.Signal()

    def __init__(self, text, index, parent=None):
        super().__init__(text, parent)
        self.index = index

    def mousePressEvent(self, event):
        self.clicked.emit()