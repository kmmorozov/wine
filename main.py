from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

def get_correct_year_name(winery_age):
    last_two_digit = winery_age % 100
    last_digit = winery_age % 10
    if last_two_digit == 1 and last_two_digit != 11:
        return 'год'
    elif last_digit in [2, 3, 4] and last_two_digit not in [12, 13, 14]:
        return 'года'
    else:
        return 'лет'

def get_winery_age():
    now = datetime.datetime.now()
    year_now =  now.year
    date_of_create = datetime.datetime(year=1920, month=1, day=1, hour=0)
    year_of_create = date_of_create.year
    winery_age = year_now - year_of_create
    return winery_age


if __name__=='__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['j2'])
    )
    template = env.get_template('index.j2')
    rendered_page = template.render(
        winery_age = get_winery_age(),
        correct_year_name = get_correct_year_name(get_winery_age())
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
