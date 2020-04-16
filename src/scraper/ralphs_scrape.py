from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def processProduct(product):
    pass

def processType():
    hasNextPage = True
    while hasNextPage:
        productCard = driver.find_elements_by_class_name('ProductCard')
        for product in productCard:
            processProduct(product)
        nextPageLink = driver.find_elements_by_xpath("//li[@class='Pagination-item Pagination-next']")
        hasNextPage = (len(nextPageLink) > 0)
        if hasNextPage:
            nextPageLink[0].click()


def processSubDepartment(url):
    index = 0
    while True:
        driver.get(url)
        clickMoreElems = driver.find_elements_by_xpath("//button[@class='ImageLink-subText text-action-800']")
        productCards = driver.find_elements_by_class_name('ProductCard')
        if len(clickMoreElems) and len(productCards) == 0:
            driver.get(url)
            clickMoreElems = driver.find_elements_by_xpath("//button[@class='ImageLink-subText text-action-800']")
            productCards = driver.find_elements_by_class_name('ProductCard')
        if len(clickMoreElems) > 0:
            clickMore = clickMoreElems[0]
            clickMore.click()
            types = driver.find_elements_by_xpath("//a[@class='Color ImageLink-subText text-default-800 Link']")
            types[index].click()
            processType()
            index += 1
            if index >= len(types):
                break
        else:
            processType()


def processSubDepartments():
    subDepartments = driver.find_elements_by_xpath("//a[@class='kds-Link kds-Link--l kds-Link--implied SiteMenu-Link py-12 block bg-default-50 pl-48']")
    for subDepartment in subDepartments:
        subDepartment.click()
        processSubDepartment()
        break

url = 'https://www.ralphs.com'
options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
chrome_driver_binary = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(chrome_driver_binary, options=options)
driver.implicitly_wait(5)
driver.get(url)
button = driver.find_elements_by_xpath("//a[@class='kds-Button kds-Button--primary DynamicTooltip--Button--Confirm float-right']")
print(len(button))
# for url in urls:
#     processSubDepartment(url)
