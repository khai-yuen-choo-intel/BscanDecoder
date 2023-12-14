import os
import BscanDecoder as bD
import bsdlinterpreter as bI

class irdr:
    def __init__(self, ir, drtdi, drtdo):
        self.ir = ir
        self.drtdi = drtdi
        self.drtdo = drtdo

    def __repr__(self):
        return "ir:{} tdi:{} tdo:{}".format(self.ir,self.drtdi,self.drtdo)

def readFile(readfilepath):

    print("Reading {} from path: {}\n".format(os.path.basename(readfilepath), os.path.abspath(readfilepath)))
    readfile = open(readfilepath, "r")
    return readfile

def removeSymbol(text):
    unwantedSym_list = [";","->","\n","\t","\"",",","=",":"]
    for unwantedSym in unwantedSym_list:
        if unwantedSym in text:
            text = text.replace(unwantedSym," ")
    return text

def getFirstWord(text):
    text = text.lstrip()
    firstword = text.split(" ")[0]
    return firstword

def getDefaultBit(bsdlObjList):
    bitlist = []

    for bsdlObj in bsdlObjList:
        if bsdlObj.is_power() or bsdlObj.is_segmentsel() or bsdlObj.is_delay():
            bitlist.append(int(bsdlObj.num))

    return bitlist

def getSegmentSelBit(bsdlObjList):
    bitlist = []

    for bsdlObj in bsdlObjList:
        if bsdlObj.is_segmentsel():
            bitlist.append(int(bsdlObj.num))

    return bitlist

def getDelayBit(bsdlObjList):
    bitlist = []

    for bsdlObj in bsdlObjList:
        if bsdlObj.is_delay():
            bitlist.append(int(bsdlObj.num))

    return bitlist

def getPowerBit(bsdlObjList):
    bitlist = []

    for bsdlObj in bsdlObjList:
        if bsdlObj.is_power():
            bitlist.append(int(bsdlObj.num))

    return bitlist

def bsdl2obj(filepath):

    bsdlObjList = []

    if filepath.endswith('.csv'):

        bsdlObjList = bI.BSDLInterpreter(filepath).csv2ObjList()

    else:

        bsdlObjList = bI.BSDLInterpreter(filepath).bsdl2ObjList()

    return bsdlObjList

def derive_ss_spf(setupObj):

    workdir = setupObj.workdir
    basicPath = setupObj.basicPath
    prod = setupObj.prod

    spfpathList = []
    
    spfpath = "{}\\{}\\{}".format(workdir,basicPath[1],prod)
    if os.path.isdir(spfpath):
        for file in os.listdir(spfpath):
            if file.endswith(".spf"):
                spfpathList.append(os.path.join(spfpath, file))

    spfNameList = [os.path.basename(option) for option in spfpathList]

    bD.userInput_module(spfNameList)

    if len(spfpathList) > 0:
        spf_sel = int(input('Enter your choice: '))
    else:
        print("Derive SS SPF - FAIL")
        print("No SPF registered. Please follow Product Setup steps to configure the product folder.\n")
        return 0

    if spf_sel == 0:
        return 0

    spfpath = spfpathList[spf_sel - 1]
    print("SPF select: {}".format(spfpath))

    bsdlfilepath = "{}\\{}\\{}".format(workdir, basicPath[0], prod)

    bsdlpath = "{}\\bsdl_spreadsheet.csv".format(bsdlfilepath)

    for file in os.listdir(bsdlfilepath):
        if file.endswith(".bsdl"):
            bsdlpath = "{}\\{}".format(bsdlfilepath,file)
    
    print('Using {} as BSDL reference.\n'.format(bsdlpath))

    bsdlObjList = bsdl2obj(bsdlpath)

    shortChainBit = getDefaultBit(bsdlObjList)

    segselBit = getSegmentSelBit(bsdlObjList)

    if len(segselBit) < 1:
        print("No Segment Select bit found in BSDL.")
        return 0

    powerBit = getPowerBit(bsdlObjList)

    delayBit = getDelayBit(bsdlObjList)

    spfFile = readFile(spfpath)

    filelines = spfFile.readlines()

    ss_path = "{}\\{}\\{}\\subsystem".format(workdir, basicPath[1], prod)

    if not os.path.exists(ss_path):
        os.makedirs(ss_path)

    rootFileName = os.path.splitext(os.path.basename(spfpath))[0]

    for segsel_index, segsel in enumerate(segselBit):
        
        ssFileName = os.path.join(ss_path,"{}_ss{}.spf".format(rootFileName,segsel_index))

        writefile = open(ssFileName, "w")

        line_to_skip = 0
        for line_num, line in enumerate(filelines):
        #print("Processing line: " + line)
            
            if getFirstWord(line) == "tap_raw_shift":
                fullstring = ''

                while (1):
                    fullstring += filelines[line_num + line_to_skip].strip()
                    if filelines[line_num + line_to_skip].find(';') > 0:
                        break
                    line_to_skip += 1

                irtdi_end_index = fullstring.find(',')
                irtdi_segment = fullstring[fullstring.find(':') + 1: irtdi_end_index].strip()

                if irtdi_end_index > 0:
                    fullstring = fullstring[irtdi_end_index + 1:]
                    drtdi_end_index = fullstring.find(',')
                    end_of_line = fullstring.find(';')
                    if drtdi_end_index < 0:
                        drtdi_segment = fullstring[:end_of_line].strip()
                    else:
                        drtdi_segment = fullstring[:drtdi_end_index].strip()
                        drtdo_segment = fullstring[drtdi_end_index + 1:end_of_line].strip()
                
                    irtdi_value = irtdi_segment[irtdi_segment.find('=') + 1:].strip()
                    drtdi_value = drtdi_segment[drtdi_segment.find('=') + 1:].strip().replace("'b","")
                    drtdo_value = 'X' * len(drtdi_value) if drtdi_end_index < 0 else drtdo_segment[drtdo_segment.find('=') + 1:].strip().replace("'b","")

                    drtdo_list = list(drtdo_value)
                    drtdi_list = list(drtdi_value)
                    drtdi_list.reverse()
                    drtdo_list.reverse()

                    start_bit = delayBit[segsel_index] + 1
                    end_bit = segsel
                    new_tdi = []
                    new_tdo = []

                    if len(drtdi_list) == len(bsdlObjList):
                        for shortbit_index, shortbit in enumerate(shortChainBit):
                            if shortbit == segsel:
                                for i in drtdi_list[start_bit:end_bit]:
                                    new_tdi.append(i)
                                for j in drtdo_list[start_bit:end_bit]:
                                    new_tdo.append(j)
                                new_tdi.append('1')
                                new_tdo.append('X')
                            elif shortbit in powerBit:
                                new_tdi.append('1') if shortChainBit[shortbit_index - 1] == segsel else new_tdi.append('0')
                                new_tdo.append('X')
                            else:
                                new_tdi.append('0')
                                new_tdo.append('X')
                    elif len(drtdi_list) == len(shortChainBit):
                        for shortbit_index, shortbit in enumerate(shortChainBit):
                            if shortbit == segsel:
                                new_tdi.append('1')
                                new_tdo.append('X')
                            elif shortbit in powerBit:
                                new_tdi.append('1') if shortChainBit[shortbit_index - 1] == segsel else new_tdi.append('0')
                                new_tdo.append('X')
                            else:
                                new_tdi.append('0')
                                new_tdo.append('X')

                    new_tdi.reverse()
                    new_tdo.reverse()
                    writefile.write("tap_raw_shift :\nir_tdi = {},\ndr_tdi = 'b{},\ndr_tdo = 'b{};\n".format(irtdi_value,''.join(new_tdi),''.join(new_tdo)))
            else:
                if line_to_skip < 1:
                    writefile.write(line)
                else: 
                    line_to_skip -= 1

        writefile.close()

    return 1

def generate_SS_Spf(setupObj):
    if setupObj.prod == 0:
        return 0
    else:
        try:
            return derive_ss_spf(setupObj)
        except:
            return -1