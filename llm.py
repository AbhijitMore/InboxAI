from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Tuple


class LLMProcessor:
    def __init__(self, model: str = "llama3.2:3b-instruct-q8_0"):
        self.model = model
        self.llm = ChatOllama(model=model)
    
    def generate_reply(self, body: str) -> Tuple[str, str]:
        """Generates the subject and body for the reply using the LLM."""
        prompt = PromptTemplate.from_template("""Write a reply to this email with first line as subject and next lines for body: {body}""")
        llm_chain = prompt| self.llm | StrOutputParser()
        result = llm_chain.invoke({'body': body})

        subject, body_reply = result.split('\n')[0], '\n'.join(result.split('\n')[1:])
        return subject, body_reply
