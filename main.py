import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class Coin:
    def __init__(self, name, price, symbol):
        self.name = name 
        self.price = price
        self.symbol = symbol
    
    def format_line(self):
        return f'{self.name}: ${self.price:,.2f}'
        

class CryptoTestApp(App):
    def build(self):
        self.root_box = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.status = Label(text='Crypto Market', font_size=24)
        self.price = Label(text='press load prices', font_size=18)
        self.button = Button(text='load prices', size_hint_y=None, height=55)
        self.button.bind(on_press=self.load_prices)
        
        self.root_box.add_widget(self.status)
        self.root_box.add_widget(self.price)
        self.root_box.add_widget(self.button)
        return self.root_box
        
    def load_prices(self, instance):
        self.status.text = 'Loading...'
        threading.Thread(target=self.fetch_prices, daemon=True).start()
        
    def fetch_prices(self):
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {"vs_currency": "usd", "ids": "bitcoin,ethereum,solana"}
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()

            data = response.json()
            lines = []

            for coin in data:
                c = Coin(coin['name'], coin['current_price'], coin['symbol'])
                lines.append(c.format_line())
            
            result = '\n'.join(lines)
            if not result:
                result = 'no data received'
    
            Clock.schedule_once(lambda dt: self.show_result(result))
            
        except Exception as error:
            message = str(error)
            Clock.schedule_once(lambda dt, msg=message: self.show_error(msg))
            
    def show_result(self, result):
        self.status.text = 'Market Price'
        self.price.text = result
            
    def show_error(self, message):
        self.status.text = "API Error"
        self.price.text = message[:300]
    
    
if __name__ == "__main__":
    CryptoTestApp().run()
