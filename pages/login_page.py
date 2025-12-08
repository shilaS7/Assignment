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

    def validation_tooltip_message_menu(self):
        tooltip_element = self.page.locator("#clubBenefitsFTUE4")
        tooltip_element.wait_for(state="visible", timeout=10000)
        tooltip_element.hover()
        
        # Wait for tooltip to appear
        self.page.wait_for_timeout(2000)
        
        # Try to find tooltip by text first (most reliable)
        try:
            tooltip_by_text = self.page.get_by_text("Message & Gift Inbox", exact=False)
            if tooltip_by_text.is_visible(timeout=2000):
                return tooltip_by_text.text_content() or ""
        except:
            pass
        
        # Try aria-describedby approach
        try:
            aria_describedby = tooltip_element.get_attribute("aria-describedby")
            if aria_describedby:
                described_element = self.page.locator(f"#{aria_describedby}")
                if described_element.is_visible(timeout=2000):
                    return described_element.text_content() or ""
        except:
            pass
        
        # Find tooltip using common selectors
        tooltip_selectors = [
            "[role='tooltip']",
            ".tooltip",
            ".popover",
            "[class*='tooltip']",
            "[class*='Tooltip']",
            "[id*='tooltip']"
        ]
        
        for selector in tooltip_selectors:
            try:
                tooltip = self.page.locator(selector).first
                if tooltip.is_visible(timeout=2000):
                    text = tooltip.text_content() or ""
                    if text and "Message" in text:
                        return text
            except:
                continue
        
        # Last resort: search all visible elements for the text
        try:
            all_elements = self.page.locator("body").locator("*")
            count = all_elements.count()
            for i in range(min(count, 100)):  # Limit search to first 100 elements
                try:
                    element = all_elements.nth(i)
                    if element.is_visible():
                        text = element.text_content() or ""
                        if "Message & Gift Inbox" in text:
                            return text
                except:
                    continue
        except:
            pass
        
        return ""
      