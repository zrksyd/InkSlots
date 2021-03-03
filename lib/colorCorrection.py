import colorsys

def gammaCorrect(colors, gamma):
    gammaCorrected = []
    for i in colors:
        if i == None:
            gammaCorrected.append(None)
            continue
        color = []
        for j in i:
            j = round(256 * ((j / 256) ** gamma))
            color.append(j)
        gammaCorrected.append(tuple(color))
    return gammaCorrected

def addHSL(colors, factor, index):
    colorCorrected = []
    for i in colors:
        if i == None:
            colorCorrected.append(None)
            continue
        hsl = list(colorsys.rgb_to_hsv(i[0], i[1], i[2]))
        hsl[index] *= factor
        newColor = list(colorsys.hsv_to_rgb(hsl[0],hsl[1],hsl[2]))
        for rgb in range(len(newColor)):
            newColor[rgb] = int(min(255,newColor[rgb]))
        colorCorrected.append(tuple(newColor))
    return colorCorrected

def multiplyHSL(colors, factor, index):
    colorCorrected = []
    for i in colors:
        if i == None:
            colorCorrected.append(None)
            continue
        hsl = list(colorsys.rgb_to_hsv(i[0], i[1], i[2]))
        hsl[index] *= factor
        newColor = list(colorsys.hsv_to_rgb(hsl[0],hsl[1],hsl[2]))
        for rgb in range(len(newColor)):
            newColor[rgb] = int(min(255,newColor[rgb]))
        colorCorrected.append(tuple(newColor))
    return colorCorrected

def addHue(colors, factor):
    return addHSL(colors, factor, 0)

def addSaturation(colors, factor):
    return addHSL(colors, factor, 1)

def addValue(colors, factor):
    return addHSL(colors, factor, 2)

def multiplyHue(colors, factor):
    return multiplyHSL(colors, factor, 0)

def multiplySaturation(colors, factor):
    return multiplyHSL(colors, factor, 1)

def multiplyValue(colors, factor):
    return multiplyHSL(colors, factor, 2)
