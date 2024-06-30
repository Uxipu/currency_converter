import tkinter as tk
from tkinter import ttk
from requests import get

BASE_URL = "https://free.currconv.com/"
API_KEY = "0e95030a9c5ba6cee694"

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
        output_text.insert(tk.END, "Invalid currencies or failed to fetch exchange rate.\n")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        output_text.insert(tk.END, "Invalid amount.\n")
        return
    
    converted_amount = rate * amount
    output_text.insert(tk.END, f"{amount} {currency1} is equal to {converted_amount} {currency2}\n")

def list_currencies():
    clear_output()
    currencies = get_currencies()
    if not currencies:
        output_text.insert(tk.END, "Failed to fetch currencies.\n")
        return
    
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        output_text.insert(tk.END, f"{_id} - {name} - {symbol}\n")

def show_help():
    clear_output()
    output_text.insert(tk.END, "List = lists the different currencies\n")
    output_text.insert(tk.END, "Convert - convert from one currency to another\n")
    output_text.insert(tk.END, "Rate - get the exchange rate of two currencies\n")

def clear_output():
    output_text.delete(1.0, tk.END)


root = tk.Tk()
root.title("Currency Converter")


style = ttk.Style()
style.configure("TButton", padding=10, font=('Helvetica', 12))
style.configure("TLabel", font=('Helvetica', 12))
style.configure("TEntry", font=('Helvetica', 12))
style.configure("TText", font=('Helvetica', 12))


frame_input = ttk.Frame(root, padding=(20, 10))
frame_input.pack()

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

frame_buttons = ttk.Frame(root, padding=(20, 5))
frame_buttons.pack()

button_convert = ttk.Button(frame_buttons, text="Convert", command=convert_currency)
button_convert.pack(side=tk.LEFT, padx=10)

button_list = ttk.Button(frame_buttons, text="List Currencies", command=list_currencies)
button_list.pack(side=tk.LEFT, padx=10)

button_help = ttk.Button(frame_buttons, text="Help", command=show_help)
button_help.pack(side=tk.LEFT, padx=10)

frame_output = ttk.Frame(root, padding=(20, 10))
frame_output.pack()

scrollbar = ttk.Scrollbar(frame_output)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(frame_output, height=10, width=50, wrap=tk.WORD, yscrollcommand=scrollbar.set)
output_text.pack()

scrollbar.config(command=output_text.yview)


root.mainloop()
