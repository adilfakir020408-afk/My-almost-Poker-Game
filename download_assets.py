import os
import urllib.request
import json
import ssl

# Create directory
os.makedirs("assets/cards", exist_ok=True)

# URL
url = "https://api.github.com/repos/hayeah/playing-cards-assets/contents/png"

# Create context to avoid SSL errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Fetch file list
print("Fetching file list...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = response.read()
        files = json.loads(data)
except Exception as e:
    print(f"Error fetching list: {e}")
    exit(1)

# Download each file
for file_info in files:
    name = file_info['name']
    download_url = file_info['download_url']
    if name.endswith(".png"):
        print(f"Downloading {name}...")
        try:
            urllib.request.urlretrieve(download_url, f"assets/cards/{name}")
        except Exception as e:
            print(f"Error downloading {name}: {e}")

print("Done.")
