"""
Benchmark datasets with predefined questions and answers.
"""
import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_diabetes
from typing import Dict, List, Tuple, Any


class BenchmarkDataset:
    """Base class for benchmark datasets."""
    
    def __init__(self, name: str, df: pd.DataFrame, qa_pairs: List[Dict[str, Any]]):
        self.name = name
        self.df = df
        self.qa_pairs = qa_pairs
    
    def get_dataset(self) -> pd.DataFrame:
        return self.df
    
    def get_qa_pairs(self) -> List[Dict[str, Any]]:
        return self.qa_pairs


def load_iris_benchmark() -> BenchmarkDataset:
    """Load Iris dataset with benchmark Q&A pairs."""
    iris = load_iris()
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['species'] = iris.target
    df['species_name'] = df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
    
    qa_pairs = [
        {
            "question": "How many rows are in the dataset?",
            "answer": "150",
            "reasoning": "The Iris dataset contains 150 samples"
        },
        {
            "question": "What is the average sepal length?",
            "answer": "5.843",
            "reasoning": "Mean of sepal length (cm) column rounded to 3 decimals"
        },
        {
            "question": "What is the maximum petal width?",
            "answer": "2.5",
            "reasoning": "Maximum value in petal width (cm) column"
        },
        {
            "question": "How many species are in the dataset?",
            "answer": "3",
            "reasoning": "Three species: setosa, versicolor, and virginica"
        },
        {
            "question": "What is the minimum sepal width?",
            "answer": "2.0",
            "reasoning": "Minimum value in sepal width (cm) column"
        }
    ]
    
    return BenchmarkDataset("Iris", df, qa_pairs)


def load_wine_benchmark() -> BenchmarkDataset:
    """Load Wine dataset with benchmark Q&A pairs."""
    wine = load_wine()
    df = pd.DataFrame(
        data=wine.data,
        columns=wine.feature_names
    )
    df['target'] = wine.target
    
    qa_pairs = [
        {
            "question": "How many samples are in the dataset?",
            "answer": "178",
            "reasoning": "The Wine dataset contains 178 samples"
        },
        {
            "question": "What is the average alcohol content?",
            "answer": "13.000",
            "reasoning": "Mean of alcohol column rounded to 3 decimals"
        },
        {
            "question": "What is the maximum malic acid value?",
            "answer": "5.8",
            "reasoning": "Maximum value in malic_acid column"
        },
        {
            "question": "How many features are in the dataset?",
            "answer": "13",
            "reasoning": "The dataset has 13 feature columns (excluding target)"
        }
    ]
    
    return BenchmarkDataset("Wine", df, qa_pairs)


def load_diabetes_benchmark() -> BenchmarkDataset:
    """Load Diabetes dataset with benchmark Q&A pairs."""
    diabetes = load_diabetes()
    df = pd.DataFrame(
        data=diabetes.data,
        columns=diabetes.feature_names
    )
    df['target'] = diabetes.target
    
    qa_pairs = [
        {
            "question": "How many patients are in the dataset?",
            "answer": "442",
            "reasoning": "The Diabetes dataset contains 442 samples"
        },
        {
            "question": "What is the mean target value?",
            "answer": "152.133",
            "reasoning": "Mean of target column rounded to 3 decimals"
        },
        {
            "question": "How many columns are in the dataset?",
            "answer": "11",
            "reasoning": "10 feature columns plus 1 target column"
        }
    ]
    
    return BenchmarkDataset("Diabetes", df, qa_pairs)


def load_custom_sales_benchmark() -> BenchmarkDataset:
    """Load a custom sales dataset with benchmark Q&A pairs."""
    data = {
        'date': pd.date_range('2024-01-01', periods=12, freq='M'),
        'revenue': [10000, 12000, 11000, 15000, 14000, 16000, 18000, 17000, 19000, 21000, 20000, 23000],
        'customers': [100, 120, 110, 150, 140, 160, 180, 170, 190, 210, 200, 230],
        'region': ['North', 'South', 'North', 'South', 'North', 'South', 'North', 'South', 'North', 'South', 'North', 'South']
    }
    df = pd.DataFrame(data)
    
    qa_pairs = [
        {
            "question": "What is the total revenue?",
            "answer": "196000",
            "reasoning": "Sum of all revenue values"
        },
        {
            "question": "What is the average number of customers?",
            "answer": "160",
            "reasoning": "Mean of customers column rounded to nearest integer"
        },
        {
            "question": "How many months of data are there?",
            "answer": "12",
            "reasoning": "Count of rows in the dataset"
        },
        {
            "question": "What is the maximum revenue?",
            "answer": "23000",
            "reasoning": "Maximum value in revenue column"
        }
    ]
    
    return BenchmarkDataset("Sales", df, qa_pairs)


def load_ecommerce_benchmark() -> BenchmarkDataset:
    """Load synthetic e-commerce dataset with benchmark Q&A pairs."""
    from synthetic_generator import generate_ecommerce_dataset
    
    df = generate_ecommerce_dataset(n_rows=100, seed=42)
    
    # Pre-calculate correct answers
    total_revenue = df['total_amount'].sum()
    avg_order_value = df['total_amount'].mean()
    total_orders = len(df)
    top_category = df['product_category'].value_counts().index[0]
    max_order_amount = df['total_amount'].max()
    
    qa_pairs = [
        {
            "question": "What is the total revenue from all orders?",
            "answer": str(round(total_revenue, 2)),
            "reasoning": f"Sum of all total_amount values: {round(total_revenue, 2)}"
        },
        {
            "question": "What is the average order value?",
            "answer": str(round(avg_order_value, 2)),
            "reasoning": f"Mean of total_amount column: {round(avg_order_value, 2)}"
        },
        {
            "question": "How many orders were placed?",
            "answer": str(total_orders),
            "reasoning": f"Total number of rows: {total_orders}"
        },
        {
            "question": "What is the most popular product category?",
            "answer": top_category,
            "reasoning": f"Category with highest count: {top_category}"
        },
        {
            "question": "What is the maximum order amount?",
            "answer": str(round(max_order_amount, 2)),
            "reasoning": f"Maximum total_amount value: {round(max_order_amount, 2)}"
        }
    ]
    
    return BenchmarkDataset("E-commerce", df, qa_pairs)


def load_employee_benchmark() -> BenchmarkDataset:
    """Load synthetic employee dataset with benchmark Q&A pairs."""
    from synthetic_generator import generate_employee_dataset
    
    df = generate_employee_dataset(n_rows=50, seed=42)
    
    # Pre-calculate correct answers
    avg_salary = df['salary'].mean()
    highest_salary = df['salary'].max()
    total_employees = len(df)
    engineering_count = len(df[df['department'] == 'Engineering'])
    remote_count = df['is_remote'].sum()
    
    qa_pairs = [
        {
            "question": "What is the average salary?",
            "answer": str(round(avg_salary, 2)),
            "reasoning": f"Mean of salary column: {round(avg_salary, 2)}"
        },
        {
            "question": "What is the highest salary?",
            "answer": str(highest_salary),
            "reasoning": f"Maximum salary value: {highest_salary}"
        },
        {
            "question": "How many employees are in Engineering?",
            "answer": str(engineering_count),
            "reasoning": f"Count of employees where department='Engineering': {engineering_count}"
        },
        {
            "question": "How many employees work remotely?",
            "answer": str(remote_count),
            "reasoning": f"Count where is_remote=True: {remote_count}"
        }
    ]
    
    return BenchmarkDataset("Employees", df, qa_pairs)


def load_titanic_benchmark() -> BenchmarkDataset:
    """Load Titanic dataset with benchmark Q&A pairs."""
    from external_datasets import load_titanic_dataset
    
    df = load_titanic_dataset()
    
    # Pre-calculate correct answers
    total_passengers = len(df)
    survived_count = df['survived'].sum()
    avg_age = df['age'].mean()
    fare_max = df['fare'].max()
    male_count = len(df[df['sex'] == 'male'])
    
    qa_pairs = [
        {
            "question": "How many passengers were on the Titanic?",
            "answer": str(total_passengers),
            "reasoning": f"Total number of rows: {total_passengers}"
        },
        {
            "question": "How many passengers survived?",
            "answer": str(survived_count),
            "reasoning": f"Count where survived=1: {survived_count}"
        },
        {
            "question": "What is the average age of passengers?",
            "answer": str(round(avg_age, 2)),
            "reasoning": f"Mean of age column (excluding NaN): {round(avg_age, 2)}"
        },
        {
            "question": "What is the maximum fare paid?",
            "answer": str(round(fare_max, 2)),
            "reasoning": f"Maximum fare value: {round(fare_max, 2)}"
        },
        {
            "question": "How many male passengers were there?",
            "answer": str(male_count),
            "reasoning": f"Count where sex='male': {male_count}"
        }
    ]
    
    return BenchmarkDataset("Titanic", df, qa_pairs)


def load_happiness_benchmark() -> BenchmarkDataset:
    """Load World Happiness dataset with benchmark Q&A pairs."""
    from external_datasets import load_world_happiness_sample
    
    df = load_world_happiness_sample()
    
    # Pre-calculate correct answers
    happiest_country = df.loc[df['Happiness_Score'].idxmax(), 'Country']
    avg_happiness = df['Happiness_Score'].mean()
    western_europe_count = len(df[df['Region'] == 'Western Europe'])
    highest_gdp = df['GDP_per_capita'].max()
    
    qa_pairs = [
        {
            "question": "Which country has the highest happiness score?",
            "answer": happiest_country,
            "reasoning": f"Country with max Happiness_Score: {happiest_country}"
        },
        {
            "question": "What is the average happiness score?",
            "answer": str(round(avg_happiness, 3)),
            "reasoning": f"Mean of Happiness_Score: {round(avg_happiness, 3)}"
        },
        {
            "question": "How many countries are from Western Europe?",
            "answer": str(western_europe_count),
            "reasoning": f"Count where Region='Western Europe': {western_europe_count}"
        },
        {
            "question": "What is the highest GDP per capita?",
            "answer": str(round(highest_gdp, 3)),
            "reasoning": f"Maximum GDP_per_capita: {round(highest_gdp, 3)}"
        }
    ]
    
    return BenchmarkDataset("World Happiness", df, qa_pairs)


def load_supermarket_benchmark() -> BenchmarkDataset:
    """Load Supermarket Sales dataset with benchmark Q&A pairs."""
    from external_datasets import load_supermarket_sales_sample
    
    df = load_supermarket_sales_sample()
    
    # Pre-calculate correct answers
    total_sales = df['total'].sum()
    avg_rating = df['rating'].mean()
    branch_a_count = len(df[df['branch'] == 'A'])
    top_product_line = df['product_line'].value_counts().index[0]
    cash_payments = len(df[df['payment'] == 'Cash'])
    
    qa_pairs = [
        {
            "question": "What is the total sales amount?",
            "answer": str(round(total_sales, 2)),
            "reasoning": f"Sum of total column: {round(total_sales, 2)}"
        },
        {
            "question": "What is the average customer rating?",
            "answer": str(round(avg_rating, 2)),
            "reasoning": f"Mean of rating column: {round(avg_rating, 2)}"
        },
        {
            "question": "How many sales were made at branch A?",
            "answer": str(branch_a_count),
            "reasoning": f"Count where branch='A': {branch_a_count}"
        },
        {
            "question": "What is the most popular product line?",
            "answer": top_product_line,
            "reasoning": f"Product line with highest count: {top_product_line}"
        },
        {
            "question": "How many payments were made in cash?",
            "answer": str(cash_payments),
            "reasoning": f"Count where payment='Cash': {cash_payments}"
        }
    ]
    
    return BenchmarkDataset("Supermarket Sales", df, qa_pairs)


def load_covid_benchmark() -> BenchmarkDataset:
    """Load COVID-19 dataset with benchmark Q&A pairs."""
    from external_datasets import load_covid_sample
    
    df = load_covid_sample()
    
    # Pre-calculate correct answers
    total_cases = df['total_cases'].sum()
    country_max_cases = df.loc[df['total_cases'].idxmax(), 'country']
    avg_recovery_rate = df['recovery_rate'].mean()
    usa_deaths = df.loc[df['country'] == 'USA', 'total_deaths'].values[0]
    
    qa_pairs = [
        {
            "question": "What is the total number of COVID cases across all countries?",
            "answer": str(total_cases),
            "reasoning": f"Sum of total_cases: {total_cases}"
        },
        {
            "question": "Which country has the most COVID cases?",
            "answer": country_max_cases,
            "reasoning": f"Country with max total_cases: {country_max_cases}"
        },
        {
            "question": "What is the average recovery rate?",
            "answer": str(round(avg_recovery_rate, 2)),
            "reasoning": f"Mean of recovery_rate: {round(avg_recovery_rate, 2)}"
        },
        {
            "question": "How many deaths were there in the USA?",
            "answer": str(usa_deaths),
            "reasoning": f"total_deaths for USA: {usa_deaths}"
        }
    ]
    
    return BenchmarkDataset("COVID-19", df, qa_pairs)


def load_stackoverflow_benchmark() -> BenchmarkDataset:
    """Load Stack Overflow Survey dataset with benchmark Q&A pairs."""
    from external_datasets import load_stackoverflow_survey_sample
    
    df = load_stackoverflow_survey_sample()
    
    # Pre-calculate correct answers
    avg_salary = df['annual_salary'].mean()
    fulltime_remote = len(df[df['remote_work'] == 'Full-time'])
    top_country = df['country'].value_counts().index[0]
    max_years_coding = df['years_coding'].max()
    
    qa_pairs = [
        {
            "question": "What is the average annual salary?",
            "answer": str(round(avg_salary, 2)),
            "reasoning": f"Mean of annual_salary: {round(avg_salary, 2)}"
        },
        {
            "question": "How many developers work remotely full-time?",
            "answer": str(fulltime_remote),
            "reasoning": f"Count where remote_work='Full-time': {fulltime_remote}"
        },
        {
            "question": "Which country has the most respondents?",
            "answer": top_country,
            "reasoning": f"Country with highest count: {top_country}"
        },
        {
            "question": "What is the maximum years of coding experience?",
            "answer": str(max_years_coding),
            "reasoning": f"Maximum years_coding: {max_years_coding}"
        }
    ]
    
    return BenchmarkDataset("Stack Overflow Survey", df, qa_pairs)


def load_california_housing_benchmark() -> BenchmarkDataset:
    """Load California Housing dataset (4000 rows) with benchmark Q&A pairs."""
    from src.external_datasets import load_california_housing_dataset
    
    df = load_california_housing_dataset()
    
    # Pre-calculate correct answers
    total_rows = len(df)
    avg_median_income = df['MedInc'].mean()
    max_house_value = df['MedHouseVal'].max()
    min_house_age = df['HouseAge'].min()
    avg_rooms = df['AveRooms'].mean()
    max_population = df['Population'].max()
    houses_above_3 = len(df[df['MedHouseVal'] > 3.0])
    avg_latitude = df['Latitude'].mean()
    max_bedrooms = df['AveBedrms'].max()
    total_population = df['Population'].sum()
    
    qa_pairs = [
        {
            "question": "How many houses are in the dataset?",
            "answer": str(total_rows),
            "reasoning": f"Total number of rows: {total_rows}"
        },
        {
            "question": "What is the average median income?",
            "answer": str(round(avg_median_income, 3)),
            "reasoning": f"Mean of MedInc column: {round(avg_median_income, 3)}"
        },
        {
            "question": "What is the maximum median house value?",
            "answer": str(round(max_house_value, 5)),
            "reasoning": f"Maximum MedHouseVal: {round(max_house_value, 5)}"
        },
        {
            "question": "What is the minimum house age?",
            "answer": str(round(min_house_age, 1)),
            "reasoning": f"Minimum HouseAge: {round(min_house_age, 1)}"
        },
        {
            "question": "What is the average number of rooms?",
            "answer": str(round(avg_rooms, 3)),
            "reasoning": f"Mean of AveRooms column: {round(avg_rooms, 3)}"
        },
        {
            "question": "What is the maximum population in a block?",
            "answer": str(int(max_population)),
            "reasoning": f"Maximum Population: {int(max_population)}"
        },
        {
            "question": "How many houses have median value above 3.0?",
            "answer": str(houses_above_3),
            "reasoning": f"Count where MedHouseVal > 3.0: {houses_above_3}"
        },
        {
            "question": "What is the average latitude?",
            "answer": str(round(avg_latitude, 3)),
            "reasoning": f"Mean of Latitude column: {round(avg_latitude, 3)}"
        },
        {
            "question": "What is the maximum average number of bedrooms?",
            "answer": str(round(max_bedrooms, 3)),
            "reasoning": f"Maximum AveBedrms: {round(max_bedrooms, 3)}"
        },
        {
            "question": "What is the total population across all blocks?",
            "answer": str(int(total_population)),
            "reasoning": f"Sum of Population column: {int(total_population)}"
        }
    ]
    
    return BenchmarkDataset("California Housing", df, qa_pairs)


# Registry of available datasets
AVAILABLE_DATASETS = {
    'iris': load_iris_benchmark,
    'wine': load_wine_benchmark,
    'diabetes': load_diabetes_benchmark,
    'sales': load_custom_sales_benchmark,
    'ecommerce': load_ecommerce_benchmark,
    'employees': load_employee_benchmark,
    'titanic': load_titanic_benchmark,
    'happiness': load_happiness_benchmark,
    'supermarket': load_supermarket_benchmark,
    'covid': load_covid_benchmark,
    'stackoverflow': load_stackoverflow_benchmark,
    'california_housing': load_california_housing_benchmark
}


def get_benchmark_dataset(name: str) -> BenchmarkDataset:
    """Get a benchmark dataset by name."""
    if name not in AVAILABLE_DATASETS:
        raise ValueError(f"Dataset '{name}' not found. Available: {list(AVAILABLE_DATASETS.keys())}")
    return AVAILABLE_DATASETS[name]()
