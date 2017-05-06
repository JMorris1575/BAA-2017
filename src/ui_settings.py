from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os, os.path, sys

class Settings(QDialog):

    def __init__(self, config, parent=None):
        super(Settings, self).__init__(parent)
        self.config = config
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
        dirEdit = QLineEdit()
        dirEdit.setWhatsThis('This is where your image file will be saved. You can type it in here or browse to' +
                              'the desired location by clicking on the Browse... button at the right.')
        dirEdit.setAlignment(Qt.AlignLeft)
        dirEdit.setText(current_path)
        dirEdit.setCursorPosition(0)
        dirEdit.editingFinished.connect(self.changeDir)
        browseButton = QPushButton('Browse...')
        dirLayout = QHBoxLayout()
        dirLayout.addWidget(dirLabel, 1)
        dirLayout.addWidget(dirEdit, 3)
        dirLayout.addWidget(browseButton, 0)
        fileWidgetLayout.addLayout(dirLayout)

        nameLabel = QLabel('Filename:')
        nameLabel.setAlignment(Qt.AlignRight)
        nameEdit = QLineEdit()
        nameEdit.setWhatsThis('This is the core part of the image filename. It can be prefixed with the current date.' +
                              'See below.')
        nameEdit.setAlignment(Qt.AlignLeft)
        nameEdit.setText(config['imageStorage']['basename'])
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(nameLabel, 1)
        nameLayout.addWidget(nameEdit, 4)
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
    def changeDir(self):
        """
        Checks whether the directory the user enters actually exists. If so, changes self.config accordingly
        :return: True if the directory is successfully changed, False otherwise
        """
        path = self.sender().text()
        if os.path.exists(path):
            self.config['imageStorage']['path'] = path
        else:
            msg = "That path does not exist. Would you like me to create it for you?"
            response = QMessageBox.question(self, 'BAA Progress', msg)
            if response == QMessageBox.Yes:
                os.mkdir(path)
                try:
                    os.mkdir(path)
                    self.config['imageStorage']['path'] = path
                except:
                    print("Unexpected error in changeDir:", sys.exc_info()[0])






