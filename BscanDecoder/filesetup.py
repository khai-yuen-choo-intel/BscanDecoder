import os
import shutil

drive_path = "\\\\gar.corp.intel.com\\ec\\proj\\mdl\\pg\\intel\\engineering\\dev\\team_pgm_analog\\khaiyuen\\Tools\\Python\\BscanDecoder" 
workdir = os.getcwd()

def getProductCode():

    while(True):
        userInput = input('Enter Product Code: ')

        confirmUserInput = input('Use {} as Product Code? (Y/N): '.format(userInput))

        prodcode_exist = False
        if confirmUserInput.lower() == 'y':
            basicPath = ['COLLATERAL', 'SPF', 'ITPP']
            for path in basicPath:
                if os.path.exists("{}\\{}\\{}".format(workdir,path,userInput)):
                    prodcode_exist = True
        
        if prodcode_exist == False:
            return userInput
        else:
            print("Product Code {} already created. Please use another Product Code!!!\n".format(userInput))

def setupBasicFolder(prod):

    basicPath = ['COLLATERAL', 'SPF', 'ITPP']

    print("\nCheck/Create Folder Structure:")

    for path in basicPath:
        prodPath = "{}\\{}".format(workdir,path)
        os.makedirs(os.path.join(prodPath,prod))
        print("{}\{} ---------------------------- CREATED".format(prodPath,prod))

    print("\n")

def copyBasicCollateral():
    
    collateral_path = "{}\\{}".format(drive_path, 'COLLATERAL\\COMMON')
    dest_path = "{}\\{}".format(workdir, 'COLLATERAL\\COMMON')
    if os.path.exists(collateral_path) and not os.path.exists(dest_path):
        shutil.copytree(collateral_path,dest_path)
        print('Folder ({}) copied to ({}) \n'.format(collateral_path, dest_path))

def getProductBSDL(prod):

    bsdl_path = "{}\\COLLATERAL\\{}".format(workdir,prod)

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
            destination_folder = "{}\\SPF\\{}".format(workdir,prod)
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
            destination_folder = "{}\\ITPP\\{}".format(workdir,prod)
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

        copyBasicCollateral()

        getProductBSDL(prodCode)   
        
        getProductSPF(prodCode)

        getProductITPP(prodCode)

    def removeProduct():

        prodlist = []

        spfFolder = "{}\\SPF".format(workdir)
        itppFolder = "{}\\ITPP".format(workdir)

        basicPath = ['COLLATERAL', 'SPF', 'ITPP']

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