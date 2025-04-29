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
        self._price = price
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}, {self.price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        return (self._price * self.quantity) + (other._price * other.quantity)

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
        if isinstance(product, Product) or issubclass(Smartphone, Product) or issubclass(LawnGrass, Product):
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


class Smartphone(Product):
    efficiency : int
    model: str
    memory: int
    color: str

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        if type is LawnGrass:
            return self._price * self.quantity + other.quantity + other.quantity
        raise TypeError

class LawnGrass(Product):
    country: str
    germination_period: int
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other):
        if type is LawnGrass:
            return self._price * self.quantity + other.quantity + other.quantity
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
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                             "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)

    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)

    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)

    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)

    smartphone_sum = smartphone1 + smartphone2
    print(smartphone_sum)

    grass_sum = grass1 + grass2
    print(grass_sum)

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")

    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    category_smartphones.add_product(smartphone3)

    print(category_smartphones.products)

    print(Category.product_count)

    try:
        category_smartphones.add_product("Not a product")
    except TypeError:
        print("Возникла ошибка TypeError при добавлении не продукта")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта")