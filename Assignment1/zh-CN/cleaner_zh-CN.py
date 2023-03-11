import datetime
import re

def process():
    for year in range(2019, 2023):
        for month in range(1, 13):
            with open('./raw/%d/%d-%d.txt'%(year, year, month), 'r', encoding='utf-8') as fin:
                temp = fin.read()
            with open('./cleaned/%d/%d-%d.txt'%(year, year, month), 'w', encoding="utf-8") as fout:
                fout.write(re.sub('[^\u4e00-\u9fa5]+','', temp))   

if __name__ == "__main__":
    process()
    print("OK.")
