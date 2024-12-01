def get_answer_from_langgraph(qa_graph, resume_text, user_state_collection, user_id, question):
    user_state = user_state_collection.find_one({"user_id": user_id})
    thread_id = user_state.get('thread_id', '')

    config = {"configurable": {"thread_id": user_id + thread_id}}

    # If state is 0, send resume to LLM first
    # if state == '0':
    events = qa_graph.stream(
        {"messages": [("user", resume_text)]}, config, stream_mode="values"
    )
    # Update state to 1
    new_state = {
        "user_id": user_id,
        "state": '1',
        "thread_id": thread_id
    }
    user_state_collection.replace_one({"user_id": user_id}, new_state, upsert=True)
    for event in events:
        if event["messages"][-1].type == "ai":
            print('User ask for the first time!')
    # Then send the question
    events = qa_graph.stream(
        {"messages": [("user", question)]}, config, stream_mode="values"
    )
    for event in events:
        if event["messages"][-1].type == "ai":
            return event["messages"][-1].content

    return
