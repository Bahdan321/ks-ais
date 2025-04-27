import flet as ft

# Импортируем представления страниц
from pages.login_page import login_view
from pages.registration_page import registration_view
from pages.user_page import user_view
from pages.admin_page import admin_view
from pages.cart_page import cart_view
from pages.orders_page import orders_view


def main(page: ft.Page):
    page.title = "KS AIS"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Словарь для хранения представлений по маршрутам (статичные маршруты)
    static_views = {
        "/login": login_view(page),
        "/registration": registration_view(page),
        # "/user": user_view(page), # Удаляем статический маршрут user
        "/admin": admin_view(page),
        # "/cart": cart_view(page),
        # "/orders": orders_view(page),
    }

    def route_change(route):
        page.views.clear()
        view_content = None
        current_route = page.route

        # Проверяем динамические маршруты
        if current_route.startswith("/user/"):
            parts = current_route.split("/")
            if len(parts) == 3:
                user_id = parts[2]
                view_content = user_view(page, user_id)
            else:
                view_content = static_views["/login"]
                current_route = "/login"
        elif current_route.startswith("/cart/"):
            parts = current_route.split("/")
            if len(parts) == 3:
                user_id = parts[2]
                view_content = cart_view(page, user_id)
            else:
                view_content = static_views["/login"]
                current_route = "/login"
        elif current_route.startswith("/orders/"):
            parts = current_route.split("/")
            if len(parts) == 3:
                user_id = parts[2]
                view_content = orders_view(page, user_id)
            else:
                view_content = static_views["/login"]
                current_route = "/login"
        else:
            # Обрабатываем статичные маршруты
            view_content = static_views.get(current_route)
            if view_content is None:
                # Если маршрут не найден (ни динамический, ни статичный), перенаправляем на логин
                view_content = static_views["/login"]
                current_route = "/login"

        page.views.append(
            ft.View(
                route=current_route,  # Используем определенный current_route
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
