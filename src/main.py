from datetime import datetime

import requests
from openvpn_api import VPN
import os
import subprocess
import time




# Skyscanner API key and URL
SKYSCANNER_API_KEY = 'your_api_key'
BASE_URL = 'https://partners.api.skyscanner.net/apiservices/browseroutes/v1.0'

# VPN credentials and country codes
VPN_CREDENTIALS = 'https://wpc7845129678.openvpn.com'
COUNTRIES = [
    {'name': 'India', 'vpn_code': 'IN', 'skyscanner_code': 'IN'},
    # Add more countries here
]

def connect_to_vpn():
    """Connect to the VPN using the given country code."""
    vpn = VPN(host="100.96.1.16")
    #vpn.connect(credentials=VPN_CREDENTIALS, config_file=f'config/{country_code}.ovpn')
    vpn.connection()
    vpn.connect()
    return vpn

def disconnect_from_vpn(vpn):
    """Disconnect from the VPN."""
    vpn.disconnect()

def get_cheapest_flight(country, origin, destination, date):
    """Get the cheapest flight price for the given country, origin, destination, and date."""
    vpn = connect_to_vpn(country['vpn_code'])
    url = f"{BASE_URL}/ES/EUR/{country['skyscanner_code']}/{origin}/{destination}/{date}"
    headers = {'apikey': SKYSCANNER_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    disconnect_from_vpn(vpn)
    return min(quote['MinPrice'] for quote in data['Quotes']) if 'Quotes' in data else None

def main():
    """Main function that gets the cheapest flight prices for each country."""
    origin = 'MAD'  # Example: Madrid Airport (MAD)
    destination = 'JFK'  # Example: New York Airport (JFK)
    date = datetime.now().strftime('%Y-%m-%d')

    for country in COUNTRIES:
        if price := get_cheapest_flight(country, origin, destination, date):
            print(f"Country: {country['name']} - Price: {price} EUR - Origin: {origin} - Destination: {destination}")
        else:
            print(f"Country: {country['name']} - No flights found - Origin: {origin} - Destination: {destination}")

if __name__ == '__main__':
    connect_to_vpn()