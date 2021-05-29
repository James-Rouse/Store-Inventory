from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import csv
import os


try:
    os.remove("inventory.db")
    # ^^^Source for above line:
    # https://www.w3schools.com/python/python_file_remove.asp
except PermissionError:
    print(f"{'-'*107}\nPlease close any program accessing inventory.db so that \
it can be deleted and remade when this script runs.\n{'-'*107}")
except FileNotFoundError:
    pass

engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    """Model that SQLAlchemy ORM will use to build DB."""

    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_price = Column(Integer)
    product_quantity = Column(Integer)
    date_updated = Column(Date)

    def __repr__(self):
        """Return printable representation of Product."""
        return f"""\n----------
                \rProduct ID: {self.product_id}
                \r----------
                \rName: {self.product_name}
                \r----------
                \rQuantity: {self.product_quantity}
                \r----------
                \rPrice: {self.product_price}
                \r----------
                \rDate Updated: {self.date_updated}
                \r----------\n"""


def add_csv_to_db():
    """Add CSV contents into DB."""
    with open("inventory.csv") as csvfile:
        inventory_reader = csv.reader(csvfile)
        next(inventory_reader, None)
        # ^^^Source for above line:
        # https://stackoverflow.com
        # /questions/14257373/skip-the-headers-when-editing-a-csv-file-using-python
        for item in inventory_reader:
            name = item[0]
            price = clean_price(item[1])
            quantity = item[2]
            date = clean_date(item[3])
            product = Product(product_name=name, product_price=price,
                              product_quantity=quantity, date_updated=date)
            session.add(product)
            session.commit()


def clean_date(date_string):
    """Reformat CSV date for entry into DB."""
    split_date = date_string.split("/")
    year = int(split_date[2])
    month = int(split_date[0])
    day = int(split_date[1])
    return datetime.date(year, month, day)


def clean_price(uncleaned_price):
    """Reformat CSV price for entry into DB."""
    split_dollar_sign = uncleaned_price.split("$")
    split_decimal = split_dollar_sign[1].split(".")
    cleaned_price = "".join(split_decimal)
    # ^^^Source for above 2 lines:
    # https://www.kite.com/python/answers/how-to-join-a-list-of-integers-into-a-string-in-python
    return cleaned_price


def menu():
    """Add menu with options to display product ID,\
    add new product to DB, and backup DB to CSV."""
    while True:
        print(f"""\n{'-'*15}\nStore Inventory\n{'-'*15}\n
            \r>Press [V] to view a specific inventory product's information.\n
            \r>Press [A] to add a new product to the inventory.\n
            \r>Press [B] to generate a CSV backup of the store inventory.\n
            \r>Press [Q] to quit program.\n""")
        while True:
            answer = input("Enter an option: ")
            answer = answer.upper()
            if answer == "V":
                display_product_id(answer)
            elif answer == "A":
                pass
            elif answer == "B":
                pass
            elif answer == "Q":
                print("\nExiting program...\n")
                exit()
            else:
                print("\nPlease input one of the given options.\n")
                continue
            break


def display_product_id(answer):
    """Display a product's info via its product ID."""
    while True:
        id_number = input("\nEnter product ID number: ")
        product = session.query(Product).get(id_number)
        # ^^^Source for above line:
        # https://stackoverflow.com/questions/6750017/how-to-query-database-by-id-using-sqlalchemy
        if product is None:
            print("\nPlease enter an existing product ID.")
            continue
        else:
            print(product)
            input("Enter any key to return to main menu: ")
            break


def add_product_to_db():
    """Add new product to DB."""
    pass


def backup_db_to_csv():
    """Backup BD as CSV."""
    pass


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    add_csv_to_db()
    menu()
