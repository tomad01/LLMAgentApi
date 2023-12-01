import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi import HTTPException

from llm_agent_api.apihelper.constants import TextInput,TaskType
from llm_agent_api.apihelper.logger import log_config
from llm_agent_api.apihelper.pipelines import LLMAgentPipeline,ChatRetrievePipeline,EmailRetrievePipeline
from llm_agent_api.apihelper.settings import CHATS_TXT,QDRANT_CHATS,EMAILS_TXT,QDRANT_EMAILS

dictConfig(log_config)
app = FastAPI(debug=True)
llm_agent_pipeline = LLMAgentPipeline()
chat_retrieve_pipeline = ChatRetrievePipeline(CHATS_TXT,QDRANT_CHATS,TaskType.CHAT)
email_retrieve_pipeline = EmailRetrievePipeline(EMAILS_TXT,QDRANT_EMAILS,TaskType.EMAIL)

@app.get("/")
def status_check() -> dict[str, str]:
    return {
        "status": "I am ALIVE!",
    }

@app.post("/retrieve")
async def retrieve_docs(data: TextInput) -> dict[str, str]:

    # try:
    query = data.query
    query_type = data.query_type
    parameters = data.parameters
    if query_type==TaskType.CHAT:
        docs = chat_retrieve_pipeline.retrieve(query,parameters)
    elif query_type==TaskType.EMAIL:
        docs = email_retrieve_pipeline.retrieve(query,parameters)
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
    parameters = data.parameters
    if query_type==TaskType.CHAT:
        docs = chat_retrieve_pipeline.retrieve(ChatRetrievePipeline.parse(query),
                                               parameters)
    elif query_type==TaskType.EMAIL:
        docs = email_retrieve_pipeline.retrieve(EmailRetrievePipeline.parse(query),
                                                parameters)
    else:
        raise Exception(f"unknown query type {query_type}")
    solution,isok = llm_agent_pipeline.solution(docs)
    
    return {"solution": solution,"isok":str(isok)}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
