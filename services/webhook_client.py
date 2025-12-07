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
        # For webhook.site email inboxes, use just UUID@emailhook.site format
        test_email = f"{uuid}@{os.getenv('EMAIL_HOOK_URL')}"

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

        # Initial delay to allow email to be sent
        print(f"⏳ Waiting {interval:.1f}s before checking for emails...")
        time.sleep(interval)

        for attempt in range(max_retries):
            print(f"🔄 Checking email (Attempt {attempt+1}/{max_retries})")

            res = self.request.get(
                f"{os.getenv('WEBHOOK_URL')}/token/{uuid}/requests?sorting=newest"
            )
            assert res.status == 200, f"Expected status 200, got {res.status}"

            response_data = res.json()
            emails = response_data.get("data", [])
            print(f"📬 Requests/Emails received: {len(emails)}")

            # Debug: print full response structure on first attempt if no emails
            if attempt == 0 and len(emails) == 0:
                print(f"🔍 Response keys: {list(response_data.keys())}")
                print(f"🔍 Full response: {str(response_data)[:500]}...")

            for email in emails:
                # Debug: print request structure for first request
                if attempt == 0:
                    print(f"🔍 Request keys: {list(email.keys())}")
                    if "headers" in email:
                        content_type = email.get("headers", {}).get("content-type", [])
                        print(f"🔍 Content-Type: {content_type}")
                    if "content" in email:
                        print(f"🔍 Request content type: {type(email.get('content'))}")
                
                # Check multiple possible fields for email content
                text = ""
                
                # For webhook.site, email data might be in the request body
                # Try to get the raw content first
                raw_content = email.get("content", "")
                if raw_content:
                    # Try to parse as JSON if it's a string
                    if isinstance(raw_content, str):
                        try:
                            import json
                            parsed = json.loads(raw_content)
                            if isinstance(parsed, dict):
                                # Email data might be in parsed JSON
                                raw_content = parsed
                        except:
                            pass
                    
                    # If content is a dict, extract email fields
                    if isinstance(raw_content, dict):
                        text = (raw_content.get("text") or 
                               raw_content.get("text_content") or
                               raw_content.get("body") or
                               raw_content.get("message") or
                               "")
                
                # Try different possible field names directly on email object
                if not text:
                    possible_fields = [
                        "text_content", 
                        "html_content", 
                        "content", 
                        "body",
                        "text",
                        "message"
                    ]
                    
                    for field in possible_fields:
                        if field in email and email[field]:
                            field_value = email[field]
                            if isinstance(field_value, str):
                                text = field_value
                            elif isinstance(field_value, dict):
                                text = str(field_value.get("text", "") or field_value.get("html", ""))
                            else:
                                text = str(field_value)
                            if text:
                                break
                
                # If still no text, try to get raw body from nested structures
                if not text:
                    # Check if there's a nested body or content structure
                    if "body" in email and isinstance(email["body"], dict):
                        text = str(email["body"].get("text", "") or email["body"].get("html", ""))
                    elif "content" in email and isinstance(email["content"], dict):
                        text = str(email["content"].get("text", "") or email["content"].get("html", ""))
                
                # Also check query parameters or form data
                if not text:
                    query = email.get("query", {})
                    if isinstance(query, dict):
                        text = str(query.get("text", "") or query.get("body", "") or query.get("message", ""))
                
                # Debug: print email structure for first email
                if attempt == 0 and len(emails) > 0:
                    print(f"🔍 Email keys: {list(email.keys())}")
                    if text:
                        print(f"🔍 Email text preview: {text[:300]}...")
                    else:
                        print(f"🔍 Full email structure: {str(email)[:500]}...")
                
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
