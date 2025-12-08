from pages.base_page import BasePage
from config.config import Config

class LoginPage(BasePage):
    username_field = "input[name='username']"
    password_field = "input[name='password']"
    login_button = "button[type='submit']"

    def open(self):
        self.navigate(Config.BASE_URL)

    def go_to_login(self):
        self.page.get_by_role("button", name="Sign In").click()
    
    def enter_email(self, email: str):
        self.page.fill("#email", email)
    
    def click_next(self):
        self.page.click("#logInBtn")
    
    def enter_password(self, password: str):
        self.page.type("#password", password,delay=100)
        print(f"Typed password: {password}")
        self.page.keyboard.press("Tab")

    def validation_tooltip_pogime(self):
        tooltip_element = self.page.locator("#clubBenefitsFTUE4")
        tooltip_element.wait_for(state="visible", timeout=10000)
        tooltip_element.hover()
        
        self.page.wait_for_timeout(2000)
        
        # Find tooltip using common selectors
        tooltip_selectors = [
            "[role='tooltip']",
            ".tooltip",
            ".popover",
            "[class*='tooltip']",
            "text=Message & Gift Inbox"
        ]
        
        actual_tooltip = ""
        for selector in tooltip_selectors:
            try:
                tooltip = self.page.locator(selector).first
                if tooltip.is_visible(timeout=1000):
                    actual_tooltip = tooltip.text_content() or ""
                    if actual_tooltip:
                        break
            except:
                continue
        
        expected_tooltip = "Message & Gift Inbox"
        assert expected_tooltip in actual_tooltip, f"Expected tooltip '{expected_tooltip}' not found. Found: '{actual_tooltip}'"
      