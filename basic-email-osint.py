import requests
import tkinter as tk
from tkinter import scrolledtext

requests.packages.urllib3.disable_warnings()


services = {
    "PayPal": {
        "url": "https://www.paypal.com/authflow/password-recovery",
        "method": "POST",
        "data": lambda e: {"email": e}
    },
    "Spotify": {
        "url": "https://www.spotify.com/api/password-reset",
        "method": "POST",
        "data": lambda e: {"email": e}
    },
    "Reddit": {
        "url": "https://www.reddit.com/api/password.json",
        "method": "POST",
        "data": lambda e: {"email": e}
    },
    "GitHub": {
        "url": "https://github.com/password_reset",
        "method": "POST",
        "data": lambda e: {"email": e}
    },
    "Facebook": {
        "url": "https://www.facebook.com/login/identify/?ctx=recover",
        "method": "POST",
        "data": lambda e: {"email": e}
    },
    "Instagram": {
        "url": "https://www.instagram.com/accounts/account_recovery_send_ajax/",
        "method": "POST",
        "data": lambda e: {"email_or_username": e}
    },
    "Twitter (X)": {
        "url": "https://api.twitter.com/i/users/email_available.json?email={}",
        "method": "GET"
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/checkpoint/rp/request-password-reset-submit",
        "method": "POST",
        "data": lambda e: {"userName": e}
    },
    "YouTube (Google)": {
        "url": "https://accounts.google.com/InputValidator?resource=SignIn",
        "method": "POST",
        "data": lambda e: {
            "input01": {
                "Input": "GmailAddress",
                "GmailAddress": e
            }
        }
    }
}

def run_scan(email, output):
    headers = {"User-Agent": "Mozilla/5.0"}
    output.delete(1.0, tk.END)
    output.insert(tk.END, f"📡 Scanning: {email}\n\n")

    for name, config in services.items():
        try:
            output.insert(tk.END, f"🔎 {name}: ")
            if config["method"] == "POST":
                res = requests.post(config["url"], headers=headers, data=config.get("data", lambda x: {})(email), verify=False)
            else:
                res = requests.get(config["url"].format(email), headers=headers, verify=False)

            if res.status_code == 200 and len(res.text) > 300:
                output.insert(tk.END, "✅ Possibly Registered\n")
            elif res.status_code == 429:
                output.insert(tk.END, "⏱️ Rate Limited\n")
            else:
                output.insert(tk.END, "❌ Not Found or Blocked\n")
        except Exception as e:
            output.insert(tk.END, f"⚠️ Error: {e}\n")


window = tk.Tk()
window.title("Email OSINT Scanner 🔍")
window.geometry("600x500")

tk.Label(window, text="Enter Email Address:", font=("Arial", 12)).pack(pady=10)

email_entry = tk.Entry(window, width=40, font=("Arial", 12))
email_entry.pack(pady=5)

output_box = scrolledtext.ScrolledText(window, width=70, height=20, font=("Courier", 10))
output_box.pack(pady=10)

tk.Button(window, text="Start Scan", font=("Arial", 12), command=lambda: run_scan(email_entry.get(), output_box)).pack(pady=10)

window.mainloop()
