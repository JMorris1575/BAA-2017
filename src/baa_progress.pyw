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
                self.drawWelcome()
            else:
                self.drawGraphic()

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
        config['imageStorage'] = {'path': '.', 'basename': 'baa_progress.jpg', 'useDate': True}
        config['targets'] = {'set':False, 'year':time.strftime('%Y'), 'goal': 0, 'families': 0}
        config['current'] = {'pledged':0, 'collected':0, 'families':0}
        config['type'] = ".png"
        config['style'] = "2DVertical"
        config['displayColor'] = False
        config['border'] = True
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
        self.drawWelcome()

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
        text += "Progress program!  It will draw a "
        text += "graphic indicating the parish's"
        text += "current progress in the Appeal."
        text += "Click the target in the toolbar "
        text += "above to set your goal information, "
        text += "then click the hand icon to enter "
        text += "the current data."
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
        Draws the graphic according to the current data and current settings.
        This method only creates the painter and draws the border, if any, the
        heading and sub-heading then farms out the rest of the work to the 
        methods for drawing the chosen style of indicator.
        :return: None
        """
        painter = QPainter(self.image)
        imageWidth = self.image.width()
        imageHeight = self.image.height()
        # gap = 35        # used to set the vertical spacing between elements

        # draw background
        painter.setPen(self.pens['no_pen'])
        painter.setBrush(self.config['imageBackground'])
        painter.drawRect(0, 0, imageWidth, imageHeight)
        if self.config['border']:
            painter.setPen(self.pens['border_pen'])
            painter.pen().setWidth(10)
            penWidth = painter.pen().width()
            print('penWidth = ', penWidth)
            painter.drawRect(0, 0, imageWidth-penWidth, imageHeight-penWidth)

        # draw heading prefix
        painter.setFont(self.fonts['prefixFont'])
        textRect = painter.fontMetrics().boundingRect(self.config['heading_prefix'])
        textWidth = textRect.width()
        textHeight = textRect.height()
        verticalPosition = imageHeight * (textHeight/imageHeight) - textHeight
        drawRect = painter.boundingRect((imageWidth - textWidth)/2, verticalPosition, textWidth, textHeight,
                                        Qt.AlignCenter, self.config['heading_prefix'])
        painter.drawText(drawRect, Qt.AlignCenter, self.config['heading_prefix'])
        verticalPosition += textHeight

        # draw heading
        painter.setFont(self.fonts['headingFont'])
        textRect = painter.fontMetrics().boundingRect(self.config['heading'])
        drawRect = painter.boundingRect((imageWidth - textRect.width())/2, verticalPosition,
                                        textRect.width(), textRect.height(),
                                        Qt.AlignCenter, self.config['heading'])
        painter.drawText(drawRect, Qt.AlignCenter, self.config['heading'])
        verticalPosition += textRect.height()

        # draw target goal text
        painter.setFont(self.fonts['captionFont'])
        text = 'Target Goal: ' + helperFunctions.decimalFormat(self.config['targets']['goal'], 'dollars')
        textRect = painter.fontMetrics().boundingRect(text)
        drawRect = painter.boundingRect((imageWidth - textRect.width())/2, verticalPosition,
                                        textRect.width(), textRect.height(),
                                        Qt.AlignCenter, text)
        painter.drawText(drawRect, Qt.AlignCenter, text)
        verticalPosition += textRect.height()       # set to bottom of textRect, extra spacing added according to style

        # draw current style of indicators
        currentStyle = self.config['style']
        if currentStyle == '2DHorizontal':
            self.horizontalIndicators(painter, '2D', verticalPosition)
        elif currentStyle == '3DHorizontal':
            self.horizontalIndicators(painter, '3D', verticalPosition)
        elif currentStyle == '2DVertical':
            self.verticalIndicators(painter, '2D', verticalPosition)
        elif currentStyle == '3DVertical':
            self.verticalIndicators(painter, '3D', verticalPosition)
        elif currentStyle == 'Guages':
            self.guageIndicators(painter, verticalPosition)
        else:
            msg = "Hmm... The program is calling for a style of display that it does not know how to draw."
            msg += "That shouldn't have happened! Try renaming your config.cfg file, which is in the same directory"
            msg += "as the program and then restart the program. You will have to re-enter the target information and"
            msg += "current data and re-adjust the settings to your liking."
            QMessageBox.critical(self, "Style Error", msg)

        self.drawingBoard.setPixmap(QPixmap.fromImage(self.image))

    def horizontalIndicators(self, painter, style, verticalPosition):
        """
        Draws all three horizontal indicators in vertical order: pledged, collected and families participating from top
        to bottom according to the style selected in 'style'
        :param style: a string, either '2D' or '3D' to control the style of the indicator
        :return: None
        """
        gap = 35  # vertical spacing increment
        verticalPosition += gap
        drawingWidth = (self.image.width() - 2 * gap)       # gives a margin on each side equal to the gap
        drawingHeight = (self.image.height() - verticalPosition - 3 * gap) / 3

        values, percents, modifiers = self.getIndicatorInfo()
        pledgedString, collectedString, familiesString = values
        pledgePercent, collectedPercent, familiesPercent = percents
        pledgeModifier, collectedModifier, familiesModifier = modifiers
        pledgeCaption = 'Pledged: ' + pledgedString + ' = ' + pledgeModifier + str(pledgePercent) + '%'
        collectedCaption = 'Collected: ' + collectedString + ' = ' + collectedModifier + str(collectedPercent) + '%'
        familiesCaption = 'Participating Families: ' + familiesString + ' = ' + \
                          familiesModifier + str(familiesPercent) + '%'

        if self.config['displayColor']:
            self.drawHorizontalIndicator(painter, style, 'red', pledgeCaption, pledgePercent,
                                         verticalPosition, drawingWidth, drawingHeight)
            verticalPosition += drawingHeight + gap

            self.drawHorizontalIndicator(painter, style, 'green', collectedCaption, collectedPercent,
                                         verticalPosition, drawingWidth, drawingHeight)
            verticalPosition += drawingHeight + gap

            self.drawHorizontalIndicator(painter, style, 'blue', familiesCaption, familiesPercent,
                                          verticalPosition, drawingWidth, drawingHeight)
        else:
            self.drawHorizontalIndicator(painter, style, 'gray', pledgeCaption, pledgePercent,
                                         verticalPosition, drawingWidth, drawingHeight)
            verticalPosition += drawingHeight + gap

            self.drawHorizontalIndicator(painter, style, 'gray', collectedCaption, collectedPercent,
                                         verticalPosition, drawingWidth, drawingHeight)
            verticalPosition += drawingHeight + gap

            self.drawHorizontalIndicator(painter, style, 'gray', familiesCaption, familiesPercent,
                                         verticalPosition, drawingWidth, drawingHeight)

    def drawHorizontalIndicator(self, painter, style, color, caption, percent, startY, width, height):
        """
        Draws the current horizontal indicator with the given parameters
        :param painter: the painter being used to draw
        :param style: a string: '2D' or '3D'
        :param color: currently a string 'red', 'green', 'blue' or 'gray' indicating the color of the indicator
        :param caption: a string that will appear as the caption under the drawing
        :param percent: an integer indicating the amount of the bar to fill in
        :param vert: an integer indicating the vertical position
        :param width: an integer indicating the width to draw the indicator
        :param height: an integer indicating the height for the indicator and caption
        :return: None
        """
        painter.setFont(self.fonts['captionFont'])
        fontMetrics = painter. fontMetrics()
        radius = (height - fontMetrics.height())/2
        startX = (self.image.width() - width)/2 + radius
        endX = (self.image.width() + width)/2 - radius
        startCapRect = QRectF(startX - radius, startY, 2 * radius, 2 * radius)
        endCapRect = QRectF(endX - radius, startY, 2 * radius, 2 * radius)
        if percent > 100:
            percent = 100       # assure the indicator bar does not exceed the end of the indicator itself
        centralRect = QRectF(startX, startY, percent * (endX - startX) / 100, 2 * radius)
        captionRect = QRectF(startX, startY + 2 * radius + 10, endX - startX, fontMetrics.height())

        if style == '2D':
            brush1 = self.fills['black_brush']
            brush2 = self.fills['black_brush']
            brush3 = self.fills['gray_brush']

        elif style == '3D':
            if color == 'red':
                gradient1 = self.fills['red_radial_gradient']
                gradient2 = self.fills['red_linear_gradient']
            elif color == 'green':
                gradient1 = self.fills['green_radial_gradient']
                gradient2 = self.fills['green_linear_gradient']
            elif color == 'blue':
                gradient1 = self.fills['blue_radial_gradient']
                gradient2 = self.fills['blue_linear_gradient']
            elif color == 'gray':
                gradient1 = self.fills['gray_radial_gradient']
                gradient2 = self.fills['gray_linear_gradient']
            else:
                msg = "There has been an unexpected error."
                QMessageBox.critical(self, "Color Error", msg)

            # set brushes to gradients
            brush1 = gradient1
            brush1.setCenter(startX, startY + radius)
            brush1.setRadius(radius)
            brush1.setFocalPoint(startX, startY + radius - 0.33 * radius)
            brush2 = QRadialGradient(gradient1)
            brush2.setCenter(endX, startY + radius)
            brush2.setRadius(radius)
            brush2.setFocalPoint(endX, startY + radius - 0.33 * radius)
            brush3 = gradient2
            brush3.setStart(startX, startY)
            brush3.setFinalStop(startX, startY + 2 * radius)

        # draw the indicator
        # first the fill
        painter.setBrush(brush1)
        painter.setPen(self.pens['no_pen'])
        painter.drawChord(startCapRect, 90 * 16, 180 * 16)
        painter.setBrush(brush2)
        painter.drawChord(endCapRect, 90 * 16, -180 * 16)
        painter.setBrush(brush3)
        painter.drawRect(centralRect)

        # then the outline
        painter.setPen(self.pens['outline_pen'])
        painter.drawArc(startCapRect, 90 * 16, 180 * 16)
        painter.drawLine(startX, startY, endX, startY)
        painter.drawLine(startX, startY + 2* radius, endX, startY + 2* radius)
        painter.drawArc(endCapRect, 90 * 16, -180 * 16)

        # draw the caption
        startY += centralRect.height() + 10
        painter.setPen(self.pens['border_pen'])
        drawRect = painter.boundingRect(captionRect, Qt.AlignCenter, caption)
        painter.drawText(drawRect, Qt.AlignCenter, caption)


    def verticalIndicators(self, painter, style, verticalPosition):
        # """
        # Draws all three vertical indicators in horizontal order: pledged, collected and families participating from
        # left to right according to the style selected in 'style'
        # :param style: a string, either '2D' or '3D' to control the style of the indicator
        # :return: None
        # """
        gap = 35  # horizontal and vertical spacing increment
        verticalPosition += gap     # move down a little from the heading
        drawingWidth = (self.image.width() - 4 * gap)/3       # since total image width = three images and four gaps
        drawingHeight = (self.image.height() - verticalPosition) - gap / 2  # saves a little space at the bottom too

        values, percents, modifiers = self.getIndicatorInfo()
        pledgedString, collectedString, familiesString = values
        pledgePercent, collectedPercent, familiesPercent = percents
        pledgeModifier, collectedModifier, familiesModifier = modifiers
        pledgeCaption = pledgedString + '\n' + 'Pledged\n' + pledgeModifier + '(' + str(pledgePercent) + '%)'
        collectedCaption = collectedString + ' \n' + 'Collected\n'  + '(' + collectedModifier \
                           + str(collectedPercent) + '%)'
        familiesCaption = familiesString + '\n' + 'Families\n' + \
                          '(' + familiesModifier + str(familiesPercent) + '%)'

        horizontalPosition = gap
        if self.config['displayColor']:
            self.drawVerticalIndicator(painter, style, 'red', pledgeCaption, pledgePercent,
                                         horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
            horizontalPosition += drawingWidth + gap

            self.drawVerticalIndicator(painter, style, 'green', collectedCaption, collectedPercent,
                                         horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
            horizontalPosition += drawingWidth + gap

            self.drawVerticalIndicator(painter, style, 'blue', familiesCaption, familiesPercent,
                                          horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
        else:
            self.drawVerticalIndicator(painter, style, 'gray', pledgeCaption, pledgePercent,
                                         horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
            horizontalPosition += drawingWidth + gap

            self.drawVerticalIndicator(painter, style, 'gray', collectedCaption, collectedPercent,
                                         horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
            horizontalPosition += drawingWidth + gap

            self.drawVerticalIndicator(painter, style, 'gray', familiesCaption, familiesPercent,
                                         horizontalPosition, verticalPosition, drawingWidth, drawingHeight)

    def drawVerticalIndicator(self, painter, style, color, caption, percent, startX, startY, width, height):
        """
        Draws the current horizontal indicator with the given parameters
        :param painter: the painter being used to draw
        :param style: a string: '2D' or '3D'
        :param color: currently a string 'red', 'green', 'blue' or 'gray' indicating the color of the indicator
        :param caption: a string that will appear as the caption under each drawing
        :param percent: an integer indicating the amount of the bar to fill in
        :param startY: an integer indicating the top of the drawings
        :param width: an integer indicating the width of the containing rectangle
        :param height: an integer indicating the height for the indicator and caption
        :return: None
        """
        # startX = (self.image.width() - width) / 2
        # #        startX = self.image.width() / 10        # the horizontal starting point of the central rectangle
        painter.setFont(self.fonts['smallCaptionFont'])
        fontMetrics = painter.fontMetrics()
        captionHeight = fontMetrics.boundingRect(QRect(0, 0, 640, 480),  # text should fit easily within this QRect
                                                 Qt.AlignHCenter,
                                                 'M\nM\nM').height() + 10 # allows for 4-line families caption + 10 px
        indicatorHeight = height - captionHeight
        radius = indicatorHeight / 10
        bulb_center = QPointF(startX + width / 2, startY + indicatorHeight - radius)
        tube_left = startX + (width - radius) / 2
        tube_right = tube_left + radius     # since bulb ends at 90 +/- 30 we have 30 - 60 - 90 triangle
        tube_top = startY + radius / 2      # tube is one radius in width
        tube_bottom = tube_top + indicatorHeight - 1.5 * radius - radius * 1.732 / 2   # allow for top cap too
        tube_length = tube_bottom - tube_top
        bulbRectF = QRectF(tube_left - radius / 2, startY + indicatorHeight - 2 * radius, 2 * radius, 2 * radius)
        if percent > 100:
            percent = 100
        mercury_length = percent * (tube_length)/100
        tubeRectF = QRectF(tube_left, tube_top + tube_length - mercury_length, radius, mercury_length)
        capRectF = QRectF(tube_left, tube_top - radius / 2, radius, radius)

        if style == '2D':
            if color == 'red':
                bulbBrush = self.fills['darkRed_brush']
                mercuryBrush = self.fills['red_brush']
            elif color == 'green':
                bulbBrush = self.fills['darkGreen_brush']
                mercuryBrush = self.fills['green_brush']
            elif color == 'blue':
                bulbBrush = self.fills['darkBlue_brush']
                mercuryBrush = self.fills['blue_brush']
            else:
                bulbBrush = self.fills['darkGray_brush']
                mercuryBrush = self.fills['gray_brush']
        elif style == '3D':
            if color == 'red':
                bulbGradient = self.fills['red_radial_gradient']
                mercuryGradient = self.fills['red_linear_gradient']
            elif color == 'green':
                bulbGradient = self.fills['green_radial_gradient']
                mercuryGradient = self.fills['green_linear_gradient']
            elif color == 'blue':
                bulbGradient = self.fills['blue_radial_gradient']
                mercuryGradient = self.fills['blue_linear_gradient']
            else:
                bulbGradient = self.fills['gray_radial_gradient']
                mercuryGradient = self.fills['gray_linear_gradient']

            # set 3D brushes to gradients
            bulbBrush = bulbGradient
            bulbBrush.setCenter(bulb_center.x(), bulb_center.y())
            bulbBrush.setRadius(radius)
            bulbBrush.setFocalPoint(bulb_center.x() - radius / 2, bulb_center.y() - radius / 2)
            capBrush = QRadialGradient(bulbGradient)
            capBrush.setCenter(startX + width / 2, tube_top)
            capBrush.setFocalPoint(startX + width / 2 - 0.17 * radius, tube_top)
            mercuryBrush = mercuryGradient
            mercuryBrush.setStart(tube_left, tube_top)
            mercuryBrush.setFinalStop(tube_right, tube_top)

        # draw the indicator

        # first draw the bulb
        painter.setPen(self.pens['no_pen'])
        painter.setBrush(bulbBrush)
        painter.drawChord(bulbRectF, 60 * 16, -300 * 16)

        # now draw the tube
        painter.setBrush(mercuryBrush)
        painter.drawRect(tubeRectF)

        # finally draw the cap if percent is 100 or more
        if percent >= 100:
            painter.setBrush(capBrush)
            painter.drawChord(capRectF, 0, 180 * 16)

        # draw the outline
        painter.setPen(self.pens['outline_pen'])
        painter.drawArc(bulbRectF, 60 * 16, -300 * 16)
        painter.drawLine(tube_left, tube_top, tube_left, tube_bottom)
        painter.drawLine(tube_right, tube_top, tube_right, tube_bottom)
        painter.drawArc(capRectF, 0, 180 * 16)

        # draw the caption
        captionTop = startY + indicatorHeight
        painter.setPen(self.pens['border_pen'])
        captionRect = QRectF(startX, captionTop, width, captionHeight)
        drawRect = painter.boundingRect(captionRect, Qt.AlignCenter, caption)
        painter.drawText(drawRect, Qt.AlignCenter, caption)

    def guageIndicators(self, painter, verticalPosition):
        print('Got to guage indicators.')

    def getIndicatorInfo(self):
        """
        Computes several values that are used in all of the images defined above
        :return: A tuple of tuples, the first containing value strings, possibly converted to monetary format
                the second containing percent values rounded off to one decimal place,
                the third the modifier strings that may be needed if the amounts are near or over 100%
        """
        goal = float(self.config['targets']['goal'])
        pledged = float(self.config['current']['pledged'])
        pledgedString = helperFunctions.decimalFormat(pledged, 'dollars')
        collected = float(self.config['current']['collected'])
        collectedString = helperFunctions.decimalFormat(collected, 'dollars')
        totalFamilies = self.config['targets']['families']
        participatingFamilies = self.config['current']['families']
        familiesString = str(participatingFamilies) + ' of ' + str(totalFamilies)
        pledgePercent = int(pledged * 1000/goal + 0.5)/10
        collectedPercent = int(collected * 1000/goal + 0.5)/10
        familiesPercent = int(participatingFamilies * 1000/totalFamilies + 0.5)/10

        pledgeModifier = ''
        if pledgePercent == 100.0:
            if pledged < goal: pledgeModifier = 'almost '
            if pledged > goal: pledgeModifier = 'over '

        collectedModifier = ''
        if collectedPercent == 100.0:
            if collected < goal: collectedModifier = 'almost '
            if collected > goal: collectedModifier = 'over '

        familiesModifier = ''
        if familiesPercent == 100.0:
            if participatingFamilies < totalFamilies: familiesModifier = 'almost '
            if participatingFamilies > totalFamilies: familiesModifier =  'over '

        return ( (pledgedString, collectedString, familiesString), # value strings
                 (pledgePercent, collectedPercent, familiesPercent), # percents
                 (pledgeModifier, collectedModifier, familiesModifier) # modifiers
               )

    def setTargets(self):
        dlg = EditTargetsDlg(self.config["targets"])
        if dlg.exec():
            self.config_changed = True
            self.grantAccess()
            self.drawGraphic()

    def setCurrent(self):
        dlg = EditCurrentValuesDlg(self.config['current'])
        if dlg.exec():
            self.config_changed = True
            self.drawGraphic()

    def saveImage(self):
        print("Got to saveImage")

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
        if self.config_changed:
            result = self.checkForSave()
            if result == QMessageBox.Yes:
                fileDesignation = self.getFileDesignation()
                self.image.save(fileDesignation)
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
        if self.config['imageStorage']['useDate']:
            now = datetime.datetime.now()
            filename = str(now.date()) + '-' + filename
        return path + '/' + filename

    def settings(self):
        dlg = Settings(self.config)
        dlg.exec()


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