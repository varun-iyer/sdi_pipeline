with open('/home/williamwang/subtracted_Alard_Lupton5by5/sources_Alard_Lupton5by5.txt','r') as input1:
    f1 = [line.rstrip('\n') for line in input1]
with open('/home/williamwang/Alard_Lupton_modified1/sources_Alard_Lupton_modified1.txt','r') as input2:
    f2 = [line.rstrip('\n') for line in input2]

def compare(f1,f2):
    counter = 0
    not_counter = 0
    for line1 in f1:
        if line1 in f2:
            counter = counter + 1
            print(line1)
        else:
            not_counter += 1
    print('Lines not equal', not_counter)
    return counter
print(compare(f1,f2))
input1.close()
input2.close()
