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
    """Создает представление страницы администратора, адаптированное для мобильных устройств."""

    # Установка свойств страницы
    page.padding = 0
    page.bgcolor = YELLOW_LIGHT

    # Функция для проверки мобильного режима
    def is_mobile(page):
        return page.width < 600

    # Заголовок панели администратора
    def admin_header():
        is_mob = is_mobile(page)

        # Кнопка выхода
        logout_button = ft.ElevatedButton(
            text="Выйти" if not is_mob else "",
            icon=ft.icons.LOGOUT,
            style=ft.ButtonStyle(
                bgcolor=PINK_MEDIUM,
                color=YELLOW_LIGHT,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda e: page.go("/login"),
        )

        # Адаптивная компоновка заголовка
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        ft.icons.ADMIN_PANEL_SETTINGS,
                        color=PINK_DARK,
                        size=30 if not is_mob else 24,
                    ),
                    ft.Text(
                        "Панель администратора",
                        size=24 if not is_mob else 18,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    logout_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(15),
            bgcolor=YELLOW_LIGHT,
            border=ft.border.only(bottom=ft.BorderSide(1, PINK_LIGHT)),
            margin=ft.margin.only(bottom=10),
        )

    # Создание панели с метриками
    def metrics_panel():
        is_mob = is_mobile(page)

        # Элементы метрик
        metrics = [
            {"icon": ft.icons.PEOPLE_ALT, "title": "Пользователи", "value": "256"},
            {"icon": ft.icons.INVENTORY_2, "title": "Товары", "value": "532"},
            {"icon": ft.icons.SHOPPING_BAG, "title": "Заказы", "value": "128"},
            {"icon": ft.icons.TRENDING_UP, "title": "Прибыль", "value": "$12,450"},
        ]

        metric_items = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(metric["icon"], size=24, color=PINK_DARK),
                        ft.Text(
                            metric["title"],
                            size=14,
                            color=TEXT,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text(
                            metric["value"],
                            size=20,
                            color=PINK_DARK,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(15),
                border_radius=ft.border_radius.all(10),
                bgcolor=PINK_LIGHT,
                width=110 if is_mob else 150,
            )
            for metric in metrics
        ]

        # Размещение метрик в ряд или столбец в зависимости от размера экрана
        if is_mob:
            metrics_layout = ft.Column(
                [
                    ft.Row(
                        metric_items[:2], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        metric_items[2:], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                ],
                spacing=10,
            )
        else:
            metrics_layout = ft.Row(
                metric_items,
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Статистика",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    metrics_layout,
                ],
                spacing=10,
            ),
            padding=ft.padding.all(15),
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, PINK_LIGHT),
            margin=ft.margin.only(bottom=15),
        )

    # Функция для создания карточек управления
    def create_management_card(title, description, icon, action_text):
        is_mob = is_mobile(page)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(icon, size=30, color=PINK_DARK),
                                ft.Column(
                                    [
                                        ft.Text(
                                            title,
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=PINK_DARK,
                                        ),
                                        ft.Text(
                                            description,
                                            size=14,
                                            color=TEXT,
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Text(
                                        action_text,
                                        size=14,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    ft.Icon(ft.icons.ARROW_FORWARD, size=16),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=PINK_MEDIUM,
                                color=YELLOW_LIGHT,
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            width=None if is_mob else 200,
                        ),
                    ],
                    spacing=15,
                ),
                padding=ft.padding.all(15),
            ),
            elevation=3,
            margin=ft.margin.only(bottom=10),
        )

    # Функции управления
    management_functions = [
        {
            "title": "Управление пользователями",
            "description": "Добавление, удаление и изменение прав пользователей системы",
            "icon": ft.icons.PEOPLE,
            "action": "Управлять пользователями",
        },
        {
            "title": "Управление товарами",
            "description": "Добавление новых товаров, редактирование цен и характеристик",
            "icon": ft.icons.INVENTORY,
            "action": "Управлять товарами",
        },
        {
            "title": "Управление заказами",
            "description": "Просмотр и обработка заказов, изменение статусов, отчеты",
            "icon": ft.icons.SHOPPING_CART,
            "action": "Управлять заказами",
        },
        {
            "title": "Скидки и акции",
            "description": "Создание промокодов, настройка акций и специальных предложений",
            "icon": ft.icons.LOCAL_OFFER,
            "action": "Настроить акции",
        },
        {
            "title": "Отчеты и статистика",
            "description": "Формирование отчетов по продажам, анализ данных",
            "icon": ft.icons.BAR_CHART,
            "action": "Просмотреть отчеты",
        },
    ]

    # Создание карточек функций управления
    management_cards = [
        create_management_card(
            func["title"],
            func["description"],
            func["icon"],
            func["action"],
        )
        for func in management_functions
    ]

    # Главная секция с функциями управления
    def management_section():
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Функции управления",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=PINK_DARK,
                    ),
                    ft.Column(management_cards, spacing=10, scroll=ft.ScrollMode.AUTO),
                ],
                spacing=10,
            ),
            padding=ft.padding.all(15),
            expand=True,
        )

    # Быстрые действия (для мобильной версии)
    def quick_actions():
        if not is_mobile(page):
            return ft.Container()  # Пустой контейнер для десктопа

        quick_buttons = [
            ft.IconButton(
                icon=ft.icons.PEOPLE,
                icon_color=YELLOW_LIGHT,
                bgcolor=PINK_MEDIUM,
                icon_size=24,
                tooltip="Пользователи",
            ),
            ft.IconButton(
                icon=ft.icons.INVENTORY,
                icon_color=YELLOW_LIGHT,
                bgcolor=PINK_MEDIUM,
                icon_size=24,
                tooltip="Товары",
            ),
            ft.IconButton(
                icon=ft.icons.SHOPPING_CART,
                icon_color=YELLOW_LIGHT,
                bgcolor=PINK_MEDIUM,
                icon_size=24,
                tooltip="Заказы",
            ),
            ft.IconButton(
                icon=ft.icons.BAR_CHART,
                icon_color=YELLOW_LIGHT,
                bgcolor=PINK_MEDIUM,
                icon_size=24,
                tooltip="Отчеты",
            ),
        ]

        return ft.Container(
            content=ft.Row(
                quick_buttons,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            padding=ft.padding.symmetric(vertical=10),
            bgcolor=YELLOW_LIGHT,
            border=ft.border.only(top=ft.BorderSide(1, PINK_LIGHT)),
        )

    # Боковая панель навигации (для десктопа)
    def sidebar_navigation():
        if is_mobile(page):
            return ft.Container()  # Пустой контейнер для мобильной версии

        nav_items = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(func["icon"], size=20, color=PINK_DARK),
                        ft.Text(
                            func["title"],
                            size=14,
                            color=PINK_DARK,
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.all(5),
                bgcolor=PINK_LIGHT,
                margin=ft.margin.only(bottom=5),
                ink=True,
                on_click=lambda e, title=func["title"]: print(f"Выбрано: {title}"),
            )
            for func in management_functions
        ]

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.icons.MENU, color=PINK_DARK),
                                ft.Text(
                                    "Навигация",
                                    weight=ft.FontWeight.BOLD,
                                    color=PINK_DARK,
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=ft.padding.all(10),
                    ),
                    *nav_items,
                ],
                spacing=5,
            ),
            width=250,
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, PINK_LIGHT),
            margin=ft.margin.only(right=15),
            padding=ft.padding.all(10),
        )

    # Основной макет с учетом мобильного режима
    def build_layout():
        is_mob = is_mobile(page)

        # Для мобильного: вертикальное расположение
        if is_mob:
            return ft.Column(
                [
                    admin_header(),
                    ft.Container(
                        content=ft.Column(
                            [
                                metrics_panel(),
                                management_section(),
                            ],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        padding=ft.padding.symmetric(horizontal=15),
                        expand=True,
                    ),
                    quick_actions(),
                ],
                expand=True,
            )
        # Для десктопа: горизонтальный макет с боковой панелью
        else:
            return ft.Column(
                [
                    admin_header(),
                    ft.Row(
                        [
                            sidebar_navigation(),
                            ft.Column(
                                [
                                    metrics_panel(),
                                    management_section(),
                                ],
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                            ),
                        ],
                        expand=True,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
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
