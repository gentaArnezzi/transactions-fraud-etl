import os, json, requests
from dotenv import load_dotenv


load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
API_URL = os.getenv("API_URL", "")
SRC_FILE = os.path.join(RAW_DIR, "api_transactions.json")
EXTRACTED_FILE = os.path.join(RAW_DIR, "api_extracted.json")


os.makedirs(RAW_DIR, exist_ok=True)


if API_URL:
    print(f"Fetching from API: {API_URL}")
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()
else:
    print(f"Reading local file: {SRC_FILE}")
    with open(SRC_FILE, "r") as f:
        data = json.load(f)


# (Optional) Validasi minimal
assert isinstance(data, list), "API data should be a list of objects"


with open(EXTRACTED_FILE, "w") as f:
    json.dump(data, f, ensure_ascii=False)


print("✅ Extract API →", EXTRACTED_FILE)