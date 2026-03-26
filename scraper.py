import sys
from curl_cffi import requests

def fetch_playlist():
    url = "https://hilay.tv/play.m3u"
    
    try:
        session = requests.Session(impersonate="chrome120")
        headers = {
            "Referer": "https://hilay.tv/",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        # First visit the homepage to potentially solve CF and get cookies
        print("Visiting homepage to get cookies...")
        session.get("https://hilay.tv/", headers=headers, timeout=30)
        
        # Now fetch the playlist
        print(f"Fetching playlist from {url}...")
        response = session.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Basic validation to check if it's actually an m3u file and not a CF challenge page
            if "#EXTM3U" in response.text or "EXTINF" in response.text:
                with open("playlist.m3u", "wb") as f:
                    f.write(response.content)
                print("Successfully downloaded and saved playlist.m3u")
            else:
                print("Failed: The response does not look like a valid m3u playlist. It might be a Cloudflare challenge page.")
                print("Response starts with:")
                print(response.text[:200])
                sys.exit(1)
        else:
            print(f"Failed to fetch. Status code: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_playlist()
