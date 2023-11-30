# YouTube Summarizer | 🎬🎥🔴 ---> 📝

## Motivation

You see a colorful array of thumbnails. 

You open a bunch of tabs. 

So many tabs...

so little time. 

In the past, you might've swept through comments-first, *hoping* for a gracious commenter with a summary to guide you. Hope no longer!&mdash;paste the URL, get a summary.

[**for example...**](https://www.youtube.com/watch?v=OI_3bQ-EWSI)
![Screenshot](assets/videoscreenshot.png) 
![Screenshot2](assets/summaryscreenshot.png)


## Features

**YoutubeSummarizer** offers a few bonus features:

1. Text analytics dashboard to view your videos, *broken down* to their *finest* parts
2. Compare and contrast up to 3 videos at a time
3. Chat with your model of choice about your video(s)
4. Translation
5. Customizable summary prompts
6. Script to process multishot transcript example &ndash; summary example pairings if you want your summaries to look a certain way

## Requirements
This project uses
1. `python` (3.9 [just not 3.9.7 {for some (unspecified) reason}])
2. `pytest`, for testing
3. `poetry`, for dependency management
4. `langchain`, for LLM operations
5. `openai`, as our LLM provider
6. `youtube-transcript-api` and `pytube` for YouTube transcript I/O
7. `streamlit`, for the frontend
8. `python-dotenv`, for loading API keys when using a local installation

## Local Installation
1. Clone the repo and move into it

    ```bash
    git clone https://github.com/spencerzezulka/youtube-summary.git
    cd youtube-summary
    ```

2. Install [**Poetry**](https://python-poetry.org/) if you haven't already

    e.g. on Mac with [**Homebrew**](https://brew.sh/)
    ```bash
    brew install poetry
    ```


3. Create a Poetry environment
    ```bash 
    poetry init
    ```

4. Install the packages to the Poetry environment (which are already specified in `pyproject.toml`)
    ```bash
    poetry install
    ```

5. Create a .env file in the root directory of the repo with your OpenAI API Key (if you want to avoid having to copy-paste it repeatedly into the Streamlit UI)
    ```py
    OPEN_AI_KEY='yourapikeyhere' #fill in the quotes with your API key
    ```

6. Use the Poetry environment to run the app
    ```bash
    poetry run streamlit run app/main.py
    ```

7. Follow the instructions in the frontend to analyze your videos. Enjoy!


## Testing
A testing suite is included for identifying any problems with your poetry environment upon initialization, and in case you'd like to make any changes to the source. To run tests, you may use:

```bash
poetry run pytest
```

## Contributions
We're committed to the spirit of open-source&mdash;all feedback, including pull requests, is welcome.
