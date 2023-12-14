import os
import BscanDecoder as bD


class pinvalue:
    def __init__(self,pin,value):
        self.pin = pin
        self.value = value

    def __repr__(self):
        return "Pin:{} Value:{}".format(self.pin, self.value)

def fpConversion(setupObj):

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

    spfList = getSpfPath()

    def removeSymbol(text):
        unwantedSym_list = [";","->","\n","\t","\"",",","=",":"]
        for unwantedSym in unwantedSym_list:
            if unwantedSym in text:
                text = text.replace(unwantedSym,"")
        return text

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

    spffile = open(spfpath, "r")
    readLines = spffile.readlines()
    writeLines = readLines
    pinvalueObjList = []

    for line_num,line in enumerate(readLines):
        if line.isspace():
            continue
        elif line.lstrip()[0] == "#":
            continue
        elif "peek_signal" in line:
            splitline = line.split(" ")
            for idx, i in enumerate(splitline):
                if removeSymbol(i) == "peek_signal":
                    signal = splitline[idx+1]
                    value = removeSymbol(splitline[idx+2])

            try:
                pin = signal.split(".")[-1]
            except:
                pin = signal

            try:
                value = "H" if int(value) == 1 else "L"
            except:
                value = value.split("x")[-1]
                value = "H" if int(value) == 1 else "L"
        
            pinvalueObjList.append(pinvalue(pin,value))
            last_line = line_num

        elif "force_signal" in line:
            splitline = line.split(" ")
            for idx, i in enumerate(splitline):
                if removeSymbol(i) == "force_signal":
                    signal = splitline[idx+1]
                    value = removeSymbol(splitline[idx+2])

            try:
                pin = signal.split(".")[-1]
            except:
                pin = signal

            try:
                value = int(value)
            except:
                value = value.split("x")[-1]
        
            pinvalueObjList.append(pinvalue(pin,value))
            last_line = line_num

        else:
            if len(pinvalueObjList) > 0:
                pinvalue_str = ""
                for pinvalueObj in pinvalueObjList:
                    pinvalue_str += "{}({}) ".format(pinvalueObj.pin,pinvalueObj.value)

                pinvalue_str = "pass itpp \"vector: " + pinvalue_str + ";\";\n"
                writeLines.insert(last_line + 1, pinvalue_str)
                pinvalueObjList.clear()

    if len(pinvalueObjList) > 0:
        pinvalue_str = ""
        for pinvalueObj in pinvalueObjList:
            pinvalue_str += "{}({}) ".format(pinvalueObj.pin,pinvalueObj.value)

        pinvalue_str = "pass itpp \"vector: " + pinvalue_str + ";\";\n"
        writeLines.insert(last_line + 1, pinvalue_str)
        pinvalueObjList.clear()
    #print(pinvalue_str)

    folderPath = os.path.join(workdir,basicPath[1],prod,"regen")

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    regenSpf = os.path.join(folderPath, os.path.basename(spfpath))

    with open(regenSpf, "w") as f:
        writeLines = "".join(writeLines)
        f.write(writeLines)      

    print("Force/Peek conversion - PASS.\n New File Path: {}\n".format(regenSpf))
    
def forcepeek_conversion(setupObj):
    if setupObj.prod == 0:
        return 0
    else:
        try:
            fpConversion(setupObj)
            return 1
        except:
            return -1


