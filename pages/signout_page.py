from pages.base_page import BasePage

class SignoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
    
    def profile_dropdown(self):
        # Try to find profile dropdown in header area (most common location)
        # Strategy 1: Look in header/banner for the profile button
        try:
            header = self.page.locator("header, [role='banner']").first
            if header.is_visible(timeout=2000):
                # Get all buttons in header and use the last one (usually profile)
                header_buttons = header.locator("[role='button']")
                button_count = header_buttons.count()
                if button_count > 0:
                    # Use the last button in header (profile dropdown is usually last)
                    profile_dropdown = header_buttons.nth(button_count - 1)
                    profile_dropdown.wait_for(state="visible", timeout=5000)
                    profile_dropdown.click()
                    self.page.wait_for_timeout(500)
                    # Verify Sign Out button appeared
                    sign_out = self.page.get_by_text("Sign Out")
                    if sign_out.is_visible(timeout=2000):
                        return profile_dropdown
        except Exception as e:
            print(f"Strategy 1 failed: {e}")
        
        # Strategy 2: Try finding button that reveals Sign Out when clicked
        # Check buttons from the end (profile is usually near the end)
        try:
            all_buttons = self.page.locator("[role='button']")
            count = all_buttons.count()
            # Check last 10 buttons (profile dropdown is usually in this range)
            for i in range(max(0, count - 10), count):
                try:
                    btn = all_buttons.nth(i)
                    if btn.is_visible(timeout=1000):
                        btn.click()
                        self.page.wait_for_timeout(500)
                        # Check if Sign Out appeared
                        sign_out = self.page.get_by_text("Sign Out")
                        if sign_out.is_visible(timeout=1000):
                            return btn
                except:
                    continue
        except Exception as e:
            print(f"Strategy 2 failed: {e}")
        
        # Strategy 3: Fallback - use last button in header
        header = self.page.locator("header, [role='banner']").first
        header_buttons = header.locator("[role='button']")
        button_count = header_buttons.count()
        if button_count > 0:
            profile_dropdown = header_buttons.nth(button_count - 1)
            profile_dropdown.wait_for(state="visible", timeout=10000)
            profile_dropdown.click()
            return profile_dropdown
        
        raise Exception("Could not find profile dropdown button")
    
    def sign_out_button(self):
        sign_out_btn = self.page.get_by_text("Sign Out")
        sign_out_btn.wait_for(state="visible", timeout=10000)
        sign_out_btn.click()
        return sign_out_btn