import time
import pytest
import uuid
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.color import Color

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    # wd = webdriver.Firefox()
    # wd = webdriver.Ie()
    # wd = webdriver.Edge()
    # wd = webdriver.Firefox(capabilities={"marionette": False})
    # wd = webdriver.Firefox(firefox_binary="c:\\Program Files\\Firefox Nightly\\firefox.exe")
    # wd = webdriver.Firefox(firefox_binary="c:\\Program Files\\Mozilla Firefox\\firefox.exe")
    # print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def is_element_present(driver, *args):
    try:
        driver.find_element(*args)
        return True
    except NoSuchElementException:
        return False

def test_example(driver):
    # driver.get("http://localhost/litecart/admin/")
    for i in range(3):
        driver.get("http://localhost/litecart/")
        #driver.delete_all_cookies()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#box-campaigns')))

        time.sleep(2)

        driver.find_element_by_css_selector('#box-most-popular a').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, \
                                                                    '#box-product button[name="add_cart_product"]')))
        if is_element_present(driver, By.CSS_SELECTOR, '#box-product select[name="options[Size]"]'):
            driver.find_element_by_css_selector('#box-product select option[value="Small"]').click()
        box = driver.find_element_by_css_selector('#cart span.quantity').text
        driver.find_element_by_css_selector('#box-product button[name="add_cart_product"]').click()

        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart span.quantity'), \
                                                                     str(int(box)+1)))
    driver.find_element_by_css_selector('#cart a').click()
    time.sleep(2)

    for i in range(3):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, \
                                                                 '#box-checkout-cart button[name="remove_cart_item')))
        driver.find_element_by_css_selector('#box-checkout-cart button[name="remove_cart_item"]').click()
        driver.refresh()
        if not is_element_present(driver, By.CSS_SELECTOR, '#box-checkout-cart button[name="remove_cart_item]'):
            break
    time.sleep(3)