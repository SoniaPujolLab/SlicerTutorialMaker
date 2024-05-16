from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi 
from PyQt5.QtWidgets import QLabel, QWidget, QToolBar, QGridLayout, QTextEdit, QAction, QMenu, QFileDialog, QColorDialog, QSpinBox, QToolButton, QLineEdit, QWidgetAction
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QPen, QBrush, QColor, QColor, QPainterPath, QFont
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
import imutils
import cv2
import sys, os
import numpy as np
import json
import math

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__() 
        loadUi('Resources/UI/TutorialGUI_v2.ui', self)
        
        self.scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        
        # Agregar el QWidget al QScrollArea
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.my_text_edit = self.findChild(QTextEdit, "myTextEdit")
        self.my_text_edit.setEnabled(False)

        self.title_screen = self.findChild(QLineEdit, "lineEdit")

        self.scree_prev = -1
        self.screen_act = None
        self.prev_name = ""
        self.select_annt = ""

        self.rectangles = []
        self.anotations = []

        toolbar = QToolBar("File", self)
        toolbar2 = QToolBar("Actions", self)
        toolbar3 = QToolBar("Edit", self)

        self.action5 = QAction(QIcon('Resources/Icons/open.png'), "Open", self)
        toolbar.addAction(self.action5)

        self.action6 = QAction(QIcon('Resources/Icons/save.png'), "Save", self)
        toolbar.addAction(self.action6)

        self.action8 = QAction(QIcon('Resources/Icons/back.png'), "Undo", self)
        toolbar.addAction(self.action8)

        self.action9 = QAction(QIcon('Resources/Icons/del.png'), "Delete", self)
        toolbar.addAction(self.action9)

        self.action13 = QAction(QIcon('Resources/Icons/remove.png'), "Remove", self)
        toolbar.addAction(self.action13)
        
        self.action14 = QAction(QIcon('Resources/Icons/selec.png'), "Selection", self)
        self.action14.setCheckable(True)
        #toolbar2.addAction(self.action14)
        
        self.selected_id = None
        self.select_annt = False

        self.action1 = QAction(QIcon('Resources/Icons/act1.png'), "Square", self)
        self.action1.setCheckable(True)
        toolbar2.addAction(self.action1)

        self.action2 = QAction(QIcon('Resources/Icons/act2.png'), "Circle", self)
        self.action2.setCheckable(True)
        toolbar2.addAction(self.action2)

        self.action3 = QAction(QIcon('Resources/Icons/act3.png'), "Arrow", self)
        self.action3.setCheckable(True)
        toolbar2.addAction(self.action3)

        self.action4 = QAction(QIcon('Resources/Icons/act4.png'), "Icon", self)
        self.action4.setCheckable(True)
        # self.action4.setChecked(False)
        toolbar2.addAction(self.action4)

        self.action11 = QAction(QIcon('Resources/Icons/act5.png'), "Text", self)
        self.action11.setCheckable(True)
        toolbar2.addAction(self.action11)

        self.icons = {
            self.action1: {
                'active': QIcon('Resources/Icons/act1_p.png'),
                'inactive': QIcon('Resources/Icons/act1.png')
            },
            self.action2: {
                'active': QIcon('Resources/Icons/act2_p.png'),
                'inactive': QIcon('Resources/Icons/act2.png')
            },
            self.action3: {
                'active': QIcon('Resources/Icons/act3_p.png'),
                'inactive': QIcon('Resources/Icons/act3.png')
            },
            self.action4: {
                'active': QIcon('Resources/Icons/act4_p.png'),
                'inactive': QIcon('Resources/Icons/act4.png')
            },
            self.action11: {
                'active': QIcon('Resources/Icons/act5_p.png'),
                'inactive': QIcon('Resources/Icons/act5.png')
            },
            self.action14: {
                'active': QIcon('Resources/Icons/selec_p.png'),
                'inactive': QIcon('Resources/Icons/selec.png')
            }
        }

        self.action7 = QAction(QIcon('Resources/Icons/color.png'), "color", self)
        toolbar3.addAction(self.action7)

        self.valor = 3
        self.spin_box = QSpinBox()
        self.spin_box.setSuffix(" thick.")
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(15)
        self.spin_box.setSingleStep(1)
        self.spin_box.setValue(self.valor)
        toolbar3.addWidget(self.spin_box)
        self.spin_box.valueChanged.connect(self.actualizar_valor)

        self.action10 = QAction(QIcon('Resources/Icons/fill_u.png'), "Fill", self)
        self.action10.setCheckable(True)
        self.fill = False
        #self.action10.setChecked(False)
        toolbar3.addAction(self.action10)

        self.t_px = 13
        self.spin_box_txt = QSpinBox()
        self.spin_box_txt.setSuffix(" px")
        self.spin_box_txt.setMinimum(5)
        self.spin_box_txt.setMaximum(25)
        self.spin_box_txt.setSingleStep(1)
        self.spin_box_txt.setValue(self.t_px)
        toolbar3.addWidget(self.spin_box_txt)
        self.spin_box_txt.valueChanged.connect(self.actualizar_size)

        self.line_edit = QLineEdit()
        self.line_edit.setMaxLength(30)
        self.line_edit.setFixedWidth(250)
        self.widget_action = QWidgetAction(self)
        self.widget_action.setDefaultWidget(self.line_edit)
        toolbar3.addAction(self.widget_action)

        self.action12 = QAction(QIcon('Resources/Icons/image.png'), "Load icon", self)
        self.action12.setCheckable(True)
        toolbar3.addAction(self.action12)
        self.new_image = QPixmap(20, 20)
        self.dir_icon = None

        self.addToolBar(toolbar)
        self.addToolBar(toolbar2)
        self.addToolBar(toolbar3)

        self.actions = [self.action1, self.action2, self.action3, self.action4, self.action11, self.action14]
        for action in self.actions:
            action.triggered.connect(self.on_action_triggered)

        self.action5.triggered.connect(self.open_json_file)
        self.action6.triggered.connect(self.save_json_file)
        self.action7.triggered.connect(self.change_color)
        self.action8.triggered.connect(self.delete_annotation)
        self.action9.triggered.connect(self.delete_screen)
        self.action10.triggered.connect(self.fill_figures)
        self.action12.triggered.connect(self.load_icon)

        self.label_imagen.mousePressEvent = self.mouse_press_event
        self.label_imagen.mouseMoveEvent = self.mouse_move_event
        self.label_imagen.mouseReleaseEvent = self.mouse_release_event

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.start = None
        self.end = None

        label_width = 800  # Ancho deseado
        label_height = 500  # Alto deseado
        self.label_imagen.setFixedSize(label_width, label_height)
        self.background_image = QPixmap(label_width, label_height)
        self.background_image.fill(QtGui.QColor(255, 255, 255))
        
        self.label_imagen.setPixmap(self.background_image)

        self.pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.SolidLine)
        self.brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 50), QtCore.Qt.SolidPattern)
        self.drawRect = True

        self.selected_color = QtGui.QColor(0, 0, 0)
        self.action7.setIcon(self.createColorIcon(self.selected_color))
        
        self.my_text_edit.setEnabled(True)

    def open_json_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Archivos JSON (*.json)")
        file_dialog.exec()

        if file_dialog.result() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            with open(selected_file, "r", encoding='utf-8') as file:
                data = json.load(file)
                #print("Contenido del archivo JSON:")
                #print(data)
        
        self.load_all_images(data)
    
    def save_json_file(self):
        json_out = []
        title = 'Slicer4Minute Tutorial'
        authors = [
                "Sonia Pujol, Ph.D.",
                "Andras Lasso"
            ]
        description_tutorial = "This tutorial is a 4-minute introduction to Slicer."
        i = 0
        for x, y, z in zip(self.edit_screen, self.steps, self.widgets):
            print(x)
            print(len(self.anotations[i]))
            imagen = QImage()
            if not imagen.load(x):  # Reemplaza "imagen_original.png" con tu ruta de archivo
                print("Error al cargar la imagen.")
            if imagen.isNull():
                print("La imagen no se ha cargado correctamente.")
            painter = QPainter(imagen)
            for antts in self.anotations[i]:
                print(antts.tp)
                pen = QPen(antts.cl)
                pen.setWidth(antts.tk)
                painter.setPen(pen)
                painter.setBrush(Qt.NoBrush) if antts.fl == False else painter.setBrush(QBrush(antts.cl))
                if antts.tp == "rect":
                    painter.drawRect(QRect(antts.ip, antts.fp))
                elif antts.tp == "crcls":
                    painter.drawEllipse(antts.ip, self.Mdistance(antts.ip, antts.fp), self.Mdistance(antts.ip, antts.fp))
                elif antts.tp == "arwT":
                    painter.drawPath(self.arrowPath(antts.tp, antts.ip, antts.fp))
                elif antts.tp == "icon":
                    painter.drawImage(antts.ip, QImage(antts.tx))
                elif antts.tp == "text":
                    font_small = QFont("Arial", antts.tk)
                    painter.setFont(font_small)
                    painter.drawText(antts.ip.x(), antts.ip.y(), antts.tx)
            painter.end()
            path = x.replace("new_", "edit_")
            imagen.save(path)

            json_out.append({
                "action":z,
                #"description":description,
                "steps-to-follow": y.split('\n'),
                "image":path
            })
            i+=1
        
        data = {
                "title":title,
                "authors":authors,
                "description":description_tutorial,
                "instructions":json_out
            }
        
        print(data)
        with open("sample_edited.json", "w", encoding='utf-8') as outfile:json.dump(data, outfile)

    def change_color(self):
        # print('vamos a cambiar color')
        QColorDialog.setCustomColor(0,self.selected_color)
        color_dialog = QColorDialog()
        color_dialog.setCurrentColor(self.selected_color)
        color = color_dialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.sender().setIcon(self.createColorIcon(color))

    def createColorIcon(self, color):
        # Crear un icono de color sólido
        pixmap = QPixmap(20, 20)
        pixmap.fill(color)

        return QIcon(pixmap)
    
    def delete_annotation(self):
        if len(self.anotations[self.scree_prev]) != 0:
            self.anotations[self.scree_prev].pop()
        self.update()
    
    def delete_screen(self):
        print('delete_screen: ', self.scree_prev)
        index = self.scree_prev

        # Verificar si el índice está dentro del rango válido
        if 0 <= index < len(self.labels):
            label = self.labels[index]
            label.setParent(None)
            self.labels.remove(label)
            self.prev_name = ""
            
            # Borrar el elemento de las demas listas 

    def fill_figures(self):
        if self.fill == True:
            # print('is Checked change not Checked')
            self.action10.setChecked(False)
            self.fill = False
            self.action10.setIcon(QIcon('Resources/Icons/fill_u.png'))
        else:
            # print('is not Checked change Checked')
            self.action10.setChecked(True)
            self.fill = True
            self.action10.setIcon(QIcon('Resources/Icons/fill_p.png'))
    
    def load_icon(self):
        print('load_icon')
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Icons (*.png)")
        file_dialog.exec()

        if file_dialog.result() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            self.new_image = QImage(selected_file)
            self.dir_icon = selected_file
    
    def actualizar_valor(self, valor):
        # Actualiza el valor de self cuando el QSpinBox cambia
        self.valor = valor
    
    def actualizar_size(self, valor):
        self.t_px = valor

    def mouse_press_event(self, event):
        self.start = event.pos()
        if self.action1.isChecked():
            self.select_annt = "rect"
        elif self.action2.isChecked():
            self.select_annt = "crcls"
        elif self.action3.isChecked():
            self.select_annt = "arwT"
        elif self.action4.isChecked():
            self.select_annt = "icon"
            self.end = event.pos()    
        elif self.action11.isChecked():
            self.select_annt = "text"
            self.end = event.pos()        
        # elif self.action14.isChecked():
        #     self.select_annt = "select"
        #     # self.end = event.pos()   
        #     print('seleccionar elemento')
        #     if len(self.anotations[self.scree_prev])>0:
        #         for index, annotation in enumerate(self.anotations[self.scree_prev]):
        #             start_point = annotation.ip
        #             end_point = annotation.fp

        #             # Crear un QRect a partir de los puntos de inicio y fin de la anotación
        #             rect = QRect(start_point, end_point)
        #             if rect.contains(self.start):
        #                 self.selected_id = index
        #                 self.select_annt = True
        #                 print('se selecciono', self.selected_id)
        #                 # self.selected_annotation = annotation
        #                 # self.mouse_offset = self.start - start_point
        #                 self.border = QRect(self.anotations[self.scree_prev][self.selected_id].ip - QPoint(2, 2), self.anotations[self.scree_prev][self.selected_id].fp + QPoint(2, 2))
        #                 print('self.border',self.border)
        #                 self.border_n = self.border.normalize()
        #                 print('self.border_n',self.border_n)
        #                 square_size = 8
        #                 self.top_left = QRect(self.border_n.topLeft() - QPoint(square_size, square_size), QSize(square_size, square_size))
        #                 self.top_right = QRect(self.border_n.topRight() + QPoint(0, -square_size), QSize(square_size, square_size))
        #                 self.bottom_left = QRect(self.border_n.bottomLeft() + QPoint(-square_size, 0), QSize(square_size, square_size))
        #                 self.bottom_right = QRect(self.border_n.bottomRight(), QSize(square_size, square_size))
        #                 break

        else:
            print("Nada activado")
            
        self.update()

    def mouse_move_event(self, event):
        if self.action4.isChecked() or self.action11.isChecked():
            self.start = event.pos()
            self.end = event.pos()
        # elif self.action14.isChecked()
        else:
            self.end = event.pos()
        self.update()

    def mouse_release_event(self, event):
        if self.action4.isChecked():
            anotation = Notes(self.select_annt, self.start, self.end, self.selected_color, self.t_px, self.fill, self.dir_icon)
        elif self.action11.isChecked():
            anotation = Notes(self.select_annt, self.start, self.end, self.selected_color, self.t_px, self.fill, self.line_edit.text())
        else:
        #     if self.action1.isChecked():
        #         rect = QRect(self.start, self.end)
        #         print('rect',rect)
        #         x = rect.x()
        #         y = rect.y()
        #         width = rect.width()
        #         height = rect.height()
        #         print(x ,y ,width ,height)
        #         if width < 0:
        #             x += width
        #             width = abs(width)
        #         if height < 0:
        #             y += height
        #             height = abs(height)
        #         # Crear un nuevo QRect con valores positivos
        #         anotation = Notes(self.select_annt, QPoint(x,y), QPoint(x-width,y-height), self.selected_color, self.valor, self.fill)
        #     else:
            anotation = Notes(self.select_annt, self.start, self.end, self.selected_color, self.valor, self.fill)
        self.end = event.pos()
        
        # if self.action14.isChecked():
        #     None
        # else:
        self.anotations[self.scree_prev].append(anotation)
        
        self.start = None
        self.end = None
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        pixmap = self.label_imagen.pixmap()
        painter = QPainter(pixmap)
        painter.drawPixmap(self.label_imagen.rect(), self.background_image)  # Dibujar la imagen de fondo
        #self.anotations[self.scree_prev].append(QRect(self.start, self.end))
        #for rect in self.rectangles:
        for antts in self.anotations[self.scree_prev]:
            # print('annotations: ', antts.tp)
            pen = QPen(antts.cl)
            pen.setWidth(antts.tk)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush) if antts.fl == False else painter.setBrush(QBrush(antts.cl))
            if antts.tp == "rect":
                painter.drawRect(QRect(antts.ip, antts.fp))
            elif antts.tp == "crcls":
                painter.drawEllipse(antts.ip, self.Mdistance(antts.ip, antts.fp), self.Mdistance(antts.ip, antts.fp))
            elif antts.tp == "arwT":
                painter.drawPath(self.arrowPath(antts.tp, antts.ip, antts.fp))
            elif antts.tp == "icon":
                painter.drawImage(antts.ip, QImage(antts.tx))
            elif antts.tp == "text":
                font_small = QFont("Arial", antts.tk)
                painter.setFont(font_small)
                painter.drawText(antts.ip.x(), antts.ip.y(), antts.tx)
            
            # if self.select_annt == True:  # Selecciono una figura
            #     pen = QPen(QColor(250, 250, 250))
            #     pen.setStyle(Qt.DashLine)  # Estilo de línea punteada
            #     painter.setPen(pen)
            #     painter.drawRect(self.border_n)
            #     square_size = 5
            #     painter.setBrush(QBrush(QColor(250, 250, 250)))
            #     painter.drawRect(self.top_left)
            #     painter.drawRect(self.top_right)
            #     painter.drawRect(self.bottom_left)
            #     painter.drawRect(self.bottom_right)


        if self.start and self.end:
            pen = QPen(self.selected_color)
            pen.setWidth(self.valor)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush) if self.fill == False else painter.setBrush(QBrush(self.selected_color))
            if self.select_annt == "rect":
                painter.drawRect(QRect(self.start, self.end))
            elif self.select_annt == "crcls":
                painter.drawEllipse(self.start, self.Mdistance(self.start, self.end), self.Mdistance(self.start, self.end))
            elif self.select_annt == "arwT":
                painter.drawPath(self.arrowPath(self.select_annt, self.start, self.end))
            elif self.select_annt == "icon":
                painter.drawImage(self.start, QImage(self.dir_icon))
            elif self.select_annt == "text":
                font_small = QFont("Arial", self.t_px)
                painter.setFont(font_small)
                painter.drawText(self.start.x(), self.start.y(), self.line_edit.text())

    def figure_form(self, p_ini, p_fin):
        a1 = p_ini.x()
        a2 = p_ini.y()
        a3 = p_fin.x()
        a4 = p_fin.y()
        print(a1, a2, a3, a4)
        return QRect(p_ini, p_fin)

    def Mdistance(self, p1, p2):
        if p2 == None:
            p2 = QPoint(p1.x(), p1.y())
        d = abs(((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2) ** 0.5)
        return d
    
    def arrowPath(self, ty, p1, p2):
        path = QPainterPath()
        tip = abs(int((((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2) ** 0.5)/4))
        tip = tip if tip < 15 else 15
        x = p2.x() - p1.x()
        y = p2.y() - p1.y()
        if x >= 0 and y >= 0: # 4ro
            path.moveTo(p1)  # Punto de inicio
            path.lineTo(p2)
            pa1_x, pa1y = self.rotate_point((p1.x()-tip, p1.y()+tip), p1, self.angle(x, y)-90)
            pa2_x, pa2y = self.rotate_point((p1.x()+tip, p1.y()+tip), p1, self.angle(x, y)-90)
            path.moveTo(pa1_x, pa1y)
            path.lineTo(p1)
            path.lineTo(pa2_x, pa2y)
        elif x < 0 and y >= 0: # 3ro
            path.moveTo(p1)  # Punto de inicio
            path.lineTo(p2)
            pa1_x, pa1y = self.rotate_point((p1.x()-tip, p1.y()+tip), p1, self.angle(x, y)+180)
            pa2_x, pa2y = self.rotate_point((p1.x()-tip, p1.y()-tip), p1, self.angle(x, y)+180)
            path.moveTo(pa1_x, pa1y)
            path.lineTo(p1)
            path.lineTo(pa2_x, pa2y)
        elif x < 0 and y < 0: # 3ro
            path.moveTo(p1)  # Punto de inicio
            path.lineTo(p2)
            pa1_x, pa1y = self.rotate_point((p1.x()+tip, p1.y()-tip), p1, self.angle(x, y)+90)
            pa2_x, pa2y = self.rotate_point((p1.x()-tip, p1.y()-tip), p1, self.angle(x, y)+90)
            path.moveTo(pa1_x, pa1y)
            path.lineTo(p1)
            path.lineTo(pa2_x, pa2y)
        else: # 1ro
            path.moveTo(p1)  # Punto de inicio
            path.lineTo(p2)
            pa1_x, pa1y = self.rotate_point((p1.x()+tip, p1.y()-tip), p1, self.angle(x, y))
            pa2_x, pa2y = self.rotate_point((p1.x()+tip, p1.y()+tip), p1, self.angle(x, y))
            path.moveTo(pa1_x, pa1y)
            path.lineTo(p1)
            path.lineTo(pa2_x, pa2y)
        return path
    
    def angle(self, dx, dy):
        rad = math.atan2(dy, dx)
        deg = math.degrees(rad)
        return deg
    
    def rotate_point(self, point, center, angle):
        # Convertir el ángulo a radianes
        angle_rad = math.radians(angle)
        
        # Descomponer las coordenadas de los puntos
        x, y = point
        cx = center.x()
        cy = center.y()

        # Calcular las diferencias
        dx = x - cx
        dy = y - cy

        # Aplicar la rotación
        rotated_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
        rotated_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)

        # Calcular las nuevas coordenadas
        new_x = rotated_x + cx
        new_y = rotated_y + cy

        return int(new_x), int(new_y)


    def load_image(self, path):
        # print('Se va a cargar la imagen')
        image = cv2.imread(path)
        # cv2.imshow('original',image)
        frame = imutils.resize(image, width=800, height=800)

        lh, lw, lc = frame.shape
        self.label_imagen.setFixedSize(lw, lh)

        image2 = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0], QImage.Format_BGR888 ) 
        # self.label_imagen.setPixmap(QPixmap.fromImage(image2))
        self.background_image = QPixmap.fromImage(image2)
        self.label_imagen.setPixmap(self.background_image)
        #self.label_imagen.setFixedSize(self.label_imagen.pixmap().width(), self.label_imagen.pixmap().height())
        #self.original_pixmap = self.label_imagen.pixmap()
    
    def load_all_images(self, json_file):
        widget = self.scrollAreaWidgetContents
        # print('ScrollArea', widget)
        layout = widget.layout()
        #print('layout', layout)
        
        self.anotations = []
        self.images_list = []
        test = 4
        cont = 1
        self.labels = []
        self.steps = []
        self.edit_screen = []
        self.widgets = []

        while self.gridLayout.count():
            widget = self.gridLayout.itemAt(0).widget()
            self.gridLayout.removeWidget(widget)
            widget.deleteLater()

        for i in json_file:
            new_anotation = []
            path = i["path"]
            image = cv2.imread(path)
            print(path)
            cv2.rectangle(image, (i["position"]), (i["size"]), (0, 255, 255), 4)
            self.anotations.append(new_anotation)
            
            new_frame = imutils.resize(image, width=800, height=800)
            new_path = i["path"]
            cv2.imwrite(new_path, new_frame)
            # print(new_path)
            self.edit_screen.append(new_path)

            frame = imutils.resize(image, width=200, height=200)
            label = QLabel("QLabel {}".format(cont))
            label.setObjectName("QLabel_{}".format(cont))
            cont += 1
            image2 = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0], QImage.Format_BGR888 ) 
            label.setPixmap(QPixmap.fromImage(image2))
            label.mousePressEvent = lambda event, label=label: self.label_clicked(label)
            self.gridLayout.addWidget(label)
            self.labels.append(label)
            self.images_list.append(path)
            self.steps.append("")
            self.widgets.append("Instrucctión for " + i["widget name"])
        
        self.firts_screen()
        
    def firts_screen(self):
        self.scree_prev = 0
        path = self.edit_screen[self.scree_prev]
        self.load_image(path)
        self.my_text_edit.append(self.steps[self.scree_prev])
        self.title_screen.setText(self.widgets[self.scree_prev])
        label = self.gridLayout.itemAt(0).widget()
        label.setStyleSheet("border: 2px solid red;")
        self.prev_name = label.objectName()

    def label_clicked(self, label):
    # Esta función se llama cuando se hace clic en cualquier QLabel
        sender = self.sender()  # Obtiene la QLabel que envió la señal

        # Se actualiza el texto para cada uno de los screens
        if str(self.prev_name) != "":
            # Guardamos el texto del screenshot
            text = self.my_text_edit.toPlainText()
            self.steps[self.scree_prev] = text
            self.widgets[self.scree_prev] = self.title_screen.text()
            my_label = self.findChild(QLabel, self.prev_name)
            my_label.setStyleSheet("widget")

            # title = self.label_widget.text()
            # self.widgets[self.scree_prev] = title

            
            # Guardamos la screenshottitle_scren
            # path_save = self.edit_screen[self.scree_prev]
            # print('path_save',path_save)
            # pixmap = self.label_imagen.pixmap()
            # width = pixmap.width()
            # height = pixmap.height()
            # image = pixmap.toImage().convertToFormat(4)
            # buffer = image.bits().asstring(width * height * 4)
            # imagen_np = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 4))

            # cv2.imwrite(path_save, imagen_np)
        
        self.my_text_edit.clear()
        # Se carga el texto para cada uno de los screens
        self.my_text_edit.append(self.steps[self.labels.index(label)])

        # self.title_screen.clear()
        self.title_screen.setText(self.widgets[self.labels.index(label)])

        # print(f"Se hizo clic en la QLabel: {label.text()}")
        label.setStyleSheet("border: 2px solid red;")
        # print("ID de la QLabel:", self.labels.index(label))
        # print("Path de la Imagen:", self.images_list[self.labels.index(label)])
        path = self.edit_screen[self.labels.index(label)]
        self.load_image(path)
        self.my_text_edit.setEnabled(True)

        self.scree_prev = self.labels.index(label)
        # print('previo:',self.scree_prev)
        self.prev_name = label.objectName()
        # print('prev_name:', self.prev_name)

        #self.original_pixmap = self.label_imagen.pixmap()
    
    def on_action_triggered(self):
        sender = self.sender()
        # print(sender.objectName)
        for action, icons in self.icons.items():
            # print(action.objectName)
            if action is sender:
                # Activar QAction y cambiar su icono
                action.setChecked(True)
                action.setIcon(icons['active'])
            else:
                # Desactivar QAction y restaurar su icono original
                action.setChecked(False)
                action.setIcon(icons['inactive'])

class Notes:
    def __init__(self, tp, ip, fp, cl, tk, fl, tx=None):
        self.tp = tp    # type for annotation
        self.ip = ip    # inicial point
        self.fp = fp    # final point
        self.cl = cl    # color selected 
        self.tk = tk    # thickness and size
        self.fl = fl    # fill (boolean)
        self.tx = tx    # text and path image

    def metodo(self):
        print("Hola desde MiClase")

def main():
    app = QApplication(sys.argv)
    my_app = MyApp()
    json_file = [
        {
            'widget name': '', 
               'position': [13, 23], 
            'size': [31, 30], 
            'path': 'Resources/Images/wall.png'
        }
        ]

    my_app.load_all_images(json_file)
    my_app.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

#call it anyway for now
main()


