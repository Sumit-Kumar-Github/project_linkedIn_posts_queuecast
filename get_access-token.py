import requests

# 1. Fill in your credentials here
CLIENT_ID = 'your_client_id_here'
CLIENT_SECRET = 'your_client_secret_here'
REDIRECT_URI = 'http://localhost:8000/callback'

# 2. Paste the code you just copied from the browser URL
AUTH_CODE = 'your_authorization_code_here' 

url = "https://www.linkedin.com/oauth/v2/accessToken"

payload = {
    "grant_type": "authorization_code",
    "code": AUTH_CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)

# 3. This will print your access token!
print(response.json())