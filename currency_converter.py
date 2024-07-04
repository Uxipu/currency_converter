import os
import ttkbootstrap as ttk
from tkinter import Tk
from requests import get
from dotenv import load_dotenv

#load environment variables
load_dotenv()

#API configuration
BASE_URL = "https://free.currconv.com/"
API_KEY = os.getenv("API_KEY")

def get_currencies():
    "Fetch the list of currencies from the API"
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    try:
        response = get(url)
        response.raise_for_status()
    except Exception as e:
        output_text.insert(ttk.END, f"Error fetching currencies: {e}\n")
        return []
    
    data = response.json().get('results', {})
    data = list(data.items())
    data.sort()
    return data

def exchange_rate(currency1, currency2):
    "Fetch the exchange rate between two currencies"
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    try:
        response = get(url)
        response.raise_for_status()
    except Exception as e:
        output_text.insert(ttk.END, f"Error fetching exchange rate: {e}\n")
        return None
    
    data = response.json()
    if not data:
        return None
    
    rate = list(data.values())[0]
    return rate

def convert_currency():
    "Convert amount from one currency to another"
    clear_output()
    currency1 = entry_currency1.get().upper()
    amount = entry_amount.get().replace(" ", "")
    currency2 = entry_currency2.get().upper()
    
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        output_text.insert(ttk.END, "Invalid currencies or failed to fetch exchange rate.\n")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        output_text.insert(ttk.END, "Invalid amount.\n")
        return
    
    converted_amount = rate * amount
    output_text.insert(ttk.END, f"{amount} {currency1} is equal to {converted_amount} {currency2}\n")

def list_currencies():
    "List all available currencies"
    clear_output()
    currencies = get_currencies()
    if not currencies:
        output_text.insert(ttk.END, "Failed to fetch currencies.\n")
        return
    
    for _, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        output_text.insert(ttk.END, f"{_id} - {name} - {symbol}\n")

def search_currency():
    "Search for a currency by name"
    clear_output()
    search_term = entry_search.get().lower()
    currencies = get_currencies()
    if not currencies:
        output_text.insert(ttk.END, "Failed to fetch currencies.\n")
        return

    for _, currency in currencies:
        currency_name = currency['currencyName'].lower()
        if search_term in currency_name:
            _id = currency['id']
            symbol = currency.get("currencySymbol", "")
            output_text.insert(ttk.END, f"{_id} - {currency['currencyName']} - {symbol}\n")

def show_help():
    "Display help information"
    clear_output()
    help_text = (
        "List = lists the different currencies\n"
        "Convert - convert from one currency to another and get the exchange rate\n"
        "Search - search for a currency by name\n"
        "Toggle Search - show/hide the search entry\n"
    )
    output_text.insert(ttk.END, help_text)

def clear_output():
    "Ckear the output text widget"
    output_text.delete(1.0, ttk.END)

def toggle_search_entry():
    "Toggle the visisbility of the search entry field"
    if entry_search.winfo_ismapped():
        label_search.grid_remove()
        entry_search.grid_remove()
    else:
        label_search.grid()
        entry_search.grid()

def clear_all():
    "Clear all input fields and output text"
    entry_currency1.delete(0, ttk.END)
    entry_amount.delete(0, ttk.END)
    entry_currency2.delete(0, ttk.END)
    entry_search.delete(0, ttk.END)
    clear_output()

#Main GUI setup
root = Tk()
root.title("Currency Converter")

style = ttk.Style("darkly")

frame_input = ttk.Frame(root, padding=(20, 10))
frame_input.pack()

#Input fields
label_currency1 = ttk.Label(frame_input, text="Base Currency:")
label_currency1.grid(row=0, column=0, padx=10, pady=5)
entry_currency1 = ttk.Entry(frame_input, width=20)
entry_currency1.grid(row=0, column=1, padx=10, pady=5)

label_amount = ttk.Label(frame_input, text="Amount:")
label_amount.grid(row=1, column=0, padx=10, pady=5)
entry_amount = ttk.Entry(frame_input, width=20)
entry_amount.grid(row=1, column=1, padx=10, pady=5)

label_currency2 = ttk.Label(frame_input, text="Target Currency:")
label_currency2.grid(row=2, column=0, padx=10, pady=5)
entry_currency2 = ttk.Entry(frame_input, width=20)
entry_currency2.grid(row=2, column=1, padx=10, pady=5)

label_search = ttk.Label(frame_input, text="Search Currency:")
label_search.grid(row=3, column=0, padx=10, pady=5)
entry_search = ttk.Entry(frame_input, width=20)
entry_search.grid(row=3, column=1, padx=10, pady=5)
label_search.grid_remove()
entry_search.grid_remove()

frame_buttons = ttk.Frame(root, padding=(20, 5))
frame_buttons.pack()

#Buttons
button_convert = ttk.Button(frame_buttons, text="Convert", command=convert_currency)
button_convert.pack(side=ttk.LEFT, padx=10)

button_list = ttk.Button(frame_buttons, text="List Currencies", command=list_currencies)
button_list.pack(side=ttk.LEFT, padx=10)

button_search = ttk.Button(frame_buttons, text="Search", command=search_currency)
button_search.pack(side=ttk.LEFT, padx=10)

button_toggle_search = ttk.Button(frame_buttons, text="Toggle Search", command=toggle_search_entry)
button_toggle_search.pack(side=ttk.LEFT, padx=10)

button_help = ttk.Button(frame_buttons, text="Help", command=show_help)
button_help.pack(side=ttk.LEFT, padx=10)

button_clear = ttk.Button(frame_buttons, text="Clear", command=clear_all)
button_clear.pack(side=ttk.LEFT, padx=10)

frame_output = ttk.Frame(root, padding=(20, 10))
frame_output.pack()

#Output text and scrollbar
scrollbar = ttk.Scrollbar(frame_output)
scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

output_text = ttk.Text(frame_output, height=10, width=50, wrap=ttk.WORD, yscrollcommand=scrollbar.set)
output_text.pack()

scrollbar.config(command=output_text.yview)

root.mainloop()
