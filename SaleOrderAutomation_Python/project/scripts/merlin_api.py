import requests
from config.config import MERLIN_API_URL

def upload_to_merlin(payload):
    print("🚀 Uploading data to Merlin API...")

    response = requests.post(
        MERLIN_API_URL,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"❌ Merlin API failed: {response.status_code} - {response.text}"
        )

    result = response.json()

    print("✅ Merlin API upload successful")
    print("📄 Response:", result)

    return result
