import os
import filesetup as fS
import prod_decode as pD
import forcepeek_conversion as fpC
import lkg_file as lkg
import derive_spf as dS
import label_insert as lI

os.system("")

class setup_properties:

    def __init__(self):
        self.workdir = os.getcwd()
        self.basicPath = ['1_COLLATERAL', '2_SPF', '3_ITPP']
        self.prod = ""
        self.major = "4"
        self.minor = "0"
        self.patch = "0"

setupProperties = setup_properties()

def format_violation(text):
    return "Bscan Rules Violation:[{}]".format(text)

def collateral_violation(text):
    return "Collateral Violation:[{}]".format(text)

def print_color(text, index):
    switch = {
        'red': '\033[91m',
        'purple': '\033[95m',
        'blue': '\033[94m',
        'cyan':'\033[96m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'orange': '\033[33m'
        }

    if index < 7:
        color_ansi = list(switch.values())[index]
    else:
        index = index % 7 + 1
        color_ansi = list(switch.values())[index]

    print('{}{}{}'.format(color_ansi,text,'\033[00m'))

def print_version(major,minor,patch):
    logo =\
    '===========================================================\n'+\
    '\n********      ********     ********    *****    *****   ***'+\
    '\n**     ***   ***          ***         *** ***   ******  ***'+\
    '\n**      *** ***          ***         ***   ***  ******  ***'+\
    '\n**     ***   ***        ***         ***     *** *** *** ***'+\
    '\n********      *******   ***         ***     *** *** *** ***'+\
    '\n**     ***         ***  ***         *********** *** *** ***'+\
    '\n**      ***         ***  ***        *********** ***  ******'+\
    '\n**     ***         ***    ****      ***     *** ***   *****'+\
    '\n********     ********       ******* ***     *** ***    ****'+\
    '\n\n  *****   *******   *****   ***   *****   ******* ******'+\
    '\n  **  **  **       **     **   ** **  **  **      **   **'+\
    '\n  **   ** ******  **      **   ** **   ** ******  ******'+\
    '\n  **  **  **       **     **   ** **  **  **      **  **'+\
    '\n  *****   *******   *****   ***   *****   ******* **   **'+\
    '\n==========================================================='+\
    '\n********************* VERSION: {}.{}.{} **********************'.format(major,minor,patch) +\
    '\n==========================================================='
    print(logo)

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


def userInput_main(optionlist, color):
    if color == True:
        for index, option in enumerate(optionlist):
            try:
                print_color("{}--{}".format(index+1,option),index+1)
            except:
                print("{}--{}".format(index+1,option))
    else:
        for index, option in enumerate(optionlist):
            print("{}--{}".format(index+1,option))

    print_color("{}--{}".format("0","Exit"),0)

def userInput_module(optionlist):
    for index, option in enumerate(optionlist):
        print("{}--{}".format(index+1,option))

    print_color("{}--{}".format("0","Back to Main"),0)

def setupBasicFolder(setupObj):

    print("\nCheck/Create Folder Structure:")

    for path in setupObj.basicPath:
        folder = "{}\\{}".format(setupObj.workdir,path)
        if os.path.exists(folder):
            print("BASIC FOLDER {:<20}     ---------------------------- OK".format(path))
            pass
        else:
            os.makedirs(folder)
            print("BASIC FOLDER {:<20}     ---------------------------- CREATED".format(path))

    print("\n")

def getProdList(setupObj):

    prodlist = []

    spfFolder = "{}\\{}".format(setupObj.workdir,setupObj.basicPath[1])
    itppFolder = "{}\\{}".format(setupObj.workdir,setupObj.basicPath[2])

    for item in list(set(os.listdir(spfFolder) + os.listdir(itppFolder))):
        if os.path.isdir("{}\\{}".format(spfFolder, item)) or os.path.isdir("{}\\{}".format(itppFolder, item)):
            prodlist.append(item)
    
    prodlist.sort()

    return prodlist

def selectProd():

    prodlist = getProdList(setupProperties)

    userInput_module(prodlist)

    prod_sel = int(input('Enter your choice: '))

    if prod_sel > 0:
        return prodlist[prod_sel - 1]
    else:
        return 0

if __name__ == "__main__":

    print_version(setupProperties.major,setupProperties.minor,setupProperties.patch)

    setupBasicFolder(setupProperties)

    print("Current Work Directory: {}\n".format(setupProperties.workdir))

    while(1):
        optionlist = ["BscanDecoder", "Product Setup", "Remove Product", "Force/Peek Conversion", "Leakage InputFile", "Derive SS SPF", "Label Insertion"]

        userInput_main(optionlist,1)

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a valid number in the options ...')
            continue

        if option == 0:
            quit_program()
        elif option == 1:
            setupProperties.prod = selectProd()
            result = pD.prod_decode(setupProperties)
        elif option == 2:
            fS.FileSetup.setupProduct()
            result = 1
        elif option == 3:
            fS.FileSetup.removeProduct()
            result = 1
        elif option == 4:
            setupProperties.prod = selectProd()
            result = fpC.forcepeek_conversion(setupProperties)
        elif option == 5:
            setupProperties.prod = selectProd()
            result = lkg.generateLKG(setupProperties)
        elif option == 6:
            setupProperties.prod = selectProd()
            result = dS.generate_SS_Spf(setupProperties)
        elif option == 7:
            setupProperties.prod = selectProd()
            result = lI.label_insertion(setupProperties)
        else:
            print('Wrong input. Please enter a valid number in the options ...')
            result = -1

        print("Program exit with code ({})".format(result))
