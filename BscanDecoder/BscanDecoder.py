import os
import re
import pandas as pd
import spffield as sF
import bsdlinterpreter as bI
import ruleschecker as rC
import filesetup as fS

workdir = os.getcwd()
os.system("")

def format_violation(text):
    return "Bscan Rules Violation:[{}]".format(text)

def collateral_violation(text):
    return "Collateral Violation:[{}]".format(text)

def print_color(text, color):
    switch = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'cyan':'\033[96m',
        'blue': '\033[34m',
        'orange': '\033[33m',
        }
    color_ansi = switch.get(color)

    print('{}{}{}'.format(color_ansi,text,'\033[00m'))


def quit_program():
    input('Exiting Program. Press any key to exit ..... ')
    quit()

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

def setupBasicFolder():

    basicPath = ['COLLATERAL', 'SPF', 'ITPP']

    print("\nCheck/Create Folder Structure:")

    for path in basicPath:
        folder = "{}\\{}".format(workdir,path)
        if os.path.exists(folder):
            print("BASIC FOLDER {:<20}     ---------------------------- OK".format(path))
            pass
        else:
            os.makedirs(folder)
            print("BASIC FOLDER {:<20}     ---------------------------- CREATED".format(path))

    print("\n")

def getuserinput():

    while(True):
        prodlist = []

        spfFolder = "{}\\SPF".format(workdir)
        itppFolder = "{}\\ITPP".format(workdir)

        for item in list(set(os.listdir(spfFolder) + os.listdir(itppFolder))):
            if os.path.isdir("{}\\{}".format(spfFolder, item)) or os.path.isdir("{}\\{}".format(itppFolder, item)):
                prodlist.append(item)
    
        prodlist.sort()

        optionlist = [prod for prod in prodlist]
    
        optionlist.append("Product Setup")
        optionlist.append("Remove Product")

        for index, option in enumerate(optionlist):
            if option == "Product Setup":
                print_color("{}--{}".format(index,option),'cyan')
            elif option == "Remove Product":
                print_color("{}--{}".format(index,option),'red')
            else:
                print("{}--{}".format(index,option))

        option = int(input('Enter your choice: '))
        if optionlist[option] in prodlist:
            return prodlist[option]
        elif optionlist[option] == "Product Setup":
            fS.FileSetup.setupProduct()
        elif optionlist[option] == "Remove Product":
            fS.FileSetup.removeProduct()
        else:
            print('Wrong input. Please enter a number in the options ...')

def getSpfPath():
    spfpathList = []
    
    spfpath = "{}\\SPF\\{}".format(workdir,prod)
    if os.path.isdir(spfpath):
        print("Searching for SPF in Directory: {}\n".format(spfpath))
        for file in os.listdir(spfpath):
            if file.endswith(".spf"):
                print("SPF File detected: {}".format(file))
                spfpathList.append(os.path.join(spfpath, file))
    
        if len(spfpathList) < 1:
            print("No SPF Detected!!!!")

    else:
        print("SPF Directory ({}) not found !!! \n".format(spfpath))
    print("Total {} SPF detected.\n".format(len(spfpathList)))
    return spfpathList

def getITPPPath():
    itpppathList = []
    itpppath = "{}\\ITPP\\{}".format(workdir,prod)

    if os.path.isdir(itpppath):
        print("Searching for ITPP in Directory: {}\n".format(itpppath))
        if os.path.isdir(itpppath):
            for file in os.listdir(itpppath):
                if file.endswith(".itpp"):
                    print("ITPP File detected: {}".format(file))
                    itpppathList.append(os.path.join(itpppath, file))
    
        if len(itpppathList) < 1:
            print("No ITPP Detected!!!!")

    else:
        print("ITPP Directory ({}) not found !!! \n".format(itpppath))
    print("Total {} ITPP detected.\n".format(len(itpppathList)))
    return itpppathList

def checkCollateralPath():

    commonCollateral_path = "{}\\COLLATERAL\\COMMON".format(workdir)
    customCollateral_path = "{}\\COLLATERAL\\{}".format(workdir,prod)

    collateralPath_list = [commonCollateral_path, customCollateral_path]
    print("Searching for collateral files:")

    collateral_filelist = ['bsdl_spreadsheet.csv','bscan_opcode_table.csv','pinfile.csv','rulesfile.csv']
    compulsory_filelist = ['bsdl_spreadsheet.csv','bscan_opcode_table.csv','rulesfile.csv']
    
    for file in os.listdir(customCollateral_path):
        if file.endswith('.bsdl'):
            collateral_filelist.remove('bsdl_spreadsheet.csv')
            compulsory_filelist.remove('bsdl_spreadsheet.csv')
            collateral_filelist.append(file)
            compulsory_filelist.append(file)
            break

    for collateral_file in collateral_filelist:
        file_found = False
        for collateral_path in collateralPath_list:
            collateral_filepath = "{}\\{}".format(collateral_path, collateral_file)
            if os.path.exists(collateral_filepath):
                file_found = True
        
        if file_found == True:
            print("{:<30} ---------------------------- OK".format(collateral_file))
        else:
            print("{:<30} ---------------------------- Not Found".format(collateral_file))
            if collateral_file in compulsory_filelist:
                print("Compulsory file ({}) not found!!!! Program Exiting.....".format(collateral_file))
                quit_program()

    print("\n")

def getBsdl():

    bsdlfilepath = "{}\\COLLATERAL\\{}".format(workdir, prod)

    bsdlpath = "{}\\bsdl_spreadsheet.csv".format(bsdlfilepath)

    for file in os.listdir(bsdlfilepath):
        if file.endswith(".bsdl"):
            bsdlpath = "{}\\{}".format(bsdlfilepath,file)
    
    print('Using {} as BSDL reference.\n'.format(bsdlpath))
    return bsdlpath


def getOpcode():

    opcodefilepath = "{}\\COLLATERAL\\{}\\bscan_opcode_table.csv".format(workdir,prod)

    opcodefilepath = opcodefilepath if os.path.exists(opcodefilepath) else "{}\\COLLATERAL\\COMMON\\bscan_opcode_table.csv".format(workdir)

    df_opcode = pd.read_csv(opcodefilepath, index_col = 0)
    df_opcode = df_opcode.fillna('')
    df_dict = df_opcode.to_dict()
    return df_dict['OPCODE']

def mapPinName(ObjList):

    pinMapPath = "{}\\COLLATERAL\\{}\\pinfile.csv".format(workdir,prod)
    if os.path.exists(pinMapPath):

        pinMap_df = pd.read_csv(pinMapPath, header = None)
        bsdl_pinlist = pinMap_df[0].to_list()
        reference_pinlist = pinMap_df[1].to_list()

        for obj in ObjList:
            for reference_pin in reference_pinlist:
                if obj.field.lower() == reference_pin.lower():
                    map_pin = bsdl_pinlist[reference_pinlist.index(reference_pin)]
                    obj.pinmap = map_pin  
                    
def readFile(readfilepath):

    print("Reading {} from path: {}\n".format(os.path.basename(readfilepath), os.path.abspath(readfilepath)))
    readfile = open(readfilepath, "r")
    return readfile

def processSpf(spffile):
    processSpflist = []
    focus_tap = ""
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
            processSpflist.append(sF.SpfField(configurationType="execute",focus_tap=focus_tap,register=temp_line[1]))
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
        elif "pass itpp" in line:
            itppline = line[line.find("\"")+1:line.find(";")]
            itppcmd = itppline.split(":")[0].strip()
            itppval = itppline.split(":")[1].strip()

            if itppcmd.lower() == "label" and "Pin_" in itppval:
                pinName = itppval[itppval.find("_")+1:itppval.find("@")]
                processSpflist.append(sF.SpfField(configurationType="pin_label", field = pinName, write = itppval))
            elif "expandata" in itppcmd:
                expandpin = itppval[:itppval.find(",")].strip()
                expandscale = itppval[itppval.find(",")+1:].strip()
                processSpflist.append(sF.SpfField(configurationType="expandata", register = expandpin, write = expandscale))
            elif itppcmd == "scani" :
                processSpflist.append(sF.SpfField(configurationType="scani", register = itppval))
            elif itppcmd == "to_state" :
                processSpflist.append(sF.SpfField(configurationType="to_state", register = itppval))
            elif itppcmd == "scand" :
                tdilist = itppval[:itppval.find(",")].strip()
                tdolist = itppval[itppval.find(",")+1:].strip()
                processSpflist.append(sF.SpfField(configurationType="scand", write= tdilist, read = tdolist))
            elif itppcmd == "vector":
                pinvectorlist = (itppval.split(",")[0]).split(" ")
                try:
                    vector_rpt = itppval.split(",")[1].strip()
                except:
                    vector_rpt = "1"
                for vector in pinvectorlist:
                    pinvector = vector.split("(")[0]
                    vectorvalue = vector[vector.find("(")+1:vector.find(")")]
                    processSpflist.append(sF.SpfField(configurationType="vector",field = pinvector, write=vectorvalue, rpt=vector_rpt))


    return processSpflist

def processItpp(itppfile):
    processItpplist = []

    for line in itppfile:
        if line.isspace():
            continue
        elif line.lstrip()[0] == "#":
            continue
        elif getFirstWord(removeSymbol(line)) == "label":
            if "Pin_" in line and "@" in line:
                itppval = line.split(":")[1].strip()
                processItpplist.append(sF.SpfField(configurationType="pin_label", field = itppval[itppval.find("_")+1:itppval.find("@")], write = itppval))
            else:
                processItpplist.append(sF.SpfField(configurationType="label",write = line.split(":")[1].strip()))
        elif getFirstWord(line) == "expandata:":
            itppval = line.split(":")[1].strip()
            expandpin = removeSymbol(itppval[:itppval.find(",")]).strip()
            expandscale = removeSymbol(itppval[itppval.find(",")+1:]).strip()
            processItpplist.append(sF.SpfField(configurationType="expandata", register = expandpin, write = expandscale))
        elif getFirstWord(line) == "scani:" :
            itppval = removeSymbol(line.split(":")[1]).strip()
            processItpplist.append(sF.SpfField(configurationType="scani", register = itppval))
        #elif "to_state" in line:
            #processItpplist.append(sF.SpfField(configurationType="to_state", register = removeSymbol(line.split(":")[1].strip())))
        elif getFirstWord(line) == "scand:" :
            itppval = line.split(":")[1].strip()
            tdilist = removeSymbol(itppval[:itppval.find(",")]).strip()
            tdolist = removeSymbol(itppval[itppval.find(",")+1:]).strip()
            processItpplist.append(sF.SpfField(configurationType="scand", write= tdilist, read = tdolist))
        elif getFirstWord(line) == "vector:":
            itppval = line.split(":")[1].strip()
            pinvectorlist = (itppval.split(",")[0]).split(" ")
            try:
                vector_rpt = removeSymbol(itppval.split(",")[1].strip())
            except:
                vector_rpt = "1"
            for vector in pinvectorlist:
                pinvector = vector.split("(")[0]
                vectorvalue = vector[vector.find("(")+1:vector.find(")")]
                processItpplist.append(sF.SpfField(configurationType="vector",field = pinvector, write=vectorvalue, rpt=vector_rpt))

    return processItpplist

def bsdl2obj(filepath):

    bsdlObjList = []

    if filepath.endswith('.csv'):

        bsdlObjList = bI.BSDLInterpreter(filepath).csv2ObjList()

    else:

        bsdlObjList = bI.BSDLInterpreter(filepath).bsdl2ObjList()

    return bsdlObjList         

def mapBSDLInfo(spfObjList,bsdlObjList):

    updatedSpfObjList = []
    currentIr = ""
    bscanIRList = list(opcodeDict.keys())

    opcodeList = [opcodeDict[ir].replace("b","") for ir in opcodeDict]

    for obj in spfObjList:
        if obj.register in bscanIRList and obj.configurationType == "ir_tdi":
            currentIr = obj.register
            updatedSpfObjList.append(obj)
            tdi_list = [*spfObjList[spfObjList.index(obj) + 1].write]
            tdo_list = [*spfObjList[spfObjList.index(obj) + 2].read]
            tdi_list.reverse()
            tdo_list.reverse()
            if len(tdi_list) != len(tdo_list):
                print("Error!TDI & TDO Length mismatch")
                updatedSpfObjList.append(sF.SpfField(configurationType = "Error", register = "TDI & TDO Length mismatch", write = tdi_list, read= tdo_list))
            elif len(bsdlObjList) != len(tdi_list):
                print("Warning!BSDL({}) & TDI({}) Length mismatch at opcode({})".format(len(bsdlObjList),len(tdi_list), obj.register))
                for i in range (len(tdi_list)):
                    updatedSpfObjList.append(sF.SpfField(configurationType = "dr_tdi/tdo", write = tdi_list[i],  read = tdo_list[i]))
            else:
                for i in range (len(tdi_list)):
                    for bsdlObj in bsdlObjList:
                        if bsdlObj.num == str(i):
                            bsdlindex = bsdlObjList.index(bsdlObj)
                    updatedSpfObjList.append(sF.SpfField(configurationType = "dr_tdi/tdo-bsdlmapped", register = currentIr, field = bsdlObjList[bsdlindex].port, \
                    cell = bsdlObjList[bsdlindex].cell, function = bsdlObjList[bsdlindex].function, safe = bsdlObjList[bsdlindex].safe, write = tdi_list[i],  read = tdo_list[i]))
        elif obj.configurationType == "dr_tdi" or obj.configurationType == "dr_tdo":
            continue

        elif obj.configurationType == "scani":
            currentIr = obj.register
            if currentIr in opcodeList:
                obj.register = "{}({})".format(obj.register, bscanIRList[opcodeList.index(obj.register)])
            updatedSpfObjList.append(obj)

        elif obj.configurationType == "scand":
            tdi_list =[]
            tdo_list =[]
            if currentIr in opcodeList:  
                tdi_list[:0] = obj.write
                tdo_list[:0] = obj.read
                tdi_list.reverse()
                tdo_list.reverse()
                if len(tdi_list) != len(tdo_list):
                    print("Error!TDI({}) & TDO({}) Length mismatch".format(len(tdi_list),len(tdo_list)))
                    updatedSpfObjList.append(sF.SpfField(configurationType = "Error", register = "TDI & TDO Length mismatch", write = tdi_list, read= tdo_list))
                if len(bsdlObjList) != len(tdi_list):
                    print("Warning!BSDL({}) & TDI({}) Length mismatch at opcode({})".format(len(bsdlObjList),len(tdi_list), currentIr))
                    for i in range (len(tdi_list)):
                        updatedSpfObjList.append(sF.SpfField(configurationType = "scand", write = tdi_list[i],  read = tdo_list[i]))
                else:
                    for i in range (len(tdi_list)):
                        for bsdlObj in bsdlObjList:
                            if bsdlObj.num == str(i):
                                bsdlindex = bsdlObjList.index(bsdlObj)
                        updatedSpfObjList.append(sF.SpfField(configurationType = "scand-bsdlmapped", register = "{}({})".format(currentIr, bscanIRList[opcodeList.index(currentIr)]), \
                        field = bsdlObjList[bsdlindex].port, cell = bsdlObjList[bsdlindex].cell, function = bsdlObjList[bsdlindex].function, safe = bsdlObjList[bsdlindex].safe, write = tdi_list[i],  read = tdo_list[i]))
            elif currentIr in bscanIRList:
                tdi_list[:0] = obj.write
                tdo_list[:0] = obj.read
                tdi_list.reverse()
                tdo_list.reverse()
                if len(tdi_list) != len(tdo_list):
                    print("Error!TDI({}) & TDO({}) Length mismatch".format(len(tdi_list),len(tdo_list)))
                    updatedSpfObjList.append(sF.SpfField(configurationType = "Error", register = "TDI & TDO Length mismatch", write = tdi_list, read= tdo_list))
                if len(bsdlObjList) != len(tdi_list):
                    print("Warning!BSDL({}) & TDI({}) Length mismatch at opcode({})".format(len(bsdlObjList),len(tdi_list), currentIr))
                    for i in range (len(tdi_list)):
                        updatedSpfObjList.append(sF.SpfField(configurationType = "scand", write = tdi_list[i],  read = tdo_list[i]))
                else:
                    for i in range (len(tdi_list)):
                        for bsdlObj in bsdlObjList:
                            if bsdlObj.num == str(i):
                                bsdlindex = bsdlObjList.index(bsdlObj)
                        updatedSpfObjList.append(sF.SpfField(configurationType = "scand-bsdlmapped", register = "{}".format(currentIr), \
                        field = bsdlObjList[bsdlindex].port, cell = bsdlObjList[bsdlindex].cell, function = bsdlObjList[bsdlindex].function, safe = bsdlObjList[bsdlindex].safe, write = tdi_list[i],  read = tdo_list[i]))
            else:
                updatedSpfObjList.append(obj)
        else:
            updatedSpfObjList.append(obj)

    return updatedSpfObjList

def checkBSDLRule(bsdlObjList):

    rulesFieldList = []

    powercell_count = sum(obj.is_power() for obj in bsdlObjList)
    segmentsel_count = sum(obj.is_segmentsel() for obj in bsdlObjList)
    acrx_count = sum(obj.is_acrx() for obj in bsdlObjList)

    if powercell_count == 0:
        rulesFieldList.append(rC.RulesField(spffile = bsdlFile , category = "ERROR", desc = collateral_violation("No Power Cell category found in BSDL. Partial error checking feature impacted.")))

    if segmentsel_count == 0:
        rulesFieldList.append(rC.RulesField(spffile = bsdlFile , category = "ERROR", desc = collateral_violation("No Segment Select Cell category found in BSDL. Partial error checking feature impacted.")))

    if acrx_count == 0:
        rulesFieldList.append(rC.RulesField(spffile = bsdlFile , category = "ERROR", desc = collateral_violation("No AC Input/Observe_only category found in BSDL. Partial error checking feature impacted.")))

    return rulesFieldList

def mandatoryBscanRule():

    rulesFieldList = []

    if not sum(obj.is_expandata() for obj in bsdlMappedObjList):
        rulesFieldList.append(rC.RulesField(spffile = testName, category = "ERROR", desc = format_violation("Expandata not found.")))

    for spfObj in bsdlMappedObjList:
        if spfObj.is_cyclemorethan1000():
            rulesFieldList.append(rC.RulesField(spffile = testName, line = bsdlMappedObjList.index(spfObj) ,category = "WARNING", desc = format_violation("Found high cycle count ({}) .".format(spfObj.is_cyclemorethan1000()))))
        
        if spfObj.is_powernotsafe():
            rulesFieldList.append(rC.RulesField(spffile = testName, line = bsdlMappedObjList.index(spfObj), category = "ERROR", desc = format_violation("Power bit not set to safe.")))

        if spfObj.is_segmentselnotsafe():
            rulesFieldList.append(rC.RulesField(spffile = testName, line = bsdlMappedObjList.index(spfObj), category = "ERROR", desc = format_violation("Segment Select bit not set to safe.")))

    rule_status = 'PASS' if len(rulesFieldList) < 1 else 'FAIL'

    print("Rule BASIC      ---------------------------- {}".format(rule_status))

    return rulesFieldList

def bscanRuleChecker():

    conditionalrulesFieldList = []

    conditionalRuleChecker = rC.conditionalBscanRule(testName, bsdlObjList, bsdlMappedObjList)

    rules_Dict = {
                "1.1": conditionalRuleChecker.Rule1_1, #Rule1.1: Input Pin Strobe Count lesser than Input Pin Count 
                "1.2": conditionalRuleChecker.Rule1_2, #Rule1.2: Input Pin Strobe Count lesser than Input Pin Force Count
                "1.3": conditionalRuleChecker.Rule1_3, #Rule1.3: Input Pin Label Count lesser than Input Pin Strobe Count
                "1.4": conditionalRuleChecker.Rule1_4, #Rule1.4: Control bit not set to safe for input test
                "2.1": conditionalRuleChecker.Rule2_1, #Rule2.1: Output Pin Vector Strobe Count lesser than Output Pin Count
                "2.2": conditionalRuleChecker.Rule2_2, #Rule2.2: Control bit set to safe for output test
                "2.3": conditionalRuleChecker.Rule2_3, #Rule2.3: Vector Strobe RPT count less than 10
                "2.4": conditionalRuleChecker.Rule2_4, #Rule2.4: Pin Vector Strobing without H->L/ L->H transition
                "3.1": conditionalRuleChecker.Rule3_1, #Rule3.1: Toggle Pin Vector Strobe Count leser than Toggle Pin Count
                "6.1": conditionalRuleChecker.Rule6_1, #Rule6.1: No strobe found for AC RX pin
                "6.2": conditionalRuleChecker.Rule6_2, #Rule6.2: AC Input Pin Strobe Count lesser than AC Input Pin Count
                "6.3": conditionalRuleChecker.Rule6_3  #Rule6.3: AC Output Pin Vector Strobe Count lesser than AC Output Pin Count
            }

    rulesFilepath = "{}\\COLLATERAL\\{}\\rulesfile.csv".format(workdir,prod)
    
    rulesFilepath = rulesFilepath if os.path.exists(rulesFilepath) else "{}\\COLLATERAL\\COMMON\\rulesfile.csv".format(workdir)

    rulesFile_df = pd.read_csv(rulesFilepath)
    rulesFile_df = rulesFile_df.fillna('')
    testfile_list = rulesFile_df['TEST_FILE'].tolist()
        
    rulesSet_list = rulesFile_df['RULES_SET'].tolist()

    print("Running mandatory BSCAN Rules:")
    mandatoryrulesFieldList = mandatoryBscanRule()

    for testfile in testfile_list:
        testfileregex = testfile.replace('*','.+')
        if re.search(testfileregex,testName):
            if rulesSet_list[testfile_list.index(testfile)]:
                print("Running conditional BSCAN Rules:")
                rulesSet = rulesSet_list[testfile_list.index(testfile)].split(',') 
            else:
                conditionalrulesFieldList.append(rC.RulesField(spffile = testName, category = "WARNING", desc = "SPF/ITPP skipped Conditional Rules Checker." ))
                break
            for rule in rulesSet:

                rule_execute = rules_Dict.get(rule, conditionalRuleChecker.RuleUndefined)
                rulefield = rule_execute() if rule in rules_Dict.keys() else rule_execute(rule)

                if len(rulefield) < 1:
                    rule_status = 'PASS'
                    conditionalrulesFieldList.append(rC.RulesField(spffile = testName, rule = "Rule{}".format(rule), category = "PASS"))
                else:
                   rule_status = 'FAIL'

                print("Rule {:<10} ---------------------------- {}".format(rule, rule_status if rule in rules_Dict.keys() else 'UNDEFINED'))

                if rulefield:
                    conditionalrulesFieldList = conditionalrulesFieldList + rulefield

    return conditionalrulesFieldList + mandatoryrulesFieldList

def getTestSummary():

    conditionalRuleChecker = rC.conditionalBscanRule(testName, bsdlObjList, bsdlMappedObjList)

    testSummaryObj = rC.TestSummaryField()

    testSummaryObj.spffile = testName

    testSummaryObj.bidir_pin = len(conditionalRuleChecker.bidirpinlist)
    testSummaryObj.input_pin = len(conditionalRuleChecker.inputpinlist)
    testSummaryObj.output_pin = len(conditionalRuleChecker.outputpinlist)
    testSummaryObj.observe_pin = len(conditionalRuleChecker.observepinlist)

    testSummaryObj.pin_label = len(conditionalRuleChecker.pinlabellist)
    testSummaryObj.tdo_strobe = len(conditionalRuleChecker.input_strobe_list + conditionalRuleChecker.bidir_strobe_list + conditionalRuleChecker.acrxstrobelist)
    testSummaryObj.vector_force0 = len(conditionalRuleChecker.vectorforcelowlist)
    testSummaryObj.vector_force1 = len(conditionalRuleChecker.vectorforcehighlist)
    testSummaryObj.vector_strobeH = len(conditionalRuleChecker.vectorstrobehighlist)
    testSummaryObj.vector_strobeL = len(conditionalRuleChecker.vectorstrobelowlist)

    category_list = list(set([bscanrulesField.category for bscanrulesField in bscanrulesFieldList if bscanrulesField.spffile == testSummaryObj.spffile]))
    rules_list = list(set([bscanrulesField.rule for bscanrulesField in bscanrulesFieldList if bscanrulesField.spffile == testSummaryObj.spffile]))

    testSummaryObj.rules = ', '.join(rules_list)
    testSummaryObj.status = 'ERROR' if 'ERROR' in category_list else 'PASS'

    return testSummaryObj

def obj2DataFrame(objList):
    newDict = []

    for obj in objList:
        newDict.append(obj.__dict__)

    return pd.DataFrame.from_dict(newDict)

def generateBsdlExcel(DF):

    fileName = 'BSDL.xlsx'
    filePath = "{}\\COLLATERAL\\{}".format(workdir,prod)
    print("Generating BSDL Excel Spreadsheet. Please wait ...... ")
      
    with pd.ExcelWriter(filePath + "\\" + fileName, engine='xlsxwriter') as writer:
        DF.to_excel(writer, sheet_name = 'BSDL', index=False)

        worksheet = writer.sheets['BSDL']
        worksheet.freeze_panes(1, 1)

    print("{} generated to path {} \n".format(fileName,filePath))

def generateSPFExcel(DF):
    groupdatalist = ['bsdlmapped','vector']
    print("Generating decoded file. Please wait......")
    outputFilePath = "{}\\DECODED\\{}".format(workdir, prod)
    outputFile = os.path.splitext(testName)[0]
    outputFile_full = outputFilePath + "\\" + outputFile + "_spf_decoded.xlsx"

    if not os.path.exists(outputFilePath):
        os.makedirs(outputFilePath)

    writer = pd.ExcelWriter(outputFile_full, engine='xlsxwriter')

    DF.to_excel(writer, sheet_name = 'DecodedSPF')

    worksheet = writer.sheets['DecodedSPF']

    worksheet.freeze_panes(1, 1)

    groupRow_list = []
    line_num_to_grp_threshold = 10
    consecutive_configType_num = 0

    for groupdata in groupdatalist:
        for DF_index, configType in enumerate(DF['configurationType']):
            
            if groupdata in configType:
                consecutive_configType_num += 1
            else:
                consecutive_configType_num = 0

            if consecutive_configType_num == line_num_to_grp_threshold:
                for i in range(line_num_to_grp_threshold):
                    groupRow_list.append(DF_index - line_num_to_grp_threshold + i + 2)
            elif consecutive_configType_num > line_num_to_grp_threshold:
                groupRow_list.append(DF_index + 1)

    for groupRow in groupRow_list:
        worksheet.set_row(groupRow, None, None, {'level': 1, "hidden": True})

    writer.close()
    print("Decoded SPF generated: {}\n\n".format(outputFile_full))

def generateITPPExcel(DF):
    groupdatalist = ['bsdlmapped','vector']
    print("Generating decoded file. Please wait......")
    outputFilePath = "{}\\DECODED\\{}".format(workdir, prod)
    outputFile = os.path.splitext(testName)[0]
    outputFile_full = outputFilePath + "\\" + outputFile + "_itpp_decoded.xlsx"

    if not os.path.exists(outputFilePath):
        os.makedirs(outputFilePath)
    
    writer = pd.ExcelWriter(outputFile_full, engine='xlsxwriter')

    DF.to_excel(writer, sheet_name = 'DecodedITPP')

    worksheet = writer.sheets['DecodedITPP']

    worksheet.freeze_panes(1, 1)

    groupRow_list = []
    line_num_to_grp_threshold = 10
    consecutive_configType_num = 0

    for groupdata in groupdatalist:
        for DF_index, configType in enumerate(DF['configurationType']):
            
            if groupdata in configType:
                consecutive_configType_num += 1
            else:
                consecutive_configType_num = 0

            if consecutive_configType_num == line_num_to_grp_threshold:
                for i in range(line_num_to_grp_threshold):
                    groupRow_list.append(DF_index - line_num_to_grp_threshold + i + 2)
            elif consecutive_configType_num > line_num_to_grp_threshold:
                groupRow_list.append(DF_index + 1)

    for groupRow in groupRow_list:
        worksheet.set_row(groupRow, None, None, {'level': 1, "hidden": True})

    writer.close()
    print("Decoded ITPP generated: {}\n\n".format(outputFile_full))

def generateReport(SummaryDF, RulesDF):
    
    reportName = 'SummaryReport.xlsx'
    reportpath = "{}\\REPORT\\{}".format(workdir,prod)
    print("Generating Summary Report. Please wait ...... ")
    
    if not os.path.isdir(reportpath):
        os.makedirs(reportpath)
    
    def format_cell(column):    
        for category in column:
            if category == 'PASS':
                highlight = 'background-color: #00B050;'
            elif category == 'ERROR':
                highlight = 'background-color: #FF0000;'
            else:
                highlight = ''
        
        return [highlight]

    RulesDF_formatted = RulesDF.style.apply(format_cell, subset=['category'], axis=1)
    SummaryDF_formatted = SummaryDF.style.apply(format_cell, subset=['status'], axis=1)

    with pd.ExcelWriter(reportpath + "\\" + reportName, engine='xlsxwriter') as writer:
        SummaryDF_formatted.to_excel(writer, sheet_name = 'Summary')
        RulesDF_formatted.to_excel(writer, sheet_name = 'Violation')

        worksheet = writer.sheets['Summary']
        worksheet.freeze_panes(1, 1)

        worksheet = writer.sheets['Violation']
        worksheet.freeze_panes(1, 1)

    print("{} generated to path {} ".format(reportName,reportpath))

if __name__ == "__main__":

    setupBasicFolder()

    prod = getuserinput()

    print("Current Work Directory: {}\n".format(workdir))

    checkCollateralPath()

    spfPathList = getSpfPath()

    itppPathList = getITPPPath()

    if len(spfPathList + itppPathList) == 0:
        quit_program()

    opcodeDict = getOpcode()

    bsdlFile = getBsdl()

    bsdlObjList = bsdl2obj(bsdlFile)

    bsdl_DF = obj2DataFrame(bsdlObjList)

    generateBsdlExcel(bsdl_DF)

    bsdlrulesFieldList = checkBSDLRule(bsdlObjList)

    bscanrulesFieldList = []

    testSummaryList = []

    if len(spfPathList) >= 1:
        for spfPath in spfPathList:

            spfFile = readFile(spfPath)

            testName = os.path.basename(spfPath)

            print("Decoding SPF {} ({}/{})\n".format(testName, spfPathList.index(spfPath) + 1,len(spfPathList)))

            spfLineObjList = processSpf(spfFile)

            mapPinName(spfLineObjList)

            bsdlMappedObjList = mapBSDLInfo(spfLineObjList,bsdlObjList)
        
            bsdlMappedDF = obj2DataFrame(bsdlMappedObjList)

            generateSPFExcel(bsdlMappedDF)

            bscanrulesFieldList += bscanRuleChecker()

            testSummaryList.append(getTestSummary())

    if len(itppPathList) >= 1:   
        for itppPath in itppPathList:

            itppFile = readFile(itppPath)

            testName = os.path.basename(itppPath)

            print("Decoding ITPP {} ({}/{})\n".format(testName, itppPathList.index(itppPath) + 1,len(itppPathList)))

            itppLineObjList = processItpp(itppFile)

            mapPinName(itppLineObjList)

            bsdlMappedObjList = mapBSDLInfo(itppLineObjList,bsdlObjList)
        
            bsdlMappedDF = obj2DataFrame(bsdlMappedObjList)

            generateITPPExcel(bsdlMappedDF)

            bscanrulesFieldList += bscanRuleChecker()

            testSummaryList.append(getTestSummary())

    RulesDF = obj2DataFrame(bsdlrulesFieldList + bscanrulesFieldList)

    TestSummaryDF = obj2DataFrame(testSummaryList)
    
    generateReport(TestSummaryDF, RulesDF)

    quit_program()