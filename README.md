# 🛡️ Server Protection with Cloudflare Firewall Script

This Python script is designed for small websites to monitor server CPU usage and mitigate potential DDoS attacks or anomalies by leveraging Cloudflare’s custom firewall rules. It ensures continuous server protection by automatically enabling or disabling mitigation (Forced CAPTCHA) based on CPU load.

Refer to https://developers.cloudflare.com/waf/custom-rules/create-api/ for making changes or adding extra functions in the code.

---

## 📋 Features

- Continuous Monitoring: Checks server CPU usage at fixed intervals.
- Attack Mitigation: Automatically creates a custom Cloudflare firewall rule to apply Forced CAPTCHA when CPU usage spikes.
- Adaptive Response: Disables the firewall rule when CPU usage normalizes.
- Seamless Automation: Ensures efficient and hands-free protection for your website.

---

## ⚙️ Setup and Usage

### 1️⃣ Prerequisites
- Python 3+
- Install required Python libraries:
- ```py
  pip install psutil requests
  ```
- Cloudflare API Token: Generate a Cloudflare API token with permissions for managing firewall rules for your zone.

### 2️⃣ Configuration
Update the following variables in the script:
- `API_TOKEN`: Your Cloudflare API token.
- `ZONE_ID`: The ID of your Cloudflare zone.
- `RULE_NAME`: The name for the custom rule (default is ForceChallenge).
- `CHECK_INTERVAL`: Time interval (in minutes) between CPU checks.
- `CPU_THRESHOLD`: CPU usage percentage threshold to trigger mitigation.

### 3️⃣ Run the Script
Execute the script to test: 
```
python script.py
```

Execute the script for production:
```
nohup script.py &
```

nohup will keep the script running in background even if the terminal is closed.

---

## 🚦 Workflow Overview

1. The script monitors server CPU usage at regular intervals.
2. If CPU usage exceeds the specified `CPU_THRESHOLD`:
   - Creates or enables a Cloudflare firewall rule (ForceChallenge).
   - Applies Forced CAPTCHA to visitors, mitigating potential attacks.
3. When CPU usage normalizes:
   - Disables the firewall rule automatically after a set interval.

---

## 🛠️ Customization

### Modify the Thresholds:
Adjust CPU_THRESHOLD and CHECK_INTERVAL in the script for your specific needs:
`CHECK_INTERVAL` = 20  # Check CPU every 20 minute  // Adjust as per your requirements
`CPU_THRESHOLD` = 70  # Trigger mitigation if CPU usage exceeds 70% or as per your requirements

### Change the Rule Configuration:
Update the RULE_NAME and the filter expression in the create_rule function to customize the firewall rule name.

---

## 🖥️ Example Output

```
Current CPU usage: 93.3%
High CPU usage detected. Enabling Firewall Rule...
Rule status updated successfully: Enabled.
Waiting 20 minutes before next check...

Current CPU usage: 5.6%
CPU usage back to normal. Disabling Firewall Rule...
Rule status updated successfully: Disabled.
Waiting 20 minutes before next check...
```
---

## 🚨 Important Notes

- Ensure the API token has permissions to manage firewall rules for your domain or zone.
- The script is intended for small websites or scenarios with limited traffic and may not work for web servers with constant high CPU use.

---

## 🤝 Contributions

Feel free to fork this repository, submit issues, or suggest improvements to make this script even better! 🚀
