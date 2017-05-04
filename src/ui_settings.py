from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Settings(QDialog):

    def __init__(self, config, parent=None):
        super(Settings, self).__init__(parent)
        self.setup(config)

    def setup(self, config):

        self.resize(QSize(400, 360))

        settingsWidget = QTabWidget(self)
        settingsLayout = QVBoxLayout(self)

        fileSettingsWidget = QWidget()
        helloLabel = QLabel('Hello Jim!')
        fileWidgetLayout = QVBoxLayout(fileSettingsWidget)
        fileWidgetLayout.addWidget(helloLabel)

        settingsWidget.addTab(fileSettingsWidget, 'File Settings')

        appearanceSettingsWidget = QWidget()
        lookLabel = QLabel('Look at me!')
        appearanceWidgetLayout = QVBoxLayout(appearanceSettingsWidget)
        appearanceWidgetLayout.addWidget(lookLabel)
        settingsWidget.addTab(appearanceSettingsWidget, 'Graphic Appearance')

        settingsLayout.addWidget(settingsWidget)

