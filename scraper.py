from bs4 import BeautifulSoup
import requests
import sys
from enum import Enum
import re

class Category(Enum):
    WEATHER = 'pogoda'
    POLITICS = 'polityka'
    SPORT = 'sport'
    ECONOMY = 'ekonomia'
    SCIENCE = 'nauka'
    CULTURE = 'kultura'


class Article:
    def __init__(self, text, category):
        self.text = text
        self.category = category


def got_site_info(category, page):
    response = requests.get(f'https://www.rmf24.pl/{category},nPack,{page}')
    if response.status_code == 200:
        return response
    else:
        print('cannot find urls')
        return False

def has_class_but_no_id(tag):
    return tag.has_attr('h3') and tag.has_attr('a')

def parse_html_to_urls(html, i):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.find("div", class_="categoryPage").find_all('h3'))
    links_array = []
    for link in soup.find("div", class_="categoryPage").find_all('h3'):
        # print(link.a.get('href'))
        links_array.append(link.a.get('href'))

    #     remove last link to nex page and to previous
    # if i > 0:
    #     links_array.pop()
    # links_array.pop()
    return links_array


def get_article_html(link, category):
    # print(f'{link}\n')
    domain = 'https://www.rmf24.pl/'
    if '/raport-' in link:
        domain = domain + category
    response = requests.get(domain+link)
    if response.status_code == 200:
        return response
    else:
        print('cannot reach')
        return False

# def get_category_from_link(link):
#     return link.split('.')[0].split('//')[1]

def parse_article(html_to_parse):
    soup = BeautifulSoup(html_to_parse, 'html.parser')
    article_text = ""
    for paragraph in soup.find(class_='article-body').find_all(['p', 'b'], text=True, recursive=False):
        article_text += paragraph.get_text()
    for paragraph in soup.find(class_='articleContent').find_all(['p', 'b'], text=True, recursive=False):
        article_text += paragraph.get_text()
    return article_text

def getNews():
    polityka = 13908
    sport = 3352
    ekonomia = 2379
    nauka = 1616
    kultura = 1094
    pogoda = 492

    categories = [Category.SPORT, Category.CULTURE, Category.SCIENCE, Category.WEATHER, Category.ECONOMY, Category.POLITICS]
    separator_category = '(=-=-=-)'
    separator_article = '\n-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=\n'
    pagesOfArticles = 100

    print('Create empty file')
    with open("Output.txt", "w") as text_file:
        text_file.write("")

    for category in categories:
        print(f'\nGetting articles by category: {category.value}')
        links = []
        fileText = ""

        print('Page: ', end='')
        for i in range(pagesOfArticles):
            html = got_site_info(category.value, i + 1)
            if not html:
                sys.exit()
            try:
                tempLink = parse_html_to_urls(html.text, i)
                links = links + tempLink
            except Exception as exc:
                print(f'getting link error: {exc}')

            print(f'{i + 1} ', end='', flush=True)
            if i % 20 == 0:
                print('')

        print(f'\ngot {len(links)} links to articles\n')
        print('Processing article:')
        for i in range(len(links)):
            try:
                tempFileText = ""
                print(f'{i} ', end='', flush=True)
                if i % 20 == 0:
                    print('')

                # fileText += get_category_from_link(links[i])
                tempFileText += category.value
                tempFileText += separator_category

                articleHtml = get_article_html(links[i], category.value)
                if articleHtml:
                    tempFileText += parse_article(articleHtml.text)
                tempFileText += separator_article
                fileText += tempFileText
            except Exception as exc:
                print(f'getting article error: {exc}')

        print('saving to file...')

        with open("Output.txt", "a") as text_file:
            text_file.write(fileText)

    print('articles saved!')

def countNews():
    separator_article = '-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\='

    with open("Output.txt", "r") as text_file:
        print(f'Number of news: {text_file.read().count(separator_article)}')



if __name__ == '__main__':
    getNews()
    countNews()