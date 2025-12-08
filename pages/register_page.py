import random
import string
from pages.base_page import BasePage
from config.config import Config

class RegisterPage(BasePage):
    """Page object for registration page."""
    
    def __init__(self, page):
        super().__init__(page)
    
    def open(self):
        """Open the registration page."""
        self.page.goto(Config.BASE_URL)
    
    def go_to_signup(self):
        """Click the register button to start signup."""
        self.page.get_by_role("button", name="Register free").click()
    
    def select_country(self, country: str):
        """Select country from dropdown."""
        dropdown = self.page.locator("#clientreg_country-selctrl")
        dropdown.wait_for(state="visible")
        dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try different methods to select country
        try:
            self.page.select_option("#clientreg_country-selctrl", label=country)
        except:
            try:
                dropdown.locator("option").filter(has_text=country).first.click()
            except:
                self.page.get_by_text(country, exact=True).first.click()
    
    def select_random_country(self):
        """Select a random country from the list."""
        countries = [
            "Nepal", "United States", "United Kingdom", "India", "Canada",
            "Australia", "Germany", "France", "Japan", "China", "Brazil",
            "Mexico", "Spain", "Italy", "South Korea", "Netherlands",
            "Sweden", "Norway", "Denmark", "Finland", "Poland", "Portugal"
        ]
        country = random.choice(countries)
        self.select_country(country)
        print(f"🌍 Selected country: {country}")
        return country
    
    def _select_dropdown_option(self, selector: str, value: str):
        """Helper method to select an option from a dropdown."""
        dropdown = self.page.locator(selector)
        dropdown.wait_for(state="visible")
        dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try different selection methods
        try:
            self.page.select_option(selector, value=value)
        except:
            try:
                self.page.select_option(selector, label=value)
            except:
                dropdown.locator("option").filter(has_text=value).first.click()
    
    def select_month(self, month: int):
        """Select month (1-12)."""
        self._select_dropdown_option("#clientreg_dobmonth-selctrl", str(month))
    
    def select_day(self, day: int):
        """Select day (1-31)."""
        self._select_dropdown_option("#clientreg_dobday-selctrl", str(day))
    
    def select_year(self, year: int):
        """Select year."""
        self._select_dropdown_option("#clientreg_dobyear-selctrl", str(year))
    
    def click_next(self):
        """Click next button after DOB selection."""
        self.page.click("#countryDobNextBtn")
    
    def enter_email(self, email: str):
        """Enter email address."""
        field = self.page.locator("#email")
        field.wait_for(state="visible")
        field.fill(email)
        self.page.keyboard.press("Tab")
        print(f"📧 Email entered: {email}")
    
    def send_otp(self):
        """Click button to send OTP."""
        print("📤 Sending OTP...")
        self.page.click("#basicInfoNextBtn")
        self.page.wait_for_timeout(2000)  # Wait for OTP to be sent
    
    def enter_verification_code(self, code: str):
        """Enter verification code."""
        print(f"🔑 Entering verification code: {code}")
        
        # Wait for the verification code field to appear after OTP is sent
        field = self.page.locator("#emailVerifyCode")
        field.wait_for(state="visible", timeout=10000)
        field.fill(code)
        print("✅ Verification code entered")
    
    def send_verification_code(self):
        """Click button to send/verify the code."""
        self.page.click("#btnSendCode")
        
    @staticmethod
    def generate_unique_ea_id() -> str:
        """Generate a unique fake EA ID.
        
        Returns:
            A unique EA ID string with format: Bonsoir followed by 3 random digits
        """
        # Generate 3 random digits
        random_digits = ''.join(random.choices(string.digits, k=3))
        ea_id = f"Bonsoir{random_digits}"
        print(f"🆔 Generated EA ID: {ea_id}")
        return ea_id
    
    def enter_ea_id(self, ea_id: str):
        """Enter EA ID."""
        self.page.fill("#originId", ea_id)
    
    def enter_password(self, password: str):
        """Enter password."""
        self.page.type("#password", password)
        self.page.keyboard.press("Tab")

    def click_terms_and_conditions(self):
        """Click terms and conditions checkbox."""
        self.page.click("#read-accept-container")
    
    def click_create_account(self):
        """Click create account button."""
        self.page.click("#basicInfoNextBtn")
    def click_finish(self):
        """Click finish button."""
        self.page.click("#submitBtn")
    def click_next_to_login(self, button_name: str = "Next to Login"):
        self.page.get_by_role("button", name=button_name).click()