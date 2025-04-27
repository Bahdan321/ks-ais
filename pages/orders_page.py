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
from models.models import OrderStatusEnum


def orders_view(page: ft.Page, user_id: str):  # Добавляем user_id как параметр
    """Создает представление страницы заказов пользователя."""

    try:
        # Пытаемся преобразовать user_id в int. Если не получится, значит ID некорректный.
        client_id = int(user_id)
        print(
            f"[DEBUG orders_page] Received user_id from route: {client_id}"
        )  # Отладка
        # Сохраняем ID в сессию для последующих запросов на этой странице, если нужно
        page.session.set("user_id", client_id)
        page.update()
    except (ValueError, TypeError):
        print(f"[DEBUG orders_page] Invalid user_id received: {user_id}")
        client_id = None  # Считаем ID невалидным

    if not client_id:
        # Если пользователь не авторизован или ID некорректен, показываем сообщение
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Для доступа к этой странице необходимо войти в систему или указать корректный ID пользователя",
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

    # Получение заказов пользователя
    def get_user_orders():
        try:
            print(1231231313122312)
            # Получаем заказы из базы данных
            return db_manager.get_user_orders(client_id)
        except Exception as e:
            print(f"Ошибка при получении заказов: {e}")
            # Возвращаем тестовые данные, если получить из БД не удалось
            return [
                {
                    "id": 1,
                    "date": "15.05.2023 14:30",
                    "status": "Доставлен",
                    "total_price": "$979.97",
                    "items_count": 3,
                    "items": [
                        {
                            "id": 1,
                            "name": "Ноутбук Acer Aspire 5",
                            "category": "Ноутбуки",
                            "quantity": 1,
                            "price": "$699.99",
                            "total_price": "$699.99",
                        },
                        {
                            "id": 2,
                            "name": "Механическая клавиатура Logitech G Pro",
                            "category": "Периферия",
                            "quantity": 2,
                            "price": "$129.99",
                            "total_price": "$259.98",
                        },
                        {
                            "id": 3,
                            "name": "USB Hub 4-портовый",
                            "category": "Периферия",
                            "quantity": 1,
                            "price": "$19.99",
                            "total_price": "$19.99",
                        },
                    ],
                },
                {
                    "id": 2,
                    "date": "03.04.2023 11:15",
                    "status": "Отменен",
                    "total_price": "$349.99",
                    "items_count": 1,
                    "items": [
                        {
                            "id": 4,
                            "name": 'Монитор Dell UltraSharp 27"',
                            "category": "Мониторы",
                            "quantity": 1,
                            "price": "$349.99",
                            "total_price": "$349.99",
                        }
                    ],
                },
            ]

    # Заголовок страницы
    def header_layout():
        is_mob = is_mobile(page)

        # Кнопка назад
        back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=PINK_DARK,
            tooltip="Вернуться к товарам",
            on_click=lambda e: page.go(f"/user/{client_id}"),  # Обновляем переход назад
        )

        return ft.Container(
            content=ft.Row(
                [
                    back_button,
                    ft.Text(
                        "История заказов",
                        color=PINK_DARK,
                        size=22 if is_mob else 28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(width=48),  # Пустой контейнер для баланса
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(10 if is_mob else 20),
            bgcolor=YELLOW_LIGHT,
            border=ft.border.only(bottom=ft.BorderSide(1, PINK_LIGHT)),
        )

    # Функция для получения цвета статуса заказа
    def get_status_color(status):
        status_colors = {
            "Создан": ft.colors.BLUE,
            "Обработан": ft.colors.ORANGE,
            "Отправлен": ft.colors.INDIGO,
            "Доставлен": ft.colors.GREEN,
            "Отменен": ft.colors.RED,
        }
        return status_colors.get(status, ft.colors.GREY)

    # Компонент карточки товара в заказе
    def create_order_item_card(item):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                item["name"],
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=PINK_DARK,
                            ),
                            # ft.Container(
                            #     content=ft.Text(item["category"], size=12, color=TEXT),
                            #     bgcolor=PINK_LIGHT,
                            #     padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            #     border_radius=ft.border_radius.all(12),
                            #     width=120 if is_mobile(page) else None,
                            # ),
                        ],
                        spacing=5,
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"Цена: {item['price']}",
                                size=14,
                                color=TEXT,
                            ),
                            ft.Text(
                                f"Кол-во: {item['quantity']}",
                                size=14,
                                color=TEXT,
                            ),
                            # ft.Text(
                            #     f"Итого: {item['total_price']}",
                            #     size=14,
                            #     weight=ft.FontWeight.BOLD,
                            #     color=PINK_DARK,
                            # ),
                        ],
                        spacing=5,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(10),
            bgcolor=YELLOW_LIGHT,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, PINK_LIGHT),
            margin=ft.margin.only(bottom=8),
        )

    # Функция для создания карточки заказа
    def create_order_card(order):
        # Состояние раскрытия деталей заказа
        is_expanded = False

        # Контейнер для элементов заказа
        items_container = ft.Container(
            content=ft.Column(
                [create_order_item_card(item) for item in order["items"]],
                spacing=5,
            ),
            padding=ft.padding.all(10),
            visible=is_expanded,  # Изначально скрыт
        )

        # Функция для переключения видимости деталей заказа
        def toggle_expand(e):
            nonlocal is_expanded
            is_expanded = not is_expanded
            items_container.visible = is_expanded
            expand_icon.icon = (
                ft.icons.KEYBOARD_ARROW_UP
                if is_expanded
                else ft.icons.KEYBOARD_ARROW_DOWN
            )
            page.update()

        # Иконка для раскрытия/скрытия деталей
        expand_icon = ft.Icon(
            ft.icons.KEYBOARD_ARROW_DOWN,
            color=PINK_DARK,
        )

        # Создаем карточку заказа
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        # Заголовок заказа с основной информацией
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                f"Заказ №{order['order_id']}",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                color=PINK_DARK,
                                            ),
                                            ft.Text(
                                                f"от {order['order_date']}",
                                                size=14,
                                                color=TEXT,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Container(
                                                content=ft.Text(
                                                    order["status"],
                                                    size=14,
                                                    color=YELLOW_LIGHT,
                                                    weight=ft.FontWeight.W_500,
                                                ),
                                                bgcolor=get_status_color(
                                                    order["status"]
                                                ),
                                                padding=ft.padding.symmetric(
                                                    horizontal=12, vertical=5
                                                ),
                                                border_radius=ft.border_radius.all(15),
                                            ),
                                            ft.Text(
                                                f"Итого: {order['total_price']}",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color=PINK_DARK,
                                            ),
                                        ],
                                        spacing=5,
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.all(10),
                        ),
                        # Кнопка для раскрытия деталей заказа
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(
                                        f"Товаров в заказе: {len(order['items'])}",
                                        size=14,
                                        color=TEXT,
                                    ),
                                    ft.TextButton(
                                        content=ft.Row(
                                            [
                                                ft.Text(
                                                    "Детали заказа",
                                                    size=14,
                                                    color=PINK_DARK,
                                                ),
                                                expand_icon,
                                            ],
                                            spacing=5,
                                        ),
                                        on_click=toggle_expand,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.symmetric(horizontal=10),
                        ),
                        # Контейнер с элементами заказа (изначально скрыт)
                        items_container,
                    ],
                    spacing=5,
                ),
                padding=ft.padding.all(5),
            ),
            elevation=3,
            margin=ft.margin.only(bottom=15),
            color=YELLOW_LIGHT,
        )

    # Получаем заказы пользователя
    user_orders = get_user_orders()

    # Создаем список заказов
    orders_list = (
        ft.ListView(
            [create_order_card(order) for order in user_orders],
            expand=True,
            spacing=10,
            padding=15,
        )
        if user_orders
        else ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.icons.RECEIPT_LONG, size=50, color=PINK_DARK),
                    ft.Text("У вас еще нет заказов", size=20, color=PINK_DARK),
                    ft.ElevatedButton(
                        "Перейти к покупкам",
                        on_click=lambda e: page.go(
                            f"/user/{client_id}"
                        ),  # Обновляем переход к товарам
                        style=ft.ButtonStyle(
                            bgcolor=PINK_MEDIUM,
                            color=YELLOW_LIGHT,
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
            expand=True,
            alignment=ft.alignment.center,
        )
    )

    # Основной макет страницы
    def build_layout():
        return ft.Column(
            [
                header_layout(),
                orders_list,
            ],
            spacing=0,
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
