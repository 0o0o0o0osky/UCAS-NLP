# Multinomial Naive Bayes Classifier

import numpy as np
import pandas as pd
import jieba
import warnings
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# Importing the dataset
dataset = pd.read_csv('data.csv')
review = dataset['review'].values
sentiment = dataset['sentiment'].values

for index in range(len(review)):
    review[index] = review[index].replace('\n', ' ')
    oldline = review[index]
    newline = jieba.cut(oldline, cut_all=False)
    review[index] = " ".join(newline)

mystopwords = []
with open('.\\stopwords\\stopwords.txt', 'r', encoding='utf8') as f:
    words = f.readlines()
    for word in words:
        new_word = word.strip()
        mystopwords.append(new_word)

# splitting the dataset
Xtrain, Xremain, Ytrain, Yremain = train_test_split(review, sentiment, test_size=0.4, random_state=7)
Xtest, Xvalid, Ytest, Yvalid = train_test_split(Xremain, Yremain, test_size=0.5, random_state=7)

# converting to list
t1=Xtrain.tolist()
t2=Ytrain.tolist()
train_list = {'review':t1, 'sentiment': np.array(t2)}

t3=Xvalid.tolist()
t4=Yvalid.tolist()
valid_list = {'review':t3, 'sentiment': np.array(t4)}

t5=Xtest.tolist()
t6=Ytest.tolist()
test_list = {'review':t5, 'sentiment': np.array(t6)}

# dataframe
train_list = pd.DataFrame(train_list)
valid_list = pd.DataFrame(valid_list)
test_list = pd.DataFrame(test_list)

alphalist = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100]
clf_list = []
maxscore = 0
best_alpha = 0

for i in alphalist:
    clf = MultinomialNB(alpha=i)
    vectorizer = TfidfVectorizer(stop_words=mystopwords, max_df=0.8, min_df=3)
    X_train = vectorizer.fit_transform(train_list["review"].values.astype('U'))
    Y_train = train_list['sentiment']
    clf_list.append(clf.fit(X_train, Y_train))
    X_valid = vectorizer.transform(valid_list['review'].values.astype('U'))
    Y_valid = valid_list['sentiment']
    pred = clf.predict(X_valid)
    score = f1_score(Y_valid, pred)
    if score > maxscore:
        maxscore = score
        best_alpha = i
    print("alpha =", i, "score =", score)

print("Choose alpha =", best_alpha, "as the best alpha.")

index = alphalist.index(best_alpha)
clf = clf_list[index]
X_test = vectorizer.transform(test_list['review'].values.astype('U'))
Y_test = test_list['sentiment']
pred = clf.predict(X_test)
score = f1_score(Y_test, pred)
print("Test score =", score)
# Test score =  0.846

# show false positive and false negative samples, header: review, sentiment, prediction
false_positive = []
false_negative = []
for i in range(len(pred)):
    if pred[i] != Y_test[i]:
        if pred[i] == 1:
            false_positive.append([test_list['review'][i], Y_test[i], pred[i]])
        else:
            false_negative.append([test_list['review'][i], Y_test[i], pred[i]])

false_positive = pd.DataFrame(false_positive)
false_negative = pd.DataFrame(false_negative)

# these samples are saved in the same csv files
false_positive.to_csv('MNB_false_results.csv', index=False, header=['review', 'sentiment', 'prediction'])
false_negative.to_csv('MNB_false_results.csv', index=False, mode='a', header=False)

# Confusion Matrix
cm = confusion_matrix(Y_test, pred)
print(cm)

# Output the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Negative', 'Positive'])
disp.plot()
plt.show()
