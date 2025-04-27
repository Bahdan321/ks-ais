import flet as ft
from styles.colors import (
    TEXT,
    PINK_LIGHT,
    YELLOW_LIGHT,
    PINK_MEDIUM,
    YELLOW_DARK,
    PINK_DARK,
)
from db import db_manager


def user_view(page: ft.Page, user_id: str):  # Добавляем user_id как параметр
    """Создает представление страницы пользователя с фильтрацией товаров по категориям."""
    try:
        # Пытаемся преобразовать user_id в int. Если не получится, значит ID некорректный.
        client_id = int(user_id)
        print(
            f"[DEBUG user_page] Received user_id from route: {client_id}"
        )  # Отладка: Показываем ID из маршрута
        # Сохраняем ID в сессию для последующих запросов на этой странице, если нужно
        page.session.set("user_id", client_id)
        page.update()
    except (ValueError, TypeError):
        print(f"[DEBUG user_page] Invalid user_id received: {user_id}")
        client_id = None  # Считаем ID невалидным

    if not client_id:
        # Вместо редиректа и пустого return
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Для доступа к этой странице необходимо войти в систему",
                        size=16,
                        color=PINK_DARK,
                    ),
                    ft.ElevatedButton(
                        "Войти",
                        on_click=lambda _: page.go("/login"),
                        style=ft.ButtonStyle(
                            bgcolor=PINK_MEDIUM,
                            color=YELLOW_LIGHT,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
            alignment=ft.alignment.center,
        )

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
            on_click=lambda e: page.go(
                f"/cart/{client_id}"
            ),  # Обновляем переход на корзину
        )

        orders_button = ft.TextButton(
            content=ft.Text(
                "Заказы",
                color=PINK_DARK,
                size=14 if is_mob else 16,
                weight=ft.FontWeight.W_500,
            ),
            style=ft.ButtonStyle(
                bgcolor=YELLOW_LIGHT,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda e: page.go(
                f"/orders/{client_id}"
            ),  # Обновляем переход на заказы
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
                    orders_button,
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
                {
                    "id": 3,
                    "name": "Комплектующие",
                    "description": "Детали для компьютеров",
                },
                {"id": 4, "name": "Периферия", "description": "Внешние устройства"},
                {
                    "id": 5,
                    "name": "Сетевое оборудование",
                    "description": "Устройства для сети",
                },
            ]

    # Получение всех товаров из базы данных
    def get_all_products():
        try:
            # return db_manager.get_all_products()
            products = db_manager.get_all_products()

            for p in products:
                if isinstance(p.get("category"), dict):
                    p["category"] = p["category"].get("name", "")

            return products

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
                },
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
                highlight_selected_category(
                    category_name
                )  # Выделяем выбранную категорию

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
                container.bgcolor = (
                    PINK_MEDIUM  # Выделяем "Все товары" если ничего не выбрано
                )
                container.content.color = YELLOW_LIGHT
            else:
                container.bgcolor = (
                    PINK_LIGHT  # Сбрасываем стиль для остальных категорий
                )
                container.content.color = TEXT
        page.update()

    # Построение меню категорий с обработкой нажатий
    # Категории для мобильного режима - горизонтальный скролл
    def categories_layout():
        is_mob = is_mobile(page)
        
        # Контейнер для "Все товары"
        all_products_container = ft.Container(
            content=ft.Text(
                "Все товары",
                size=14,  # Меньший размер на мобильных
                color=YELLOW_LIGHT,
            ),
            margin=ft.margin.only(top=5, bottom=5, right=5, left=5),
            on_click=lambda e: filter_by_category(e, "Все товары"),
            border_radius=ft.border_radius.all(5),
            padding=ft.padding.all(6),  # Меньший отступ на мобильных
            ink=True,
            bgcolor=PINK_MEDIUM,
        )
        
        # Сохраняем ссылку на контейнер
        category_containers["Все товары"] = all_products_container
        
        # Создаем контейнеры для каждой категории
        category_items = []
        for category in categories:
            category_container = ft.Container(
                content=ft.Text(
                    category["name"],
                    size=14,
                    color=TEXT,
                    max_lines=1,  # Ограничиваем одной строкой
                    overflow=ft.TextOverflow.ELLIPSIS,  # Добавляем многоточие
                ),
                margin=ft.margin.only(top=5, bottom=5, right=5, left=5),
                on_click=lambda e, name=category["name"]: filter_by_category(e, name),
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(6),
                ink=True,
                bgcolor=PINK_LIGHT,
                tooltip=category["description"] if "description" in category and category["description"] else None,
            )
            
            category_containers[category["name"]] = category_container
            category_items.append(category_container)
        
        # На мобильных - горизонтальный скролл для категорий
        if is_mob:
            return ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Категории",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [all_products_container, *category_items],
                            spacing=5,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    )
                ]),
                padding=ft.padding.all(10),
                bgcolor=YELLOW_LIGHT,
                border_radius=ft.border_radius.all(10),
            )
        else:  # десктоп – тот же горизонтальный скролл, что и на мобилке
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Категории",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=PINK_DARK,
                        ),
                        ft.Row(
                            [all_products_container, *category_items],
                            spacing=5,
                            scroll=ft.ScrollMode.AUTO,
                            wrap=True,
                        ),
                    ]
                ),
                padding=ft.padding.all(10),
                bgcolor=YELLOW_LIGHT,
                border_radius=ft.border_radius.all(10),
            )

    # Создание карточки товара (без изменений)
    def create_product_card(product):
        category_name = (
            product["category"]["name"] if isinstance(product["category"], dict) else product["category"]
        )

        warranty_info = (
            f", Гарантия: {product['warranty']} мес."
            if "warranty" in product and product["warranty"]
            else ""
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        # Название товара с ограничением и переносом
                        ft.Container(
                            content=ft.Text(
                                # product["name"],
                                category_name,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=PINK_DARK,
                                max_lines=2,  # Ограничим количество строк
                                overflow=ft.TextOverflow.ELLIPSIS,  # Добавим многоточие
                                text_align=ft.TextAlign.CENTER,  # Центрируем текст
                            ),
                            height=50,  # Фиксированная высота
                            alignment=ft.alignment.center,
                            width=float("inf"),  # Занимает всю ширину
                        ),
                        ft.Container(
                            content=ft.Text(
                                product["category"],
                                size=12,
                                color=TEXT,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            bgcolor=PINK_LIGHT,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            border_radius=ft.border_radius.all(12),
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(
                            f"Количество: {product['quantity']}{warranty_info}",
                            size=14,
                            color=TEXT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            f"Цена: {product['price']}",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=PINK_DARK,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        # Кнопка на всю ширину карточки
                        ft.Container(
                            content=ft.ElevatedButton(
                                text="Заказать",
                                icon=ft.icons.SHOPPING_CART,
                                style=ft.ButtonStyle(
                                    bgcolor=PINK_MEDIUM,
                                    color=YELLOW_LIGHT,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e, p=product["name"], prod_id=product["id"]: (
                                    db_manager.add_product_to_cart(
                                        client_id=client_id,
                                        product_id=prod_id,
                                        quantity=1,
                                    ),
                                    print(f"Заказан {p} (ID: {prod_id}) для пользователя {client_id}"),
                                    setattr(page, "snack_bar", ft.SnackBar(
                                        ft.Text(f"{p} добавлен в корзину."), open=True
                                    )),
                                    page.update(),
                                ),
                                width=float("inf"),  # Растягиваем на всю ширину
                            ),
                            width=float("inf"),  # Контейнер на всю ширину
                        ),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=float("inf"),  # Колонка на всю ширину
                ),
                padding=ft.padding.all(10),
                width=float("inf"),  # Контейнер на всю ширину
            ),
            width=160 if is_mobile(page) else 200,  # Адаптивная ширина в зависимости от устройства
            elevation=3,
            margin=ft.margin.all(5),
            color=YELLOW_LIGHT,
        )


    # Инициализируем GridView с продуктами, сохраняя ссылку
    products_grid_view = ft.Container(
        content=ft.GridView(
            [create_product_card(product) for product in current_products],
            # Адаптивное количество столбцов в зависимости от размера экрана
            runs_count=1 if is_mobile(page) else (2 if page.width < 900 else 3),
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
        # независимо от размера экрана категории идут сверху
        return ft.Column(
            [
                header_layout(),
                categories_layout(),
                products_grid(),
            ],
            spacing=10,
            expand=True,
        )


    # Обработка изменения размера
    def page_resize(e):
        products_grid_view.content.runs_count = 1 if is_mobile(page) else (2 if page.width < 900 else 3)
        page.update()

    page.on_resize = page_resize

    # Возвращаем контейнер с адаптивным макетом
    return ft.Container(
        content=build_layout(),
        expand=True,
        bgcolor=YELLOW_LIGHT,
    )
