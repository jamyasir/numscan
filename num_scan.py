 
import argparse
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

def is_valid_phone_number(phonenumber: str):
    try:
        parsed_number = phonenumbers.parse("+" + phonenumber)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False

def get_ip_info():
    try:
        ip_info = requests.get('https://ipinfo.io/json').json()
        return ip_info
    except Exception as e:
        print(f"Failed to fetch IP information: {e}")
        return None

def parse_phonenumber(phonenumber: str):
    if not is_valid_phone_number(phonenumber):
        print("[!] Invalid phone number.")
        return

    parsed_phonenumber = phonenumbers.parse("+" + phonenumber)
    print(f"[*] Parsed Phone Number: {parsed_phonenumber}")
    print(f"[*] Valid: {phonenumbers.is_valid_number(parsed_phonenumber)}")
    print(f"[*] Possible: {phonenumbers.is_possible_number(parsed_phonenumber)}")
    print(f"[*] Number Type: {phonenumbers.number_type(parsed_phonenumber)}")
    print(f"[*] Network Provider: {carrier.name_for_number(parsed_phonenumber,'en')}")
    print(f"[*] Location: {geocoder.description_for_number(parsed_phonenumber,  'en')}")

    # Get Timezone Information
    time_zone_info = timezone.time_zones_for_number(parsed_phonenumber)
    if time_zone_info:
        print(f"[*] Time Zone: {time_zone_info[0]}")

    # Get IP information
    ip_info = get_ip_info()
    if ip_info:
        print(f"[*] IP Address: {ip_info['ip']}")
        print(f"[*] Location (IP): {ip_info['city']}, {ip_info['region']}, {ip_info['country']}")
        
        # Get coordinates if available
        if 'loc' in ip_info:
            latitude, longitude = map(float, ip_info['loc'].split(','))
            print(f"[*] Coordinates: Latitude {latitude}, Longitude {longitude}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=Markdown(
            """
# Phone Number Info
> Simple script to get phone number information.""",
            style="argparse.text",
        ),
        epilog=Markdown(
            """
# by [Jam Yasir](https://facebook.com/jamyasir.jam.581)

MIT License

Copyright (c) 2023-2024 Jam Yasir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        ),
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument(
        "phonenumber", help="target phone number with country code (without `+`)"
    )
    parser.add_argument(
        "-o", "--output", help="save results to a file", action="store_true"
    )
    args = parser.parse_args()
    try:
        print(
            """
      ┏┓┓         ┳┓     ┓       ┳  ┏  
      ┃┃┣┓┏┓┏┓┏┓  ┃┃┓┏┏┳┓┣┓┏┓┏┓  ┃┏┓╋┏┓
      ┣┛┛┗┗┛┛┗┗   ┛┗┗┻┛┗┗┗┛┗ ┛   ┻┛┗┛┗┛ 
      ┌┐ ┬ ┬
      ├┴┐└┬┘
      └─┘ ┴ 
      ╔╦╗┬─┐  ╦ ╦╔═╗╔═╗
      ║║║├┬┘  ║ ║╠╣ ║ ║
      ╩ ╩┴└─  ╚═╝╚  ╚═╝
        """
        )
        parse_phonenumber(phonenumber=args.phonenumber)
    except Exception as e:
        print(f"Error: {e}")


