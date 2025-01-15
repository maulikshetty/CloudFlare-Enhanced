import time
import psutil
import requests

# Cloudflare API Configuration
API_TOKEN = "your_api_key" # Can be created in CF DashBoard > Get Your API Token > Create Token ( Read README.md for more info on creation of API Key )
ZONE_ID = "your_zone_id" # Found in the domain page of CF
RULE_NAME = "ForceChallenge"  # Ensure this name is unique and consistent
CHECK_INTERVAL = 20  # in minutes
CPU_THRESHOLD = 70  # CPU usage percentage threshold

# Cloudflare API Endpoints
RULES_ENDPOINT = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/firewall/rules"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Store filter_id globally to avoid repeated lookups
filter_id = None

def get_rule():
    """Check if the Firewall Rule with the given description exists in Cloudflare."""
    global filter_id
    response = requests.get(RULES_ENDPOINT, headers=HEADERS)
    if response.status_code == 200:
        rules = response.json().get("result", [])
        for rule in rules:
            # Match the rule based on description
            if rule.get("description") == RULE_NAME:
                # print(f"Matched Rule: {rule}") # Remove in production env
                # Update the global filter_id if it changes
                filter_id = rule["filter"]["id"]
                return rule
    print("Rule not found.")
    return None

def create_rule():
    """Create the Firewall Rule in Cloudflare."""
    global filter_id
    payload = [
        {
            "filter": {
                "expression": "(http.request.uri contains \"/\")",
                "description": "ForceChallenge rule"
            },
            "action": "challenge",
            "description": RULE_NAME,
            "paused": True  # Create the rule in a disabled state initially
        }
    ]
    response = requests.post(RULES_ENDPOINT, headers=HEADERS, json=payload)
    if response.status_code == 200:
        # print("Rule created successfully in a disabled state.") # Debug Statement
        # Update filter_id from the response
        rule = response.json().get("result", [])[0]
        filter_id = rule["filter"]["id"]
        return True
    print(f"Failed to create rule: {response.text}")
    return False

def update_rule_status(rule_id, enabled):
    """Enable or disable the Firewall Rule."""
    global filter_id
    # Always enforce RULE_NAME during updates
    payload = [
        {
            "id": rule_id,
            "paused": not enabled,  # Enable or disable the rule
            "action": "challenge",  # Keep the action consistent
            "description": RULE_NAME,  # Ensure the rule name is consistent
            "filter": {
                "id": filter_id,
                "expression": "(http.request.uri contains \"/\")",  # Use the same expression
                "description": "ForceChallenge rule"  # Keep the description consistent
            }
        }
    ]
    response = requests.put(RULES_ENDPOINT, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"Rule status updated successfully: {'Enabled' if enabled else 'Disabled'}.")
        return True
    print(f"Failed to update rule status: {response.text}")
    return False

def check_and_manage_rule():
    """Continuously monitor CPU usage and manage the Firewall Rule."""
    while True:
        # Check CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"Current CPU usage: {cpu_usage}%")

        # Check if the rule exists
        rule = get_rule()
        if not rule:
            print("Rule not found. Creating rule...")
            if not create_rule():
                print("Failed to create rule. Exiting.")
                break
            # Retrieve the created rule to work with it
            rule = get_rule()
            if not rule:
                print("Failed to retrieve the created rule. Exiting.")
                break

        rule_id = rule["id"]
        is_paused = rule.get("paused", True)

        # Enable or disable the rule based on CPU usage
        if cpu_usage > CPU_THRESHOLD:
            if is_paused:
                print("High CPU usage detected. Enabling Firewall Rule...")
                if update_rule_status(rule_id, enabled=True):
                    pass
                else:
                    print("Failed to enable Firewall Rule.")
            else:
                print("Firewall Rule already enabled.")
        else:
            if not is_paused:
                print("CPU usage back to normal. Disabling Firewall Rule...")
                if update_rule_status(rule_id, enabled=False):
                    pass
                else:
                    print("Failed to disable Firewall Rule.")
            else:
                print("Firewall Rule already disabled.")

        # Wait for the next check
        print(f"Waiting {CHECK_INTERVAL} minutes before next check...")
        time.sleep(CHECK_INTERVAL * 60)

if __name__ == "__main__":
    try:
        check_and_manage_rule()
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
