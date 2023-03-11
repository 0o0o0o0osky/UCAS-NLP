import newspaper
import datetime

# I'm not a bad guy. :-)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

config = newspaper.Config()
config.browser_user_agent = USER_AGENT
config.fetch_images = False

# You can change the start day and the end day.
startday = datetime.date(2019, 2, 1)
endday = datetime.date(2022, 12, 31)

# Record titie and text
articles_text = []
articles_num = 0

# The people's Daily
URL1 = 'http://paper.people.com.cn/rmrb/html/'
URL2 = '/nw.D110000renmrb_'
URL3 = '.htm'

for day in range((endday-startday).days + 1):
    now = startday + datetime.timedelta(day)
    for num1 in range(1,15):
        for num2 in range (1,21):
            URL = URL1 + now.strftime('%Y-%m/') + now.strftime('%d') + URL2 + now.strftime('%Y%m%d_') + "%d"%num1 + "-%02d"%num2 + URL3
            try:
                article = newspaper.Article(URL, language='zh')
                article.download()
                article.parse()
            # If there raises an exception, most of the time it is 404 Not Found.
            except:
                pass
                break
            # Sometimes we fail to fetch articles, skip and ignore.
            if article.title != None and article.text != None and article.text[0:4] != '版权声明' and article.text[0:6] != '我给文章打分':
                articles_text.append(article.text)
                articles_num += 1
                print("1 article added, %d articles in total."%articles_num)
            else:
                continue
    print(now.strftime("%Y-%m-%d") + " is over.")
    if now.month % 12 + 1 == (now + datetime.timedelta(1)).month:
        # Save per month
        print("Now we save these articles.")
        str = ''
        with open('./raw/%d/%d-%d.txt'%(now.year, now.year, now.month), 'a', encoding='utf-8') as f:
            f.write(str.join(articles_text))
        articles_text.clear()
        print("Now we continue.")

print("OK. There are %d articles in total."%articles_num)