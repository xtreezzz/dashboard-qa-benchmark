# Synthetic Datasets

Система включает несколько синтетических датасетов для расширенного тестирования фреймворков.

## 📊 Доступные синтетические датасеты

### 1. E-commerce (ecommerce)

**Описание:** Данные об онлайн-заказах интернет-магазина

**Размер:** 100 строк × 9 колонок

**Колонки:**
- `order_id` - ID заказа
- `customer_id` - ID клиента  
- `product_category` - Категория товара (Electronics, Clothing, Home & Garden, Sports, Books)
- `quantity` - Количество
- `price` - Цена за единицу
- `order_date` - Дата заказа
- `region` - Регион (North, South, East, West, Central)
- `payment_method` - Способ оплаты (Credit Card, PayPal, Cash, Debit Card)
- `total_amount` - Общая сумма заказа

**Вопросы (5):**
1. What is the total revenue from all orders?
2. What is the average order value?
3. How many orders were placed?
4. What is the most popular product category?
5. What is the maximum order amount?

**Запуск:**
```bash
python3 main.py --dataset ecommerce --save-results
```

**Результаты тестирования:**
- PandasAI: 100% (5/5)
- Sketch: 80% (4/5)
- LangChain: 100% (5/5)

---

### 2. Employees (employees)

**Описание:** Данные о сотрудниках компании

**Размер:** 50 строк × 7 колонок

**Колонки:**
- `employee_id` - ID сотрудника
- `name` - Имя
- `department` - Отдел (Engineering, Sales, Marketing, HR, Finance)
- `salary` - Зарплата
- `years_experience` - Лет опыта
- `performance_rating` - Рейтинг производительности (2.5-5.0)
- `is_remote` - Работает удаленно (True/False)

**Вопросы (4):**
1. What is the average salary?
2. What is the highest salary?
3. How many employees are in Engineering?
4. How many employees work remotely?

**Запуск:**
```bash
python3 main.py --dataset employees --save-results
```

**Результаты тестирования:**
- PandasAI: 100% (4/4)
- Sketch: 75% (3/4)
- LangChain: 75% (3/4)

---

## 🔧 Дополнительные генераторы

В файле `src/synthetic_generator.py` есть дополнительные генераторы, которые можно легко добавить:

### Stock Trading Data
```python
from src.synthetic_generator import generate_stock_dataset
df = generate_stock_dataset(n_rows=60, seed=42)
```

**Колонки:** date, ticker, open_price, close_price, high, low, volume

### Customer Churn Data
```python
from src.synthetic_generator import generate_customer_churn_dataset
df = generate_customer_churn_dataset(n_rows=80, seed=42)
```

**Колонки:** customer_id, age, tenure_months, monthly_charges, total_charges, contract_type, churned

### Weather Data
```python
from src.synthetic_generator import generate_weather_dataset
df = generate_weather_dataset(n_rows=90, seed=42)
```

**Колонки:** date, city, temperature, humidity, precipitation, wind_speed, condition

## 📝 Добавление своего датасета

### Шаг 1: Создайте генератор в `src/synthetic_generator.py`

```python
def generate_custom_dataset(n_rows=50, seed=42):
    """Generate your custom dataset."""
    np.random.seed(seed)
    
    data = {
        'id': range(n_rows),
        'value': np.random.randint(1, 100, n_rows),
        # ... добавьте свои колонки
    }
    
    return pd.DataFrame(data)
```

### Шаг 2: Добавьте в `src/benchmark_datasets.py`

```python
def load_custom_benchmark() -> BenchmarkDataset:
    """Load custom dataset with Q&A pairs."""
    from synthetic_generator import generate_custom_dataset
    
    df = generate_custom_dataset(n_rows=50, seed=42)
    
    # Вычислите правильные ответы
    total = df['value'].sum()
    
    qa_pairs = [
        {
            "question": "What is the total value?",
            "answer": str(total),
            "reasoning": f"Sum of values: {total}"
        }
    ]
    
    return BenchmarkDataset("Custom", df, qa_pairs)

# Добавьте в реестр
AVAILABLE_DATASETS = {
    ...
    'custom': load_custom_benchmark
}
```

### Шаг 3: Запустите тест

```bash
python3 main.py --dataset custom --save-results
```

## 🎯 Преимущества синтетических данных

1. **Контролируемость** - известны точные правильные ответы
2. **Воспроизводимость** - seed гарантирует одинаковые данные
3. **Разнообразие** - разные типы данных и вопросов
4. **Масштабируемость** - легко генерировать любой размер
5. **Безопасность** - нет реальных чувствительных данных

## 📊 Сравнительные результаты

| Датасет | Строк | Вопросов | PandasAI | Sketch | LangChain |
|---------|-------|----------|----------|---------|-----------|
| Iris | 150 | 5 | 100% | 100% | 100% |
| Wine | 178 | 4 | - | - | - |
| Diabetes | 442 | 3 | - | - | - |
| Sales | 12 | 4 | 75% | 75% | 75% |
| **E-commerce** | 100 | 5 | **100%** | **80%** | **100%** |
| **Employees** | 50 | 4 | **100%** | **75%** | **75%** |

## 💡 Рекомендации по использованию

1. **Для тестирования новых фреймворков** - используйте все синтетические датасеты
2. **Для отладки** - начните с маленьких датасетов (employees, sales)
3. **Для стресс-тестов** - используйте большие датасеты (ecommerce с n_rows=1000)
4. **Для разнообразия** - комбинируйте разные типы данных (числовые, категориальные, даты)

## 🔍 Просмотр сгенерированных данных

```bash
# Просмотр структуры датасета
python3 demo.py

# Тестовый запуск
python3 -c "
import sys
sys.path.insert(0, 'src')
from synthetic_generator import generate_ecommerce_dataset
df = generate_ecommerce_dataset(n_rows=10)
print(df.head())
print(df.info())
"
```

## 🚀 Расширенное использование

### Генерация нескольких датасетов
```bash
# Запустить все синтетические датасеты
for dataset in ecommerce employees; do
    python3 main.py --dataset $dataset --save-results
done
```

### Изменение seed для разных данных
```python
# В synthetic_generator.py измените seed
df = generate_ecommerce_dataset(n_rows=100, seed=123)  # Новые данные!
```

### Увеличение размера для стресс-теста
```python
# Генерация большого датасета
df = generate_ecommerce_dataset(n_rows=10000, seed=42)
```
