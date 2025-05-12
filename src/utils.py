from abc import ABC, abstractmethod
import json
from itertools import product

from unicodedata import category


class BaseProduct(ABC):
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class MixinMro:

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        print(f"{self.__class__.__name__}")

    def __repr__(self):
        return f"{self.__class__.__name__}, ({self.name}, {self.description}, {self.price}, {self.quantity})"


class Product(BaseProduct, MixinMro):
    def __init__(self, name, description, price, quantity):
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, data: dict):
        return cls(data["name"], data["description"], data["price"], data["quantity"])

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):

        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self._price:
            ans = input("Новая цена ниже старый, вы уверены в изменение цены (y/n?)")
            if ans == "y":
                self._price = new_price
            else:
                print("Изменения не применены")
        else:
            self._price = new_price


class BaseOrderCategory(ABC):
    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Order(BaseOrderCategory):
    def __init__(self, quantity, product: "Product", total_price):
        self.product = product
        self.quantity = quantity

    def get_total_price(self):
        return self.product.price * self.quantity

    def get_items(self):
        return [self.product]

    def __str__(self):
        return f"Заказ: {self.product.name}, кол-во: {self.quantity}, на сумму: {self.quantity * self.product.price}"



class Category(BaseOrderCategory):
    category_count = 0
    product_count = 0

    name: str
    description: str
    products: list["Product"]

    def __init__(self, name, description, products):
        self._products = products
        self.name = name
        self.description = description

        Category.product_count += len(products)

    def get_items(self):
        return [self._products]

    def add_product(self, product):
        if isinstance(product, Product):
            self._products.append(product)
            Category.product_count += 1

    @property
    def products(self):
        result = []
        for product in self._products:
            result.append(
                f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            )
        return "\n".join(result)

    @property
    def product_list(self):
        return self._products

    def __str__(self):
        return f"{self.name}, количество продуктов: {Product.quantity}."

    def middle_price(self):
        count = 0
        try:
            for i in self._products:
                count += i.price
            return count / len(self._products)
        except ZeroDivisionError as o:
            return 0

class Smartphone(Product):
    efficiency: int
    model: str
    memory: int
    color: str

    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        if type(other) is LawnGrass:
            return self.price * self.quantity + other.price * other.quantity
        raise TypeError


class LawnGrass(Product):
    country: str
    germination_period: int
    color: str

    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other):
        if type(other) is LawnGrass:
            return self.price * self.quantity + other.price * other.quantity
        raise TypeError


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


if __name__ == "__main__":
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())