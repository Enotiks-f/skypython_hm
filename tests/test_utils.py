import pytest

from src.utils import Category, Product


@pytest.fixture
def reset_category_counters():
    Category.total_categories = 0
    Category.total_products = 0


@pytest.fixture
def sample_products():
    return [
        Product("Iphone", "Apple smartphone", 1000.0, 5),
        Product("Samsung", "Android smartphone", 800.0, 3),
    ]


@pytest.fixture
def sample_category(reset_category_counters, sample_products):
    return Category("Smartphones", "Mobile devices", sample_products)


def test_product_initialization():
    product = Product("Laptop", "Gaming laptop", 2000.0, 10)
    assert product.name == "Laptop"
    assert product.description == "Gaming laptop"
    assert product.price == 2000.0
    assert product.quantity == 10


def test_category_initialization(sample_category):
    assert sample_category.name == "Smartphones"
    assert sample_category.description == "Mobile devices"
    assert isinstance(sample_category.products, list)
    assert len(sample_category.products) == 2


def test_total_categories(sample_category):
    assert Category.total_categories == 0


def test_total_products(sample_category):
    assert Category.total_products == 3
