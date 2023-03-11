import requests
import newspaper
from bs4 import BeautifulSoup
import re

headers = {
    'Accept': "application/json, text/plain, */*",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

articles_text=[]
articles_num = 0

# CNN
source_url = 'https://edition.cnn.com'
cnn_categories = ['health', 'world', 'business', 'markets', 'sport', 'weather', 'entertainment', 'politics', 'style', 'tech']
for category in cnn_categories:
    news_num=0
    if category == 'tech':
        url = source_url + '/' + 'business' + '/' + category
    else:
        url = source_url + '/' + category
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    article_urls = []
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            if category != 'style':
                article_url = re.findall('/\d{4}/\d{2}/\d{2}/\w+/.+', a['href'])
            else:
                article_url = re.findall('/%s/article/.+'%category, a['href'])
            if article_url:
                article_urls += article_url
            else:
                continue
        else:
            continue
    for article_url in article_urls:
        try:
            article = newspaper.Article(url=source_url + article_url, language='en')
            article.download()
            article.parse()
        except:
            pass
            break
        if article.text != None:
            articles_text.append(article.text)
            articles_num += 1
            news_num += 1
            print("1 article added, %d articles in total."%news_num)
        else:
            continue
    print("Now we save these articles.")
    str = ''
    with open('./raw/cnn/%s.txt'%(category), 'a', encoding='utf-8') as f:
        f.write(str.join(articles_text))
        articles_text.clear()
    print("Now we continue.")
print("OK")


# CBS
source_url = 'https://www.cbsnews.com'
cbs_categories = ['us', 'world', 'cbsvillage', 'moneywatch', 'healthwatch', 'science', 'entertainment', 'politics', 'crime', 'technology']
article_urls = []
str = ''
for category in cbs_categories:
    url = source_url + '/' + category
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            article_url = re.findall('https://www.cbsnews.com/news/.+', a['href'])
            if article_url:
                article_urls += article_url
            else:
                continue
        else:
            continue
    print("Now we finish %s."%category)
for article_url in list(set(article_urls)):
    try:
        article = newspaper.Article(url=article_url, language='en')
        article.download()
        article.parse()
    except:
        pass
    if article.text != None:
        articles_text.append(article.text)
    else:
        continue
with open('./raw/cbs/raw.txt', 'a', encoding='utf-8') as f:
    f.write(str.join(articles_text))
print("OK.")


# ABC
source_url = 'https://abcnews.go.com/'
cnn_categories = ['US', 'Politics', 'International', 'Entertainment', 'Business', 'Technology', 'Lifestyle', 'Health', 'Sports']
for category in cnn_categories:
    news_num=0
    url = source_url + category
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    article_urls = []
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            article_url = re.findall(url + '/.+', a['href'])
            if article_url:
                article_urls += article_url
            else:
                continue
        else:
            continue
    for article_url in article_urls:
        try:
            article = newspaper.Article(url=article_url, language='en')
            article.download()
            article.parse()
        except:
            pass
            break
        if article.text != None:
            articles_text.append(article.text)
            articles_num += 1
            news_num += 1
            print("1 article added, %d articles in total."%news_num)
        else:
            continue
    print("Now we save these articles.")
    str = ''
    with open('./raw/abc/%s.txt'%(category), 'a', encoding='utf-8') as f:
        f.write(str.join(articles_text))
        articles_text.clear()
    print("Now we continue.")
print("OK")


# National Geographic
source_url = 'https://www.nationalgeographic.com/'
cnn_categories = ['animals', 'environment', 'history', 'science', 'travel']
for category in cnn_categories:
    news_num=0
    url = source_url + category
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    article_urls = []
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            article_url = re.findall(url + '/.+', a['href'])
            if article_url:
                article_urls += article_url
            else:
                continue
        else:
            continue
    for article_url in article_urls:
        try:
            article = newspaper.Article(url=article_url, language='en')
            article.download()
            article.parse()
        except:
            pass
            break
        if article.text != None:
            articles_text.append(article.text)
            articles_num += 1
            news_num += 1
            print("1 article added, %d articles in total."%news_num)
        else:
            continue
    print("Now we save these articles.")
    str = ''
    with open('./raw/ng/%s.txt'%(category), 'a', encoding='utf-8') as f:
        f.write(str.join(articles_text))
        articles_text.clear()
    print("Now we continue.")
print("OK")


# Fox News
source_url = 'https://www.foxnews.com'
cnn_categories = ['us', 'politics', 'world', 'opinion', 'media', 'entertainment', 'sports', 'lifestyle', 'science', 'health']
for category in cnn_categories:
    url = source_url + '/' + category
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    article_urls = []
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            article_url = re.findall('/%s/[^/]{20,}'%category, a['href'])
            if article_url:
                article_urls += article_url
            else:
                continue
        else:
            continue
    for article_url in list(set(article_urls)):
        try:
            article = newspaper.Article(url=source_url + article_url, language='en')
            article.download()
            article.parse()
        except:
            pass
            break
        if article.text != None:
            articles_text.append(article.text)
        else:
            continue
    print("Now we save these articles.")
    str = ''
    with open('./raw/fox/%s.txt'%(category), 'a', encoding='utf-8') as f:
        f.write(str.join(articles_text))
        articles_text.clear()
    print("Now we continue.")
print("OK")


# AP News
source_url = 'https://apnews.com/hub'
cnn_categories = ['us-news', 'world-news', 'politics', 'sports', 'entertainment', 'business', 'technology', 'lifestyle', 'science', 'health', 'oddities', 'photography']
for category in cnn_categories:
    url = source_url + '/' + category
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    article_urls = []
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            article_url = re.findall('/article/.+', a['href'])
            if article_url:
                article_urls += article_url
            else:
                continue
        else:
            continue
    for article_url in list(set(article_urls)):
        try:
            article = newspaper.Article(url='https://apnews.com' + article_url, language='en')
            article.download()
            article.parse()
        except:
            pass
            break
        if article.text != None:
            articles_text.append(article.text)
        else:
            continue
    print("Now we save these articles.")
    str = ''
    with open('./raw/ap/%s.txt'%(category), 'a', encoding='utf-8') as f:
        f.write(str.join(articles_text))
        articles_text.clear()
    print("Now we continue.")
print("OK")
