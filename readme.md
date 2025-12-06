Setup and Run Locally
Step 1: Clone the repository
    git clone <Repo URL>
    cd <Project folder name>

Step 2: Create a Virtual Environment
    Mac/linux
    python3 -m venv .venv
    source .venv/bin/activate

    ⚠️ IMPORTANT: You must activate the virtual environment in EACH new terminal session:
       cd /Users/shilashrestha/Assignment source .venv/bin/activate source .venv/bin/activate

Step 3: Install Dependencies
    pip install -r requirements.txt

Step 4: Install Playwright Browsers
    playwright install

Step 5: Set Up Environment Variables

Step 6: Run Tests Locally
    ⚠️ Make sure your virtual environment is activated first!
    
    pytest
    Run tests in headed mode (Browser Visible)
    pytest --headed
    Generate HTML Report
    pytest --html=report.html