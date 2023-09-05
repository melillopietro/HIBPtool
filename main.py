import requests
import time

API_KEY = ''
BASE_URL = 'https://haveibeenpwned.com/api/v3/breachedaccount/'

MAX_RETRIES = 5
INITIAL_DELAY = 1  # Initial delay in seconds


def check_breaches(email):
    headers = {'hibp-api-key': API_KEY}
    retries = 0

    while retries < MAX_RETRIES:
        response = requests.get(BASE_URL + email, headers=headers)

        if response.status_code == 429:
            print("Rate limit exceeded. Retrying after delay...")
            time.sleep(INITIAL_DELAY * (2 ** retries))  # Exponential backoff
            retries += 1
        elif response.status_code == 404:
            return f"{email} has not been breached.\n"
        elif response.status_code == 200:
            breaches = ""
            for breach in response.json():
                breaches += f"- {breach['Name']}\n"
            return f"{email} has been breached in the following breaches:\n{breaches}"
        else:
            return f"An error occurred for {email}. Status code: {response.status_code}\n"


def main():
    with open('email_list.txt', 'r') as f:
        email_list = f.read().splitlines()

    results = []

    for email in email_list:
        result = check_breaches(email)
        results.append(result)

    with open('breach_results.txt', 'w') as output_file:
        output_file.writelines(results)


if __name__ == "__main__":
    main()
