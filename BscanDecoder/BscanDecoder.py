import os
from unicodedata import bidirectional
import pandas as pd
import spffield as sF
import bsdl_lib as bL
import ruleschecker as rC

workdir = os.getcwd()

def format_violation(text):
    return "Bscan Rules Violation:[{}]".format(text)

def getSpfPath(prod = ""):
    spfpathList = []
    spfpath = "{}\\SPF{}".format(workdir,prod)
    print("Searching for SPF in Directory: {}\n".format(spfpath))
    for file in os.listdir(spfpath):
        if file.endswith(".spf"):
            print("SPF File detected: {}\n".format(file))
            spfpathList.append(os.path.join(spfpath, file))

    return spfpathList

def readSpfFile(readfilepath):

    print("Reading SPF from path: \n{}\n".format(readfilepath))
    readSpf = open(readfilepath, "r")
    return readSpf

def removeSymbol(text):
    unwantedSym_list = [";","->","\n","\t","\"",",","=",":"]
    for unwantedSym in unwantedSym_list:
        if unwantedSym in text:
            text = text.replace(unwantedSym," ")
    return text

def getFirstWord(text):
    if " " in text: 
        text = text.split(" ")
        return text[0]
    else:
        return text

def processSpf(spffile):
    processSpflist = []
    focus_tap = ""
    print("Running processSpf()")
    for line in spffile:
        #print("Processing line: " + line)
        if line.isspace():
            continue
        elif line.lstrip()[0] == "#":
            continue
        elif getFirstWord(line) == "focus_tap":
            focus_tap = removeSymbol(line).split(" ")[1]
            #processSpflist.append(sF.SpfField(configurationType="focus_tap",focus_tap=focus_tap))
        elif getFirstWord(line) == "set":
            temp_line = removeSymbol(line).split(" ")
            temp_line = [item for item in temp_line if item]
            if len(temp_line) == 4:
                processSpflist.append(sF.SpfField(configurationType="set",focus_tap=focus_tap,register=temp_line[1],field=temp_line[2],write=temp_line[3]))
            elif len(temp_line) == 3:
                processSpflist.append(sF.SpfField(configurationType="set",focus_tap=focus_tap,register=temp_line[1],write=temp_line[2]))
        elif getFirstWord(line) == "execute":
            temp_line = removeSymbol(line).split(" ")
            temp_line = [item for item in temp_line if item]
            processSpflist.append(sF.SpfField(configurationType="ir_tdi",focus_tap=focus_tap,register=temp_line[1]))
        elif getFirstWord(line) == "ir_tdi":
            temp_line = removeSymbol(line).split(" ")
            temp_line = [item for item in temp_line if item]
            processSpflist.append(sF.SpfField(configurationType="ir_tdi",focus_tap=focus_tap,register=temp_line[1]))
        elif getFirstWord(line) == "dr_tdi":
            temp_line = removeSymbol(line).split(" ")
            temp_line = [item for item in temp_line if item]
            processSpflist.append(sF.SpfField(configurationType="dr_tdi",write=temp_line[1].replace("'b","")))
        elif getFirstWord(line) == "dr_tdo":
            temp_line = removeSymbol(line).split(" ")
            temp_line = [item for item in temp_line if item]
            processSpflist.append(sF.SpfField(configurationType="dr_tdo",read=temp_line[1].replace("'b","")))
        elif getFirstWord(line) == "cycle":
            temp_line = removeSymbol(line).split(" ")
            temp_line = [item for item in temp_line if item]
            processSpflist.append(sF.SpfField(configurationType="cycle",write=temp_line[1]))
        elif getFirstWord(line) == "label":
            temp_line = removeSymbol(line).split(" ")
            temp_line = [item for item in temp_line if item]
            processSpflist.append(sF.SpfField(configurationType="label",write=temp_line[1]))
        elif "flush" in line:
            processSpflist.append(sF.SpfField(configurationType="flush"))
        elif "vector" in line:
            vectorlist = []
            temp_line = line.split(",")
            vector_line = removeSymbol(temp_line[0]).split(" ")
            try:
                vector_rpt = removeSymbol(temp_line[1]).strip()
            except:
                vector_rpt = "1"
            vector_line = [item for item in vector_line if item]
            vectorlist = vector_line[vector_line.index("vector") + 1:]
            for vector in vectorlist:
                pinvector = vector.split("(")[0]
                vectorvalue = vector.split("(")[1].rstrip(")")
                processSpflist.append(sF.SpfField(configurationType="vector",field = pinvector, write=vectorvalue, rpt=vector_rpt))
        elif getFirstWord(line) == "pass":
            temp_line = line.split("\"")[1]
            if "label:Pin" in temp_line.replace(" ",""):
                processSpflist.append(sF.SpfField(configurationType="pin_label",write = temp_line.rstrip(";")))
            elif "expandata" in temp_line.replace(" ",""):
                scale = removeSymbol(temp_line.split(",")[1].replace(" ",""))
                processSpflist.append(sF.SpfField(configurationType="expandata", write = scale))

    return processSpflist

def getOpcode(filepath):
    df_opcode = pd.read_csv(filepath)
    return list(df_opcode["OPCODE"])

def bsdl2dict(filepath):
    df_bsdl = pd.read_csv(filepath)
    return df_bsdl.to_dict()

def bsdl2obj(filepath):

    bsdl_dict = bsdl2dict(filepath)

    bsdlObjList = []
    for i in range(len(bsdl_dict['num'])):
        bsdlObj = bL.Bsdl()
        bsdlObj.num = i
        bsdlObj.port = bsdl_dict['port'][i].strip()
        bsdlObj.cell = bsdl_dict['cell'][i].strip()
        bsdlObj.function = bsdl_dict['function'][i].strip()
        bsdlObj.safe = bsdl_dict['safe'][i].strip()

        bsdlObjList.append(bsdlObj)

    return bsdlObjList

def mapBSDLInfo(spfObjList,bsdlObjList):

    updatedSpfObjList = []

    opcodelist = getOpcode('bscan_opcode_table.csv')

    for obj in spfObjList:
        if obj.register in opcodelist:
            updatedSpfObjList.append(obj)
            tdi_list = [*spfObjList[spfObjList.index(obj) + 1].write]
            tdo_list = [*spfObjList[spfObjList.index(obj) + 2].read]
            tdi_list.reverse()
            tdo_list.reverse()
            if len(tdi_list) != len(tdo_list):
                print("Error!TDI & TDO Length mismatch")
                return -1
            if len(bsdlObjList) != len(tdi_list):
                print("Warning!BSDL({}) & TDI({}) Length mismatch".format(len(bsdlObjList),len(tdi_list)))
                for i in range (len(tdi_list)):
                    updatedSpfObjList.append(sF.SpfField(configurationType = "dr_tdi/dr_tdo", write = tdi_list[i],  read = tdo_list[i]))
            else:
                for i in range (len(tdi_list)):
                    updatedSpfObjList.append(sF.SpfField(configurationType = "dr_tdi/dr_tdo", field = bsdlObjList[i].port, cell = bsdlObjList[i].cell, function = bsdlObjList[i].function, safe = bsdlObjList[i].safe, write = tdi_list[i],  read = tdo_list[i]))
        elif obj.configurationType == "dr_tdi" or obj.configurationType == "dr_tdo":
            continue
        else:
            updatedSpfObjList.append(obj)

    return updatedSpfObjList

def checkBscanRule(spfObjList, bsdlObjList, mode):
    
    pinlabel_count = sum(obj.is_pinlabel() for obj in spfObjList)
    input_pincount = sum(obj.is_input() for obj in bsdlObjList)
    output_pincount = sum(obj.is_output() for obj in bsdlObjList)
    bidir_pincount = sum(obj.is_bidir() for obj in bsdlObjList)
    observe_pincount = sum(obj.is_observe() for obj in bsdlObjList)
    acrx_pincount = sum(obj.is_ac() for obj in bsdlObjList)

    vectorstrobehigh_count = sum(obj.is_vectorstrobehigh() for obj in spfObjList)
    vectorstrobelow_count = sum(obj.is_vectorstrobelow() for obj in spfObjList)
    vectorforcehigh_count = sum(obj.is_vectorforcehigh() for obj in spfObjList)
    vectorforcelow_count = sum(obj.is_vectorforcelow() for obj in spfObjList)
    bidir_strobe_pincount = sum(obj.is_bidirstrobe() for obj in spfObjList)
    input_strobe_pincount = sum(obj.is_inputstrobe() for obj in spfObjList)
    controlnotsafe_count= sum(obj.is_controlnotsafe() for obj in spfObjList)
    controlsafe_count= sum(obj.is_controlsafe() for obj in spfObjList)
    powernotsafe_count = sum(obj.is_powernotsafe() for obj in spfObjList)
    segmentselnotsafe_count = sum(obj.is_segmentselnotsafe() for obj in spfObjList)
    acrxstrobe_pincount = sum(obj.is_acrxstrobe() for obj in spfObjList)

    ########################################################### Mandatory Check ########################################################################
    if rC.check_expandata(sum(obj.is_expandata() for obj in spfObjList)):
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Expandata not found.")))

    if powernotsafe_count:
        rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Total of ({}) power bit not set to safe.".format(powernotsafe_count))))

    if segmentselnotsafe_count:
        rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Total of ({}) segment_select bit not set to safe.".format(segmentselnotsafe_count))))

    ########################################################### Conditional Check ########################################################################

    if "chain" in mode:
        pass

    elif "input" in mode:

        if rC.check_inputstrobe(input_pincount + bidir_pincount, bidir_strobe_pincount + input_strobe_pincount):
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Input Pin Count and Input TDO Strobe Count mismatch.")))

        if rC.check_inputforce(bidir_strobe_pincount + input_strobe_pincount, vectorforcelow_count + vectorforcehigh_count):
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Input Pin Strobe count ({}) and Vector Forcing Pin count ({}) mismatch.".format(bidir_strobe_pincount + input_strobe_pincount,vectorforcelow_count + vectorforcehigh_count))))
    
        if controlnotsafe_count:
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Total of ({}) control bit not set to safe.".format(controlnotsafe_count))))

        if rC.check_pinlabel(input_strobe_pincount + bidir_strobe_pincount, pinlabel_count):
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Input Pin strobe count ({}) and Pin Label count ({}) mismatch.".format(input_strobe_pincount + bidir_strobe_pincount,pinlabel_count))))
    
    elif "output" in mode:
        if controlsafe_count:
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Total of ({}) control bit set to safe.".format(controlsafe_count))))

        if rC.check_outputstrobe(output_pincount + bidir_pincount + observe_pincount,vectorstrobehigh_count + vectorstrobelow_count):
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("Output Pin Count ({}) and Pin Vector Strobe Count ({}) mismatch.".format(output_pincount + bidir_pincount + observe_pincount, vectorstrobehigh_count + vectorstrobelow_count))))

    elif "pulse" in mode or "train" in mode:
        print("RX pincount:{}, RX strobe:{}".format(acrx_pincount, acrxstrobe_pincount))
        if rC.check_inputstrobe(acrx_pincount, acrxstrobe_pincount):
            rulesFieldList.append(rC.RulesField(spffile = spfName, desc = format_violation("AC RX Pin count ({}) and AC RX Pin strobe count ({}) mismatch.".format(acrx_pincount,acrxstrobe_pincount))))

def obj2DataFrame(objList):
    newDict = []

    for obj in objList:
        newDict.append(obj.__dict__)

    return pd.DataFrame.from_dict(newDict)

def generateExcel(DF):
    print("Generating decoded file. Please wait......")
    outputFilePath = "{}\\DECODED\\{}".format(workdir, prod)
    outputFile = os.path.splitext(spfName)[0]
    outputFile_full = outputFilePath + "\\" + outputFile + "_decoded.xlsx"

    if not os.path.exists(outputFilePath):
        os.makedirs(outputFilePath)
    
    DF.to_excel(outputFile_full)
    print("Decoded SPF generated: {}\n\n".format(outputFile_full))

if __name__ == "__main__":

    prod = ""
    
    rulesFieldList = []

    print("Current Work Directory: {}\n".format(workdir))

    spfPathList = getSpfPath()

    for spfPath in spfPathList:

        spfFile = readSpfFile(spfPath)

        spfName = os.path.basename(spfPath)

        mode = spfName.split(".")[0].split("_")

        spfLineObjList = processSpf(spfFile)

        bsdlObjList = bsdl2obj('bsdl_spreadsheet.csv')

        bsdlMappedObjList = mapBSDLInfo(spfLineObjList,bsdlObjList)
        
        bsdlMappedDF = obj2DataFrame(bsdlMappedObjList)

        generateExcel(bsdlMappedDF)

        checkBscanRule(bsdlMappedObjList,bsdlObjList,mode)

        print("Current progress: ({}/{})\n".format(spfPathList.index(spfPath) + 1,len(spfPathList)))

    RulesDict = obj2DataFrame(rulesFieldList)
    
    reportName = 'Report.xlsx'
    pd.DataFrame.from_dict(RulesDict).to_excel(reportName)

    print("{} generated on {}".format(reportName,workdir))

