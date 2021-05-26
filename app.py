from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    """Model called Product that the SQLAlchemy ORM will use to build the database."""

    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)

    def __repr__(self):
        return f"<Product(product_name={self.product_name}, product_quantity={self.product_quantity}, product_price={self.product_price}, date_updated={self.date_updated})>"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    