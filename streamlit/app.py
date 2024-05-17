import streamlit as st
from utils import answer_question

st.set_page_config(
    page_title="Gemini + Google Search",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/ninjajon/gemini-with-google-search-grounding",
        "About": """
            ## Gemini + Google Search
            **GitHub**: https://github.com/ninjajon/gemini-with-google-search-grounding
        """
    }
)

with st.sidebar:
    st.title("Gemini + Google Search")
    st.markdown("This AI Assistant will answer your questions while making sureit grounds its responses on Google Search results.")
    st.markdown("You can simply ask a question and hit Enter, or you can also add context/instructions to your question. For example, let's say you want to ask the following question:")
    st.markdown("- What is Gen AI?")
    st.markdown("Try it without any context, and then try it again with the following context:")
    st.markdown("- Answer like I'm a 5 years old")
    st.markdown("Notice the difference in the response.")
    st.markdown("Built with Google [Grounding API](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/grounding#ground-on-public-data)")
    st.markdown("Source Code: https://github.com/ninjajon/gemini-with-google-search-grounding")

st.header("Gemini + Google Search", divider="rainbow")
st.subheader("Ask me anything... I'll use Google Search to answer")

question = st.text_input("Ask your question here")
context = st.text_area("[Optional] Add context to your question")
prompt = "Question: " + question + "\nContext: " + context + "\nAnswer:"

button_pressed = ""
if st.button("Search", type="secondary"):
    button_pressed = True

if button_pressed:
    with st.spinner("Searching..."):
        answer = answer_question(prompt)
        st.write("### Answer")
        st.write(answer)