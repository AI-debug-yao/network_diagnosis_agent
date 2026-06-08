import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi

load_dotenv()


def get_tongyi_llm(temperature: float = 0.0, model_name: str = "qwen-turbo"):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    
    llm = Tongyi(
        model_name=model_name,
        temperature=temperature,
        dashscope_api_key=api_key
    )
    return llm
