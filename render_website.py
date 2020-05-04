import json
import math
import urllib.parse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked

def fix_book_paths(books):
    books_with_normalized_paths = []
    for book in books:
        normalized_path = urllib.parse.quote(book['book_path'])
        book['book_path'] = normalized_path
        books_with_normalized_paths.append(book)
    return books_with_normalized_paths
        
def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    with open('book_db.json') as file:
        books = json.load(file)
    books = fix_book_paths(books)
    paired_books = list(chunked(books, 2))
    book_rows_per_page = 10
    chunks = [paired_books[x:x+10] for x in range(0, len(paired_books), book_rows_per_page)]
    total_pages = math.ceil(len(paired_books)/book_rows_per_page)
    total_pages = range(1, total_pages+1)
    for number, chunk in enumerate(chunks, 1):
        rendered_page = template.render(
            books=chunk,
            total_pages=total_pages,
            current_page=int(number)
        )
        filename = f'index{number}.html'
        with open(filename, 'w', encoding="utf8") as file:
            file.write(rendered_page)

def main():

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

if __name__ == '__main__':
    main()