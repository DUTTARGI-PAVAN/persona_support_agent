import streamlit as st

from src.classifier import classify_persona
from src.rag_pipeline import retrieve
from src.generator import generate_response
from src.escalator import should_escalate

st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

.persona-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1e1e1e;
    border: 1px solid #444;
}

.response-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #262730;
    border-left: 5px solid #4CAF50;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Persona-Adaptive Support Agent")
st.caption("AI-Powered Customer Support using RAG and Persona Detection")

query = st.text_area(
    "Enter your support query",
    height=120,
    placeholder="Example: I forgot my password and can't access my account..."
)

if st.button("🚀 Generate Response", use_container_width=True):

    if query:

        result = classify_persona(query)

        persona = result["persona"]
        confidence = result["confidence"]

        chunks = retrieve(query)

        response = generate_response(
            query,
            persona,
            chunks
        )

        escalate, reason = should_escalate(
            query,
            confidence
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Detected Persona",
                persona
            )

        with col2:
            st.metric(
                "Confidence",
                f"{confidence*100:.0f}%"
            )

        st.divider()

        st.subheader("📋 AI Response")

        st.markdown(
            f"""
            <div class="response-box">
            {response}
            </div>
            """,
            unsafe_allow_html=True
        )

        if chunks:

            st.divider()

            with st.expander("📚 Retrieved Knowledge Base Context"):

                for idx, chunk in enumerate(chunks, 1):

                    st.markdown(
                        f"""
                        **Document {idx}**

                        {chunk['text'][:300]}...
                        """
                    )

        if escalate:

            st.error(
                f"⚠️ Escalation Required: {reason}"
            )

        else:

            st.success(
                "✅ No escalation required"
            )