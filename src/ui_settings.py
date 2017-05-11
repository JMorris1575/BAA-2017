from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os, os.path, sys, re

class Settings(QDialog):

    def __init__(self, main, parent=None):
        super(Settings, self).__init__(parent)
        self.main = main
        config = main.config
        self.image_changed = False
        self.setup(config)

    def setup(self, config):

        self.resize(QSize(400, 360))

        settingsWidget = QTabWidget(self)
        settingsLayout = QVBoxLayout(self)

        # File Settings Tab

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
        yesButton.clicked.connect(self.setDateUse)
        noButton = QRadioButton('No')
        noButton.clicked.connect(self.setDateUse)
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
        #formatGroup.setMinimumWidth(200)
        jpgButton = QRadioButton('.jpg')
        jpgButton.clicked.connect(self.setImageFormat)
        pngButton = QRadioButton('.png')
        pngButton.clicked.connect(self.setImageFormat)
        bmpButton = QRadioButton('.bmp')
        bmpButton.clicked.connect(self.setImageFormat)
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

        # Appearance Settings Tab

        appearanceSettingsWidget = QWidget()
        appearanceWidgetLayout = QVBoxLayout(appearanceSettingsWidget)
        settingsWidget.addTab(appearanceSettingsWidget, 'Border/Titles')
        settingsWidget.setToolTip('Control the border and titles used in the image.')

        borderLabel = QLabel('Border:')
        borderLabel.setAlignment(Qt.AlignRight)
        borderGroup = QGroupBox('Select One:')
        borderGroup.setWhatsThis('Allows you to decide whether to have a border and whether it is to be a' +
                                 'single or double-line border.')
        noneButton = QRadioButton('None')
        noneButton.clicked.connect(self.setBorder)
        singleButton = QRadioButton('Single')
        singleButton.clicked.connect(self.setBorder)
        doubleButton = QRadioButton('Double')
        doubleButton.clicked.connect(self.setBorder)
        borderGroupLayout = QHBoxLayout()
        borderGroupLayout.addWidget(noneButton)
        borderGroupLayout.addWidget(singleButton)
        borderGroupLayout.addWidget(doubleButton)
        borderStyle = self.main.config['border']
        if borderStyle == 'none':
            noneButton.setChecked(True)
        elif borderStyle == 'single':
            singleButton.setChecked(True)
        else:
            doubleButton.setChecked(True)
        borderGroup.setLayout(borderGroupLayout)
        borderLayout = QHBoxLayout()
        borderLayout.addWidget(borderLabel, 1)
        borderLayout.addWidget(borderGroup, 4)
        appearanceWidgetLayout.addLayout(borderLayout)

        headingPrefixLabel = QLabel('Heading 1:')
        headingPrefixLabel.setAlignment(Qt.AlignRight)
        self.headingPrefixEdit = QLineEdit()
        self.headingPrefixEdit.setWhatsThis('Here you can rewrite the initial line of the heading. You may, for instance' +
                                            'want to include the name of the parish.')
        self.headingPrefixEdit.setAlignment(Qt.AlignLeft)
        self.headingPrefixEdit.setText(config['heading_prefix'])
        self.headingPrefixEdit.editingFinished.connect(self.prefixEdit)
        prefixLayout = QHBoxLayout()
        prefixLayout.addWidget(headingPrefixLabel, 1)
        prefixLayout.addWidget(self.headingPrefixEdit, 4)
        appearanceWidgetLayout.addLayout(prefixLayout)

        mainHeadingLabel = QLabel('Main Heading:')
        mainHeadingLabel.setAlignment(Qt.AlignRight)
        self.mainHeadingEdit = QLineEdit()
        self.mainHeadingEdit.setWhatsThis('Here you can rewrite the initial line of the heading. You may, for instance' +
                                            'want to include the name of the parish.')
        self.mainHeadingEdit.setAlignment(Qt.AlignLeft)
        self.mainHeadingEdit.setText(config['heading'])
        self.mainHeadingEdit.editingFinished.connect(self.headingEdit)
        headingLayout = QHBoxLayout()
        headingLayout.addWidget(mainHeadingLabel, 1)
        headingLayout.addWidget(self.mainHeadingEdit, 4)
        appearanceWidgetLayout.addLayout(headingLayout)

        appearanceWidgetLayout.addStretch(0)

        # Style Settings Tab

        styleSettingsWidget = QWidget()
        styleWidgetLayout = QVBoxLayout(styleSettingsWidget)
        settingsWidget.addTab(styleSettingsWidget, 'Style')
        settingsWidget.setToolTip('Control the color, appearance and type of the indicators.')

        colorLabel = QLabel('Coloring:')
        colorLabel.setAlignment(Qt.AlignRight)
        colorGroup = QGroupBox('Select One:')
        colorGroup.setWhatsThis('Choose color or grayscale (which may print better in the bulletin).')
        colorButton = QRadioButton('Color')
        colorButton.clicked.connect(self.setColor)
        grayscaleButton = QRadioButton('Grayscale')
        grayscaleButton.clicked.connect(self.setColor)
        colorGroupLayout = QHBoxLayout()
        colorGroupLayout.addWidget(colorButton)
        colorGroupLayout.addWidget(grayscaleButton)
        colorGroup.setLayout(colorGroupLayout)
        if self.main.config['displayColor']:
            colorButton.setChecked(True)
        else:
            grayscaleButton.setChecked(True)
        colorLayout = QHBoxLayout()
        colorLayout.addWidget(colorLabel, 1)
        colorLayout.addWidget(colorGroup, 4)
        styleWidgetLayout.addLayout(colorLayout)

        styleLabel = QLabel('Style:')
        styleLabel.setAlignment(Qt.AlignRight)
        styleGroup = QGroupBox('Select One:')
        styleGroup.setWhatsThis('Give the indicators either a flat or a three-dimensional appearance.')
        flatButton = QRadioButton('Flat')
        flatButton.clicked.connect(self.setStyle)
        solidButton = QRadioButton('Solid')
        solidButton.clicked.connect(self.setStyle)
        styleGroupLayout = QHBoxLayout()
        styleGroupLayout.addWidget(flatButton)
        styleGroupLayout.addWidget(solidButton)
        styleGroup.setLayout(styleGroupLayout)
        style = self.main.config['style'][0:2]
        if style == '2D':
            flatButton.setChecked(True)
        else:
            solidButton.setChecked(True)
        styleLayout = QHBoxLayout()
        styleLayout.addWidget(styleLabel, 1)
        styleLayout.addWidget(styleGroup, 4)
        styleWidgetLayout.addLayout(styleLayout)

        typeLabel = QLabel('Type:')
        typeLabel.setAlignment(Qt.AlignRight)
        typeGroup = QGroupBox('Select One:')
        typeGroup.setWhatsThis('Lets you select the type of indicator to be displayed.')
        horizontalButton = QRadioButton('Horizontal')
        horizontalButton.clicked.connect(self.setType)
        verticalButton = QRadioButton('Vertical')
        verticalButton.clicked.connect(self.setType)
        meterButton = QRadioButton('Meters')
        meterButton.clicked.connect(self.setType)
        guageButton = QRadioButton('Guages')
        guageButton.clicked.connect(self.setType)
        guageButton.setEnabled(False)
        pieButton = QRadioButton('Pies')
        pieButton.clicked.connect(self.setType)
        pieButton.setEnabled(False)
        typeGroupLayout = QVBoxLayout()
        typeGroupLayout.addWidget(horizontalButton)
        typeGroupLayout.addWidget(verticalButton)
        typeGroupLayout.addWidget((meterButton))
        typeGroupLayout.addWidget(guageButton)
        typeGroupLayout.addWidget(pieButton)
        typeGroup.setLayout(typeGroupLayout)
        type = self.main.config['style'][2:]
        if type == 'Horizontal':
            horizontalButton.setChecked(True)
        elif type == 'Vertical':
            verticalButton.setChecked(True)
        elif type == 'Guage':
            guageButton.setChecked(True)
        else:
            pieButton.setChecked(True)
        typeLayout = QHBoxLayout()
        typeLayout.addWidget(typeLabel, 1)
        typeLayout.addWidget(typeGroup, 4)
        styleWidgetLayout.addLayout(typeLayout)

        styleWidgetLayout.addStretch(0)

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

    @pyqtSlot()
    def setDateUse(self):
        setting = self.sender().text()
        if setting == 'Yes':
            self.main.config['imageStorage']['useDate'] = True
        else:
            self.main.config['imageStorage']['useDate'] = False
        self.main.config_changed = True

    @pyqtSlot()
    def setImageFormat(self):
        setting = self.sender().text()[1:]      # gets the caption and strips off the period (.)
        self.main.config['imageStorage']['format'] = setting
        self.main.config_changed = True

    @pyqtSlot()
    def setBorder(self):
        setting = self.sender().text()
        if setting == 'None':
            self.main.config['border'] = 'none'
        elif setting == 'Single':
            self.main.config['border'] = 'single'
        else:
            self.main.config['border'] = 'double'
        self.main.config_changed = True
        self.image_changed = True

    def prefixEdit(self):
        heading_prefix = self.headingPrefixEdit.text()
        self.main.config['heading_prefix'] = heading_prefix
        self.main.config_changed = True
        self.image_changed = True

    def headingEdit(self):
        heading = self.mainHeadingEdit.text()
        self.main.config['heading'] = heading
        self.main.config_changed = True
        self.image_changed = True

    @pyqtSlot()
    def setColor(self):
        if self.sender().text() == 'Color':
            self.main.config['displayColor'] = True
        else:
            self.main.config['displayColor'] = False
        self.main.config_changed = True
        self.image_changed = True

    @pyqtSlot()
    def setStyle(self):
        if self.sender().text() == 'Flat':
            style = '2D'
        else:
            style = '3D'
        type = self.main.config['style'][2:]
        self.main.config['style'] = style + type
        self.main.config_changed = True
        self.image_changed = True

    @pyqtSlot()
    def setType(self):
        style = self.main.config['style'][0:2]
        self.main.config['style'] = style + self.sender().text()
        self.main.config_changed = True
        self.image_changed = True