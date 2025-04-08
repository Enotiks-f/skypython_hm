import json
class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

class Category:
    total_categotries = 0
    total_products = 0

    name: str
    description: str
    products: list['Product']

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        Category.total_products += 1
        Category.total_products += len(products)

