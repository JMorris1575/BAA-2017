from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os, os.path, sys, re

class Settings(QDialog):

    def __init__(self, main, parent=None):
        super(Settings, self).__init__(parent)
        self.main = main
        config = main.config
        print('parent = ', parent)
        self.setup(config)

    def setup(self, config):

        self.resize(QSize(400, 360))

        settingsWidget = QTabWidget(self)
        settingsLayout = QVBoxLayout(self)

        fileSettingsWidget = QWidget()
        fileWidgetLayout = QVBoxLayout(fileSettingsWidget)
        settingsWidget.addTab(fileSettingsWidget, 'Filename/Location')
        settingsWidget.setTabToolTip(0, 'Change the name, location and date inclusion of the image files.')

        dirLabel = QLabel('Directory:')
        dirLabel.setAlignment(Qt.AlignRight)
        current_path = os.path.abspath(config['imageStorage']['path'])
        self.dirEdit = QLineEdit()
        self.dirEdit.setWhatsThis('This is where your image file will be saved. You can type it in here or browse to' +
                              'the desired location by clicking on the Browse... button at the right.')
        self.dirEdit.setAlignment(Qt.AlignLeft)
        self.dirEdit.setText(current_path)
        self.dirEdit.setCursorPosition(0)
        self.dirEdit.editingFinished.connect(self.pathEdit)
        browseButton = QPushButton('Browse...')
        browseButton.clicked.connect(self.browse)
        dirLayout = QHBoxLayout()
        dirLayout.addWidget(dirLabel, 1)
        dirLayout.addWidget(self.dirEdit, 3)
        dirLayout.addWidget(browseButton, 0)
        fileWidgetLayout.addLayout(dirLayout)

        nameLabel = QLabel('Filename:')
        nameLabel.setAlignment(Qt.AlignRight)
        self.nameEdit = QLineEdit()
        self.nameEdit.setWhatsThis('This is the core part of the image filename. It can be prefixed with the current date.' +
                              'See below.')
        self.nameEdit.setAlignment(Qt.AlignLeft)
        self.nameEdit.setText(config['imageStorage']['basename'])
        self.nameEdit.editingFinished.connect(self.changeFilename)
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(nameLabel, 1)
        nameLayout.addWidget(self.nameEdit, 4)
        fileWidgetLayout.addLayout(nameLayout)

        dateLabel = QLabel('Date:')
        dateLabel.setAlignment(Qt.AlignRight)
        dateGroup = QGroupBox('Include in Filename?')
        dateGroup.setWhatsThis('This determines whether the date will be included in the filename to keep them' +
                               'separate and for archiving purposes.')
        yesButton = QRadioButton('Yes')
        noButton = QRadioButton('No')
        dateGroupLayout = QHBoxLayout()
        dateGroupLayout.addWidget(yesButton)
        dateGroupLayout.addWidget(noButton)
        if config['imageStorage']['useDate']:
            yesButton.setChecked(True)
        else:
            noButton.setChecked(True)
        dateGroup.setLayout(dateGroupLayout)
        dateLayout = QHBoxLayout()
        dateLayout.addWidget(dateLabel, 1)
        dateLayout.addWidget(dateGroup, 4)
        fileWidgetLayout.addLayout(dateLayout)

        formatLabel = QLabel('File Format:')
        formatLabel.setAlignment(Qt.AlignRight)
        formatGroup = QGroupBox('Select One:')
        formatGroup.setWhatsThis('This is where you select one of the three formats in which the image can be saved.')
        formatGroup.setMinimumWidth(200)
        jpgButton = QRadioButton('.jpg')
        pngButton = QRadioButton('.png')
        bmpButton = QRadioButton('.bmp')
        formatGroupLayout = QHBoxLayout()
        formatGroupLayout.addWidget(jpgButton)
        formatGroupLayout.addWidget(pngButton)
        formatGroupLayout.addWidget(bmpButton)
        fileFormat = config['imageStorage']['format']
        if fileFormat == 'jpg':
            jpgButton.setChecked(True)
        elif fileFormat == 'png':
            pngButton.setChecked(True)
        else:
            bmpButton.setChecked(True)
        formatGroup.setLayout(formatGroupLayout)
        formatLayout = QHBoxLayout()
        formatLayout.addWidget(formatLabel, 1)
        formatLayout.addWidget(formatGroup, 4)
        fileWidgetLayout.addLayout(formatLayout)
        fileWidgetLayout.addStretch(0)

        appearanceSettingsWidget = QWidget()
        lookLabel = QLabel('Look at me!')
        appearanceWidgetLayout = QVBoxLayout(appearanceSettingsWidget)
        appearanceWidgetLayout.addWidget(lookLabel)
        settingsWidget.addTab(appearanceSettingsWidget, 'Border/Titles')

        styleSettingsWidget = QWidget()
        seeLabel = QLabel('"I see" said the blind man.')
        styleWidgetLayout = QVBoxLayout(styleSettingsWidget)
        styleWidgetLayout.addWidget(seeLabel)
        settingsWidget.addTab(styleSettingsWidget, 'Styles')

        settingsLayout.addWidget(settingsWidget)

    @pyqtSlot()
    def pathEdit(self):
        """
        Obtains the path text from the sender and sends it on to self.changeDir()
        :return: None
        """
        path = self.sender().text()
        self.changeDir(path)

    def changeDir(self, path):
        """
        Checks whether the directory the user enters actually exists. If so, changes self.config accordingly
        :return: True if the directory is successfully changed, False otherwise
        """
        if os.path.exists(path):
            self.main.config['imageStorage']['path'] = path
            self.main.config_changed = True
        else:
            msg = "That path does not exist. Would you like me to create it for you?"
            response = QMessageBox.question(self, 'BAA Progress', msg)
            if response == QMessageBox.Yes:
                try:
                    os.mkdir(path)
                    self.main.config['imageStorage']['path'] = path
                    self.main.config_changed = True
                except:
                    print("Unexpected error in changeDir:", sys.exc_info()[0])

    def browse(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory', self.main.config['imageStorage']['path'])
        self.dirEdit.setText(path)
        self.changeDir(path)

    def changeFilename(self):
        filename = self.nameEdit.text()
        test = re.match(r'[\w]+', filename)
        if test.group() == filename:
            self.main.config['imageStorage']['basename'] = filename
            self.main.config_changed = True
        else:
            msg = 'Filenames can only contain letters, numbers, and the underscore (_). Please try again.'
            QMessageBox.information(self, 'BAA Progress', msg)
            self.nameEdit.setFocus()
            self.nameEdit.selectAll()








