from pprint import pprint
import requests
import re
from fake_headers import Headers
import bs4

KEYWORDS = ['Python', 'SQL' ]


headers = Headers(browser="chrome", os="windows").generate()
response = requests.get(url="https://habr.com/ru/articles", headers=headers)


soup = bs4.BeautifulSoup(response.text, features='lxml')
articles = soup.find_all(name='article')

def sort_articles_by_title(KEYWORDS=KEYWORDS):
    print("Сортировка по наличию в заголовке статьи:")
    if articles:
        for article in articles:
            title_tag = article.find('a', class_='tm-title__link')
            if title_tag:
                title = title_tag.get_text(strip=True)
                for keyword in KEYWORDS: 
                    if keyword.lower() in title.lower():
                        link = title_tag['href']
                        full_link = f"https://habr.com{link}"

                        time_tag = article.find('time')
                        time = time_tag['datetime'] if time_tag else "время не указано"
                        print(f"<{time}>-<{title}>-<{full_link}>")

def sort_articles_by_content(): 
    print("Сортировка по наличию в статье:")
    if articles:
        for article in articles:
            title_tag = article.find('a', class_='tm-title__link')
            if title_tag:
                link = title_tag['href']
                full_link = f"https://habr.com{link}"

                article_response = requests.get(full_link, headers=headers)
                if article_response.status_code == 200:
                    article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')
                    content = article_soup.find('div', class_='tm-article-body')
                    full_text = content.get_text(strip=True) if content else ""

                    for keyword in KEYWORDS:
                        if keyword.lower() in full_text.lower():
                            time_tag = article.find('time')
                            time = time_tag['datetime'] 
                            print(f"<{time}>-<{title_tag.get_text(strip=True)}>-<{full_link}>")

if __name__ == '__main__':
    sort_articles_by_title()  
    sort_articles_by_content()
