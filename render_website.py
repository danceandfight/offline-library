import json
import os
import math
import urllib.parse
import glob

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked

def normalize_book_paths(books):
    books_with_normalized_paths = []
    for book in books:
        normalized_path = urllib.parse.quote(book['book_path'])
        book['book_path'] = normalized_path
        books_with_normalized_paths.append(book)
    return books_with_normalized_paths

def update_paths_in_books_db(books):
    updated_books = []
    for book in books:
        book_path = book['book_path']
        fixed_book_path = f'../{book_path}'
        book['book_path'] = fixed_book_path
        img_src = book['img_src']
        fixed_img_src = f'../{img_src}'
        book['img_src'] = fixed_img_src
        updated_books.append(book)
    return updated_books
        
def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    with open('book_db.json') as file:
        books = json.load(file)
    books = normalize_book_paths(books)
    books = update_paths_in_books_db(books)
    paired_books = list(chunked(books, 2))
    book_rows_per_page = 10
    chunks = [paired_books[x:x+10] for x in range(0, len(paired_books), book_rows_per_page)]
    total_pages = math.ceil(len(paired_books)/book_rows_per_page)
    total_pages = range(1, total_pages+1)
    existed_files = set(glob.glob('pages/*.html'))
    created_files = set()
    for number, chunk in enumerate(chunks, 1):
        rendered_page = template.render(
            books=chunk,
            total_pages=total_pages,
            current_page=int(number)
        )
        filename = f'index{number}.html'
        created_files.add(f'pages/{filename}')
        full_path = os.path.join(os.getcwd(), 'pages', filename)
        with open(full_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)
    outdated_files = existed_files.difference(created_files)
    for file in outdated_files:
        os.remove(file)


def main():

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

if __name__ == '__main__':
    main()