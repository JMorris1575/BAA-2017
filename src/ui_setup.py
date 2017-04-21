from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time

class BAA_Setup():

    def setupUI(self):
        panel = QWidget()
        self.setCentralWidget(panel)

        # grid = QGridLayout(panel)
        wholeLayout = QVBoxLayout(panel)
        wholeLayout.setContentsMargins(10, 10, 10, 10)
        self.drawingBoard = QLabel(panel)
        self.drawingBoard.setFrameShape(QFrame.Panel)
        self.drawingBoard.setFrameShadow(QFrame.Sunken)
        self.drawingBoard.setMinimumSize(640, 480)
        self.drawingBoard.setMaximumSize(640, 480)
        self.drawingBoard.setStyleSheet("QLabel { background-color : white; }")
        wholeLayout.addWidget(self.drawingBoard)

        self.pledgeInput = QLineEdit()
        self.pledgeInput.setAlignment(Qt.AlignRight)
        self.pledgeInput.setMaximumWidth(125)
        self.pledgeInput.setPlaceholderText("Enter amount pledged")
        self.pledgeLabel = QLabel("Pledged: ")
        self.pledgeLabel.setAlignment(Qt.AlignRight)
        self.pledgeLabel.setSizePolicy(0, 0)
        self.pledgeLabel.setEnabled(False)
        self.pledgeInput.textChanged.connect(self.test)

        self.collectedInput = QLineEdit()
        self.collectedInput.setAlignment(Qt.AlignRight)
        self.collectedInput.setMaximumWidth(125)
        self.collectedInput.setPlaceholderText("Enter amount collected")
        self.collectedLabel = QLabel("Collected: ")
        self.collectedLabel.setAlignment(Qt.AlignRight)

        self.familiesInput = QLineEdit()
        self.familiesInput.setAlignment(Qt.AlignRight)
        self.familiesInput.setMaximumWidth(125)
        self.familiesInput.setPlaceholderText("Enter number of families")
        self.familiesLabel = QLabel("Families: ")
        self.familiesLabel.setAlignment(Qt.AlignRight)

        lowerLayout = QHBoxLayout(panel)
        lowerLayout.addWidget(self.pledgeLabel)
        lowerLayout.addWidget(self.pledgeInput)

        hSpace = QSpacerItem(0, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)
        lowerLayout.addSpacerItem(hSpace)

        lowerLayout.addWidget(self.collectedLabel)
        lowerLayout.addWidget(self.collectedInput)

        lowerLayout.addSpacerItem(hSpace)

        lowerLayout.addWidget(self.familiesLabel)
        lowerLayout.addWidget(self.familiesInput)

        wholeLayout.addLayout(lowerLayout)

        # self.resize(660, 480)
        menubar = self.menuBar()
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)
        self.setupBars(menubar, toolbar)

    # Temp Section
    def test(self):
        print(self.pledgeInput.text())
    # End of Temp Section


    def setupBars(self, menubar=None, toolbar=None):
        self.createFileControls(menubar, toolbar)
        self.createSettingsControls(menubar, toolbar)
        self.createHelpControls(menubar, toolbar)


    def createFileControls(self, menubar=None, toolbar=None):
        if menubar:
            fileMenu = QMenu("&File", self)
            fileMenu.setToolTipsVisible(True)
            menubar.addMenu(fileMenu)

            self.saveAction = QAction(QIcon("images/icons/Save.png"), "&Save Graphic", self)
            self.saveAction.setShortcuts(QKeySequence.Save)
            self.saveAction.setToolTip("Save Graphic: Saves the current image in the standard location")
            self.saveAction.triggered.connect(self.saveImage)
            fileMenu.addAction(self.saveAction)
            if toolbar:
                toolbar.addAction(self.saveAction)

            self.saveAsAction = QAction(QIcon("images/icons/SaveAs.png"), "Save Graphic &As...", self)
            self.saveAsAction.setShortcuts(QKeySequence.SaveAs)
            self.saveAsAction.setToolTip("Save Graphic As: Saves the current image with a given name and location")
            self.saveAsAction.triggered.connect(self.saveImageAs)
            fileMenu.addAction(self.saveAsAction)
            if toolbar:
                toolbar.addAction(self.saveAsAction)

            fileMenu.addSeparator()

            quitAction = QAction(QIcon(""), "E&xit", self)
            quitAction.setShortcuts(QKeySequence.Close)
            quitAction.setToolTip("Exit: Exit BAA Thermometers program")
            quitAction.triggered.connect(self.close)
            fileMenu.addAction(quitAction)


    def createSettingsControls(self, menubar=None, toolbar=None):
        if menubar:
            settingsMenu = QMenu("&Settings", self)
            settingsMenu.setToolTipsVisible(True)
            menubar.addMenu(settingsMenu)

            targetAction = QAction(QIcon("images/icons/Target.png"), "Set &Targets", self)
            targetAction.setToolTip("Set Targets: Enter target goal and number of families.")
            targetAction.triggered.connect(self.setTargets)
            settingsMenu.addAction(targetAction)
            if toolbar:
                toolbar.addSeparator()
                toolbar.addAction(targetAction)

            imageOptionsAction = QAction(QIcon("images/icons/Settings.png"), "&Image Options...", self)
            imageOptionsAction.setToolTip("Image Options: Manage type and save location of images")
            imageOptionsAction.triggered.connect(self.settings)
            settingsMenu.addAction(imageOptionsAction)
            if toolbar:
                toolbar.addAction(imageOptionsAction)


    def createHelpControls(self, menubar=None, toolbar=None):
        if menubar:
            helpMenu = QMenu("&Help", self)
            helpMenu.setToolTipsVisible(True)
            menubar.addMenu(helpMenu)

            helpAction = QAction(QIcon("images/icons/Help.png"), "&Help", self)
            helpAction.setToolTip("Help: Get help about the program.")
            helpAction.triggered.connect(self.help)
            helpMenu.addAction(helpAction)
            if toolbar:
                toolbar.addSeparator()
                toolbar.addAction(helpAction)

            aboutAction = QAction(QIcon(""), "&About", self)
            aboutAction.setToolTip("About: Learn about the BAA Thermometers program")
            aboutAction.triggered.connect(self.about)
            helpMenu.addAction(aboutAction)
