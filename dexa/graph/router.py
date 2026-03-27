def router(state):
    decision = state.get("decision", "continue")
    history = state.get("history", [])

    # Safety: force response if history is too long
    if len(history) > 10:
        return "response"

    if decision == "continue":
        return "execution"

    return "response"