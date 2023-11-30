import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi import HTTPException


from llm_agent_api.apihelper.constants import TextInput
from llm_agent_api.apihelper.logger import log_config
from llm_agent_api.apihelper.settings import env_test


dictConfig(log_config)
app = FastAPI(debug=True)

env_test()


@app.get("/")
def status_check() -> dict[str, str]:
    return {
        "status": "I am ALIVE!",
    }


@app.post("/generate/")
async def generate_text(data: TextInput) -> dict[str, str]:
    try:
        params = data.parameters or {}
        model_out = "todo ..."
        return {"solution": model_out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
