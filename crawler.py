import requests
from bs4 import BeautifulSoup
import json
import traceback
import threading
import time
import io

def crawl_moneydigest():
    # Crawl from http://www.moneydigest.sg/category/deals/dining/page/6/
    num_pages = 27
    base_url = "http://www.moneydigest.sg/category/deals/dining/page/{}/"
    count = 0
    with io.open('result.md', 'w', encoding='utf-8') as f:
        for i in range(num_pages):
            url = base_url.format(i+1)
            p = requests.get(url)
            soup = BeautifulSoup(p.content, "html.parser")
            soup.encode("utf-8")
            articles = soup.find_all("article")

            for art in articles:
                try:
                    count+=1
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