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
from db import db_manager
from models.models import UserRoleEnum


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

    # Обработчик нажатия кнопки входа
    def login_click(e):
        if not email_field.value or not password_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Пожалуйста, введите почту и пароль!"), open=True
            )
            page.update()
            return

        # Проверяем учетные данные пользователя
        success, user_data = db_manager.verify_user(
            email_field.value, password_field.value
        )

        if success:
            # Сохраняем ID пользователя в сессии
            try:
                page.session.set("user_id", user_data["id"])
                page.session.set("user_name", user_data["name"])
                # Преобразуем Enum в строку перед сохранением
                page.session.set(
                    "user_role",
                    (
                        str(user_data["role"].value)
                        if isinstance(user_data["role"], UserRoleEnum)
                        else user_data["role"]
                    ),
                )
                print(
                    f"[DEBUG login_page] Session after set: user_id={page.session.get('user_id')}, user_name={page.session.get('user_name')}, user_role={page.session.get('user_role')}"
                )  # Отладка
                page.update()  # Обновляем страницу, чтобы сохранить сессию ПЕРЕД редиректом
            except Exception as e:
                print(f"Ошибка при сохранении данных сессии: {e}")
                page.snack_bar = ft.SnackBar(
                    ft.Text("Ошибка при сохранении данных сессии."), open=True
                )
                page.update()
                return

            page.snack_bar = ft.SnackBar(
                ft.Text(f"Добро пожаловать, {user_data['name']}!"), open=True
            )

            # Очистка полей
            email_field.value = ""
            password_field.value = ""

            print(
                f"[DEBUG login_page] Session before redirect: user_id={page.session.get('user_id')}, user_name={page.session.get('user_name')}, user_role={page.session.get('user_role')}"
            )  # Отладка
            # Перенаправление в зависимости от роли
            user_id = user_data["id"]  # Получаем ID пользователя
            # Сравниваем строковое представление роли из сессии
            if page.session.get("user_role") == UserRoleEnum.ADMIN.value:
                page.go(
                    "/admin"
                )  # Для админа оставляем как есть или передаем ID, если нужно
            else:
                page.go(f"/user/{user_id}")  # Передаем user_id в URL
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
