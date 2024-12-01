# configs/openai_key.py

from ..configs.database import get_key_database

def get_openai_api_key():
    """
    Retrieve the OpenAI API key from the MongoDB database.
    
    Returns:
        str: The OpenAI API key.
        
    Raises:
        ValueError: If the API key is not found or is empty.
    """
    db = get_key_database()
    keys_collection = db["keys"]
    openai_key_doc = keys_collection.find_one({"_id": "chatgpt_api"})
    
    if not openai_key_doc:
        raise ValueError("OpenAI API key not found in the database.")
    
    openai_key = openai_key_doc.get("api_key")
    
    if not openai_key:
        raise ValueError("OpenAI API key is empty.")
    
    return openai_key
