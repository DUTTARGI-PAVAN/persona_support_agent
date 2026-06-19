def should_escalate(query, confidence):

    query = query.lower()

    if confidence < 0.5:
        return True, "Low Confidence"

    if any(word in query for word in [
        "refund",
        "billing",
        "chargeback",
        "duplicate charge"
    ]):
        return True, "Billing Issue"

    if any(word in query for word in [
        "legal",
        "court",
        "lawsuit"
    ]):
        return True, "Legal Issue"

    return False, None