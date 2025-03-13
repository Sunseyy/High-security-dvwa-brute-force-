Brute Force Login Script for DVWA

Overview

This Python script performs a brute-force attack on the Damn Vulnerable Web Application (DVWA) login page by attempting username and password combinations from specified wordlists. It handles CSRF tokens, implements request throttling to avoid detection, and allows users to provide custom username and password lists.

Features

Extracts CSRF tokens dynamically.

Detects login failure response length to differentiate between failed and successful attempts.

Supports user-defined or default username and password lists.

Implements random throttling between login attempts.

Validates custom wordlist paths before usage.

Requirements

Python 3.x

requests library

A running instance of DVWA

Installation

Clone this repository:

git clone https://github.com/your-username/brute-force-dvwa.git
cd brute-force-dvwa

Install required dependencies:

pip install requests

Usage

Run the script:

python brute_force.py

Options:

The script will ask if you want to provide a custom username and password list.

If yes, enter the paths to the username and password files.

If no, the script will use the default lists.

Configuration

You can modify the following variables inside brute_force.py:

target: The URL of the DVWA login page.

cookies: Authentication cookies for the DVWA session.

default_username_list: Path to the default username wordlist.

default_passwords_list: Path to the default password wordlist.

min_delay & max_delay: Adjusts throttling delay between requests.

Example Output

Do you want to enter a custom username and password list? (yes/no): no
[*] Using default username and password lists.
Trying admin:123456 - Response Length: 3024
[-] Waiting 2.34 seconds before next attempt.
Trying admin:password - Response Length: 2789
[+] Found credentials: admin:password

Disclaimer

This script is intended for educational and security research purposes only. Do not use it for unauthorized access or illegal activities. The author is not responsible for any misuse.

License

This project is licensed under the MIT License.

