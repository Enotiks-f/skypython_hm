import unittest
import json
from unittest.mock import mock_open, patch
from src.utils import Product, Category, read_json


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
        "quantity": 5
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
    with patch('builtins.print') as mocked_print:
        product.price = -100.0
        mocked_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 1000.0


def test_price_setter_zero():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    with patch('builtins.print') as mocked_print:
        product.price = 0
        mocked_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
        assert product.price == 1000.0


def test_price_setter_lower_price_accepted():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    with patch('builtins.input', return_value='y'):
        product.price = 500.0
        assert product.price == 500.0


def test_price_setter_lower_price_rejected():
    product = Product("Test Product", "Test Description", 1000.0, 10)
    with patch('builtins.input', return_value='n'):
        with patch('builtins.print') as mocked_print:
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
                {"name": "Product 1", "description": "P Desc 1", "price": 1000.0, "quantity": 5},
                {"name": "Product 2", "description": "P Desc 2", "price": 2000.0, "quantity": 10}
            ]
        }
    ]
    mock_file = mock_open(read_data=json.dumps(mock_data))
    with patch('builtins.open', mock_file):
        categories = read_json("dummy_path.json")

    assert len(categories) == 1
    assert categories[0].name == "Category 1"
    assert categories[0].description == "Desc 1"
    assert len(categories[0]._Category__products) == 2
    assert categories[0]._Category__products[0].name == "Product 1"
    assert categories[0]._Category__products[1].price == 2000.0


if __name__ == '__main__':
    unittest.main()