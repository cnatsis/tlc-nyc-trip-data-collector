import asyncio
import contextvars
import functools
import logging
import os
from os.path import isfile, join
import pyarrow.parquet as pq
from time import perf_counter
from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

TLC_URL = 'https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page'
DATA_DIR = 'data'


def construct_url_list() -> set:
    """
    This method is used to scrap all the URLs of TLC Trip Data from the web and store them to a list

    :return: List of unique URLs that contain the parquet data files
    """
    url_list = set()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(TLC_URL)
    link = driver.find_element(By.LINK_TEXT, 'Expand All')
    link.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for u in soup.select('[class="faq-v1"] div'):
        for a in u.find_all('a', href=True):
            href: str = a.get('href')
            if href.startswith('https://'):
                url_list.add(href)
    driver.close()
    driver.quit()
    return url_list


def write_to_file(file_name: str, data: List[str]) -> None:
    """
    Writes data to file

    :param file_name: file name
    :param data: data to write
    """
    with open(file_name, 'w') as f:
        f.write('\n'.join(data))


def clean_faulty_files() -> None:
    """
    Removes all faulty parquet files from the data directory
    """
    files = [f for f in os.listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]
    for f in files:
        try:
            pq.ParquetFile('{}/{}'.format(DATA_DIR, f))
        except Exception as e:
            logging.info("Deleting corrupted file '{}': {}".format(f, e))
            os.remove('{}/{}'.format(DATA_DIR, f))


async def download_file(file_url: str) -> None:
    """
    Download a single file in concurrent mode. Output file is stored in the 'data' directory.

    :param file_url: URL of data file
    """
    logging.info("Downloading file '{}'".format(file_url))
    file_name = file_url.split('/')[-1]

    content = http_get(file_url)
    with open(os.path.join(os.path.dirname(__file__), DATA_DIR, file_name), 'wb') as f:
        f.write(await content)
    logging.info("Finished downloading file '{}'".format(file_url))


async def download_all_files(url_list: List[str]) -> None:
    """
    Method to download all files concurrently

    :param url_list: URLs to download files from
    """
    await asyncio.gather(*[download_file(f) for f in url_list])


def http_get_sync(url: str) -> bytes:
    """
    Synchronous call to get the content of a URL
    :param url: URL address
    :return: URL content
    """
    response = requests.get(url)
    return response.content


async def http_get(url: str):
    return await to_thread(http_get_sync, url)


async def to_thread(func, /, *args, **kwargs):
    """
    Asyncio's to_thread implementation on Python 3.9
    """
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


async def main():
    start = perf_counter()

    # Fetch URLs list from the web using scraper
    s3_urls = list(construct_url_list())

    # Flush URLs to file for future usage
    write_to_file('tlc_nyc_data_url_list.txt', s3_urls)

    # Download all files asynchronously
    await download_all_files(s3_urls)

    # Cleanup faulty parquet files
    clean_faulty_files()

    logging.info('Total time: {}'.format(perf_counter() - start))


def run() -> None:
    asyncio.run(main())


if __name__ == '__main__':
    run()
