#######################
import qt
import slicer
import json
import os
import time
import pyautogui
from PyQt5 import QtWidgets, QtCore


class MousePressFilter(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.last_ctrl = False
        self.last_widget = None
        self.step = 0
        self.metadata = []


    def screen_shot(self, widget, metadataJson, step):
        screenshot_folder = os.path.join(os.getcwd(), "screenshot_new")
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        hora = time.strftime("%Y%m%d-%H%M%S")
        root = os.path.join(screenshot_folder, f"{hora}.png")
        cap = pyautogui.screenshot()
        cap.save(root)
        print("Captura de pantalla guardada.")


        mainWindow = slicer.util.mainWindow()
        mainWindowPos_global = mainWindow.mapToGlobal(mainWindow.rect.topLeft())
        widgetTopLeft_global = widget.mapToGlobal(widget.rect.topLeft())
        widgetBottomRight_global = widget.mapToGlobal(widget.rect.bottomRight())
        widgetPos_mainWindow = [widgetTopLeft_global.x() - mainWindowPos_global.x(), widgetTopLeft_global.y() - mainWindowPos_global.y()]
        widgetSize_mainWindow = [widgetBottomRight_global.x() - widgetTopLeft_global.x(), widgetBottomRight_global.y() - widgetTopLeft_global.y()]
        # Widget by index
        my_list = slicer.util.findChildren(mainWindow)
        compare_string = str(widget)
        for index, element in enumerate(my_list):
            if str(element) == compare_string:
                print("El elemento", element,"en el índice", index)
                break
        wroot = " "    
        w = widget
        if w.name:
            wroot = "/" + str(w.name)
        else:
            my_list = slicer.util.findChildren(w.parent() , className = w.className())
            compare_string = str(w)
            for index, element in enumerate(my_list):
                if str(element) == compare_string:
                    #print("El elemento", element,"en el índice", index)
                    break
            wroot = "/" + str(index) + " " +str(w.className())
        while w != slicer.util.mainWindow():
            w = w.parent()
            if w.name:
                wroot = "/" + str(w.name) + wroot
            else:
                my_list = slicer.util.findChildren(w.parent(), className = w.className())
                compare_string = str(w)
                for index, element in enumerate(my_list):
                    if str(element) == compare_string:
                        #print("El elemento", element,"en el índice", index)
                        break
                wroot = "/" + str(index) + " " +str(w.className()) + wroot


        metadataJsonUpdate =  {    "step": step,
                                    "wiget": str(widget),
                                    "wiget root": wroot,
                                    "widget index": "slicer.util.findChildren(slicer.util.mainWindow())[" + str(index) + "]" ,
                                    "widget type": str(type(widget)),
                                    "widget name": widget.name,
                                    "widget classname": widget.className(),
                                    "position": widgetPos_mainWindow,
                                    "size": widgetSize_mainWindow,
                                    "path": root }
        metadataJson.append(metadataJsonUpdate)
        with open(os.path.join("screenshot_new", "metadata.json"), "w", encoding='utf-8') as file:
            json.dump(metadataJson, file)
        return metadataJson


    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            slicer.app.processEvents()
            print("Boton izquierdo del mouse presionado en:", event.pos())
            widget = self.widgetAtPos(qt.QCursor().pos())
            if widget == self.last_widget:
                return False
               
            self.step = self.step + 1


            if event.modifiers() & QtCore.Qt.ControlModifier:
                print("Se presionó la tecla Ctrl")
                self.BorderWidget(widget, True)
                slicer.app.processEvents()
                time.sleep(0.5)  
                self.last_ctrl = True
            else:
                if self.last_ctrl:
                    print(self.last_ctrl)
                    self.metadata = self.screen_shot(widget, self.metadata, self.step)
                print("Ctrl key is NOT pressed")
                for child_widget in slicer.util.mainWindow().findChildren(qt.QWidget):
                    self.BorderWidget(child_widget, 0)
                self.BorderWidget(widget, True)
                slicer.app.processEvents()
                time.sleep(0.5)    
                self.metadata = self.screen_shot(widget, self.metadata, self.step)
                self.BorderWidget(widget, False)
                self.last_ctrl = False
            self.last_widget = widget


        return False
   
    def widgetAtPos(self, pos):
        widget = qt.QApplication.widgetAt(pos)
        print(widget)
        return widget
   
    def BorderWidget(self, widget, state):
        if state == True:
            stylesheet = """
                QWidget {
                    border: 2px solid pink;
                }
                """
            widget.setStyleSheet(stylesheet)
        else:
            widget.setStyleSheet(" ")




class TutorialMaker:
    def __init__(self):
        self.window = qt.QMainWindow()
        self.mouse_press_filter = None
        #self.label = qt.QLabel("Please, before starting the tutorial, choose the file you want to work with\n\n", self.window)
        self.label = qt.QLabel("Por favor antes de comenzar el tutorial, elige el archivo con el que quieres trabajar\n\n", self.window)
        self.label.setAlignment(qt.Qt.AlignCenter)
        self.label.setWordWrap(True)
       
        # self.tutorial_text = qt.QLabel("The recording of the tutorial has started.\n\n"
        #                                 "Use slicer as usual. In case you want to highlight more than two elements at the same time, use Ctrl + Mouse click.", self.window)
        self.tutorial_text = qt.QLabel("La grabación del tutorial ha iniciado.\n\n"
                                        "Utilice 3D Slicer de forma habitual. En caso de querer resaltar más de dos elemetos al mismo tiempo utilice Ctrl + clic del ratón.", self.window)

        self.tutorial_text.setAlignment(qt.Qt.AlignJustify | qt.Qt.AlignVCenter)
        self.tutorial_text.setWordWrap(True)
        self.tutorial_text.hide()
       
        #self.add_data_button = qt.QPushButton("Add Data", self.window)
        self.add_data_button = qt.QPushButton("Añadir datos", self.window)
        self.add_data_button.clicked.connect(self.on_add_data_clicked)
       
        #self.stop_tutorial_button = qt.QPushButton("Stop and save tutorial", self.window)
        self.stop_tutorial_button = qt.QPushButton("Terminar y guardar el tutorial", self.window)
        self.stop_tutorial_button.clicked.connect(self.on_stop)
        self.stop_tutorial_button.setStyleSheet("background-color: #000000;")
        self.stop_tutorial_button.hide()
       
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tutorial_text)
        self.layout.addWidget(self.add_data_button)
        self.layout.addWidget(self.stop_tutorial_button)
       
        self.widget = qt.QWidget()
        self.widget.setLayout(self.layout)
       
        self.window.setCentralWidget(self.widget)
        self.window.setWindowTitle("Tutorial Maker Tool")
        #self.window.setFixedSize(500, 200)
        self.window.show()




   
    def on_add_data_clicked(self):
        file_dialog = qt.QFileDialog()
        file_dialog.setFileMode(qt.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                print("Archivo seleccionado:", file_path)
                slicer.util.loadScene(file_path)
                self.add_data_button.hide()
                self.label.hide()
                self.tutorial_text.show()
                self.stop_tutorial_button.show()
                self.window.adjustSize()
                self.window.setStyleSheet("background-color: #8b0000;")
                # default parameters
                slicer.util.selectModule("Welcome")
                ConvencionalW=slicer.util.findChildren(None, className="QToolButton")[15].menu()
                ConvencionalW.actions()[0].trigger()
                slicer.util.mainWindow().showMaximized()
                # Crear la aplicación
                self.app = QtWidgets.QApplication.instance()
                # Crear el filtro de eventos del mouse
                self.mouse_press_filter = MousePressFilter()
                # Instalar el filtro de eventos en la aplicación
                self.app.installEventFilter(self.mouse_press_filter)
                # Remover el filtro de eventos de las ventanas a excluir


    def on_stop(self):
        print("Stopped and saved tutorial")
        #self.app.removeEventFilter(self.mouse_press_filter)
        # Keep a reference to the MousePressFilter instance
        if self.mouse_press_filter:
            self.app.removeEventFilter(self.mouse_press_filter)
        self.mouse_press_filter = None
        # Close the pop-up window
        self.window.close()


tutorial_maker = TutorialMaker()






