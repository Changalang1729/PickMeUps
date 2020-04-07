from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def processShop():
    print('in process shop1')
    more_link = driver.find_element_by_link_text('#more-departments')
    print('in process shop')
    print(more_link)
    more_link.click()
    driver.close()

url = 'https://www.instacart.com/grocery-delivery/tustin-ca'
options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
chrome_driver_binary = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
driver.implicitly_wait(30)
driver.get(url)

shops = driver.find_elements_by_class_name('rmq-5ff715cf')
for shop in shops:
    shop_link = shop.find_elements_by_tag_name('a')[0]
    shop_link.click()
    processShop()
    break
