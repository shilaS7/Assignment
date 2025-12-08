import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page(request):
    # Create videos directory if it doesn't exist
    videos_dir = os.path.join(os.getcwd(), "videos")
    os.makedirs(videos_dir, exist_ok=True)
    
    # Get test name for video filename
    test_name = request.node.name.replace("::", "_").replace("/", "_")
    video_path = os.path.join(videos_dir, f"{test_name}.webm")
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        # Enable video recording - videos will be saved in videos_dir
        context = browser.new_context(
            record_video_dir=videos_dir,
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        yield page
        
        # Close page and context to save video
        page.close()
        context.close()
        browser.close()
        
        # Rename the video file to match test name
        # Playwright saves videos with random names, so we find the most recent one
        try:
            video_files = [f for f in os.listdir(videos_dir) if f.endswith(('.webm', '.mp4'))]
            if video_files:
                # Sort by modification time, get the most recent
                video_files.sort(key=lambda x: os.path.getmtime(os.path.join(videos_dir, x)), reverse=True)
                latest_video = os.path.join(videos_dir, video_files[0])
                # Rename to test name
                if os.path.exists(video_path):
                    os.remove(video_path)  # Remove old video if exists
                os.rename(latest_video, video_path)
                print(f"📹 Video saved: {video_path}")
        except Exception as e:
            print(f"⚠️ Could not rename video file: {e}")
        
"""@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def playwright_instance():
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
"""