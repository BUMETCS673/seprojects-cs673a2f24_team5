from configs.database import get_key_database
from openai import OpenAI


def get_openai_client():
    db = get_key_database()
    keys_collection = db["keys"]
    openai_key = keys_collection.find_one({"_id": "chatgpt_api"})
    try:
        client = OpenAI(
            api_key=openai_key["api_key"]
        )
        return client
    except Exception as e:
        print(f"Error: {str(e)}")
