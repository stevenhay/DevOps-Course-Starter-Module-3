from threading import Thread
from todo_app.data.mongo_items import MongoDB
from dotenv import find_dotenv, load_dotenv
from todo_app import app
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pytest
import os

@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    db = MongoDB()
    os.environ['MONGO_DATABASE'] = 'E2E'

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    db.client.drop_database(os.getenv('MONGO_DATABASE'))

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

