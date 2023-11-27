import streamlit as st
from langchain.document_loaders import YoutubeLoader
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv, find_dotenv


def load_api_key():
    load_dotenv(find_dotenv())
    if os.environ.getenv('OPEN_AI_KEY') is not None:
        apiKey = os.environ.get('OPEN_AI_KEY')
    else:
        with st.sidebar:
            apiKey = st.text_input(
                "Enter OpenAI API Key", key="openai_api_key", type="password"
            )
            st.markdown(
                "[Get an OpenAI API Key here!](https://platform.openai.com/account/api-keys)"
            )


def generate_summary(transcript, llm):
    agent = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="metadata")
    response = agent.run(transcript)
    return st.success(response)

# Streamlit app


def main():
    load_api_key()
    llmName = "gpt-3.5-turbo-16k"  # Choose a model, defaulting to gpt-3.5

    prompt = PromptTemplate.from_template(summaryPrompt)

    # Initialize the LangChain agent with the selected model
    llm = ChatOpenAI(temperature=0.2, model_name=llmName)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # App title
    st.set_page_config(
        layout='wide', page_title='YouTube Video Summary')
    st.title("YouTube Video Summary Bot :robot_face:")

    # Input form for the YouTube link
    with st.form(key='my_form'):
        video_url = st.text_input(label='Enter the YouTube video link')
        submit_button = st.form_submit_button(label='Summarize')

    if not submit_button:
        exit()

    loader = YoutubeLoader.from_youtube_url(
        video_url, add_video_info=True, language=['en', 'cn'], translation='en'
    )
    # Load metadata
    youtube_metadata = loader.load()

    # Process the form input
    if submit_button and youtube_metadata:
        try:
            st.subheader("Summary")
            generate_summary(youtube_metadata, llm)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Invalid YouTube video link. Please make sure the link is correct.")


if __name__ == "__main__":
    main()
