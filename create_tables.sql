drop TYPE if EXISTS order_status;
CREATE TYPE order_status AS ENUM ('Создано', 'Подтверждено', 'В_процессе', 'Собрано', 'Отправлено', 'Доставлено', 'Отменено', 'Возвращено');

-- drop TABLE if EXISTS Client;
CREATE TABLE Client (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255)
);

-- drop TABLE if EXISTS Category;
CREATE TABLE Category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
-- drop TABLE if EXISTS Supplier;
CREATE TABLE Supplier (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contacts VARCHAR(255) NOT NULL,
    rating DECIMAL(3,2)
);
-- drop TABLE if EXISTS Warehouse;
CREATE TABLE Warehouse (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL
);
-- drop TABLE if EXISTS Product;
CREATE TABLE Product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    warranty INT,
    category_id INT REFERENCES Category(id),
    supplier_id INT REFERENCES Supplier(id)
);
-- drop TABLE if EXISTS Order;
CREATE TABLE "Order" (
    id SERIAL PRIMARY KEY,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status order_status DEFAULT 'Создано',
    client_id INT REFERENCES Client(id)
);
-- drop TABLE if EXISTS OrderItem;
CREATE TABLE OrderItem (
    order_id INT REFERENCES "Order"(id),
    product_id INT REFERENCES Product(id),
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
-- drop TABLE if EXISTS ProductInWarehouse;
CREATE TABLE ProductInWarehouse (
    warehouse_id INT REFERENCES Warehouse(id),
    product_id INT REFERENCES Product(id),
    quantity INT NOT NULL,
    PRIMARY KEY (warehouse_id, product_id)
);

drop TYPE if EXISTS user_role;

CREATE TYPE user_role AS ENUM ('USER', 'ADMIN');

ALTER TABLE Client ADD COLUMN role user_role NOT NULL DEFAULT 'USER';
ALTER TABLE Client ADD COLUMN password VARCHAR(255);
ALTER TABLE "public"."Order"
RENAME TO "orders"