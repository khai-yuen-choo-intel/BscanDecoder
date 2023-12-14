import math

def binToHexa2(n):
   
    # convert binary to int
    num = int(n, 2)
     
    # convert int to hexadecimal
    hex_num = hex(num)
    return(hex_num)

def hex2Bin(ini_string):
    n = int(ini_string, 16)
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1   
    return bStr

# Driver code
if __name__ == '__main__':
    while(1):
        print ('0 -- Bin2Hex\n1 -- Hex2Bin\n')
        mode = int(input('Select Mode: '))
        if mode == 0:
            bnum = input('Enter Binary Value: ')
            hnum = binToHexa2(bnum)
            print("Hex equivalnet : {}\n".format(hnum))
        elif mode == 1:
            hnum = input('Enter Hex Value: ')
            bnum = hex2Bin(hnum)
            print("Binary equivalnet : {}\n".format(bnum))