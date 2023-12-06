from pyexpat import model
import streamlit as st
from langchain.document_loaders import YoutubeLoader
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv, find_dotenv
from utils.langchain_utils import generate_summary
from utils.streamlit_utils import double_newlines


def load_api_key() -> str: 
    load_dotenv(find_dotenv())
    # Escape entering api key in UI if .env file provided with api key
    if os.environ.get('OPEN_AI_KEY'):
        api_key = os.environ.get('OPEN_AI_KEY')
    
    # If no valid API key provided in .env, request through UI
    else:
        with st.sidebar:
            api_key = st.text_input(
                "Enter OpenAI API Key", key="openai_api_key", type="password"
            )
            st.markdown(
                "[Get an OpenAI API Key here!](https://platform.openai.com/account/api-keys)"
            )
    return api_key

# UI logic
def main():
    # App title
    st.set_page_config(
        layout='wide', page_title='YouTube Video Summary')
    st.title("YouTube Video Summary Bot :robot_face:")

    api_key = load_api_key()
    if not api_key:
        with st.sidebar(key='no_api_key'):
            st.write('You must please provide a valid OpenAI API key in the sidebar to access this app.')
        exit()
    
    # Input form for the YouTube link

    if api_key:
        with st.sidebar:
            # Model selection
            model_names = ('gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 
                'gpt-4', 'gpt-4-32k', 'gpt-4-1106-preview') # defaults to prereleased gpt-4
            model_information = '''
            Larger models (size is denoted by the suffix, e.g. '-16k', '-32k') can read in more tokens at once,
            and thus can read in larger videos as a whole, but also tend to cost more. All else equal, using gpt-4 costs more 
            than using gpt-3.5. gpt-4-1106, at the time of writing, has a 128k token context window
            and is faster.
            '''
            best_default_model_index = len(model_names)-1
            user_selected_model = st.selectbox('Select model', options=model_names, help=model_information, index=best_default_model_index)
            st.markdown('For more information on models and their costs, check the [OpenAI API Models page](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo)')

            # Temperature selection
            temperature_information = '''
            Temperature is a parameter passed into the LLM of choice. Higher temperature gives more random responses. A temperature of 0
            is deterministic.
            '''
            temperature = st.slider(label='Set temperature', min_value=0.0, max_value=1.0, step=0.01, help=temperature_information)
            
            # Toggle confirm submission after seeing cost (to be added later)
            # confirm_submission = st.checkbox('Toggle confirm submission?')

    with st.form(key='valid_api_key'):
        video_url = st.text_input(label='Enter the YouTube video link')
        if api_key:
            submit_button = st.form_submit_button(label='Summarize')
        else:
            st.warning('Please provide an OpenAI API key.')
        
    if not submit_button:
        exit()

    loader = YoutubeLoader.from_youtube_url(
        video_url, add_video_info=True, language=['en', 'cn'], translation='en'
    )

    # Load metadata
    youtube_metadata = loader.load()

    # Process metadata on submission
    if submit_button and youtube_metadata:
        try:
            st.subheader("Summary")
            summary = generate_summary(metadata=str(youtube_metadata), api_key=api_key, temperature=temperature, model=user_selected_model)
            markdown_summary = double_newlines(summary.content)
            st.markdown(markdown_summary)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Invalid YouTube video link. Please make sure the link is correct.")

if __name__ == "__main__":
    main()
