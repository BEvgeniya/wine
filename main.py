import datetime
import pandas

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def isNaN(num):
    return num != num


foundation_year = 1920
current_year = datetime.datetime.now().year
company_age = foundation_year - current_year

excel_data_df = pandas.read_excel('wine3.xlsx', sheet_name='Лист1')
wines = excel_data_df.to_dict(orient='record')

grouped_wines = defaultdict(list)
for wine in wines:
    for category in wine:
        if isNaN(wine[category]):
            wine[category] = ''
    grouped_wines[wine['Категория']].append(wine)

sorted_items = sorted(grouped_wines.items(), key=lambda x: x[0])
grouped_wines = dict(sorted_items)

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
