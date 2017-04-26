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

    # ToDo: Update formatting in targetEdit, pledgedEdit and collectedEdit when editing is finished
    # ToDo: Update graphic every time either the targets or the current values change

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUI(self)
        # self.config = self.setDefaults()      # Establishes the structure of the configuration dictionary

# ----------------------------------------------------------------------------------------------------------------------
        """
        The following section is for development purposes. By editing the configuration of baa_progress.pyw in 
        PyCharm to include a "Script Parameter" of 'config' (without the quotes) one can change the structure of
        the config file as it is written in config.cfg
        """
        if len(sys.argv) > 1:
            # configFile = open('config.cfg', 'rb')
            # temp_config = self.readConfig(configFile)
            temp_config = self.setDefaults()
            self.writeConfig(temp_config)
# ----------------------------------------------------------------------------------------------------------------------

        self.image = QImage(640, 480, QImage.Format_RGB32)
        # self.pens = self.createPens()
        # self.brushes = self.createFills()
        # self.fonts = self.createFonts()

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
            self.config = self.setDefaults()
            self.getSettings(self.config)
            self.limitAccess()

        finally:
            if configFile is not None:
                configFile.close()
                self.getSettings(self.config)
                self.drawGraphic()

    def setDefaults(self):
        """
        Sets the defaults for the program.
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
        config["title"] = "Our Parish Response to the"
        config['penDefinitions'] = self.definePens()
        config['brushDefinitions'] = self.defineFills()
        # config['fontDefinitions'] = self.defineFonts()
        self.config_changed = True
        return config

    def getSettings(self, config):
        """
        Uses the configuration dictionary, config, to create pens, brushes, fonts and other often needed objects
        :param config: dictionary
        :return: None
        """
        self.pens = self.createPens(config['penDefinitions'])
        self.fills = self.createFills(config['brushDefinitions'])

    def definePens(self):
        """
        Defines a dictionary of pens used in the program and to be saved in the config.cfg file. These pens can have
        their attributes set by the user through the settings panel. They need to be actualized into a QPen after they
        have been defined.
        :return: a dictionary with keys for the definitions of the different pens used in the program
        """
        penDefinitions = {}
        penDefinitions['no_pen'] = {'color':QColor(Qt.black), 'width':1, 'style':Qt.NoPen,
                                    'cap':Qt.RoundCap, 'join':Qt.RoundJoin}
        penDefinitions['border_pen'] = {'color':QColor(Qt.black), 'width':2, 'style':Qt.SolidLine,
                                        'cap':Qt.RoundCap, 'join':Qt.RoundJoin}
        return penDefinitions

    def createPens(self, defs):
        """
        Creates a dictionary of the QPens used in the program from the given definitions (defs).
        These pens can have their characteristics set by the user through the settings panel.
        :return: a dictionary with keys for each of the different QPens used in the program
        """
        pens = {}
        for penkey in defs.keys():
            pendef = defs[penkey]
            new_pen = QPen()
            new_pen.setColor(pendef['color'])
            new_pen.setWidth(pendef['width'])
            new_pen.setStyle(pendef['style'])
            new_pen.setCapStyle(pendef['cap'])
            new_pen.setJoinStyle(pendef['join'])
            pens[penkey] = new_pen

        return pens

    def defineFills(self):
        """
        Defines a dictionary of brushes used in the program and to be saved in the config.cfg file. These brushes can
        have their attributes set by the user through the settings panel. They need to be actualized into QBrushes after
        they have been defined.
        :return: a dictionary with keys for the definitions of the different brushes used in the program
        """
        fillDefinitions = {}
        fillDefinitions['white_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.white)}
        fillDefinitions['black_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.black)}
        fillDefinitions['gray_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.gray)}
        fillDefinitions['gray_linear_gradient'] = {'style': Qt.LinearGradientPattern,
                                                'colors': [[0.0, QColor(Qt.gray)],
                                                           [0.3, QColor(Qt.white)],
                                                           [1.0, QColor(Qt.black)]]}
        fillDefinitions['gray_radial_gradient'] = {'style': Qt.RadialGradientPattern,
                                               'colors': [[0.0, QColor(Qt.white)],
                                                          [0.3, QColor(Qt.gray)],
                                                          [1.0, QColor(Qt.black)]]}
        fillDefinitions['red_linear_gradient'] = {'style': Qt.LinearGradientPattern,
                                                  'colors': [[0.12, QColor(Qt.red)],
                                                             [0.35, QColor(Qt.white)],
                                                             [0.55, QColor(Qt.red)],
                                                             [1.0, QColor(Qt.darkRed)]]}
        fillDefinitions['red_radial_gradient'] = {'style': Qt.RadialGradientPattern,
                                                  'colors': [[0.0, QColor(Qt.white)],
                                                             [0.3, QColor(Qt.red)],
                                                             [1.0, QColor(Qt.darkRed)]]}
        fillDefinitions['green_linear_gradient'] = {'style': Qt.LinearGradientPattern,
                                                  'colors': [[0.12, QColor(Qt.green)],
                                                             [0.35, QColor(Qt.white)],
                                                             [0.55, QColor(Qt.green)],
                                                             [1.0, QColor(Qt.darkGreen)]]}
        fillDefinitions['green_radial_gradient'] = {'style': Qt.RadialGradientPattern,
                                                  'colors': [[0.0, QColor(Qt.white)],
                                                             [0.3, QColor(Qt.green)],
                                                             [1.0, QColor(Qt.darkGreen)]]}
        fillDefinitions['blue_linear_gradient'] = {'style': Qt.LinearGradientPattern,
                                                  'colors': [[0.12, QColor(Qt.blue)],
                                                             [0.35, QColor(Qt.white)],
                                                             [0.55, QColor(Qt.blue)],
                                                             [1.0, QColor(Qt.darkBlue)]]}
        fillDefinitions['blue_radial_gradient'] = {'style': Qt.RadialGradientPattern,
                                                  'colors': [[0.0, QColor(Qt.white)],
                                                             [0.3, QColor(Qt.blue)],
                                                             [1.0, QColor(Qt.darkBlue)]]}


        return fillDefinitions

    def createFills(self, defs):
        """
        Creates a dictionary of the fill colors and styles used in the program from the given definitions (defs).
        These can either be QBrushes or QGradients depending on their style and can have their characteristics set by
        the user through the settings panel.
        :return: a dictionary with keys for each of the different QBrushes and QGradients used in the program
        """
        fills = {}
        for fillKey in defs.keys():
            fillDef = defs[fillKey]
            if fillDef['style'] == Qt.SolidPattern:
                new_fill = QBrush()
                new_fill.setStyle(Qt.SolidPattern)
                new_fill.setColor(fillDef['color'])

            elif fillDef['style'] == Qt.LinearGradientPattern:
                gradient = QLinearGradient()
                gradient.setStops(fillDef['colors'])
                new_fill = gradient
                #new_brush.setStyle(Qt.LinearGradientPattern)

            elif fillDef['style'] == Qt.RadialGradientPattern:
                gradient = QRadialGradient()
                gradient.setStops(fillDef['colors'])
                new_fill = gradient

            else:
                new_fill.setStyle(Qt.NoBrush)

            fills[fillKey] = new_fill

        return fills

    def createFonts(self):
        """
        Creates a dictionary of the fonts used in the program. These fonts can have their characteristics set by
        the user through the settings panel.
        :return: a dictionary with keys for each of the different brushes used in the program
        """
        fonts = {}
        fonts['headerFont'] = QFont('Arial', 24, QFont.Bold)
        fonts['subheadingFont'] = QFont('Arial', 18)
        fonts['infoFont'] = QFont('Arial', 12)
        return fonts

    def limitAccess(self):
        """
        if the config.cfg file is not found or if the targets are not set, limit access to
        the program's functions and draw the welcome screen
        :return: 
        """
        self.saveAction.setEnabled(False)
        self.saveAsAction.setEnabled(False)
        self.enterData.setEnabled(False)
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
# ----------------------------------------------------------------------------------------------------------------------
        # Temporary Section -- Info being written to config.cfg"
        print("config = ", config)
# ----------------------------------------------------------------------------------------------------------------------

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
        text += "goal information then click the "
        text += "hand icon to enter the current data. "
        text += "the program will draw a graphic for "
        text += "the bulletin."
        textRect = painter.boundingRect(QRectF(0, 0, self.image.width() / 2, self.image.height() / 2),
                                        Qt.AlignLeft | Qt.TextWordWrap,
                                        text)
        textRect.moveCenter(QPointF(self.image.width() / 2, self.image.height() / 2))
        borderRect = textRect.adjusted(-5, -5, 5, 5)
        painter.drawRect(borderRect)
        painter.drawText(textRect, text)
        self.drawingBoard.setPixmap(QPixmap.fromImage(self.image))

    def drawGraphic(self):
        """
        Draws the graphic according to the current data and current settings
        :return: None
        """
        painter = QPainter(self.image)
        borderPen = self.pens['border_pen']
        painter.setBrush(self.fills['white_brush'])
        painter.setPen(borderPen)
        print(self.image.width(), self.image.height())
        for i in range(10):
            painter.drawRect(i * 10, i * 10, self.image.width() - 2 * i * 10, self.image.height() - 2 * i * 10)
        painter.setBrush(self.fills['gray_brush'])
        painter.drawEllipse(320, 240, 50, 50)
        gradient = self.fills['gray_linear_gradient']
        gradient.setStart(0, 120)
        gradient.setFinalStop(0, 170)
        painter.setBrush(gradient)
        painter.setPen(self.pens['no_pen'])
        painter.drawRect(200, 120, 150, 50)

        gradient = self.fills['blue_linear_gradient']
        gradient.setStart(0, 60)
        gradient.setFinalStop(0, 160)
        painter.setBrush(gradient)
        painter.drawRect(400, 60, 100, 100)

        gradient = self.fills['gray_radial_gradient']
        gradient.setCenter(QPointF(200, 135))
        gradient.setRadius(36)
        gradient.setFocalPoint(QPointF(200,135))
        painter.setBrush(gradient)
        painter.drawChord(QRectF(175,120,50,50), 16*90, 16*180)

        gradient = self.fills['blue_radial_gradient']
        gradient.setCenter(QPointF(400, 90))
        gradient.setRadius(72)
        gradient.setFocalPoint(QPointF(400, 95))
        painter.setBrush(gradient)
        painter.drawChord(QRectF(350, 60, 100, 100), 16*90, 16*180)

        self.drawingBoard.setPixmap(QPixmap.fromImage(self.image))



    def setTargets(self):
        print("Got to setTargets")
        dlg = EditTargetsDlg(self.config["targets"])
        if dlg.exec():
            self.config_changed = True
        else:
            print("Skipped dlg.exec")
        self.drawGraphic()

    def setCurrent(self):
        print("Got to setCurrent")
        dlg = EditCurrentValuesDlg(self.config['current'])
        if dlg.exec():
            self.config_changed = True
        else:
            print("Skipped dlg.exec")
        self.drawGraphic()

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