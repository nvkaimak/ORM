from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base, relationship, mapped_column

Base = declarative_base()


class GenID(Base):
    __abstract__ = True
    # __abstract__ = True в GenID говорит SQLAlchemy, что этот класс не должен быть
    # связан с какой-либо конкретной таблицей в базе данных сам по себе.
    # Вместо этого он предоставляет общие поля и поведение (например, столбец id),
    # которые наследуются другими моделями.
    id: Mapped[int] = mapped_column(primary_key=True)


class Publisher(GenID):
    __tablename__ = "publisher"

    name: Mapped[str] = mapped_column(String(100), unique=True)

    # def __repr__(self):
    #     return "<{}:{}>".format(self.id, self.name)


class Shop(GenID):
    __tablename__ = "shop"

    name: Mapped[str] = mapped_column(String(100), unique=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.name)


class Book(GenID):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(100))
    id_publisher: Mapped[int] = mapped_column(ForeignKey("publisher.id"))

    publisher = relationship(Publisher, backref="books")

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)


class Stock(GenID):
    __tablename__ = "stock"

    id_book: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    id_shop: Mapped[int] = mapped_column(ForeignKey("shop.id"), nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)

    stock_book = relationship(Book, backref="stock_book")
    stock_shop = relationship(Shop, backref="stock_shop")
    def __repr__(self):
        return "<{}:{}>".format(self.id_book, self.id_shop, self.count)




class Sale(GenID):
    __tablename__ = "sale"

    price: Mapped[float] = mapped_column(nullable=False)
    date_sale: Mapped[datetime] = mapped_column(nullable=False)
    id_stock: Mapped[int] = mapped_column(ForeignKey("stock.id"), nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)

    stock_sale = relationship(Stock, backref="sale")

    def __repr__(self):
        return "<{}:{}>".format(self.price, self.date_sale, self.count)



def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
