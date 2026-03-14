from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load data once at startup
CSV_PATH = os.path.join('dataset', 'housing_data.csv')

def get_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()

@app.route('/')
def index():
    df = get_data()
    stats = {}
    if not df.empty:
        stats = {
            'total_records': len(df),
            'avg_price': int(df['Sale_Price'].mean()),
            'max_price': int(df['Sale_Price'].max()),
            'min_price': int(df['Sale_Price'].min()),
            'avg_area': int(df['Flat Area (in Sqft)'].mean())
        }
    return render_template('index.html', stats=stats)

@app.route('/api/data')
def api_data():
    df = get_data()
    if df.empty:
        return jsonify([])
    
    # Sample data to avoid heavy browser load if dataset is huge
    # In this case, we'll send a subset of columns needed for charts
    columns = [
        'Sale_Price', 'Flat Area (in Sqft)', 'No of Bedrooms', 
        'No of Bathrooms', 'Overall Grade', 'Latitude', 'Longitude'
    ]
    data = df[columns].to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
