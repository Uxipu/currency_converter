from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://open.er-api.com/v6/latest" 

printer = PrettyPrinter()

def get_currencies():
    
    url = BASE_URL
    response = get(url)
    
    if response.status_code == 200:
        data = response.json()
        printer.pprint(data)
    else:
        print(f"Error: unable to fetch currencies (Status Code: {response.status_code})")
        print("Response content:", response.content.decode())    
    
get_currencies()