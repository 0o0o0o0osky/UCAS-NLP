import datetime
import re

def process():
    str = ''
    for month in range(1, 13):
        with open('./raw/2019/2019-%d.txt'%(month), 'r', encoding='utf-8') as fin:
            temp = fin.read()
            str += temp
    for month in range(1, 13):
        with open('./raw/2020/2020-%d.txt'%(month), 'r', encoding='utf-8') as fin:
            temp = fin.read()
            str += temp
    with open('./cleaned/cleaned.txt', 'w', encoding="utf-8") as fout:
        fout.write(re.sub('[^\u4e00-\u9fa5]+','', str))   

if __name__ == "__main__":
    process()
    print("OK.")