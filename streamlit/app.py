import streamlit as st
from utils import search_document, generate_answer

st.set_page_config(
    page_title="Ninja Rail LLM",
    #page_icon="imgs/avatar_streamly.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/ninjajon/gcp-ninjarail-llm",
        "About": """
            ## Ninja Rail LLM 
            **GitHub**: https://github.com/ninjajon/gcp-ninjarail-llm
        """
    }
)

with st.sidebar:
    st.title("🥷Ninja Rail LLM")
    st.markdown("""
        This AI Assistant aims to simulate what a Corporate Rail internal search/chatbot could look like. 
        Fictive data has been generated with the Gemini LLM and has been stored in Vertex AI Search datastore.
    """)
    st.markdown("""
        When users ask questions, the agent first search against this datastore. 
        Then, with the retrieved data, it will use Gemini LLM to generate an answer.
    """)
    st.markdown("If the Assistant does not find any corporate data in the datastore, it will revert to its common knowledge (thanks Gemini!) to answer.")
    
    st.subheader("You can explore the fictive data here:")
    st.link_button("Ninja Rail Public Doc", "https://storage.googleapis.com/ninjarail-llm-data/pdfs/ninjarail-public-corporate-data.pdf")
    st.link_button("Ninja Rail Internal Doc", "https://storage.googleapis.com/ninjarail-llm-data/pdfs/ninjarail-internal-corporate-data.pdf")

st.header("🥷Ninja Rail LLM", divider="rainbow")
st.subheader("Ask me anything...")

example_prompts = [
    "Where is our Head Quarter?",
    "What is our mission?",
    "Who is our CEO?",
    "Summarize the code of conduct",
]

button_pressed = ""

button_cols = st.columns(4)

if button_cols[0].button(example_prompts[0]):
    button_pressed = example_prompts[0]
if button_cols[1].button(example_prompts[1]):
    button_pressed = example_prompts[1]
if button_cols[2].button(example_prompts[2]):
    button_pressed = example_prompts[2]
if button_cols[3].button(example_prompts[3]):
    button_pressed = example_prompts[3]

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := (st.chat_input("How can I help you?") or button_pressed):

    prompt = prompt.replace('"', "").replace("'", "")
    if prompt != "":
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            search_result = search_document(prompt)
            source_doc_url = search_result.source_doc_url
            source_file_name = search_result.source_file_name
            summary = search_result.summary
            extracted_content = search_result.extracted_content

        with st.spinner("Generating answer..."):
            answer = generate_answer(prompt, summary, extracted_content, source_doc_url)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})