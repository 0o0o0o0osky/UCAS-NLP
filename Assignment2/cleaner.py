import re
from zhon.hanzi import punctuation

with open('ChineseCorpus199801.txt', 'r', encoding='GBK') as fin:
    text = fin.read()
    text = re.sub(r'(\d{8}-\d{2}-\d{3}-\d{3})?/[a-zA-Z]+', "", text)
    text = re.sub("[{}]+".format(punctuation), "", text)
    text = re.sub(r"[\[(\]nt)]", "", text)
    text = re.sub("[a-z]", "", text)
    # words_list = text.split()
    # words_set = list(collections.OrderedDict.fromkeys(words_list).keys())
    # new_text = ""
    # for word in words_list:
    #     if word in words_set:
    #         new_text += word
    #     else:
    #         new_text += "UNK"
    #     new_text += " "
    with open('cleaned.txt', 'w', encoding='GBK') as fout:
        fout.write(text)
