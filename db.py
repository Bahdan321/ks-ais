import os
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
import bcrypt
from models.models import Category, Client, UserRoleEnum, Product

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
        """Метод для проверки учетных данных пользователя."""
        if not self.Session:
            print("Ошибка: Сессия базы данных не инициализирована.")
            return None

        session = self.Session()
        try:
            user = session.query(Client).filter_by(email=email).first()
            if user and bcrypt.checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                print(f"Пользователь {email} успешно аутентифицирован.")
                return (
                    user,
                    user.role,
                )  # Возвращаем объект пользователя и его роль при успехе
            else:
                print(f"Ошибка аутентификации для пользователя {email}.")
                return None, None
        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return None, None
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
                categories_list.append({
                    # "id": category.id,
                    "name":category.name,
                    # "description": category.description
                })
            
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
            query = session.query(Product).join(Category).filter(Category.name == category_name)
            
            products_list = []
            for product in query:
                products_list.append({
                    "id": product.id,
                    "name": product.name,
                    "price": f"${float(product.price)}",
                    "quantity": product.quantity,
                    "category": product.category.name if product.category else "Без категории",
                    "warranty": product.warranty
                })
                
            print(f"Получено {len(products_list)} товаров категории '{category_name}'")
            return products_list
        except Exception as e:
            print(f"Ошибка при получении товаров категории '{category_name}': {e}")
            return []
        finally:
            session.close()


db_manager = DatabaseManager()
# db_manager.create_tables()
# db_manager.add_data()
