import datetime
import pandas

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def isNaN(num):
    return num != num


event1 = datetime.datetime(year=1920,
                           month=12, day=24)
event2 = datetime.datetime.now()
agewine = event2 - event1

event1_year = event1.year
event2_year = event2.year
agewine_year = event2_year - event1_year

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
    agewine_year=agewine_year,
    grouped_wines=grouped_wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
