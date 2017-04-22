# Module Level Functions-------------------------------------------------------

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

# End of Module Level Functions------------------------------------------------
