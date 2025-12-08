import os
from pages.login_page import LoginPage
from pages.signout_page import SignoutPage

def test_login_signout_login_flow(page):
    # Get credentials from environment variables
    email = os.getenv('USERNAME') or os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    # Perform initial login
    print(f"\n{'='*60}")
    print(f"INITIAL LOGIN")
    print(f"{'='*60}")
    login_page = LoginPage(page)
    login_page.open()
    login_page.go_to_login()
    login_page.enter_email(email)
    login_page.click_next()
    
    # Wait for password field
    try:
        login_page.page.locator("#password").wait_for(state="visible", timeout=5000)
    except:
        pass
    
    login_page.enter_password(password)
    login_page.click_next()
    page.wait_for_timeout(3000)
    print(f"✅ Initial login completed")
    
    #Perform signout
    print(f"\n{'='*60}")
    print(f"SIGNOUT")
    print(f"{'='*60}")
    signout_page = SignoutPage(page)
    signout_page.profile_dropdown()
    signout_page.sign_out_button()
    page.wait_for_timeout(3000)
    
    # Validate signout,should redirect to home page
    expected_url = "https://www.pogo.com/signout"
    actual_url = page.url
    print(f"Expected URL after signout: {expected_url}")
    print(f"Actual URL: {actual_url}")
    
    assert expected_url in actual_url or actual_url == expected_url, (
        f"\n{'='*60}\n"
        f"SIGNOUT VALIDATION FAILED\n"
        f"{'='*60}\n"
        f"Expected URL: {expected_url}\n"
        f"Actual URL: {actual_url}\n"
        f"{'='*60}\n"
    )
    print(f"✅ Signout completed and validated")
    
    #Login again
    login_page = LoginPage(page)
    login_page.open()
    login_page.go_to_login()
    login_page.enter_email(os.getenv('USERNAME'))
    login_page.click_next()
    login_page.enter_password(os.getenv('PASSWORD'))
    login_page.click_next()
    page.wait_for_timeout(3000)
    print(f"✅ Second login completed")
    