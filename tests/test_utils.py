import json
import unittest
from unittest.mock import mock_open, patch

from skypython_hm.src.utils import (Category, CategoryIterator, LawnGrass,
                                    Product, Smartphone, read_json)


# Тесты для Product
def test_product_initialization():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 1000.0
    assert product.quantity == 10


def test_new_product_classmethod():
    data = {
        "name": "New Product",
        "description": "New Description",
        "price": 500.0,
        "quantity": 5,
    }
    product = Product.new_product(data)
    assert product.name == "New Product"
    assert product.description == "New Description"
    assert product.price == 500.0
    assert product.quantity == 5


def test_price_setter_positive():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    product.price = 2000.0
    assert product.price == 2000.0


def test_price_setter_negative():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    with patch("builtins.print") as mocked_print:
        product.price = -100.0
        mocked_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 1000.0


def test_price_setter_zero():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    with patch("builtins.print") as mocked_print:
        product.price = 0
        mocked_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 1000.0


def test_price_setter_lower_price_accepted():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    with patch("builtins.input", return_value="y"):
        product.price = 500.0
        assert product.price == 500.0


def test_price_setter_lower_price_rejected():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    with patch("builtins.input", return_value="n"):
        with patch("builtins.print") as mocked_print:
            product.price = 500.0
            mocked_print.assert_called_with("Изменения не применены")
            assert product.price == 1000.0


# Тесты для Category
def test_category_initialization():
    # Сброс product_count перед тестом
    Category.product_count = 0
    product1 = Product("Product 1", "Desc 1", 1000.0, 5)
    product2 = Product("Product 2", "Desc 2", 2000.0, 10)
    category = Category("Test Category", "Test Description", [product1, product2])
    assert category.name == "Test Category"
    assert category.description == "Test Description"
    assert len(category._Category__products) == 2
    assert Category.product_count == 2


def test_add_product():
    # Сброс product_count перед тестом
    Category.product_count = 0
    product1 = Product("Product 1", "Desc 1", 1000.0, 5)
    category = Category("Test Category", "Test Description", [product1])
    new_product = Product("Product 2", "Desc 2", 2000.0, 10)
    category.add_product(new_product)
    assert len(category._Category__products) == 2
    assert Category.product_count == 2  # 1 (изначально) + 1 (добавлен)


def test_add_non_product():
    # Сброс product_count перед тестом
    Category.product_count = 0
    product1 = Product("Product 1", "Desc 1", 1000.0, 5)
    category = Category("Test Category", "Test Description", [product1])
    initial_count = len(category._Category__products)
    category.add_product("Not a product")
    assert len(category._Category__products) == initial_count
    assert Category.product_count == 1  # Только 1 продукт изначально


def test_products_property():
    # Сброс product_count перед тестом
    Category.product_count = 0
    product1 = Product("Product 1", "Desc 1", 1000.0, 5)
    product2 = Product("Product 2", "Desc 2", 2000.0, 10)
    category = Category("Test Category", "Test Description", [product1, product2])
    expected_output = (
        "Product 1, 1000.0 руб. Остаток: 5 шт.\n"
        "Product 2, 2000.0 руб. Остаток: 10 шт."
    )
    assert category.products == expected_output


# Тесты для read_json
def test_read_json():
    # Сброс product_count перед тестом
    Category.product_count = 0
    mock_data = [
        {
            "name": "Category 1",
            "description": "Desc 1",
            "products": [
                {
                    "name": "Product 1",
                    "description": "P Desc 1",
                    "price": 1000.0,
                    "quantity": 5,
                },
                {
                    "name": "Product 2",
                    "description": "P Desc 2",
                    "price": 2000.0,
                    "quantity": 10,
                },
            ],
        }
    ]
    mock_file = mock_open(read_data=json.dumps(mock_data))
    with patch("builtins.open", mock_file):
        categories = read_json("dummy_path.json")

    assert len(categories) == 1
    assert categories[0].name == "Category 1"
    assert categories[0].description == "Desc 1"
    assert len(categories[0]._Category__products) == 2
    assert categories[0]._Category__products[0].name == "Product 1"
    assert categories[0]._Category__products[1].price == 2000.0


def test_category_iterator():
    Category.product_count = 0
    product1 = Product("Product 1", "Desc 1", 100.0, 2)
    product2 = Product("Product 2", "Desc 2", 200.0, 5)
    category = Category("Test Category", "Test Description", [product1, product2])

    iterator = CategoryIterator(category)

    products = list(iterator)

    assert len(products) == 2
    assert products[0].name == "Product 1"
    assert products[1].name == "Product 2"


def test_category_iterator_stop_iteration():
    Category.product_count = 0
    product1 = Product("Product 1", "Desc 1", 100.0, 2)
    category = Category("Test Category", "Test Description", [product1])

    iterator = CategoryIterator(category)
    next(iterator)
    try:
        next(iterator)
        assert False, "Ожидалось исключение StopIteration"
    except StopIteration:
        pass


def test_add_products():
    Category.product_count = 0
    category = Category("Test", "Desc", [])
    product = Product("Product", "Desc", 100.0, 1)
    category.add_product(product)
    assert product in category.product_list
    assert Category.product_count == 1


def test_add_invalid_product():
    category = Category("Test", "Desc", [])
    initial_count = Category.product_count
    category.add_product("NotAProduct")
    # Не выбрасывается исключение, но и не добавляется
    assert len(category.product_list) == 0
    assert Category.product_count == initial_count


def test_category_products_property():
    p1 = Product("P1", "D1", 100, 1)
    p2 = Product("P2", "D2", 200, 2)
    category = Category("Cat", "Desc", [p1, p2])
    result = category.products
    assert "P1, 100 руб." in result
    assert "P2, 200 руб." in result


# Тесты для CategoryIterator
def test_category_iterators():
    p1 = Product("P1", "D1", 100, 1)
    p2 = Product("P2", "D2", 200, 2)
    category = Category("Cat", "Desc", [p1, p2])
    iterator = iter(CategoryIterator(category))
    assert next(iterator) == p1
    assert next(iterator) == p2
    try:
        next(iterator)
        assert False  # должно быть исключение StopIteration
    except StopIteration:
        assert True


# Тесты для Smartphone
def test_smartphone_initialization():
    phone = Smartphone("Phone", "Desc", 1000, 3, 99, "Model", 256, "Black")
    assert phone.name == "Phone"
    assert phone.efficiency == 99
    assert phone.model == "Model"
    assert phone.memory == 256
    assert phone.color == "Black"


# Тесты для LawnGrass
def test_lawngrass_initialization():
    grass = LawnGrass("Grass", "Desc", 300, 5, "Russia", "7 дней", "Green")
    assert grass.name == "Grass"
    assert grass.country == "Russia"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Green"


# Тесты для read_json
def test_read_json_parses_correctly():
    mock_data = json.dumps(
        [
            {
                "name": "Category1",
                "description": "Desc1",
                "products": [
                    {
                        "name": "Prod1",
                        "description": "D1",
                        "price": 10.0,
                        "quantity": 1,
                    },
                    {
                        "name": "Prod2",
                        "description": "D2",
                        "price": 20.0,
                        "quantity": 2,
                    },
                ],
            }
        ]
    )

    with patch("builtins.open", mock_open(read_data=mock_data)):
        categories = read_json("fakepath.json")
        assert len(categories) == 1
        assert categories[0].name == "Category1"
        assert len(categories[0].product_list) == 2
        assert categories[0].product_list[0].name == "Prod1"


# Проверка на сложение продуктов
def test_product_addition():
    p1 = Product("A", "D", 10.0, 2)
    p2 = Product("B", "D", 15.0, 3)
    total = p1 + p2
    assert total == 10.0 * 2 + 15.0 * 3


def test_invalid_addition_between_different_types():
    phone = Smartphone("Phone", "Desc", 1000, 2, 90, "M1", 128, "Black")
    grass = LawnGrass("Grass", "Desc", 300, 5, "RU", "7 days", "Green")
    try:
        assert phone + grass
    except TypeError:
        assert True
    else:
        assert False, "Ожидалась ошибка TypeError при сложении разных типов"


if __name__ == "__main__":
    unittest.main()
