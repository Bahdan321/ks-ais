import flet as ft

# Импортируем цвета
from styles.colors import (
    TEXT,
    PINK_LIGHT,
    YELLOW_LIGHT,
    PINK_MEDIUM,
    YELLOW_DARK,
    PINK_DARK,  # Добавляем PINK_DARK для заголовка
)


def login_view(page: ft.Page):
    """Создает представление страницы авторизации."""

    # Обработчики навигации (пока заглушки, нужно будет реализовать в main.py)
    def go_to_registration(e):
        page.go("/registration")

    # Поля ввода
    email_field = ft.TextField(
        label="Почта",
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
    )
    password_field = ft.TextField(
        label="Пароль",
        width=300,
        password=True,
        can_reveal_password=True,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
    )

    # Кнопка входа
    login_button = ft.ElevatedButton(
        text="Войти",
        width=300,
        bgcolor=PINK_MEDIUM,
        color=YELLOW_LIGHT,
    )

    # Обработчик нажатия кнопки входа (пока пустой)
    def login_click(e):
        print("Попытка входа:")
        print(f"  Почта: {email_field.value}")
        print(f"  Пароль: {password_field.value}")
        # Здесь будет логика проверки данных
        page.snack_bar = ft.SnackBar(ft.Text("Данные для входа (в консоли)"), open=True)
        page.update()

    # Импортируем db_manager
    from db import db_manager

    # Обработчик нажатия кнопки входа
    def login_click(e):
        if not email_field.value or not password_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Пожалуйста, введите почту и пароль!"), open=True
            )
            page.update()
            return

        user = db_manager.verify_user(email_field.value, password_field.value)

        if user:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Добро пожаловать, {user.full_name}!"), open=True
            )
            # Очистка полей
            email_field.value = ""
            password_field.value = ""
            # Здесь можно добавить переход на главную страницу или панель управления
            # page.go("/dashboard") # Пример
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Неверная почта или пароль."), open=True
            )
        page.update()

    login_button.on_click = login_click

    # Текст-ссылка для перехода на регистрацию
    register_link = ft.TextButton(
        content=ft.Text("Нет аккаунта? Зарегистрироваться", color=PINK_DARK, size=14),
        on_click=go_to_registration,
    )

    # Контейнер для формы
    form_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Авторизация",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=PINK_DARK,  # Цвет заголовка
                ),
                email_field,
                password_field,
                ft.Container(height=10),  # Небольшой отступ
                login_button,
                ft.Container(height=5),  # Небольшой отступ
                register_link,  # Добавляем ссылку
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=ft.padding.all(20),
        border_radius=ft.border_radius.all(10),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[PINK_LIGHT, YELLOW_LIGHT],
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

    return form_container
