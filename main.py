import requests


def get_exchange_rate():
    """
    Fetches USD and EUR exchange rates from PrivatBank and Monobank APIs.
    Determines where it is better to buy or sell based on user input.
    """
    privatbank_url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    monobank_url = "https://api.monobank.ua/bank/currency"

    try:
        # Get user choice for action and currency
        action = input("Do you want to 'buy' or 'sell' UAH? (type 'buy' or 'sell'): ").strip().lower()
        if action not in ['buy', 'sell']:
            print("Invalid choice. Please type 'buy' or 'sell'.")
            return

        currency = input("Which currency do you want to exchange? (type 'USD' or 'EUR'): ").strip().upper()
        if currency not in ['USD', 'EUR']:
            print("Invalid currency. Please type 'USD' or 'EUR'.")
            return

        # Map currency to codes
        currency_codes = {
            'USD': {'privatbank': 'USD', 'monobank_code': 840},
            'EUR': {'privatbank': 'EUR', 'monobank_code': 978}
        }

        # Fetch PrivatBank exchange rates
        privatbank_response = requests.get(privatbank_url)
        privatbank_response.raise_for_status()
        privatbank_data = privatbank_response.json()

        # Extract PrivatBank rates
        privatbank_currency = next(
            item for item in privatbank_data if item['ccy'] == currency_codes[currency]['privatbank'])
        privatbank_rate = float(privatbank_currency['buy' if action == 'buy' else 'sale'])  # 'buy' or 'sell'

        # Fetch Monobank exchange rates
        monobank_response = requests.get(monobank_url)
        monobank_response.raise_for_status()
        monobank_data = monobank_response.json()

        # Extract Monobank rates
        monobank_currency = next(item for item in monobank_data
                                 if item['currencyCodeA'] == currency_codes[currency]['monobank_code'] and item[
                                     'currencyCodeB'] == 980)
        monobank_rate = float(monobank_currency['rateBuy' if action == 'buy' else 'rateSell'])

        # Determine the better option
        if action == 'buy':
            # Lower rate is better for buying
            better_bank = "PrivatBank" if privatbank_rate < monobank_rate else "Monobank"
            better_rate = min(privatbank_rate, monobank_rate)
        else:
            # Higher rate is better for selling
            better_bank = "PrivatBank" if privatbank_rate > monobank_rate else "Monobank"
            better_rate = max(privatbank_rate, monobank_rate)

        # Output comparison results
        print(f"\nPrivatBank {currency} {action.capitalize()} Rate: {privatbank_rate} UAH/{currency}")
        print(f"Monobank {currency} {action.capitalize()} Rate: {monobank_rate} UAH/{currency}")
        print(f"It is better to {action} {currency} at {better_bank} at a rate of {better_rate} UAH/{currency}.\n")

    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function
get_exchange_rate()
