import slicer
import qt
import json
import math
import os
from Lib.tmLabel import tmLabel
from Lib.Anotations import Notes
from Lib.FileMDHTML import markdownHTMLCreator
import Lib.painter as AnnotationPainter
from slicer import qMRMLWidget

class TutorialGUI(qt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.rectangles = []
        self.selected_id = None
        self.select_annt = False

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.start = None
        self.end = None

        self.drawing = False
        self.scree_prev = -1
        self.selected_color = qt.QColor(254, 254, 254)

        self.title = ""
        self.author = ""
        self.date = ""
        self.desc = ""

        self.output_name = "output"
        self.save_annotation = False

        self.metadata_image = None
        self.i_blank = 0

        # Load a UI file
        self.dir_path = os.path.dirname(__file__)
        self.uiWidget = slicer.util.loadUI(self.dir_path+'/../Resources/UI/ScreenshotAnnotator.ui')
        
        # Create a new accessible qt layout component
        self.newlayout = qt.QVBoxLayout()
        self.newlayout.setObjectName("uiWidget")

        # Create new toolbar
        self.addToolBar(self.create_toolbar_menu())
        self.addToolBar(self.create_toolbar_actions())
        self.addToolBar(self.create_toolbar_edit())

        # Add Widget from IU file to new layout
        self.newlayout.addWidget(self.uiWidget)

        # Set self layout with UI components 
        #self.setLayout(self.newlayout)
        self.setCentralWidget(self.uiWidget)

        width = 1250
        height = 780

        self.setFixedSize(width, height)

        children = self.uiWidget.children()
        # for child in children:
        #     print(child)

        self.scrollAreaWidgetContents = qt.QWidget()
        self.gridLayout = qt.QGridLayout(self.scrollAreaWidgetContents)
        
        # Add QWidget to QScrollArea
        self.uiWidget.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.imageslayout = qt.QVBoxLayout()

        self.scroll_area = self.uiWidget.findChild(qt.QScrollArea, "scrollArea")
        self.scroll_area.setFixedSize(315, 715) 

        label_width = 900  
        label_height = 530 
        self.label_image = self.uiWidget.findChild(qt.QLabel, "label_imagen")
        # print(type(self.label_image))
        self.label_image.setFixedSize(label_width, label_height)

        self.label_image.installEventFilter(self)
        self.label_image.setMouseTracking(True)

        self.background_image = qt.QPixmap(label_width, label_height)
        self.background_image.fill(qt.QColor(255, 255, 255))
        
        self.line_edit = self.uiWidget.findChild(qt.QLineEdit, "lineEdit")
        self.line_edit.setMinimumWidth(label_width)
        self.line_edit.setMaximumWidth(label_width) 

        self.text_edit = self.uiWidget.findChild(qt.QTextEdit, "myTextEdit")
        self.text_edit.setFixedSize(label_width, 150)

    def eventFilter(self, obj, event):
        if obj == self.label_image:
            if event.type() == qt.QEvent.MouseButtonPress:
                self.mouse_press_event(event)
            elif event.type() == qt.QEvent.MouseMove:
                self.mouse_move_event(event)
            elif event.type() == qt.QEvent.MouseButtonRelease:
                self.mouse_release_event(event)
        return False

    def create_toolbar_menu(self):
        toolbar = qt.QToolBar("File", self)

        actionOpen = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/open.png'), "Open", self)
        actionSave = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/save.png'), "Save", self)
        actionBack = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/back.png'), "Undo", self)
        actionDelete = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/remove.png'), "Delete", self)
        actionAdd = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/add.png'), "Add", self)
        # actionSelect = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/selec.png'), "Selection", self)
        # actionSelect.setCheckable(True)

        toolbar.addAction(actionOpen)
        toolbar.addAction(actionSave)
        toolbar.addAction(actionBack)
        toolbar.addAction(actionDelete)
        toolbar.addAction(actionAdd)
        # toolbar.addAction(actionSelect)

        actionOpen.triggered.connect(self.open_json_file_dialog)
        actionSave.triggered.connect(self.save_json_file)
        actionBack.triggered.connect(self.delete_annotation)
        actionDelete.triggered.connect(self.delete_screen)
        actionAdd.triggered.connect(self.add_page)
        # actionSelect.triggered.connect(self.fill_figures)

        toolbar.setMovable(True)
        return toolbar
    
    def create_toolbar_actions(self):
        toolbar = qt.QToolBar("Actions", self)
        
        self.square = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act1.png'), "Square", self)
        self.square.setCheckable(True)
        toolbar.addAction(self.square)

        self.circle = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act2.png'), "Circle", self)
        self.circle.setCheckable(True)
        #toolbar.addAction(self.circle)

        self.clck = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/pointer.png'), "Click", self)
        self.clck.setCheckable(True)
        toolbar.addAction(self.clck)

        self.arrow = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act3.png'), "Arrow", self)
        self.arrow.setCheckable(True)
        toolbar.addAction(self.arrow)

        self.icon_image = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act4.png'), "Icon", self)
        self.icon_image.setCheckable(True)
        # toolbar.addAction(self.icon_image)

        self.in_text = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act5.png'), "Text", self)
        self.in_text.setCheckable(True)
        # toolbar.addAction(self.in_text)

        # self.select = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/selec.png'), "Selection", self)
        # self.select.setCheckable(True)
        # toolbar.addAction(self.select)  

        self.icons = {
            self.square: {
                'active': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act1_p.png'),
                'inactive': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act1.png')
            },
            self.circle: {
                'active': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act2_p.png'),
                'inactive': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act2.png')
            },
            self.clck: {
                'active': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/pointer_p.png'),
                'inactive': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/pointer.png')
            },
            self.arrow: {
                'active': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act3_p.png'),
                'inactive': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act3.png')
            },
            self.icon_image: {
                'active': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act4_p.png'),
                'inactive': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act4.png')
            },
            self.in_text: {
                'active': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act5_p.png'),
                'inactive': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/act5.png')
            },
            # self.select: {
            #     'active': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/selec_p.png'),
            #     'inactive': qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/selec.png')
            # }
        }

        self.toolbar_actions = [self.square, self.circle, self.clck, self.arrow, self.icon_image, self.in_text] #, self.select]
        for a in self.toolbar_actions:
            # print(a)
            a.triggered.connect(lambda checked, a=a: self.on_action_triggered(a))

        toolbar.setMovable(True)
        return toolbar
    
    def create_toolbar_edit(self):
        toolbar = qt.QToolBar("Edit", self)
        
        self.action7 = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/color.png'), "color", self)
        toolbar.addAction(self.action7)
        self.action7.triggered.connect(self.change_color)

        self.valor = 3
        self.spin_box = qt.QSpinBox()
        self.spin_box.setSuffix(" thick.")
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(15)
        self.spin_box.setSingleStep(1)
        self.spin_box.setValue(self.valor)
        toolbar.addWidget(self.spin_box)
        self.spin_box.valueChanged.connect(self.actualizar_valor)

        self.fill_annot = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/fill_u.png'), "Fill", self)
        self.fill_annot.setCheckable(True)
        self.fill = False
        toolbar.addAction(self.fill_annot)

        self.t_px = 13
        self.spin_box_txt = qt.QSpinBox()
        self.spin_box_txt.setSuffix(" px")
        self.spin_box_txt.setMinimum(5)
        self.spin_box_txt.setMaximum(25)
        self.spin_box_txt.setSingleStep(1)
        self.spin_box_txt.setValue(self.t_px)
        toolbar.addWidget(self.spin_box_txt)
        self.spin_box_txt.valueChanged.connect(self.actualizar_size)

        self.text_in = qt.QLineEdit()
        self.text_in.setMaxLength(70)
        self.text_in.setFixedWidth(560)
        self.widget_action = qt.QWidgetAction(self)
        self.widget_action.setDefaultWidget(self.text_in)
        toolbar.addAction(self.widget_action)

        self.load_icon = qt.QAction(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/image.png'), "Load icon", self)
        self.load_icon.setCheckable(True)
        #toolbar.addAction(self.load_icon)
        self.new_image = qt.QPixmap(20, 20)
        self.dir_icon = None
        self.open_icon()

        self.fill_annot.triggered.connect(self.fill_figures)
        self.load_icon.triggered.connect(self.open_icon)

        toolbar.setMovable(True)

        return toolbar
    
    def open_json_file_dialog(self):
        file_dialog = qt.QFileDialog()
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.exec()

        # Check the result of the file dialog
        if file_dialog.result() == qt.QFileDialog.Accepted:
            # The user selected a file
            selected_file = file_dialog.selectedFiles()[0]
            self.open_json_file(selected_file)
        else:
            # The user canceled the file dialog
            print("The user canceled the file dialog")

    def open_json_file(self, filepath):

        directory_path = os.path.dirname(filepath)
        # Read the data from the file
        with open(filepath, "r") as file:
            data = json.load(file)
        # print(data)
        self.load_all_images(data, directory_path)

    def delete_screen(self):
        pass

    def add_page(self):
        newListImages = self.images_list
        self.labels = []
        new_annotation = []
        new_annotation_json = []
        cont = 0
        
        pos = self.scree_prev
        new_path = self.dir_path+'/../Resources/NewSlide/white.png'

        # Insert new_path at position pos
        newListImages.insert(pos, new_path)
        self.metadata_list.insert(pos, [])
        self.annotations.insert(pos, new_annotation)
        self.annotations_json.insert(pos, new_annotation_json)
        self.steps.insert(pos, "")
        self.widgets.insert(pos, "")
        self.images_list = []

        while self.gridLayout.count():
            widget = self.gridLayout.itemAt(0).widget()
            self.gridLayout.removeWidget(widget)
            widget.deleteLater()

        for img in newListImages:
            print(img)
            try:
                image = qt.QImage(img)
            except Exception as e:
                print(f"An unexpected error occurred while opening file '{image}': {str(e)}")
                exception_occurred = True
                break

            new_size = qt.QSize(280, 165)
            scaled_image = image.scaled(new_size)
            pixmap = qt.QPixmap.fromImage(scaled_image)

            label = tmLabel("QLabel_{}".format(cont), cont)
            label.setObjectName("QLabel_{}".format(cont))
            label.clicked.connect(lambda index=cont: self.label_clicked(index))
            label.setPixmap(pixmap)

            self.gridLayout.addWidget(label)
            self.labels.append(label)
            self.images_list.append(img)
            
            cont += 1
        
        self.label_clicked(self.scree_prev)

    def create_blank_image(self, width, height, color=(255, 255, 255)):
        image = qt.QImage(width, height, qt.QImage.Format_RGB32)
        image.fill(qt.QColor("white"))
        return image

    def load_all_images(self, data, directory_path):
        self.annotations = []
        self.annotations_json = [] 
#        self.annotations_json = [] Enrique line
        self.images_list = []
        self.metadata_list = []
        cont = 0
        self.labels = []
        self.steps = []
        self.edit_screen = []
        self.widgets = []

        print("directory_path:",directory_path)
        self.title = data["title"]
        self.author = data["author"]
        self.date = data["date"]
        self.desc = data["desc"]

        while self.gridLayout.count():
            widget = self.gridLayout.itemAt(0).widget()
            self.gridLayout.removeWidget(widget)
            widget.deleteLater()

        exception_occurred = False
        # Load all directories for images and metadata
        for step in data["steps"]:
            # Load files 
            for m_data in step:
                new_annotation = []
                new_annotation_json = []
                path_image = directory_path+"/"+m_data["window"]
                path_meta = directory_path+"/"+m_data["metadata"]

                try:
                    with open(path_meta, 'r') as file:
                        content = file.read()
                    image = qt.QImage(path_image)
                except FileNotFoundError:
                    print(f"File '{path_meta}' was not found.")
                    exception_occurred = True   
                    break
                except IOError:
                    print(f"Could not open file '{path_meta}'.")
                    exception_occurred = True
                    break
                except Exception as e:
                    print(f"An unexpected error occurred while opening file '{path_image}': {str(e)}")
                    exception_occurred = True
                    break

                new_size = qt.QSize(280, 165)
                scaled_image = image.scaled(new_size)
                pixmap = qt.QPixmap.fromImage(scaled_image)

                label = tmLabel("QLabel_{}".format(cont), cont)
                label.setObjectName("QLabel_{}".format(cont))
                label.clicked.connect(lambda index=cont: self.label_clicked(index))
                label.setPixmap(pixmap)

                self.gridLayout.addWidget(label)
                self.labels.append(label)
                self.images_list.append(path_image)
                self.metadata_list.append(content)
                self.annotations.append(new_annotation)
                self.annotations_json.append(new_annotation_json)
                self.steps.append("")
                self.widgets.append("")
                cont += 1

            if exception_occurred:
                break
        #print(self.metadata_list)
        print('self.annotations')
        print(self.annotations)
        self.firts_screen()

    def firts_screen(self):
        self.scree_prev = 0
        path = self.images_list[self.scree_prev]
        self.load_image(path)
        self.line_edit.setText(self.widgets[self.scree_prev])
        self.text_edit.append(self.steps[self.scree_prev])
        label = self.labels[self.scree_prev]
        label.setStyleSheet("border: 2px solid red;")
        #self.prev_name = label.objectName()

    def label_clicked(self, index):
        print('index:',index)
        # Se actualiza el texto para cada uno de los screens
        if str(self.scree_prev) != -1:
            label = self.labels[self.scree_prev]
            label.setStyleSheet("border: 0px")
            # Save text
            text = self.text_edit.toPlainText()
            self.steps[self.scree_prev] = text
            text = self.line_edit.text
            self.widgets[self.scree_prev] = text
        
        self.text_edit.clear()

        # Load the image to viewer from qlabel selected
        label = self.labels[index]
        label.setStyleSheet("border: 2px solid red;")
        # print("ID de la QLabel:", self.labels.index(label))
        # print("Path de la Imagen:", self.images_list[self.labels.index(label)])
        path = self.images_list[index]
        self.load_image(path)
        self.metadata_image = self.metadata_list[index]
        self.line_edit.setText(self.widgets[index])
        self.text_edit.append(self.steps[index])
        # self.my_text_edit.setEnabled(True)
        # self.draw_annotations()
        self.scree_prev = index
        
        # print("Paint Annotations in ", self.scree_prev)
        # print(self.annotations[self.scree_prev])
        self.draw_annotations()

    def load_image(self, path):
        image = qt.QImage(path)
        x = image.width()
        y = image.height()
        
        label_width = self.label_image.width

        a = x / label_width
        z = y / a

        self.label_image.setFixedSize(label_width, z)

        new_size = qt.QSize(label_width, z)
        scaled_image = image.scaled(new_size, qt.Qt.KeepAspectRatio, qt.Qt.SmoothTransformation)
        pixmap = qt.QPixmap.fromImage(scaled_image)

        self.background_image = pixmap
        self.label_image.setPixmap(self.background_image)

    def showEvent(self, event):
        pass

    def mouse_press_event(self, event):
        #print('press_event', event)
        self.start = event.pos()
        self.save_annotation = True
        if self.square.isChecked():
            self.select_annt = "rect"
        elif self.circle.isChecked():
            self.select_annt = "crcls"
        elif self.arrow.isChecked():
            self.select_annt = "arwT"
        elif self.icon_image.isChecked():
            self.select_annt = "icon"
            self.end = event.pos()    
        elif self.in_text.isChecked():
            self.select_annt = "text"
            self.end = event.pos()   
        elif self.clck.isChecked():
            self.select_annt = "click"
            self.end = event.pos()   
        else:
            print("No select annotation")  

        # self.metadata_list[self.scree_prev] contend all widgets from scree_prev index
        if self.select_annt != False:
            self.calculate_annotation()

    def mouse_move_event(self, event):
        self.start = event.pos()
        self.save_annotation = False
        #print('press_event', event)
        if self.square.isChecked():
            self.select_annt = "rect"
        elif self.circle.isChecked():
            self.select_annt = "crcls"
        elif self.arrow.isChecked():
            self.select_annt = "arwT"
        elif self.icon_image.isChecked():
            self.select_annt = "icon"
            self.end = event.pos()    
        elif self.in_text.isChecked():
            self.select_annt = "text"
            self.end = event.pos()   
        elif self.clck.isChecked():
            self.select_annt = "click"
            self.end = event.pos()   
        else:
            pass
            #print("No select annotation")  

        # self.metadata_list[self.scree_prev] contend all widgets from scree_prev index
        if self.select_annt != False:
            self.calculate_annotation()

    def mouse_release_event(self, event):
        pass

    def calculate_annotation(self):
        widgets = self.metadata_list[self.scree_prev]
        # print("Old point: ", self.start)
        pnt_clk = self.map_point(self.start)
        # print("New point: ", pnt_clk)
        wdgts_match = self.find_widget(widgets, pnt_clk)
        wdgts_child = self.select_widget_child(wdgts_match)
        
        star = None
        end = None

        anotation = None
        if wdgts_child is not None:
            if self.select_annt == "rect":
                x_i,y_i = wdgts_child["position"]
                a,b = wdgts_child["size"]
                x_f = x_i + a
                y_f = y_i + b
                star = self.remap_point(qt.QPoint(x_i, y_i))
                end = self.remap_point(qt.QPoint(x_f, y_f))
                anotation = Notes(self.select_annt, star, end, self.selected_color, self.valor, self.fill)
            elif self.select_annt == "crcls":
                x_i, y_i = wdgts_child["position"]
                w, h = wdgts_child["size"]
                c_x = x_i + w / 2
                c_y = y_i + h / 2
                wdgts_child['center'] = [c_x, c_y]
                wdgts_child['radio'] = [x_i, y_i]
                star = self.remap_point(qt.QPoint(c_x, c_y))
                end = self.remap_point(qt.QPoint(x_i, y_i)) 
                anotation = Notes(self.select_annt, star, end, self.selected_color, self.valor, self.fill)
            elif self.select_annt == "click":
                x_i, y_i = wdgts_child["position"]
                w, h = wdgts_child["size"]
                offset_x = 3 * w // 4
                offset_y = 3 * h // 4
                c_x = x_i + offset_x
                c_y = y_i + offset_y
                star = self.remap_point(qt.QPoint(c_x, c_y))
                
                anotation = Notes(self.select_annt, star, end, self.selected_color, self.t_px, self.fill, self.dir_icon)
                wdgts_child['labelText'] = self.text_in.text
            elif self.select_annt == "arwT":
                x_i, y_i = wdgts_child["position"]
                w, h = wdgts_child["size"]

                top_left = (x_i, y_i)
                top_right = (x_i + w, y_i)
                bottom_left = (x_i, y_i + h)
                bottom_right = (x_i + w, y_i + h)

                top_center = (x_i + w / 2, y_i)
                bottom_center = (x_i + w / 2, y_i + h)
                left_center = (x_i, y_i + h / 2)
                right_center = (x_i + w, y_i + h / 2)

                click = self.map_point(self.start)

                m1 = (bottom_right[1] - top_left[1]) / (bottom_right[0] - top_left[0])
                b1 = top_left[1] - m1 * top_left[0]

                m2 = (bottom_left[1] - top_right[1]) / (bottom_left[0] - top_right[0])
                b2 = top_right[1] - m2 * top_right[0]
                
                distance = 100

                if click.y() > m1 * click.x() + b1 and click.y() > m2 * click.x() + b2:
                    # print ("1")
                    wdgts_child['labelPosition'] = 'down'
                    wdgts_child['position_tail'] = [bottom_center[0], bottom_center[1]+distance]
                    star = self.remap_point(qt.QPoint(bottom_center[0], bottom_center[1]))
                    end = self.remap_point(qt.QPoint(bottom_center[0], bottom_center[1]+distance))
                elif click.y() < m1 * click.x() + b1 and click.y() > m2 * click.x() + b2:
                    # print ("2")
                    wdgts_child['labelPosition'] = 'right'
                    wdgts_child['position_tail'] = [right_center[0]+distance, right_center[1]]
                    star = self.remap_point(qt.QPoint(right_center[0], right_center[1]))
                    end = self.remap_point(qt.QPoint(right_center[0]+distance, right_center[1]))
                elif click.y() < m1 * click.x() + b1 and click.y() < m2 * click.x() + b2:
                    # print ("3")
                    wdgts_child['labelPosition'] = 'top'
                    wdgts_child['position_tail'] = [top_center[0], top_center[1]-distance]
                    star = self.remap_point(qt.QPoint(top_center[0], top_center[1]))
                    end = self.remap_point(qt.QPoint(top_center[0], top_center[1]-distance))
                else:
                    # print ("4")
                    wdgts_child['labelPosition'] = 'left'
                    wdgts_child['position_tail'] = [left_center[0]-distance, left_center[1]]
                    star = self.remap_point(qt.QPoint(left_center[0], left_center[1]))
                    end = self.remap_point(qt.QPoint(left_center[0]-distance, left_center[1]))
                
                wdgts_child['labelText'] = self.text_in.text
                anotation = Notes(self.select_annt, star, end, self.selected_color, self.valor, self.fill, self.text_in.text)

            elif self.select_annt == "icon":
                pass
            elif self.select_annt == "text":
                pass
            else:
                pass
            
            if self.save_annotation == True:
                self.annotations[self.scree_prev].append(anotation)
                self.annotations_json[self.scree_prev].append(wdgts_child)
                # print("add annotatión on ", self.scree_prev, " screen")
                self.draw_annotations()
            else:
                self.draw_annotations()
                self.draw_preview(anotation)
            
    
    def find_widget(self, widgets_json, pnt_clk):
        w_match = []
        x = pnt_clk.x()
        y = pnt_clk.y()
        
        widgets = json.loads(widgets_json)

        for id, info in widgets.items():
            rect_x, rect_y = info["position"]
            rect_width, rect_height = info["size"]
            if rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height:
                # print("Widget ID:", id, " name:",info["name"])
                # print("path:",info["path"])
                # print("position:", info["position"], " size:",info["size"])
                w_match.append(info)
        
        return w_match
    
    def select_widget_child(self, all_widgets):
        last_wdgt = None
        for w in all_widgets:
            last_wdgt = w
        return last_wdgt

    def map_point(self, p):
        image = qt.QImage(self.images_list[self.scree_prev])
        x = image.width()
        y = image.height()
        
        label_width = self.label_image.width
        label_height = self.label_image.height

        print('image size:', x, y)
        print('label image size:', label_width, label_height)

        x_ratio = p.x() / label_width
        y_ratio = p.y() / label_height
        
        new_x = int(x * x_ratio)
        new_y = int(y * y_ratio)

        new_point = qt.QPoint(new_x, new_y)
        
        return new_point

    def remap_point(self, p):
        image = qt.QImage(self.images_list[self.scree_prev])
        x = image.width()
        y = image.height()

        label_width = self.label_image.width
        label_height = self.label_image.height

        print('image size:', x, y)
        print('label image size:', label_width, label_height)

        rel_x = p.x() / x
        rel_y = p.y() / y

        print('point:', p.x(), p.y())

        new_x = int(label_width * rel_x)
        new_y = int(label_height * rel_y)

        print('new point:', new_x, new_y)

        new_point = qt.QPoint(new_x, new_y)

        return new_point

    def draw_annotations(self):
        # print("Paint annotation on ", self.scree_prev)
        pixmap = self.label_image.pixmap
        # print("pixmap", pixmap)
        painter = qt.QPainter(pixmap)
        painter.drawPixmap(self.label_image.rect, self.background_image)
        # painter.setRenderHint(qt.QPainter.Antialiasing)

        for antts in self.annotations[self.scree_prev]:
            pen = qt.QPen(antts.cl)
            pen.setWidth(antts.tk)
            painter.setPen(pen)
            painter.setBrush(qt.QBrush()) if antts.fl == False else painter.setBrush(qt.QBrush(qt.QColor(antts.cl)))
            if antts.tp == "rect":
                painter.drawRect(qt.QRect(antts.ip, antts.fp))
            elif antts.tp == "crcls":
                painter.drawEllipse(antts.ip, self.Mdistance(antts.ip, antts.fp), self.Mdistance(antts.ip, antts.fp))
            elif antts.tp == "click":
                painter.drawImage(antts.ip, self.new_image)
            elif antts.tp == "arwT":
                painter.drawPath(self.arrowPath(antts.tp, antts.ip, antts.fp))
                pen = qt.QPen(qt.QColor(255, 255, 255))
                painter.setPen(pen)
                painter.setBrush(qt.QBrush(qt.QColor(255, 255, 255)))
                font_small = qt.QFont("Arial", 14)
                painter.setFont(font_small)
                if antts.ip.y() > antts.fp.y():
                    #print("La flecha apunta hacia abajo")
                    tb_i = qt.QPoint(antts.fp.x()-100, antts.fp.y()-20)
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+21, antts.tx)
                elif antts.ip.y() < antts.fp.y():
                    #print("La flecha apunta hacia arriba")
                    tb_i = qt.QPoint(antts.fp.x()-100, antts.fp.y())
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+19, antts.tx)
                elif antts.ip.x() > antts.fp.x():
                    #print("La flecha apunta hacia la derecha")
                    tb_i = qt.QPoint(antts.fp.x()-200, antts.fp.y()-10)
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+19, antts.tx)
                elif antts.ip.x() < antts.fp.x():
                    #print("La flecha apunta hacia la izquierda")
                    tb_i = qt.QPoint(antts.fp.x(), antts.fp.y()-10)
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+19, antts.tx)
            elif antts.tp == "icon":
                painter.drawImage(antts.ip, qt.QImage(antts.tx))
            elif antts.tp == "text":
                font_small = qt.QFont("Arial", antts.tk)
                painter.setFont(font_small)
                painter.drawText(antts.ip.x(), antts.ip.y(), antts.tx)
        
        painter.end()
        self.label_image.setPixmap(pixmap)

    def draw_preview(self, antt):
        #print("draw annotation preview:", antt.tp)
        pixmap = self.label_image.pixmap
        # print("pixmap", pixmap)
        painter = qt.QPainter(pixmap)
        painter.drawPixmap(self.label_image.rect, self.background_image)
        # painter.setRenderHint(qt.QPainter.Antialiasing)

        for antts in self.annotations[self.scree_prev]:
            pen = qt.QPen(antts.cl)
            pen.setWidth(antts.tk)
            painter.setPen(pen)
            painter.setBrush(qt.QBrush()) if antts.fl == False else painter.setBrush(qt.QBrush(qt.QColor(antts.cl)))
            if antts.tp == "rect":
                painter.drawRect(qt.QRect(antts.ip, antts.fp))
            elif antts.tp == "crcls":
                painter.drawEllipse(antts.ip, self.Mdistance(antts.ip, antts.fp), self.Mdistance(antts.ip, antts.fp))
            elif antts.tp == "click":
                painter.drawImage(antts.ip, self.new_image)
            elif antts.tp == "arwT":
                painter.drawPath(self.arrowPath(antts.tp, antts.ip, antts.fp))
                pen = qt.QPen(qt.QColor(255, 255, 255))
                painter.setPen(pen)
                painter.setBrush(qt.QBrush(qt.QColor(255, 255, 255)))
                font_small = qt.QFont("Arial", 14)
                painter.setFont(font_small)
                if antts.ip.y() > antts.fp.y():
                    #print("La flecha apunta hacia abajo")
                    tb_i = qt.QPoint(antts.fp.x()-100, antts.fp.y()-20)
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+21, antts.tx)
                elif antts.ip.y() < antts.fp.y():
                    #print("La flecha apunta hacia arriba")
                    tb_i = qt.QPoint(antts.fp.x()-100, antts.fp.y())
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+19, antts.tx)
                elif antts.ip.x() > antts.fp.x():
                    #print("La flecha apunta hacia la derecha")
                    tb_i = qt.QPoint(antts.fp.x()-200, antts.fp.y()-10)
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+19, antts.tx)
                elif antts.ip.x() < antts.fp.x():
                    #print("La flecha apunta hacia la izquierda")
                    tb_i = qt.QPoint(antts.fp.x(), antts.fp.y()-10)
                    tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                    painter.drawRect(qt.QRect(tb_i, tb_f))
                    pen = qt.QPen(qt.QColor(0, 0, 0))
                    painter.setPen(pen)
                    painter.drawText(tb_i.x(), tb_i.y()+19, antts.tx)
            elif antts.tp == "icon":
                painter.drawImage(antts.ip, qt.QImage(antts.tx))
            elif antts.tp == "text":
                font_small = qt.QFont("Arial", antts.tk)
                painter.setFont(font_small)
                painter.drawText(antts.ip.x(), antts.ip.y(), antts.tx)

        pen = qt.QPen(antt.cl)
        pen.setWidth(antt.tk)
        painter.setPen(pen)
        painter.setBrush(qt.QBrush()) if antt.fl == False else painter.setBrush(qt.QBrush(qt.QColor(antt.cl)))
        if antt.tp == "rect":
            painter.drawRect(qt.QRect(antt.ip, antt.fp))
        elif antt.tp == "crcls":
            painter.drawEllipse(antt.ip, self.Mdistance(antt.ip, antt.fp), self.Mdistance(antt.ip, antt.fp))
        elif antt.tp == "click":
            painter.drawImage(antt.ip, self.new_image)
        elif antt.tp == "arwT":
            painter.drawPath(self.arrowPath(antt.tp, antt.ip, antt.fp))
            pen = qt.QPen(qt.QColor(255, 255, 255))
            painter.setPen(pen)
            painter.setBrush(qt.QBrush(qt.QColor(255, 255, 255)))
            font_small = qt.QFont("Arial", 14)
            painter.setFont(font_small)
            if antt.ip.y() > antt.fp.y():
                #print("La flecha apunta hacia abajo")
                tb_i = qt.QPoint(antt.fp.x()-100, antt.fp.y()-20)
                tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                painter.drawRect(qt.QRect(tb_i, tb_f))
                pen = qt.QPen(qt.QColor(0, 0, 0))
                painter.setPen(pen)
                painter.drawText(tb_i.x(), tb_i.y()+21, antt.tx)
            elif antt.ip.y() < antt.fp.y():
                #print("La flecha apunta hacia arriba")
                tb_i = qt.QPoint(antt.fp.x()-100, antt.fp.y())
                tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                painter.drawRect(qt.QRect(tb_i, tb_f))
                pen = qt.QPen(qt.QColor(0, 0, 0))
                painter.setPen(pen)
                painter.drawText(tb_i.x(), tb_i.y()+19, antt.tx)
            elif antt.ip.x() > antt.fp.x():
                #print("La flecha apunta hacia la derecha")
                tb_i = qt.QPoint(antt.fp.x()-200, antt.fp.y()-10)
                tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                painter.drawRect(qt.QRect(tb_i, tb_f))
                pen = qt.QPen(qt.QColor(0, 0, 0))
                painter.setPen(pen)
                painter.drawText(tb_i.x(), tb_i.y()+19, antt.tx)
            elif antt.ip.x() < antt.fp.x():
                #print("La flecha apunta hacia la izquierda")
                tb_i = qt.QPoint(antt.fp.x(), antt.fp.y()-10)
                tb_f = qt.QPoint(tb_i.x()+200, tb_i.y()+20)
                painter.drawRect(qt.QRect(tb_i, tb_f))
                pen = qt.QPen(qt.QColor(0, 0, 0))
                painter.setPen(pen)
                painter.drawText(tb_i.x(), tb_i.y()+19, antt.tx)
        elif antt.tp == "icon":
            painter.drawImage(antt.ip, qt.QImage(antt.tx))
        elif antt.tp == "text":
            font_small = qt.QFont("Arial", antt.tk)
            painter.setFont(font_small)
            painter.drawText(antt.ip.x(), antt.ip.y(), antt.tx)
        
        painter.end()
        self.label_image.setPixmap(pixmap)

    def figure_form(self, p_ini, p_fin):
        a1 = p_ini.x()
        a2 = p_ini.y()
        a3 = p_fin.x()
        a4 = p_fin.y()
        print(a1, a2, a3, a4)
        return qt.QRect(p_ini, p_fin)

    def Mdistance(self, p1, p2):
        if p2 == None:
            p2 = qt.QPoint(p1.x(), p1.y())
        d = abs(((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2) ** 0.5)
        return d
    
    def arrowPath(self, ty, p1, p2):
        # print("p1:", p1, "  p2:" ,p2)
        path = qt.QPainterPath()
        tip = abs(int((((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2) ** 0.5)/4))
        tip = 10#tip if tip < 15 else 15
        x = p2.x() - p1.x()
        y = p2.y() - p1.y()
        # print("x:", x, "  y:" ,y)
        if x >= 0 and y >= 0: # 4ro
            path.moveTo(qt.QPointF(p1))  # Punto de inicio
            path.lineTo(qt.QPointF(p2))
            pa1_x, pa1y = self.rotate_point((p1.x()-tip, p1.y()+tip), p1, self.angle(x, y)-90)
            pa2_x, pa2y = self.rotate_point((p1.x()+tip, p1.y()+tip), p1, self.angle(x, y)-90)
            path.moveTo(pa1_x, pa1y)
            path.lineTo(qt.QPointF(p1))
            path.lineTo(pa2_x, pa2y)
        elif x < 0 and y >= 0: # 3ro
            path.moveTo(qt.QPointF(p1))  # Punto de inicio
            path.lineTo(qt.QPointF(p2))
            pa1_x, pa1y = self.rotate_point((p1.x()-tip, p1.y()+tip), p1, self.angle(x, y)+180)
            pa2_x, pa2y = self.rotate_point((p1.x()-tip, p1.y()-tip), p1, self.angle(x, y)+180)
            path.moveTo(pa1_x, pa1y)
            path.lineTo(qt.QPointF(p1))
            path.lineTo(pa2_x, pa2y)
        elif x < 0 and y < 0: # 3ro
            path.moveTo(qt.QPointF(p1)) # Punto de inicio
            path.lineTo(qt.QPointF(p2))
            pa1_x, pa1y = self.rotate_point((p1.x()+tip, p1.y()-tip), p1, self.angle(x, y)+90)
            pa2_x, pa2y = self.rotate_point((p1.x()-tip, p1.y()-tip), p1, self.angle(x, y)+90)
            path.moveTo(pa1_x, pa1y)
            path.lineTo(qt.QPointF(p1))
            path.lineTo(pa2_x, pa2y)
        else: # 1ro
            path.moveTo(qt.QPointF(p1))  # Punto de inicio
            path.lineTo(qt.QPointF(p2))
            pa1_x, pa1y = self.rotate_point((p1.x()+tip, p1.y()-tip), p1, self.angle(x, y))
            pa2_x, pa2y = self.rotate_point((p1.x()+tip, p1.y()+tip), p1, self.angle(x, y))
            path.moveTo(pa1_x, pa1y)
            path.lineTo(qt.QPointF(p1))
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

    def change_color(self):
        color_dialog = qt.QColorDialog()
        color_dialog.setCurrentColor(self.selected_color)
        if color_dialog.exec_():
            # Obtener el color seleccionado
            color = color_dialog.selectedColor()
            self.selected_color = color
            # self.sender().setIcon(self.createColorIcon(color))

    def createColorIcon(self, color):
        # Crear un icono de color sólido
        pixmap = qt.QPixmap(20, 20)
        pixmap.fill(color)

        return qt.QIcon(pixmap)
    
    def delete_annotation(self):
        # print("delete_annotation")
        if len(self.annotations[self.scree_prev]) != 0:
            self.annotations[self.scree_prev].pop()
            self.annotations_json[self.scree_prev].pop()
        self.draw_annotations()

    def fill_figures(self):
        if self.fill == True:
            # print('is Checked change not Checked')
            self.fill_annot.setChecked(False)
            self.fill = False
            self.fill_annot.setIcon(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/fill_u.png'))
        else:
            # print('is not Checked change Checked')
            self.fill_annot.setChecked(True)
            self.fill = True
            self.fill_annot.setIcon(qt.QIcon(self.dir_path+'/../Resources/Icons/ScreenshotAnnotator/fill_p.png'))

    def open_icon(self):
        # print('load_icon')
        selected_file = self.dir_path+'/../Resources/Icons/Painter/click_icon.png'
        self.new_image = qt.QImage(selected_file)
        self.new_image = self.new_image.scaled(20,30)  
        self.dir_icon = selected_file
        #print("self.dir_icon:", self.dir_icon)

    def actualizar_valor(self, valor):
        # Actualiza el valor de self cuando el QSpinBox cambia
        self.valor = valor
    
    def actualizar_size(self, valor):
        self.t_px = valor

    def on_action_triggered(self, sender):
        # print(sender)

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
    
    def set_output_name(self, filename):
        self.output_name = filename

    def save_json_file(self):
        # Create json file 
        self.label_clicked(self.scree_prev) # Enrique line
        print("Create json file")
        json_out = []
        data = {}

        for i, image in enumerate(self.images_list, start=1):
            annotations = []
            for annts, wdg in zip(self.annotations[i-1], self.annotations_json[i-1]):
                print("wdg ", wdg )
                color_rgb = f"{annts.cl.red()}, {annts.cl.green()}, {annts.cl.blue()}"
                if annts.tp == "rect":
                    annotation = { #Convert all to string
                        "path": wdg["path"],
                        "type": "rectangle",
                        "color": color_rgb, # (r,g,b)
                        "labelText":"", #text on annotation
                        "fontSize": "14", # size of text on annotions 14px 
                        #"offset": "()" # (x,y) distance bettewn center and text box
                    }
                elif annts.tp == "click":
                    annotation = {
                        "path": wdg["path"],
                        "type": "clickMark",
                        "labelText":"", #text on annotation
                        "fontSize": "14", # size of text on annotions 14px 
                        #"offset": "" # (x,y) distance bettewn center and text box
                    }
                elif annts.tp == "arwT":
                    pos_off = wdg["position_tail"]
                    annotation = {
                        "path": wdg["path"],
                        "type": "arrow",
                        "color": color_rgb,
                        "labelText": wdg["labelText"],
                        "fontSize": "14",
                        "direction_draw" : wdg["labelPosition"] #Enrique Line
                        #"offset": "({},{})".format(pos_off[0], pos_off[1]) # position tail
                    }
                # elif annts.tp == "textBox":
                #     annotation = {
                #         "type": "textBox",
                #         "color": color_rgb, #optional
                #         "labelText":"", #text on annotation
                #         "fontSize": "14", # size of text on annotions 14px
                #         "position": "(x,y)",
                #     }
                annotations.append(annotation)

            data[str(i)] = {
                #"image:":image,
                "slide_title":self.widgets[i-1],
                "slide_text": self.steps[i-1],
                "annotations":annotations
            }

        output_file_path = os.path.join(self.dir_path, '..', 'Outputs/Annotations', self.output_name + '.json')
        #print("Data", data)
        with open(output_file_path, 'w', encoding='utf-8') as archivo:
            json.dump(data, archivo, indent=4)


        # Create MD and HTML file
        tutorialName = "fourMin_tutorial"
        #Painter creates screenshot with annotations
        AnnotationPainter.ImageDrawer.StartPaint(os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/Annotations/"+tutorialName+".json")   
        
        # Crear markdown and html
        markdown_creator = markdownHTMLCreator()  # Instancia de la clase
        html_content = markdown_creator.markdown_to_html((os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/Annotations/"+tutorialName))
        #html_content = markdownHTMLCreator.markdown_to_html((os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/Annotations/"+tutorialName))  
      