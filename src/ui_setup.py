from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import helperFunctions

import time

class BAA_Setup():

    def setupUI(self, BAA_Progress_UI):
        panel = QWidget()
        BAA_Progress_UI.setCentralWidget(panel)
        #self.setCentralWidget(panel)

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

        # self.pledgeInput = QLineEdit()
        # self.pledgeInput.setObjectName("pledgeInput")
        # self.pledgeInput.setAlignment(Qt.AlignRight)
        # self.pledgeInput.setMaximumWidth(125)
        # self.pledgeInput.setPlaceholderText("Enter amount pledged")
        # self.pledgeInput.setToolTip("Enter amount pledged with or without formatting.")
        # self.pledgeInput.setWhatsThis('Amount pledged can be entered either as plain digits: 1234.56\n' +
        #                               'or formatted as currency: $1,234.56')
        # self.pledgeLabel = QLabel("Pledged: ")
        # self.pledgeLabel.setAlignment(Qt.AlignRight)
        # self.pledgeLabel.setSizePolicy(0, 0)
        # self.pledgeInput.returnPressed.connect(self.currentValuesChanged)
        # self.pledgeInput.editingFinished.connect(self.currentValuesChanged)
        #
        # self.collectedInput = QLineEdit()
        # self.collectedInput.setObjectName('collectedInput')
        # self.collectedInput.setAlignment(Qt.AlignRight)
        # self.collectedInput.setMaximumWidth(125)
        # self.collectedInput.setPlaceholderText("Enter amount collected")
        # self.collectedLabel = QLabel("Collected: ")
        # self.collectedLabel.setAlignment(Qt.AlignRight)
        # self.collectedInput.returnPressed.connect(self.currentValuesChanged)
        # self.collectedInput.editingFinished.connect(self.currentValuesChanged)
        #
        # self.familiesInput = QLineEdit()
        # self.familiesInput.setObjectName('familiesInput')
        # self.familiesInput.setAlignment(Qt.AlignRight)
        # self.familiesInput.setMaximumWidth(125)
        # self.familiesInput.setPlaceholderText("Enter number of families")
        # self.familiesLabel = QLabel("Families: ")
        # self.familiesLabel.setAlignment(Qt.AlignRight)
        # self.familiesInput.returnPressed.connect(self.currentValuesChanged)
        # self.familiesInput.editingFinished.connect(self.currentValuesChanged)
        #
        # lowerLayout = QHBoxLayout(panel)
        # lowerLayout.addWidget(self.pledgeLabel)
        # lowerLayout.addWidget(self.pledgeInput)
        #
        # hSpace = QSpacerItem(0, 0, QSizePolicy.Maximum, QSizePolicy.Minimum)
        # lowerLayout.addSpacerItem(hSpace)
        #
        # lowerLayout.addWidget(self.collectedLabel)
        # lowerLayout.addWidget(self.collectedInput)
        #
        # lowerLayout.addSpacerItem(hSpace)
        #
        # lowerLayout.addWidget(self.familiesLabel)
        # lowerLayout.addWidget(self.familiesInput)
        #
        # wholeLayout.addLayout(lowerLayout)

        # self.resize(660, 480)
        menubar = self.menuBar()
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)
        self.setupBars(menubar, toolbar)

    def setupBars(self, menubar=None, toolbar=None):
        self.createFileControls(menubar, toolbar)
        self.createEditControls(menubar, toolbar)
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


    def createEditControls(self, menubar=None, toolbar=None):
        if menubar:
            editMenu = QMenu("&Edit", self)
            editMenu.setToolTipsVisible(True)
            menubar.addMenu(editMenu)

            targetAction = QAction(QIcon("images/icons/Target.png"), "Set &Targets", self)
            targetAction.setToolTip("Set Targets: Enter target goal and number of families.")
            targetAction.triggered.connect(self.setTargets)
            editMenu.addAction(targetAction)

            currentAction = QAction(QIcon('images/icons/Target.png'), 'Enter &Current Data', self)
            currentAction.setToolTip("Enter current data: amount pledged, amount collected and number of families"
                                     " participating.")
            currentAction.triggered.connect(self.setCurrent)
            editMenu.addAction(currentAction)

            settingsAction = QAction(QIcon("images/icons/Settings.png"), "&Image Options...", self)
            settingsAction.setToolTip("Settings: Manage how the program displays and saves its data.")
            settingsAction.triggered.connect(self.settings)
            editMenu.addAction(settingsAction)

            if toolbar:
                toolbar.addSeparator()
                toolbar.addAction(targetAction)
                toolbar.addAction(currentAction)
                toolbar.addAction(settingsAction)


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
