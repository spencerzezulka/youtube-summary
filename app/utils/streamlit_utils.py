def double_newlines(input_string: str):
    # Replace single newline characters with double newlines (for Streamlit markdown)
    output_string = input_string.replace('\n', '\n\n')
    return output_string