import os
import re
import time
import pytest
from playwright.sync_api import sync_playwright, APIRequestContext

DEFAULT_RETRY = 5


class WebhookClient:
    def __init__(self, request: APIRequestContext):
        self.request = request

    
    #Create webhook inbox to get verification code
    def create_token(self):
        alias = f"webhook-{int(time.time() * 1000)}"

        response = self.request.post(
        f"{os.getenv('WEBHOOK_URL')}/token",
        data={
            "default_status": 200,
            "default_content": "Hello Testing Shila!",
            "default_content_type": "text/html",
            "timeout": 0,
            "cors": False,
            "expiry": 604800,
            "alias": alias,  # YOUR alias
            "actions": True,
            },
        )
        assert response.status == 201, f"Expected 201, got {response.status}"
        data = response.json()
        uuid = data["uuid"]
        # email_domain="emailhook.site"  # MUST use this
        test_email = f"{alias}+{uuid}@{os.getenv('EMAIL_HOOK_URL')}"

        print(f"UUID: {uuid}")
        print(f"Alias: {alias}")
        print(f"Email inbox: {test_email}")
        print(f"Inbox URL: https://webhook.site/token/{uuid}")

        return uuid, test_email

    
    # Fetch verification code from email
    def wait_for_code(self, uuid: str, timeout_ms=15000) -> str:
        CODE_REGEX = re.compile(r"\b(\d{6})\b")  # adjust if different format

        max_retries = DEFAULT_RETRY
        interval = timeout_ms / max_retries / 1000

        for attempt in range(max_retries):
            print(f"🔄 Checking email (Attempt {attempt+1}/{max_retries})")

            res = self.request.get(
                f"{os.getenv('WEBHOOK_URL')}/token/{uuid}/requests?sorting=newest"
            )
            assert res.status == 200, f"Expected status 200, got {res.status}"

            emails = res.json().get("data", [])
            print(f"📬 Emails received: {len(emails)}")

            for email in emails:
                text = email.get("text_content", "")
                match = CODE_REGEX.search(text)

                if match:
                    code = match.group(1)
                    print(f"✅ Verification Code Found: {code}")
                    return code

            time.sleep(interval)

        raise Exception("❌ No verification code received in time")


    # Cleanup generated inbox and token
    def delete_token(self, uuid: str):
        res = self.request.delete(f"{os.getenv('WEBHOOK_URL')}/token/{uuid}")
        assert res.status == 204, f"Expected status 204, got {res.status}"
        print(f"🗑️ Token {uuid} deleted")

    def delete_requests(self, uuid: str):
        res = self.request.delete(f"{os.getenv('WEBHOOK_URL')}/token/{uuid}/request")
        assert res.status == 200, f"Expected status 200, got {res.status}"
        print(f"🗑️ Requests for {uuid} deleted")
