# Implementing the calculation of BLEU score without using NLTK
# source language: Chinese
# target language: English
# data set: WMT18
# Chinese data: newstest2018-enzh-src.zh.sgm
# English data: newstest2018-enzh-ref.en.sgm

import re
import math

# only used for checking the result
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def preprocess(text):
    for line in text:
        newline = line.strip('\n')
        newline = newline.lower()
        newline = re.sub(r'^\d+\.\s', ' ', newline)
        newline = re.sub(r'\b[.,?!;:"\']+\B', '', newline)
        newline = newline.strip()
        newline = newline.split(' ')
        text[text.index(line)] = newline

# read the reference data
reference = open('testdata/reference30.txt', 'r', encoding='utf-8').readlines()
preprocess(reference)

# data of translators
baidu = open('result/Baidu.txt', 'r', encoding='utf-8').readlines()
preprocess(baidu)
bing = open('result/Bing.txt', 'r', encoding='utf-8').readlines()
preprocess(bing)
google = open('result/Google.txt', 'r', encoding='utf-8').readlines()
preprocess(google)
gpt = open('result/ChatGPT.txt', 'r', encoding='utf-8').readlines()
preprocess(gpt)

# generate the analysis data
baidu_result = open('result/Baidu_result.txt', 'w', encoding='utf-8')
bing_result = open('result/Bing_result.txt', 'w', encoding='utf-8')
google_result = open('result/Google_result.txt', 'w', encoding='utf-8')
gpt_result = open('result/ChatGPT_result.txt', 'w', encoding='utf-8')
def generate_result(target, result_dict):
    if target == baidu_result:
        translator_name = 'Baidu'
    elif target == bing_result:
        translator_name = 'Bing'
    elif target == google_result:
        translator_name = 'Google'
    elif target == gpt_result:
        translator_name = 'ChatGPT'
    else:
        print('ERROR')
        exit()
    target.write('test sentence: ' + str(i+1) + '\n')
    target.write('BLEU-BP score: ' + str(result_dict['BP']) + ' (' + translator_name + ': ' + str(result_dict['trans_words']) + ' / ' 
                 + 'total: ' + str(result_dict['ref_words']) + ')' + '\n')
    target.write('BLEU-1 score: ' + str(result_dict['uni_score']) + ' (match'  + ': ' + str(result_dict['uni_match']) 
          + ' /' + ' total: ' + str(result_dict['uni_total']) + ')' + '\n')
    target.write('BLEU-2 score: ' + str(result_dict['bi_score']) + ' (match'  + ': ' + str(result_dict['bi_match'])
          + ' /' + ' total: ' + str(result_dict['bi_total']) + ')' + '\n')
    target.write('BLEU-3 score: ' + str(result_dict['tri_score']) + ' (match'  + ': ' + str(result_dict['tri_match'])
          + ' /' + ' total: ' + str(result_dict['tri_total']) + ')' + '\n')
    target.write('BLEU-4 score: ' + str(result_dict['quad_score']) + ' (match'  + ': ' + str(result_dict['quad_match']) 
          + ' /' + ' total: ' + str(result_dict['quad_total']) + ')' + '\n')
    target.write('BLEU score: ' + str(result_dict['BLEU']) + '\n')

# generate the n-gram
def ngram(text, n):
    ngram = []
    for i in range(0, len(text)-n+1):
        ngram.append(text[i:i+n])
    return ngram

# get the name of translator
def get_name(translator):
    if translator == baidu:
        return 'Baidu'
    elif translator == bing:
        return 'Bing'
    elif translator == google:
        return 'Google'
    elif translator == gpt:
        return 'ChatGPT'

# calculate the BLEU score
def BLEU(translator, ref, loc):
    score = 0
    score_BP = 1
    translator_name = get_name(translator)
    result_dict = {'uni_match': 0, 'uni_total': 0, 'uni_score': 0,
                   'bi_match': 0, 'bi_total': 0, 'bi_score': 0,
                   'tri_match': 0, 'tri_total': 0, 'tri_score': 0,
                   'quad_match': 0, 'quad_total': 0, 'quad_score': 0,
                   'BP': 0, 'trans_words': 0, 'ref_words': 0,
                   'BLEU': 0
                   }
    # calculate the brevity penalty
    if len(translator[loc]) < len(reference[loc]):
        score_BP = math.exp(1 - len(ref[loc])/len(translator[loc]))
    print('BLEU-BP score of ' + translator_name + ': ' + str(score_BP) + ' (' + translator_name + ': ' + str(len(translator[loc])) 
          + ' /' + ' reference: ' + str(len(reference[loc])) + ')')
    
    for j in range(1, 5):
        count = 0
        ngram_score = 0
        ngram_ref = ngram(reference[loc], j)
        ngram_trans = ngram(translator[loc], j)
        count_dict = {}
        # count the number of n-gram
        for gram in ngram_ref:
            if str(gram) not in count_dict:
                count_dict[str(gram)] = 1
            else:
                count_dict[str(gram)] += 1
        for k in range(0, len(ngram_trans)):
            if ngram_trans[k] in ngram_ref:
                if count_dict[(str(ngram_trans[k]))] > 0:
                    count += 1
                    count_dict[(str(ngram_trans[k]))] -= 1
        
        # smoothing
        if count != 0:
            ngram_score = count / len(ngram_trans)
        else:
            ngram_score = 0.1 / len(ngram_trans)
        
        print('BLEU-' + str(j) + ' score of ' + translator_name + ': ' + str(ngram_score) + 
              ' (match: ' + str(count) + ' / total: ' + str(len(ngram_trans)) + ')')
        
        # save the result
        result_dict['BP'] = score_BP
        if j == 1:
            result_dict['uni_match'] = count
            result_dict['uni_total'] = len(ngram_trans)
            result_dict['uni_score'] = ngram_score
        elif j == 2:
            result_dict['bi_match'] = count
            result_dict['bi_total'] = len(ngram_trans)
            result_dict['bi_score'] = ngram_score
        elif j == 3:
            result_dict['tri_match'] = count
            result_dict['tri_total'] = len(ngram_trans)
            result_dict['tri_score'] = ngram_score
        elif j == 4:
            result_dict['quad_match'] = count
            result_dict['quad_total'] = len(ngram_trans)
            result_dict['quad_score'] = ngram_score
        else:
            print('ERROR')
            exit()
        
        score += math.log(ngram_score)
    score = math.exp(score/4)
    score *= score_BP

    print('BLEU score of ' + translator_name + ': ' + str(score))

    # check the result
    if abs(score - sentence_bleu([reference[loc]], translator[loc], smoothing_function=SmoothingFunction().method1)) > 1e-5:
        print('ERROR')
        print('BLEU score of NLTK: ' + str(sentence_bleu([reference[loc]], translator[loc], smoothing_function=SmoothingFunction().method1)))
        exit()

    # save the result
    result_dict['BLEU'] = score
    result_dict['BP'] = score_BP
    result_dict['trans_words'] = len(translator[loc])
    result_dict['ref_words'] = len(reference[loc])

    return result_dict

# start the calculation
for i in range(0, 30):
    print('Sentence ' + str(i+1) + ':')
    # calculate the BLEU score
    baidu_dict = BLEU(baidu, reference, i)
    generate_result(baidu_result, baidu_dict)
    print('---------------------------------')
    bing_dict = BLEU(bing, reference, i)
    generate_result(bing_result, bing_dict)
    print('---------------------------------')
    google_dict = BLEU(google, reference, i)
    generate_result(google_result, google_dict)
    print('---------------------------------')
    gpt_dict = BLEU(gpt, reference, i)
    generate_result(gpt_result, gpt_dict)
    print('---------------------------------')
    print('=================================')
print('OK')


