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
    login_page.go_to_login()
    login_page.enter_email(os.getenv('USERNAME'))
    login_page.click_next()
    login_page.enter_password(os.getenv('PASSWORD'))
    login_page.click_next()
    page.wait_for_timeout(5000)
    
    # Validate tooltip
    actual_tooltip = login_page.validation_tooltip_pogime()
    expected_tooltip = "Message & Gift Inbox"
    
    print(f"\n{'='*60}")
    print(f"TOOLTIP VALIDATION")
    print(f"{'='*60}")
    print(f"Expected: {expected_tooltip}")
    print(f"Actual:   {actual_tooltip}")
    print(f"{'='*60}\n")
    
    assert expected_tooltip in actual_tooltip, (
        f"\n{'='*60}\n"
        f"TOOLTIP VALIDATION FAILED\n"
        f"{'='*60}\n"
        f"Expected: {expected_tooltip}\n"
        f"Actual:   {actual_tooltip}\n"
        f"{'='*60}\n"
    )
    
    print(f"✅ Tooltip validation passed!")
    
    # Validate redirection
    # assert expected_logged_in_url in page.url

  