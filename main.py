# main.py
import streamlit as st
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

# Load .env variables
load_dotenv()

# --- Streamlit Page Config ---
st.set_page_config(page_title="Knife Forged Assistant", page_icon="🗡️", layout="centered")

# --- Custom Dark UI CSS ---
st.markdown("""
    <style>
    /* Clean dark background */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        margin: 0;
        padding: 0;
    }

    /* Hide any Streamlit top blank space */
    header, footer {
        visibility: hidden;
        height: 0;
    }

    .block-container {
        padding-top: 10px !important;
    }

    .main-container {
        max-width: 750px;
        margin: auto;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        margin-top: 20px;
    }

    .title-style {
        font-size: 34px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
        color: #00BFFF;
    }

    .subtitle-style {
        font-size: 16px;
        text-align: center;
        color: #ccc;
        margin-bottom: 25px;
    }

    .tip-box {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px 20px;
        border-left: 4px solid #00BFFF;
        border-radius: 12px;
        font-size: 15px;
        margin-bottom: 20px;
        color: #aaa;
    }

    .response-box {
        background-color: rgba(0, 191, 255, 0.1);
        padding: 20px;
        border-left: 5px solid #00BFFF;
        border-radius: 12px;
        font-size: 17px;
        margin-top: 20px;
        color: #e0f7ff;
    }

    input {
        background-color: #0f2027 !important;
        color: #ffffff !important;
        border: 2px solid #00BFFF !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }

    .stTextInput>div>div>input::placeholder {
        color: #aaa !important;
    }

    .stTextInput>label {
        font-weight: 600 !important;
        font-size: 17px !important;
        color: #ccc !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- Main Container ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title-style">🔪 Knife Forged Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">Ask about any knife, tool, or product – we’ve got you covered!</div>', unsafe_allow_html=True)

# --- Tip Box ---
st.markdown("""
<div class="tip-box">
    💡 Try asking:<br>
    • "Do you have chef’s knives under $50?"<br>
    • "What is the steel type for your hunting knives?"<br>
    • "Which knife would be best for camping?"
</div>
""", unsafe_allow_html=True)

# --- Input ---
question = st.text_input("Ask your question here:", placeholder="e.g. Do you have Small Castrator with Finger Guard?")

# --- Logic + QA ---
if question:
    api_key = os.getenv("GOOGLE_API_KEY")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-001", google_api_key=api_key)

    prompt_template = """
    You are Knife Forged Assistant, a helpful and friendly e-commerce assistant for a knife store.

    Use the context below to answer the customer’s question. If relevant info is found, respond informatively. If not, gently say the info isn’t available and suggest asking something else.

    Context:
    {context}

    Question:
    {question}

    Answer as the Knife Forged Assistant:
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt": prompt})
    response = qa_chain.run(question)

    st.markdown(f'<div class="response-box"><strong>Answer:</strong><br>{response}</div>', unsafe_allow_html=True)

# --- Close Container ---
st.markdown('</div>', unsafe_allow_html=True)
