# Testing Guide

Руководство по тестированию системы бенчмаркинга DataFrame Q&A фреймворков.

## Быстрый старт

### 1. Установка

```bash
cd ~/dashboard-qa-benchmark
bash quickstart.sh
```

Или вручную:

```bash
python3 -m venv venv
source venv/bin/activate
# Установите зависимости под сценарий тестирования
pip install -r requirements-benchmarks.txt      # CLI-бенчмарки
pip install -r requirements.txt                 # Streamlit UI и UI-тесты
# альтернативный файл со Streamlit-зависимостями
# pip install -r requirements-streamlit.txt
cp .env.example .env
# Отредактируйте .env и добавьте ваш OPENAI_API_KEY
```

### 2. Проверка установки

```bash
source venv/bin/activate
python main.py --list-datasets
```

Ожидаемый результат:
```
Available datasets:
  - iris
  - wine
  - diabetes
  - sales
```

## Тестовые сценарии

### Тест 1: Базовый запуск на Iris датасете

```bash
python main.py --dataset iris
```

**Что проверяется:**
- Загрузка датасета из sklearn
- Инициализация всех трех фреймворков
- Обработка 5 вопросов
- Сравнение с benchmark ответами
- Отображение результатов в таблицах

**Ожидаемый результат:**
- Таблица для каждого вопроса с 4 строками (Benchmark + 3 фреймворка)
- Сводная таблица с точностью каждого фреймворка
- Нет ошибок импорта или выполнения

### Тест 2: Сохранение результатов

```bash
python main.py --dataset sales --save-results
```

**Что проверяется:**
- Работа с пользовательским датасетом
- Сохранение результатов в JSON
- Создание директории results/

**Ожидаемый результат:**
- Файл `results/sales_results_YYYYMMDD_HHMMSS.json`
- JSON содержит все вопросы, ответы и сравнения

### Тест 3: Пользовательская директория

```bash
python main.py --dataset wine --save-results --output-dir my_tests
```

**Что проверяется:**
- Создание пользовательской директории
- Сохранение в указанное место

**Ожидаемый результат:**
- Файл создается в `my_tests/wine_results_*.json`

### Тест 4: Программное использование

```bash
python example_usage.py
```

**Что проверяется:**
- Программный API
- Работа с отдельными вопросами
- Кастомные датасеты

## Проверка результатов

### Формат таблицы результатов

Каждая таблица должна содержать:

```
====================================================================================================
QUESTION: [Вопрос]
====================================================================================================
+-----------+----------+------------------------------------------+------------------+
| Source    | Answer   | Reasoning                                | Match            |
+===========+==========+==========================================+==================+
| Benchmark | [Ответ]  | [Объяснение]                             | ✓ (Ground Truth) |
+-----------+----------+------------------------------------------+------------------+
| PandasAI  | [Ответ]  | [Рассуждение]                            | ✓ или ✗          |
+-----------+----------+------------------------------------------+------------------+
| Sketch    | [Ответ]  | [Рассуждение]                            | ✓ или ✗          |
+-----------+----------+------------------------------------------+------------------+
| LangChain | [Ответ]  | [Рассуждение]                            | ✓ или ✗          |
+-----------+----------+------------------------------------------+------------------+
```

### Сводная статистика

```
====================================================================================================
SUMMARY STATISTICS
====================================================================================================
Total Questions: X

+-----------+---------+--------+----------+
| Framework | Correct | Errors | Accuracy |
+===========+=========+========+==========+
| PandasAI  | X/Y     | 0      | XX.X%    |
+-----------+---------+--------+----------+
| Sketch    | X/Y     | 0      | XX.X%    |
+-----------+---------+--------+----------+
| LangChain | X/Y     | 0      | XX.X%    |
+-----------+---------+--------+----------+
```

## Отладка проблем

### Фреймворк недоступен

**Проблема:** Framework shows "✗ Not available"

**Решение:**
```bash
# Проверьте установку
pip list | grep pandasai
pip list | grep langchain
pip list | grep sketch

# Переустановите
pip install --upgrade pandasai langchain langchain-openai langchain-experimental
```

### API ключ не работает

**Проблема:** "OpenAI API key required"

**Решение:**
```bash
# Проверьте переменную окружения
echo $OPENAI_API_KEY

# Или проверьте .env файл
cat .env

# Установите временно
export OPENAI_API_KEY='your-key-here'
python main.py --dataset iris
```

### Ошибки импорта

**Проблема:** ImportError или ModuleNotFoundError

**Решение:**
```bash
# Убедитесь что venv активирован
which python
# Должно показать: /Users/family/dashboard-qa-benchmark/venv/bin/python

# Если нет, активируйте
source venv/bin/activate

# Переустановите Streamlit-зависимости
pip install -r requirements.txt --force-reinstall

# Для CLI-бенчмарков
# pip install -r requirements-benchmarks.txt --force-reinstall
```

### Неточные ответы

**Проблема:** Фреймворки дают неправильные ответы

**Причины:**
- LLM не всегда детерминирован
- Разные фреймворки используют разные промпты
- Некоторые вопросы могут быть амбигуозными

**Решение:**
- Запустите несколько раз для проверки консистентности
- Проверьте логику в benchmark_datasets.py
- Уточните формулировку вопросов

## Валидация JSON результатов

```bash
# Проверка корректности JSON
python -m json.tool results/iris_results_*.json

# Извлечение точности
python -c "
import json
with open('results/iris_results_*.json') as f:
    data = json.load(f)
    print(f'Total questions: {len(data)}')
"
```

## Метрики качества

Хорошие результаты:
- ✓ Точность > 70% для числовых вопросов
- ✓ Нет ошибок импорта или выполнения
- ✓ Время ответа < 10 секунд на вопрос
- ✓ JSON файлы валидны и содержат все поля

Требуют внимания:
- ⚠ Точность < 50%
- ⚠ Частые ошибки выполнения
- ⚠ Долгое время ответа (> 30 сек)

## Расширенное тестирование

### Добавление своих тестов

Создайте файл `test_custom.py`:

```python
import sys
import os
sys.path.insert(0, 'src')

from benchmark_datasets import get_benchmark_dataset
from framework_integrations import FrameworkManager

def test_accuracy():
    """Test framework accuracy."""
    benchmark = get_benchmark_dataset('iris')
    manager = FrameworkManager()
    
    correct = 0
    total = 0
    
    for qa_pair in benchmark.get_qa_pairs():
        results = manager.query_all(benchmark.get_dataset(), qa_pair['question'])
        
        for name, result in results.items():
            total += 1
            if not result.error and result.answer == qa_pair['answer']:
                correct += 1
    
    accuracy = correct / total * 100
    print(f"Overall accuracy: {accuracy:.1f}%")
    assert accuracy > 50, "Accuracy too low!"

if __name__ == '__main__':
    test_accuracy()
```

Запустите:
```bash
python test_custom.py
```

## Continuous Integration

Для CI/CD добавьте в `.github/workflows/test.yml`:

```yaml
name: Test Benchmarks
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements-benchmarks.txt
      # Для UI-тестов добавьте: pip install -r requirements.txt
      - run: python main.py --dataset iris
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## Заключение

После успешного прохождения всех тестов система готова к:
- Добавлению новых датасетов
- Интеграции новых фреймворков
- Развертыванию в production
- Расширению функционала
