import django
django.setup()
from stocks_project import settings
settings.configure()
import os
import yfinance as yf
from datetime import datetime, timedelta
from stocks.models import Company, StockPrice

os.environ['DJANGO_SETTINGS_MODULE'] = 'stocks_project.settings'

# Define the ticker symbol for the company
ticker_symbol = 'AAPL'

# Get the company object from the database
company = Company.objects.get(ticker=ticker_symbol)

# Define the date range
start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()

# Fetch the stock price data from Yahoo Finance
stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Loop through each row of the stock data and save it to the database
for index, row in stock_data.iterrows():
    stock_price = StockPrice(
        company=company,
        date=index,
        open=row['Open'],
        close=row['Close'],
        volume=row['Volume']
    )
    stock_price.save()

print('Stock price data saved to database.')
