from email.policy import default
import streamlit as st
from langchain.document_loaders import YoutubeLoader
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv, find_dotenv
from utils.langchain_utils import generate_summary
from utils.streamlit_utils import double_newlines


def load_api_key() -> str: 
    # A
    try:
        load_dotenv(find_dotenv())
        api_key = os.environ.get('OPEN_AI_KEY')
    
    # If no valid API key provided in .env, request through UI
    except:
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

    
    # Input form for the YouTube link

    if api_key:
        with st.sidebar:
            # Model selection
            model_names = ('gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 
                'gpt-4', 'gpt-4-32k', 'gpt-4-1106-preview')
            model_information = '''
            Larger models (size is denoted by the suffix, e.g. '-16k', '-32k') can read in more tokens at once,
            and thus can read in larger videos as a whole, but also tend to cost more. All else equal, using gpt-4 costs more 
            than using gpt-3.5. gpt-4-1106, at the time of writing, has a 128k token context window
            and is faster.
            '''
            user_selected_model = st.selectbox('Select model', options=model_names, help=model_information)

            # Temperature selection
            temperature = st.slider(label='Set temperature', min_value=0.0, max_value=1.0, step=0.01)
            
            # Toggle confirm submission after seeing cost (to be added later)
            # confirm_submission = st.checkbox('Toggle confirm submission?')

    with st.form(key='my_form'):
        video_url = st.text_input(label='Enter the YouTube video link')
        if api_key:
            submit_button = st.form_submit_button(label='Summarize')
        # elif api_key and confirm_submission:
        #     confirm_button = 
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
            st.write('Metadata: '+  str(youtube_metadata))
            st.error(f"An error occurred: {e}")
    else:
        st.error("Invalid YouTube video link. Please make sure the link is correct.")


if __name__ == "__main__":
    main()
