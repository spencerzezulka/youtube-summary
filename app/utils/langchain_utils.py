from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
import os
import json

basic_summary_prompt = """The following is metadata for a given video, including its transcript. Please summarize it
            concisely in one sentence, and then extract insights. Include timestamps.
            The output should be formatted in markdown, and each insight should be enumerated and should
            begin with a representative emoji."""


def load_examples(file_path: str) -> dict:
    # Load few-shot examples from examples.json
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No JSON found at {file_path}")
    with open(file_path, "r") as file:
        examples = json.load(file)
    return examples


def format_examples_for_prompt_template(examples: dict) -> dict:
    # Convert examples loaded from metadata json to GPT-readable format
    formatted_examples = []
    for example in examples:
        metadata = example["fewshotmapping"]["metadata"]
        summary = example["fewshotmapping"]["summary"]
        formatted_example = {"metadata": str(metadata), "summary": summary}
        formatted_examples.append(formatted_example)
    return formatted_examples


def select_examples(
    formatted_examples: dict, number_examples: str = 1, **kwargs
) -> SemanticSimilarityExampleSelector:
    to_vectorize = [" ".join(example.values()) for example in formatted_examples]
    embeddings = OpenAIEmbeddings(**kwargs)
    vectorstore = Chroma.from_texts(
        to_vectorize, embeddings, metadatas=formatted_examples
    )
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore, k=number_examples
    )
    return example_selector


def generate_summary(metadata: str, **kwargs) -> str:
    # Merge formatted examples into few-shot prompt and feed into LLM
    examplePrompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{metadata}"),
            ("ai", "{summary}"),
        ]
    )

    unformatted_examples = load_examples("app/examples/examples.json")
    formatted_examples = format_examples_for_prompt_template(unformatted_examples)

    api_key = kwargs.get("api_key", None)
    # Check if 'api_key' is not present; if present, pass it to select_examples
    if not api_key:
        raise ValueError("api_key not provided.")
    example_selector = select_examples(formatted_examples, api_key=api_key)

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=examplePrompt,
        example_selector=example_selector,
        input_variables=["metadata"],
    )

    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                basic_summary_prompt
                + """
            The following message records, denoted by "human" and "ai," give examples for how the summary should be formatted.
        """,
            ),
            few_shot_prompt,
            ("human", "{metadata}"),
        ]
    )

    chain = summary_prompt | ChatOpenAI(**kwargs)

    return chain.invoke({"metadata": metadata})
