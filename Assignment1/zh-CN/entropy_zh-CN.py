import math

char_dict={}
character_num = 0
key_num = 0
entropy = 0
str = ''
for year in range(2019, 2023):
    for month in range(1, 13):
        with open('./cleaned/%d/%d-%d.txt'%(year, year, month), 'r', encoding='utf-8') as f:
            fin = f.read()
            str += fin
for character in str:
    character_num += 1
    if character not in char_dict:
        char_dict[character] = 1
        key_num += 1
    else:
        char_dict[character] += 1
    if character_num % 2000000 == 0:
        entropy = 0
        for value in char_dict.values():
            p = value / character_num
            entropy += math.log2(p) * p
        entropy = -entropy
        print("Characters: %dM\nEntropy: %.5f"%(character_num // 1000000, entropy))
        sorted_dict = sorted(char_dict.items(), key=lambda x:x[1], reverse=True)
        print("Top 10 characters:")
        for key,value in sorted_dict[0:10]:
            print("\'%s\': %.2f%%"%(key, value * 100 / character_num))
entropy = 0   
for value in char_dict.values():
    p = value / character_num
    entropy += math.log2(p) * p
entropy = -entropy
print("Total characters:%d\nEntropy:%.5f"%(character_num, entropy))
sorted_dict = sorted(char_dict.items(), key=lambda x:x[1], reverse=True)
print("Top 10 characters:")
for key,value in sorted_dict[0:10]:
    print("\'%s\': %.2f%%"%(key, value * 100 / character_num))
