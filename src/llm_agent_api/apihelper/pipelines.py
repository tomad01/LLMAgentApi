import os
import logging
from pathlib import Path
from typing import Tuple
from dotenv import load_dotenv

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatOpenAI


logger = logging.getLogger(__name__)


dotenv_path = Path(os.path.dirname(__file__)).parent / ".env"
load_dotenv(dotenv_path)
# we are using the default model, ada_002
embeddings = OpenAIEmbeddings()

class ChatRetrievePipeline:
    """this looks so ugly because we are using
    a dummy qdrant client based on a locally saved vector db
    in prod pobably we would use a server
    if embeddings are already created then the client loads them from disk"""
    def __init__(self):
        loader = TextLoader(os.environ['CHATS_TXT'])
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)        
        self.qdrant = Qdrant.from_documents(
            docs,
            embeddings,
            path=os.environ["QDRANT_CHATS"],
            collection_name="chats",
        )        
        logger.info("chats qdrant initialised")
        
    def parse(self,text:str)->str:
        # apply some specific chats parsing
        return text
            
    def retrieve(self,query:str)->list[str]:
        found_docs = self.qdrant.max_marginal_relevance_search(query, k=2, fetch_k=2)
        return found_docs

class EmailRetrievePipeline:
    """this looks so ugly because we are using
    a dummy qdrant client based on a locally saved vector db
    in prod pobably we would use a server
    if embeddings are already created then the client loads them from disk"""
    def __init__(self):
        loader = TextLoader(os.environ['EMAILS_TXT'])
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)        
        self.qdrant = Qdrant.from_documents(
            docs,
            embeddings,
            path=os.environ["QDRANT_EMAILS"],
            collection_name="emails",
        )       
        logger.info("emails qdrant initialised")
    def parse(self,text:str)->str:
        # apply some specific email parsing
        return text
    
    def retrieve(self,query:str)->list[str]:
        # probably we have to experiment to find out the best settings or search method
        found_docs = self.qdrant.max_marginal_relevance_search(query, k=2, fetch_k=2)
        return found_docs
    
class LLMAgentPipeline:
    def __init__(self):
        # of course we can parameterize this
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        logger.info("llm initialised")
        
    def _get_prompt(self,docs:list[str]):
        prompt = ""
        return prompt
        
    def _check_if_ok(response:str)->bool:
        ## do some parsing
        return True
        
    def solution(self,docs:list[str])->Tuple[str,bool]:
        if len(docs)>0:
            prompt = self._get_prompt(docs)
            response = self.llm.invoke(prompt)
            isok = self._check_if_ok(response)
            return response,isok
        return "",False