import pandas as pd
import numpy as np
import os

def generate_housing_data(filename, num_records=1000):
    np.random.seed(42)
    
    # Generate synthetic data matching the real schema
    data = {
        'Sale_Price': np.random.normal(500000, 150000, num_records).astype(int),
        'No of Bedrooms': np.random.randint(1, 6, num_records),
        'No of Bathrooms': np.random.randint(1, 5, num_records),
        'Flat Area (in Sqft)': np.random.normal(2000, 500, num_records).astype(int),
        'Lot Area (in Sqft)': np.random.normal(5000, 2000, num_records).astype(int),
        'No of Floors': np.random.randint(1, 4, num_records),
        'No of Times Visited': np.random.randint(0, 5, num_records),
        'Overall Grade': np.random.randint(5, 13, num_records),
        'Area of the House from Basement (in Sqft)': lambda d: d['Flat Area (in Sqft)'] * 0.8,
        'Basement Area (in Sqft)': lambda d: d['Flat Area (in Sqft)'] * 0.2,
        'Age of House (in Years)': np.random.randint(0, 120, num_records),
        'Latitude': np.random.uniform(47.1, 47.8, num_records),
        'Longitude': np.random.uniform(-122.5, -121.3, num_records),
        'Living Area after Renovation (in Sqft)': np.random.normal(2100, 500, num_records).astype(int),
        'Lot Area after Renovation (in Sqft)': np.random.normal(5100, 2000, num_records).astype(int),
        'Years Since Renovation': np.random.choice([0] * 80 + list(range(1, 70)), num_records),
        'Condition_of_the_House_Excellent': np.random.choice([0, 1], num_records, p=[0.9, 0.1]),
        'Condition_of_the_House_Fair': np.random.choice([0, 1], num_records, p=[0.7, 0.3]),
        'Condition_of_the_House_Good': np.random.choice([0, 1], num_records, p=[0.6, 0.4]),
        'Condition_of_the_House_Okay': np.random.choice([0, 1], num_records, p=[0.95, 0.05]),
        'Ever_Renovated_Yes': np.random.choice([0, 1], num_records, p=[0.8, 0.2]),
        'Waterfront_View_Yes': np.random.choice([0, 1], num_records, p=[0.95, 0.05])
    }
    
    # Note: Zipcode groups are omitted for brevity in synthetic generation 
    # but can be added if needed for specific dashboard tests.
    
    df = pd.DataFrame(data)
    
    # Calculate derived fields
    df['Area of the House from Basement (in Sqft)'] = (df['Flat Area (in Sqft)'] * 0.8).astype(int)
    df['Basement Area (in Sqft)'] = (df['Flat Area (in Sqft)'] * 0.2).astype(int)
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    df.to_csv(filename, index=False)
    print(f"Synthetic dataset matching real schema generated at {filename}")

if __name__ == "__main__":
    generate_housing_data("dataset/housing_data.csv")
