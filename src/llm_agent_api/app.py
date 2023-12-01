import logging
from logging.config import dictConfig
from typing import Tuple 

from fastapi import FastAPI
from fastapi import HTTPException

from llm_agent_api.apihelper.constants import TextInput,TaskType
from llm_agent_api.apihelper.logger import log_config
from llm_agent_api.apihelper.settings import CHATS_TXT,QDRANT_CHATS,EMAILS_TXT,QDRANT_EMAILS
from llm_agent_api.apihelper.pipelines import ChatRetrievePipeline,EmailRetrievePipeline,RetrievalAgent


dictConfig(log_config)
app = FastAPI(debug=True)
chat_retrieve_pipeline = ChatRetrievePipeline(CHATS_TXT,QDRANT_CHATS,TaskType.CHAT)
email_retrieve_pipeline = EmailRetrievePipeline(EMAILS_TXT,QDRANT_EMAILS,TaskType.EMAIL)
retrieval_agent = RetrievalAgent(chat_retrieve_pipeline.qdrant,email_retrieve_pipeline.qdrant)


@app.get("/")
def status_check() -> dict[str, str]:
    return {
        "status": "I am ALIVE!",
    }

@app.post("/retrieve")
async def retrieve_docs(data: TextInput) -> dict[str, list[str]]:
    # try:
    query = data.query
    query_type = data.query_type
    parameters = data.parameters
    if query_type==TaskType.CHAT:
        parsed_query = ChatRetrievePipeline.parse(query)
        docs = chat_retrieve_pipeline.retrieve(parsed_query,parameters)
    elif query_type==TaskType.EMAIL:
        parsed_query = EmailRetrievePipeline.parse(query)
        docs = email_retrieve_pipeline.retrieve(parsed_query,parameters)
    else:
        raise Exception(f"unknown query type {query_type}")
    return {"docs": docs}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_text(data: TextInput) -> dict[str, str]:
    """
    we assume the type of the query is known because usually 
    there are different data sources for emails and chats
    otherwise we need to perform classification with an intent detection model
    """
    # try:
    query = data.query
    query_type = data.query_type    
    if query_type==TaskType.CHAT:
        parsed_query = ChatRetrievePipeline.parse(query)        
    elif query_type==TaskType.EMAIL:
        parsed_query = EmailRetrievePipeline.parse(query)        
    else:
        raise Exception(f"unknown query type {query_type}")    
    
    # for async we should user the "arun" method
    solution = retrieval_agent.run(parsed_query)
    
    return {"solution": solution}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
