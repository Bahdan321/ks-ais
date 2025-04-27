import flet as ft
import re  # Для валидации полей
import time  # Для отладки и задержек

# Импортируем цвета
from styles.colors import (
    TEXT,
    PINK_LIGHT,
    YELLOW_LIGHT,
    PINK_MEDIUM,
    YELLOW_DARK,
    PINK_YELLOW_GRADIENT,
    PINK_DARK,
)
from db import db_manager


def registration_view(page: ft.Page):
    """Создает представление страницы регистрации."""
    
    # Состояние загрузки
    is_registering = False
    
    # Функции валидации
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    
    def is_valid_phone(phone):
        # Простая проверка на формат телефона: от 10 до 15 цифр с возможными +, -, ()
        pattern = r"^[+]?[\s(]?\d{1,4}[)]?[-\s.]?[\d\s]{3,14}$"
        return re.match(pattern, phone) is not None
    
    def is_valid_password(password):
        # Требования: минимум 6 символов
        return len(password) >= 6
    
    # Тексты с ошибками
    full_name_error_text = ft.Text("", color=ft.colors.RED_500, size=12)
    phone_error_text = ft.Text("", color=ft.colors.RED_500, size=12)
    email_error_text = ft.Text("", color=ft.colors.RED_500, size=12)
    address_error_text = ft.Text("", color=ft.colors.RED_500, size=12)
    password_error_text = ft.Text("", color=ft.colors.RED_500, size=12)
    
    # Обработчики изменения полей для сброса ошибок
    def field_changed(e, field, error_text):
        error_text.value = ""
        field.border_color = PINK_MEDIUM
        page.update()
    
    # Поля ввода
    full_name_field = ft.TextField(
        label="ФИО",
        width=300,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
        on_change=lambda e: field_changed(e, full_name_field, full_name_error_text),
    )
    phone_field = ft.TextField(
        label="Номер телефона",
        width=300,
        keyboard_type=ft.KeyboardType.PHONE,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
        on_change=lambda e: field_changed(e, phone_field, phone_error_text),
    )
    email_field = ft.TextField(
        label="Почта",
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
        on_change=lambda e: field_changed(e, email_field, email_error_text),
    )
    address_field = ft.TextField(
        label="Адрес",
        width=300,
        multiline=True,
        min_lines=2,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
        on_change=lambda e: field_changed(e, address_field, address_error_text),
    )
    password_field = ft.TextField(
        label="Пароль",
        width=300,
        password=True,
        can_reveal_password=True,
        border_color=PINK_MEDIUM,
        focused_border_color=YELLOW_DARK,
        color=TEXT,
        on_change=lambda e: field_changed(e, password_field, password_error_text),
    )
    
    # Создаем кнопку и индикатор загрузки
    register_button = ft.ElevatedButton(
        text="Зарегистрироваться",
        width=300,
        bgcolor=PINK_MEDIUM,
        color=YELLOW_LIGHT,
    )
    
    # Индикатор загрузки
    register_progress = ft.Row(
        [
            ft.ProgressRing(color=PINK_MEDIUM, width=20, height=20),
            ft.Text("Регистрация...", color=TEXT),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Контейнер для переключения между кнопкой и индикатором
    register_button_container = ft.Container(
        content=register_button,
        width=300,
        alignment=ft.alignment.center,
    )
    
    # Отладочный текст
    debug_text = ft.Text("", color=TEXT, size=10)

    # Обработчик нажатия кнопки регистрации
    def register_click(e):
        nonlocal is_registering
        
        # Если уже идет процесс регистрации, не обрабатываем повторные нажатия
        if is_registering:
            return
        
        # Валидация полей
        has_errors = False
        
        # Проверка ФИО
        if not full_name_field.value:
            full_name_error_text.value = "Введите ФИО"
            full_name_field.border_color = ft.colors.RED_500
            has_errors = True
        elif len(full_name_field.value) < 3:
            full_name_error_text.value = "ФИО должно содержать минимум 3 символа"
            full_name_field.border_color = ft.colors.RED_500
            has_errors = True
        
        # Проверка телефона
        if not phone_field.value:
            phone_error_text.value = "Введите номер телефона"
            phone_field.border_color = ft.colors.RED_500
            has_errors = True
        elif not is_valid_phone(phone_field.value):
            phone_error_text.value = "Некорректный формат телефона"
            phone_field.border_color = ft.colors.RED_500
            has_errors = True
        
        # Проверка email
        if not email_field.value:
            email_error_text.value = "Введите email"
            email_field.border_color = ft.colors.RED_500
            has_errors = True
        elif not is_valid_email(email_field.value):
            email_error_text.value = "Некорректный формат email"
            email_field.border_color = ft.colors.RED_500
            has_errors = True
        
        # Проверка адреса
        if not address_field.value:
            address_error_text.value = "Введите адрес"
            address_field.border_color = ft.colors.RED_500
            has_errors = True
        elif len(address_field.value) < 5:
            address_error_text.value = "Адрес должен содержать минимум 5 символов"
            address_field.border_color = ft.colors.RED_500
            has_errors = True
        
        # Проверка пароля
        if not password_field.value:
            password_error_text.value = "Введите пароль"
            password_field.border_color = ft.colors.RED_500
            has_errors = True
        elif not is_valid_password(password_field.value):
            password_error_text.value = "Пароль должен содержать минимум 6 символов"
            password_field.border_color = ft.colors.RED_500
            has_errors = True
        
        page.update()
        
        if has_errors:
            return
        
        # Показываем индикатор загрузки
        is_registering = True
        debug_text.value = "Начинаем регистрацию..."
        register_button_container.content = register_progress
        page.update()
        
        # Небольшая задержка для отображения индикатора
        time.sleep(0.5)
        
        try:
            debug_text.value = "Отправка данных для регистрации..."
            page.update()
            
            # Регистрация пользователя
            success, message = db_manager.register_user(
                full_name=full_name_field.value,
                phone=phone_field.value,
                email=email_field.value,
                address=address_field.value,
                password=password_field.value,
            )
            
            debug_text.value = f"Результат регистрации: {success}, {message}"
            page.update()
            
            # Показываем сообщение с результатом
            if success:
                page.snack_bar = ft.SnackBar(
                    ft.Text(message), 
                    bgcolor=PINK_DARK,
                    open=True
                )
                page.update()
                
                # Очистка полей после успешной регистрации
                full_name_field.value = ""
                phone_field.value = ""
                email_field.value = ""
                address_field.value = ""
                password_field.value = ""
                
                # Небольшая задержка перед перенаправлением
                time.sleep(1)
                
                debug_text.value = "Перенаправление на страницу входа..."
                page.update()
                
                # Перенаправляем на страницу входа
                page.go("/login")
            else:
                # Показываем ошибку
                page.snack_bar = ft.SnackBar(
                    ft.Text(message), 
                    bgcolor=ft.colors.RED_500,
                    open=True
                )
                
                # Возвращаем кнопку в исходное состояние
                is_registering = False
                register_button_container.content = register_button
                page.update()
                
        except Exception as e:
            debug_text.value = f"Исключение при регистрации: {str(e)}"
            page.update()
            
            # Показываем ошибку
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Ошибка при регистрации: {str(e)}"), 
                bgcolor=ft.colors.RED_500,
                open=True
            )
            
            # Возвращаем кнопку в исходное состояние
            is_registering = False
            register_button_container.content = register_button
            page.update()

    # Устанавливаем обработчик для кнопки
    register_button.on_click = register_click

    # Контейнер для формы
    form_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Регистрация нового пользователя",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=PINK_DARK,
                ),
                full_name_field,
                full_name_error_text,
                phone_field,
                phone_error_text,
                email_field,
                email_error_text,
                password_field,
                password_error_text,
                address_field,
                address_error_text,
                ft.Container(height=10),
                register_button_container,
                debug_text,
                ft.Container(height=5),
                ft.TextButton(
                    content=ft.Text(
                        "Уже есть аккаунт? Войти", color=PINK_DARK, size=14
                    ),
                    on_click=lambda e: page.go("/login"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,  # Уменьшено для компактности с добавленными сообщениями об ошибках
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
    
    # Создаем ScrollView для возможности прокрутки формы на маленьких экранах
    return ft.Container(
        content=ft.Column([form_container], scroll=ft.ScrollMode.AUTO),
        expand=True
    )
