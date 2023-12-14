import os
import json
import bsdlinterpreter as bI
import configjson as cJ
import BscanDecoder as bD
from itertools import groupby

category = ['tx','rx','txp','txn','rxp','rxn','_n','_p','_n_','_p_','wt','wr']
default_input = "[user input]"

class pinName:
    def __init__(self, pinName):
        self.pinName = pinName

        try:
            self.ip = pinName.split("_")[0]
        except:
            self.ip = pinName

        try:
            self.family = pinName.split("_")[1]
        except:
            self.family = pinName

        self.type = None
        for i in category:
            if i in pinName.lower():
                self.type = i

    def __repr__(self):
        return self.pinName

def bsdl2obj(filepath):

    bsdlObjList = []

    if filepath.endswith('.csv'):

        bsdlObjList = bI.BSDLInterpreter(filepath).csv2ObjList()

    else:

        bsdlObjList = bI.BSDLInterpreter(filepath).bsdl2ObjList()

    return bsdlObjList

def getAllPin(bsdlObjList):
    
    allpinlist = []
    pinlist = []
    
    for bsdlObj in bsdlObjList:
        if allpinlist:
            pinlist = [obj.pinName for obj in allpinlist]
        if bsdlObj.pinmap and bsdlObj.pinmap not in pinlist:
            allpinlist.append(pinName(bsdlObj.pinmap))
        if bsdlObj.differential and bsdlObj.differential.pinmap not in pinlist:
            allpinlist.append(pinName(bsdlObj.differential.pinmap))

    return allpinlist

def sortPin(allpinlist):
    pinlist_type = []
    pinlist_family = []
    sorted_ip= sorted(allpinlist, key = lambda allpin: allpin.ip)
    grouped_ip = [list(result_ip) for key, result_ip in groupby(sorted_ip, key=lambda allpin: allpin.ip)]

    for grp in grouped_ip:
        try:
            sorted_type = sorted(grp, key = lambda allpin: allpin.type)
            grouped_type = [list(result_type) for key, result_type in groupby(sorted_type, key=lambda allpin: allpin.type)]
        except:
            grouped_type = [grp]
        
        for grouped in grouped_type:
            pinlist_type.append(grouped)

    for grp in pinlist_type:
        if len(grp) > 50:
            sorted_family = sorted(grp, key = lambda allpin: allpin.family)
            grouped_family = [list(result_family) for key, result_family in groupby(sorted_family, key=lambda allpin: allpin.family)]
        else:
            grouped_family = [grp]

        for grouped in grouped_family:
            pinlist_family.append(grouped)

    return pinlist_family

def generateXML(pinGrpList):

    xmlLine = ""
    xmlLine += '<?xml version="1.0" encoding="utf-8"?>\n'
    xmlLine += '<DCLeakage_config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="GEN_DCLeakage_tt.xsd">\n'
    xmlLine += '<config_set name = "[user input]" config_pingroup="[user input]">\n'
    xmlLine += '\n'

    for pingrp in pinGrpList:
        xmlLine += '\t<measurement group="[user input]" measurement_pingroup="[user input]">\n'
        xmlLine += '\t\t<setting>\n'

        for pin in pingrp:
            xmlLine += '\t\t<pin>' + pin.pinName + '</pin>\n'

        xmlLine += '\t\t\t<limit_high>[user input]</limit_high>\n'
        xmlLine += '\t\t\t<limit_low>[user input]</limit_low>\n'
        xmlLine += '\t\t\t<force_high_value type="double">[user input]</force_high_value>\n'
        xmlLine += '\t\t\t<force_low_value type="double">0.0</force_low_value>\n'
        xmlLine += '\t\t\t<measure_range>[user input]</measure_range>\n'
        xmlLine += '\t\t</setting>\n'
        xmlLine += '\t</measurement>\n\n'

    xmlLine += '</config_set>\n'
    xmlLine += '</DCLeakage_config>'

    return xmlLine

def generateJSON(pinGrpList):
    measurement = []
    
    pinSetting = cJ.PinSetting(default_input,default_input,default_input,default_input,default_input,default_input,default_input).__dict__
    
    for pingrp in pinGrpList:
        setting = []
        pinlist = [pin.pinName for pin in pingrp]
        setting.append(cJ.Settings(pinlist,pinSetting).__dict__)
        measurement.append(cJ.Measurements(default_input,default_input,setting).__dict__)

    configset = cJ.ConfigurationSet(default_input,default_input,measurement).__dict__

    x = {
            "ConfigurationSets": [configset]
        }

    return x

def generateFile(setupProperties):

    path = os.path.join(setupProperties.workdir,setupProperties.basicPath[0],setupProperties.prod)

    for file in os.listdir(path):
        if file.endswith(".bsdl"):
            bsdlpath = "{}\\{}".format(path,file)

    bsdlObjList = bsdl2obj(bsdlpath)
    allpinlist = getAllPin(bsdlObjList)
    sortPinList = sortPin(allpinlist)
    bD.userInput_module(["JSON","XML"])
    while(1):
        try:
            file_format = int(input("Enter your choice: "))
            if file_format == 0:
                return 0
            elif file_format ==1:
                jsonFileName = "{}\\{}.json".format(path,"bsdl")
                x = generateJSON(sortPinList)
                with open(jsonFileName, "w") as outfile:
                    json.dump(x, outfile, indent=4)
                print("JSON InputFile Generation - PASS.\nNew file Path: {}\n".format(jsonFileName))
                return 0
            elif file_format ==2:
                xmlFileName = "{}\\{}.dcleak.xml".format(path,"bsdl")
                xmlLine = generateXML(sortPinList)
                xmlFile = open(xmlFileName, "w")
                xmlFile.write(xmlLine)
                xmlFile.close()
                print("XML InputFile Generation - PASS.\nNew file Path: {}\n".format(xmlFileName))
                return 0
            else:
                print("Invalid selection. Please enter number 1/2.")
        except:
            print("Invalid selection. Please enter number 1/2.")

def generateLKG(setupProperties):
    if setupProperties.prod == 0:
        return 0
    else:
        try:
            generateFile(setupProperties)
            return 1
        except:
            return -1
