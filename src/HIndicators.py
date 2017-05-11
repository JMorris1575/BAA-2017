from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import helperFunctions


def horizontalIndicators(main, painter, style, verticalPosition):
    """
    Draws all three horizontal indicators in vertical order: pledged, collected and families participating from top
    to bottom according to the style selected in 'style'
    :param style: a string, either '2D' or '3D' to control the style of the indicator
    :return: None
    """
    gap = 35  # vertical spacing increment
    verticalPosition += gap
    drawingWidth = (main.image.width() - 2 * gap)  # gives a margin on each side equal to the gap
    drawingHeight = (main.image.height() - verticalPosition - 3 * gap) / 3

    values, percents, modifiers = helperFunctions.getIndicatorInfo()
    pledgedString, collectedString, familiesString = values
    pledgePercent, collectedPercent, familiesPercent = percents
    pledgeModifier, collectedModifier, familiesModifier = modifiers
    pledgeCaption = 'Pledged: ' + pledgedString + ' = ' + pledgeModifier + str(pledgePercent) + '%'
    collectedCaption = 'Collected: ' + collectedString + ' = ' + collectedModifier + str(collectedPercent) + '%'
    familiesCaption = 'Participating Families: ' + familiesString + ' = ' + \
                      familiesModifier + str(familiesPercent) + '%'

    if main.config['displayColor']:
        drawHorizontalIndicator(main, painter, style, 'red', pledgeCaption, pledgePercent,
                                verticalPosition, drawingWidth, drawingHeight)
        verticalPosition += drawingHeight + gap

        drawHorizontalIndicator(main, painter, style, 'green', collectedCaption, collectedPercent,
                                verticalPosition, drawingWidth, drawingHeight)
        verticalPosition += drawingHeight + gap

        drawHorizontalIndicator(main, painter, style, 'blue', familiesCaption, familiesPercent,
                                verticalPosition, drawingWidth, drawingHeight)
    else:
        drawHorizontalIndicator(main, painter, style, 'gray', pledgeCaption, pledgePercent,
                                verticalPosition, drawingWidth, drawingHeight)
        verticalPosition += drawingHeight + gap

        drawHorizontalIndicator(main, painter, style, 'gray', collectedCaption, collectedPercent,
                                verticalPosition, drawingWidth, drawingHeight)
        verticalPosition += drawingHeight + gap

        drawHorizontalIndicator(main, painter, style, 'gray', familiesCaption, familiesPercent,
                                verticalPosition, drawingWidth, drawingHeight)


def drawHorizontalIndicator(caller, painter, style, color, caption, percent, startY, width, height):
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
    painter.setFont(caller.fonts['captionFont'])
    fontMetrics = painter.fontMetrics()
    radius = (height - fontMetrics.height()) / 2
    startX = (caller.image.width() - width) / 2 + radius
    endX = (caller.image.width() + width) / 2 - radius
    startCapRect = QRectF(startX - radius, startY, 2 * radius, 2 * radius)
    endCapRect = QRectF(endX - radius, startY, 2 * radius, 2 * radius)
    if percent > 100:
        percent = 100  # assure the indicator bar does not exceed the end of the indicator itself
    centralRect = QRectF(startX, startY, percent * (endX - startX) / 100, 2 * radius)
    captionRect = QRectF(startX, startY + 2 * radius + 10, endX - startX, fontMetrics.height())

    if style == '2D':
        brush1 = caller.fills['black_brush']
        brush2 = caller.fills['black_brush']
        brush3 = caller.fills['gray_brush']

    elif style == '3D':
        if color == 'red':
            gradient1 = caller.fills['red_radial_gradient']
            gradient2 = caller.fills['red_linear_gradient']
        elif color == 'green':
            gradient1 = caller.fills['green_radial_gradient']
            gradient2 = caller.fills['green_linear_gradient']
        elif color == 'blue':
            gradient1 = caller.fills['blue_radial_gradient']
            gradient2 = caller.fills['blue_linear_gradient']
        elif color == 'gray':
            gradient1 = caller.fills['gray_radial_gradient']
            gradient2 = caller.fills['gray_linear_gradient']
        else:
            msg = "There has been an unexpected error."
            QMessageBox.critical(caller, "Color Error", msg)

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
    painter.setPen(caller.pens['no_pen'])
    painter.drawChord(startCapRect, 90 * 16, 180 * 16)
    painter.setBrush(brush2)
    painter.drawChord(endCapRect, 90 * 16, -180 * 16)
    painter.setBrush(brush3)
    painter.drawRect(centralRect)

    # then the outline
    painter.setPen(caller.pens['outline_pen'])
    painter.drawArc(startCapRect, 90 * 16, 180 * 16)
    painter.drawLine(startX, startY, endX, startY)
    painter.drawLine(startX, startY + 2 * radius, endX, startY + 2 * radius)
    painter.drawArc(endCapRect, 90 * 16, -180 * 16)

    # draw the caption
    startY += centralRect.height() + 10
    painter.setPen(caller.pens['border_pen'])
    drawRect = painter.boundingRect(captionRect, Qt.AlignCenter, caption)
    painter.drawText(drawRect, Qt.AlignCenter, caption)
