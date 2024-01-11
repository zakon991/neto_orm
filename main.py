import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Book, Publisher, Shop, Stock, Sale

dmn = {
    'base_type': 'postgresql',
    'user': 'postgres',
    'password': 'Kirill123!',
    'host': 'localhost',
    'port': 5432,
    'database': 'neto_orm'
}

engine = sqlalchemy.create_engine(
    f'{dmn['base_type']}://{dmn['user']}:{dmn['password']}@{dmn['host']}:{dmn['port']}/{dmn['database']}')

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publisher_name = input("Введите имя издателя: ")

results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
    .join(Stock, Stock.id_book == Book.id) \
    .join(Shop, Stock.id_shop == Shop.id) \
    .join(Sale, Sale.id_stock == Stock.id) \
    .join(Publisher, Book.id_publisher == Publisher.id) \
    .filter(Publisher.name == publisher_name) \
    .all()

for result in results:
    print(f'{result.title} | {result.name} | {result.price} | {result.date_sale}')

session.close()
