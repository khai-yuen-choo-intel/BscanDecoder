import os
import shutil

#drive_path = "\\\\gar.corp.intel.com\\ec\\proj\\mdl\\pg\\intel\\engineering\\dev\\team_pgm_analog\\khaiyuen\\Tools\\Python\\BscanDecoder" 
workdir = os.getcwd()

basicPath = ['1_COLLATERAL', '2_SPF', '3_ITPP']

def getProductCode():

    while(True):
        userInput = input('Enter Product Code: ')

        confirmUserInput = input('Use {} as Product Code? (Y/N): '.format(userInput))

        prodcode_exist = False
        if confirmUserInput.lower() == 'y':
            for path in basicPath:
                if os.path.exists("{}\\{}\\{}".format(workdir,path,userInput)):
                    prodcode_exist = True
        
        if prodcode_exist == False:
            return userInput
        else:
            print("Product Code {} already created. Please use another Product Code!!!\n".format(userInput))

def setupBasicFolder(prod):

    print("\nCheck/Create Folder Structure:")

    for path in basicPath:
        prodPath = "{}\\{}".format(workdir,path)
        os.makedirs(os.path.join(prodPath,prod))
        print("{}\{} ---------------------------- CREATED".format(prodPath,prod))

    print("\n")

'''
def copyBasicCollateral():
    
    collateral_path = os.path.join(drive_path, basicPath[0], "COMMON")
    dest_path = os.path.join(workdir, basicPath[0], "COMMON")
    if os.path.exists(collateral_path) and not os.path.exists(dest_path):
        shutil.copytree(collateral_path,dest_path)
        print('Folder ({}) copied to ({}) \n'.format(collateral_path, dest_path))
'''

def generateRuleFile():
    rulesfile_folder = os.path.join(workdir, basicPath[0], "COMMON")
    if not os.path.exists(rulesfile_folder):
        os.mkdir(rulesfile_folder)
        print("{} ---------------------------- CREATED".format(rulesfile_folder))

    rulesfile_path = os.path.join(rulesfile_folder, "rulesfile.csv")
    if not os.path.exists(rulesfile_path):

        

        testlist_Dict = {
            "*input*":"1.1,1.2,1.3,1.4",
            "*vix*":"1.1,1.2,1.3,1.4",
            "*output*":"2.1,2.2,2.3,2.5",
            "*vox*":"2.1,2.2,2.3",
            "*toggle*":"3.1,2.2,2.4",
            "*train*":"6.1,6.2,6.3",
            "*pulse*":"6.1,6.2,6.3"
            }

        with open(rulesfile_path, "w") as rulesfile:
            rulesfile.writelines('TEST_FILE,RULES_SET\n')
            for key in testlist_Dict:
                rulesfile.writelines('{},"{}"\n'.format(key,testlist_Dict[key]))

        print("{} ---------------------------- CREATED".format(rulesfile_path))

def getProductBSDL(prod):

    bsdl_path = "{}\\{}\\{}".format(workdir,basicPath[0],prod)

    while(True):
        userInput = input('BSDL File Path: ')

        if os.path.isfile(userInput):
            bsdlName = os.path.basename(userInput)
            if bsdlName.endswith('.bsdl'):
                shutil.copy(userInput,os.path.join(bsdl_path,bsdlName))
                break
            else:
                print("Non BSDL file detected!!!\n")
                continue
        else:
            print("BSDL File not found!!!\n")
    print("\n")

def getProductSPF(prod):

    def copySPF(path):
        for file_name in os.listdir(path):
            source = os.path.join(path,file_name)
                
            if os.path.isfile(source) and file_name.endswith('.spf'):
                destination = os.path.join(destination_folder, file_name)
                print('Copying SPF from {}. Please Wait......'.format(source))
                shutil.copy(source, destination)

            if os.path.isdir(source):
                copySPF(source)

    while(True):
        userInput = input('Upload SPF? (Y/N): ')

        if userInput.lower() == 'y':
            destination_folder = "{}\\{}\\{}".format(workdir,basicPath[1],prod)
        else:
            print('Upload SPF skipped.\n')
            break

        userInput = input('SPF Folder Path: ')

        if os.path.isdir(userInput):
            copySPF(userInput)
            break
        else:
            print("Invalid SPF Folder Path!!!\n")

   

def getProductITPP(prod):

    def copyITPP(path):
        for file_name in os.listdir(path):
            source = os.path.join(path,file_name)
                
            if os.path.isfile(source) and file_name.endswith('.itpp'):
                destination = os.path.join(destination_folder, file_name)
                print('Copying ITPP from {}. Please Wait......'.format(source))
                shutil.copy(source, destination)
               
            if os.path.isdir(source):
                copyITPP(source)

    while(True):
        userInput = input('Upload ITPP? (Y/N): ')

        if userInput.lower() == 'y':
            destination_folder = "{}\\{}\\{}".format(workdir,basicPath[2],prod)
        else:
            print('Upload ITPP skipped.\n')
            break

        userInput = input('ITPP Folder Path: ')

        if os.path.isdir(userInput):
            copyITPP(userInput)
            break
        
        else:
            print("Invalid ITPP Folder Path!!!\n")
    

class FileSetup:    
 
    def setupProduct():

        prodCode = getProductCode()

        setupBasicFolder(prodCode)

        #copyBasicCollateral()
        generateRuleFile()

        getProductBSDL(prodCode)   
        
        getProductSPF(prodCode)

        getProductITPP(prodCode)

    def removeProduct():

        prodlist = []

        spfFolder = "{}\\{}".format(workdir, basicPath[1])
        itppFolder = "{}\\{}".format(workdir, basicPath[2])


        while(True):
            
            for item in list(set(os.listdir(spfFolder) + os.listdir(itppFolder))):
                if os.path.isdir("{}\\{}".format(spfFolder, item)) or os.path.isdir("{}\\{}".format(itppFolder, item)):
                    prodlist.append(item)
    
            prodlist.sort()

            for index, option in enumerate(prodlist):
                print ("{}--{}".format(index,option))

            userInput = int(input('Enter your choice: '))

            if prodlist[userInput] in prodlist:
                prod = prodlist[userInput]
                for path in basicPath:
                    delete_path = os.path.join(workdir,path,prod)
                    print("Deleting folder {}".format(delete_path))
                    try:
                        shutil.rmtree(delete_path)
                    except:
                        print("Fail to delete folder {}".format(delete_path))
                break
            else:
                print('Invalid selection !!! Please re-enter from the options.')