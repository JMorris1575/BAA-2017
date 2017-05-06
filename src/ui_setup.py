from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import helperFunctions

import time

class BAA_Setup():

    def setupUI(self, BAA_Progress_UI):
        panel = QWidget()
        BAA_Progress_UI.setCentralWidget(panel)

        wholeLayout = QVBoxLayout(panel)
        wholeLayout.setContentsMargins(10, 10, 10, 10)
        self.drawingBoard = QLabel(panel)
        self.drawingBoard.setFrameShape(QFrame.Panel)
        self.drawingBoard.setFrameShadow(QFrame.Sunken)
        frameWidth = self.drawingBoard.frameWidth()
        self.drawingBoard.setMinimumSize(self.image.width()+2*frameWidth, self.image.height()+2*frameWidth)
        self.drawingBoard.setMaximumSize(self.image.width()+2*frameWidth, self.image.height()+2*frameWidth)
        self.drawingBoard.setStyleSheet("QLabel { background-color : white; }")
        wholeLayout.addWidget(self.drawingBoard)

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

            self.saveAsAction = QAction("Save Graphic &As...", self)
            self.saveAsAction.setShortcuts(QKeySequence.SaveAs)
            self.saveAsAction.setToolTip("Save Graphic As: Saves the current image with a given name and location")
            self.saveAsAction.triggered.connect(self.saveImageAs)
            fileMenu.addAction(self.saveAsAction)

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

            self.enterData = QAction(QIcon('images/icons/enterData.png'), 'Enter &Current Data', self)
            self.enterData.setToolTip("Enter current data: amount pledged, amount collected and number of families"
                                     " participating.")
            self.enterData.triggered.connect(self.setCurrent)
            editMenu.addAction(self.enterData)

            settingsAction = QAction(QIcon("images/icons/Settings.png"), "&Image Options...", self)
            settingsAction.setToolTip("Settings: Manage how the program displays and saves its data.")
            settingsAction.triggered.connect(self.settings)
            editMenu.addAction(settingsAction)

            if toolbar:
                toolbar.addSeparator()
                toolbar.addAction(targetAction)
                toolbar.addAction(self.enterData)
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
