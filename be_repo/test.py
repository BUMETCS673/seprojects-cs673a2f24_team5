from configs.database import get_user_database

database = get_user_database()
state_collection = database.get_collection("user_chat_state")

new_state = {
    "user_id": 'test',
    "state": '0',
    "thread_id": '1'
}
result = state_collection.replace_one({"user_id": 'test'}, new_state, upsert=True)
