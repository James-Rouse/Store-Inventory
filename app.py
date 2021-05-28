from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import csv
import os


try:
    os.remove("inventory.db")
    # ^^^Line 37 source: https://www.w3schools.com/python/python_file_remove.asp
except PermissionError:
    print(f"{'-'*107}\nPlease close any program accessing inventory.db so that \
it can be deleted and remade when this script runs.\n{'-'*107}")
except FileNotFoundError:
    pass

engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


def add_csv_to_db():
    """Add CSV contents into DB."""
    with open("inventory.csv") as csvfile:
        inventory_reader = csv.reader(csvfile)
        next(inventory_reader, None)
        # ^^^Line 76 source:
        # https://stackoverflow.com
        # /questions/14257373/skip-the-headers-when-editing-a-csv-file-using-python
        for item in inventory_reader:
            name = item[0]
            price = clean_price(item[1])
            quantity = item[2]
            date = clean_date(item[3])
            product_one = Product(product_name=name, product_price=price,
                                  product_quantity=quantity, date_updated=date)
            session.add(product_one)
            session.commit()


def clean_date(date_string):
    """Format date from csv appropriately for database entry."""
    split_date = date_string.split("/")
    year = int(split_date[2])
    month = int(split_date[0])
    day = int(split_date[1])
    return datetime.date(year, month, day)


def clean_price(uncleaned_price):
    """Format price from csv appropriately for database entry."""
    split_price = uncleaned_price.split("$")
    return split_price[1]


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

    add_csv_to_db()
