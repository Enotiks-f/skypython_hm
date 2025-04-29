import json
from itertools import product


class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        return (self.__price * self.quantity) + (other.__price * other.quantity)

    @classmethod
    def new_product(cls, data: dict):
        return cls(data["name"], data["description"], data["price"], data["quantity"])

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):

        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            ans = input("Новая цена ниже старый, вы уверены в изменение цены (y/n?)")
            if ans == "y":
                self.__price = new_price
            else:
                print("Изменения не применены")
        else:
            self.__price = new_price



class Category:
    categotries_count = 0
    product_count = 0

    name: str
    description: str
    products: list["Product"]

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products

        Category.product_count += len(products)

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1

    @property
    def products(self):
        result = []
        for product in self.__products:
            result.append(
                f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            )
        return "\n".join(result)

    @property
    def product_list(self):
        return self.__products

    def __str__(self):
        return f'{self.name}, количество продуктов: {Product.quantity}.'

class CategoryIterator:

    def __init__(self, category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._category.product_list):
            raise StopIteration
        product = self._category.product_list[self._index]
        self._index += 1
        return product

def read_json(file_patch):
    categories = []

    with open(file_patch, encoding="utf-8") as f:
        data = json.load(f)

    for i in data:
        name = i["name"]
        description = i["description"]
        products_data = i["products"]

        products = []
        for j in products_data:
            product = Product(
                name=j["name"],
                description=j["description"],
                price=j["price"],
                quantity=j["quantity"],
            )
            products.append(product)

        category = Category(name, description, products)
        categories.append(category)

    return categories

