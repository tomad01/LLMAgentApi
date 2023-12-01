
import logging
from typing import Tuple


from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatOpenAI


logger = logging.getLogger(__name__)

# we are using the default model, ada_002
embeddings = OpenAIEmbeddings()


class RetrievePipeline:
    """this looks so ugly because we are using
    a dummy qdrant client based on a locally saved vector db
    in prod pobably we would use a server
    if embeddings are already created then the client loads them from disk"""
    def __init__(self,text_path,qdrant_path,collection_name,k=5):
        loader = TextLoader(text_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)        
        self.qdrant = Qdrant.from_documents(
            docs,
            embeddings,
            path=qdrant_path,
            collection_name=collection_name,
        )       
        logger.info(f"{collection_name} qdrant initialised")
        self.max_results = k
    
    def retrieve(self,query:str,parameters:dict)->list[str]:
        # probably we have to experiment to find out the best settings or search method
        if "score_threshold" in  parameters:
            score_threshold = parameters["score_threshold"]
        else:
            score_threshold = 0.7
        found_docs = self.qdrant.similarity_search_with_score(query, k=self.max_results, score_threshold=score_threshold)
        return [item[0][0].page_content for item in found_docs]

class ChatRetrievePipeline(RetrievePipeline):
    def __init__(self,text_path,qdrant_path,collection_name):
        RetrievePipeline.__init__(text_path,qdrant_path,collection_name)
    
    @staticmethod
    def parse(text:str)->str:
        # apply some specific chats parsing
        return text


class EmailRetrievePipeline(RetrievePipeline):
    def __init__(self,text_path,qdrant_path,collection_name):
        RetrievePipeline.__init__(text_path,qdrant_path,collection_name)
        
    @staticmethod
    def parse(text:str)->str:
        # apply some specific email parsing
        return text
    
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