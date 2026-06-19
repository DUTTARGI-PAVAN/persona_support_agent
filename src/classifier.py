def classify_persona(message):
    msg = message.lower()

    if any(word in msg for word in [
        "api", "401", "token", "error", "integration",
        "database", "authentication"
    ]):
        return {
            "persona": "Technical Expert",
            "confidence": 0.9
        }

    elif any(word in msg for word in [
        "angry", "frustrated", "nothing works",
        "terrible", "upset", "annoyed"
    ]):
        return {
            "persona": "Frustrated User",
            "confidence": 0.85
        }

    else:
        return {
            "persona": "Business Executive",
            "confidence": 0.8
        }