import os
from pages.login_page import LoginPage
from pages.search_page import SearchPage

def test_search(page):
    # Get credentials from environment variables
    email = os.getenv('USERNAME') or os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    # Validate credentials are provided
    if not email:
        raise ValueError("USERNAME or EMAIL environment variable must be set")
    if not password:
        raise ValueError("PASSWORD environment variable must be set")
    
    # Perform login first
    login_page = LoginPage(page)
    login_page.open()
    login_page.go_to_login()
    login_page.enter_email(email)
    login_page.click_next()
    try:
        login_page.page.locator("#password").wait_for(state="visible", timeout=5000)
    except:
        pass
    
    login_page.enter_password(password)
    login_page.click_next()
    page.wait_for_timeout(3000)
    
    # Perform search after login
    search_query = "Solitaire"
    search_page = SearchPage(page)
    actual_results = search_page.search(search_query)
    
    # Expected result text
    expected_result = f"Search Results for \"{search_query}\""
    # Get actual result text for comparison
    if actual_results:
        actual_text = actual_results if isinstance(actual_results, str) else str(actual_results)
    else:
        # Try to get page content as fallback
        try:
            page_text = page.text_content("body") or ""
            # Look for search results heading
            if "Search Results" in page_text or "search results" in page_text:
                actual_text = page_text
            else:
                actual_text = "No search results text found on the page"
        except:
            actual_text = "Unable to retrieve page content"
    
    display_actual = actual_text[:300] + "..." if len(actual_text) > 300 else actual_text
    
    # Assert that expected text is in actual results
    assert expected_result.lower() in actual_text.lower(), (
        f"\n{'='*60}\n"
        f"SEARCH RESULTS ASSERTION FAILED\n"
        f"{'='*60}\n"
        f"Expected: {expected_result}\n"
        f"Actual:   {display_actual}\n"
        f"{'='*60}\n"
    )
    
    print(f"\n✅ Search assertion passed!")
    print(f"Expected: {expected_result}")
    print(f"Actual:   {display_actual}")
    
    # Validate that play button is available
    is_available, button_info = search_page.is_play_button_available()
    
    print(f"\n{'='*60}")
    print(f"PLAY BUTTON VALIDATION")
    print(f"{'='*60}")
    print(f"Expected: Play button should be available")
    print(f"Actual:   {button_info}")
    print(f"{'='*60}\n")
    
    assert is_available, (
        f"\n{'='*60}\n"
        f"PLAY BUTTON VALIDATION FAILED\n"
        f"{'='*60}\n"
        f"Expected: Play button should be available\n"
        f"Actual:   {button_info}\n"
        f"{'='*60}\n"
    )
    
    print(f"✅ Play button validation passed!")
