import requests
import json
from datetime import datetime

API_KEY = "API KEY HERE"

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Prepare log file with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"{timestamp}.log"

def print_and_log(api_name, status_code, log_file):
    if status_code == 200:
        status_text = f"{GREEN}VALID{RESET}"
        log_status = "VALID"
    else:
        status_text = f"{RED}INVALID{RESET}"
        log_status = "INVALID"
    output_line = f"{api_name} response status: {status_code} ({status_text})"
    print(output_line)
    # Write plain text without color codes to log
    log_file.write(f"{api_name} response status: {status_code} ({log_status})\n")

def test_maps_geocoding(api_key, log_file):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address=New+York&key={api_key}"
    response = requests.get(url)
    print_and_log("Google Maps Geocoding API", response.status_code, log_file)

def test_youtube_data(api_key, log_file):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UC_x5XG1OV2P6uZZ5FSM9Ttw&maxResults=1&key={api_key}"
    response = requests.get(url)
    print_and_log("YouTube Data API", response.status_code, log_file)

def test_cloud_vision(api_key, log_file):
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    payload = {
        "requests": [
            {
                "image": {
                    "source": {
                        "imageUri": "https://example.com/image.jpg"
                    }
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": 1
                    }
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print_and_log("Google Cloud Vision API", response.status_code, log_file)

def test_google_translate(api_key, log_file):
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}&q=hello&target=es"
    response = requests.get(url)
    print_and_log("Google Translate API", response.status_code, log_file)

if __name__ == "__main__":
    print("Testing Google API key validity...\n")
    with open(log_filename, "w") as log_file:
        test_maps_geocoding(API_KEY, log_file)
        test_youtube_data(API_KEY, log_file)
        test_cloud_vision(API_KEY, log_file)
        test_google_translate(API_KEY, log_file)
    print(f"\nFull output saved to {log_filename}")
