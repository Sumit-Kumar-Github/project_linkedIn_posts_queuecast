# 🚀 Serverless LinkedIn Content Pipeline

An automated, zero-cost content distribution system built with **Python** and **GitHub Actions**. This project automates the end-to-end process of scheduling and publishing LinkedIn posts (text and images) without requiring a dedicated server.

![Architecture Diagram](https://github.com/Sumit-Kumar-Github/zz_Raw-Data/blob/4b71913dd0bf007b73dd81d2850900efa9f1c632/linkedIn-autopost-data/automated-linkedin-poster-workflow.png) 

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Orchestration:** GitHub Actions (Serverless Cron)
* **API Integrations:** LinkedIn Marketing Developer API, Twilio (WhatsApp Business API)
* **Storage:** JSON-based state management

## 🌟 Key Features
* **Zero-Cost Execution:** Leverages GitHub Actions' free tier for public/private repositories.
* **Media Support:** Handles both standard text posts and multi-format image uploads via API.
* **Proactive Monitoring:** Integrated WhatsApp notification system via Twilio to alert the user about:
    * Empty content queue status.
    * LinkedIn OAuth2 token expiration (preventing pipeline downtime).
* **Cron Scheduling:** Fully customizable posting frequency using YAML-based cron syntax.

## 🏗️ Architecture Flow
1.  **Content Management:** Posts are staged in a `data/queue.json` file.
2.  **Trigger:** GitHub Actions triggers a workflow on a predefined schedule (e.g., daily at 9:00 AM IST).
3.  **Execution:** A Python script fetches the next post, handles LinkedIn's multi-step image upload process (registering, uploading, and checking status), and publishes the content.
4.  **Notification:** If the script detects that the 60-day access token is nearing expiration, it sends a WhatsApp alert to the developer.

## 🔑 Environment Variables
To run this project, you will need to add the following secrets to your GitHub Repository (**Settings > Secrets and variables > Actions**):

| Secret | Description |
| :--- | :--- |
| `LINKEDIN_ACCESS_TOKEN` | Your LinkedIn OAuth2 Permanent/Long-lived token |
| `LINKEDIN_PERSON_URN` | Your unique LinkedIn Member ID (URN) |
| `TWILIO_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `WHATSAPP_TO` | Your phone number (with country code) |

## 🚀 Getting Started

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/linkedin-bot.git](https://github.com/yourusername/linkedin-bot.git)
```
2. Add your content:
Edit data/queue.json following the provided template:
```bash
{
  "posts": [
    { "text": "Hello world!", "image_path": "images/post1.jpg" }
  ]
}
```
📈 Future Roadmap
* Integration with Azure Key Vault for enhanced secret management.
* Multi-platform support (Twitter/X and Medium).
* Generative AI integration to suggest post captions based on project keywords.
