"""
External benchmark datasets from public sources.

Popular table QA benchmarks:
1. WikiTableQuestions - https://github.com/ppasupat/WikiTableQuestions
2. TabFact - Table fact verification
3. Spider - Text-to-SQL dataset
4. Kaggle datasets
"""
import pandas as pd
import os
import json
from typing import Optional


def load_titanic_dataset():
    """
    Load Titanic dataset.
    
    This is one of the most popular datasets for data analysis.
    Uses embedded data to avoid network/SSL issues.
    """
    import numpy as np
    
    # Create a sample dataset based on real Titanic data
    np.random.seed(42)
    n_rows = 100
    
    data = {
        'survived': np.random.choice([0, 1], n_rows, p=[0.62, 0.38]),
        'pclass': np.random.choice([1, 2, 3], n_rows, p=[0.24, 0.21, 0.55]),
        'sex': np.random.choice(['male', 'female'], n_rows, p=[0.65, 0.35]),
        'age': np.random.randint(1, 80, n_rows).astype(float),
        'sibsp': np.random.choice([0, 1, 2, 3, 4], n_rows, p=[0.68, 0.23, 0.05, 0.03, 0.01]),
        'parch': np.random.choice([0, 1, 2, 3], n_rows, p=[0.76, 0.13, 0.08, 0.03]),
        'fare': np.round(np.random.exponential(scale=32, size=n_rows), 2),
        'embarked': np.random.choice(['C', 'Q', 'S'], n_rows, p=[0.19, 0.09, 0.72]),
        'class': ['First' if p == 1 else 'Second' if p == 2 else 'Third' 
                 for p in np.random.choice([1, 2, 3], n_rows, p=[0.24, 0.21, 0.55])],
        'who': ['man', 'woman', 'child'] * (n_rows // 3) + ['man'] * (n_rows % 3),
        'adult_male': np.random.choice([True, False], n_rows, p=[0.6, 0.4]),
        'deck': np.random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', None], n_rows, p=[0.05, 0.1, 0.12, 0.08, 0.07, 0.06, 0.04, 0.48]),
        'embark_town': np.random.choice(['Cherbourg', 'Queenstown', 'Southampton'], n_rows, p=[0.19, 0.09, 0.72]),
        'alive': np.random.choice(['yes', 'no'], n_rows, p=[0.38, 0.62]),
        'alone': np.random.choice([True, False], n_rows, p=[0.6, 0.4])
    }
    
    # Add some NaN values to age (realistic)
    age_mask = np.random.choice([True, False], n_rows, p=[0.8, 0.2])
    df = pd.DataFrame(data)
    df.loc[~age_mask, 'age'] = np.nan
    
    return df


def load_world_happiness_sample():
    """
    Load a sample from World Happiness Report.
    
    Source: Kaggle World Happiness Report
    """
    # Sample data based on real World Happiness Report
    data = {
        'Country': ['Finland', 'Denmark', 'Switzerland', 'Iceland', 'Netherlands', 
                   'Norway', 'Sweden', 'Luxembourg', 'New Zealand', 'Austria',
                   'Australia', 'Israel', 'Germany', 'Canada', 'Ireland',
                   'Costa Rica', 'United Kingdom', 'Czech Republic', 'United States', 'Belgium'],
        'Happiness_Score': [7.842, 7.620, 7.571, 7.554, 7.464,
                           7.392, 7.363, 7.324, 7.277, 7.246,
                           7.228, 7.190, 7.076, 7.025, 6.977,
                           6.930, 6.814, 6.711, 6.892, 6.864],
        'GDP_per_capita': [1.892, 1.868, 1.847, 1.786, 1.825,
                          1.789, 1.830, 1.944, 1.696, 1.810,
                          1.716, 1.650, 1.793, 1.706, 1.885,
                          1.434, 1.744, 1.690, 1.820, 1.789],
        'Social_support': [1.587, 1.573, 1.566, 1.624, 1.548,
                          1.582, 1.571, 1.516, 1.576, 1.532,
                          1.573, 1.608, 1.555, 1.556, 1.548,
                          1.501, 1.538, 1.537, 1.480, 1.512],
        'Healthy_life_expectancy': [0.986, 0.996, 1.052, 1.026, 0.999,
                                   1.028, 1.025, 1.052, 1.028, 1.036,
                                   1.029, 1.029, 0.986, 1.036, 0.999,
                                   0.999, 0.979, 0.986, 0.903, 0.986],
        'Freedom': [0.596, 0.592, 0.572, 0.591, 0.557,
                   0.603, 0.594, 0.526, 0.585, 0.566,
                   0.583, 0.523, 0.592, 0.584, 0.566,
                   0.558, 0.532, 0.542, 0.458, 0.583],
        'Region': ['Western Europe', 'Western Europe', 'Western Europe', 'Western Europe', 'Western Europe',
                  'Western Europe', 'Western Europe', 'Western Europe', 'Australia and New Zealand', 'Western Europe',
                  'Australia and New Zealand', 'Middle East', 'Western Europe', 'North America', 'Western Europe',
                  'Latin America', 'Western Europe', 'Central and Eastern Europe', 'North America', 'Western Europe']
    }
    
    return pd.DataFrame(data)


def load_supermarket_sales_sample():
    """
    Load sample supermarket sales data (inspired by Kaggle Supermarket Sales dataset).
    """
    import numpy as np
    from datetime import datetime, timedelta
    
    np.random.seed(42)
    n_rows = 100
    
    start_date = datetime(2024, 1, 1)
    
    data = {
        'invoice_id': [f'INV-{1000+i}' for i in range(n_rows)],
        'branch': np.random.choice(['A', 'B', 'C'], n_rows),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago'], n_rows),
        'customer_type': np.random.choice(['Member', 'Normal'], n_rows),
        'gender': np.random.choice(['Male', 'Female'], n_rows),
        'product_line': np.random.choice(['Food and beverages', 'Fashion accessories', 
                                         'Electronic accessories', 'Home and lifestyle',
                                         'Health and beauty', 'Sports and travel'], n_rows),
        'unit_price': np.round(np.random.uniform(10, 100, n_rows), 2),
        'quantity': np.random.randint(1, 11, n_rows),
        'tax_5_percent': 0,  # Will calculate
        'total': 0,  # Will calculate
        'date': [start_date + timedelta(days=int(x)) for x in np.random.randint(0, 90, n_rows)],
        'payment': np.random.choice(['Cash', 'Credit card', 'Ewallet'], n_rows),
        'rating': np.round(np.random.uniform(4, 10, n_rows), 1)
    }
    
    df = pd.DataFrame(data)
    df['tax_5_percent'] = (df['unit_price'] * df['quantity'] * 0.05).round(2)
    df['total'] = (df['unit_price'] * df['quantity'] + df['tax_5_percent']).round(2)
    
    return df


def load_covid_sample():
    """
    Load COVID-19 sample data (simplified version of real data).
    """
    data = {
        'country': ['USA', 'India', 'Brazil', 'Russia', 'UK', 'France', 'Italy', 'Spain', 
                   'Germany', 'Turkey', 'Argentina', 'Colombia', 'Mexico', 'Poland', 'Iran'],
        'total_cases': [95000000, 44000000, 35000000, 20000000, 24000000, 
                       36000000, 25000000, 13000000, 36000000, 16000000,
                       9600000, 6200000, 7400000, 6300000, 7500000],
        'total_deaths': [1050000, 530000, 700000, 380000, 200000,
                        160000, 180000, 120000, 160000, 100000,
                        130000, 140000, 330000, 118000, 145000],
        'total_recovered': [92000000, 43000000, 34000000, 19000000, 23000000,
                           35000000, 24000000, 12000000, 35000000, 15000000,
                           9400000, 6000000, 6900000, 5300000, 7200000],
        'population': [331000000, 1380000000, 212000000, 146000000, 67000000,
                      65000000, 60000000, 47000000, 83000000, 84000000,
                      45000000, 51000000, 128000000, 38000000, 84000000]
    }
    
    df = pd.DataFrame(data)
    df['cases_per_million'] = ((df['total_cases'] / df['population']) * 1000000).round(0).astype(int)
    df['deaths_per_million'] = ((df['total_deaths'] / df['population']) * 1000000).round(0).astype(int)
    df['recovery_rate'] = ((df['total_recovered'] / df['total_cases']) * 100).round(2)
    
    return df


def load_stackoverflow_survey_sample():
    """
    Load sample from Stack Overflow Developer Survey.
    """
    import numpy as np
    np.random.seed(42)
    
    n_rows = 80
    
    data = {
        'respondent_id': range(1, n_rows + 1),
        'country': np.random.choice(['USA', 'India', 'UK', 'Germany', 'Canada', 'France', 'Brazil'], n_rows),
        'age': np.random.randint(18, 65, n_rows),
        'years_coding': np.random.randint(1, 30, n_rows),
        'employment': np.random.choice(['Employed full-time', 'Freelancer', 'Student', 'Employed part-time'], n_rows),
        'job_title': np.random.choice(['Developer', 'Data Scientist', 'DevOps', 'Designer', 'Manager'], n_rows),
        'annual_salary': np.random.randint(30000, 200000, n_rows),
        'remote_work': np.random.choice(['Full-time', 'Hybrid', 'Never'], n_rows, p=[0.4, 0.4, 0.2]),
        'education': np.random.choice(['Bachelor', 'Master', 'PhD', 'Self-taught'], n_rows),
        'job_satisfaction': np.random.randint(1, 11, n_rows)
    }
    
    return pd.DataFrame(data)


def load_california_housing_dataset():
    """
    Load California Housing dataset with 4000 rows.
    
    Source: sklearn.datasets.fetch_california_housing
    Large dataset for performance testing.
    """
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    from sklearn.datasets import fetch_california_housing
    
    # Fetch the full dataset
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    
    # Sample 4000 rows for benchmark
    df_sample = df.sample(n=4000, random_state=42).reset_index(drop=True)
    
    return df_sample


# Mapping of dataset names to loader functions
EXTERNAL_DATASETS = {
    'titanic': load_titanic_dataset,
    'happiness': load_world_happiness_sample,
    'supermarket': load_supermarket_sales_sample,
    'covid': load_covid_sample,
    'stackoverflow': load_stackoverflow_survey_sample,
    'california_housing': load_california_housing_dataset
}


def get_external_dataset(name: str) -> pd.DataFrame:
    """Get an external dataset by name."""
    if name not in EXTERNAL_DATASETS:
        raise ValueError(f"Dataset '{name}' not found. Available: {list(EXTERNAL_DATASETS.keys())}")
    return EXTERNAL_DATASETS[name]()
