class InvalidProductError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class Product:
    def __init__(self,
                 name: str,
                 price: float,
                 quantity: int):

        if price < 0:
            raise InvalidProductError("Цена должна быть неотрицательными и не равна 0.")

        if quantity < 0:
            raise InvalidProductError("Количество должно быть неотрицательными и не равно 0.")

        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):

        return f"Продукт: {self.name}, Цена: {self.price}, Количество: {self.quantity})"


class Order:
    def __init__(self,
                 products: list = None):

        if products is None:
            products = []
        self.products = products

    def add_product(self, product):

        if isinstance(product, Product):
            self.products.append(product)
            print(f"Продукт '{product.name}' успешно добавлен в заказ")

    def remove_product(self, name):

        for product in self.products:
            if product.name == name:
                self.products.remove(product)
                print(f'Продукт: {name} успешно удаленн')
            else:
                raise ProductNotFoundError(f"Продукт: {name} нету в заказе.")

    def total_price (self):
        sum_total_price = 0
        for product in self.products:
            sum_total_price += product.price * product.quantity
        print(f"Общая сумма заказа равна {sum_total_price}")


order = Order()

product1 = Product('sugar', 25.5, 5)
product2 = Product('chocolat', 15.5, 10)

order.add_product(product1)
order.add_product(product2)
order.total_price()
# order.remove_product('snickers')     # Проверка ошибки на то что продукта нету в заказе
order.remove_product('sugar')
order.total_price()


# product3 = Product('sweet', -15, 5)  # Проверка ошибки на то что цена продукта отрицательная
# product4 = Product('bubble', 10, -1) # Проверка ошибки на то что количество продукта отрицательная





