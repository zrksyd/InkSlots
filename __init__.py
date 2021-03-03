import os
from tkinter import *
from tkinter import filedialog

from lib import PRC
from lib import colorCorrection
import re
colorHexRegex = '^([A-Fa-f0-9]{6})'

ALTS = 8
colors = [None] * ALTS

#BFLAN distance between frames = 0xC
#BFLAN distance between RGB = 0xC0
#BFLAN distance between elements until guage_max = 0x278
#BFLAN emp_bg_01 <--> guage_max = 0x284
#BFLAN guage_max black <--> white = 0x240 = 0xC0 * 3
#BFLAN after guage_max white = 0x278

#BFLAN bg_grd red frame 00 offset: 0x0D4, length 0x4, little-endian float
#BFLAN bg_grd red frame 01 offset: 0x0E0, length 0x4, little-endian float
#BFLAN bg_grd red frame 02 offset: 0x0EC, length 0x4, little-endian float
#BFLAN bg_grd red frame 03 offset: 0x0F8, length 0x4, little-endian float
#BFLAN bg_grd red frame 04 offset: 0x104, length 0x4, little-endian float
#BFLAN bg_grd red frame 05 offset: 0x110, length 0x4, little-endian float
#BFLAN bg_grd red frame 06 offset: 0x11C, length 0x4, little-endian float
#BFLAN bg_grd red frame 07 offset: 0x128, length 0x4, little-endian float
#BFLAN bg_grd red frame 08 offset: 0x134, length 0x4, little-endian float
#BFLAN bg_grd red frame 09 offset: 0x140, length 0x4, little-endian float
#BFLAN bg_grd red frame 10 offset: 0x14C, length 0x4, little-endian float
#BFLAN bg_grd red frame 11 offset: 0x158, length 0x4, little-endian float
#BFLAN bg_grd red frame 12 offset: 0x164, length 0x4, little-endian float
#BFLAN bg_grd red frame 13 offset: 0x170, length 0x4, little-endian float
#BFLAN bg_grd red frame 14 offset: 0x17C, length 0x4, little-endian float

#BFLAN bg_grd green frame 00 offset: 0x194, length 0x4, little-endian float
#BFLAN bg_grd green frame 01 offset: 0x1A0, length 0x4, little-endian float

#BFLAN bg_grd blue frame 00 offset: 0x254, length 0x4, little-endian float
#BFLAN bg_grd blue frame 01 offset: 0x260, length 0x4, little-endian float

#BFLAN csr red frame 00 offset: 0x34C, length 0x4, little-endian float
#BFLAN csr red frame 01 offset: 0x358, length 0x4, little-endian float

#BFLAN csr green frame 00 offset: 0x40C, length 0x4, little-endian float

#BFLAN csr blue frame 00 offset: 0x4CC, length 0x4, little-endian float

#BFLAN guage red frame 00 offset: 0x5C4

root = Tk()
root.title("InkSlots")
root.geometry("280x200")


bools = []
for i in range(ALTS):
    bools.append(BooleanVar())

colorSquares = []
origColors = ["#e25f3b",
    "#3b46e2",
    "#e6bb3b",
    "#9ec83b",
    "#e2468d",
    "#3bb7a6",
    "#b73bc8",
    "#3b3d5f"]
for i in range(ALTS):
    colorSquares.append(Canvas(root, bg=origColors[i], width=10, height=10))


strings = [""] * ALTS

entries = []
for i in range(ALTS):
    entries.append(Entry(root, textvariable=strings[i]))

def inputSpawn(index):
    if (bools[index].get()):
        entries[index].grid(row=index, column=1)
        colorSquares[index].grid(row=index, column=2)
    else:
        entries[index].grid_remove()
        colorSquares[index].grid_remove()

checkBoxes = []
for i in range(ALTS):
    text = 'c' + format(i, '02d')
    check = Checkbutton(root, text = text, variable=bools[i])
    checkBoxes.append(check)

for i in range(ALTS):
  lambdaInputSpawn = lambda x=i: inputSpawn(x)
  checkBoxes[i].config(command=lambdaInputSpawn)

for i in range(ALTS):
    checkBoxes[i].grid(row=i,column=0)

def importColors():
    importedColors = PRC.effectPRCRead2("..\input\effect.prc")
    gammaCorrected = colorCorrection.gammaCorrect(importedColors[0:ALTS], 1.0/2.2)
    for i in range(ALTS):
        rgb = '#%02x%02x%02x' % gammaCorrected[i]
        print(rgb)
        colorSquares[i].config(bg=rgb)


def exportColors():
    for i in range(ALTS):
        color = entries[i].get()
        if len(color) > 0:
            if color[0] != "#":
                color = "#" + color
            colorSquares[i].config(bg=color)
            r = int(color[1:3],16)
            g = int(color[3:5],16)
            b = int(color[5:7],16)
            if (bools[i].get()):
                colors[i] = (r,g,b)
            else:
                colors[i] = None
            gammaCorrected = colorCorrection.gammaCorrect(colors, 2.2)
            #print(gammaCorrected)
            PRC.effectPRCWrite2("..\input\effect.prc", gammaCorrected)



menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Import Colors", command=importColors)
fileMenu.add_command(label="Export Colors", command=exportColors)

#testButton = Button(root, text='Export Colors', command=exportColors)
#testButton.grid(row=8, column=3)
