from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import csv

ZIP_CODE = '92602'
SEARCH_ITEMS = ['Milk', 'Eggs', 'Paper towels', 'Bread', 'Flour', 'Toilet paper', 'Chips', 'Vegetables', 'Fruits', 'Soap', 'Body wash', 'Shampoo', 'Pasta', 'Rice', 'Water', 'Meat', 'Wine', 'Pain killers', 'Medicine', 'Thermometer', 'Cough medicine']
DISTANCE_THRESHOLD = 7

def processProduct(product):
    # names = product.find_elements_by_class_name('ProductCard-name')
    # if len(names) == 0:
    #     print('failed on name')
    # else:
    #     name = names[0].get_attribute('innerHTML')
    # sizes = product.find_elements_by_class_name('ProductCard-sellBy-unit')
    # if len(sizes) == 0:
    #     print('failed on size')
    # else:
    #     size = sizes[0].get_attribute('innerHTML')
    # prices = product.find_elements_by_class_name('kds-Price')
    # if len(prices) == 0:
    #     print('failed on price')
    # else:
    #     price = prices[0].get_attribute('value')
    # image_urls = product.find_elements_by_class_name('ImageLoader-image')
    # if len(image_urls) == 0:
    #     print('failed on image')
    # else:
    #     image_url = image_urls[0].get_attribute('src')
    # print(name)
    try:
      names = product.find_elements_by_class_name('ProductCard-name')
      name = names[0].get_attribute('innerHTML')
      sizes = product.find_elements_by_class_name('ProductCard-sellBy-unit')
      size = sizes[0].get_attribute('innerHTML')
      prices = product.find_elements_by_class_name('kds-Price')
      price = prices[0].get_attribute('value')
      image_urls = product.find_elements_by_class_name('ImageLoader-image')
      image_url = image_urls[0].get_attribute('src')

      with open('data/1' + '.csv', 'a') as cvs:
        csv_writer_obj = csv.writer(cvs, delimiter = ',', dialect = 'excel')
        csv_writer_obj.writerow([name, size, price, image_url])
        # csv_writer_obj.writerow([Ralphs_addr, name, size, price, image_url, category])
    except Exception as e:
        print(e)

def processCategory():
    hasNextPage = True
    i = 0
    while hasNextPage:
        productCard = driver.find_elements_by_class_name('ProductCard')
        for product in productCard:
            processProduct(product)
            # TAKE THIS OUT
            i += 1
            if i == 100:
                return
        nextPageLink = driver.find_elements_by_xpath("//li[@class='Pagination-item Pagination-next']")
        hasNextPage = (len(nextPageLink) > 0)
        if hasNextPage:
            nextPageLink[0].click()

def processStore(store_name):
    first = True
    for item in SEARCH_ITEMS:
        driver.find_element_by_xpath("//button[@class='SearchButton text-default-400 border border-default-900']").click()
        if not first:
            driver.find_element_by_xpath("//button[@class='kds-Button kds-Button--primaryInverse ClearButton']").click()
        driver.find_element_by_id("searchbar").send_keys(item)
        driver.find_element_by_xpath("//button[@class='kds-Button kds-Button--primaryInverse kds-Button--hasIconOnly kds-FormField-iconButton']").click()
        processCategory()
        first = False
        # TAKE THIS OUT
        break

try:
    url = 'https://www.ralphs.com/'
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    chrome_driver_binary = '/usr/local/bin/chromedriver'


    driver = webdriver.Chrome(chrome_driver_binary, options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    driver.find_element_by_xpath("//button[@class='kds-GlobalMessage-closeButton p-0 border-none text-default-900 rounded-full']").click()
    driver.find_element_by_xpath("//button[@class='CurrentModality-button py-4 px-0 text-left']").click()
    driver.find_element_by_xpath("//input[@class='kds-Input kds-Input--compact']").clear()
    driver.find_element_by_xpath("//input[@class='kds-Input kds-Input--compact']").send_keys(ZIP_CODE)
    # distance = 0
    # start_shopping_index = 0
    all_stores = set()
    seen_stores = set()
    first = True
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

        # populate stores with the store names that are valid and within distance
        if first:
            for i in range(len(store_addresses)):
                distance = distance_elems[i].get_attribute('innerHTML').split()[0]
                if float(distance) > DISTANCE_THRESHOLD or len(store_divs[i].find_elements_by_xpath(".//button[@class='kds-Button kds-Button--primary kds-Button--compact']")) == 0:
                    continue
                else:
                    all_stores.add(store_addresses[i].get_attribute('innerHTML').replace('<br>', ', '))

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

        if not found_store:
            break

        print(store_address)
        print(store_index)
        store_divs[store_index].find_elements_by_xpath("//button[@class='kds-Button kds-Button--primary kds-Button--compact']")[store_index].click()
        # close the green box
        driver.find_element_by_xpath("//button[@class='kds-Toast-closeButton text-default-900 rounded-full p-0 border-none']").click()
        # PUT THIS BACK!
        # time.sleep(10)
        print('done')
        seen_stores.add(store_address)
        processStore(store_address)
        # TAKE THIS OUT
        break
        first = False

except Exception as e:
    print(e)
