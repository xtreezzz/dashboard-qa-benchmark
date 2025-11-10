# Datasets Quick Reference

Quick overview of all available benchmark datasets.

## 📊 Built-in Datasets (sklearn)

| ID | Name | Rows | Columns | Questions | Source |
|----|------|------|---------|-----------|--------|
| `iris` | Iris | 150 | 6 | 5 | sklearn |
| `wine` | Wine | 178 | 14 | 4 | sklearn |
| `diabetes` | Diabetes | 442 | 11 | 3 | sklearn |
| `sales` | Sales | 12 | 4 | 4 | Custom |

**Usage**: Classic machine learning datasets for testing

---

## 🔧 Synthetic Datasets

| ID | Name | Rows | Columns | Questions | Source |
|----|------|------|---------|-----------|--------|
| `ecommerce` | E-commerce | 100 | 9 | 5 | Generated |
| `employees` | Employees | 50 | 7 | 4 | Generated |

**Usage**: Controlled synthetic data for specific scenarios

**Details**: See [SYNTHETIC_DATASETS.md](SYNTHETIC_DATASETS.md)

---

## 🌐 External Datasets (Popular Benchmarks)

| ID | Name | Rows | Columns | Questions | Domain |
|----|------|------|---------|-----------|--------|
| `titanic` | Titanic | 100 | 15 | 5 | Transportation |
| `happiness` | World Happiness | 20 | 7 | 4 | Social Science |
| `supermarket` | Supermarket Sales | 100 | 13 | 5 | Retail |
| `covid` | COVID-19 | 15 | 8 | 4 | Healthcare |
| `stackoverflow` | Stack Overflow Survey | 80 | 10 | 4 | Technology |

**Usage**: Real-world inspired data for practical benchmarking

**Details**: See [EXTERNAL_DATASETS.md](EXTERNAL_DATASETS.md)

---

## Quick Commands

### List all datasets
```bash
python3 list_datasets.py
```

### Run a single dataset
```bash
python3 main.py --dataset <dataset_id> --save-results
```

### Run all external datasets
```bash
./benchmark_external.sh
```

### Run all datasets
```bash
for dataset in iris wine diabetes sales ecommerce employees titanic happiness supermarket covid stackoverflow; do
    python3 main.py --dataset $dataset --save-results
done
```

---

## Sample Questions by Dataset

### iris
- How many rows are in the dataset?
- What is the average sepal length?
- What is the maximum petal width?
- How many species are in the dataset?
- What is the minimum sepal width?

### titanic
- How many passengers were on the Titanic?
- How many passengers survived?
- What is the average age of passengers?
- What is the maximum fare paid?
- How many male passengers were there?

### happiness
- Which country has the highest happiness score?
- What is the average happiness score?
- How many countries are from Western Europe?
- What is the highest GDP per capita?

### covid
- What is the total number of COVID cases across all countries?
- Which country has the most COVID cases?
- What is the average recovery rate?
- How many deaths were there in the USA?

### supermarket
- What is the total sales amount?
- What is the average customer rating?
- How many sales were made at branch A?
- What is the most popular product line?
- How many payments were made in cash?

### stackoverflow
- What is the average annual salary?
- How many developers work remotely full-time?
- Which country has the most respondents?
- What is the maximum years of coding experience?

---

## Dataset Characteristics

### By Size
- **Small** (< 50 rows): `sales` (12), `happiness` (20)
- **Medium** (50-200 rows): `employees` (50), `titanic` (100), `ecommerce` (100), `supermarket` (100), `stackoverflow` (80), `iris` (150), `wine` (178)
- **Large** (> 200 rows): `diabetes` (442)

### By Complexity
- **Low**: Simple aggregations, counts
- **Medium**: Grouping, filtering, multiple conditions
- **High**: Complex analytical questions

### By Domain
- **Science**: `iris`, `wine`, `diabetes`
- **Business**: `sales`, `ecommerce`, `supermarket`
- **Social**: `happiness`, `stackoverflow`, `employees`
- **Healthcare**: `covid`, `diabetes`
- **Transportation**: `titanic`

---

## Adding New Datasets

See the following guides:
- **Synthetic datasets**: [SYNTHETIC_DATASETS.md](SYNTHETIC_DATASETS.md)
- **External datasets**: [EXTERNAL_DATASETS.md](EXTERNAL_DATASETS.md)
- **General guide**: [README.md](README.md)

---

## Performance Tips

1. **Start small**: Test with `iris` or `sales` first
2. **Use save-results**: Always save results for later analysis
3. **Batch processing**: Use `benchmark_external.sh` for multiple datasets
4. **View logs**: Use `view_logs.py` to inspect detailed framework execution
5. **Compare results**: Check `results/` directory for JSON files

---

## Total Available: 11 datasets
- 4 Built-in (sklearn)
- 2 Synthetic
- 5 External (Popular Benchmarks)
