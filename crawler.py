import io
import requests
from bs4 import BeautifulSoup
import html2text
from datetime import datetime

from selenium import webdriver
# https://pypi.python.org/pypi/selenium/2.7.0



def crawl_moneydigest():
    # Crawl from http://www.moneydigest.sg/category/deals/dining/page/6/
    num_pages = 31
    base_url = "http://www.moneydigest.sg/category/deals/dining/page/{}/"
    new_url = "http://www.moneydigest.sg/category/deals/dining/"
    count = 0
    with io.open('result.md', 'w', encoding='utf-8') as f:
        for i in range(num_pages):
            url = base_url.format(i+1)

            # broswer = webdriver.Safari()
            # broswer.get(url)
            # html = broswer.page_source
            # print html
            # break

            ####
            p = requests.get(url)
            # p = requests.get(new_url)
            print 'page %s' % (i+1)
            soup = BeautifulSoup(p.content, "html.parser")
            # print soup
            # soup = BeautifulSoup(p.content, "html5lib")
            soup.encode("utf-8")
            # html = html2text.html2text(repr(soup))
            # print html
            # print soup

            articles = soup.find_all("article")

            for art in articles:
                try:
                    count+=1
                    print 'item %s' % count
                    times = art.header.find('span',{'class':'posted-on'}).find_all('time')
                    publish_time = times[0].text
                    print publish_time
                    f.write(u'publish time {}\n'.format(publish_time))
                    pt = datetime.strptime('March 22, 2017', '%B %d, %Y')
                    if pt < datetime(2017, 2, 1):
                        print 'Old post, older than Feb 1, 2017'
                        continue
                    header = art.header.h2
                    title = header.a.text
                    link = header.a['href']
                    ps = art.find('div', {'class':'entry-content article-content'}).find_all('p')
                    content = ps[1].text
                    f.write(u'**[{}] {}**\n\n'.format(str(count),title))
                    f.write(u'{}\n\n'.format(link))
                    f.write(u'{}\n\n'.format(content))
                except Exception as e:
                    print e.message
                    continue

if __name__ == '__main__':
    crawl_moneydigest()
