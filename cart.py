class CartManager:
    """Класс для управления корзиной пользователя."""
    
    def __init__(self):
        # Словарь корзин пользователей: {client_id: [{product_id, quantity, ...}, ...]}
        self.user_carts = {}
    
    def get_cart(self, client_id):
        """Получает корзину пользователя."""
        if client_id not in self.user_carts:
            self.user_carts[client_id] = []
        return self.user_carts[client_id]
    
    def add_to_cart(self, client_id, product_id, quantity=1):
        """Добавляет товар в корзину."""
        cart = self.get_cart(client_id)
        
        # Проверяем, есть ли уже такой товар в корзине
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                return True
        
        # Добавляем новый товар
        cart.append({"product_id": product_id, "quantity": quantity})
        return True
    
    def remove_from_cart(self, client_id, product_id):
        """Удаляет товар из корзины."""
        cart = self.get_cart(client_id)
        
        # Удаляем товар, если он есть в корзине
        for i, item in enumerate(cart):
            if item["product_id"] == product_id:
                cart.pop(i)
                return True
        
        return False
    
    def update_quantity(self, client_id, product_id, quantity):
        """Обновляет количество товара в корзине."""
        cart = self.get_cart(client_id)
        
        for item in cart:
            if item["product_id"] == product_id:
                if quantity <= 0:
                    return self.remove_from_cart(client_id, product_id)
                item["quantity"] = quantity
                return True
        
        return False
    
    def clear_cart(self, client_id):
        """Очищает корзину пользователя."""
        self.user_carts[client_id] = []
        return True

cart_manager = CartManager()