from ast import alias
import os
from pages.register_page import RegisterPage
from services.webhook_client import WebhookClient


def test_user_registration(page):
    # WebhookCreate APIRequestContext from page context
    api_request_context = page.request
    webhook = WebhookClient(api_request_context)
    uuid , test_email = webhook.create_token()
   
    # Start registration
    register_page = RegisterPage(page)
    register_page.open()
    register_page.go_to_signup()
    
    #Fill registration form
    selected_country = register_page.select_random_country()
    print(f"🌍 Selected country: {selected_country}")
    register_page.select_month(6)
    register_page.select_day(15)
    register_page.select_year(1990)
    register_page.click_next()

    register_page.enter_email(test_email)
    register_page.send_otp()
    
    #Fetch code from webhook inbox
    code = webhook.wait_for_code(uuid)
    
    # Wait a moment for the page to be ready for verification code entry
    import time
    time.sleep(2)

    # Enter verification code
    register_page.enter_verification_code(code)
    register_page.send_verification_code()
    
    # Generate unique EA ID
    ea_id = register_page.generate_unique_ea_id()
    register_page.enter_ea_id(ea_id)
    register_page.enter_password("Test@123")
    register_page.click_terms_and_conditions()
    register_page.click_create_account()
    register_page.click_finish()
    register_page.click_next_to_login("Next")
    time.sleep(5)
    # Cleanup
    webhook.delete_requests(uuid)
    webhook.delete_token(uuid)

