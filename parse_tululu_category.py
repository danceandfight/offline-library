import os
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_page_numbers():
    parser = argparse.ArgumentParser(
        description="Parse page range"
    )
    parser.add_argument('-s', '--start_page', help='Start page number')
    parser.add_argument('-e', '--end_page', help='End page number')
    args = parser.parse_args()
    start_page = int(args.start_page) - 1
    end_page = int(args.end_page) + 1
    return start_page, end_page 

start_page, end_page = parse_page_numbers()

def get_book_collection_urls(url, start, end):
    collection_url_list = []
    for page in range(start, end):
        page_url = '{}{}'.format(url, page)
        response = requests.get(page_url, allow_redirects=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        book_cards = soup.select('#content table td > a:first-child')
        for card in book_cards:
            url_path = card.get('href')
            collection_url_list.append(url_path)
    return collection_url_list

if __name__ == '__main__':
    collection_url = 'http://tululu.org/l55/'
    books = get_book_collection_urls(collection_url, start_page, end_page)
    print(books)