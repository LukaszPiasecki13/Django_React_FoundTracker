import random
from authentication.models import UserProfile
from django.test import Client


class TransactionFactory():
    
    
    def __init__(self, user, pocket_name='NAME', operation='buy') :

        self.user = user
        self.pocket_name = pocket_name
        self.tickers = [
            'AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'FB', 'TSLA', 'NVDA', 
            'JPM', 'BABA', 'BRK.A', 'BRK.B', 'V', 'MA', 'INTC', 'NFLX', 
            'PYPL', 'AMD', 'DIS', 'CRM'
        ]
        self.operation = operation


    def genrate_ticker(self):
        '''Generate a random ticker from the list of tickers and remove it from the list.'''

        if len(self.tickers) == 0:
            return None
        
        ticker =  random.choice(self.tickers)
        self.tickers.remove(ticker)
        return ticker

    def genrate_price(self):
        return random.randint(50, 500)
    
    def genrate_quantity(self):
        return random.randint(1, 100)
    
    def genrate_fee(self):
        return random.randint(0, 10)
    
    def draw(self) -> tuple:
        '''Draw a random transaction data and the corresponding verification data.'''

        transaction_data = {
            'operation': self.operation,
            'ticker': self.genrate_ticker(),
            'date': '2022-01-01',
            'currency': 'USD',
            'quantity': self.genrate_quantity(),
            'price': self.genrate_price(),
            'fee': self.genrate_fee(),
            'comment': 'Test comment',
            'asset_class': 'Equity',
            'owner': self.user,
            'pocket_name': self.pocket_name
        }


        verification_data = {
            'ticker': transaction_data['ticker'],
            'quantity': transaction_data['quantity'],
            'price': transaction_data['price'],
            'fee': transaction_data['fee']
        }
        
        return transaction_data, verification_data
         
