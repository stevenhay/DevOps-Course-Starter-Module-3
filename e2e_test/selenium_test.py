from threading import Thread
from dotenv import find_dotenv, load_dotenv
from todo_app import app
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pytest
import os
import requests

@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    board = create_board('test board')
    os.environ['TRELLO_BOARD_ID'] = board['id']

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    delete_board(board['id'])

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(executable_path="./chromedriver", options=options) as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    driver.implicitly_wait(5)
    try:
        driver.find_element_by_css_selector('#name-input').send_keys('my new item') 
        driver.find_element_by_css_selector('#add-item').click()

        element = driver.find_element_by_css_selector('div.to-do-items h5.mb-1')
        assert element.text == 'my new item'

        driver.find_element_by_link_text('Start').click()
        element = driver.find_element_by_css_selector('div.doing-items h5.mb-1')
        assert element.text == 'my new item'

        driver.find_element_by_link_text('Complete').click()
        element = driver.find_element_by_css_selector('div.done-items h5.mb-1')
        assert element.text == 'my new item'

        driver.find_element_by_link_text('Mark as Incomplete').click()
        element = driver.find_element_by_css_selector('div.to-do-items h5.mb-1')
        assert element.text == 'my new item'
    except NoSuchElementException:
        pytest.fail('NoSuchElement')

def get_auth_params():
    return { 'key': os.environ.get('TRELLO_API_KEY'), 'token': os.environ.get('TRELLO_API_SECRET') }

def build_url(endpoint):
    return 'https://api.trello.com/1' + endpoint

def build_params(params = {}):
    full_params = get_auth_params()
    full_params.update(params)
    return full_params
    
def create_board(name):
    params = build_params({'name': name})
    url = build_url('/boards')

    response = requests.post(url, params = params)
    board = response.json()

    return board

def delete_board(id):
    params = build_params()
    url = build_url('/boards/%s' % id)

    response = requests.delete(url, params = params)
    board = response.json()

    return board