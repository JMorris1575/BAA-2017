from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os.path

class Settings(QDialog):

    def __init__(self, config, parent=None):
        super(Settings, self).__init__(parent)
        self.setup(config)

    def setup(self, config):

        self.resize(QSize(400, 360))

        settingsWidget = QTabWidget(self)
        settingsLayout = QVBoxLayout(self)

        fileSettingsWidget = QWidget()
        fileWidgetLayout = QGridLayout(fileSettingsWidget)
        settingsWidget.addTab(fileSettingsWidget, 'Filename/Location')
        settingsWidget.setTabToolTip(0, 'Change the name, location and date inclusion of the image files.')

        dirLabel = QLabel('Directory:')
        current_path = os.path.abspath(config['imageStorage']['path'])
        dirEdit = QLineEdit()
        dirEdit.setText(current_path)
        browseButton = QPushButton('Browse...')
        fileWidgetLayout.addWidget(dirLabel, 0, 0, Qt.AlignRight)
        fileWidgetLayout.addWidget(dirEdit, 0, 1, Qt.AlignLeft)
        fileWidgetLayout.addWidget(browseButton, 0, 2, Qt.AlignCenter)

        nameLabel = QLabel('Filename:')
        nameEdit = QLineEdit()
        nameEdit.setText(config['imageStorage']['basename'])
        fileWidgetLayout.addWidget(nameLabel, 1, 0, Qt.AlignRight)
        fileWidgetLayout.addWidget(nameEdit, 1, 1, Qt.AlignLeft)

        dateGroup = QGroupBox('Include Date?')
        yesButton = QRadioButton('Yes')
        noButton = QRadioButton('No')
        dateLayout = QVBoxLayout()
        dateLayout.addWidget(yesButton)
        dateLayout.addWidget(noButton)
        if config['imageStorage']['useDate']:
            yesButton.setChecked(True)
        else:
            noButton.setChecked(True)
        dateGroup.setLayout(dateLayout)
        fileWidgetLayout.addWidget(dateGroup, 2, 1, Qt.AlignCenter)

        formatGroup = QGroupBox('Image File Format:')
        jpgButton = QRadioButton('.jpg')
        pngButton = QRadioButton('.png')
        bmpButton = QRadioButton('.bmp')
        formatLayout = QVBoxLayout()
        formatLayout.addWidget(jpgButton)
        formatLayout.addWidget(pngButton)
        formatLayout.addWidget(bmpButton)
        fileFormat = config['imageStorage']['format']
        if fileFormat == 'jpg':
            jpgButton.setChecked(True)
        elif fileFormat == 'png':
            pngButton.setChecked(True)
        else:
            bmpButton.setChecked(True)
        formatGroup.setLayout(formatLayout)
        fileWidgetLayout.addWidget(formatGroup, 2, 2, Qt.AlignCenter)


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

