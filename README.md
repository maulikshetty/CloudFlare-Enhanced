# CloudFlare-Enhanced
A python script mainly for small websites that checks the CPU levels of the server in fixed intervals for any anomaly (high CPU usage possibly due to attacks) and creates a custom firewall rule on CloudFlare to mitigate the attack. Similarly it disables the mitigation (Forced Captcha) if the CPU usage is seemed to reduce after set amount of time
