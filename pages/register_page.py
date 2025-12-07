from pages.base_page import BasePage
from config.config import Config

class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def open(self):
        self.page.goto(Config.BASE_URL)

    def go_to_signup(self):
        self.page.get_by_role("button", name="Register free").click()

    
    def select_country(self, country: str):
        country_dropdown = self.page.locator("#clientreg_country-selctrl")
        country_dropdown.wait_for(state="visible")
        country_dropdown.click()
        # Wait for dropdown menu to open
        self.page.wait_for_timeout(500)
        # Try using select_option if it's a native select element
        try:
            self.page.select_option("#clientreg_country-selctrl", label=country)
        except:
            # If select_option doesn't work, it's likely a custom dropdown
            # Look for the option in the dropdown menu (could be in option tags or list items)
            # Try option element first - use filter approach
            try:
                select_element = self.page.locator("#clientreg_country-selctrl")
                country_option = select_element.locator("option").filter(has_text=country).nth(0)
                country_option.wait_for(state="attached", timeout=3000)
                country_option.click()
            except:
                # If option doesn't work, try finding by text in the visible dropdown menu
                # The dropdown might have opened a menu with the options
                self.page.get_by_text(country, exact=True).filter(
                    has=self.page.locator("option, li, [role='option']")
                ).nth(0).click()
    
    def select_random_country(self):
        """Select a random country from a predefined list"""
        import random
        # Common countries that are typically available in registration forms
        countries = [
            "Nepal", "United States", "United Kingdom", "India", "Canada", 
            "Australia", "Germany", "France", "Japan", "China", "Brazil", 
            "Mexico", "Spain", "Italy", "South Korea", "Netherlands", 
            "Sweden", "Norway", "Denmark", "Finland", "Poland", "Portugal"
        ]
        random_index = random.randint(0, len(countries) - 1)
        selected_country = countries[random_index]
        self.select_country(selected_country)
        return selected_country
        
    def select_month(self, month: int):
        """Select month from dropdown - accepts static value (1-12)"""
        month_dropdown = self.page.locator("#clientreg_dobmonth-selctrl")
        month_dropdown.wait_for(state="visible")
        month_dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try multiple approaches to find and select the month
        try:
            # First try: select by value
            self.page.select_option("#clientreg_dobmonth-selctrl", value=str(month))
        except:
            try:
                # Second try: select by label
                self.page.select_option("#clientreg_dobmonth-selctrl", label=str(month))
            except:
                # Third try: find option by text and click
                select_element = self.page.locator("#clientreg_dobmonth-selctrl")
                month_option = select_element.locator("option").filter(has_text=str(month)).first
                month_option.click()
    
    def select_day(self, day: int):
        """Select day from dropdown - accepts static value (1-31)"""
        day_dropdown = self.page.locator("#clientreg_dobday-selctrl")
        day_dropdown.wait_for(state="visible")
        day_dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try multiple approaches to find and select the day
        try:
            self.page.select_option("#clientreg_dobday-selctrl", value=str(day))
        except:
            try:
                self.page.select_option("#clientreg_dobday-selctrl", label=str(day))
            except:
                select_element = self.page.locator("#clientreg_dobday-selctrl")
                day_option = select_element.locator("option").filter(has_text=str(day)).first
                day_option.click()
    
    def select_year(self, year: int):
        """Select year from dropdown - accepts static value (e.g., 1990)"""
        year_dropdown = self.page.locator("#clientreg_dobyear-selctrl")
        year_dropdown.wait_for(state="visible")
        year_dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try multiple approaches to find and select the year
        try:
            self.page.select_option("#clientreg_dobyear-selctrl", value=str(year))
        except:
            try:
                self.page.select_option("#clientreg_dobyear-selctrl", label=str(year))
            except:
                select_element = self.page.locator("#clientreg_dobyear-selctrl")
                year_option = select_element.locator("option").filter(has_text=str(year)).first
                year_option.click()

    # def enter_dob(self, day: int = None, month: int = None, year: int = None):
    #     """
    #     Enter date of birth
    #     Args:
    #         day: Day of month (1-31), optional - defaults to random if not provided
    #         month: Month (1-12), optional - defaults to random if not provided
    #         year: Year, optional - defaults to random if not provided
    #     """
    #     import random
    #     from datetime import datetime
        
    #     # Generate random values if not provided
    #     if day is None:
    #         day = random.randint(1, 28)
    #     if month is None:
    #         month = random.randint(1, 12)
    #     if year is None:
    #         current_year = datetime.now().year
    #         year = random.randint(current_year - 65, current_year - 18)
        
    #     # Select month
    #     month_select = self.page.locator("[id*='dobMonth'], select[name*='month']").first
    #     month_select.wait_for(state="visible")
    #     try:
    #         month_select.select_option(label=str(month))
    #     except:
    #         month_select.select_option(value=str(month))
        
    #     # Select day
    #     day_select = self.page.locator("#clientreg_dobday-selctrl, [id*='dobday'], select[name*='day']").first
    #     day_select.wait_for(state="visible")
    #     try:
    #         day_select.select_option(label=str(day))
    #     except:
    #         day_select.select_option(value=str(day))
        
    #     # Select year
    #     year_select = self.page.locator("[id*='dobYear'], select[name*='year']").first
    #     year_select.wait_for(state="visible")
    #     try:
    #         year_select.select_option(label=str(year))
    #     except:
    #         year_select.select_option(value=str(year))
    def click_next(self):
        self.page.click("#countryDobNextBtn")

    def enter_email(self, email: str):
        email_field = self.page.locator("#email")
        email_field.wait_for(state="visible")
        email_field.fill(email)
        self.page.keyboard.press("Tab")
        # Verify email was entered correctly
        entered_email = email_field.input_value()
        print(f"📧 Email entered: {entered_email}")
        assert entered_email == email, f"Email mismatch! Expected: {email}, Got: {entered_email}" 
    
    def send_otp(self):
        print("📤 Clicking send OTP button...")
        self.page.click("#basicInfoNextBtn")
        
        # Wait a moment for any immediate validation errors
        self.page.wait_for_timeout(1000)
        
        # Check for error messages
        error_selectors = [
            "[role='alert']",
            ".error",
            ".error-message",
            "[class*='error']",
            "[id*='error']"
        ]
        
        for selector in error_selectors:
            try:
                error_element = self.page.locator(selector).first
                if error_element.is_visible(timeout=500):
                    error_text = error_element.text_content()
                    print(f"⚠️ Error detected: {error_text}")
            except:
                pass
        
        # Wait for OTP to be sent - wait for either a success message, 
        # verification code input field to appear, or a loading state to complete
        print("⏳ Waiting for page to process OTP request...")
        
        # Wait for any loading indicators to disappear
        self.page.wait_for_timeout(2000)
        
        # Check for success message or verification field
        verification_selectors = [
            "#verification-code",
            "#verificationCode", 
            "#verification_code",
            "input[name*='verification']",
            "input[name*='code']",
            "[id*='verification']"
        ]
        
        field_found = False
        for selector in verification_selectors:
            try:
                field = self.page.locator(selector).first
                if field.is_visible(timeout=3000):
                    print(f"✅ Verification code field appeared with selector: {selector}")
                    field_found = True
                    break
            except:
                continue
        
        if not field_found:
            print("⚠️ Verification field not found immediately, but OTP request was sent")
            print("   Will wait for email and then try to find the field again")

    def enter_password(self, password: str):
        self.page.fill("#password", password)

    def submit(self):
        self.page.click("button[type=submit]")

    def enter_verification_code(self, code: str):
        print(f"🔑 Attempting to enter verification code: {code}")
        
        # Try multiple possible selectors for verification code field
        possible_selectors = [
            "#verification-code",
            "#verificationCode",
            "#verification_code",
            "input[name='verification-code']",
            "input[name='verificationCode']",
            "input[name='verification_code']",
            "input[type='text'][placeholder*='code' i]",
            "input[type='text'][placeholder*='verification' i]",
            "input[type='number']",
            "[id*='verification']",
            "[id*='code']",
            "[name*='verification']",
            "[name*='code']"
        ]
        
        verification_field = None
        for selector in possible_selectors:
            try:
                print(f"🔍 Trying selector: {selector}")
                field = self.page.locator(selector).first
                field.wait_for(state="visible", timeout=5000)
                if field.is_visible():
                    verification_field = field
                    print(f"✅ Found verification field with selector: {selector}")
                    break
            except:
                continue
        
        if not verification_field:
            # Debug: print all input fields on the page
            print("🔍 Debugging: Looking for input fields on the page...")
            all_inputs = self.page.locator("input").all()
            print(f"📋 Found {len(all_inputs)} input fields")
            for i, inp in enumerate(all_inputs[:10]):  # Show first 10
                try:
                    inp_id = inp.get_attribute("id") or "no-id"
                    inp_name = inp.get_attribute("name") or "no-name"
                    inp_type = inp.get_attribute("type") or "no-type"
                    inp_placeholder = inp.get_attribute("placeholder") or "no-placeholder"
                    print(f"  Input {i+1}: id='{inp_id}', name='{inp_name}', type='{inp_type}', placeholder='{inp_placeholder}'")
                except:
                    pass
            
            raise Exception(f"❌ Could not find verification code field. Tried selectors: {possible_selectors}")
        
        verification_field.fill(code)
        print(f"✅ Verification code entered successfully")

    def send_verification_code(self):
        self.page.click("#btnSendCode")


    def click_verify(self):
        # Try multiple possible selectors for verify button
        possible_selectors = [
            "#verify-button",
            "#verifyButton",
            "#verify_button",
            "button[type='submit']",
            "button:has-text('Verify')",
            "button:has-text('Continue')",
            "[id*='verify']",
            "[name*='verify']"
        ]
        
        verify_button = None
        for selector in possible_selectors:
            try:
                button = self.page.locator(selector).first
                if button.is_visible(timeout=2000):
                    verify_button = button
                    print(f"✅ Found verify button with selector: {selector}")
                    break
            except:
                continue
        
        if not verify_button:
            raise Exception(f"❌ Could not find verify button. Tried selectors: {possible_selectors}")
        
        verify_button.click()
        print("✅ Verify button clicked")