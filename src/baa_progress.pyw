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


class MainWindow(QMainWindow, BAA_Setup):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUI()
        self.config = {}        # configuration dictionary used throughout the program
        self.image = QImage(640, 480, QImage.Format_RGB32)
        try:
            configFile = None
            configFile = open("config.cfg")
            self.config = self.readConfig()

        except FileNotFoundError:
            self.pledgeLabel.setEnabled(False)
            self.pledgeInput.setEnabled(False)
            self.collectedLabel.setEnabled(False)
            self.collectedInput.setEnabled(False)
            self.familiesLabel.setEnabled(False)
            self.familiesInput.setEnabled(False)
            self.saveAction.setEnabled(False)
            self.saveAsAction.setEnabled(False)
            self.config = self.setDefaults()
            self.drawWelcome()

        finally:
            if configFile is not None:
                configFile.close()
                self.config = self.readConfig()
                # set up drawing pens and brushes here?

    def readConfig(self):
        """
        Reads the configuration information from config.cfg in the same directory as the program.
        :return: a dictionary of configuration values
        """
        config = {}

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
            print("Got to dlg.exec")
        else:
            print("Skipped dlg.exec")


    def saveImage(self):
        print("Got to saveImage")

    def saveImageAs(self):
        print("Got to saveImageAs")

    def exit(self):
        self.close()  # goes to closeEvent below

    def closeEvent(self, Event):
        print("Got to closeEvent")
        print("Save config.cfg if it has been changed. If it keeps current data, it will probably have been changed")
        # conditional file saving goes here
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