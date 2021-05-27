from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import csv


def clean_date(date_string):
    split_date = date_string.split("/")
    year = int(split_date[2])
    month = int(split_date[0])
    day = int(split_date[1])
    cleaned_date = datetime.date(year, month, day)
    return cleaned_date


def add_csv():
    with open("inventory.csv") as csvfile:
        inventory_reader = csv.reader(csvfile)
        next(inventory_reader, None)
        # Source for above line:
        # https://stackoverflow.com
        # /questions/14257373/skip-the-headers-when-editing-a-csv-file-using-python
        for item in inventory_reader:
            name = item[0]
            price = item[1]
            quantity = item[2]
            date = clean_date(item[3])

engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    """Model called Product that the SQLAlchemy ORM will use to build the database."""

    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_price = Column(Integer)
    product_quantity = Column(Integer)
    date_updated = Column(Date)

    def __repr__(self):
        return f"<Product(product_name={self.product_name},\
                product_quantity={self.product_quantity},\
                product_price={self.product_price},\
                date_updated={self.date_updated})>"


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    add_csv()
