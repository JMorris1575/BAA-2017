from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os.path

class Settings(QDialog):

    def __init__(self, config, parent=None):
        super(Settings, self).__init__(parent)
        self.setup(config)

    def setup(self, config):

        # ToDo: Change the fileWidgetLayout to a QVBoxLayout and use QHBoxLayouts to set the individual lines with a spacer at the bottom of them all.
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
        dirEdit.setMinimumWidth(200)
        dirEdit.setText(current_path)
        browseButton = QPushButton('Browse...')
        fileWidgetLayout.addWidget(dirLabel, 0, 0, Qt.AlignRight)
        fileWidgetLayout.addWidget(dirEdit, 0, 1, Qt.AlignLeft)
        fileWidgetLayout.addWidget(browseButton, 0, 2, Qt.AlignCenter)

        nameLabel = QLabel('Filename:')
        nameEdit = QLineEdit()
        nameEdit.setMinimumWidth(200)
        nameEdit.setText(config['imageStorage']['basename'])
        fileWidgetLayout.addWidget(nameLabel, 1, 0, Qt.AlignRight)
        fileWidgetLayout.addWidget(nameEdit, 1, 1, Qt.AlignLeft)

        dateLabel = QLabel('Date in Filename:')
        fileWidgetLayout.addWidget(dateLabel, 2, 0, Qt.AlignRight)

        dateGroup = QGroupBox('Select One:')
        dateGroup.setMinimumWidth(200)
        yesButton = QRadioButton('Yes')
        noButton = QRadioButton('No')
        dateLayout = QHBoxLayout()
        dateLayout.addWidget(yesButton)
        dateLayout.addWidget(noButton)
        if config['imageStorage']['useDate']:
            yesButton.setChecked(True)
        else:
            noButton.setChecked(True)
        dateGroup.setLayout(dateLayout)
        fileWidgetLayout.addWidget(dateGroup, 2, 1, Qt.AlignCenter)

        formatLabel = QLabel('File Format:')
        fileWidgetLayout.addWidget(formatLabel, 3, 0, Qt.AlignRight)

        formatGroup = QGroupBox('Select One:')
        formatGroup.setMinimumWidth(200)
        jpgButton = QRadioButton('.jpg')
        pngButton = QRadioButton('.png')
        bmpButton = QRadioButton('.bmp')
        formatLayout = QHBoxLayout()
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
        fileWidgetLayout.addWidget(formatGroup, 3, 1, Qt.AlignCenter)
        fileWidgetLayout.setRowStretch(0, 2)
        fileWidgetLayout.setRowStretch(1, 2)
        fileWidgetLayout.setRowStretch(2, 1)
        fileWidgetLayout.setRowStretch(3, 1)

        for i in range(4):
            print('row ' + str(i) + ' stretch: ' + str(fileWidgetLayout.rowStretch(i)))

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

