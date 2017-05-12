from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import helperFunctions
import HIndicators, VIndicators, MIndicators

def drawWelcome(main):
    """
    Draws and displays the welcome image the first time the program is used
    :return: None
    """
    painter = QPainter(main.image)
    linePen = QPen()  # default black pen 1 pixel wide
    whiteBrush = QBrush(Qt.white)  # white brush for background of rectangle
    infoFont = QFont('Arial', 12)
    painter.setPen(linePen)
    painter.setBrush(whiteBrush)
    painter.setFont(infoFont)
    painter.drawRect(0, 0, main.image.width() - 1, main.image.height() - 1)
    text = "Welcome to the Bishop's Annual Appeal "
    text += "Progress program!  It will draw a "
    text += "graphic indicating the parish's"
    text += "current progress in the Appeal."
    text += "Click the target in the toolbar "
    text += "above to set your goal information, "
    text += "then click the hand icon to enter "
    text += "the current data."
    textRect = painter.boundingRect(QRectF(0, 0, main.image.width() / 2, main.image.height() / 2),
                                    Qt.AlignLeft | Qt.TextWordWrap,
                                    text)
    textRect.moveCenter(QPointF(main.image.width() / 2, main.image.height() / 2))
    borderRect = textRect.adjusted(-5, -5, 5, 5)
    painter.drawRect(borderRect)
    painter.drawText(textRect, text)
    main.drawingBoard.setPixmap(QPixmap.fromImage(main.image))

def drawGraphic(main):
    """
    Draws the graphic according to the current data and current settings.
    This method only creates the painter and draws the border, if any, the
    heading and sub-heading then farms out the rest of the work to the 
    methods for drawing the chosen style of indicator.
    :return: None
    """
    painter = QPainter(main.image)
    imageWidth = main.image.width()
    imageHeight = main.image.height()
    # gap = 35        # used to set the vertical spacing between elements

    # draw background
    painter.setPen(main.pens['no_pen'])
    painter.setBrush(main.config['imageBackground'])
    painter.drawRect(0, 0, imageWidth, imageHeight)
    painter.setPen(main.pens['border_pen'])
    borderStyle = main.config['border']
    if borderStyle == 'single' or borderStyle == 'double':
        painter.setPen(main.pens['border_pen'])
        painter.pen().setWidth(10)
        penWidth = painter.pen().width()
        painter.drawRect(1, 1, imageWidth-penWidth-2, imageHeight-penWidth-2)
    if borderStyle == 'double':
        painter.drawRect(4, 4, imageWidth-penWidth - 8, imageHeight - penWidth - 8)

    # draw heading prefix
    painter.setFont(main.fonts['prefixFont'])
    textRect = painter.fontMetrics().boundingRect(main.config['heading_prefix'])
    textWidth = textRect.width()
    textHeight = textRect.height()
    verticalPosition = imageHeight * (textHeight/imageHeight) - textHeight + 2
    drawRect = painter.boundingRect((imageWidth - textWidth)/2, verticalPosition, textWidth, textHeight,
                                    Qt.AlignCenter, main.config['heading_prefix'])
    painter.drawText(drawRect, Qt.AlignCenter, main.config['heading_prefix'])
    verticalPosition += textHeight

    # draw heading
    painter.setFont(main.fonts['headingFont'])
    textRect = painter.fontMetrics().boundingRect(main.config['heading'])
    drawRect = painter.boundingRect((imageWidth - textRect.width())/2, verticalPosition,
                                    textRect.width(), textRect.height(),
                                    Qt.AlignCenter, main.config['heading'])
    painter.drawText(drawRect, Qt.AlignCenter, main.config['heading'])
    verticalPosition += textRect.height()

    # draw target goal text
    painter.setFont(main.fonts['captionFont'])
    text = 'Target Goal: ' + helperFunctions.decimalFormat(main.config['targets']['goal'], 'dollars')
    textRect = painter.fontMetrics().boundingRect(text)
    drawRect = painter.boundingRect((imageWidth - textRect.width())/2, verticalPosition,
                                    textRect.width(), textRect.height(),
                                    Qt.AlignCenter, text)
    painter.drawText(drawRect, Qt.AlignCenter, text)
    verticalPosition += textRect.height()       # set to bottom of textRect, extra spacing added according to style

    # draw current style of indicators
    currentStyle = main.config['style']
    if currentStyle == '2DHorizontal':
        HIndicators.horizontalIndicators(main, painter, '2D', verticalPosition)
    elif currentStyle == '3DHorizontal':
        HIndicators.horizontalIndicators(main, painter, '3D', verticalPosition)
    elif currentStyle == '2DVertical':
        VIndicators.verticalIndicators(main, painter, '2D', verticalPosition)
    elif currentStyle == '3DVertical':
        VIndicators.verticalIndicators(main, painter, '3D', verticalPosition)
    elif currentStyle == '2DMeters':
        MIndicators.meterIndicators(main, painter, '2D', verticalPosition)
    elif currentStyle == '3DMeters':
        MIndicators.meterIndicators(main, painter, '3D', verticalPosition)
    elif currentStyle == '2DGuages':
        main.guageIndicators(painter, verticalPosition)
    elif currentStyle == '3DGuages':
        main.guageIndicators(painter, verticalPosition)
    elif currentStyle == '2DPies':
        main.pieIndicators(painter, verticalPosition)
    elif currentStyle == '3DPies':
        main.pieIndicators(painter, verticalPosition)
    else:
        msg = "Hmm... The program is calling for a style of display that it does not know how to draw."
        msg += "That shouldn't have happened! Try renaming your config.cfg file, which is in the same directory"
        msg += "as the program and then restart the program. You will have to re-enter the target information and"
        msg += "current data and re-adjust the settings to your liking."
        QMessageBox.critical(main, "Style Error", msg)

    main.drawingBoard.setPixmap(QPixmap.fromImage(main.image))


