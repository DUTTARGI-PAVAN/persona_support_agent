import streamlit as st

from src.classifier import classify_persona
from src.rag_pipeline import retrieve
from src.generator import generate_response
from src.escalator import should_escalate

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.response-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #262730;
    border-left: 5px solid #4CAF50;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("📊 System Information")

    st.success("System Ready")

    st.markdown("""
### Components

- Persona Classification
- RAG Retrieval
- ChromaDB
- Response Generator
- Escalation Engine
""")

    st.markdown("---")

    st.subheader("📚 Knowledge Base")

    st.write("• Password Reset Guide")
    st.write("• Login Issues")
    st.write("• Billing Policy")
    st.write("• Account Recovery")
    st.write("• Subscription Management")
    st.write("• API Troubleshooting")

# --------------------------------------------------
# Main Header
# --------------------------------------------------

st.title("🤖 Persona-Adaptive Support Agent")

st.caption(
    "AI-Powered Customer Support using Retrieval-Augmented Generation (RAG)"
)

# --------------------------------------------------
# User Input
# --------------------------------------------------

query = st.text_area(
    "Enter your support query",
    height=150,
    placeholder="Example: I forgot my password and can't access my account..."
)

# --------------------------------------------------
# Submit Button
# --------------------------------------------------

if st.button("🚀 Generate Response", use_container_width=True):

    if not query.strip():

        st.warning("Please enter a query.")

    else:

        with st.spinner("Analyzing your request..."):

            try:

                # Persona Classification
                result = classify_persona(query)

                persona = result["persona"]
                confidence = result["confidence"]

                # Retrieval
                try:
                    chunks = retrieve(query)
                except Exception as e:
                    st.error(f"Retrieval Error: {e}")
                    chunks = []

                # Response Generation
                response = generate_response(
                    query,
                    persona,
                    chunks
                )

                # Escalation Check
                escalate, reason = should_escalate(
                    query,
                    confidence
                )

                # ----------------------------------
                # Metrics
                # ----------------------------------

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        label="Detected Persona",
                        value=persona
                    )

                with col2:
                    st.metric(
                        label="Confidence",
                        value=f"{confidence * 100:.0f}%"
                    )

                st.divider()

                # ----------------------------------
                # Response
                # ----------------------------------

                st.subheader("📋 AI Response")

                st.markdown(
                    f"""
                    <div class="response-box">
                    {response}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ----------------------------------
                # Retrieved Context
                # ----------------------------------

                if chunks:

                    st.divider()

                    with st.expander(
                        "📚 Retrieved Knowledge Base Context"
                    ):

                        for idx, chunk in enumerate(chunks, start=1):

                            st.markdown(
                                f"""
**Document {idx}**

{chunk['text'][:400]}...
"""
                            )

                # ----------------------------------
                # Escalation
                # ----------------------------------

                st.divider()

                if escalate:

                    st.error(
                        f"⚠️ Escalation Required: {reason}"
                    )

                else:

                    st.success(
                        "✅ No escalation required"
                    )

            except Exception as e:

                st.error(
                    f"An error occurred: {str(e)}"
                )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Built using Streamlit, ChromaDB, Sentence Transformers, and RAG Architecture"
)