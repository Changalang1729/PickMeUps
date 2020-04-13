from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# TODO: get the relevant information from the item element and create an Item object
def getItemFromHtml(elem):
    pass

# TODO: get the relevant information from the shop element and create a Shop object
def getShopFromHtml(elem):
    pass

def getItemsForCategory():
    all_items = []
    moreItems = True
    while moreItems:
        items = driver.find_elements_by_class_name('rmq-b2d27d72')
        all_items.extend(items)
        main_content = driver.find_elements_by_class_name('rmq-9aaf6e9d')[0]
        page_bar = main_content.find_element_by_xpath("following-sibling::*")
        arrow = page_bar.find_elements_by_tag_name('svg')[-1]
        arrow_style = arrow.get_attribute("style")
        moreItems = (arrow_style == '') or 'cursor: not-allowed;' not in arrow_style
        if moreItems:
            next_page_link = arrow.find_element_by_xpath("..")
            next_page_link.click()
    return all_items

def processShop():
    more_link = driver.find_element_by_xpath("//a[@href='#more-departments']")
    more_link.click()
    all_categories = driver.find_elements_by_class_name('rmq-bd106dfd')
    needed_categories = [category for category in all_categories if category.tag_name == 'a']
    for category in needed_categories:
        category.click()
        getItemsForCategory()


try:
    url = 'https://www.instacart.com/grocery-delivery/tustin-ca'
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    chrome_driver_binary = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chrome_driver_binary, options=options)
    driver.implicitly_wait(30)
    driver.get(url)

    shops = driver.find_elements_by_class_name('rmq-5ff715cf')
    for shop in shops:
        shop_link = shop.find_elements_by_tag_name('a')[0]
        shop_link.click()
        processShop()
        break
except:
    driver.close()
