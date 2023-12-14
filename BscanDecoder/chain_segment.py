bit = "1a01b01c0"

bit_reverse = "".join(reversed(bit))

newbit = ""
start = 5
end = 3

for index,i in enumerate(bit_reverse):
    if i == '1' or i == '0':
        if index == start:
            newbit += '1'
        else:
            newbit += '0'
    else:
        try:
            int(i)
        except:
            if index < 5 and index > 3:
                newbit += i

print("".join(reversed(newbit)))
        




