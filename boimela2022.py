#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.rokomari.com/book/category/2657/book-fair-2022'

res = requests.get(url).text
try:
    bookContent = BeautifulSoup(res, 'html.parser')
    pagination = bookContent.find("div", class_='pagination')
    totalPage = pagination.find_all('a')
    page = int(totalPage[len(totalPage) - 2].text)
    

    for x in range(page + 1):
        
        sourceCode = requests.get(url + str(x + 1)).text

        
        soup = BeautifulSoup(sourceCode, 'html.parser')

        
        for eachBook in soup.find_all('div', {'class': 'book-list-wrapper'}):
            content = []
            bookTitle = eachBook.find('p', {'class': 'book-title'}).text
            bookAuthor = eachBook.find('p', {'class': 'book-author'}).text
            bookStatus = eachBook.find('p', {'class': 'book-status'}).text
            try:
                bookOrgPrice = eachBook.find('p', {'class': 'book-price'}).strike.text
            except:
                bookOrgPrice = ''
            bookPrice = eachBook.find('p', {'class': 'book-price'}).span.text

            content.append([bookTitle, bookAuthor, bookStatus, bookOrgPrice, bookPrice])
            print(content)

            with open("bookfair2022.csv", 'a', newline='', encoding='utf-8') as csvfile:
                csvfile.write('\ufeff')
                writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
                writer.writerows(content)

except Exception as e:
    print(e)

