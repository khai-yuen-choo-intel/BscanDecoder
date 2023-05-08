import bsdl_lib as bL
import pandas as pd

def removeSymbol(text):
    unwantedSym_list = [";","&","(",")","\""," ","\n"]
    for unwantedSym in unwantedSym_list:
        if unwantedSym in text:
            text = text.replace(unwantedSym,"")
    return text

class BSDLInterpreter:
    
    def __init__(self, bsdlfilepath = ""):
        self.bsdlfilepath = bsdlfilepath

    def getACIOList(self):

        acio_list = []

        with open(self.bsdlfilepath, "r") as bsdlfile:
            bsdlline = bsdlfile.readlines()
            start_line =  None

            for line_num, line in enumerate (bsdlline):
                if 'AIO_Pin_Behavior' in line:
                    start_line = line_num + 1
                    continue

                if start_line != None:
                    if '\"' not in line:
                        end_line = line_num
                        break

            acio_segment = bsdlline[start_line:end_line]

            for line in acio_segment:
                open_quote_index = line.find('\"')
                close_quote_index = line.find('\"', open_quote_index + 1)
                acio_list.append(removeSymbol(line[open_quote_index + 1:close_quote_index].split(" ")[0]))

        return acio_list

    def bsdl2ObjList(self):

        bsdlObjList = []
        ACIO_List = self.getACIOList()
        with open(self.bsdlfilepath, "r") as bsdlfile:
            bsdlline = bsdlfile.readlines()
            start_line =  None

            for line_num, line in enumerate (bsdlline):
                if 'BOUNDARY_REGISTER' in line:
                    start_line = line_num + 1

                if start_line != None:
                    if ";" in line:
                        end_line = line_num + 1
                        break

            boundary_reg = bsdlline[start_line:end_line]

            for line in boundary_reg:

                bsdlObj = bL.Bsdl()

                if line.isspace():
                    continue
                if '\"' not in line:
                    continue

                bsdlObj.num = removeSymbol(line[:line.find('(')])

                bsdlinfo = line[line.find('(') + 1:].split(',')

                bsdlObj.port = bsdlinfo[1].strip()
                for ACIO in ACIO_List:
                    if bsdlObj.port in ACIO:
                        bsdlObj.cell = 'AC'
                        break
                    else:
                        bsdlObj.cell = bsdlinfo[0].strip()
                bsdlObj.function = bsdlinfo[2].strip()
                bsdlObj.safe = removeSymbol(bsdlinfo[3])

                try:
                    bsdlObj.ccell = removeSymbol(bsdlinfo[4])
                except:
                    bsdlObj.ccell = ""

                try:
                    bsdlObj.disval = bsdlinfo[5].strip()
                except:
                    bsdlObj.disval = ""

                try:
                    bsdlObj.rslt = removeSymbol(bsdlinfo[6])
                except:
                    bsdlObj.rslt = ""
                
                bsdlObjList.append(bsdlObj)

        return bsdlObjList

    def csv2ObjList(self):

        bsdlObjList = []

        bsdl_df = pd.read_csv(self.bsdlfilepath)
        bsdl_df = bsdl_df.fillna("")
        bsdl_dict = bsdl_df.to_dict()

        bsdlheaderlist = ['num','port','cell','function','safe','disval']
        bsdlkeylist = bsdl_df.columns

        if not (set(bsdlheaderlist).issubset(set(bsdlkeylist))):
            print('Mandatory column ({}) not found in bsdl spreadsheet.'.format(str(bsdlheaderlist)))
            quit()

        for i in range(len(bsdl_dict['num'])):
            bsdlObj = bL.Bsdl()
            bsdlObj.num = str(bsdl_dict['num'][i]).strip()
            bsdlObj.port = str(bsdl_dict['port'][i]).strip()
            bsdlObj.cell = str(bsdl_dict['cell'][i]).strip()
            bsdlObj.function = str(bsdl_dict['function'][i]).strip()
            bsdlObj.safe = str(bsdl_dict['safe'][i]).strip()
            bsdlObj.ccell = str(bsdl_dict['ccell'][i]).strip()
            bsdlObj.disval = str(bsdl_dict['disval'][i]).strip()
            bsdlObj.rslt = str(bsdl_dict['rslt'][i]).strip()

            bsdlObjList.append(bsdlObj)

        return bsdlObjList