
import logging
from typing import Tuple


from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.agents import AgentType, Tool, initialize_agent,load_tools


logger = logging.getLogger(__name__)

# we are using the default model, ada_002
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

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
    def __init__(self,text_path,qdrant_path,collection_name,k=5):
        RetrievePipeline.__init__(self,text_path,qdrant_path,collection_name,k)
    
    @staticmethod
    def parse(text:str)->str:
        # apply some specific chats parsing
        return text


class EmailRetrievePipeline(RetrievePipeline):
    def __init__(self,text_path,qdrant_path,collection_name,k=5):
        RetrievePipeline.__init__(self,text_path,qdrant_path,collection_name,k)
        
    @staticmethod
    def parse(text:str)->str:
        # apply some specific email parsing
        return text
    
class LLMPipeline:
    def __init__(self):                
        logger.info("llm initialised")
        
    def _get_prompt(self,query:str,docs:list[str]):
        joined_docs = "\n\n".join(["'''"+doc+"'''" for doc in docs])
        prompt = "You a senior support assistent with extensive knowledge in the IT field.\n"+\
        "considering the folowing support documents build an answer for the given question that follows after:"+\
        f"\n\n{joined_docs}\n\n"+\
        f"question: {query}\n"+\
        "Hint: Give a detailed and informative answer based on documents. If you don't have enough information "+\
        '''to answer the question you can simply respond: "I don't know"'''                                     
        return prompt
        
    def _check_if_ok(response:str)->bool:
        ## do some parsing
        return True
        
    def solution(self,query,docs:list[str])->Tuple[str,bool]:
        if len(docs)>0:
            prompt = self._get_prompt(query,docs)
            response = llm.invoke(prompt)
            isok = self._check_if_ok(response)
            return response,isok
        return "",False
    
    
class RetrievalAgent:
    def __init__(self,chat_vector_store,email_vector_store):
  
        tools = load_tools(["google-serper"], llm=llm)
        
        chats_retrieve = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=chat_vector_store.as_retriever()
        )                 
        emails_retrieve = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=email_vector_store.as_retriever()
        )              
        tools = tools+[
            Tool(
                name="email data",
                func=emails_retrieve.run,
                description="useful for when you need to answer questions about various it stuff. Input should be a fully formed question.",
            ),
            Tool(
                name="chats data",
                func=chats_retrieve.run,
                description="useful for when you need to answer questions about robots. Input should be a fully formed question.",
            ),            
        ]                
        self.agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
            handle_parsing_errors="Check your output and make sure it conforms!",
        )        
        
    def run(self,query):
        return self.agent.run(query)