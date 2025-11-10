# Dashboard Q&A Benchmark - Быстрый старт

## 🎯 Что это?

Система сравнения трех фреймворков для ответов на вопросы к датасетам:
- **PandasAI** - AI агент для pandas
- **Sketch** - AI расширение для pandas  
- **LangChain Pandas Agent** - агент LangChain

**Как это работает:**
1. Загружается датасет с готовыми вопросами и ответами (benchmark)
2. Каждый фреймворк получает датасет и вопрос
3. Фреймворки возвращают ответ и рассуждение
4. Результаты сравниваются с benchmark
5. Выводится таблица с 4 ответами: benchmark + 3 фреймворка

## 🚀 Установка (3 минуты)

```bash
cd ~/dashboard-qa-benchmark
bash quickstart.sh
```

Или пошагово:

```bash
# 1. Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 2. Зависимости
# Только CLI-бенчмарки
pip install -r requirements-benchmarks.txt

# Только Streamlit-дэшборд
pip install -r requirements.txt

# Альтернатива: тот же набор зависимостей отдельным файлом
# pip install -r requirements-streamlit.txt

# 3. API ключ
cp .env.example .env
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

## 📊 Доступные датасеты

| Датасет   | Источник  | Размер      | Вопросов |
|-----------|-----------|-------------|----------|
| iris      | sklearn   | 150 × 5     | 5        |
| wine      | sklearn   | 178 × 14    | 4        |
| diabetes  | sklearn   | 442 × 11    | 3        |
| sales     | Custom    | 12 × 4      | 4        |

```bash
python main.py --list-datasets
```

## 💻 Основные команды

### Базовый запуск

```bash
python main.py --dataset iris
```

### С сохранением результатов

```bash
python main.py --dataset sales --save-results
```

### С API ключом из командной строки

```bash
python main.py --dataset wine --api-key sk-your-key-here
```

### Все опции

```bash
python main.py --help
```

## 📖 Пример вывода

```
====================================================================================================
QUESTION: How many rows are in the dataset?
====================================================================================================
+-----------+----------+------------------------------------------+------------------+
| Source    | Answer   | Reasoning                                | Match            |
+===========+==========+==========================================+==================+
| Benchmark | 150      | The Iris dataset contains 150 samples    | ✓ (Ground Truth) |
+-----------+----------+------------------------------------------+------------------+
| PandasAI  | 150      | PandasAI processed the query and retur   | ✓                |
+-----------+----------+------------------------------------------+------------------+
| Sketch    | 150      | Sketch processed the query using AI      | ✓                |
+-----------+----------+------------------------------------------+------------------+
| LangChain | 150      | LangChain agent analyzed the dataframe   | ✓                |
+-----------+----------+------------------------------------------+------------------+

====================================================================================================
SUMMARY STATISTICS
====================================================================================================
Total Questions: 5

+-----------+---------+--------+----------+
| Framework | Correct | Errors | Accuracy |
+===========+=========+========+==========+
| PandasAI  | 5/5     | 0      | 100.0%   |
+-----------+---------+--------+----------+
| Sketch    | 4/5     | 0      | 80.0%    |
+-----------+---------+--------+----------+
| LangChain | 5/5     | 0      | 100.0%   |
+-----------+---------+--------+----------+
```

## 🔧 Структура проекта

```
dashboard-qa-benchmark/
├── main.py                      # Основной скрипт
├── example_usage.py             # Примеры программного использования
├── quickstart.sh                # Скрипт быстрой установки
├── requirements-benchmarks.txt  # Зависимости для CLI-бенчмарков
├── requirements-streamlit.txt   # Зависимости для дэшборда
├── requirements.txt             # Основные зависимости Streamlit (та же подборка)
├── .env.example                 # Шаблон для API ключей
├── README.md                    # Полная документация
├── TESTING.md                   # Руководство по тестированию
│
├── src/
│   ├── benchmark_datasets.py    # Датасеты с Q&A парами
│   ├── framework_integrations.py # Интеграция фреймворков
│   └── evaluation.py            # Оценка и сравнение
│
├── data/                        # Директория данных
└── results/                     # Сохраненные результаты (JSON)
```

## 🎓 Программное использование

```python
from src.benchmark_datasets import get_benchmark_dataset
from src.framework_integrations import FrameworkManager
from src.evaluation import ResultFormatter

# Загрузить датасет
benchmark = get_benchmark_dataset('iris')
df = benchmark.get_dataset()

# Инициализировать фреймворки
manager = FrameworkManager()

# Задать вопрос
question = "How many rows?"
results = manager.query_all(df, question)

# Вывести результаты
for name, result in results.items():
    print(f"{name}: {result.answer}")
```

## 🔍 Добавление своего датасета

Отредактируйте `src/benchmark_datasets.py`:

```python
def load_my_dataset() -> BenchmarkDataset:
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c']
    })
    
    qa_pairs = [
        {
            "question": "Сколько строк?",
            "answer": "3",
            "reasoning": "Количество строк в датасете"
        }
    ]
    
    return BenchmarkDataset("MyData", df, qa_pairs)

# Добавить в реестр
AVAILABLE_DATASETS['my_data'] = load_my_dataset
```

Использовать:

```bash
python main.py --dataset my_data
```

## 🐛 Частые проблемы

### Фреймворк недоступен

```bash
pip install --upgrade pandasai langchain langchain-experimental
```

### API ключ не найден

```bash
# Проверить
echo $OPENAI_API_KEY

# Установить временно
export OPENAI_API_KEY='sk-your-key'
python main.py --dataset iris
```

### Ошибки импорта

```bash
# Убедиться что venv активен
source venv/bin/activate

# Переустановить Streamlit-зависимости
pip install -r requirements.txt --force-reinstall

# Для CLI-бенчмарков
# pip install -r requirements-benchmarks.txt --force-reinstall
```

## 📚 Документация

- **README.md** - Полная документация
- **TESTING.md** - Руководство по тестированию
- **example_usage.py** - Примеры кода

## 🎯 Следующие шаги

1. ✅ Установить и запустить на iris
2. ✅ Попробовать разные датасеты
3. ✅ Сохранить результаты
4. ✅ Добавить свой датасет
5. ✅ Интегрировать новый фреймворк

## 📞 Поддержка

Проблемы? Смотрите:
- `TESTING.md` - руководство по отладке
- `example_usage.py` - примеры использования
- GitHub Issues (если репозиторий опубликован)

---

**Лицензия:** MIT  
**Python:** 3.8+  
**Требуется:** OpenAI API key
