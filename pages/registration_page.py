import flet as ft

# Импортируем цвета
from styles.colors import (
    TEXT,
    PINK_LIGHT,
    YELLOW_LIGHT,
    PINK_MEDIUM,
    YELLOW_DARK,
    PINK_YELLOW_GRADIENT,
    PINK_DARK,  # Добавлен PINK_DARK
)
from db import db_manager


def registration_view(page: ft.Page):
    """Создает представление страницы регистрации."""

    # Поля ввода
    full_name_field = ft.TextField(
        label="ФИО",
        width=300,
        border_color=PINK_MEDIUM,  # Цвет рамки
        focused_border_color=YELLOW_DARK,  # Цвет рамки при фокусе
        color=TEXT,
    )
    phone_field = ft.TextField(
        label="Номер телефона",
        width=300,
        keyboard_type=ft.KeyboardType.PHONE,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
    )
    email_field = ft.TextField(
        label="Почта",
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
    )
    address_field = ft.TextField(
        label="Адрес",
        width=300,
        multiline=True,
        min_lines=2,
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

    # Кнопка регистрации
    register_button = ft.ElevatedButton(
        text="Зарегистрироваться",
        width=300,
        bgcolor=PINK_MEDIUM,  # Цвет фона кнопки
        color=YELLOW_LIGHT,  # Цвет текста кнопки
    )

    # Обработчик нажатия кнопки
    def register_click(e):
        # Валидация полей (простая проверка на пустоту)
        if not all(
            [
                full_name_field.value,
                phone_field.value,
                email_field.value,
                address_field.value,
                password_field.value,
            ]
        ):
            page.snack_bar = ft.SnackBar(
                ft.Text("Пожалуйста, заполните все поля!"), open=True
            )
            page.update()
            return

        success, message = db_manager.register_user(
            full_name=full_name_field.value,
            phone=phone_field.value,
            email=email_field.value,
            address=address_field.value,
            password=password_field.value,
        )

        page.snack_bar = ft.SnackBar(ft.Text(message), open=True)
        if success:
            # Очистка полей после успешной регистрации (опционально)
            full_name_field.value = ""
            phone_field.value = ""
            email_field.value = ""
            address_field.value = ""
            password_field.value = ""

            page.go("/login")
        page.update()

    register_button.on_click = register_click

    # Контейнер для формы
    form_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Регистрация нового пользователя",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=PINK_DARK,  # Цвет заголовка
                ),
                full_name_field,
                phone_field,
                email_field,
                password_field,  # Добавляем поле пароля
                address_field,
                ft.Container(height=10),  # Небольшой отступ
                register_button,
                ft.Container(height=5),  # Небольшой отступ
                ft.TextButton(
                    content=ft.Text(
                        "Уже есть аккаунт? Войти", color=PINK_DARK, size=14
                    ),
                    on_click=lambda e: page.go(
                        "/login"
                    ),  # Добавляем обработчик для перехода
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=ft.padding.all(20),
        border_radius=ft.border_radius.all(10),
        # Используем градиент для фона контейнера
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[PINK_LIGHT, YELLOW_LIGHT],
        ),
        # bgcolor=ft.colors.SURFACE_VARIANT, # Заменяем на градиент
        alignment=ft.alignment.center,
        expand=True,  # Чтобы контейнер занимал все доступное пространство
    )

    return form_container
