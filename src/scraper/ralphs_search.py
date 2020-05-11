from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import csv
import os.path

ZIP_CODE = '92602'
# 'Milk', 'Eggs', 'Paper towels', 'Bread', 'Flour', 'Toilet paper', 'Chips', 'fruits', 'Soap', 'Body wash', 'Shampoo', 'Pasta', 'Rice', 'Water', 'Meat','Wine','Thermometer', 'Cough medicine', 'vegetables', 'Tylenol', 'Advil', 'Medicine'
# didn't work: 'Medicine',
SEARCH_ITEMS = []
# maximum distance from ZIP_CODE
DISTANCE_THRESHOLD = 7

# Get relevant product information from each product and put it
# in the csv named by store_name. If first is True, write the csv
# header along with the product info.
def processProduct(product, store_name, item, first):
    name = ''
    size = ''
    price = ''
    image_url = ''
    names = product.find_elements_by_class_name('ProductCard-name')
    if len(names) != 0:
        name = names[0].get_attribute('innerHTML')
    sizes = product.find_elements_by_class_name('ProductCard-sellBy-unit')
    if len(sizes) != 0:
        size = sizes[0].get_attribute('innerHTML')
    prices = product.find_elements_by_class_name('kds-Price')
    if len(prices) != 0:
        price = prices[0].get_attribute('value')
    image_urls = product.find_elements_by_class_name('ImageLoader-image')
    if len(image_urls) != 0:
        image_url = image_urls[0].get_attribute('src')

    try:
      dirsname = 'ralphs_data/' + store_name
      if not os.path.exists(dirsname):
        os.makedirs(dirsname)

      # open the right file in the right directory for the Ralphs being scraped
      with open(dirsname + '/' + item + '.csv', 'a') as cvs:
        csv_writer_obj = csv.writer(cvs, delimiter = ',', dialect = 'excel')
        if first:
            # Write the csv header
            csv_writer_obj.writerow(['Store', 'Product', 'Size', 'Price', 'Url', 'Category'])
        csv_writer_obj.writerow(['Ralphs_' + store_name, name, size, price, image_url, item])
    except Exception as e:
        print(e)

# Given the search item, scrape all products that pop up for that search item.
# For each product, get specific information about that product from the html
# by calling processProduct. If the next page button is not present, then the scraper
# has reached the last page for the search item and all products for that search
# item have been scraped. If the next page button is present, click on it
# and repeat.
def processCategory(store_name, item):
    hasNextPage = True
    i = 0
    first = True
    while hasNextPage:
        productCard = driver.find_elements_by_class_name('ProductCard')
        for product in productCard:
            # If first is True, then the csv header is written
            # along with the product information in the csv
            # (see processProduct)
            processProduct(product, store_name, item, first)
            first = False
            # TAKE THIS OUT
            # i += 1
            # if i == 100:
            #     return
        nextPageLink = driver.find_elements_by_xpath("//li[@class='Pagination-item Pagination-next']")
        hasNextPage = (len(nextPageLink) > 0)
        if hasNextPage:
            nextPageLink[0].click()

# Given the store name, scrape all products from the SEARCH_ITEMS list.
def processStore(store_name):
    first = True
    for item in SEARCH_ITEMS:
        driver.find_element_by_xpath("//button[@class='SearchButton text-default-400 border border-default-900']").click()
        if not first:
            driver.find_element_by_xpath("//button[@class='kds-Button kds-Button--primaryInverse ClearButton']").click()
        driver.find_element_by_id("searchbar").send_keys(item)
        driver.find_element_by_xpath("//button[@class='kds-Button kds-Button--primaryInverse kds-Button--hasIconOnly kds-FormField-iconButton']").click()
        processCategory(store_name, item)
        first = False

try:
    url = 'https://www.ralphs.com/'
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    # options.binary_location = '/Users/vikas/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome'
    chrome_driver_binary = '/usr/local/bin/chromedriver'


    driver = webdriver.Chrome(chrome_driver_binary, options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    driver.find_element_by_xpath("//button[@class='kds-GlobalMessage-closeButton p-0 border-none text-default-900 rounded-full']").click()
    driver.find_element_by_xpath("//button[@class='CurrentModality-button py-4 px-0 text-left']").click()
    driver.find_element_by_xpath("//input[@class='kds-Input kds-Input--compact']").clear()
    driver.find_element_by_xpath("//input[@class='kds-Input kds-Input--compact']").send_keys(ZIP_CODE)
    all_stores = set()
    seen_stores = set()
    # add scraped stores here
    seen_stores.add('13321 Jamboree Rd, Tustin, CA')
    seen_stores.add('14400 Culver Dr, Irvine, CA')
    first = True

    # On the first iteration, this loop opens up the store modal and finds the names
    # of all stores that are within DISTANCE_THRESHOLD, storing those stores in all_stores.
    # On all other iterations, this loop finds the next store to scrape by looking through
    # all_stores to find the next store within DISTANCE_THRESHOLD that hasn't been
    # visited yet (not in seen_stores). It then scrapes that store, and after
    # it is finished, adds it to seen_stores.
    while True:
        if not first:
            # open the search zip code modal
            driver.find_element_by_xpath("//button[@class='CurrentModality-button py-4 px-0 text-left']").click()
        if first:
            # click search
            driver.find_element_by_xpath("//button[@class='kds-Button kds-Button--primary kds-Button--compact']").click()
            # click select store
            driver.find_element_by_xpath("//button[@aria-label='In-Store [object Object]   Select Store']").click()
        else:
            # click change store
            driver.find_element_by_xpath("//button[@aria-label='In-Store [object Object] Currently Shopping undefined Change Store']").click()

        store_divs = driver.find_elements_by_xpath("//div[@class='ModalitySelector--StoreSearchResult sm:flex sm:flex-row flex-col border-default-400 ml-24 py-16 border-solid border-t-none border-r-none border-l-none border-b']")
        store_addresses = driver.find_elements_by_xpath("//div[@class='kds-Text--s text-default-600']")
        distance_elems = driver.find_elements_by_xpath("//div[@class='kds-Text--s text-default-600 sm:pl-0 mb-12']")

        # Populate all_stores with the store names that are valid and within distance
        if first:
            for i in range(len(store_addresses)):
                distance = distance_elems[i].get_attribute('innerHTML').split()[0]
                if float(distance) > DISTANCE_THRESHOLD or len(store_divs[i].find_elements_by_xpath(".//button[@class='kds-Button kds-Button--primary kds-Button--compact']")) == 0:
                    continue
                else:
                    all_stores.add(store_addresses[i].get_attribute('innerHTML').replace('<br>', ', '))

        # Find a store in all_stores to scrape (can't be in seen_stores)
        store_index = 0
        num_stores = len(store_addresses)
        store_address = None
        found_store = False
        for i in range(len(store_addresses)):
            curr_address = store_addresses[i].get_attribute('innerHTML').replace('<br>', ', ')
            distance = distance_elems[i].get_attribute('innerHTML').split()[0]
            if curr_address in all_stores and curr_address not in seen_stores:
                store_address = curr_address
                store_index = i
                found_store = True
                break

        # If found_store is False, all stores have been scraped
        if not found_store:
            break

        print(store_address)
        print(store_index)
        store_divs[store_index].find_elements_by_xpath("//button[@class='kds-Button kds-Button--primary kds-Button--compact']")[store_index].click()
        # close the green box
        driver.find_element_by_xpath("//button[@class='kds-Toast-closeButton text-default-900 rounded-full p-0 border-none']").click()
        print('done')
        # Add current store to seen_stores
        seen_stores.add(store_address)
        # Scrape the store (see above for processStore)
        processStore(store_address)
        first = False

except Exception as e:
    print(e)
