import json
import slicer
import qt
import pyautogui
import re
import time


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    # Replace 'your_json_file_path.json' with the actual path to your JSON file
    json_file_path = 'C:/Users/Dell/AppData/Local/slicer.org/Slicer 5.4.0/screenshot_new/metadata.json'


    # Read the JSON file
    json_data = read_json_file(json_file_path)


    # Process the data
    for item in json_data:
        step = item['step']
        widget = item['wiget']
        widget_root = item['wiget root']
        widget_index = item['widget index']
        widget_type = item['widget type']
        widget_name = item['widget name']
        widget_classname = item['widget classname']
        position = item['position']
        size = item['size']
        screenshot_path = item['path']


        # Print the information for each item in the JSON
        print(f"Step: {step}")
        print(f"Widget: {widget}")
        print(f"Widget Root: {widget_root}")
        print(f"Widget Index: {widget_index}")
        print(f"Widget Type: {widget_type}")
        print(f"Widget Name: {widget_name}")
        print(f"Widget Classname: {widget_classname}")
        print(f"Position: {position}")
        print(f"Size: {size}")
        print(f"Screenshot Path: {screenshot_path}")
        print("\n")


        w = slicer.util.mainWindow()
        for name in widget_root.split("/"):
            match = re.search(r'(\d+)\s+(.+)', name)


            if match:
                index = match.group(1)  # Obtenemos el número encontrado en la cadena
                classname = match.group(2)   # Obtenemos el texto encontrado en la cadena
                w = slicer.util.findChildren(w, className = classname)[int(index)]
                print(w)
            else:
                w = slicer.util.findChild(w.parent(), name)
                print(w)


        stylesheet = """
                QWidget {
                    border: 2px solid pink;
                }
                """
            # w.setStyleSheet(stylesheet)
            # slicer.app.processEvents()
            # time.sleep(2)
            # w.setStyleSheet(" ")
       
        w.setStyleSheet(stylesheet)
        slicer.app.processEvents()
        time.sleep(2)
        w.setStyleSheet(" ")
        print("___________________________________")

