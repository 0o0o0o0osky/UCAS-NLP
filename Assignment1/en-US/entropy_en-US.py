import math
import os

char_dict={}
character_num = 0
key_num = 0
entropy = 0
str = ''
datalist = ['abc', 'ap', 'cbs', 'cnn', 'fox', 'ng']
for data in datalist:
    for filename in os.listdir('./cleaned/%s'%data):
        with open('./cleaned/%s/%s'%(data, filename), 'r', encoding='utf-8') as f:
            fin = f.read()
            str += fin
for character in str:
    character_num += 1
    if character not in char_dict:
        char_dict[character] = 1
        key_num += 1
    else:
        char_dict[character] += 1
    if character_num % 1000000 == 0:
        entropy = 0
        for value in char_dict.values():
            p = value / character_num
            entropy += math.log2(p) * p
        entropy = -entropy
        print("Letters: %dM\nEntropy: %.5f"%(character_num // 1000000, entropy))
        sorted_dict = sorted(char_dict.items(), key=lambda x:x[1], reverse=True)
        print("Top 10 letters:")
        for key,value in sorted_dict[0:10]:
            print("\'%s\': %.2f%%"%(key, value * 100 / character_num))
entropy = 0   
for value in char_dict.values():
    p = value / character_num
    entropy += math.log2(p) * p
entropy = -entropy
print("Total letters:%d\nEntropy:%.5f"%(character_num, entropy))
sorted_dict = sorted(char_dict.items(), key=lambda x:x[1], reverse=True)
print("Top 10 letters:")
for key,value in sorted_dict[0:10]:
    print("\'%s\': %.2f%%"%(key, value * 100 / character_num))
