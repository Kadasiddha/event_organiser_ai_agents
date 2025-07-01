import os
def get_open_api_key():
    """
    Retrieves the OpenAI API key from environment variable.
    Ensure that the 'OPEN_API_KEY' environment variable is set.
    """
    api_key = os.getenv("OPEN_API_KEY")
    print('tttttttt    .',api_key,'.' )
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return api_key

def get_openai_api_key():
    """
    Retrieves the OpenAI API key from environment variable.
    Ensure that the 'OPENAI_API_KEY' environment variable is set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return api_key

def get_serper_api_key():
    """
    Retrieves the SERPER API KEY from environment variable.
    Ensure that the 'SERPER_API_KEY' environment variable is set.
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return api_key