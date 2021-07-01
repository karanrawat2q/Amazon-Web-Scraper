import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from random import random
from time import sleep

def sleep_for_random_interval():
    time_in_seconds = random() * 2
    sleep(time_in_seconds)
    print(f"R#ndom sleep (｀∀´)Ψ ---{time_in_seconds}")

def getUrl(searchTerm, page):
    # Generate a Url from Search term
    sTerm = searchTerm.strip().replace(" ","+")
    urlTemplate = f'https://www.amazon.com/s?k={sTerm}&page={page}&ref=nb_sb_noss'
    return urlTemplate.format(page)


def generateFilename(searchTerm):
    # Generate file name
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = searchTerm.replace(' ', '-') + '_' + timestamp + '.csv'
    return filename


def save(record, filename, newFile=False):
    # Save data to csv
    header = ('description', 'Price', 'Rating', 'reviewCount', 'url')
    if newFile:
        with open(filename, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
    else:
        with open(filename, 'a+', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(record)

def extractRecord(item):
    # Extract and return data from single record
    atag = item.h2.a

    description = atag.text.strip()

    url = "https://www.amazon.com"+ atag.get('href')

    try:
        priceParent = item.find('span',{'class':'a-price'})
        Price = priceParent.span.text
    except AttributeError:
        return

    try:
        Rating = item.i.text
        reviewCount = item.find('span',{'class':'a-size-base'}).text
    except AttributeError:
        Rating = ''
        reviewCount = ''
    
    result = (description, Price, Rating, reviewCount, url)
    
    return result

def main(searchTerm):
    # Run main program routine
    filename = generateFilename(searchTerm)
    save(None, filename, newFile=True) # Initialize a new file
    driver = webdriver.Chrome('D:\Python 3 Projects\chromedriver.exe')
    records = []
    scraped = 0
    for  page in range(1,21):
        # load next page
        searchUrl = getUrl(searchTerm,page)
        print(searchUrl)
        driver.get(searchUrl)
        print('Loading....')
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.findAll('div',{'data-component-type':'s-search-result'})
        
        for item in results:
            record = extractRecord(item)
            if record:
                scraped += 1
                save(record, filename)
        sleep_for_random_interval()
    driver.close()
    print(f"Scraped {scraped} for the search term: {searchTerm}")

if __name__ == '__main__':
    term = input("What you want to scrap: ")
    main(term)