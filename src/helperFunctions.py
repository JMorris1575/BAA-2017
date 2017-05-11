from PyQt5.QtCore import *

import math

def decimalFormat(n, mode=None):
    ns = '{0:.2f}'.format(round(n*1.0, 2)) # ns = string rounded to 2 decimals
    dPart = ns[-3:]     # save the decimal part
    count=0
    fs = ''
    for char in ns[ns.find('.')-1::-1]:
        fs = char + fs
        count += 1
        if count==3:
            fs = ',' + fs
            count = 0
    if fs[0:1] == ',':
        fs = fs[1:]
    if mode == 'dollars':
        fs = '$' + fs + dPart
    elif mode == 'percent':
        fs = fs + dPart + '%'
    return fs

def cleanNumber(inString):
    outString = ""
    for char in inString:
        if char.isnumeric() or char == ".":
            outString += char
    return outString

def String2Num(s):
    numchar = '0123456789.'
    s2 = ''
    for char in s:
        if char in numchar:
            s2 += char
    return(float(s2))

def testForNumbers(nString, numType):
    # tries to convert nString to the indicated numeric type
    # and returns whether it was successful or not
    clean = cleanNumber(nString)
    validNumber = True
    try:
        if numType == 'float':
            float(clean)
        if numType == 'int':
            int(clean)
    except ValueError:
        validNumber = False
    return validNumber

def getIndicatorInfo(main):
    """
    Computes several values that are used in all of the images defined above
    :return: A tuple of tuples, the first containing value strings, possibly converted to monetary format
            the second containing percent values rounded off to one decimal place,
            the third the modifier strings that may be needed if the amounts are near or over 100%
    """
    goal = float(main.config['targets']['goal'])
    pledged = float(main.config['current']['pledged'])
    pledgedString = decimalFormat(pledged, 'dollars')
    collected = float(main.config['current']['collected'])
    collectedString = decimalFormat(collected, 'dollars')
    totalFamilies = main.config['targets']['families']
    participatingFamilies = main.config['current']['families']
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

def getPointPolar(center, length, angle):
    """
    Uses trigonometry to calculate a point given a center point and polar coordinates to the desired point
    :param center: QPoint
    :param length: integer or float
    :param angle: integer or float in degrees
    :return: a Qpoint with the desired x and y coordinates
    """
    return QPoint(center.x() + length * math.cos(math.radians(angle)),
                  center.y() - length * math.sin(math.radians(angle)))
