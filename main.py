from bs4 import BeautifulSoup
import requests
import sys


class Article:
    def __init__(self, text, category):
        self.text = text
        self.category = category


def got_site_info(page):
    response = requests.get(f'https://www.dziennik.pl/artykuly,{page}')
    if response.status_code == 200:
        return response
    else:
        print('cannot find urls')
        return False


def parse_html_to_urls(html, i):
    soup = BeautifulSoup(html, 'html.parser')
    links_array = []
    for link in soup.section.find_all('a'):
        links_array.append(link.get('href'))

    #     remove last link to nex page and to previous
    if i > 0:
        links_array.pop()
    links_array.pop()
    return links_array


def get_article_html(link):
    # print(f'{link}\n')
    response = requests.get(link)
    if response.status_code == 200:
        return response
    else:
        print('cannot reach')
        return False

def get_category_from_link(link):
    return link.split('.')[0].split('//')[1]

def parse_article(html_to_parse):
    soup = BeautifulSoup(html_to_parse, 'html.parser')
    article_text = ""
    for paragraph in soup.find_all(class_='hyphenate'):
        article_text += paragraph.get_text()
    return article_text


if __name__ == '__main__':
    separator_category = '(=-=-=-)'
    separator_article = '\n-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=\n'
    pagesOfArticles = 2

    fileText = ""
    links = []

    print('Getting articles:')

    for i in range(pagesOfArticles):
        html = got_site_info(i + 1)
        if not html:
            sys.exit()
        links = links + parse_html_to_urls(html.text, i)
        print(f'Page: {i + 1}')

    print(f'\ngot {len(links)} links to articles\n')

    for i in range(len(links)):
        print(f'processing article: {i}')

        fileText += get_category_from_link(links[i])
        fileText += separator_category

        articleHtml = get_article_html(links[i])
        fileText += parse_article(articleHtml.text)
        fileText += separator_article

    print('\nsaving to file...')

    with open("Output.txt", "w") as text_file:
        text_file.write(fileText)

    print('articles saved!')
