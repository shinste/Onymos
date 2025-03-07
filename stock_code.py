import time
import random
import threading

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type 
        self.ticker = ticker
        self.quantity = quantity
        self.price = price 

order_book = []
order_event = threading.Event()

def add_order(order_type, ticker, quantity, price):
    new_order = Order(order_type, ticker, quantity, price)
    order_book.append(new_order)
    order_event.set()
    match_order()

def match_order():
    i = 0
    while i < len(order_book):
        if order_book[i].order_type == 'B':
            best_match_index = None
            for j in range(len(order_book)):
                if (
                    order_book[j].order_type == 'S' and order_book[j].ticker == order_book[i].ticker and order_book[i].price >= order_book[j].price
                ):
                    if best_match_index is None or order_book[j].price < order_book[best_match_index].price:
                        best_match_index = j
            if best_match_index is not None:
                process_trade(i, best_match_index)
        i += 1

def process_trade(buy_index, sell_index):
    buy_order = order_book[buy_index]
    sell_order = order_book[sell_index]
    executed_quantity = min(buy_order.quantity, sell_order.quantity)
    if buy_order.quantity > executed_quantity:
        buy_order.quantity -= executed_quantity
    else:
        del order_book[buy_index]

    if sell_order.quantity > executed_quantity:
        sell_order.quantity -= executed_quantity
    else:
        del order_book[sell_index]

def stock_transactions():
    tickers = ['NVDA', 'GOOGL', 'META', 'AMZN', 'JPM']
    while True:
        order_type = 'B' if random.random() > 0.5 else 'S'
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = random.randint(50, 500)
        add_order(order_type, ticker, quantity, price)
        print(f"Order Added: {order_type} {quantity} {ticker} @ ${price}")

        time.sleep(1)

trading_thread = threading.Thread(target=stock_transactions, daemon=True)
trading_thread.start()
while True:
    time.sleep(1)
