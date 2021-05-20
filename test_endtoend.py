from threading import Thread

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import app

@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    with webdriver.Chrome('/chromedriver/chromedriver', options=opts) as driver:
        yield driver


@pytest.fixture(scope='module')
def test_app():
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)


def test_basic_endtoend_flow(driver, test_app):
    driver.get('http://localhost:5000')
    assert driver.title == 'To-Do App'


def test_basic_create_card(driver, test_app):
    driver.get('http://localhost:5000')
    input = driver.find_element_by_id('new_card_textbox')
    input.send_keys('test_card')
    input.send_keys(Keys.ENTER)

    driver.implicitly_wait(20)
    driver.find_elements_by_xpath("//li[contains(text(), 'test_card')]")