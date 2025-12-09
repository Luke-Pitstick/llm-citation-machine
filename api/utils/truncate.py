# Only sends the first 10000 characters of the text

def split_text(text: str, max_length: int = 10000):
    """
    Split text into chunks of a given length. This is used to avoid giving the LLM to many tokens which helps to optimize costs and speed.
    """
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]


def truncate(text: str, max_length: int = 10000):
    return split_text(text, max_length)[0]