import flet as ft
from styles.colors import PINK_MEDIUM, YELLOW_LIGHT, TEXT, PINK_DARK


class ProductCard:
    def __init__(self, product_name, quantity, price, on_buy_click):
        super().__init__()
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.on_buy_click = on_buy_click

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            self.product_name,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT,
                        ),
                        ft.Text(f"Количество: {self.quantity}", size=14, color=TEXT),
                        ft.Text(
                            f"Цена: {self.price}",
                            size=14,
                            color=TEXT,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(height=5),  # Отступ
                        ft.ElevatedButton(
                            text="Купить",
                            on_click=lambda e: self.on_buy_click(
                                self.product_name
                            ),  # Передаем имя товара
                            bgcolor=PINK_MEDIUM,
                            color=YELLOW_LIGHT,
                            width=150,  # Фиксированная ширина кнопки
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5)
                            ),
                        ),
                    ],
                    spacing=5,
                    # Выравнивание элементов внутри карточки
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(15),
                border_radius=ft.border_radius.all(10),
                # Можно добавить легкий фон или границу для самой карточки
                # bgcolor=ft.colors.with_opacity(0.05, PINK_DARK)
            ),
            width=200,  # Ширина карточки
            # height=180, # Можно убрать высоту для авто-подстройки
            elevation=2,  # Небольшая тень
            margin=ft.margin.all(10),  # Отступы между карточками
        )
