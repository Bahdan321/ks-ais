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
                        # Название товара с ограничением высоты и переносом
                        ft.Container(
                            content=ft.Text(
                                self.product_name,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT,
                                max_lines=2,  # Ограничим двумя строками
                                overflow=ft.TextOverflow.ELLIPSIS,  # Добавляем многоточие
                                text_align=ft.TextAlign.CENTER,  # Центрирование текста
                            ),
                            height=50,  # Фиксированная высота для названия
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(
                            f"Количество: {self.quantity}", 
                            size=14, 
                            color=TEXT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            f"Цена: {self.price}",
                            size=14,
                            color=TEXT,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=5),  # Отступ
                        ft.Container(
                            content=ft.ElevatedButton(
                                text="Купить",
                                on_click=lambda e: self.on_buy_click(self.product_name),
                                bgcolor=PINK_MEDIUM,
                                color=YELLOW_LIGHT,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=5)
                                ),
                                # Кнопка на всю ширину карточки
                                width=float("inf"),
                            ),
                            # Контейнер для контроля размера кнопки
                            width=float("inf"),
                        ),
                    ],
                    spacing=5,
                    # Выравнивание элементов внутри карточки
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    # Растягиваем колонку на всю ширину контейнера
                    width=float("inf"),
                ),
                padding=ft.padding.all(15),
                border_radius=ft.border_radius.all(10),
                width=float("inf"),  # Контейнер занимает всю доступную ширину
            ),
            # Адаптивная ширина карточки с минимальным значением
            width=200,  # Минимальная ширина карточки
            margin=ft.margin.all(10),
            elevation=2,
        )
