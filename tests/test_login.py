# from pages.login_page import LoginPage

# def test_login(page):
#     login_page = LoginPage(page)
#     login_page.open()
#     login_page.login(Config.USERNAME, Config.PASSWORD)

#     # assert page.url == "https://www.pogo.com/"
#     # pass

import os
from pages.login_page import LoginPage

def test_should_login_successfully_with_valid_credentials(page):
    email = os.getenv("EMAIL", "")
    password = os.getenv("PASSWORD", "")
    expected_logged_in_url = "/project/dashboard"

    # Perform login
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(email, password)

    # Validate redirection
    assert expected_logged_in_url in page.url

  