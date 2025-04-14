# 📦 Категории и Товары

Проект реализует базовую систему управления категориями и товарами с помощью Python-классов. Это может быть полезно для создания интернет-магазина, каталога товаров и т.д.

---

## 🧩 Класс

### 🛍️ `Product`

Класс для представления отдельного товара.

#### Атрибуты экземпляра:
- `name` (`str`) — название товара.
- `description` (`str`) — описание товара.
- `price` (`float`) — цена товара.
- `quantity` (`int`) — количество товара на складе.

#### Пример:
```
product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
```

---

## 🧩 Класс

### 🛍️ `Category`

#### Атрибуты экземпляра:
- `name` (`str`) — название категории.
- `description` (`str`) — описание категории.
- `products` (`list[Product]`) - список объектов `Product`.

#### Классовые атрибуты:
- `total_categories` (`int`) - количество созданных объектов `Categories`
- `total_products` (`int`) - количество всех товаров (суммарно по количеству из всех категорий).

```
category = Category("Смартфоны", "Современные смартфоны", [product1, product2])
```

---

## 📁 Структура проекта

```project/
├── src/
│   └── utils.py          # Содержит классы Product и Category
├── data/
│   └── data.json         # JSON-файл с товарами
├── tests/
│   └── test_utils.py     # Тесты
└── README.md             # Документация (этот файл)
```

---

## 📖 Использование

Пример чтения данных из JSON и создания объектов:
```python   
from src.utils import Category, Product
import json

def read_json(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

data = read_json("data/data.json")

categories = []
for cat_data in data:
    products = [
        Product(prod["name"], prod["description"], prod["price"], prod["quantity"])
        for prod in cat_data["products"]
    ]
    category = Category(cat_data["name"], cat_data["description"], products)
    categories.append(category)
```

## 🧪 Тестирование

Тесты написаны с использованием pytest.

Запуск тестов:
```
pytest tests/
```

