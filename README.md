## 🔍 Bounty Alert Slack Bot

This is a Flask-based Python application that scrapes bounty listings from [Replit Bounties](https://replit.com/bounties), identifies the **highest paid bounties posted within the last 24 hours**, and sends a **formatted professional message** to a specified Slack channel.

---

### 🚀 Features

* ✅ Scrapes Replit bounties using Firecrawl and structured schema
* ✅ Extracts and analyzes JSON data using Gemini 1.5 Flash (via Google Generative AI)
* ✅ Automatically identifies highest paid bounty (or ties)
* ✅ Sends Slack notifications with full details
* ✅ Runs via HTTP GET on `/slack`

---

### 🧠 Tech Stack

* **Python 3.9+**
* **Flask** – lightweight API server
* **Firecrawl** – smart structured web scraping
* **Google Gemini 1.5 Flash** – LLM for extraction logic
* **Slack Incoming Webhooks** – messaging interface

---

### 📦 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone [https://github.com/HamnaCh456/slack_notifier.git](https://github.com/HamnaCh456/slack_notifier.git)
   cd bounty-alert-bot
   ```
2. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**

   Create a `.env` file in the project root:

   ```
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   GEMINI_API_KEY=your_gemini_api_key
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url
   ```

---

### ▶️ Run the App

```bash
python app.py
```

Then visit:

```
http://localhost:5000/slack
```

---

### 📤 Example Slack Message

> 🎯 **New Bounty Alert**
>
> 💰 **Reward:** \$300
> 📝 **Title:** Build a Python Slack Bot
> 🕒 **Posted:** 3 hours ago
> 🔗 **URL:** [Click here](https://replit.com/bounties/12345)

---

### 📁 File Structure

```
.
├── app.py              # Main Flask app and logic
├── .env                # Environment variables (not committed)
├── requirements.txt    # Python dependencies
└── README.md           # You're here!


Let me know if you'd like me to auto-generate `requirements.txt` for this code or deploy it using platforms like **Render**, **Railway**, or **Fly.io**.
