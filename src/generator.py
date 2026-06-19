def generate_response(query, persona, retrieved_chunks):

    context = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    )

    if persona == "Technical Expert":
        return f"""
Technical Response

User Query:
{query}

Relevant Information:
{context}

Detailed Explanation:
Please review the above technical guidance and follow the troubleshooting steps.
"""

    elif persona == "Frustrated User":
        return f"""
I understand this issue can be frustrating.

Here's what you can do:

{context}

Please follow the steps one by one. If the issue continues, contact support.
"""

    else:
        return f"""
Business Summary

Query:
{query}

Relevant Information:
{context}

Impact:
The above process should help resolve the issue while minimizing service disruption.
"""
if __name__ == "__main__":

    sample_chunks = [
        {
            "text": "To reset your password, click Forgot Password and follow the email instructions."
        }
    ]

    print(
        generate_response(
            "How do I reset my password?",
            "Frustrated User",
            sample_chunks
        )
    )