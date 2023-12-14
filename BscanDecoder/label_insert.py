import os
import BscanDecoder as bD
import bsdlinterpreter as bI
import pandas as pd

class pinlabel:
    def __init__(self,pin,bit):
        self.pin = pin
        self.bit = bit

    def __repr__(self):
        return "Pin:{} Bit:{}".format(self.pin, self.bit)

def labelInsertion(setupObj):

    workdir = setupObj.workdir
    basicPath = setupObj.basicPath
    prod = setupObj.prod

    def getSpfPath():
        spfpathList = []
    
        spfpath = "{}\\{}\\{}".format(workdir,basicPath[1],prod)
        if os.path.isdir(spfpath):
            for file in os.listdir(spfpath):
                if file.endswith(".spf"):
                    spfpathList.append(os.path.join(spfpath, file))
        return spfpathList

    def getBsdl():

        bsdlfilepath = "{}\\{}\\{}".format(workdir, basicPath[0], prod)

        bsdlpath = "{}\\bsdl_spreadsheet.csv".format(bsdlfilepath)

        for file in os.listdir(bsdlfilepath):
            if file.endswith(".bsdl"):
                bsdlpath = "{}\\{}".format(bsdlfilepath,file)
    
        print('Using {} as BSDL reference.\n'.format(bsdlpath))
        return bsdlpath

    def bsdl2obj(filepath):

        bsdlObjList = []

        if filepath.endswith('.csv'):

            bsdlObjList = bI.BSDLInterpreter(filepath).csv2ObjList()

        else:

            bsdlObjList = bI.BSDLInterpreter(filepath).bsdl2ObjList()

        return bsdlObjList    

    def mapPinName(ObjList):

        pinMapPath = "{}\\{}\\{}\\pinfile.csv".format(workdir,basicPath[0], prod)
        if os.path.exists(pinMapPath):

            pinMap_df = pd.read_csv(pinMapPath)
            bsdl_pinlist = pinMap_df["bsdl pin"].to_list()
            rtl_pinlist = pinMap_df["rtl pin"].to_list()
            socket_pinlist = pinMap_df["socket pin"].to_list()
            channel_availability_list = pinMap_df["channel available"].to_list()

            for obj in ObjList:
                for bsdl_pin in bsdl_pinlist:
                    if obj.port.lower() == bsdl_pin.lower():
                        obj.pinmap = rtl_pinlist[bsdl_pinlist.index(bsdl_pin)]
                        obj.socket = socket_pinlist[bsdl_pinlist.index(bsdl_pin)]
                        obj.channel = False if channel_availability_list[bsdl_pinlist.index(bsdl_pin)] == 0 else True
                
                    if obj.differential:
                        if obj.differential.port == bsdl_pin:
                            obj.differential.pinmap = rtl_pinlist[bsdl_pinlist.index(bsdl_pin)]
                            obj.differential.socket = socket_pinlist[bsdl_pinlist.index(bsdl_pin)]
                            obj.differential.channel = False if channel_availability_list[bsdl_pinlist.index(bsdl_pin)] == 0 else True

    spfList = getSpfPath()

    spfNameList = [os.path.basename(option) for option in spfList]

    bD.userInput_module(spfNameList)
    '''
    for index, option in enumerate(spfList):
        print("{}--{}".format(index,os.path.basename(option)))
    '''

    if len(spfList) > 0:
        spf_sel = int(input('Enter your choice: '))
    else:
        print("Force/Peek conversion - FAIL")
        print("No SPF registered. Please follow Product Setup steps to configure the product folder.\n")
        return 0

    if spf_sel == 0:
        return 0

    spfpath = spfList[spf_sel - 1]
    print("SPF select: {}".format(spfpath))

    badlpath = getBsdl()

    bsdlObjLst = bsdl2obj(badlpath)

    mapPinName(bsdlObjLst)

    spffile = open(spfpath, "r")
    readLines = spffile.readlines()
    writeLines = readLines
    pinlabelObjList = []

    for bsdlObj in bsdlObjLst:
        if bsdlObj.is_pin():
            pinlabelObjList.append(pinlabel(pin = bsdlObj.socket, bit = bsdlObj.num))
    
    pinlabel_str = ""
    pinlabelObjList.reverse()
    for pinlabelObj in pinlabelObjList:
        pinlabel_str += "pass itpp \"label:Pin_{}@{};\";\n".format(pinlabelObj.pin, pinlabelObj.bit)

    while(1):
        try:
            insert_line = int(input('Enter line to insert label: '))
            break
        except:
            return 0

    writeLines.insert(insert_line, pinlabel_str)

    folderPath = os.path.join(workdir,basicPath[1],prod,"regen")

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    regenSpf = os.path.join(folderPath, os.path.basename(spfpath))

    with open(regenSpf, "w") as f:
        writeLines = "".join(writeLines)
        f.write(writeLines)      

    print("Label Insertion - PASS.\n New File Path: {}\n".format(regenSpf))

def label_insertion(setupObj):
    if setupObj.prod == 0:
        return 0
    else:
        try:
            labelInsertion(setupObj)
            return 1
        except:
            return -1
