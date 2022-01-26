import datetime
import pandas
import argparse

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

args_parser = argparse.ArgumentParser(description='Программа импортирует данные из Excel-файла на сайт')
args_parser.add_argument('filename',
                         nargs='?',
                         help='Имя файла с расширением .xls/.xlsx. Значение по-умолчанию: wine3.xlsx',
                         default='wine3.xlsx')
args_parser.add_argument('sheet',
                         nargs='?',
                         help='Наименование листа Excel. Значение по-умолчанию: Лист1',
                         default='Лист1')
args = args_parser.parse_args()

foundation_year = 1920
current_year = datetime.datetime.now().year
company_age = current_year - foundation_year

wines = pandas\
    .read_excel(args.filename, sheet_name=args.sheet, keep_default_na=False)\
    .to_dict(orient='record')

grouped_wines = defaultdict(list)
for wine in wines:
    grouped_wines[wine['Категория']].append(wine)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')

rendered_page = template.render(
    company_age=company_age,
    grouped_wines=grouped_wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
