# Руководство по просмотру логов

## 📋 Что логируется

Каждый фреймворк теперь сохраняет подробные логи выполнения:

### PandasAI
- Время начала и завершения
- Вопрос и размер DataFrame
- Процесс генерации кода
- Промпты отправленные в LLM
- Сгенерированный Python код
- Результат выполнения

### Sketch
- Время начала и завершения
- Статистическая сводка данных
- Промпт отправленный в OpenAI
- Ответ от API

### LangChain
- Время начала и завершения
- Размер DataFrame и колонки
- Процесс мышления агента (Thought)
- Действия агента (Action)
- Выполненный Python код
- Промежуточные результаты
- Финальный ответ

## 🔍 Просмотр логов

### Способ 1: Через view_logs.py (рекомендуется)

```bash
# Просмотр всех вопросов и всех фреймворков
python3 view_logs.py results/iris_results_20251108_214147.json

# Просмотр конкретного вопроса
python3 view_logs.py results/sales_results_20251108_214522.json --question 0

# Просмотр конкретного фреймворка
python3 view_logs.py results/iris_results_20251108_214147.json --framework LangChain

# Просмотр конкретного вопроса и фреймворка
python3 view_logs.py results/sales_results_20251108_214522.json -q 1 -f PandasAI
```

### Способ 2: Через JSON напрямую

```bash
# Красивый вывод JSON
python3 -m json.tool results/iris_results_20251108_214147.json

# Извлечь логи конкретного фреймворка
python3 -c "
import json
with open('results/sales_results_20251108_214522.json') as f:
    data = json.load(f)
    print(data[0]['framework_results']['LangChain']['logs'])
"
```

### Способ 3: Программно

```python
import json

# Загрузить результаты
with open('results/iris_results_20251108_214147.json') as f:
    results = json.load(f)

# Просмотреть логи первого вопроса для LangChain
question_0 = results[0]
langchain_logs = question_0['framework_results']['LangChain']['logs']
print(langchain_logs)

# Найти все ошибки
for i, result in enumerate(results):
    for framework, data in result['framework_results'].items():
        if data['error']:
            print(f"Question {i}, {framework}: {data['error']}")
            print(f"Logs: {data['logs']}")
```

## 📊 Структура JSON с логами

```json
{
  "question": "What is the total revenue?",
  "benchmark": {
    "question": "What is the total revenue?",
    "answer": "196000",
    "reasoning": "Sum of all revenue values"
  },
  "framework_results": {
    "PandasAI": {
      "answer": "196000.0",
      "reasoning": "PandasAI processed the query and returned the result",
      "error": "",
      "logs": "[2025-11-08T21:45:08.689820] Starting PandasAI query\n..."
    },
    "Sketch": {
      "answer": "Total revenue: 196000",
      "reasoning": "Sketch-style analysis with statistical summary and sampling",
      "error": "",
      "logs": "[2025-11-08T21:45:10.350466] Starting Sketch query\n..."
    },
    "LangChain": {
      "answer": "The total revenue is 196000.",
      "reasoning": "LangChain Pandas Agent analyzed the dataframe using Python code execution",
      "error": "",
      "logs": "[2025-11-08T21:45:11.146065] Starting LangChain Pandas Agent query\n..."
    }
  }
}
```

## 🐛 Отладка проблем

### Если фреймворк дает неправильный ответ:

1. Посмотрите логи через view_logs.py:
```bash
python3 view_logs.py results/sales_results_20251108_214522.json -q 0 -f PandasAI
```

2. Проверьте:
   - Какой промпт был отправлен?
   - Какой код был сгенерирован?
   - Были ли ошибки в выполнении?
   - Какие промежуточные результаты?

### Примеры отладки:

**Проблема: PandasAI дает неправильный ответ**
```bash
# Смотрим логи
python3 view_logs.py results/sales_results_20251108_214522.json -q 0 -f PandasAI

# В логах видим сгенерированный код:
# df['revenue'].head().sum()  # ОШИБКА: суммирует только первые 5 строк!
# Правильно: df['revenue'].sum()
```

**Проблема: LangChain выдает ошибку**
```bash
# Смотрим полные логи с ошибкой
python3 view_logs.py results/iris_results_20251108_214147.json -q 2 -f LangChain

# В логах видим:
# [ERROR] KeyError: 'column_name'
# Агент пытался обратиться к несуществующей колонке
```

**Проблема: Sketch дает неточный ответ**
```bash
# Смотрим промпт
python3 view_logs.py results/sales_results_20251108_214522.json -q 1 -f Sketch

# Видим что Sketch использует только статистику (min, max, mean)
# но не видит полные данные - поэтому может ошибаться
```

## 💡 Полезные команды

```bash
# Найти все результаты
ls -lh results/

# Последний результат
ls -t results/*.json | head -1

# Просмотреть последний результат
python3 view_logs.py $(ls -t results/*.json | head -1)

# Сравнить ответы всех фреймворков для вопроса 0
python3 view_logs.py results/iris_results_20251108_214147.json -q 0

# Сохранить логи в файл
python3 view_logs.py results/sales_results_20251108_214522.json -q 0 -f LangChain > langchain_log_q0.txt
```

## 📈 Анализ производительности

```python
import json
from datetime import datetime

with open('results/iris_results_20251108_214147.json') as f:
    results = json.load(f)

# Извлечь время выполнения из логов
for i, result in enumerate(results):
    print(f"\nQuestion {i+1}:")
    for framework, data in result['framework_results'].items():
        logs = data['logs']
        # Найти строки с timestamp
        lines = [l for l in logs.split('\n') if 'Starting' in l or 'Completed' in l]
        if len(lines) >= 2:
            # Вычислить время выполнения
            print(f"  {framework}: execution logged")
```

## 🎯 Рекомендации

1. **Всегда сохраняйте результаты** с `--save-results` для последующего анализа
2. **Используйте view_logs.py** для быстрого просмотра
3. **Смотрите логи при неправильных ответах** для понимания причин
4. **Сохраняйте интересные логи** в отдельные файлы для документации
5. **Анализируйте паттерны ошибок** между фреймворками

## ⚙️ Настройка логирования

Логирование включено по умолчанию. Логи захватывают:
- stdout/stderr для PandasAI и LangChain
- Промпты и ответы для Sketch
- Timestamp для всех операций
- Все ошибки и traceback

Логи НЕ выводятся в консоль во время выполнения, но сохраняются в JSON.
