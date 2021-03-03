import os
import subprocess
from pyprc import *
import xml.etree.ElementTree as ET
import random
if __name__ == "__main__":
    import colorCorrection
else:
    from . import colorCorrection
    
paramLabels = "ParamLabels.csv"

def effectPRCRead(inputPRC):
    os.chdir(os.getcwd() + "\lib")
    xml = inputPRC[0:-4] + ".xml"
    subprocess.call("paramxml " + inputPRC + " -d -o " + xml + " -l " + paramLabels + " > nul", shell=True)
    tree = ET.parse(xml)
    colors = []

    root = tree.getroot()
    for child in root:
        if child.attrib['hash'] == "ink_effect_color":
            index = 0
            for alt in child:
                color = tuple([int(float(alt[i].text) * 256) for i in range(3)])
                '''
                if newColorArray[index] != None:
                    color = newColorArray[index]
                    for i in range(3):
                        alt[i].text = str(color[i] / 256)
                else:
                    color = tuple([int(float(alt[i].text) * 256) for i in range(3)])
                '''
                colors.append(color)
                index += 1

    for child in root:
        if child.attrib['hash'] == "ink_arrow_color":
            index = 0
            for alt in child:
                color = tuple([int(float(alt[i].text) * 256) for i in range(3)])
                colors.append(color)
                index += 1

    #Go back to original directory
    os.chdir("..")
    return colors

def effectPRCRead2(inputPRC):
    os.chdir(os.getcwd() + "\lib")
    colors = []
    root = param(inputPRC)
    hash.load_labels("ParamLabels.csv")
    for child in root:
        if child[0] == hash("ink_effect_color"):
            for alt in child[1]:
                color = []
                for colorType, rgb in alt:
                    color.append(int(rgb.value * 256))
                color=tuple(color)
                colors.append(color)
    os.chdir("..")
    return colors

def effectPRCWrite2(inputPRC, newColorArray):
    os.chdir(os.getcwd() + "\lib")
    colors = []
    root = param(inputPRC)
    hash.load_labels("ParamLabels.csv")
    for child in root:
        if child[0] == hash("ink_effect_color"):
            index = 0
            for alt in child[1]:
                if newColorArray[index] != None:
                    r = newColorArray[index][0] / 255
                    g = newColorArray[index][1] / 255
                    b = newColorArray[index][2] / 255
                    color = param.struct([
                        (hash("r"), param.float(r)),
                        (hash("g"), param.float(g)),
                        (hash("b"), param.float(b))
                    ])
                    alt = color
                    #color = newColorArray[index]
                else:
                    pass
                index += 1
        if child[0] == hash("ink_arrow_color"):
            index = 0
            newColorArray = colorCorrection.multiplySaturation(newColorArray, 1.5)
            newColorArray = colorCorrection.multiplyValue(newColorArray, 1.5)
            for alt in child[1]:
                if newColorArray[index] != None:
                    r = newColorArray[index][0] / 255
                    g = newColorArray[index][1] / 255
                    b = newColorArray[index][2] / 255
                    color = param.struct([
                        (hash("r"), param.float(r)),
                        (hash("g"), param.float(g)),
                        (hash("b"), param.float(b))
                    ])
                    alt = color
                    #color = newColorArray[index]
                else:
                    pass
                index += 1
    root.save("..\output\effect.prc")
    os.chdir("..")
    

#effectPRCRead2(r"..\input\effect.prc")

def effectPRCWrite(inputPRC, newColorArray):
    os.chdir(os.getcwd() + "\lib")
    xml = inputPRC[0:-4] + ".xml"
    subprocess.call("paramxml " + inputPRC + " -d -l " + paramLabels + " > nul", shell=True)
    tree = ET.parse(xml)
    colors = []
    root = tree.getroot()
    for child in root:
        if child.attrib['hash'] == "ink_effect_color":
            index = 0
            for alt in child:
                if newColorArray[index] != None:
                    color = newColorArray[index]
                    for i in range(3):
                        alt[i].text = str(color[i] / 256)
                else:
                    color = tuple([int(float(alt[i].text) * 256) for i in range(3)])
                colors.append(color)
                #print(color)
                index += 1

    #print()

    for child in root:
        if child.attrib['hash'] == "ink_arrow_color":
            for alt in child:
                color = tuple([float(alt[i].text) for i in range(3)])
                colors.append(color)
                #print(color)

    print()
    tree.write(xml)
    subprocess.call("paramxml " + xml + " -a -o ..\output\effect.prc -l " + paramLabels, shell=True)
    os.chdir("..")
    

'''newColorArray = []
for alt in range(8):
    if (random.uniform(0,1) < 2):
        newColorArray.append(tuple([random.randint(0,255) for i in range(3)]))
    else:
        newColorArray.append(None)
effectPRCWrite2("..\input\effect.prc", newColorArray)'''
