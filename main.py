import os
import json
import requests

# 1. Load Secrets securely
ACCESS_TOKEN = os.environ.get('LINKEDIN_TOKEN')
AUTHOR_URN = os.environ.get('LINKEDIN_URN')
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
TWILIO_FROM = os.environ.get('TWILIO_FROM')
MY_PHONE = os.environ.get('MY_PHONE')

QUEUE_FILE = 'queue.json'


def send_whatsapp_alert(message):
    """Sends a WhatsApp message to your phone."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    
    # Twilio uses Basic Auth with SID and Token
    auth = (TWILIO_SID, TWILIO_TOKEN)
    
    payload = {
        "From": TWILIO_FROM,
        "To": MY_PHONE,
        "Body": message
    }
    
    try:
        requests.post(url, auth=auth, data=payload, timeout=10)
        print("WhatsApp alert sent successfully!")
    except Exception as e:
        print(f"Error sending alert: {e}")


def upload_image(file_path, headers):
    """Handles the 3-step upload specifically for images."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    # Step 1: Register
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    register_payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": AUTHOR_URN,
            "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
        }
    }
    
    reg_res = requests.post(register_url, headers=headers, json=register_payload, timeout=10)
    if reg_res.status_code != 200:
        print(f"Registration failed: {reg_res.text}")
        return None
        
    upload_url = reg_res.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_urn = reg_res.json()['value']['asset']

    # Step 2: Upload Binary
    with open(file_path, 'rb') as file:
        file_data = file.read()
        
    upload_headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    upload_res = requests.post(upload_url, headers=upload_headers, data=file_data, timeout=60)
    
    if upload_res.status_code != 201:
        print(f"Upload failed: {upload_res.text}")
        return None

    return asset_urn
    

def process_queue():
    with open(QUEUE_FILE, 'r') as f:
        queue_data = json.load(f)

    # 2. Find the next pending post
    post_to_publish = next((item for item in queue_data if item["status"] == "pending"), None)

    if not post_to_publish:
        print("All caught up! No pending posts.")
        send_whatsapp_alert("🤖 LinkedIn Auto-Poster: Your queue is empty! Time to add more achievements.")
        return

    # 3. Post to LinkedIn
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    
    # 1. Base Payload Structure
    post_payload = {
        "author": AUTHOR_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_to_publish.get('text', '')},
                "shareMediaCategory": "NONE",
                "media": []
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    # 2. Dynamic Routing Logic
    img_paths = post_to_publish.get('images', [])

    if img_paths:
        print(f"Uploading {len(img_paths)} image(s)...")
        post_payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
        for img_path in img_paths:
            asset_urn = upload_image(img_path, headers)
            if asset_urn:
                post_payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"].append({
                    "status": "READY",
                    "media": asset_urn
                })

    # If no images were added successfully, fallback to plain text
    if not post_payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"]:
        del post_payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"]

    # 3. Publish to LinkedIn
    url = "https://api.linkedin.com/v2/ugcPosts"
    response = requests.post(url, headers=headers, json=post_payload, timeout=10)

    # 4. Update the queue file if successful
    if response.status_code == 201:
        post_to_publish['status'] = "posted"
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue_data, f, indent=2)
        print("Successfully posted and updated queue!")
        send_whatsapp_alert(f"✅ LinkedIn Auto-Poster: Successfully posted a new post on linkedIn and updated the queue!")
    elif response.status_code == 401: # 401 is the standard code for an expired/invalid token
        print("Token Expired!")
        send_whatsapp_alert("🚨 LinkedIn Auto-Poster: Your Access Token has expired (60 days reached). Please generate a new one and update GitHub Secrets.") 
    else:
        print(f"Failed to post: {response.json()}")
        send_whatsapp_alert(f"⚠️ LinkedIn Auto-Poster Error: Failed to post ID {post_to_publish['id']}.")


if __name__ == "__main__":
    process_queue()
