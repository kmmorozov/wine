from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from collections import defaultdict
import argparse

def get_cli_argumets():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    file_path = parser.parse_args().file_path
    return file_path

def get_correct_year_name(winery_age):
    last_two_digit = winery_age % 100
    last_digit = winery_age % 10
    if last_two_digit == 1 and last_two_digit != 11:
        return 'год'
    elif last_digit in [2, 3, 4] and last_two_digit not in [12, 13, 14]:
        return 'года'
    else:
        return 'лет'


def get_winery_age(year_of_create):
    now = datetime.datetime.now()
    year_now =  now.year
    winery_age = year_now - year_of_create
    return winery_age


def get_wine_catalog(wine_data_file_name):
    wines = pandas.read_excel(
        wine_data_file_name,
        keep_default_na=False
    )
    wines =  wines.to_dict(orient='records')
    wine_catalog = defaultdict(list)
    for wine in wines:
        wine_catalog[wine['Категория']].append(wine)
    return wine_catalog


if __name__ == '__main__':
    wine_data_file_name = get_cli_argumets()
    year_of_create = 1920
    winery_age = get_winery_age(year_of_create)
    correct_year_name = get_correct_year_name(winery_age)
    wines_catalog = get_wine_catalog(wine_data_file_name)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        wines_catalog = wines_catalog,
        winery_age=winery_age,
        correct_year_name=correct_year_name,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()