import inspect

def generate_response(query, persona, retrieved_chunks):
    context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])

    if persona == "Technical Expert":
        response_text = f"""
        ### Technical Response
        
        **User Query:** {query}
        
        #### Relevant Information:
        {context}
        
        ---
        **Detailed Explanation:**
        Please review the above technical guidance and follow the troubleshooting steps.
        """
    elif persona == "Frustrated User":
        response_text = f"""
        ### Reassuring Care Response
        
        I completely understand how frustrating this issue can be. Let's get this resolved for you.
        
        #### Here is what you can do:
        {context}
        
        Please follow these steps one by one. If the issue continues, our team is here to assist.
        """
    else:  # Business Executive
        response_text = f"""
        ### Business Summary
        
        **Query:** {query}
        
        #### Context Summary:
        {context}
        
        **Impact Analysis:**
        The above process outlines the roadmap to resolve this operational block while minimizing service disruption.
        """
    
    # inspect.cleandoc automatically strips out uniform leading indentation spaces 
    # that mess up markdown layouts in cloud containers.
    return inspect.cleandoc(response_text)