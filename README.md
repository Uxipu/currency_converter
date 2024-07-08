# **Currency Converter**

A Tkinter-based GUI application to fetch currency data, list currencies, convert amounts between currencies, and get exchange rates using a free currency conversion API.

## **Features**
* List Currencies: Fetch and display a list of available currencies.
* Convert Currency: Convert amounts from one currency to another.
* Exchange Rates: Fetch and display exchange rates between two currencies.
* Search Currency: Search for a specific currency by name.
* Toggle Search: Show/hide the search entry field.
* Help: Display help information about the application

## **Requirements**
* Python 3.x
* requests library
* ttkbootstrap library
* python-dotenv library


## **Setup**
1. Clone the Repository:

   git clone https://github.com/yourusername/currency_converter.git
   cd currency_converter

2. Install Dependencies:

   pip install requests ttkbootstrap python-dotenv

3. Set Up Environment Variables:

   * Create a .env file in the project root directory.
   * Add your API key in the .env file:

   API_KEY=your_api_key_here


## **Usage**
Run the application:

python currency_converter.py

## **GUI Interface**
1. Convert Currency:

   * Enter the base currency, amount, and target currency.
   * Click "Convert" to get the converted amount.

2. List Currencies:

   * Click "List Currencies" to display all available currencies.

3. Search Currency:

   * Click "Toggle Search" to show the search field.
   * Enter the name of the currency and click "Search".

4. Help:

   * Click "Help" to display help information.

5. Clear:

   * Click "Clear" to clear all input fields and output text.


## **Running Tests**

1. Navigate to the Project Directory:

   cd currency_converter

2. Run the Tests:

   python3 -m unittest discover


## **Contributing**
Feel free to submit issues and enhancement requests.

## **License**
This project is licensed under the MIT License.


## **Example of .env file:**

API_KEY=your_api_key_here


## **Example of Running the Application:**

python3 currency_converter.py


## **Example of Running Tests:**

python3 -m unittest discover
