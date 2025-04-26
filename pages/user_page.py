import flet as ft
from styles.colors import (
    TEXT, PINK_LIGHT, YELLOW_LIGHT, PINK_MEDIUM, YELLOW_DARK, PINK_DARK,
)
from db import db_manager

def user_view(page: ft.Page):
    """Создает представление страницы пользователя с фильтрацией товаров по категориям."""

    # Установка свойств страницы
    page.padding = 0
    page.bgcolor = YELLOW_LIGHT

    # Функция для проверки мобильного режима
    def is_mobile(page):
        return page.width < 600

    # Заголовок остается без изменений
    def header_layout():
        # ... код как был ранее ...
        is_mob = is_mobile(page)

        # Кнопки в верхнем углу
        personal_account_button = ft.TextButton(
            content=ft.Text(
                "Выйти",
                color=PINK_DARK,
                size=14 if is_mob else 16,
                weight=ft.FontWeight.W_500,
            ),
            style=ft.ButtonStyle(
                bgcolor=YELLOW_LIGHT,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda e: page.go("/login"),
        )

        logout_button = ft.ElevatedButton(
            text="Выйти" if not is_mob else "",
            icon=ft.icons.LOGOUT,
            style=ft.ButtonStyle(
                bgcolor=PINK_MEDIUM,
                color=YELLOW_LIGHT,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda e: page.go("/login"),
        )

        cart_button = ft.TextButton(
            content=ft.Text(
                "Корзина",
                color=PINK_DARK,
                size=14 if is_mob else 16,
                weight=ft.FontWeight.W_500,
            ),
            style=ft.ButtonStyle(
                bgcolor=YELLOW_LIGHT,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda e: page.go("/cart"),
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "HarukoShop",
                        color=PINK_DARK,
                        size=22 if is_mob else 28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    cart_button,
                    logout_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(10 if is_mob else 20),
            bgcolor=YELLOW_LIGHT,
            border=ft.border.only(bottom=ft.BorderSide(1, PINK_LIGHT)),
        )

    # Получение категорий из базы данных
    def get_categories():
        try:
            return db_manager.get_all_categories()
        except Exception as e:
            print(f"Ошибка при получении категорий: {e}")
            # Резервные категории
            return [
                {"id": 1, "name": "Ноутбуки", "description": "Портативные компьютеры"},
                {"id": 2, "name": "Мониторы", "description": "Устройства отображения"},
                {"id": 3, "name": "Комплектующие", "description": "Детали для компьютеров"},
                {"id": 4, "name": "Периферия", "description": "Внешние устройства"},
                {"id": 5, "name": "Сетевое оборудование", "description": "Устройства для сети"}
            ]

    # Получение всех товаров из базы данных
    def get_all_products():
        try:
            return db_manager.get_all_products()
        except Exception as e:
            print(f"Ошибка при получении товаров: {e}")
            # Резервные товары
            return [
                {
                    "name": "Ноутбук Acer",
                    "category": "Ноутбуки",
                    "quantity": 10,
                    "price": "$500",
                },
                {
                    "name": "Монитор Samsung",
                    "category": "Мониторы",
                    "quantity": 5,
                    "price": "$150",
                },
                {
                    "name": "Клавиатура Logitech",
                    "category": "Периферия",
                    "quantity": 20,
                    "price": "$30",
                }
            ]
    
    # Начинаем с загрузки всех товаров и категорий
    categories = get_categories()
    current_products = get_all_products()  # Текущие отображаемые товары
    selected_category = None  # Текущая выбранная категория
    
    # Функция для обновления отображаемых товаров
    def update_products_grid(products_to_display):
        nonlocal current_products, products_grid_view
        current_products = products_to_display
        
        # Создаем новый GridView с отфильтрованными товарами
        new_grid = ft.GridView(
            [create_product_card(product) for product in current_products],
            runs_count=1 if is_mobile(page) else 3,
            max_extent=250,
            spacing=10,
            run_spacing=10,
            padding=10,
            expand=1,
        )
        
        # Обновляем грид в контейнере
        products_grid_view.content = new_grid
        page.update()
    
    # Функция для фильтрации товаров по категории
    def filter_by_category(e, category_name=None):
        page.splash = ft.ProgressBar()  # Показываем индикатор загрузки
        page.update()
        
        try:
            nonlocal selected_category
            selected_category = category_name
            
            # Если выбраны все товары или категория не указана
            if category_name is None or category_name == "Все товары":
                filtered_products = get_all_products()
                highlight_selected_category(None)  # Снимаем выделение со всех категорий
            else:
                # Получаем товары выбранной категории
                filtered_products = db_manager.get_products_by_category(category_name)
                highlight_selected_category(category_name)  # Выделяем выбранную категорию
            
            update_products_grid(filtered_products)
        except Exception as e:
            print(f"Ошибка при фильтрации товаров: {e}")
        finally:
            page.splash = None
            page.update()
    
    # Словарь для хранения ссылок на контейнеры категорий для изменения их стиля
    category_containers = {}
    
    # Функция для выделения выбранной категории
    def highlight_selected_category(selected_name):
        for name, container in category_containers.items():
            if name == selected_name:
                container.bgcolor = PINK_MEDIUM  # Выделяем выбранную категорию
                container.content.color = YELLOW_LIGHT  # Меняем цвет текста
            elif name == "Все товары" and selected_name is None:
                container.bgcolor = PINK_MEDIUM  # Выделяем "Все товары" если ничего не выбрано
                container.content.color = YELLOW_LIGHT
            else:
                container.bgcolor = PINK_LIGHT  # Сбрасываем стиль для остальных категорий
                container.content.color = TEXT
        page.update()

    # Построение меню категорий с обработкой нажатий
    def categories_layout():
        # Контейнер для опции "Все товары"
        all_products_container = ft.Container(
            content=ft.Text(
                "Все товары",
                size=16,
                color=YELLOW_LIGHT,  # Начальный цвет текста - светлый
            ),
            margin=ft.margin.only(top=5, bottom=5),
            on_click=lambda e: filter_by_category(e, "Все товары"),
            border_radius=ft.border_radius.all(5),
            padding=ft.padding.all(8),
            ink=True,
            bgcolor=PINK_MEDIUM,  # Начально выделен
        )
        
        # Сохраняем ссылку на контейнер
        category_containers["Все товары"] = all_products_container
        
        # Создаем контейнеры для каждой категории
        category_items = []
        for category in categories:
            category_container = ft.Container(
                content=ft.Text(
                    category["name"],
                    size=16,
                    color=TEXT,
                ),
                margin=ft.margin.only(top=5, bottom=5),
                on_click=lambda e, name=category["name"]: filter_by_category(e, name),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(8),
                ink=True,
                bgcolor=PINK_LIGHT,
                tooltip=category["description"] if "description" in category and category["description"] else None,
            )
            
            # Сохраняем ссылку на контейнер
            category_containers[category["name"]] = category_container
            category_items.append(category_container)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Категории",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    all_products_container,  # Добавляем опцию "Все товары"
                    *category_items,  # Добавляем остальные категории
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.all(10),
            bgcolor=YELLOW_LIGHT,
            border_radius=ft.border_radius.all(10),
            width=180 if not is_mobile(page) else None,  # Увеличил ширину для лучшего отображения
            margin=ft.margin.only(right=15 if not is_mobile(page) else 0),
        )

    # Создание карточки товара (без изменений)
    def create_product_card(product):
        warranty_info = (
            f", Гарантия: {product['warranty']} мес."
            if "warranty" in product and product["warranty"]
            else ""
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            product["name"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=PINK_DARK,
                        ),
                        ft.Container(
                            content=ft.Text(product["category"], size=12, color=TEXT),
                            bgcolor=PINK_LIGHT,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            border_radius=ft.border_radius.all(12),
                        ),
                        ft.Text(
                            f"Количество: {product['quantity']}{warranty_info}",
                            size=14,
                            color=TEXT,
                        ),
                        ft.Text(
                            f"Цена: {product['price']}",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=PINK_DARK,
                        ),
                        ft.ElevatedButton(
                            text="Заказать",
                            icon=ft.icons.SHOPPING_CART,
                            style=ft.ButtonStyle(
                                bgcolor=PINK_MEDIUM,
                                color=YELLOW_LIGHT,
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda e, p=product["name"]: print(f"Заказан {p}"),
                        ),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(10),
            ),
            width=160 if is_mobile(page) else 200,
            elevation=3,
            margin=ft.margin.all(5),
            color=YELLOW_LIGHT,
        )

    # Инициализируем GridView с продуктами, сохраняя ссылку
    products_grid_view = ft.Container(
        content=ft.GridView(
            [create_product_card(product) for product in current_products],
            runs_count=1 if is_mobile(page) else 3,
            max_extent=250,
            spacing=10,
            run_spacing=10,
            padding=10,
            expand=1,
        ),
        expand=True,
    )

    # Построение сетки товаров
    def products_grid():
        is_mob = is_mobile(page)

        # Компоновка сетки товаров с заголовком
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Товары",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    products_grid_view,  # Используем сохраненный контейнер с GridView
                ],
                expand=True,
            ),
            expand=True,
            padding=ft.padding.all(10),
        )

    # Основной макет с учетом мобильного режима
    def build_layout():
        is_mob = is_mobile(page)

        # Для мобильного: вертикальное расположение
        if is_mob:
            return ft.Column(
                [
                    header_layout(),
                    categories_layout(),
                    products_grid(),
                ],
                spacing=10,
                expand=True,
            )
        # Для десктопа: горизонтальный макет
        else:
            return ft.Column(
                [
                    header_layout(),
                    ft.Row(
                        [
                            categories_layout(),
                            products_grid(),
                        ],
                        expand=True,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=10,
                expand=True,
            )

    # Обработка изменения размера
    def page_resize(e):
        page.update()

    page.on_resize = page_resize

    # Возвращаем контейнер с адаптивным макетом
    return ft.Container(
        content=build_layout(),
        expand=True,
        bgcolor=YELLOW_LIGHT,
    )
