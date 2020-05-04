import os
import requests
import json
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse

from parse_tululu_category import get_book_collection_urls, parse_page_numbers


def download_txt(url, filename, folder='books'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    filename = sanitize_filename(filename) + '.txt'
    if not response.status_code == 200:
        return
    abs_path = os.path.abspath('.')
    os.makedirs(os.path.join(abs_path, folder), exist_ok=True)
    file_with_path = os.path.join(folder, filename)
    with open(file_with_path, 'wb') as file:
        file.write(response.content)

def check_image_file_existence(filename, folder='images'):
    abs_path = os.path.abspath('.')
    folder_path = os.path.join(abs_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    if filename in os.listdir(folder_path):
        return True

def download_image(url, filename, folder='images'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    filename = url.split('/')[-1]
    if not response.status_code == 200:
        return
    abs_path = os.path.abspath('.')
    folder_path = os.path.join(abs_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    file_with_path = os.path.join(folder, filename)
    with open(file_with_path, 'wb') as file:
        file.write(response.content)

def get_book_title(soup):
    book = soup.select_one('#content > h1').text
    book_title = book.split('::')[0].strip()
    return book_title.title()

def get_book_author(soup):
    book = soup.select_one('#content > h1').text
    book_author = book.split('::')[1].strip()
    return book_author.title()

def get_book_cover(soup, collection_url):
    book_cover_path = soup.select_one('div.bookimage a img')['src']
    book_cover_url = urljoin(collection_url, book_cover_path)
    return book_cover_url

def get_comments(soup):
    raw_comments = soup.select('.texts > .black')
    comments = [comment.text for comment in raw_comments]
    return comments

def get_book_genre(soup):
    raw_genres = soup.select('span.d_book a')
    genres = [genre.text for genre in raw_genres]
    return genres

def main():
    collection_url = 'http://tululu.org/l55/'
    start_page, end_page = parse_page_numbers()
    print(f"start_page: {start_page}", f"end_page: {end_page}")
    book_page_urls = get_book_collection_urls(collection_url, start_page, end_page)
    books = []
    for url_path in book_page_urls:
        url = urljoin(collection_url, url_path)
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
        if not response.status_code == 200:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        book_title = get_book_title(soup)
        book_author = get_book_author(soup)
        book_id = url_path[2:-1]
        book_filename = sanitize_filename(book_title) + '.txt'
        book_path = os.path.join('books', book_filename)
        book_cover = get_book_cover(soup, collection_url)
        img_name = book_cover.split('/')[-1]
        img_src = os.path.join('images', img_name)
        comments = get_comments(soup)
        genres = get_book_genre(soup)
        book = {
                'title': book_title,
                'author': book_author,
                'img_src': img_src,
                'book_path': book_path,
                'comments': comments,
                'genres': genres
        }
        books.append(book)
        book_download_url = 'http://tululu.org/txt.php?id={}'.format(book_id)
        download_txt(book_download_url, book_title)
        if check_image_file_existence(book_cover):
            continue
        download_image(book_cover, str(book_id))
    with open('book_db.json', 'w') as file:
        json.dump(books, file)

if __name__ == '__main__':
    main()
