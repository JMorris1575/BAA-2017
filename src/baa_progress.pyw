"""
This program is designed to produce bulletin graphics indicating the current progress of a parish's response to the
Bishop's Annual Appeal (BAA). Once the target information is entered for a particular year's campaign all that needs
be done is to enter the current statistics:  pledge amount, amount collected and number of families who have made a
pledge so far; and the program generates a graphic indicating the percent to goal for the pledges, collected amount
and number of families involved. This can be saved as a .bmp, .png, or .jpg file to be printed in the parish bulletin.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_setup import BAA_Setup
from ui_targets_dlg import EditTargetsDlg
from ui_current_dlg import EditCurrentValuesDlg

import helperFunctions

import pickle
import os
import time


class MainWindow(QMainWindow, BAA_Setup):

    # ToDo: Make sure current values are checked for validity and saved in the config.cfg file
    # ToDo: Update graphic every time either the targets or the current values change

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUI(self)
        self.config = self.setDefaults()      # Establishes the structure of the configuration dictionary
        """
        The following section is for development purposes. By editing the configuration of baa_progress.pyw in 
        PyCharm to include a "Script Parameter" of 'config' (without the quotes) one can change the structure of
        the config file as it is written in config.cfg
        """
        if len(sys.argv) > 1:
            configFile = open('config.cfg', 'rb')
            temp_config = self.readConfig(configFile)
            temp_config['current'] = {}
            temp_config['current']['pledged'] = 0
            temp_config['current']['collected'] = 0
            temp_config['current']['families'] = 0
            self.writeConfig(temp_config)

        self.image = QImage(640, 480, QImage.Format_RGB32)

        class TargetsNotSetError(Exception): pass

        configFile = None
        try:
            configFile = open('config.cfg', 'rb')
            self.config = self.readConfig(configFile)
            try:
                if not self.config["targets"]["set"]:
                    raise TargetsNotSetError('')

            except TargetsNotSetError:
                self.limitAccess()

        except FileNotFoundError:
            self.limitAccess()

        finally:
            if configFile is not None:
                configFile.close()

        # set up drawing pens and brushes here?

    def limitAccess(self):
        """
        if the config.cfg file is not found or if the targets are not set, limit access to
        the program's functions and draw the welcome screen
        :return: 
        """
        self.pledgeLabel.setEnabled(False)
        self.pledgeInput.setEnabled(False)
        self.collectedLabel.setEnabled(False)
        self.collectedInput.setEnabled(False)
        self.familiesLabel.setEnabled(False)
        self.familiesInput.setEnabled(False)
        self.saveAction.setEnabled(False)
        self.saveAsAction.setEnabled(False)
        # self.config = self.setDefaults()
        self.drawWelcome()

    def readConfig(self, config_file):
        """
        Reads the configuration information from configFile
        :return: a dictionary of configuration values
        """
        config = pickle.load(config_file)
        self.config_changed = False
        print("Temporary Section -- Configuration just read:")
        print("config = ", config)

        return config

    def writeConfig(self, config):
        """
        Writes the configuration information from config to config.cfg in the same directory as the program.
        :return: True if successful, otherwise, False
        """
        print("Temporary Section -- Info being written to config.cfg")
        print("config = ", config)
        f = None
        f = open('config.cfg', 'wb')
        try:
            pickle.dump(config, f, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            print("{0}: saveProgramInfo error: {1}".format(
                os.path.basename(sys.argv[0]), err))
        finally:
            #self.config_changed = False
            if f is not None:
                f.close()

    def setDefaults(self):
        """
        Sets the defaults for the appearance, filename and location of the image produced by the program.
        This routine is generally only run the first time the program is used unless the user wants to
        restore the defaults through the settings dialog.
        :return: a dictionary of configuration values
        """
        config = {}
        config["targets"] = {'set':False, 'year':time.strftime('%Y'), 'goal': 0, 'families': 0}
        config['current'] = {'pledged':0, 'collected':0, 'families':0}
        config["type"] = ".png"
        config["style"] = "3DHorizontal"
        config["border"] = True
        config["title"] = "Our Parish Response to"
        self.config_changed = True
        return config

    def drawWelcome(self):
        """
        Draws and displays the welcome image the first time the program is used
        :return: None
        """
        painter = QPainter(self.image)
        linePen = QPen()    # default black pen 1 pixel wide
        whiteBrush = QBrush(Qt.white)   # white brush for background of rectangle
        infoFont = QFont('Arial', 12)
        painter.setPen(linePen)
        painter.setBrush(whiteBrush)
        painter.setFont(infoFont)
        painter.drawRect(0, 0, self.image.width() - 1, self.image.height() - 1)
        text = "Welcome to the Bishop's Annual Appeal "
        text += "Progress program!  Click the target "
        text += "in the toolbar above to set your "
        text += "goal information then enter the "
        text += "current data below and the program will "
        text += "draw a graphic for the bulletin."
        textRect = painter.boundingRect(QRectF(0, 0, self.image.width() / 2, self.image.height() / 2),
                                        Qt.AlignLeft | Qt.TextWordWrap,
                                        text)
        textRect.moveCenter(QPointF(self.image.width() / 2, self.image.height() / 2))
        borderRect = textRect.adjusted(-5, -5, 5, 5)
        painter.drawRect(borderRect)
        painter.drawText(textRect, text)
        self.drawingBoard.setPixmap(QPixmap.fromImage(self.image))

    def setTargets(self):
        print("Got to setTargets")
        dlg = EditTargetsDlg(self.config["targets"])
        if dlg.exec():
            self.config_changed = True
        else:
            print("Skipped dlg.exec")

    def setCurrent(self):
        print("Got to setCurrent")
        dlg = EditCurrentValuesDlg(self.config['current'])
        if dlg.exec():
            self.config_changed = True
        else:
            print("Skipped dlg.exec")

    # def currentValuesChanged(self):
    #     print('Got to moveFocus')
    #     self.pledgeInput.blockSignals(True)
    #     self.collectedInput.blockSignals(True)
    #     self.familiesInput.blockSignals(True)
    #     if self.sender().objectName() == 'pledgeInput':
    #         self.pledgeInput.setText(
    #             helperFunctions.decimalFormat(helperFunctions.String2Num(self.pledgeInput.text()), 'dollars')
    #         )
    #         self.collectedInput.setFocus()
    #         self.collectedInput.selectAll()
    #     elif self.sender().objectName() == 'collectedInput':
    #         self.collectedInput.setText(
    #             helperFunctions.decimalFormat(helperFunctions.String2Num(self.collectedInput.text()), 'dollars')
    #         )
    #         self.familiesInput.setFocus()
    #         self.familiesInput.selectAll()
    #     elif self.sender().objectName() == 'familiesInput':
    #         self.familiesInput.setText(str(int(self.familiesInput.text())))
    #         self.pledgeInput.setFocus()
    #         self.pledgeInput.selectAll()
    #     else:
    #         print("Problem in moveFocus method")
    #     self.pledgeInput.blockSignals(False)
    #     self.collectedInput.blockSignals(False)
    #     self.familiesInput.blockSignals(False)

    def saveImage(self):
        print("Got to saveImage")

    def saveImageAs(self):
        print("Got to saveImageAs")

    def exit(self):
        self.close()  # goes to closeEvent below

    def closeEvent(self, Event):
        print("Got to closeEvent")
        print("Save config.cfg if it has been changed. If it keeps current data, it will probably have been changed")
        if self.config_changed:
            self.writeConfig(self.config)
        self.close()

    def settings(self):
        print("Got to settings")

    def help(self):
        if not self.displayHelp():
            QMessageBox.warning(self, "Help Error",
                                "Help process timed out."
                                "  Help system currently unavailable.")

    def displayHelp(self):
        program = "assistant"
        arguments = ["-collectionFile",
                     "../docs/_build/qthelp/BAAProgress.qhc",
                     "-enableRemoteControl", ]
        helpProcess = QProcess(self)
        helpProcess.start(program, arguments)
        if not helpProcess.waitForStarted():
            return False
        print("About to send a message to helpProcess")
        ba = QByteArray()
        ba.append("setSource introduction.html\n;")
        ba.append("expandToc 1")
        helpProcess.write(ba)
        return True

    def about(self):
        print("Got to about()")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("BAA Progress")
    app.setWindowIcon(QIcon("images/icons/Mitre.png"))
    form = MainWindow()
    form.show()
    app.exec()