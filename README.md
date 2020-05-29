# Оффлайн библиотека

Этот проект позволяет создать и пользоваться оффлайн библиотекой. Демонстрационная версия доступна по адресу: [https://danceandfight.github.io/offline-library/index1.html](https://danceandfight.github.io/offline-library/index1.html)

Проект состоит из двух модулей: парсер книг с сайта tululu.org и генератора страниц оффлайн бибилиотеки.

Парсер книг `parse_books.py` позволяет скачивать книги в формате `.txt` и их обложки с сайта [tululu.org](tululu.org) и параллельно создает базу данных скаченных книг в формате `.json`. Файлы книг и обложек скачиваются в отдельные папки.
База данных хранит следующие параметры:
```
{
    'title': 'Название книги',
    'author': 'Имя автора',
    'img_src': 'Путь и название к файлу обложки книги',
    'book_path': 'Путь и название к файлу книги',
    'comments': 'Комментарии о книге от пользователей сайта tululu',
    'genres': 'Жанры к которым относится книга' 
}
```

Из скачанных книг сайт-библиотека создается с помощью `render_website.py`.

### Как установить

Для запуска программы у вас должен быть установлен Python 3.
- Скачайте репозиторий
- Установите зависимости командой `pip install -r requirements.txt`


### Как использовать

Для того, что бы запустить оффлайн библиотеку после скачивания репозитория:

1. Перейдите в папку `pages` и откройте в своем браузере файл `index1.html`.

2. Используйте номера страниц вверху страницы для перемещения между разными страницами.

3. После нажатия `читать далее` текст книги откроется в новой вкладке.

Если вы хотите скачать новые книги:

1. Вам потребуется parse_books.py. При запуске `parse_books.py` необходимо передать два аргумента в командной строке `--start_page` и `--end_page` - интервал страниц из раздела ["Научная фантастика"](http://tululu.org/l55), которые нужно скачать. На каждой странице сайта содержится 25 книг.

Для того, что бы скачать книги введите команду `python3 parse_books.py --start_page X --end_page Y`. Вместо `X` и `Y` подставьте желаемые номера страниц.

2. Для создания страниц сайта библиотеки используйте команду `python3 render_website.py`.

3. Новые страницы сайта появятся в папке `pages`. При создании новые страницы замещают существующие и удаляют лишние, если новых страниц меньше старых. 

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).