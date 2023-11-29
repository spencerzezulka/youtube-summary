import streamlit as st
from langchain.document_loaders import YoutubeLoader
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv, find_dotenv


def load_api_key():
    load_dotenv(find_dotenv())
    if os.environ.get('OPEN_AI_KEY') is not None:
        apiKey = os.environ.get('OPEN_AI_KEY')
    else:
        with st.sidebar:
            apiKey = st.text_input(
                "Enter OpenAI API Key", key="openai_api_key", type="password"
            )
            st.markdown(
                "[Get an OpenAI API Key here!](https://platform.openai.com/account/api-keys)"
            )


def generate_summary(transcript, llm_chain):
    agent = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="metadata")
    response = agent.run(transcript)
    return st.success(response)

# Streamlit app


def main():
    load_api_key()
    llmName = "gpt-3.5-turbo-16k"  # Choose a model, defaulting to gpt-3.5


    summaryPrompt = ChatPromptTemplate.from_template(
        '''
        The following is transcript-containing YouTube metadata for a given video. Please summarize it
        concisely in one sentence, and then extract insights. Include timestamps.
        The output should be formatted in markdown, and the insights should be enumerated.

        Here is an example.

        ///Example///
        Summary:

        Insights:
        1.
        2.
        3.
        [and so on]

        ///End of Format Template///

        metadata: `{metadata}`\n


        ///Your response (in format specified in 'Format Template')///

        Summary:
        ''' 
    )
    # Initialize the LangChain agent with the selected model
    llm = ChatOpenAI(temperature=0.2, model_name=llmName)
    summary_chain = LLMChain(llm=llm, prompt=summaryPrompt, output_key='summary')
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
            generate_summary(youtube_metadata, summary_chain)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Invalid YouTube video link. Please make sure the link is correct.")


if __name__ == "__main__":
    main()
