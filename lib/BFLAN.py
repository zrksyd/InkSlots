import csv
import struct

def csvParse(csvFile):
    offsets = []
    csvImport = open(csvFile, newline='')
    reader = csv.reader(csvImport, delimiter=',')
    rowNumber = 0
    for row in reader:
        if rowNumber > 0:
            offsetNumber = 0
            rowColors = []
            for offset in row:
                if offsetNumber % 3 == 1:
                    alt = []
                if offsetNumber > 0:
                    alt.append(int(offset))
                    if len(alt) == 3:
                        rowColors.append(tuple(alt))
                else:
                    #print(offset)
                    pass
                offsetNumber += 1
            offsets.append(rowColors)
        rowNumber += 1
    csvImport.close()
    #print(offsets)
    return offsets

def BFLANRead(bflan):
    offsets = csvParse("BFLAN.csv")
    bflanFile = open(bflan,'rb')
    #bflanFile.seek(212)
    #print(bflanFile.read(4))
    i = 0
    j = 0
    print("ANOTHER " + str(j))
    j += 1
    for row in offsets:
        for color in row:
            for offset in color:
                #print("Offset: " + str(offset))
                bflanFile.seek(offset)
                value = struct.unpack('<f', bflanFile.read(4))[0]
                print(int(value))
                if i % 3 == 2:
                    print()
                if i % 24 == 23:
                    print("ANOTHER " + str(j))
                    j += 1
                i += 1
    
    bflanFile.close()
    
BFLANRead("..\input\info_melee_lct_ink_ink_bg.bflan")
#csvParse("BFLAN.csv")
