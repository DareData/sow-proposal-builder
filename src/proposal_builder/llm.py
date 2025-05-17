from openai import AzureOpenAI

def create_llm(settings) -> AzureOpenAI:
    return AzureOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        base_url=settings.AZURE_OPENAI_ENDPOINT + "openai/",
        api_version=settings.AZURE_OPENAI_API_VERSION,
    )