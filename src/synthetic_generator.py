"""
Synthetic dataset generator for benchmarking.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_ecommerce_dataset(n_rows=100, seed=42):
    """
    Generate synthetic e-commerce dataset.
    
    Returns DataFrame with:
    - order_id, customer_id, product_category, quantity, price, order_date, region, payment_method
    """
    np.random.seed(seed)
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
    regions = ['North', 'South', 'East', 'West', 'Central']
    payment_methods = ['Credit Card', 'PayPal', 'Cash', 'Debit Card']
    
    start_date = datetime(2024, 1, 1)
    
    data = {
        'order_id': range(1000, 1000 + n_rows),
        'customer_id': np.random.randint(1, 50, n_rows),
        'product_category': np.random.choice(categories, n_rows),
        'quantity': np.random.randint(1, 10, n_rows),
        'price': np.round(np.random.uniform(10, 500, n_rows), 2),
        'order_date': [start_date + timedelta(days=int(x)) for x in np.random.randint(0, 180, n_rows)],
        'region': np.random.choice(regions, n_rows),
        'payment_method': np.random.choice(payment_methods, n_rows)
    }
    
    df = pd.DataFrame(data)
    df['total_amount'] = df['quantity'] * df['price']
    
    return df


def generate_employee_dataset(n_rows=50, seed=42):
    """
    Generate synthetic employee dataset.
    
    Returns DataFrame with:
    - employee_id, name, department, salary, years_experience, performance_rating, is_remote
    """
    np.random.seed(seed)
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Lisa', 'Robert', 'Maria']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    data = {
        'employee_id': range(1, n_rows + 1),
        'name': [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_rows)],
        'department': np.random.choice(departments, n_rows),
        'salary': np.random.randint(40000, 150000, n_rows),
        'years_experience': np.random.randint(0, 25, n_rows),
        'performance_rating': np.round(np.random.uniform(2.5, 5.0, n_rows), 1),
        'is_remote': np.random.choice([True, False], n_rows, p=[0.4, 0.6])
    }
    
    return pd.DataFrame(data)


def generate_stock_dataset(n_rows=60, seed=42):
    """
    Generate synthetic stock trading dataset.
    
    Returns DataFrame with:
    - date, ticker, open_price, close_price, volume, high, low
    """
    np.random.seed(seed)
    
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    start_date = datetime(2024, 1, 1)
    
    data = []
    for ticker in tickers:
        base_price = np.random.uniform(100, 300)
        for i in range(n_rows // len(tickers)):
            date = start_date + timedelta(days=i)
            open_price = base_price + np.random.uniform(-10, 10)
            close_price = open_price + np.random.uniform(-5, 5)
            high = max(open_price, close_price) + np.random.uniform(0, 3)
            low = min(open_price, close_price) - np.random.uniform(0, 3)
            volume = np.random.randint(1000000, 10000000)
            
            data.append({
                'date': date,
                'ticker': ticker,
                'open_price': round(open_price, 2),
                'close_price': round(close_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'volume': volume
            })
            
            base_price = close_price  # Next day starts from previous close
    
    return pd.DataFrame(data)


def generate_customer_churn_dataset(n_rows=80, seed=42):
    """
    Generate synthetic customer churn dataset.
    
    Returns DataFrame with:
    - customer_id, age, tenure_months, monthly_charges, total_charges, contract_type, churned
    """
    np.random.seed(seed)
    
    contract_types = ['Month-to-Month', 'One Year', 'Two Year']
    
    data = {
        'customer_id': range(5000, 5000 + n_rows),
        'age': np.random.randint(18, 75, n_rows),
        'tenure_months': np.random.randint(1, 72, n_rows),
        'monthly_charges': np.round(np.random.uniform(20, 120, n_rows), 2),
        'contract_type': np.random.choice(contract_types, n_rows),
        'has_internet': np.random.choice([True, False], n_rows, p=[0.8, 0.2]),
        'has_phone': np.random.choice([True, False], n_rows, p=[0.9, 0.1])
    }
    
    df = pd.DataFrame(data)
    df['total_charges'] = (df['tenure_months'] * df['monthly_charges']).round(2)
    
    # Simulate churn (higher charges and lower tenure = higher churn probability)
    churn_prob = (df['monthly_charges'] / 120 * 0.5) + ((72 - df['tenure_months']) / 72 * 0.5)
    df['churned'] = (np.random.random(n_rows) < churn_prob).astype(int)
    
    return df


def generate_weather_dataset(n_rows=90, seed=42):
    """
    Generate synthetic weather dataset.
    
    Returns DataFrame with:
    - date, city, temperature, humidity, precipitation, wind_speed, condition
    """
    np.random.seed(seed)
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    conditions = ['Sunny', 'Cloudy', 'Rainy', 'Snowy', 'Foggy']
    
    start_date = datetime(2024, 1, 1)
    
    data = []
    for city in cities:
        base_temp = np.random.uniform(10, 25)  # Base temperature for city
        
        for i in range(n_rows // len(cities)):
            date = start_date + timedelta(days=i)
            temp = base_temp + np.random.uniform(-10, 10)
            humidity = np.random.randint(30, 90)
            precipitation = np.random.uniform(0, 50) if np.random.random() < 0.3 else 0
            wind_speed = np.random.uniform(0, 30)
            condition = np.random.choice(conditions)
            
            data.append({
                'date': date,
                'city': city,
                'temperature': round(temp, 1),
                'humidity': humidity,
                'precipitation': round(precipitation, 1),
                'wind_speed': round(wind_speed, 1),
                'condition': condition
            })
    
    return pd.DataFrame(data)
