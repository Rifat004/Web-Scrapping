#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from csv import writer
import pandas as pd


# # Bookfair(2012-2022)

# In[ ]:


home_url = "https://www.rokomari.com"
base_url = "https://www.rokomari.com/book/category/40/amar-ekushe-bookfair?ref=act_pg0_p2"

title = []
authors = []
prices_original = []
category = []
publishers = []
image=[]
isbn=[]
description=[]


char_to_replace = {
    '\n': ''
}

for i in range(166):
    url = base_url + str(i+1)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    lists = soup.find_all('div', class_="home-details-btn-wrapper")
    
    
    for list in lists:
        for link in list.find_all('a', href=True):
            url_details = home_url + link["href"]
            page_details = requests.get(url_details)
            soup_details = BeautifulSoup(page_details.content, "lxml")
            
            lists_details = soup_details.find_all('div', class_="col details-book-main-info align-self-center")
            lists_authors = soup_details.find_all('p', class_="details-book-info__content-author")
            lists_cat = soup_details.find_all('div', class_="details-book-info__content-category d-flex align-items-center")
            lists_price = soup_details.find_all('div', 'span', class_="details-book-info__content-book-price")
            lists_pub = soup_details.find_all('td', class_="publisher-link")
            lists_isbn = soup_details.find_all('table','td',class_="table table-bordered")
            lists_image = soup_details.find_all('img', class_="look-inside")
            lists_description = soup_details.find_all('div','p', class_="details-book-additional-info__content-summery truncate")
               
            
#Scraping the title of the books
            for list_det in lists_details:
                for details in list_det.find_all('div', class_="details-book-main-info__header"):
                    title.append(details.find('h1').text)
                    
                    
#Scraping the name of the authors
            for author in lists_authors:
                authors.append(author.a.text.translate(str.maketrans(char_to_replace)).strip())
            

# Scraping the category
            for cat in lists_cat:
                category.append(cat.a.text.strip())


# scraping the prices

            for price in lists_price:
                price_origin_info = price.find('strike', class_="original-price")
                if price_origin_info == None:
                    prices_original.append('NA')
                    
                else:
                    prices_original.append(price_origin_info.text.replace('\n', ''))
                    

#Scraping the publications
                                
            for pub in lists_pub:
                publishers.append(pub.a.string.replace('\n','').strip())
                

#Scraping the isbn
                                
            for num in lists_isbn:
                for k in num.text.split():
                    if len(k)==13:
                        isbn.append(k)
                           
                
#Scraping the book images
                                
            for img in lists_image:
                image.append(img['src'])
                
#scraping the description

                                
            for des in lists_description:
                description.append(des.text.replace('\n','').strip())
                
        

################################  Final csv #################################
                
dict_book = {
    "Title": title,
    "Author": authors,
    "Publisher": publishers,
    "ISBN": isbn,
    "Original Price": prices_original,
    "Genre": category,
    "Thumbnail": image,
    "Summary": description
    
}
book_df = pd.DataFrame.from_dict(dict_book, orient='index') 
book_df = book_df.transpose()
book_df.to_csv('boimela.csv', index=False) 


# In[ ]:




