import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    ForeignKey,
    DateTime,
    Enum,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class OrderStatusEnum(enum.Enum):
    Создано = "Создано"
    Подтверждено = "Подтверждено"
    В_процессе = "В процессе"
    Собрано = "Собрано"
    Отправлено = "Отправлено"
    Доставлено = "Доставлено"
    Отменено = "Отменено"
    Возвращено = "Возвращено"


class UserRoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    address = Column(String(255))
    role = Column(Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.USER)
    password = Column(String(255))

    orders = relationship("Order", back_populates="client")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    products = relationship("Product", back_populates="category")


class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contacts = Column(String(255), nullable=False)
    rating = Column(Numeric(3, 2))

    products = relationship("Product", back_populates="supplier")


class Warehouse(Base):
    __tablename__ = "warehouse"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)

    products_in_warehouse = relationship(
        "ProductInWarehouse", back_populates="warehouse"
    )


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    warranty = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.id"))
    supplier_id = Column(Integer, ForeignKey("supplier.id"))

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    warehouses = relationship("ProductInWarehouse", back_populates="product")


class Order(Base):
    __tablename__ = (
        "orders"  # Имя таблицы в кавычках, т.к. Order - зарезервированное слово в SQL
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, default=func.current_timestamp())
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.Создано)
    client_id = Column(Integer, ForeignKey("client.id"))

    client = relationship("Client", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "orderitem"

    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


class ProductInWarehouse(Base):
    __tablename__ = "productinwarehouse"

    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    warehouse = relationship("Warehouse", back_populates="products_in_warehouse")
    product = relationship("Product", back_populates="warehouses")
