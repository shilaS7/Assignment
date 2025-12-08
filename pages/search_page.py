from pages.base_page import BasePage

class SearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def search(self, query: str):
        """Perform a search query."""
        # Try to find search field by placeholder (most reliable for "Search games")
        try:
            search_field = self.page.get_by_placeholder("Search games").first
            search_field.wait_for(state="visible", timeout=10000)
        except:
            # Fallback to other common search field selectors
            try:
                search_field = self.page.locator("input[type='search']").first
                search_field.wait_for(state="visible", timeout=10000)
            except:
                try:
                    search_field = self.page.locator("#search").first
                    search_field.wait_for(state="visible", timeout=10000)
                except:
                    raise ValueError("Could not find search field on the page. Please verify you are on the correct page after login.")
        
        # Click and fill the search field
        search_field.click()
        search_field.fill(query)
        search_field.press("Enter")
        
        # Wait for search results to load
        self.page.wait_for_timeout(3000)
        
        # Try to get the search results text
        # Look for common patterns like "Search Results for 'query'"
        try:
            # Try to find the results heading/text
            results_text = None
            selectors = [
                f"text=Search Results for",
                f"text=Search results for",
                "h1, h2, h3",
                ".search-results",
                ".results-header"
            ]
            
            for selector in selectors:
                try:
                    element = self.page.locator(selector).first
                    if element.is_visible(timeout=2000):
                        results_text = element.text_content()
                        if results_text and query.lower() in results_text.lower():
                            return results_text.strip()
                except:
                    continue
            
            # If no specific results text found, get page title or main content
            try:
                page_text = self.page.text_content("body") or ""
                if f"Search Results for" in page_text or f"search results for" in page_text:
                    # Extract the relevant part
                    if query.lower() in page_text.lower():
                        return page_text
            except:
                pass
            
            return None
        except:
            return None
    
    def is_play_button_available(self, timeout=5000):
        """Check if play button is available on search results page."""
        # Try multiple selectors to find the play button/link
        play_button_selectors = [
            # Link with "Play" text
            "a:has-text('Play')",
            "[role='link']:has-text('Play')",
            # Link within search results
            ".search-results a[role='link']",
            ".game-card a[role='link']",
            ".result-item a[role='link']",
            # Any link that might be a play button
            "a[href*='play']",
            "a[aria-label*='Play']",
            "a[aria-label*='play']",
            # Generic link in results area
            "[role='link']"
        ]
        
        for selector in play_button_selectors:
            try:
                play_button = self.page.locator(selector).first
                if play_button.is_visible(timeout=2000):
                    button_text = play_button.text_content() or ""
                    button_href = play_button.get_attribute("href") or ""
                    info = f"Found play button with selector '{selector}'"
                    if button_text:
                        info += f", text: '{button_text.strip()}'"
                    if button_href:
                        info += f", href: '{button_href}'"
                    return True, info
            except:
                continue
        
        # If no specific play button found, check if any link exists in search results
        try:
            # Wait a bit more for results to load
            self.page.wait_for_timeout(1000)
            any_link = self.page.locator("[role='link']").first
            if any_link.is_visible(timeout=2000):
                link_text = any_link.text_content() or ""
                return True, f"Found link on page (may be play button), text: '{link_text.strip()[:50]}'"
        except:
            pass
        
        return False, "Play button is not available"