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
from ui_settings import Settings

import HIndicators
import DrawingControl
import helperFunctions

import pickle
import os
import time, datetime


class MainWindow(QMainWindow, BAA_Setup):

    # ToDo: Update formatting in targetEdit, pledgedEdit and collectedEdit when editing is finished
    # ToDo: Update graphic every time either the targets or the current values change

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

# ----------------------------------------------------------------------------------------------------------------------
        """
        The following section is for development purposes. By editing the configuration of baa_progress.pyw in 
        PyCharm to include a "Script Parameter" of 'config' (without the quotes) one can change the structure of
        the config file as it is written in config.cfg
        """
        if len(sys.argv) > 1:
            configFile = open('config.cfg', 'rb')
            temp_config = self.readConfig(configFile)
            configFile.close()
            temp_config_two = self.setDefaults()
            temp_config_two['targets'] = temp_config['targets']
            temp_config_two['current'] = temp_config['current']
            self.writeConfig(temp_config_two)
            self.config_changed = False
# ----------------------------------------------------------------------------------------------------------------------


        class TargetsNotSetError(Exception): pass

        configFile = None
        limitAccess = False
        try:
            configFile = open('config.cfg', 'rb')
            self.config = self.readConfig(configFile)
            self.getSettings(self.config)
            try:
                if not self.config["targets"]["set"]:
                    raise TargetsNotSetError('')

            except TargetsNotSetError:
                limitAccess = True

        except FileNotFoundError:
            self.config = self.setDefaults()
            self.getSettings(self.config)
            limitAccess = True

        finally:
            if configFile is not None:
                configFile.close()
            self.setupUI(self)
            if limitAccess:
                self.limitAccess()
                DrawingControl.drawWelcome(self)
            else:
                DrawingControl.drawGraphic(self)

    def setDefaults(self):
        """
        Sets the defaults for the program.
        This routine is generally only run the first time the program is used unless the user wants to
        restore the defaults through the settings dialog.
        :return: a dictionary of configuration values
        """
        config = {}
        config['imageSize'] = (640, 480)
        config['imageBackground'] = QColor(Qt.white)
        config['imageStorage'] = {'path': '.', 'basename': 'baa_progress', 'format': 'jpg', 'useDate': True}
        config['targets'] = {'set':False, 'year':time.strftime('%Y'), 'goal': 0, 'families': 0}
        config['current'] = {'pledged':0, 'collected':0, 'families':0}
        config['type'] = ".png"
        config['style'] = "3DVertical"
        config['displayColor'] = True
        config['border'] = 'single'     # could be none, single or double
        config['heading_prefix'] = "Our Parish Response to the"
        config['heading'] = "Bishop's Annual Appeal"
        config['penDefinitions'] = self.definePens()
        config['brushDefinitions'] = self.defineFills()
        config['fontDefinitions'] = self.defineFonts()
        self.config_changed = True
        return config

    def getSettings(self, config):
        """
        Uses the configuration dictionary, config, to create pens, brushes, fonts and other often needed objects
        :param config: dictionary
        :return: None
        """
        self.image = QImage(config['imageSize'][0], config['imageSize'][1], QImage.Format_RGB32)
        self.pens = self.createPens(config['penDefinitions'])
        self.fills = self.createFills(config['brushDefinitions'])
        self.fonts = self.createFonts(config['fontDefinitions'])

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
        penDefinitions['outline_pen'] = {'color':QColor(Qt.black), 'width':1, 'style':Qt.SolidLine,
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
        fillDefinitions['darkGray_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.darkGray)}
        fillDefinitions['red_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.red)}
        fillDefinitions['darkRed_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.darkRed)}
        fillDefinitions['green_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.green)}
        fillDefinitions['darkGreen_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.darkGreen)}
        fillDefinitions['blue_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.blue)}
        fillDefinitions['darkBlue_brush'] = {'style': Qt.SolidPattern, 'color': QColor(Qt.darkBlue)}
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

    def defineFonts(self):
        """
        Defines a dictionary of QFonts used in the program and to be saved in the config.cfg file. These fonts can have
        their attributes set by the user through the settings panel. They need to be actualized into a QFont after they
        have been defined.
        :return: a dictionary with keys for the definitions of the different fonts used in the program
        """
        fontDefinitions = {}
        fontDefinitions['headingFont'] = {'fontName': 'Arial', 'size': 24, 'weight':QFont.Bold, 'italic':False}
        fontDefinitions['captionFont'] = {'fontName': 'Arial', 'size': 16, 'weight':QFont.Normal, 'italic':False}
        fontDefinitions['smallCaptionFont'] = {'fontName': 'Arial', 'size': 12, 'weight':QFont.Normal, 'italic':False}
        fontDefinitions['prefixFont'] = {'fontName':'Arial', 'size':18, 'weight':QFont.Normal, 'italic':False}
        fontDefinitions['infoFont'] = {'fontName':'Arial', 'size':12, 'weight':QFont.Normal, 'italic':False}

        return fontDefinitions

    def createFonts(self, defs):
        """
        Creates a dictionary of the fonts used in the program from the definitions (defs). These fonts can have their
        characteristics set by the user through the settings panel.
        :return: a dictionary with keys for each of the different fonts used in the program
        """
        fonts = {}
        for fontKey in defs:
            fontDef = defs[fontKey]
            fonts[fontKey] = QFont(fontDef['fontName'], fontDef['size'], fontDef['weight'], fontDef['italic'])
        return fonts

    def limitAccess(self):
        """
        if the config.cfg file is not found or if the targets are not set, limit access to
        the program's functions and draw the welcome screen
        :return: None
        """
        self.saveAction.setEnabled(False)
        self.saveAsAction.setEnabled(False)
        self.enterData.setEnabled(False)

    def grantAccess(self):
        """
        Once the targets have been set, access to the program's functions can be granted
        :return: None
        """
        self.saveAction.setEnabled(True)
        self.saveAsAction.setEnabled(True)
        self.enterData.setEnabled(True)


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
        f = None
        f = open('config.cfg', 'wb')
        try:
            pickle.dump(config, f, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            print("{0}: saveProgramInfo error: {1}".format(
                os.path.basename(sys.argv[0]), err))
        finally:
            if f is not None:
                f.close()



    def meterIndicators(self, painter, verticalPosition):
        print('Got to meterIndicators')

    def guageIndicators(self, painter, verticalPosition):
        print('Got to guage indicators.')

    def setTargets(self):
        dlg = EditTargetsDlg(self.config["targets"])
        if dlg.exec():
            self.config_changed = True
            self.grantAccess()
            DrawingControl.drawGraphic(self)

    def setCurrent(self):
        dlg = EditCurrentValuesDlg(self.config['current'])
        if dlg.exec():
            if dlg.config_changed:
                self.config_changed = True
                DrawingControl.drawGraphic(self)

    def saveImage(self):
        fileDesignation = self.getFileDesignation()
        self.image.save(fileDesignation)

    def saveImageAs(self):
        print("Got to saveImageAs")

    def checkForSave(self):
        """
        Creates a yes/no/cancel message box so the user can decide whether to save the image file with the current
        default settings, change the settings, temporarily or permanently, or not at all
        :return: The QMessageBox results: QMessageBox.Yes, QMessageBox.No, or QMessageBox.Cancel
        """
        box = QMessageBox()
        msg = 'Do you wish to save the changes you have made?'
        box.setText(msg)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No |
                               QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Yes)
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Save Graphic Query')
        return box.exec()

    def closeEvent(self, event):
        self.saveImage()
        if self.config_changed:
            result = self.checkForSave()
            if result == QMessageBox.Yes:
                self.writeConfig(self.config)
                self.close()
            elif result == QMessageBox.No:
                self.close()
            else:
                event.ignore()

    def getFileDesignation(self):
        """
        Creates the complete filename, including path, for the image file
        :return: the complete filename as a string
        """
        path = self.config['imageStorage']['path']
        filename = self.config['imageStorage']['basename']
        image_format = self.config['imageStorage']['format']
        if self.config['imageStorage']['useDate']:
            now = datetime.datetime.now()
            filename = str(now.date()) + '-' + filename
        return path + '/' + filename + '.' + image_format

    def settings(self):
        dlg = Settings(self)
        dlg.exec()
        if dlg.image_changed:
            DrawingControl.drawGraphic(self)


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