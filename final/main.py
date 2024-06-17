import pandas as pd
import yahooquery as yq
from information import key_metrics_def
from yahooquery import Screener
import locale
import warnings

warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, '')

from yahooquery import Ticker

class Stock:
    def __init__(self, ticker_obj, ticker_str):
        self.ticker = ticker_obj
        self.tck = ticker_str
        self.rsi_value = None
        self.summary = self.ticker.summary_detail
        self.asset_profile = self.ticker.asset_profile
        self.name = self.ticker.price[ticker_str].get('longName', 'N/A')
        self.industry = self.ticker.asset_profile[ticker_str].get('industry', 'N/A')
        self.current_price = self.ticker.price[ticker_str].get('regularMarketPrice', 0)
        self.fifty_two_week_high = self.ticker.summary_detail[ticker_str].get('fiftyTwoWeekHigh', 0)
        self.fifty_two_week_low = self.ticker.summary_detail[ticker_str].get('fiftyTwoWeekLow', 0)
        self.capitalization = self.ticker.price[ticker_str].get('marketCap', 0)
        self.debt_to_equity_ratio = self.ticker.financial_data[ticker_str].get('debtToEquity', 0)
        self.price_to_earnings = self.ticker.summary_detail[ticker_str].get('trailingPE', 0)
        self.enterprise_value = self.ticker.key_stats[ticker_str].get('enterpriseValue', 0)
        self.earnings_per_share = self.ticker.key_stats[ticker_str].get('trailingEps', 0)
        self.dividend_yield = self.ticker.summary_detail[ticker_str].get('dividendYield', 0)
        self.beta = self.ticker.key_stats[ticker_str].get('beta', 0)
        self.currency = self.ticker.price[ticker_str].get('currency', 'N/A')
        self.history = self.ticker.history(period="1mo")

    def get_most_important_info(self):
        info = {
            'Earnings Per Share': locale.currency(self.earnings_per_share, grouping=True),
            'Price-to-Earnings Ratio': round(self.price_to_earnings, 2),
            'Dividend Yield': f"{self.dividend_yield:.2%}",
            'Market Capitalization': locale.currency(self.capitalization, grouping=True),
            'Debt-to-Equity Ratio': f"{self.debt_to_equity_ratio*0.01:.2%}"
        }
        return info

    def get_all_financial_info(self):
        info = {
            'Name': self.name,
            'Ticker': self.tck,
            'Industry': self.industry,
            'Current Price': locale.currency(self.current_price, grouping=True),
            '52 Week High': locale.currency(self.fifty_two_week_high, grouping=True),
            '52 Week Low': locale.currency(self.fifty_two_week_low, grouping=True),
            'Market Cap': locale.currency(self.capitalization, grouping=True),
            'P/E Ratio': round(self.price_to_earnings, 2),
            'Debt/Equity Ratio': self.debt_to_equity_ratio,
            'Enterprise Value': self.enterprise_value,
            'Earnings Per Share': locale.currency(self.earnings_per_share, grouping=True),
            'Dividend Yield': self.dividend_yield,
            'Beta': self.beta,
            'Currency': self.currency
        }
        return info

    def rsi_index(self, period=15):
        def price_changes(period):
            price_list = self.ticker.history(period=f"{period}d", interval="1d")['close'].tolist()
            n = len(price_list)

            if n < 15:
                return None, None
            gains = []
            losses = []

            for i in range(1, len(price_list)):
                change = price_list[i] - price_list[i - 1]
                if change > 0:
                    gains.append(change)
                else:
                    losses.append(abs(change))

            gain_average = sum(gains) / (period - 1)
            loss_average = sum(losses) / (period - 1)
            return gain_average, loss_average

        gain_avg, loss_avg = price_changes(period)

        if gain_avg is None or loss_avg is None:
            self.rsi_value = None
            return "Not enough price data to calculate RSI"

        if loss_avg == 0:
            self.rsi_value = 100
        else:
            rs = gain_avg / loss_avg
            self.rsi_value = 100 - (100 / (1 + rs))

        return self.rsi_value

    def get_rsi(self, period=15):
        if self.rsi_value is None:
            self.rsi_index(period)

        if self.rsi_value is None:
            return "The RSI value could not be calculated"

        advice = ''

        if self.rsi_value > 70:
            advice = 'Sell'
        elif self.rsi_value < 30:
            advice = 'Buy'
        else:
            advice = 'Hold'

        return f"The RSI is {self.rsi_value:.2f}. Advice: {advice}"

    def get_corporate_events(self, number_of_events):
        events_df = self.ticker.corporate_events
        events_df = events_df.iloc[::-1]
        events_df.reset_index(inplace=True)

        events_list = []

        if 'date' in events_df.columns and 'headline' in events_df.columns and 'description' in events_df.columns and 'parentTopics' in events_df.columns:
            for i in range(min(number_of_events, len(events_df))):
                event = {
                    'date': events_df['date'][i],
                    'headline': events_df['headline'][i],
                    'description': events_df['description'][i],
                    'topic': events_df['parentTopics'][i]
                }
                events_list.append(event)

        return events_list


def get_tickers_from_screeners(screeners=['most_actives', 'day_gainers', 'day_losers']):
    s = Screener()
    all_tickers = set()
    for screener in screeners:
        try:
            data = s.get_screeners([screener], 250)
            quotes = data[screener]['quotes']
            tickers = [quote['symbol'] for quote in quotes]
            all_tickers.update(tickers)
        except Exception as e:
            print(f"Error fetching data for screener {screener}: {e}")
    all_tickers = list(all_tickers)
    all_tickers.sort()
    return all_tickers

def find_ticker():
    print("Fetching Tickers")
    print("_ " * 25, "\n")
    tickers = get_tickers_from_screeners()

    print("Available Tickers:")
    for idx, ticker in enumerate(tickers, 1):
        print(f"{idx}. {ticker}")

    choice = input("Enter the number corresponding to the ticker or the ticker symbol: ").strip()

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(tickers):
            return tickers[index]
        else:
            print("Invalid selection. Please try again.")
            return find_ticker()
    elif choice.upper() in tickers:
        return choice.upper()
    else:
        print("Invalid selection. Please try again.")
        return find_ticker()


def runner():
    try:
        ticker_symbol = find_ticker()

        if ticker_symbol:
            stock_input = Ticker(ticker_symbol)
            stock_obj = Stock(stock_input, ticker_symbol)

            while True:
                print(f"\nYou have selected: {ticker_symbol}\n")
                print("What would you like to do?")
                print("1. Get RSI and advice")
                print("2. Get most important info")
                print("3. Get all financial info")
                print("4. Get corporate events")
                print("5. Exit")

                choice = input("Enter the number corresponding to your choice: ")

                if choice == '1':
                    print(stock_obj.get_rsi())
                elif choice == '2':
                    print(stock_obj.get_most_important_info())
                elif choice == '3':
                    stock_obj.get_all_financial_info()
                elif choice == '4':
                    number_of_events = int(input("Enter the number of corporate events to retrieve: "))
                    stock_obj.get_corporate_events(number_of_events)
                elif choice == '5':
                    print("Exiting the program.")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("No valid ticker provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

# runner()
