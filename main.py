import json

import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from conn import *
from model import *

DSN = f'postgresql://{USER}:{PASSWORD}@localhost:5432/{DATABASE}'

engine = sqlalchemy.create_engine(DSN)  # подключение к базе данных

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

models_mapping = {
    'publisher': Publisher
    , 'book': Book
    , 'stock': Stock
    , 'sale': Sale
    , 'shop': Shop
}

with open('tests_data.json', 'r') as file:
    data = json.load(file)
    for instance in data:
        class_model = instance.get('model')
        fields = instance.get('fields')
        obj = models_mapping[class_model](**fields)
        session.add(obj)
        session.commit()


def get_info():
    publisher = input()
    q = (session.query(Publisher.name, Book.title, Shop.name, Sale.date_sale, Sale.count * Sale.price) \
         .filter(Publisher.name == publisher) \
         .join(Book) \
         .join(Stock) \
         .join(Sale) \
         .join(Shop))
    print(pd.DataFrame(q.all(),columns=['Издатель', 'Название книги', 'Магазин', 'Дата продажи', 'Сумма продажи']))

get_info()
