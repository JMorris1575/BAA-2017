from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import helperFunctions



def meterIndicators(main, painter, style, verticalPosition):
    """
    Draws all three meter indicators in horizontal order: pledged, collected and families participating from
    left to right according to the style selected in 'style'
    :param style: a string, either '2D' or '3D' to control the style of the indicator
    :return: None
    """

    gap = 20  # horizontal and vertical spacing increment
    verticalPosition += gap  # move down a little from the heading
    drawingWidth = (main.image.width() - 4 * gap) / 3  # since total image width = three images and four gaps
    drawingHeight = (main.image.height() - verticalPosition) - gap / 2  # saves a little space at the bottom too

    values, percents, modifiers = helperFunctions.getIndicatorInfo(main)
    pledgedString, collectedString, familiesString = values
    pledgePercent, collectedPercent, familiesPercent = percents
    pledgeModifier, collectedModifier, familiesModifier = modifiers
    pledgeCaption = pledgedString + '\n' + 'Pledged\n' + pledgeModifier + '(' + str(pledgePercent) + '%)'
    collectedCaption = collectedString + ' \n' + 'Collected\n' + '(' + collectedModifier \
                       + str(collectedPercent) + '%)'
    familiesCaption = familiesString + '\n' + 'Families\n' + \
                      '(' + familiesModifier + str(familiesPercent) + '%)'

    horizontalPosition = gap
    if main.config['displayColor']:
        drawMeterIndicator(main, painter, style, 'red', pledgeCaption, pledgePercent,
                           horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
        horizontalPosition += drawingWidth + gap

        drawMeterIndicator(main, painter, style, 'green', collectedCaption, collectedPercent,
                           horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
        horizontalPosition += drawingWidth + gap

        drawMeterIndicator(main, painter, style, 'blue', familiesCaption, familiesPercent,
                           horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
    else:
        drawMeterIndicator(main, painter, style, 'gray', pledgeCaption, pledgePercent,
                           horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
        horizontalPosition += drawingWidth + gap

        drawMeterIndicator(main, painter, style, 'gray', collectedCaption, collectedPercent,
                           horizontalPosition, verticalPosition, drawingWidth, drawingHeight)
        horizontalPosition += drawingWidth + gap

        drawMeterIndicator(main, painter, style, 'gray', familiesCaption, familiesPercent,
                           horizontalPosition, verticalPosition, drawingWidth, drawingHeight)

def drawMeterIndicator(main, painter, style, color, caption, percent, startX, startY, width, height):
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

    # Calculate drawing parameters
    painter.setFont(main.fonts['captionFont'])
    fontMetrics = painter.fontMetrics()
    captionHeight = fontMetrics.boundingRect(QRect(0, 0, 640, 480),  # text should fit easily within this QRect
                                              Qt.AlignHCenter,
                                              'M\nM\nM').height() + 10  # allows for 4-line families caption + 10 px
    indicatorHeight = height - 2 * captionHeight
    meterTop = startY + captionHeight / 2
    pivotPoint = QPoint(startX + width / 2, meterTop + indicatorHeight * 0.7 + 10)
    meterBaseTop = pivotPoint.y() - 10
    if percent > 100:
        percent = 100
    needleLength = pivotPoint.y() - meterTop - 30
    needleAngle = 135 - 90 * percent/100
    needleEndpoint = helperFunctions.getPointPolar(pivotPoint, needleLength, needleAngle)

    # Draw Meter
    painter.setPen(main.pens['border_pen'])
    painter.drawRoundedRect(startX, meterTop, width, indicatorHeight, 15.0, 15.0)
    painter.setBrush(main.fills['black_brush'])
    painter.drawRoundedRect(startX, meterBaseTop, width, indicatorHeight * 0.3, 15.0, 15.0)
    painter.drawRect(startX, meterBaseTop, width, 15)
    painter.drawEllipse(pivotPoint.x()-20, pivotPoint.y()-20, 40, 40)
    painter.setBrush(main.fills['white_brush'])
    painter.setPen(main.pens['outline_pen'])
    for displayPercent in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        angle = 135 - 90 * displayPercent/100
        p1 = helperFunctions.getPointPolar(pivotPoint, needleLength, angle)
        p2 = helperFunctions.getPointPolar(pivotPoint, needleLength + 10, angle)
        painter.drawLine(p1, p2)

    painter.drawLine(pivotPoint, needleEndpoint)



    # Draw caption
    captionTop = startY + indicatorHeight + captionHeight/2
    captionRect = QRectF(startX, captionTop, width, captionHeight)
    drawRect = painter.boundingRect(captionRect, Qt.AlignCenter, caption)
    painter.drawText(drawRect, Qt.AlignCenter, caption)



    # mercury_length = percent * (tube_length) / 100
    # tubeRectF = QRectF(tube_left, tube_top + tube_length - mercury_length, radius, mercury_length)
    # capRectF = QRectF(tube_left, tube_top - radius / 2, radius, radius)
    #
    # if style == '2D':
    #     if color == 'red':
    #         bulbBrush = main.fills['darkRed_brush']
    #         mercuryBrush = main.fills['red_brush']
    #     elif color == 'green':
    #         bulbBrush = main.fills['darkGreen_brush']
    #         mercuryBrush = main.fills['green_brush']
    #     elif color == 'blue':
    #         bulbBrush = main.fills['darkBlue_brush']
    #         mercuryBrush = main.fills['blue_brush']
    #     else:
    #         bulbBrush = main.fills['darkGray_brush']
    #         mercuryBrush = main.fills['gray_brush']
    # elif style == '3D':
    #     if color == 'red':
    #         bulbGradient = main.fills['red_radial_gradient']
    #         mercuryGradient = main.fills['red_linear_gradient']
    #     elif color == 'green':
    #         bulbGradient = main.fills['green_radial_gradient']
    #         mercuryGradient = main.fills['green_linear_gradient']
    #     elif color == 'blue':
    #         bulbGradient = main.fills['blue_radial_gradient']
    #         mercuryGradient = main.fills['blue_linear_gradient']
    #     else:
    #         bulbGradient = main.fills['gray_radial_gradient']
    #         mercuryGradient = main.fills['gray_linear_gradient']
    #
    #     # set 3D brushes to gradients
    #     bulbBrush = bulbGradient
    #     bulbBrush.setCenter(bulb_center.x(), bulb_center.y())
    #     bulbBrush.setRadius(radius)
    #     bulbBrush.setFocalPoint(bulb_center.x() - radius / 2, bulb_center.y() - radius / 2)
    #     capBrush = QRadialGradient(bulbGradient)
    #     capBrush.setCenter(startX + width / 2, tube_top)
    #     capBrush.setFocalPoint(startX + width / 2 - 0.17 * radius, tube_top)
    #     mercuryBrush = mercuryGradient
    #     mercuryBrush.setStart(tube_left, tube_top)
    #     mercuryBrush.setFinalStop(tube_right, tube_top)
    #
    # # draw the indicator
    #
    # # first draw the bulb
    # painter.setPen(main.pens['no_pen'])
    # painter.setBrush(bulbBrush)
    # painter.drawChord(bulbRectF, 60 * 16, -300 * 16)
    #
    # # now draw the tube
    # painter.setBrush(mercuryBrush)
    # painter.drawRect(tubeRectF)
    #
    # # finally draw the cap if percent is 100 or more
    # if percent >= 100:
    #     painter.setBrush(capBrush)
    #     painter.drawChord(capRectF, 0, 180 * 16)
    #
    # # draw the outline
    # painter.setPen(main.pens['outline_pen'])
    # painter.drawArc(bulbRectF, 60 * 16, -300 * 16)
    # painter.drawLine(tube_left, tube_top, tube_left, tube_bottom)
    # painter.drawLine(tube_right, tube_top, tube_right, tube_bottom)
    # painter.drawArc(capRectF, 0, 180 * 16)
    #
    # # draw the caption
    # captionTop = startY + indicatorHeight
    # painter.setPen(main.pens['border_pen'])
    # captionRect = QRectF(startX, captionTop, width, captionHeight)
    # drawRect = painter.boundingRect(captionRect, Qt.AlignCenter, caption)
    # painter.drawText(drawRect, Qt.AlignCenter, caption)
