import os
import re

datalist = ['abc', 'ap', 'cbs', 'cnn', 'fox', 'ng']
def process():
    for data in datalist:
        for filename in os.listdir('./raw/%s'%data):
            with open('./raw/%s/%s'%(data, filename), 'r', encoding='utf-8') as fin:
                temp = fin.read().lower()
                with open('./cleaned/%s/%s'%(data, filename), 'w', encoding="utf-8") as fout:
                    fout.write(re.sub('[^a-z]+','', temp))   

if __name__ == "__main__":
    process()
    print("OK.")