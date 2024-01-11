import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    book = relationship("Book", backref="publisher")

    def __str__(self):
        return self.name


class Book(Base):
    __tablename__ = "book"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("publisher.id"))

    stock = relationship("Stock", backref="book")

    def __str__(self):
        return self.title


class Shop(Base):
    __tablename__ = "shop"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    stock = relationship("Stock", backref="shop")

    def __str__(self):
        return self.name


class Stock(Base):
    __tablename__ = "stock"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("book.id"))
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shop.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer)

    sale = relationship("Sale", backref="stock")

    def __str__(self):
        return self.count


class Sale(Base):
    __tablename__ = "sale"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Float)
    date_sale = sqlalchemy.Column(sqlalchemy.Date)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stock.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer)

    def __str__(self):
        return f'{self.price}, {self.date_sale}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
