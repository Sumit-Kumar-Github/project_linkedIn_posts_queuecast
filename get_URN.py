import requests

# Paste your new 60-day access token here
ACCESS_TOKEN = 'your_long_access_token_here'

# This endpoint returns your basic profile info
url = "https://api.linkedin.com/v2/userinfo"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers)
data = response.json()

# The 'sub' field contains your unique profile ID
if 'sub' in data:
    my_urn = f"urn:li:person:{data['sub']}"
    print(f"Success! Your author URN is: {my_urn}")
else:
    print("Error fetching profile:")
    print(data)