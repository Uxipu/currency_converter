from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END
from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://free.currconv.com/"
API_KEY = "0e95030a9c5ba6cee694"

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    response = get(url)
    
    if response.status_code != 200:
        return []
    
    data = response.json().get('results', {})
    data = list(data.items())
    data.sort()
    
    return data

def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    response = get(url)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    
    if len(data) == 0:
        return None
    
    rate = list(data.values())[0]
    return rate

def convert_currency():
    clear_output() 
    currency1 = entry_currency1.get().upper()
    amount = entry_amount.get()
    currency2 = entry_currency2.get().upper()
    
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        output_text.insert(END, f"Invalid currencies or failed to fetch exchange rate.\n")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        output_text.insert(END, "Invalid amount.\n")
        return
    
    converted_amount = rate * amount
    output_text.insert(END, f"{amount} {currency1} is equal to {converted_amount} {currency2}\n")

def list_currencies():
    clear_output() 
    currencies = get_currencies()
    if not currencies:
        output_text.insert(END, "Failed to fetch currencies.\n")
        return
    
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        output_text.insert(END, f"{_id} - {name} - {symbol}\n")

def show_help():
    clear_output() 
    output_text.insert(END, "List = lists the different currencies\n")
    output_text.insert(END, "Convert - convert from one currency to another\n")
    output_text.insert(END, "Rate - get the exchange rate of two currencies\n")

def clear_output():
    output_text.delete(1.0, END)


root = Tk()
root.title("Currency Converter")


Label(root, text="Base Currency:").grid(row=0, column=0)
entry_currency1 = Entry(root)
entry_currency1.grid(row=0, column=1)

Label(root, text="Amount:").grid(row=1, column=0)
entry_amount = Entry(root)
entry_amount.grid(row=1, column=1)

Label(root, text="Target Currency:").grid(row=2, column=0)
entry_currency2 = Entry(root)
entry_currency2.grid(row=2, column=1)

Button(root, text="Convert", command=convert_currency).grid(row=3, column=0, columnspan=2)
Button(root, text="List Currencies", command=list_currencies).grid(row=4, column=0, columnspan=2)
Button(root, text="Help", command=show_help).grid(row=5, column=0, columnspan=2)

output_text = Text(root, height=20, width=50)
output_text.grid(row=6, column=0, columnspan=2)

scrollbar = Scrollbar(root)
scrollbar.grid(row=6, column=2, sticky='ns')
output_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_text.yview)


root.mainloop()
