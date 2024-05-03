import sys
import ffmpeg

from PyQt5.QtWidgets import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Simple Media Converter'
        self.videoTypes = ['webm','mkv','flv','vob','gif','avi','mov','wmv','amv','mp4','m4v']
        self.soundTypes = ['flac','m4a','mp3','ogg','opus','wav']
        self.imageTypes = []
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createOpenFileLayout()
        self.createSaveFileLayout()
        
        self.combobox = QComboBox()
        self.combobox.currentTextChanged.connect(self.comboboxChanged)

        self.convertButton = QPushButton("Convert",self)
        self.convertButton.clicked.connect(self.convert)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.openFileGroupBox)
        mainLayout.addWidget(self.combobox)
        mainLayout.addWidget(self.saveFileGroupBox)
        mainLayout.addWidget(self.convertButton)
        self.setLayout(mainLayout)
        
        self.show()

    def createOpenFileLayout(self):
        self.openFileGroupBox = QGroupBox("File to be Converted")
        layout = QHBoxLayout()

        self.openFileTextBox = QLineEdit(self)
        self.openFileTextBox.setReadOnly(True)
        layout.addWidget(self.openFileTextBox)

        openFileButton = QPushButton("Open", self)
        openFileButton.clicked.connect(self.openFileNameDialog)
        layout.addWidget(openFileButton)

        self.openFileGroupBox.setLayout(layout)

    def createSaveFileLayout(self):
        self.saveFileGroupBox = QGroupBox("File to Convert to")
        layout = QHBoxLayout()

        self.saveFileTextBox = QLineEdit(self)
        layout.addWidget(self.saveFileTextBox)

        saveFileButton = QPushButton("Open", self)
        saveFileButton.clicked.connect(self.saveFileDialog)
        layout.addWidget(saveFileButton)

        self.saveFileGroupBox.setLayout(layout)
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.openFileTextBox.setText(fileName)

            self.populateComboBox(self.checkMediaType(fileName))
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.saveFileTextBox.setText(fileName)

    def checkMediaType(self, fileName):
        fileExtension = fileName.split(".")[-1]

        if fileExtension in self.videoTypes:
            return 'video'

    def populateComboBox(self, mediaType):
        self.combobox.clear()
        if mediaType == 'video':
            for i in self.videoTypes:
                self.combobox.addItem(i)
            for i in self.soundTypes:
                self.combobox.addItem(i)

    def comboboxChanged(self, text):
        print("combo box changed to: ", text)

        #one day I will find a not shit way to do this
        #string manipulation is not my strong suit
        split_up = self.openFileTextBox.text().split(".")
        split_up.pop()
        split_up.append(text)
        joined = split_up[0] + "." + split_up[1]
        self.saveFileTextBox.setText(joined)

    def convert(self):
        stream = ffmpeg.input(self.openFileTextBox.text())
        stream = ffmpeg.output(stream, self.saveFileTextBox.text())
        ffmpeg.run(stream)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
