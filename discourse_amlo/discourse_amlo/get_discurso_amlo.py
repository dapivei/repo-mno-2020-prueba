import pandas as pd
import operator

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from functools import reduce


def load_driver():
    """load_driver _summary_

    _extended_summary_

    :return: _description_
    :rtype: _type_
    """
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=options
    )

    return driver


def find_last_page(driver):
    last_page = driver.find_element(By.CLASS_NAME, "page-numbers")
    last_page = last_page.find_elements(By.CSS_SELECTOR, 'li')[-2]
    last_page = last_page.text
    return int(last_page)


def pattern_url(page):

    url = f"https://lopezobrador.org.mx/transcripciones/page/{page}"

    return url


def create_urls(pages):

    pages = range(1, pages+1)
    urls = list(map(pattern_url, pages))

    return urls


def get_links(driver, page):

    driver.get(page)

    articles = driver.find_elements(By.CLASS_NAME, "entry-title")
    articles = [article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for article in articles]

    return articles


def get_discourse_links(driver):

    driver.get('https://lopezobrador.org.mx/transcripciones')
    pages = find_last_page(driver)
    pages = create_urls(pages)
    links = [get_links(driver, page) for page in pages]
    links = reduce(operator.concat, links)
    return links


def get_item(driver, name):

    item = driver.find_element(By.CLASS_NAME, name)
    item = item.text

    return item


def get_each_manianera(link, driver):
    driver.get(link)
    date = get_item(driver, 'entry-date')
    content = get_item(driver, 'entry-content')
    title = get_item(driver, 'entry-title')

    return date, content, title


def get_discourse():
    driver = load_driver()
    links = get_discourse_links(driver)ƒƒ
    dates, contents, titles = [], [], []
    for link in links:
        date, content, title = get_each_manianera(link, driver)
        dates.append(date), contents.append(content), titles.append(title)
    lists = [dates, titles, contents, links]
    manianeras = pd.concat([pd.Series(x) for x in lists], axis=1)
    manianeras.columns = ['date', 'title', 'content', 'links']

    return manianeras
