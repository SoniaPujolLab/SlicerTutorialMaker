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

    def draw_rectangle(self, x, y, width, height, text="", font_size=12, text_color=qt.Qt.black,
                    pen_color=qt.Qt.black, pen_width=10, pen_style=qt.Qt.SolidLine):
        if self.view is None:
            print("Error: Load an image first.")
            return

        # Create a QGraphicsRectItem (rectangle) and add it to the scene
        rectangle = qt.QGraphicsRectItem(x, y, width, height)
        rectangle.setPen(qt.QPen(pen_color, pen_width, pen_style))
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


    def draw_arrow(self, start_x, start_y, end_x, end_y, color=qt.Qt.black, pen_width=4, head_size=20, offset=5 , text="" ,
                                    font_size=12, text_color=qt.Qt.black):
        if self.view is None:
            print("Error: Load an image first.")
            return

        # Create a QLineF representing the arrow line
        arrow_line = qt.QLineF(start_x, start_y, end_x, end_y)

        # Create a QGraphicsLineItem (arrow line) and add it to the scene
        line_item = qt.QGraphicsLineItem(arrow_line)
        line_item.setPen(qt.QPen(color, pen_width))
        self.scene.addItem(line_item)

        # Calculate the direction of the arrow
        direction = arrow_line.unitVector()

        # Calculate the position for arrowhead with offset
        arrowhead_pos = qt.QPointF(end_x - (direction.dx() * (head_size + offset)),
                                   end_y - (direction.dy() * (head_size + offset)))

        # Calculate points for the arrowhead polygon (triangle) with offset
        arrowhead_polygon = qt.QPolygonF()
        arrowhead_polygon.append(qt.QPointF(arrowhead_pos.x() + direction.dy() * head_size,
                                           arrowhead_pos.y() - direction.dx() * head_size))
        arrowhead_polygon.append(qt.QPointF(arrowhead_pos.x() - direction.dy() * head_size,
                                           arrowhead_pos.y() + direction.dx() * head_size))
        arrowhead_polygon.append(qt.QPointF(end_x, end_y))  # Agregar punto final para conectar

        # Create a QGraphicsPolygonItem (arrowhead) and add it to the scene
        arrowhead_item = qt.QGraphicsPolygonItem(arrowhead_polygon)
        arrowhead_item.setPen(qt.QPen(color, pen_width))
        arrowhead_item.setBrush(qt.QBrush(color))
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
            text_background = qt.QGraphicsRectItem(start_x - text_rect.width()/2 , start_y - 20 , text_rect.width(), text_rect.height() + 5)

            text_background.setBrush(qt.QBrush(qt.Qt.white))
            self.scene.addItem(text_background)

            # Set the position of the text on top of the background rectangle
            text_item.setPos(start_x - text_rect.width()/2 , start_y - 20)
            self.scene.addItem(text_item)



    def draw_click(self,x,y, text="", font_size=12, text_color=qt.Qt.black):
        if self.view is None:
            print("Error: Load an image first.")
            return   
        path =  os.path.dirname(slicer.util.modulePath("TutorialMaker")) + '/Resources/Icons/Painter/click_icon.png'
        icon_pixmap = qt.QPixmap(path).scaledToWidth(30)
        #icon_pixmap.invertPixels()  
        icon_item = qt.QGraphicsPixmapItem(icon_pixmap)
        icon_item.setPos(x,y)
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
            text_background = qt.QGraphicsRectItem(x + bounding_box.width() , y + bounding_box.height() , text_rect.width(), text_rect.height() + 5)

            text_background.setBrush(qt.QBrush(qt.Qt.white))
            self.scene.addItem(text_background)

            # Set the position of the text on top of the background rectangle
            text_item.setPos(x + bounding_box.width() , y + bounding_box.height())
            self.scene.addItem(text_item)
   

    def save_to_png(self, filename):
        if self.view is not None:
            # Utilizar una ruta dinámica para guardar el archivo
            dynamic_path = os.path.join(os.getcwd(), filename)
            # Grab the contents of the view and save it to a PNG file
            image = self.view.showFullScreen()
            image = self.view.grab()
            image.save(dynamic_path, "PNG")
            self.view.close()
            #print(f"Image saved to {dynamic_path}")
        else:
            print("Error: No view to save.")

    # screenshotData: all widgets in a json
    # metadata: Victors' outputs

    #TODO: In that moment we will remove the translation and only show in English
        # after define the infrastructre with Weblate or GitHub we will use community translation
    def painter(self, metadata, screenshotData, language ):
        
        """import ast

        #import pip
        #pip.main(['install', 'fuzzywuzzy', 'transformers','torch','pandas', 'sacremoses','SentecePiece','python-Levenshtein'])
        import pandas as pd
        from fuzzywuzzy import process
        from transformers import MarianMTModel, MarianTokenizer"""

        #path_data_translation =  os.path.dirname(slicer.util.modulePath("TutorialMaker")) + '/Outputs/Translation/data/string_en_to_es.csv'

        # Translation variable#
        """if language == 'es':
            df_sourcetext = pd.read_csv(path_data_translation, encoding='UTF-16', sep=';')
            model_name = "Helsinki-NLP/opus-mt-en-es"
            model = MarianMTModel.from_pretrained(model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            col_name = 'Espanol'"""

        # Translation variable#

        scale = 1

        for item in metadata['annotations']:
            translated_text = ""
            widgetPosX = 0
            widgetPosY = 0
            widgetSizeX = 0
            widgetSizeY = 0
            for widget in screenshotData:
                if widget["path"] == item["path"]:
                    widgetPosX = widget["position"][0]
                    widgetPosY = widget["position"][1]
                    widgetSizeX = widget["size"][0]
                    widgetSizeY = widget["size"][1]
                    
                    ## translation process ##
                    # Check if there are some words on the already translated on database
                    original_text = item['labelText']
                    """similar_text, score, value = process.extractOne(original_text, df_sourcetext['English'])
                    match_text = original_text
                    # Check if the tranformers translation is the same that database translation (needs for transalation performance)
                    if score >= 70:
                        input_ids = tokenizer.encode(similar_text, return_tensors="pt", truncation=True)
                        translation = model.generate(input_ids, max_length=50, num_beams=5, length_penalty=0.6)
                        similar_text_trans = tokenizer.decode(translation[0], skip_special_tokens=True).lower()
                        original_text_trans =  df_sourcetext.loc[df_sourcetext['English'] == similar_text, 'Espanol'].values[0].lower()
                    # Improve performance with button names 
                        if (original_text_trans != similar_text_trans):
                            match_text = original_text.replace(similar_text,original_text_trans)
                             # Check if the translated text appears before "button" and after the original text
                            if match_text.find(original_text_trans) != -1 and match_text.find("button") != -1 and match_text.find(similar_text_trans) < match_text.find("button"):
                                match_text = match_text.replace("button","")
                                match_text = match_text.replace(original_text_trans, "el botón " + original_text_trans)

                    # Final translation        
                    input_ids = tokenizer.encode(match_text, return_tensors="pt", truncation=True)
                    translation = model.generate(input_ids, max_length=50, num_beams=5, length_penalty=0.6)
                    translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
                    translated_text = translated_text.replace(";", "\n")"""
                    translated_text = original_text
                    print(translated_text)
                    ## translation process ##                                    
                    break

            if item['type'] == 'rectangle':
                self.draw_rectangle(x = widgetPosX ,
                                    y = widgetPosY,
                                    width = widgetSizeX * scale,
                                    height = widgetSizeY * scale,
                                    text =  translated_text,
                                    font_size= float(item['fontSize']),
                                    text_color=qt.Qt.black,
                                    pen_color=qt.Qt.black,
                                    pen_width=10, 
                                    pen_style=qt.Qt.SolidLine)


            elif item['type'] == 'arrow':
                self.draw_arrow(widgetPosX + (widgetSizeX/2) * scale,
                                widgetPosY + 100 ,
                                widgetPosX + (widgetSizeX/2) * scale,
                                widgetPosY + (widgetSizeY/2) * scale, 
                                color=qt.Qt.red, 
                                pen_width=5,
                                head_size=20,
                                offset=5,
                                text =  translated_text,
                                font_size= float(item['fontSize']),
                                text_color=qt.Qt.black)
                
            elif item['type'] == 'clickMark':
                self.draw_click(x=widgetPosX + (widgetSizeX/2) * scale,
                                y=widgetPosY + (widgetSizeY/2) * scale,
                                text =  translated_text,
                                font_size= float(item['fontSize']),
                                text_color=qt.Qt.black,)

    def StartPaint(path):
        import json
        # Example usage: 

        image_drawer = ImageDrawer()

        import Lib.utils as utils

        jsonHandler = utils.JSONHandler()

        tutorial = jsonHandler.parseTutorial(True)
        OutputAnnotator = utils.JSONHandler.parseJSON(path)


        for i, annotateSteps in enumerate(OutputAnnotator):
            screenshot = tutorial.steps[i].getImage()
            screenshotData = tutorial.steps[i].getWidgets()
            # Load the image
            image_drawer.load_image(screenshot)
            image_drawer.painter(OutputAnnotator[annotateSteps], screenshotData, 'es')


            # Save the view to a PNG file with a dynamic path
            image_drawer.save_to_png(os.path.dirname(slicer.util.modulePath("TutorialMaker")) + '/Outputs/Translation/output_image_' + str(i) + '.png')
            
            pass

