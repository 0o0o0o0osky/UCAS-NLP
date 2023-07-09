import csv
import os
import jieba

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname

# This code is used to merge stop words from different files into one file

# stopwords = []

# for i in findAllFile('.\\stopwords\\'):
#     with open(i, 'r', encoding='utf8', errors='ignore') as f:
#         line = f.readlines()
#         for word in line:
#             word = word.replace('\n', '')
#             stopwords.append(word)

# stopwords = set(stopwords)

# f = open('.\\stopwords\\stopwords.txt', 'w', encoding='utf8')
# f.write('\n'.join(stopwords))
# f.close()

with open("data.csv","w", encoding='utf8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['sentiment', 'review'])
    for i in findAllFile('.\\raw\\Book_del_4000\\neg\\'):
        with open(i, 'r', encoding='gbk', errors='ignore') as f:
            line = f.readlines()[2]
            line = line.replace('\n', '') 
            writer.writerow(['0', line])
    for i in findAllFile('.\\raw\\Book_del_4000\\pos\\'):
        with open(i, 'r', encoding='gbk', errors='ignore') as f:
            line = f.readlines()[2]
            line = line.replace('\n', '') 
            writer.writerow(['1', line])            
    for i in findAllFile('.\\raw\\htl_del_4000\\neg\\'):
        with open(i, 'r', encoding='gbk', errors='ignore') as f:
            lines = f.readlines()             
            line = " ".join(lines)
            line = line.replace('\n', '') 
            writer.writerow(['0', line])            
    for i in findAllFile('.\\raw\\htl_del_4000\\pos\\'):
        with open(i, 'r', encoding='gbk', errors='ignore') as f:
            lines = f.readlines()             
            line = " ".join(lines)
            line = line.replace('\n', '')
            writer.writerow(['1', line])                
    for i in findAllFile('.\\raw\\NB_del_4000\\neg\\'):
        with open(i, 'r', encoding='gbk', errors='ignore') as f:
            lines = f.readlines()             
            line = " ".join(lines)
            line = line.replace('\n', '')
            writer.writerow(['0', line])     
    for i in findAllFile('.\\raw\\NB_del_4000\\pos\\'):
        with open(i, 'r', encoding='gbk', errors='ignore') as f:
            lines = f.readlines()             
            line = " ".join(lines)
            line = line.replace('\n', '')
            writer.writerow(['1', line])     
