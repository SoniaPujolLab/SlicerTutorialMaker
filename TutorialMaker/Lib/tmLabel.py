import qt

class tmLabel(qt.QLabel):
    clicked = qt.Signal()

    def __init__(self, text, index, parent=None):
        super(tmLabel, self).__init__(text, parent)
        self.index = index

    def mousePressEvent(self, event):
        #print(event)
        #print(f"Label {self.index} clicked!")
        self.clicked.emit()
        
