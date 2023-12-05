from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
import streamlit as st
from typing import Optional
import os
import json

basic_summary_prompt = '''The following is metadata for a given video, including its transcript. Please summarize it
            concisely in one sentence, and then extract insights. Include timestamps.
            The output should be formatted in markdown, and each insight should be enumerated and should
            begin with a representative emoji.'''


def load_examples(file_path: str) -> dict:
    # Load few-shot examples from examples.json
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'No JSON found at {file_path}')
    with open(file_path, 'r') as file:
        examples = json.load(file)
    return examples

def format_examples_for_prompt_template(examples: dict) -> dict:
    formatted_examples = []
    for example in examples:
        metadata = example['fewshotmapping']['metadata']
        summary = example['fewshotmapping']['summary']
        formatted_example = {'metadata': str(metadata), 'summary': summary}
        formatted_examples.append(formatted_example)
    return formatted_examples
    
def generate_summary(metadata: str, **kwargs) -> str:
    examplePrompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{metadata}"),
            ("ai", "{summary}"),
        ]
    )

    unformatted_examples = load_examples('app/examples/examples.json')
    formatted_examples = format_examples_for_prompt_template(unformatted_examples)

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=examplePrompt,
        examples=formatted_examples
    )

    summary_prompt = ChatPromptTemplate.from_messages(
        [('system', basic_summary_prompt + '''
            The following message records, denoted by "human" and "ai," give examples for how the summary should be formatted.
        '''
        ),
            few_shot_prompt,
            ('human', '{metadata}')
        ]
    )
    
    chain = summary_prompt | ChatOpenAI(**kwargs)
    
    return chain.invoke({'metadata': metadata})


