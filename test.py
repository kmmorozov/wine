import pandas
from collections import defaultdict

def get_wine_catalog(wine_data_file):
    wines = pandas.read_excel(
        wine_data_file,
        keep_default_na=False
    )
    print(type(wines))
    wines =  wines.to_dict(orient='records')
    print(wines)
    wine_catalog = defaultdict(list)

    for wine in wines_dict:
        wine_catalog[wine['Категория']].append(wine)
    return wine_catalog

if __name__ =='__main__':
    wc = get_wine_catalog('wine2.xlsx')
    print(wc)