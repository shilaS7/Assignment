Setup and Run Locally</br>
Step 1: Clone the repository
        </br> git clone "<Repo URL>"
        </br> cd "<Project folder name>"
        </br>Example: git clone https://github.com/shilaS7/Assignment.git

Step 2: Create a Virtual Environment
    </br>Mac/linux
    </br>python3 -m venv .venv
    </br>source .venv/bin/activate

    ⚠️ IMPORTANT: You must activate the virtual environment in EACH new terminal session:
       cd /Users/shilashrestha/Assignment source .venv/bin/activate source .venv/bin/activate

Step 3: Install Dependencies
    </br> pip install -r requirements.txt

Step 4: Install Playwright Browsers
    </br>playwright install

Step 5: Set Up Environment Variables

Step 6: Run Tests Locally
    ⚠️ Make sure your virtual environment is activated first!
    
    pytest
    Run tests in headed mode (Browser Visible)
    pytest --headed
    Generate HTML Report
    pytest --html=report.html

    pytest tests/test_register.py --headed --html=report.html
    pytest tests/test_login.py --headed --html=report.html  
    pytest tests/test_search.py --headed --html=report.html  
    pytest tests/test_signout.py --headed --html=report.html
