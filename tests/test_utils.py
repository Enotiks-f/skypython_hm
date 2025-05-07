import json
import unittest
from unittest.mock import mock_open, patch
from skypython_hm.src.utils import (Category, CategoryIterator, LawnGrass,
                                    Product, Smartphone, read_json)

# Тесты для Product
class TestProduct(unittest.TestCase):

    def test_product_initialization(self):
        product = Product("Test Product", "Test Description", 1000.0, 10)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test Description")
        self.assertEqual(product.price, 1000.0)
        self.assertEqual(product.quantity, 10)

    def test_new_product_classmethod(self):
        data = {
            "name": "New Product",
            "description": "New Description",
            "price": 500.0,
            "quantity": 5,
        }
        product = Product.new_product(data)
        self.assertEqual(product.name, "New Product")
        self.assertEqual(product.description, "New Description")
        self.assertEqual(product.price, 500.0)
        self.assertEqual(product.quantity, 5)

    def test_price_setter_positive(self):
        product = Product("Test Product", "Test Description", 1000.0, 10)
        product.price = 2000.0
        self.assertEqual(product.price, 2000.0)

    def test_price_setter_negative(self):
        product = Product("Test Product", "Test Description", 1000.0, 10)
        with patch("builtins.print") as mocked_print:
            product.price = -100.0
            mocked_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
            self.assertEqual(product.price, 1000.0)

    def test_price_setter_zero(self):
        product = Product("Test Product", "Test Description", 1000.0, 10)
        with patch("builtins.print") as mocked_print:
            product.price = 0
            mocked_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
            self.assertEqual(product.price, 1000.0)

    def test_price_setter_lower_price_accepted(self):
        product = Product("Test Product", "Test Description", 1000.0, 10)
        with patch("builtins.input", return_value="y"):
            product.price = 500.0
            self.assertEqual(product.price, 500.0)

    def test_price_setter_lower_price_rejected(self):
        product = Product("Test Product", "Test Description", 1000.0, 10)
        with patch("builtins.input", return_value="n"):
            with patch("builtins.print") as mocked_print:
                product.price = 500.0
                mocked_print.assert_called_with("Изменения не применены")
                self.assertEqual(product.price, 1000.0)


# Тесты для Category
class TestCategory(unittest.TestCase):

    def test_category_initialization(self):
        Category.product_count = 0
        product1 = Product("Product 1", "Desc 1", 1000.0, 5)
        product2 = Product("Product 2", "Desc 2", 2000.0, 10)
        category = Category("Test Category", "Test Description", [product1, product2])
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test Description")
        self.assertEqual(len(category._Category__products), 2)
        self.assertEqual(Category.product_count, 2)

    def test_add_product(self):
        Category.product_count = 0
        product1 = Product("Product 1", "Desc 1", 1000.0, 5)
        category = Category("Test Category", "Test Description", [product1])
        new_product = Product("Product 2", "Desc 2", 2000.0, 10)
        category.add_product(new_product)
        self.assertEqual(len(category._Category__products), 2)
        self.assertEqual(Category.product_count, 2)


    def test_products_property(self):
        Category.product_count = 0
        product1 = Product("Product 1", "Desc 1", 1000.0, 5)
        product2 = Product("Product 2", "Desc 2", 2000.0, 10)
        category = Category("Test Category", "Test Description", [product1, product2])
        expected_output = (
            "Product 1, 1000.0 руб. Остаток: 5 шт.\n"
            "Product 2, 2000.0 руб. Остаток: 10 шт."
        )
        self.assertEqual(category.products, expected_output)


# Тесты для read_json
class TestReadJson(unittest.TestCase):

    def test_read_json(self):
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

        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].name, "Category 1")
        self.assertEqual(categories[0].description, "Desc 1")
        self.assertEqual(len(categories[0]._Category__products), 2)
        self.assertEqual(categories[0]._Category__products[0].name, "Product 1")
        self.assertEqual(categories[0]._Category__products[1].price, 2000.0)


# Тесты для CategoryIterator
class TestCategoryIterator(unittest.TestCase):

    def test_category_iterator(self):
        Category.product_count = 0
        product1 = Product("Product 1", "Desc 1", 100.0, 2)
        product2 = Product("Product 2", "Desc 2", 200.0, 5)
        category = Category("Test Category", "Test Description", [product1, product2])

        iterator = CategoryIterator(category)

        products = list(iterator)

        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].name, "Product 1")
        self.assertEqual(products[1].name, "Product 2")

    def test_category_iterator_stop_iteration(self):
        Category.product_count = 0
        product1 = Product("Product 1", "Desc 1", 100.0, 2)
        category = Category("Test Category", "Test Description", [product1])

        iterator = CategoryIterator(category)
        next(iterator)
        with self.assertRaises(StopIteration):
            next(iterator)


# Тесты для Add Products (метод add_product)
class TestAddProductMethod(unittest.TestCase):

    def test_add_multiple_products(self):
        Category.product_count = 0
        product1 = Product("Product 1", "Desc 1", 1000.0, 5)
        product2 = Product("Product 2", "Desc 2", 2000.0, 10)
        category = Category("Test Category", "Test Description", [product1])

        category.add_product(product2)
        self.assertEqual(len(category._Category__products), 2)
        self.assertEqual(Category.product_count, 2)


# Тесты для других классов
class TestLawnGrassAndSmartphone(unittest.TestCase):

    def test_lawn_grass_addition(self):
        lawn_grass1 = LawnGrass("Lawn 1", "Premium Grass", 1500.0, 10, "USA", 15, "Green")
        lawn_grass2 = LawnGrass("Lawn 2", "Standard Grass", 800.0, 15, "Russia", 10, "Green")
        self.assertEqual(lawn_grass1 + lawn_grass2, 15030.0)

if __name__ == "__main__":
    unittest.main()
