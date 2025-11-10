# External Benchmark Datasets

This document describes publicly available benchmark datasets integrated into the system.

## Available Datasets

### 1. Titanic Dataset
**Source**: Seaborn / Kaggle  
**Description**: Famous Titanic passenger survival dataset

**Columns**:
- `survived` - 0 = No, 1 = Yes
- `pclass` - Passenger class (1, 2, 3)
- `sex` - Male/Female
- `age` - Age in years
- `sibsp` - # of siblings/spouses aboard
- `parch` - # of parents/children aboard
- `fare` - Passenger fare
- `embarked` - Port of embarkation (C, Q, S)
- `class` - Passenger class name
- `who` - man, woman, child
- `deck` - Deck letter

**Sample Questions**:
- How many passengers were on the Titanic?
- How many passengers survived?
- What is the average age of passengers?
- What is the maximum fare paid?
- How many male passengers were there?

**Usage**:
```bash
python3 main.py --dataset titanic --save-results
```

---

### 2. World Happiness Report
**Source**: Kaggle World Happiness Report (sample)  
**Description**: Happiness scores and well-being indicators by country

**Columns**:
- `Country` - Country name
- `Happiness_Score` - National average happiness score
- `GDP_per_capita` - Economic production per person
- `Social_support` - National average of social support
- `Healthy_life_expectancy` - Life expectancy
- `Freedom` - National average of freedom perception
- `Region` - Geographic region

**Sample Questions**:
- Which country has the highest happiness score?
- What is the average happiness score?
- How many countries are from Western Europe?
- What is the highest GDP per capita?

**Usage**:
```bash
python3 main.py --dataset happiness --save-results
```

---

### 3. Supermarket Sales
**Source**: Kaggle Supermarket Sales (inspired by)  
**Description**: Sales transactions from a supermarket chain

**Columns**:
- `invoice_id` - Invoice number
- `branch` - Store branch (A, B, C)
- `city` - City location
- `customer_type` - Member or Normal
- `gender` - Male/Female
- `product_line` - Product category
- `unit_price` - Price per unit
- `quantity` - Number of items
- `tax_5_percent` - 5% tax amount
- `total` - Total amount including tax
- `date` - Purchase date
- `payment` - Payment method (Cash, Credit card, Ewallet)
- `rating` - Customer rating (1-10)

**Sample Questions**:
- What is the total sales amount?
- What is the average customer rating?
- How many sales were made at branch A?
- What is the most popular product line?
- How many payments were made in cash?

**Usage**:
```bash
python3 main.py --dataset supermarket --save-results
```

---

### 4. COVID-19 Statistics
**Source**: Simplified real-world COVID data  
**Description**: COVID-19 cases, deaths, and recovery by country

**Columns**:
- `country` - Country name
- `total_cases` - Total confirmed cases
- `total_deaths` - Total deaths
- `total_recovered` - Total recovered
- `population` - Country population
- `cases_per_million` - Cases per million people
- `deaths_per_million` - Deaths per million people
- `recovery_rate` - Percentage of recoveries

**Sample Questions**:
- What is the total number of COVID cases across all countries?
- Which country has the most COVID cases?
- What is the average recovery rate?
- How many deaths were there in the USA?

**Usage**:
```bash
python3 main.py --dataset covid --save-results
```

---

### 5. Stack Overflow Developer Survey
**Source**: Inspired by Stack Overflow Annual Survey  
**Description**: Developer demographics and employment data

**Columns**:
- `respondent_id` - Unique ID
- `country` - Country of residence
- `age` - Age in years
- `years_coding` - Years of coding experience
- `employment` - Employment status
- `job_title` - Job role
- `annual_salary` - Annual salary (USD)
- `remote_work` - Remote work status (Full-time, Hybrid, Never)
- `education` - Education level
- `job_satisfaction` - Satisfaction rating (1-10)

**Sample Questions**:
- What is the average annual salary?
- How many developers work remotely full-time?
- Which country has the most respondents?
- What is the maximum years of coding experience?

**Usage**:
```bash
python3 main.py --dataset stackoverflow --save-results
```

---

## Running All External Datasets

To benchmark all external datasets at once:

```bash
python3 main.py --all-datasets --save-results
```

To benchmark only external datasets:

```bash
for dataset in titanic happiness supermarket covid stackoverflow; do
    python3 main.py --dataset $dataset --save-results
done
```

## Dataset Comparison

| Dataset | Rows | Columns | Domain | Complexity |
|---------|------|---------|--------|------------|
| Titanic | 891 | 15 | Transportation | Medium |
| World Happiness | 20 | 7 | Social Science | Low |
| Supermarket Sales | 100 | 13 | Retail | Medium |
| COVID-19 | 15 | 8 | Healthcare | Low |
| Stack Overflow | 80 | 10 | Technology | Medium |

## Adding Custom Kaggle Datasets

To add a dataset from Kaggle:

1. Install Kaggle API:
```bash
pip install --user kaggle
```

2. Set up API credentials (see https://www.kaggle.com/docs/api)

3. Download a dataset:
```bash
kaggle datasets download -d <dataset-owner>/<dataset-name>
```

4. Add a loader function in `src/external_datasets.py`

5. Add benchmark Q&A pairs in `src/benchmark_datasets.py`

6. Register the dataset in `AVAILABLE_DATASETS` dictionary

## Popular Kaggle Datasets for Q&A

Here are some popular Kaggle datasets suitable for Q&A benchmarking:

- **Titanic** - Already included
- **House Prices** - `kaggle datasets download -d c/house-prices-advanced-regression-techniques`
- **Credit Card Fraud** - `kaggle datasets download -d mlg-ulb/creditcardfraud`
- **Netflix Shows** - `kaggle datasets download -d shivamb/netflix-shows`
- **Video Game Sales** - `kaggle datasets download -d gregorut/videogamesales`
- **Olympic History** - `kaggle datasets download -d heesoo37/120-years-of-olympic-history`

## References

- Kaggle: https://www.kaggle.com/datasets
- Seaborn datasets: https://github.com/mwaskom/seaborn-data
- UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/index.php
