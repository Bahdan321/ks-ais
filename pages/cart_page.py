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


def cart_view(page: ft.Page, user_id: str):  # Добавляем user_id как параметр
    """Создает представление страницы корзины пользователя."""

    try:
        # Пытаемся преобразовать user_id в int. Если не получится, значит ID некорректный.
        client_id = int(user_id)
        print(f"[DEBUG cart_page] Received user_id from route: {client_id}")  # Отладка
        # Сохраняем ID в сессию для последующих запросов на этой странице, если нужно
        page.session.set("user_id", client_id)
        page.update()
    except (ValueError, TypeError):
        print(f"[DEBUG cart_page] Invalid user_id received: {user_id}")
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

    # Получение товаров в корзине (заглушка, позже заменим на реальные данные)
    def get_cart_items():
        if db_manager:
            # Получаем товары из базы данных
            return db_manager.get_cart_products(client_id)
        return [
            {
                "id": 1,
                "name": "Ноутбук Acer Aspire 5",
                "category": "Ноутбуки",
                "quantity": 1,
                "price": "$699.99",
                "image": "laptop.png",
            },
            {
                "id": 2,
                "name": "Механическая клавиатура Logitech G Pro",
                "category": "Периферия",
                "quantity": 2,
                "price": "$129.99",
                "image": "keyboard.png",
            },
            {
                "id": 3,
                "name": 'Монитор Dell UltraSharp 27"',
                "category": "Мониторы",
                "quantity": 1,
                "price": "$349.99",
                "image": "monitor.png",
            },
        ]

    def checkout(e):
        page.splash = ft.ProgressBar()
        page.update()

        try:
            success, message, order_id = db_manager.create_order_from_cart(client_id)

            if success:
                # Если заказ успешно создан
                def close_dlg(e):
                    dlg.open = False
                    page.update()
                    # Перенаправляем на страницу заказов с ID пользователя
                    page.go(f"/orders/{client_id}")

                dlg = ft.AlertDialog(
                    title=ft.Text("Заказ оформлен!"),
                    content=ft.Text(f"{message}"),
                    actions=[
                        ft.TextButton("Мои заказы", on_click=close_dlg),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            else:
                # Если произошла ошибка
                def close_dlg(e):
                    dlg.open = False
                    page.update()

                dlg = ft.AlertDialog(
                    title=ft.Text("Ошибка"),
                    content=ft.Text(message),
                    actions=[
                        ft.TextButton("OK", on_click=close_dlg),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

            page.dialog = dlg
            dlg.open = True
        except Exception as e:
            print(f"Ошибка при оформлении заказа: {e}")
        finally:
            page.splash = None
            page.update()

    # Вычисление общей стоимости товаров в корзине
    def calculate_total_price(cart_items):
        total = 0
        for item in cart_items:
            # Преобразуем строку цены в число, удаляя символ доллара
            price = float(item["price"].replace("$", ""))
            total += price * item["quantity"]
        return f"${total:.2f}"

    # Получаем товары в корзине
    cart_items = get_cart_items()
    total_price = calculate_total_price(cart_items)

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
                        "Корзина",
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

    # Создание карточки товара в корзине
    def create_cart_item_card(item):
        is_mob = is_mobile(page)

        # Функция увеличения количества
        def increase_quantity(e, item_id):
            for item in cart_items:
                if item["id"] == item_id:
                    item["quantity"] += 1
                    quantity_text.value = f"{item['quantity']}"
                    # Обновляем общую стоимость
                    nonlocal total_price
                    total_price = calculate_total_price(cart_items)
                    total_price_text.value = f"Итого: {total_price}"
                    page.update()
                    break

        # Функция уменьшения количества
        def decrease_quantity(e, item_id):
            for item in cart_items:
                if item["id"] == item_id and item["quantity"] > 1:
                    item["quantity"] -= 1
                    quantity_text.value = f"{item['quantity']}"
                    # Обновляем общую стоимость
                    nonlocal total_price
                    total_price = calculate_total_price(cart_items)
                    total_price_text.value = f"Итого: {total_price}"
                    page.update()
                    break

        # Функция удаления товара из корзины
        def remove_item(e, item_id):
            nonlocal cart_items
            # Находим индекс товара для удаления
            index_to_remove = None
            for i, item in enumerate(cart_items):
                if item["id"] == item_id:
                    index_to_remove = i
                    break

            # Удаляем товар, если найден
            if index_to_remove is not None:
                cart_items.pop(index_to_remove)
                # Обновляем общую стоимость
                nonlocal total_price
                total_price = calculate_total_price(cart_items)
                total_price_text.value = f"Итого: {total_price}"

                # Обновляем список карточек
                cart_list.controls = [
                    create_cart_item_card(item) for item in cart_items
                ]

                # Проверяем, есть ли товары в корзине
                if not cart_items:
                    # Если корзина пуста, показываем сообщение
                    cart_list.controls = [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(
                                        ft.icons.SHOPPING_CART_OUTLINED,
                                        size=50,
                                        color=PINK_DARK,
                                    ),
                                    ft.Text(
                                        "Ваша корзина пуста", size=20, color=PINK_DARK
                                    ),
                                    ft.ElevatedButton(
                                        "Перейти к покупкам",
                                        on_click=lambda e: page.go("/user"),
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
                    ]

                page.update()

        # Текст с количеством товара
        quantity_text = ft.Text(f"{item['quantity']}", size=16, color=TEXT)

        # Создаем карточку товара в корзине
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        # Название и кнопка удаления
                        ft.Row(
                            [
                                ft.Text(
                                    item["name"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=PINK_DARK,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=PINK_DARK,
                                    tooltip="Удалить из корзины",
                                    on_click=lambda e, id=item["id"]: remove_item(
                                        e, id
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        # Категория товара
                        ft.Container(
                            content=ft.Text(item["category"], size=12, color=TEXT),
                            bgcolor=PINK_LIGHT,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            border_radius=ft.border_radius.all(12),
                            width=120 if is_mob else None,
                        ),
                        # Цена товара
                        ft.Text(
                            f"Цена: {item['price']}",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=PINK_DARK,
                        ),
                        # Количество товара с кнопками +/-
                        ft.Row(
                            [
                                ft.Text("Количество:", size=14, color=TEXT),
                                ft.IconButton(
                                    icon=ft.icons.REMOVE,
                                    icon_color=PINK_DARK,
                                    tooltip="Уменьшить",
                                    on_click=lambda e, id=item["id"]: decrease_quantity(
                                        e, id
                                    ),
                                ),
                                quantity_text,
                                ft.IconButton(
                                    icon=ft.icons.ADD,
                                    icon_color=PINK_DARK,
                                    tooltip="Увеличить",
                                    on_click=lambda e, id=item["id"]: increase_quantity(
                                        e, id
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.padding.all(15),
            ),
            elevation=3,
            margin=ft.margin.only(bottom=10),
            color=YELLOW_LIGHT,
        )

    # Создаем список товаров в корзине
    cart_list = ft.ListView(
        [create_cart_item_card(item) for item in cart_items],
        expand=True,
        spacing=10,
        padding=10,
    )

    # Текст с общей стоимостью заказа
    total_price_text = ft.Text(
        f"Итого: {total_price}",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=PINK_DARK,
    )

    def checkout(e):
        page.splash = ft.ProgressBar()
        page.update()

        try:
            print(123123213213231131131, client_id)
            success, message, order_id = db_manager.create_order_from_cart(client_id)

            if success:
                # Если заказ успешно создан
                def close_dlg(e):
                    dlg.open = False
                    page.update()
                    # Перенаправляем на страницу заказов с ID пользователя
                    page.go(f"/orders/{client_id}")

                dlg = ft.AlertDialog(
                    title=ft.Text("Заказ оформлен!"),
                    content=ft.Text(f"{message}"),
                    actions=[
                        ft.TextButton("Мои заказы", on_click=close_dlg),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            else:
                # Если произошла ошибка
                def close_dlg(e):
                    dlg.open = False
                    page.update()

                dlg = ft.AlertDialog(
                    title=ft.Text("Ошибка"),
                    content=ft.Text(message),
                    actions=[
                        ft.TextButton("OK", on_click=close_dlg),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

            page.dialog = dlg
            dlg.open = True
        except Exception as e:
            print(f"Ошибка при оформлении заказа: {e}")
        finally:
            page.splash = None
            page.update()

    # Кнопка оформления заказа
    checkout_button = ft.ElevatedButton(
        "Оформить заказ",
        on_click=checkout,
        style=ft.ButtonStyle(
            bgcolor=PINK_MEDIUM,
            color=YELLOW_LIGHT,
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.all(15),
        ),
        width=300,
    )

    # Основной макет с учетом мобильного режима
    def build_layout():
        is_mob = is_mobile(page)

        # Контейнер с итогом и кнопкой оформления заказа
        checkout_container = ft.Container(
            content=ft.Column(
                [
                    total_price_text,
                    checkout_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.all(20),
            alignment=ft.alignment.center,
            bgcolor=YELLOW_LIGHT,
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, PINK_LIGHT),
        )

        # Для мобильного и десктопного режимов используем одинаковую структуру,
        # но с разными размерами
        return ft.Column(
            [
                header_layout(),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=cart_list,
                                expand=True,
                            ),
                            checkout_container,
                        ],
                        spacing=15,
                        expand=True,
                    ),
                    expand=True,
                    padding=ft.padding.all(15),
                ),
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
