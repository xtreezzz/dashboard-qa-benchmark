# Dashboard Q&A Benchmark

Сравнение фреймворков для ответа на вопросы к датасетам (DataFrame Q&A).

## Описание

Этот проект сравнивает три популярных фреймворка для работы с данными через естественный язык:
- **PandasAI** - интеллектуальный агент для работы с pandas DataFrame
- **Sketch** - расширение pandas с AI возможностями
- **LangChain Pandas Agent** - агент LangChain для анализа DataFrame

Каждый фреймворк получает датасет и вопрос, возвращает ответ и рассуждение. Результаты сравниваются с benchmark ответами.

## Структура проекта

```
dashboard-qa-benchmark/
├── main.py                    # Основной скрипт
├── requirements-benchmarks.txt  # Зависимости для CLI-бенчмарков
├── requirements-streamlit.txt   # Зависимости для дашборда Streamlit
├── requirements.txt             # Основные зависимости для дашборда (идентичны requirements-streamlit.txt)
├── .env                       # API ключи (не включен в git)
├── src/
│   ├── benchmark_datasets.py  # Датасеты с Q&A парами
│   ├── framework_integrations.py  # Интеграция фреймворков
│   └── evaluation.py          # Оценка и сравнение результатов
├── data/                      # Директория для данных
└── results/                   # Результаты бенчмарков (JSON)
```

## Установка

1. Клонируйте репозиторий:
```bash
cd ~/dashboard-qa-benchmark
```

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости (выберите нужный сценарий):
```bash
# Только CLI-бенчмарки
pip install -r requirements-benchmarks.txt

# Только Streamlit-дэшборд
pip install -r requirements.txt

# Альтернативно: тот же набор зависимостей в отдельном файле
# pip install -r requirements-streamlit.txt
```

4. Настройте API ключ OpenAI:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваш OPENAI_API_KEY
```

## Доступные датасеты

Проект включает несколько benchmark датасетов с готовыми Q&A парами:

### Встроенные датасеты (sklearn)
- **iris** - Классический датасет Iris (150 образцов, 4 признака)
- **wine** - Датасет Wine (178 образцов, 13 признаков)
- **diabetes** - Датасет Diabetes (442 образца, 10 признаков)
- **sales** - Пользовательский датасет продаж (12 месяцев данных)

### Синтетические датасеты
- **ecommerce** - E-commerce транзакции (100 заказов, 9 колонок)
- **employees** - Данные о сотрудниках (50 записей, 7 колонок)

### Внешние датасеты (популярные бенчмарки)
- **titanic** - Пассажиры Титаника (100 записей, 15 колонок)
- **happiness** - World Happiness Report (20 стран, 7 колонок)
- **supermarket** - Продажи супермаркета (100 транзакций, 13 колонок)
- **covid** - COVID-19 статистика (15 стран, 8 колонок)
- **stackoverflow** - Stack Overflow Survey (80 разработчиков, 10 колонок)

📚 **Подробнее**: см. [EXTERNAL_DATASETS.md](EXTERNAL_DATASETS.md) для деталей

Список датасетов:
```bash
python main.py --list-datasets
```

## Использование

### 📊 Веб-интерфейс (Streamlit Dashboard)

**Интерактивная визуализация результатов:**

```bash
streamlit run streamlit_app.py
```

Дашборд откроется в браузере по адресу `http://localhost:8501`

**Возможности:**
- 📈 **Overview** - общая статистика и метрики
- 🔍 **Detailed Results** - детальный анализ вопросов
- 📊 **Compare Frameworks** - сравнение фреймворков
- ⏱️ **Historical Trends** - отслеживание точности во времени
- 🗂️ **Raw Data** - экспорт данных в CSV/JSON
- ⚖️ **LLM Judge** (NEW!) - умная оценка ответов через GPT-4
- 📥 **Download** (NEW!) - скачивание датасетов и логов

📚 **Подробнее**: см. [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)

### Командная строка

**Базовое использование:**

Запуск benchmark на датасете Iris:
```bash
python main.py --dataset iris
```

### С API ключом из командной строки

```bash
python main.py --dataset sales --api-key YOUR_OPENAI_API_KEY
```

### Сохранение результатов

```bash
python main.py --dataset wine --save-results
```

Результаты сохраняются в `results/` в формате JSON с временной меткой.

### Пользовательская директория для результатов

```bash
python main.py --dataset diabetes --save-results --output-dir my_results
```

### Запуск всех внешних датасетов

Можно запустить все внешние датасеты сразу:

```bash
./benchmark_external.sh
```

Или по отдельности:

```bash
python3 main.py --dataset titanic --save-results
python3 main.py --dataset happiness --save-results
python3 main.py --dataset covid --save-results
```

## Пример вывода

Для каждого вопроса выводится таблица сравнения:

```
====================================================================================================
QUESTION: What is the average sepal length?
====================================================================================================
+-----------+----------+------------------------------------------+------------------+
| Source    | Answer   | Reasoning                                | Match            |
+===========+==========+==========================================+==================+
| Benchmark | 5.843    | Mean of sepal length (cm) column         | ✓ (Ground Truth) |
+-----------+----------+------------------------------------------+------------------+
| PandasAI  | 5.843    | PandasAI processed the query and return  | ✓                |
+-----------+----------+------------------------------------------+------------------+
| Sketch    | 5.843    | Sketch processed the query using AI      | ✓                |
+-----------+----------+------------------------------------------+------------------+
| LangChain | 5.843    | LangChain agent analyzed the dataframe   | ✓                |
+-----------+----------+------------------------------------------+------------------+
```

После всех вопросов выводится сводная статистика:

```
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

## Добавление своих датасетов

Для добавления нового датасета отредактируйте `src/benchmark_datasets.py`:

```python
def load_my_benchmark() -> BenchmarkDataset:
    """Load my custom dataset with Q&A pairs."""
    df = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    })
    
    qa_pairs = [
        {
            "question": "How many rows?",
            "answer": "3",
            "reasoning": "Count of rows"
        }
    ]
    
    return BenchmarkDataset("MyDataset", df, qa_pairs)

# Добавьте в AVAILABLE_DATASETS
AVAILABLE_DATASETS = {
    ...
    'my_dataset': load_my_benchmark
}
```

## Требования

- Python 3.8+
- OpenAI API ключ
- Зависимости для Streamlit UI (`requirements.txt`) и/или CLI (`requirements-benchmarks.txt`)

## Лицензия

MIT

## Заметки

- Все три фреймворка требуют OpenAI API ключ
- PandasAI и LangChain используют GPT-4 по умолчанию
- Результаты могут варьироваться в зависимости от модели LLM
- Sketch может требовать дополнительной настройки для некоторых типов вопросов

## Устранение проблем

Если фреймворк недоступен:
1. Проверьте установку: `pip list | grep <package-name>`
2. Переустановите: `pip install --upgrade <package-name>`
3. Проверьте API ключ: `echo $OPENAI_API_KEY`

Если возникают ошибки импорта:
- Убедитесь, что виртуальное окружение активировано
- Переустановите Streamlit-зависимости: `pip install -r requirements.txt --force-reinstall`
- Для CLI-бенчмарков переустановите: `pip install -r requirements-benchmarks.txt --force-reinstall`
