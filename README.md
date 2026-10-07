Flipkart Product Price Analysis Using Web Scraping & EDA
An end-to-end Python project that collects product information from Flipkart search results using Selenium and performs data cleaning, statistical analysis, and exploratory data visualization.
Project Workflow
```text
Flipkart Search
      ↓
Selenium Web Scraping
      ↓
CSV Data Collection
      ↓
Price & Rating Cleaning
      ↓
NumPy Statistical Analysis
      ↓
Exploratory Data Analysis
      ↓
Business/Product Insights
```
Features
Selenium-based product search scraping
Configurable product name and number of pages
Product name, price, rating, and product URL collection
Brand extraction from product names
Price cleaning and numeric conversion
NumPy descriptive statistics
Price distribution analysis
Box plot and violin plot
KDE density analysis
Top expensive products
Rating vs price analysis
Brand frequency analysis
Correlation heatmap
Automatic chart export to `outputs/`
Project Structure
```text
flipkart-analyzer-main/
│
├── data/
│   └── flipkart_products.csv
│
├── logs/
│
├── notebooks/
│   └── analysis.ipynb
│
├── outputs/
│
├── scraper/
│   ├── __init__.py
│   ├── flipkart_scraper.py
│   └── utils.py
│
├── visualization/
│   ├── __init__.py
│   └── charts.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
Technologies
Python
Pandas
NumPy
Selenium
Matplotlib
Seaborn
Regular Expressions
Setup
Create a virtual environment:
```bash
python -m venv venv
```
Activate on Windows:
```bash
venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run
```bash
python main.py
```
Enter a search product, for example:
```text
Enter Product Name: laptops
Enter Number of Pages: 2
```
The scraped dataset is saved to:
```text
data/flipkart_products.csv
```
Charts are saved to:
```text
outputs/
```
Data Integrity
The project does not fabricate missing ratings, discounts, review counts, or availability values. Only information collected from the search results is retained, and unavailable fields remain missing.
Important Note
Flipkart's website structure can change over time. CSS/XPath selectors may therefore require maintenance if the site's HTML changes.
Use web scraping responsibly and in accordance with the website's applicable terms, policies, and access restrictions.
Resume Description
Flipkart Product Price Analysis using Web Scraping & EDA  
Developed a Selenium-based web scraping pipeline to collect Flipkart product data and performed data cleaning, NumPy statistical analysis, exploratory data analysis, price distribution analysis, brand analysis, rating-price analysis, and visualization using Pandas, Matplotlib, and Seaborn.