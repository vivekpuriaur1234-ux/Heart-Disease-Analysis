# ABC Company Housing Market Analysis

## Project Objective
The goal of this project is to analyze housing market data and identify factors influencing house prices and sales trends. This analysis helps stakeholders like real estate analysts and marketing teams understand patterns in housing prices, renovation impact, and house feature distributions.

## Tools Used
- **Tableau**: For interactive data visualizations and storyboard.
- **Python (Flask)**: For the web interface and data generation.
- **Bootstrap 5**: For responsive UI design.
- **GitHub**: For version control and deployment.

## Project Structure
```
project-folder
│
├── dataset/
│   └── housing_data.csv
│
├── tableau/
│   └── housing_dashboard.twb
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
└── README.md
```

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Visualizing houses"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Generation** (Optional, already included):
   ```bash
   python generate_data.py
   python generate_twb.py
   ```

4. **Run the Flask App**:
   ```bash
   python app.py
   ```
   Access the app at `http://localhost:5000`.

## Tableau Integration
The `tableau/housing_dashboard.twb` file contains the XML definition for the visualizations. 
- Open this file in **Tableau Desktop**.
- To embed it in the website, publish the workbook to **Tableau Public** and replace the placeholder in `templates/index.html` with your embed code.
