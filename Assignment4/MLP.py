# Multilayer Perceptron

import numpy as np
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt

# Importing the dataset
dataset = pd.read_csv('data.csv')
review = dataset['review'].values
sentiment = dataset['sentiment'].values

for index in range(len(review)):
    review[index] = review[index].replace('\n', ' ')
    oldline = review[index]
    newline = jieba.cut(oldline, cut_all=False)
    review[index] = " ".join(newline)

# build bag of words
words = []
for line in review:
    words.append(line)
vectorizer = CountVectorizer(stop_words=None, max_features=5000)
modified_review = vectorizer.fit_transform(words).toarray()
words_bag = vectorizer.vocabulary_
pd.DataFrame(modified_review)

# splitting the dataset
Xtrain, Xremain, Ytrain, Yremain = train_test_split(modified_review, sentiment, test_size=0.4, random_state=7)
Xtest, Xvalid, Ytest, Yvalid = train_test_split(Xremain, Yremain, test_size=0.5, random_state=7)

text_Xtrain, text_Xremain, text_Ytrain, text_Yremain = train_test_split(review, sentiment, test_size=0.4, random_state=7)
text_Xtest, text_Xvalid, text_Ytest, text_Yvalid = train_test_split(text_Xremain, text_Yremain, test_size=0.5, random_state=7)

# MLP
alphalist = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
clf_list = []
maxscore = 0
best_alpha = 0
for i in alphalist:
    clf = MLPClassifier(hidden_layer_sizes=(100, 100, 100), max_iter=500, alpha=i, random_state=7)
    clf.fit(Xtrain, Ytrain)
    clf_list.append(clf)
    Ypred = clf.predict(Xvalid)
    score = f1_score(Yvalid, Ypred)
    if score > maxscore:
        maxscore = score
        best_alpha = i
    print("alpha =", i, "score =", score)
    
print("Choose alpha =", best_alpha, "as the best alpha.")

Ypred = clf_list[alphalist.index(best_alpha)].predict(Xtest)
score = f1_score(Ytest, Ypred)
print("Test score: ", score)
# Test score:  0.862

# show false positive and false negative samples, header: review, sentiment, prediction
false_positive = []
false_negative = []
for i in range(len(Ypred)):
    if Ypred[i] != Ytest[i]:
        if Ypred[i] == 1:
            false_positive.append([text_Xtest[i], Ytest[i], Ypred[i]])
        else:
            false_negative.append([text_Xtest[i], Ytest[i], Ypred[i]])

false_positive = pd.DataFrame(false_positive)
false_negative = pd.DataFrame(false_negative)

# these samples are saved in the same csv files
false_positive.to_csv('MLP_false_results.csv', index=False, header=['review', 'sentiment', 'prediction'])
false_negative.to_csv('MLP_false_results.csv', index=False, mode='a', header=False)

# confusion matrix
cm = confusion_matrix(Ytest, Ypred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Negative', 'Positive'])
disp.plot()
plt.show()

