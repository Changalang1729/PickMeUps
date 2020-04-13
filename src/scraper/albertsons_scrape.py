from selenium import webdriver
from selenium.webdriver.common.keys import Keys

try:
    url = 'https://www.albertsons.com/'
    url = 'https://local.albertsons.com/ca/irvine/3931-irvine-blvd.html'
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    chrome_driver_binary = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(chrome_driver_binary, options=options)
    driver.implicitly_wait(30)
    driver.get(url)

    shop_link = driver.find_element_by_xpath("//a[@href='https://www.albertsons.com/shop/home.html']")
    shop_link.click()

    link = driver.find_element_by_xpath("//button[@onclick='AB.DATALAYER.pushEvent({ name: 'modalClick', modalLink: 'fulfillment-onboarding|close'}); AB.DATALAYER.updateSatelliteTrack('modalclick');']")
    link.click()
    # while link.get_attribute('onclick') == None:
    #     link = driver.find_element_by_id('onboardingCloseButton')
    #     print(link)
    # link.click()

    # driver.implicitly_wait(1000)
    # get_started = driver.find_element_by_id('getStartedButton')
    # print(get_started.get_attribute("onclick"))
    # get_started.click()
    # driver.implicitly_wait(1000)
    # onboarding_close = driver.find_element_by_id('onboardingCloseButton')
    # onboarding_close.click()
    # change_button = driver.find_element_by_id('openFulfillmentModalButton')
    # change_button.click()
    # input_box = driver.find_element_by_id('input-search fulfillment-content__search-wrapper__input ng-pristine ng-valid ng-touched')
    # print(len(input_box))
    # for shop in shops:
    #     shop_link = shop.find_elements_by_tag_name('a')[0]
    #     shop_link.click()
    #     processShop()
    #     break
except:
    pass
    # driver.close()
