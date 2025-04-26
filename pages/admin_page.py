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


def admin_view(page: ft.Page):
    """Создает представление страницы администратора."""

    # Пример функциональности для администратора
    admin_functions = [
        {
            "name": "Управление товарами",
            "action": lambda e: print("Управление товарами"),
        },
        {
            "name": "Управление пользователями",
            "action": lambda e: print("Управление пользователями"),
        },
    ]

    # Кнопки функциональности
    function_buttons = [
        ft.ElevatedButton(
            text=function["name"],
            on_click=function["action"],
            width=200,
            bgcolor=PINK_MEDIUM,
            color=YELLOW_LIGHT,
        )
        for function in admin_functions
    ]

    # Контейнер для страницы
    page_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Панель администратора",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=PINK_DARK,
                ),
                # ft.Wrap(function_buttons, spacing=10),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.all(20),
        expand=True,
    )

    return page_container
