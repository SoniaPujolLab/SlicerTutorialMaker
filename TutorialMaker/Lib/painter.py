import qt
import slicer
import os

class ImageDrawer:
    def __init__(self):
        self.image_path = None
        self.pixmap_item = None
        self.scene = None
        self.view = None

    def load_image(self, pixmap):
        # Create a QGraphicsPixmapItem from the QPixmap
        self.pixmap_item = qt.QGraphicsPixmapItem(pixmap)

        # Create a QGraphicsScene and add the item to it
        self.scene = qt.QGraphicsScene()
        self.scene.addItem(self.pixmap_item)

        # Create a QGraphicsView and set the scene
        self.view = qt.QGraphicsView(self.scene)

        # Show the QGraphicsView
        self.view.show()

    def draw_rectangle(self, x, y, width, height, text, font_size, color, text_color=qt.Qt.black, pen_width=5, pen_style=qt.Qt.SolidLine):
        if self.view is None:
            print("Error: Load an image first.")
            return

        # Create a QGraphicsRectItem (rectangle) and add it to the scene
        rectangle = qt.QGraphicsRectItem(x, y, width, height)
        pen = qt.QPen(qt.QColor.fromRgb(*color)); pen.setWidth(pen_width); pen.setStyle(pen_style)
        rectangle.setPen(pen)
        self.scene.addItem(rectangle)

        # Add text below the rectangle
        if text:
            # Create a background rectangle for the text
            text_item = qt.QGraphicsTextItem(text)
            text_item.setDefaultTextColor(text_color)
            font = qt.QFont()
            font.setPixelSize(font_size)
            text_item.setFont(font)

            # Calculate the background size based on the text size
            text_rect = text_item.boundingRect()
            text_background = qt.QGraphicsRectItem(x + width / 2 - text_rect.width() / 2, y + height + 5, text_rect.width(), text_rect.height() + 5)

            text_background.setBrush(qt.QBrush(qt.Qt.white))
            self.scene.addItem(text_background)

            # Set the position of the text on top of the background rectangle
            text_item.setPos(x + width / 2 - text_rect.width() / 2, y + height + 5)
            self.scene.addItem(text_item)


    def draw_arrow(self, sizex, sizey, start_x, start_y, end_x, end_y, direction_draw , color, text, font_size, pen_width=4, head_size=20, offset=5, text_color=qt.Qt.black):
        if self.view is None:
            print("Error: Load an image first.")
            return

        # Create a QLineF representing the arrow line
        if direction_draw == 'down':
            offset_x = 0;offset_y = 110;sizey = sizey;sizex = 0
            arrow_line = qt.QLineF(start_x, start_y + offset_y, end_x , end_y + sizey)
        elif direction_draw == 'down-left':
            offset_x = 0 - 100;offset_y = 110 + 100   ;sizey = sizey ;sizex = 0
            arrow_line = qt.QLineF(start_x -100, start_y + offset_y, end_x + sizex , end_y + sizey)
        elif direction_draw == 'down-right':
            offset_x = 0 + 100 ;offset_y = 110 + 100 ;sizey = sizey ;sizex = 0
            arrow_line = qt.QLineF(start_x +100, start_y + offset_y , end_x + sizex , end_y + sizey)
        elif direction_draw == 'top-left':
            offset_x = 0 - 100;offset_y = - 110 - 100   ;sizey = -sizey ;sizex = 0
            arrow_line = qt.QLineF(start_x -100, start_y + offset_y, end_x + sizex , end_y + sizey)
        elif direction_draw == 'top-right':
            offset_x = 0 + 100 ;offset_y = -110 - 100 ;sizey = -sizey ;sizex = 0
            arrow_line = qt.QLineF(start_x + 100, start_y + offset_y , end_x + sizex , end_y + sizey)
        elif direction_draw == 'top':
            offset_x = 0;offset_y = -100;sizey = -sizey;sizex = 0
            arrow_line = qt.QLineF(start_x, start_y + offset_y, end_x , end_y + sizey)
        elif direction_draw == 'left':
            sizex = -sizex;sizey = 0;offset_x = -200;offset_y = 0
            arrow_line = qt.QLineF(start_x + offset_x , start_y , end_x + sizex - 20 , end_y )
        elif direction_draw == 'right':
            sizex = sizex;sizey = 0;offset_x = 200;offset_y = 0
            arrow_line = qt.QLineF(start_x + offset_x , start_y , end_x + sizex + 20 , end_y )

        # Create a QGraphicsLineItem (arrow line) and add it to the scene
        line_item = qt.QGraphicsLineItem(arrow_line)
        pen = qt.QPen(qt.QColor.fromRgb(*color)); pen.setWidth(pen_width + 2)
        line_item.setPen(pen)
        self.scene.addItem(line_item)

        # Calculate the direction of the arrow
        direction_vector = arrow_line.unitVector()

        # Calculate the position for arrowhead with offset
        arrowhead_pos = qt.QPointF(end_x - (direction_vector.dx() * (head_size) - sizex ),
                                end_y - (direction_vector.dy() * (head_size) - sizey))

        # Calculate points for the arrowhead polygon (triangle) with offset
        arrowhead_polygon = qt.QPolygonF()
        arrowhead_polygon.append(qt.QPointF(arrowhead_pos.x() + direction_vector.dy() * head_size,
                                            arrowhead_pos.y() - direction_vector.dx() * head_size))
        arrowhead_polygon.append(qt.QPointF(arrowhead_pos.x() - direction_vector.dy() * head_size,
                                            arrowhead_pos.y() + direction_vector.dx() * head_size))
        arrowhead_polygon.append(qt.QPointF(end_x + sizex , end_y + (-offset_y*0.05) + sizey))  # Agregar punto final para conectar

        # Create a QGraphicsPolygonItem (arrowhead) and add it to the scene
        arrowhead_item = qt.QGraphicsPolygonItem(arrowhead_polygon)
        pen = qt.QPen(qt.QColor.fromRgb(*color)); pen.setWidth(pen_width - offset)
        arrowhead_item.setPen(pen)
        arrowhead_item.setBrush(qt.QBrush(qt.QColor.fromRgb(*color)))
        self.scene.addItem(arrowhead_item)

        if text:
            # Create a background rectangle for the text
            text_item = qt.QGraphicsTextItem(text)
            text_item.setDefaultTextColor(text_color)
            text_item.setPos(end_x, end_y)
            font = qt.QFont()
            font.setPixelSize(font_size)
            text_item.setFont(font)

            # Calculate the background size based on the text size
            text_rect = text_item.boundingRect()
            text_background = qt.QGraphicsRectItem(  start_x - text_rect.width()/2 + offset_x,
                                                     start_y - text_rect.height()/2 + offset_y,
                                                     text_rect.width(), 
                                                     text_rect.height() + 5)

            text_background.setBrush(qt.QBrush(qt.Qt.white))
            self.scene.addItem(text_background)

            # Set the position of the text on top of the background rectangle
            text_item.setPos( start_x - text_rect.width()/ 2 + offset_x,
                              start_y - text_rect.height()/2 + offset_y)
            self.scene.addItem(text_item)



    def draw_click(self, x, y, text, font_size, text_color=qt.Qt.black):
        if self.view is None:
            print("Error: Load an image first.")
            return
        path = os.path.dirname(slicer.util.modulePath("TutorialMaker")) + '/Resources/Icons/Painter/click_icon.png'
        icon_pixmap = qt.QPixmap(path).scaledToWidth(30)
        # icon_pixmap.invertPixels()
        icon_item = qt.QGraphicsPixmapItem(icon_pixmap)
        icon_item.setPos(x, y)
        self.scene.addItem(icon_item)
        bounding_box = icon_item.boundingRect()

        # Add text below the rectangle
        if text:
            # Create a background rectangle for the text
            text_item = qt.QGraphicsTextItem(text)
            text_item.setDefaultTextColor(text_color)
            font = qt.QFont()
            font.setPixelSize(font_size)
            text_item.setFont(font)

            # Calculate the background size based on the text size
            text_rect = text_item.boundingRect()
            text_background = qt.QGraphicsRectItem(x + bounding_box.width(), y + bounding_box.height(), text_rect.width(), text_rect.height() + 5)

            text_background.setBrush(qt.QBrush(qt.Qt.white))
            self.scene.addItem(text_background)

            # Set the position of the text on top of the background rectangle
            text_item.setPos(x + bounding_box.width(), y + bounding_box.height())
            self.scene.addItem(text_item)


    def save_to_png(self, filename):
        if self.view is not None:
            #print(filename)
            # Utilizar una ruta dinámica para guardar el archivo
            dynamic_path = os.path.join(os.getcwd(), filename)
            # Grab the contents of the view and save it to a PNG file
            image = self.view.showFullScreen()
            image = self.view.grab()
            image.save(dynamic_path, "PNG")
            self.view.close()
            # print(f"Image saved to {dynamic_path}")
        else:
            print("Error: No view to save.")

    # screenshotData: all widgets in a json
    # metadata: Victors' outputs

    # TODO: In that moment we will remove the translation and only show in English
    # after define the infrastructre with Weblate or GitHub we will use community translation
    def painter(self, metadata, screenshotData, language):
        scale = 1

        for item in metadata['annotations']:
            text_ann = ""
            widgetPosX = 0
            widgetPosY = 0
            widgetSizeX = 0
            widgetSizeY = 0

            for widget in screenshotData:
                if widget["path"] == item["path"]:
                    #print(item)
                    widgetPosX = widget["position"][0]
                    widgetPosY = widget["position"][1]
                    widgetSizeX = widget["size"][0]
                    widgetSizeY = widget["size"][1]
                    text_ann = item["labelText"]

            if item['type'] == 'rectangle':
                self.draw_rectangle(x=widgetPosX,
                                    y=widgetPosY,
                                    width=widgetSizeX * scale,
                                    height=widgetSizeY * scale,
                                    text=text_ann,
                                    font_size=int(item['fontSize']),
                                    text_color=qt.Qt.black,
                                    color=tuple(map(int, item["color"].split(', '))),
                                    pen_width=5,
                                    pen_style=qt.Qt.SolidLine)

            elif item['type'] == 'arrow':
                self.draw_arrow(direction_draw = item["direction_draw"],
                                sizex= (widgetSizeX / 2) * scale,
                                sizey= (widgetSizeY / 2) * scale,
                                start_x= widgetPosX + (widgetSizeX / 2) * scale,
                                start_y= widgetPosY + (widgetSizeY / 2) * scale,
                                end_x= widgetPosX + (widgetSizeX / 2) * scale,
                                end_y= widgetPosY + (widgetSizeY / 2) * scale,
                                color=tuple(map(int, item["color"].split(', '))),
                                pen_width=6,
                                head_size=20,
                                offset=5,
                                text=text_ann,
                                font_size=int(item['fontSize']),
                                text_color=qt.Qt.black)

            elif item['type'] == 'clickMark':
                self.draw_click(x=widgetPosX + (widgetSizeX / 2) * scale,
                                y=widgetPosY + (widgetSizeY / 2) * scale,
                                text=text_ann,
                                font_size=int(item['fontSize']),
                                text_color=qt.Qt.black)

    def StartPaint(path,ListPositionWhite, ListoTotalImages):
        import json
        # Example usage:

        image_drawer = ImageDrawer()

        import Lib.utils as utils

        jsonHandler = utils.JSONHandler()

        tutorial = jsonHandler.parseTutorial(True)
        OutputAnnotator = utils.JSONHandler.parseJSON(path)

        cont = 0
        imgSS = 0
        ListPositionWhite.sort()
        #print(ListPositionWhite)
        for i, annotateSteps in enumerate(OutputAnnotator): 
            #print(i)
            #print(imgSS)
            #if ListPositionWhite: #Is not empty
            #if( i ==  ListPositionWhite[cont]):
            if(ListoTotalImages[i] == -1):
            # print('Cont')
                
                #imgSS = cont
                #print('imgSS')
                
                #print(len(ListPositionWhite))
                if(cont < len(ListPositionWhite)-1):
                    cont = cont + 1
                #agregar imagen blanca y texto
            else: 
            
                screenshot = tutorial.steps[ListoTotalImages[i]].getImage()
                screenshotData = tutorial.steps[ListoTotalImages[i]].getWidgets()
                # Load the image
                image_drawer.load_image(screenshot)
                #print(screenshot)
                image_drawer.painter(OutputAnnotator[annotateSteps], screenshotData, 'es')

                # Save the view to a PNG file with a dynamic path
                image_drawer.save_to_png(
                    os.path.dirname(slicer.util.modulePath("TutorialMaker")) + '/Outputs/Translation/output_image_' + str(i) + '.png')
                
                imgSS = imgSS + 1 
                #print('Hola')
                #print(i)
            #if(cont != len(ListPositionWhite)-1):
            #  imgSS = imgSS + 1

                
            pass
            
