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
    products: list["Product"]

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        Category.total_products += 1
        Category.total_products += len(products)


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
    categories = read_json("../data/products.json")
    for category in categories:
        print("Категория:", category.name)
        for product in category.products:
            print(f"  - {product.name}: {product.price}₽")