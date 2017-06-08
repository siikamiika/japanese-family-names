#!/usr/bin/env python3
import os
import sys
import csv
import time
from urllib.parse import quote_plus
from urllib import robotparser
import requests
from bs4 import BeautifulSoup as BS
from bs4 import Comment

RATE = 5
OUTPUT_DIR = 'name_info'
DOMAIN = 'kanji.reader.bz'
BASE_URL = 'http://{}/?kanji='.format(DOMAIN)
BLACKLIST = {
    'element': [
        'script',
        'noscript',
        'style',
        'link',
        'iframe',
        'img',
    ],
    'class': [
        'bookmark',
    ],
    'id': [
        'footer',
    ],
}

def process_page(data):
    page = BS(data, 'html5lib')

    for element in page.find_all(text=lambda text: isinstance(text, Comment)):
        element.extract()

    for element_name in BLACKLIST['element']:
        for element in page.find_all(element_name):
            element.extract()

    for bad_class in BLACKLIST['class']:
        for element in page.find_all(None, {'class': bad_class}):
            element.extract()

    for bad_id in BLACKLIST['id']:
        for element in page.find_all(None, {'id': bad_id}):
            element.extract()

    return str(page)

def download_info(family_name):
    filename = os.path.join(OUTPUT_DIR, '{}.html'.format(family_name))
    if os.path.isfile(filename):
        return
    time.sleep(RATE)
    page = requests.get(BASE_URL + quote_plus(family_name))
    page = process_page(page.text)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page)
    print(filename)

def get_names(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        return [tuple(row) for row in reader]

def scrape_allowed(domain):
    robots_url = 'http://{}/robots.txt'.format(domain)
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch('*', 'http://{}/'.format(domain))

def main():
    if not scrape_allowed(DOMAIN):
        print('scraping not allowed by robots.txt, exiting')
        sys.exit(1)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    names = get_names(sys.argv[1])
    for name in names:
        download_info(name[0])

if __name__ == '__main__':
    main()
