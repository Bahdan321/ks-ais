import flet as ft

# Импортируем цвета
from styles.colors import (
    TEXT,
    PINK_LIGHT,
    YELLOW_LIGHT,
    PINK_MEDIUM,
    YELLOW_DARK,
    PINK_DARK,
)


def user_view(page: ft.Page):
    """Создает представление страницы пользователя."""

    # Кнопки в правом верхнем углу
    personal_account_button = ft.TextButton(
        content=ft.Text("Личный кабинет", color=PINK_DARK),
        on_click=lambda e: page.go("/personal_account"),
    )
    cart_button = ft.TextButton(
        content=ft.Text("Корзина", color=PINK_DARK), on_click=lambda e: page.go("/cart")
    )

    # Категории товаров
    categories = [
        "Ноутбуки",
        "Мониторы",
        "Комплектующие",
        "Периферия",
        "Сетевое оборудование",
    ]

    # Пример товаров
    products = [
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

    # Карточки товаров
    product_cards = [
        ft.Card(
            content=ft.Column(
                [
                    ft.Text(product["name"], size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Категория: {product['category']}", size=14),
                    ft.Text(f"Количество: {product['quantity']}", size=14),
                    ft.Text(f"Цена: {product['price']}", size=14),
                    ft.ElevatedButton(
                        text="Заказать",
                        on_click=lambda e: print(f"Заказан {product['name']}"),
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=200,
            height=150,
            # padding=ft.padding.all(10),
            margin=ft.margin.all(5),
        )
        for product in products
    ]

    # Контейнер для страницы
    page_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [personal_account_button, cart_button],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "Категории", size=18, weight=ft.FontWeight.BOLD
                                ),
                                *[
                                    ft.Text(category, size=16)
                                    for category in categories
                                ],
                            ],
                            width=150,
                        ),
                        # ft.Wrap(product_cards, spacing=10),
                    ]
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.all(20),
        expand=True,
    )

    return page_container
