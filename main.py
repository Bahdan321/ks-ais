import flet as ft

# Импортируем представления страниц
from pages.login_page import login_view
from pages.registration_page import registration_view


def main(page: ft.Page):
    page.title = "KS AIS"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Словарь для хранения представлений по маршрутам
    views = {
        "/login": login_view(page),  # Передаем объект page
        "/registration": registration_view(page),  # Передаем объект page
    }

    def route_change(route):
        page.views.clear()
        # Получаем представление по маршруту или страницу входа по умолчанию
        view_content = views.get(page.route, views["/login"])
        page.views.append(
            ft.View(
                route=page.route,  # Устанавливаем текущий маршрут для View
                controls=[view_content],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                padding=0,  # Убираем отступы у View, т.к. они есть в контейнерах страниц
            )
        )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Устанавливаем начальный маршрут
    page.go("/login")


# Запуск приложения
ft.app(target=main)
