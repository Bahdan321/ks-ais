import datetime
import os
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
import bcrypt
from cart import CartManager, cart_manager
from models.models import (
    Category,
    Client,
    Order,
    OrderItem,
    OrderStatusEnum,
    ProductInWarehouse,
    UserRoleEnum,
    Product,
)

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.connect()

    def connect(self):
        """Метод для подключения к базе данных."""
        try:
            db_name = os.getenv("DB_NAME")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_host = os.getenv("DB_HOST")
            db_port = os.getenv("DB_PORT")

            if not all([db_name, db_user, db_password, db_host, db_port]):
                print(
                    "Ошибка: Не все переменные окружения для подключения к БД установлены."
                )
                return

            db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
            print("Успешное подключение к базе данных.")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def create_tables(self, sql_file_path="/create_tables.sql"):
        """Метод для создания таблиц в базе данных из SQL файла."""
        if not self.engine:
            print("Ошибка: Подключение к базе данных не установлено.")
            return

        try:
            with open(sql_file_path, "r") as f:
                sql_script = f.read()

            with self.engine.connect() as connection:
                with connection.begin():  # Начать транзакцию
                    # Разделяем скрипт на отдельные команды, учитывая точки с запятой
                    # и игнорируя комментарии
                    commands = [
                        cmd.strip()
                        for cmd in sql_script.split(";")
                        if cmd.strip() and not cmd.strip().startswith("--")
                    ]
                    for command in commands:
                        if command:  # Убедимся, что команда не пустая
                            connection.execute(text(command))
            print(f"Таблицы успешно созданы из файла {sql_file_path}.")
        except FileNotFoundError:
            print(f"Ошибка: SQL файл не найден по пути {sql_file_path}")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")

    def add_data(self, sql_file_path="/insert_data.sql"):
        """Метод для добавления данных в базу данных из SQL файла."""
        if not self.engine:
            print("Ошибка: Подключение к базе данных не установлено.")
            return

        try:
            with open(sql_file_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            with self.engine.connect() as connection:
                with connection.begin():  # Начать транзакцию
                    # Разделяем скрипт на отдельные команды, учитывая точки с запятой
                    # и игнорируя комментарии
                    commands = [
                        cmd.strip()
                        for cmd in sql_script.split(";")
                        if cmd.strip() and not cmd.strip().startswith("--")
                    ]
                    for command in commands:
                        if command:  # Убедимся, что команда не пустая
                            connection.execute(text(command))
            print(f"Данные успешно добавлены из файла {sql_file_path}.")
        except FileNotFoundError:
            print(f"Ошибка: SQL файл не найден по пути {sql_file_path}")
        except Exception as e:
            print(f"Ошибка при добавлении данных: {e}")

    def register_user(
        self, full_name, phone, email, address, password, role=UserRoleEnum.USER
    ):
        """Метод для регистрации нового пользователя."""
        if not self.Session:
            print("Ошибка: Сессия базы данных не инициализирована.")
            return False, "Ошибка подключения к базе данных."

        session = self.Session()
        try:
            # Проверка, существует ли пользователь с таким email
            existing_user = session.query(Client).filter_by(email=email).first()
            if existing_user:
                return False, "Пользователь с таким email уже существует."

            # Хеширование пароля
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Создание нового пользователя
            new_user = Client(
                full_name=full_name,
                phone=phone,
                email=email,
                address=address,
                password=hashed_password.decode("utf-8"),  # Сохраняем хеш как строку
                role=role,
            )
            session.add(new_user)
            session.commit()
            print(f"Пользователь {email} успешно зарегистрирован.")
            return True, "Регистрация прошла успешно!"
        except Exception as e:
            session.rollback()
            print(f"Ошибка при регистрации пользователя: {e}")
            return False, f"Ошибка при регистрации: {e}"
        finally:
            session.close()

    def verify_user(self, email, password):
        """
        Проверяет учетные данные пользователя.
        """
        if not self.Session:
            return False, None

        session = self.Session()
        try:
            # Находим пользователя по email
            user = session.query(Client).filter(Client.email == email).first()

            if not user:
                return False, None

            # Проверяем пароль
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                # Возвращаем данные о пользователе
                user_data = {
                    "id": user.id,
                    "name": user.full_name,
                    "role": user.role,
                    "email": user.email,
                }
                print(user_data)
                return True, user_data
            else:
                return False, None
        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return False, None
        finally:
            session.close()

    def get_all_products(self):
        """Метод для получения всех товаров из базы данных с использованием ORM SQLAlchemy."""
        if not self.Session:
            print("Ошибка: Сессия базы данных не инициализирована.")
            return []

        session = self.Session()
        try:
            # Используем joinedload для загрузки связанных категорий за один запрос
            products_query = session.query(Product).options(
                joinedload(Product.category)
            )

            products_list = []
            for product in products_query:
                products_list.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": f"${float(product.price)}",
                        "quantity": product.quantity,
                        "category": (
                            product.category.name
                            if product.category
                            else "Без категории"
                        ),
                        "warranty": product.warranty,
                    }
                )

            print(f"Получено {len(products_list)} товаров из базы данных.")
            return products_list
        except Exception as e:
            print(f"Ошибка при получении товаров: {e}")
            return []
        finally:
            session.close()

    def get_all_categories(self):
        """
        Метод для получения всех категорий товаров из базы данных.
        Возвращает список словарей с информацией о категориях.
        """
        if not self.Session:
            print("Ошибка: Сессия базы данных не инициализирована.")
            return []

        session = self.Session()
        try:
            categories = session.query(Category).all()

            categories_list = []
            for category in categories:
                categories_list.append(
                    {
                        # "id": category.id,
                        "name": category.name,
                        # "description": category.description
                    }
                )

            print(f"Получено {len(categories_list)} категорий из базы данных.")
            return categories_list
        except Exception as e:
            print(f"Ошибка при получении категорий: {e}")
            # Резервные данные в случае ошибки
            return [
                {"id": 1, "name": "Ноутбуки", "description": "Портативные компьютеры"},
                # {"id": 2, "name": "Мониторы", "description": "Устройства отображения"},
                # {"id": 3, "name": "Комплектующие", "description": "Детали для компьютеров"},
                # {"id": 4, "name": "Периферия", "description": "Внешние устройства"},
                # {"id": 5, "name": "Сетевое оборудование", "description": "Устройства для сети"}
            ]
        finally:
            session.close()

    def get_products_by_category(self, category_name):
        """
        Метод для получения товаров определенной категории.
        """
        if not self.Session:
            print("Ошибка: Сессия базы данных не инициализирована.")
            return []

        session = self.Session()
        try:
            # Объединяем таблицы Product и Category для фильтрации по имени категории
            query = (
                session.query(Product)
                .join(Category)
                .filter(Category.name == category_name)
            )

            products_list = []
            for product in query:
                products_list.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": f"${float(product.price)}",
                        "quantity": product.quantity,
                        "category": (
                            product.category.name
                            if product.category
                            else "Без категории"
                        ),
                        "warranty": product.warranty,
                    }
                )

            print(f"Получено {len(products_list)} товаров категории '{category_name}'")
            return products_list
        except Exception as e:
            print(f"Ошибка при получении товаров категории '{category_name}': {e}")
            return []
        finally:
            session.close()

    def get_user_orders(self, client_id):
        """
        Получает все заказы указанного пользователя вместе с информацией о товарах.
        """
        if not self.Session:
            print("Ошибка: Сессия базы данных не инициализирована.")
            return []

        session = self.Session()
        try:
            # Получаем все заказы пользователя
            orders = (
                session.query(Order)
                .filter(Order.client_id == client_id)
                .order_by(Order.order_date.desc())
                .all()
            )

            orders_list = []
            for order in orders:
                # Получаем элементы заказа с информацией о товарах
                order_items = (
                    session.query(OrderItem)
                    .filter(OrderItem.order_id == order.id)
                    .options(joinedload(OrderItem.product))
                    .all()
                )

                # Создаем список товаров в заказе
                items = []
                total_price = 0

                for item in order_items:
                    # Получаем категорию товара
                    category_name = (
                        item.product.category.name
                        if item.product.category
                        else "Без категории"
                    )

                    # Рассчитываем стоимость позиции (цена * количество)
                    item_price = float(item.price) * item.quantity
                    total_price += item_price

                    items.append(
                        {
                            "id": item.product.id,
                            "name": item.product.name,
                            "category": category_name,
                            "quantity": item.quantity,
                            "price": f"${float(item.price)}",
                            "total_price": f"${item_price:.2f}",
                        }
                    )

                # Форматируем дату для отображения
                order_date = (
                    order.order_date.strftime("%d.%m.%Y %H:%M")
                    if order.order_date
                    else "Дата не указана"
                )

                # Собираем информацию о заказе
                orders_list.append(
                    {
                        "id": order.id,
                        "date": order_date,
                        "status": order.status.value,  # Используем значение из enum
                        "items": items,
                        "total_price": f"${total_price:.2f}",
                        "items_count": len(items),
                    }
                )

            print(f"Получено {len(orders_list)} заказов для пользователя {client_id}")
            return orders_list
        except Exception as e:
            print(f"Ошибка при получении заказов пользователя: {e}")
            return []
        finally:
            session.close()

    def create_order_from_cart(self, client_id):
        """
        Создает заказ на основе корзины пользователя.
        """
        if not self.Session:
            return False, "Ошибка подключения к базе данных", None

        session = self.Session()
        try:
            print(2222222, client_id)
            # Получаем корзину пользователя
            cart_items = cart_manager.get_cart(client_id)

            if not cart_items:
                return False, "Корзина пуста", None

            # Проверяем наличие товаров в нужном количестве
            for item in cart_items:
                product = session.query(Product).get(item["product_id"])
                if not product:
                    return False, f"Товар с ID {item['product_id']} не найден", None

                if product.quantity < item["quantity"]:
                    return (
                        False,
                        f"Недостаточное количество товара '{product.name}' на складе",
                        None,
                    )

            # Создаем новый заказ
            new_order = Order(
                client_id=client_id,
                status=OrderStatusEnum.Создано,
                order_date=datetime.datetime.now(),
            )
            session.add(new_order)
            session.flush()  # Получаем ID нового заказа

            # Добавляем товары в заказ
            for item in cart_items:
                product = session.get(Product, item["product_id"])

                # Создаем запись в OrderItem
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=item["quantity"],
                    price=product.price,
                )
                session.add(order_item)

                # Уменьшаем количество товара на складе
                product.quantity -= item["quantity"]

                # Сохраняем изменения
                session.commit()

                # Очищаем корзину пользователя
                cart_manager.clear_cart(client_id)

                return True, f"Заказ №{new_order.id} успешно создан", new_order.id

        except Exception as e:
            session.rollback()
            print(f"Ошибка при создании заказа: {e}")
            return False, f"Ошибка при создании заказа: {e}", None
        finally:
            session.close()

    def get_user_orders(self, client_id):
        """
        Получает список всех заказов пользователя.
        """
        if not self.Session:
            return []

        session = self.Session()
        try:
            # Получаем все заказы пользователя
            orders = (
                session.query(Order)
                .filter(Order.client_id == client_id)
                .order_by(Order.order_date.desc())
                .all()
            )

            result = []
            for order in orders:
                # Для каждого заказа получаем его товары
                order_items = []
                total_price = 0

                for item in order.order_items:
                    product = item.product
                    item_price = float(item.price) * item.quantity
                    total_price += item_price

                    order_items.append(
                        {
                            "product_id": product.id,
                            "name": product.name,
                            "quantity": item.quantity,
                            "price": float(item.price),
                            "total_item_price": item_price,
                        }
                    )

                result.append(
                    {
                        "order_id": order.id,
                        "order_date": order.order_date.strftime("%d.%m.%Y %H:%M"),
                        "status": order.status.value,
                        "items": order_items,
                        "total_price": total_price,
                    }
                )

            return result
        except Exception as e:
            print(f"Ошибка при получении заказов пользователя: {e}")
            return []
        finally:
            session.close()

    def get_cart_products(self, client_id):
        """
        Получает информацию о товарах в корзине пользователя.
        """
        if not self.Session:
            return []

        session = self.Session()
        try:
            cart_items = cart_manager.get_cart(client_id)
            result = []

            for item in cart_items:
                product = (
                    session.query(Product)
                    .options(joinedload(Product.category))
                    .get(item["product_id"])
                )
                if product:
                    result.append(
                        {
                            "id": product.id,
                            "name": product.name,
                            "category": (
                                product.category.name
                                if product.category
                                else "Без категории"
                            ),
                            "quantity": item["quantity"],
                            "price": f"${float(product.price)}",
                            "price_value": float(
                                product.price
                            ),  # Числовое значение для расчетов
                            "warranty": product.warranty,
                            "available_quantity": product.quantity,  # Доступное количество на складе
                        }
                    )

            return result
        except Exception as e:
            print(f"Ошибка при получении товаров корзины: {e}")
            return []
        finally:
            session.close()

    def add_product_to_cart(self, client_id, product_id, quantity=1):
        """
        Добавляет товар в корзину, проверяя его наличие.
        """
        if not self.Session:
            return False, "Ошибка подключения к базе данных"

        session = self.Session()
        try:
            # Проверяем наличие товара в нужном количестве
            product = session.query(Product).get(product_id)

            if not product:
                return False, "Товар не найден"

            if product.quantity < quantity:
                return (
                    False,
                    f"На складе недостаточно товара (в наличии {product.quantity})",
                )

            # Добавляем товар в корзину
            cart_manager.add_to_cart(client_id, product_id, quantity)

            return True, "Товар добавлен в корзину"
        except Exception as e:
            print(f"Ошибка при добавлении товара в корзину: {e}")
            return False, f"Ошибка: {e}"
        finally:
            session.close()
    
    def get_all_clients(self):
        """
        Получает список всех клиентов из базы данных.
        """
        try:
            session = self.Session()
            clients = session.query(Client).all()
            
            # Преобразуем объекты Client в словари с необходимыми данными
            result = []
            for client in clients:
                result.append({
                    "id": client.id,
                    "full_name": client.full_name,
                    "phone": client.phone,
                    "email": client.email,
                    "address": client.address,
                    "role": client.role.value if client.role else None,
                    # Не возвращаем пароль в целях безопасности
                    "orders_count": len(client.orders)  # Количество заказов
                })
            
            return result
        except Exception as e:
            print(f"Ошибка при получении клиентов: {e}")
            return []
        finally:
            session.close()

    def get_all_products(self):
        """
        Получает список всех товаров из базы данных с информацией о категории и поставщике.
        """
        try:
            session = self.Session()
            # Используем joinedload для загрузки связанных объектов одним запросом
            products = session.query(Product).options(
                joinedload(Product.category),
                joinedload(Product.supplier)
            ).all()
            
            # Преобразуем объекты Product в словари
            result = []
            for product in products:
                result.append({
                    "id": product.id,
                    "name": product.name,
                    "price": float(product.price) if product.price else 0,
                    "quantity": product.quantity,
                    "warranty": product.warranty,
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name
                    } if product.category else None,
                    "supplier": {
                        "id": product.supplier.id,
                        "name": product.supplier.name
                    } if product.supplier else None
                })
            
            return result
        except Exception as e:
            print(f"Ошибка при получении товаров: {e}")
            return []
        finally:
            session.close()

    def get_all_orders(self):
        """
        Получает список всех заказов с информацией о клиенте и товарах.
        """
        try:
            session = self.Session()
            # Загружаем связанные объекты
            orders = session.query(Order).options(
                joinedload(Order.client),
                joinedload(Order.order_items).joinedload(OrderItem.product)
            ).all()
            
            # Преобразуем объекты Order в словари
            result = []
            for order in orders:
                # Рассчитываем общую сумму заказа
                total_price = sum(float(item.price) * item.quantity for item in order.order_items)
                
                # Собираем информацию о товарах в заказе
                items = []
                for item in order.order_items:
                    items.append({
                        "product_id": item.product_id,
                        "product_name": item.product.name if item.product else "Неизвестный товар",
                        "quantity": item.quantity,
                        "price": float(item.price) if item.price else 0
                    })
                
                result.append({
                    "id": order.id,
                    "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S") if order.order_date else None,
                    "status": order.status.value if order.status else None,
                    "client": {
                        "id": order.client.id,
                        "full_name": order.client.full_name,
                        "phone": order.client.phone
                    } if order.client else None,
                    "total_price": total_price,
                    "items_count": len(order.order_items),
                    "items": items
                })
            
            return result
        except Exception as e:
            print(f"Ошибка при получении заказов: {e}")
            return []
        finally:
            session.close()
    
    def delete_client(self, client_id):
        """
        Удаляет клиента из базы данных.
        Если у клиента есть заказы, удаление будет отклонено.
        """
        session = self.Session()
        try:
            # Проверяем, существует ли клиент
            client = session.query(Client).filter(Client.id == client_id).first()
            if not client:
                return False, f"Клиент с ID {client_id} не найден"
            
            # Проверяем, есть ли у клиента заказы
            orders_count = session.query(Order).filter(Order.client_id == client_id).count()
            if orders_count > 0:
                return False, f"Невозможно удалить клиента, так как у него есть {orders_count} заказов"
            
            # Удаляем клиента
            session.delete(client)
            session.commit()
            return True, f"Клиент '{client.full_name}' успешно удален"
        
        except Exception as e:
            session.rollback()
            return False, f"Ошибка при удалении клиента: {e}"
        finally:
            session.close()

    def delete_product(self, product_id):
        """
        Удаляет товар из базы данных.
        Если товар есть в заказах, удаление будет отклонено.
        """
        session = self.Session()
        try:
            # Проверяем, существует ли товар
            product = session.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False, f"Товар с ID {product_id} не найден"
            
            # Проверяем, есть ли товар в заказах
            order_items_count = session.query(OrderItem).filter(OrderItem.product_id == product_id).count()
            if order_items_count > 0:
                return False, f"Невозможно удалить товар, так как он присутствует в {order_items_count} заказах"
            
            # Проверяем, есть ли товар на складах
            warehouse_items_count = session.query(ProductInWarehouse).filter(
                ProductInWarehouse.product_id == product_id
            ).count()
            if warehouse_items_count > 0:
                # Удаляем записи о товаре на складах
                session.query(ProductInWarehouse).filter(
                    ProductInWarehouse.product_id == product_id
                ).delete()
            
            # Удаляем товар
            session.delete(product)
            session.commit()
            return True, f"Товар '{product.name}' успешно удален"
        
        except Exception as e:
            session.rollback()
            return False, f"Ошибка при удалении товара: {e}"
        finally:
            session.close()

    def delete_order(self, order_id):
        """
        Удаляет заказ из базы данных вместе со всеми его позициями.
        """
        session = self.Session()
        try:
            # Проверяем, существует ли заказ
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order:
                return False, f"Заказ с ID {order_id} не найден"
            
            # Удаляем все позиции заказа
            session.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
            
            # Запоминаем информацию о заказе для сообщения
            order_info = f"#{order.id} от {order.order_date.strftime('%d.%m.%Y')}"
            
            # Удаляем заказ
            session.delete(order)
            session.commit()
            return True, f"Заказ {order_info} успешно удален"
        
        except Exception as e:
            session.rollback()
            return False, f"Ошибка при удалении заказа: {e}"
        finally:
            session.close()



db_manager = DatabaseManager()
# db_manager.create_tables()
# db_manager.add_data()
