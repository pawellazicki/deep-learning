# from selenium import webdriver
import array

from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys

def gotSiteInfo():
    response = requests.get("https://www.dziennik.pl/artykuly,1")
    if response.status_code == 200:
        print('got urls')
        return response
    else:
        print('cannot find urls')
        return False

def parseHtmlToUrls(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.section.find_all('a'):
        links.append(link.get('href'))
#     remove last link to nex page
    links.pop()
    return links

def getArticleSite(link):
    response = requests.get(link)
    if response.status_code == 200:
        return response
    else:
        print('cannot reach')
        return False

def parseArticle(html):
    soup = BeautifulSoup(html, 'html.parser')
    articleText = ""
    for paragraph in soup.find_all(class_='hyphenate'):
        articleText += paragraph.get_text()
    return articleText

if __name__ == '__main__':
    separator = "\n-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=-\=\n"
    fileText = ""

    html = gotSiteInfo()
    if html == False:
        sys.exit()
    links = parseHtmlToUrls(html.text)


    for link in links:
        articleHtml = getArticleSite(link)
        fileText += parseArticle(articleHtml.text)
        fileText += separator

    with open("Output.txt", "w") as text_file:
        text_file.write(fileText)
    print("finished")