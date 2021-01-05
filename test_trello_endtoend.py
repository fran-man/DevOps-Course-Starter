import os
from threading import Thread

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv

import app
from trello_utils import TRELLO_URL_BASE, DEFAULT_PARAMS

def create_board():
    params = {'name': 'integration_test'}
    params.update(DEFAULT_PARAMS)
    print(DEFAULT_PARAMS)
    print(TRELLO_URL_BASE)
    response = requests.post(TRELLO_URL_BASE + 'boards/', data=params).json()
    board_id = response['id']
    return board_id


def delete_board(board_id):
    requests.delete(TRELLO_URL_BASE + 'boards/' + board_id, data=DEFAULT_PARAMS).json()


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


@pytest.fixture(scope='module')
def test_app():
    load_dotenv()

    # Create the new board & update the board id environment variable
    board_id = create_board()
    os.environ['TRELLO_BOARD'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    delete_board(board_id)


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